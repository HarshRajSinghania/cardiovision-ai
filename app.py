from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
import os
from datetime import datetime
import sqlite3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cardiovision.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# OpenRouter API configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')  # Set this environment variable
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    heart_assessments = db.relationship('HeartAssessment', backref='patient', lazy=True)
    stroke_assessments = db.relationship('StrokeAssessment', backref='patient', lazy=True)
    medication_analyses = db.relationship('MedicationAnalysis', backref='patient', lazy=True)
    chat_sessions = db.relationship('ChatSession', backref='patient', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class HeartAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    answers = db.Column(db.Text, nullable=False)  # JSON string
    ai_report = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StrokeAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    answers = db.Column(db.Text, nullable=False)  # JSON string
    ai_report = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MedicationAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medications = db.Column(db.Text, nullable=False)
    ai_analysis = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_ai_response(prompt, system_message="You are a helpful medical AI assistant."):
    """Get response from DeepSeek via OpenRouter"""
    if not OPENROUTER_API_KEY:
        return "Please set your OPENROUTER_API_KEY environment variable to use AI features."
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(OPENROUTER_BASE_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error getting AI response: {str(e)}"

def calculate_heart_attack_risk(answers):
    """Calculate heart attack risk based on answers"""
    factors = {
        "chest_pain": 20,
        "shortness_breath": 15,
        "fatigue": 10,
        "palpitations": 10,
        "dizziness": 10,
        "swelling": 10,
        "nausea": 5,
        "high_bp": 10,
        "high_cholesterol": 10,
        "diabetes": 10,
        "smoking": 10,
        "alcohol": 5,
        "obesity": 10,
        "sedentary": 5,
        "family_history": 5,
        "age": 5,
        "stress": 5
    }
    
    score = 0
    for key, weight in factors.items():
        if answers.get(key) == 'yes':
            score += weight
    
    return min(score, 100)

def calculate_stroke_risk(answers):
    """Calculate stroke risk based on answers"""
    factors = {
        "weakness_numbness": 25,
        "speech_difficulty": 20,
        "vision_problems": 10,
        "balance_issues": 10,
        "severe_headache": 10,
        "high_bp": 15,
        "diabetes": 10,
        "high_cholesterol": 10,
        "irregular_heartbeat": 10,
        "smoking": 10,
        "alcohol": 5,
        "obesity": 10,
        "sedentary": 5,
        "family_history": 5,
        "age": 5,
        "stress": 5
    }
    
    score = 0
    for key, weight in factors.items():
        if answers.get(key) == 'yes':
            score += weight
    
    return min(score, 100)

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date_of_birth = request.form.get('date_of_birth')
        
        # Validation
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=datetime.strptime(date_of_birth, '%Y-%m-%d').date() if date_of_birth else None
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('landing'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Patient dashboard"""
    # Get recent assessments
    recent_heart = HeartAssessment.query.filter_by(user_id=current_user.id).order_by(HeartAssessment.created_at.desc()).limit(5).all()
    recent_stroke = StrokeAssessment.query.filter_by(user_id=current_user.id).order_by(StrokeAssessment.created_at.desc()).limit(5).all()
    recent_medications = MedicationAnalysis.query.filter_by(user_id=current_user.id).order_by(MedicationAnalysis.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         recent_heart=recent_heart,
                         recent_stroke=recent_stroke, 
                         recent_medications=recent_medications)

@app.route('/')
def landing():
    """Landing page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')

@app.route('/heart-attack')
@login_required
def heart_attack():
    """Heart attack risk assessment page"""
    return render_template('heart_attack.html')

@app.route('/heart-attack', methods=['POST'])
@login_required
def heart_attack_assessment():
    """Process heart attack risk assessment"""
    answers = request.form.to_dict()
    score = calculate_heart_attack_risk(answers)
    
    # Generate AI report
    risk_level = "Low" if score < 30 else "Moderate" if score < 60 else "High"
    
    ai_prompt = f"""
    A patient has completed a heart attack risk assessment with a score of {score}/100 ({risk_level} risk).
    
    Their responses indicate:
    {json.dumps(answers, indent=2)}
    
    Please provide:
    1. A detailed analysis of their risk factors
    2. Specific recommendations for lifestyle changes
    3. When they should see a doctor
    4. Emergency signs to watch for
    
    Keep the response professional but accessible to a general audience.
    """
    
    system_message = "You are a medical AI assistant specializing in cardiovascular health. Provide helpful, accurate medical information but always remind users to consult healthcare professionals for medical decisions."
    
    ai_report = get_ai_response(ai_prompt, system_message)
    
    # Save assessment to database
    assessment = HeartAssessment(
        user_id=current_user.id,
        score=score,
        risk_level=risk_level,
        answers=json.dumps(answers),
        ai_report=ai_report
    )
    db.session.add(assessment)
    db.session.commit()
    
    return render_template('heart_attack_result.html', 
                         score=score, 
                         risk_level=risk_level, 
                         ai_report=ai_report,
                         answers=answers,
                         assessment_id=assessment.id)

@app.route('/stroke')
@login_required
def stroke():
    """Stroke risk assessment page"""
    return render_template('stroke.html')

@app.route('/stroke', methods=['POST'])
@login_required
def stroke_assessment():
    """Process stroke risk assessment"""
    answers = request.form.to_dict()
    score = calculate_stroke_risk(answers)
    
    # Generate AI report
    risk_level = "Low" if score < 30 else "Moderate" if score < 60 else "High"
    
    ai_prompt = f"""
    A patient has completed a stroke risk assessment with a score of {score}/100 ({risk_level} risk).
    
    Their responses indicate:
    {json.dumps(answers, indent=2)}
    
    Please provide:
    1. A detailed analysis of their stroke risk factors
    2. Specific recommendations for prevention
    3. When they should seek medical attention
    4. Warning signs of stroke (BE-FAST protocol)
    
    Keep the response professional but accessible to a general audience.
    """
    
    system_message = "You are a medical AI assistant specializing in stroke prevention and neurological health. Provide helpful, accurate medical information but always remind users to consult healthcare professionals for medical decisions."
    
    ai_report = get_ai_response(ai_prompt, system_message)
    
    # Save assessment to database
    assessment = StrokeAssessment(
        user_id=current_user.id,
        score=score,
        risk_level=risk_level,
        answers=json.dumps(answers),
        ai_report=ai_report
    )
    db.session.add(assessment)
    db.session.commit()
    
    return render_template('stroke_result.html', 
                         score=score, 
                         risk_level=risk_level, 
                         ai_report=ai_report,
                         answers=answers,
                         assessment_id=assessment.id)

@app.route('/medication-analysis')
@login_required
def medication_analysis():
    """Medication interaction analysis page"""
    return render_template('medication_analysis.html')

@app.route('/medication-analysis', methods=['POST'])
@login_required
def analyze_medications():
    """Analyze medication interactions"""
    medications = request.form.get('medications', '').strip()
    
    if not medications:
        return render_template('medication_analysis.html', error="Please enter at least one medication.")
    
    ai_prompt = f"""
    Please analyze the following list of medications for potential interactions, side effects, and safety concerns:
    
    Medications: {medications}
    
    Please provide:
    1. Potential drug interactions between these medications
    2. Common side effects for each medication
    3. Any serious warnings or contraindications
    4. Recommendations for monitoring or precautions
    5. Suggestions for timing of doses if relevant
    
    Important: This is for educational purposes only and should not replace professional medical advice.
    """
    
    system_message = "You are a clinical pharmacist AI assistant. Provide detailed medication interaction analysis while emphasizing the importance of consulting healthcare professionals for medication management."
    
    ai_analysis = get_ai_response(ai_prompt, system_message)
    
    # Save analysis to database
    analysis = MedicationAnalysis(
        user_id=current_user.id,
        medications=medications,
        ai_analysis=ai_analysis
    )
    db.session.add(analysis)
    db.session.commit()
    
    return render_template('medication_result.html', 
                         medications=medications, 
                         analysis=ai_analysis,
                         analysis_id=analysis.id)

@app.route('/ai-chat')
@login_required
def ai_chat():
    """AI chat interface"""
    return render_template('ai_chat.html')

@app.route('/ai-chat', methods=['POST'])
@login_required
def chat_with_ai():
    """Handle AI chat messages"""
    user_message = request.json.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Please enter a message'})
    
    # Prepare AI prompt with context
    system_message = f"""You are CardioVision AI, a helpful medical assistant specializing in cardiovascular health, stroke prevention, and general health guidance. 
    
    You are speaking with {current_user.first_name} {current_user.last_name}, a registered patient.
    
    You can help with:
    - Heart health questions
    - Stroke prevention
    - General health and wellness
    - Medication questions (general information only)
    - Lifestyle recommendations
    
    Always remind users that your advice is for educational purposes and they should consult healthcare professionals for medical decisions."""
    
    ai_response = get_ai_response(user_message, system_message)
    
    # Save chat to database
    chat = ChatSession(
        user_id=current_user.id,
        message=user_message,
        response=ai_response
    )
    db.session.add(chat)
    db.session.commit()
    
    return jsonify({'response': ai_response})

@app.route('/clear-chat', methods=['POST'])
@login_required
def clear_chat():
    """Clear chat history"""
    # Delete user's chat sessions from database
    ChatSession.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
