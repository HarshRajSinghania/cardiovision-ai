# CardioVision AI - Comprehensive Health Assessment Platform

A Flask-based web application that provides AI-powered cardiovascular health assessments, stroke risk evaluation, medication interaction analysis, and health chat functionality using OpenRouter's DeepSeek AI. Features secure user authentication and personal health record management.

## Features

- **🔐 User Authentication**: Secure login/registration system with password hashing
- **👤 Personal Dashboard**: Individual patient portal with health history overview
- **🫀 Heart Attack Risk Assessment**: Comprehensive evaluation with saved results
- **🧠 Stroke Risk Assessment**: Evidence-based evaluation with personal tracking
- **💊 Medication Analysis**: AI-powered analysis with interaction history
- **🤖 AI Health Chat**: Personalized chat with conversation history
- **📊 Health Records**: Secure storage of all assessments and AI reports
- **📈 Progress Tracking**: Monitor health trends over time

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

You need to set your OpenRouter API key as an environment variable:

**Windows (Command Prompt):**
```cmd
set OPENROUTER_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:OPENROUTER_API_KEY="your_api_key_here"
```

**Linux/Mac:**
```bash
export OPENROUTER_API_KEY="your_api_key_here"
```

### 3. Get OpenRouter API Key

1. Visit [OpenRouter.ai](https://openrouter.ai)
2. Sign up for an account
3. Navigate to the API section
4. Generate an API key
5. Copy the key and set it as the environment variable above

### 4. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Application Structure

```
CardioVision AI/
├── app.py                 # Main Flask application with authentication
├── cardiovision.db        # SQLite database (created automatically)
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── heartattack.py        # Original heart attack assessment (reference)
├── stroke.py             # Original stroke assessment (reference)
└── templates/            # HTML templates
    ├── base.html         # Base template with auth navigation
    ├── landing.html      # Public home page
    ├── login.html        # User login form
    ├── register.html     # User registration form
    ├── dashboard.html    # Personal patient dashboard
    ├── heart_attack.html # Heart attack assessment form
    ├── heart_attack_result.html # Heart attack results
    ├── stroke.html       # Stroke assessment form
    ├── stroke_result.html # Stroke results
    ├── medication_analysis.html # Medication input form
    ├── medication_result.html # Medication analysis results
    └── ai_chat.html      # AI chat interface
```

## Endpoints

### Public Routes
- `/` - Landing page with feature overview
- `/login` - User login page
- `/register` - User registration page

### Protected Routes (Login Required)
- `/dashboard` - Personal patient dashboard
- `/heart-attack` - Heart attack risk assessment
- `/stroke` - Stroke risk assessment  
- `/medication-analysis` - Medication interaction analysis
- `/ai-chat` - AI health chat interface
- `/logout` - User logout

## AI Integration

The application uses OpenRouter's DeepSeek AI model for:

- **Risk Analysis**: Generates detailed health reports based on assessment results
- **Medication Analysis**: Analyzes drug interactions and provides safety recommendations
- **Health Chat**: Provides interactive health guidance and answers medical questions

## Security & Privacy

- **User Authentication**: Secure login system with password hashing using Werkzeug
- **Personal Data Protection**: Each user can only access their own health records
- **Database Security**: SQLite database with user isolation and secure queries
- **Session Management**: Flask-Login handles secure user sessions
- **API Security**: OpenRouter communications secured with API keys
- **Medical Disclaimers**: All AI responses include appropriate medical disclaimers

## Important Disclaimers

⚠️ **This application is for educational purposes only and should not replace professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for medical decisions.**

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your OpenRouter API key is set correctly as an environment variable
2. **Module Not Found**: Run `pip install -r requirements.txt` to install dependencies
3. **Port Already in Use**: Change the port in `app.py` or stop other applications using port 5000

### First Time Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Set OpenRouter API key: `$env:OPENROUTER_API_KEY="your_key"`
3. Run the application: `python app.py`
4. Visit `http://localhost:5000` and create an account
5. The SQLite database will be created automatically

### Support

If you encounter issues:
1. Check that all dependencies are installed
2. Verify your OpenRouter API key is valid and has sufficient credits
3. Ensure you're running Python 3.7 or higher
4. Check that the database file `cardiovision.db` is created and accessible
5. Verify user registration and login functionality

## Database Schema

The application uses SQLite with the following tables:

- **User**: Patient accounts (username, email, password_hash, personal info)
- **HeartAssessment**: Heart attack risk assessment results
- **StrokeAssessment**: Stroke risk assessment results  
- **MedicationAnalysis**: Medication interaction analyses
- **ChatSession**: AI chat conversation history

## Development

To modify the application:

1. **Adding New Assessments**: Create new routes in `app.py`, database models, and templates
2. **Database Changes**: Modify models in `app.py` and recreate database
3. **Authentication**: Use `@login_required` decorator for protected routes
4. **User Data**: Access current user with `current_user` in templates and routes
5. **Styling Changes**: Update the CSS in `templates/base.html`
6. **New Features**: Follow the existing pattern of routes, templates, database storage, and AI integration

## License

This project is for educational and demonstration purposes.
