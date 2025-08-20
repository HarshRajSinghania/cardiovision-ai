# Research: AI-Driven Early Cardiovascular Event Risk Stratification in Primary Care

## 1) Problem Statement (Existing Biology/Healthcare Problem)
- Cardiovascular diseases (CVD) are the leading global cause of death, with many first events (heart attack/stroke) occurring without prior diagnosis.
- Primary care settings often lack rapid, precise risk triage tools that combine multi-modal patient data beyond traditional scores (e.g., Framingham/ASCVD), leading to under- or over-referral.
- Early, proactive identification is critical to reduce mortality, improve outcomes, and lower system burden.

## 2) Why This Matters (Biology + Public Health Context)
- Atherosclerosis progresses silently via endothelial dysfunction, inflammation, plaque formation, and rupture.
- Risk is multifactorial: genetics, lipids, blood pressure, glycemic control, lifestyle, environmental exposures, and social determinants.
- Traditional scores are population-averaged and can miss high-risk individuals in diverse cohorts.

## 3) Opportunity for Innovation (Merging Biology with Technology)
- Use AI to integrate heterogeneous signals—EHR data, vitals, labs, ECG, symptoms, lifestyle—and produce individualized, explainable risk predictions for near-term events (e.g., 90-day, 1-year risk).
- Embed mechanistic biological knowledge (e.g., inflammation, endothelial dysfunction proxies) via engineered biomarkers and representation learning.
- Deliver actionable, clinician-friendly insights at the point of care, with patient-facing education to drive adherence.

## 4) Related Work & Gaps
- Existing tools: ASCVD, Framingham, QRISK—use limited variables, lower precision in underrepresented groups.
- ML papers show gains using ECG signals, imaging, and labs, but are often siloed, not real-time, or not explainable at the visit-level.
- Gaps: Limited external validation, fairness across demographics, and integration into clinical workflow with feedback loops.

## 5) Proposed Solution: CardioVision AI
- Multi-modal risk stratification model for imminent CVD events (MI and ischemic stroke) tailored to primary care.
- Inputs (available in primary care): demographics, vitals, labs (lipids, HbA1c), medications, PMH, symptoms, single-lead or 12-lead ECG features, lifestyle, and SDOH proxies.
- Outputs: calibrated risk scores (90-day/1-year), key drivers (SHAP/explanations), guideline-linked recommendations, and alerts for red-flag phenotypes.

## 6) Biology-Informed Feature Design
- Inflammation proxies: hs-CRP (if available), WBC differential; chronic inflammation flags.
- Endothelial dysfunction: BP variability, hypertension duration, albuminuria (if available).
- Lipid/atherogenic indices: non-HDL, TG/HDL ratio, ApoB (if available).
- Glycemic burden: HbA1c trajectory, fasting glucose variability.
- Arrhythmia/ischemia surrogates: ECG-derived features (PR/QRS/QT intervals, ST-T changes, HRV metrics where possible).
- Lifestyle/SDOH: smoking status, BMI/waist, activity, diet proxies, deprivation index (if permissible), medication adherence.

## 7) Data & Datasets
- Phase 1: Public or synthetic EHR-like datasets (e.g., MIMIC-IV for prototyping concepts; careful with ICU bias), open ECG datasets (e.g., PTB-XL) for feature pretraining, and WHO/CDC statistics for priors.
- Phase 2: Local clinical partner de-identified primary care dataset (with DUA/IRB). If unavailable, federated learning pilot with participating clinics.
- Data governance: HIPAA/GDPR compliance, PHI handling, consent model (broad/waiver as applicable), robust de-identification.

## 8) Modeling Approach
- Structured data: Gradient boosting (XGBoost/LightGBM) baseline for tabular features.
- Time-aware features: simple RNN/Transformer or time-aggregation for longitudinal labs/vitals.
- ECG features: pretrained 1D-CNN embedding extraction; combine with tabular via late fusion.
- Calibration: Platt/Isotonic. Thresholds tuned for sensitivity in safety-first mode.
- Explainability: SHAP for globals/locals; counterfactual suggestions for modifiable risks.

## 9) Evaluation Plan
- Splits: patient-level train/val/test; external validation site if possible.
- Metrics: AUROC, AUPRC, Sensitivity @ fixed FPR, Calibration (ECE), NRI vs ASCVD, decision-curve analysis.
- Fairness: subgroup metrics by sex, age bands, ethnicity, deprivation; mitigate via reweighting/thresholding.
- Prospective shadow testing: clinician-in-the-loop assessment for actionability and alarm fatigue.

## 10) Clinical Workflow Integration
- Simple web dashboard/API for primary care workflow with role-based access.
- Risk score + top contributors + recommended next steps: repeat labs, intensified statin, ambulatory BP, lifestyle referral.
- Patient-facing summary: plain-language risk and behavioral nudges.

## 11) Safety, Ethics, and Bias Mitigation
- Transparency: model cards, dataset documentation.
- Guardrails: never replace clinical judgment; surfaces uncertainty and contraindication warnings.
- Bias monitoring: periodic drift and equity audits; retraining with feedback.
- Security: encryption at rest/in transit; audit logging; least-privilege access.

## 12) Feasibility for Hackathon
- Scope MVP: ingest basic demographics, vitals, a few labs, and simple ECG-derived features if available.
- Implement baseline GBDT with SHAP explanations, calibrated risk score, and a minimal Flask UI (already aligned with this repo).
- Synthetic demo data for privacy-safe showcase.

## 13) Tentative Timeline (Hackathon)
- Day 1: Problem framing, data schema, baseline model, SHAP.
- Day 2: Calibration, fairness slices, Flask UI integration, demo dataset.
- Day 3: Usability polish, documentation, demo script, ablation vs ASCVD baseline.

## 14) Expected Impact
- Earlier detection and targeted prevention in primary care.
- Reduced unnecessary referrals and missed high-risk patients.
- Scalable, explainable AI that augments clinicians and empowers patients.

## 15) Deliverables
- Trained baseline model + inference API.
- Demo web app with risk score and explanations.
- Documentation: model card, data sheet, ethics/bias statement.
- Slide/demo script with case studies.
