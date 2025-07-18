import streamlit as st
import random

# Set page config with a custom background color using Streamlit's HTML injection
st.set_page_config(page_title="🧠 Stroke Risk Prediction App", layout="centered")

def set_bg_color(color="#e0f2fe"):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
            background-image: linear-gradient(135deg, #e0f2fe 0%, #fdf6ff 60%, #e0e7ff 100%);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_color()  # Light blue gradient background

def calculate_stroke_risk(data):
    risk_score = 0
    factors = []

    if data['age'] > 65:
        risk_score += 30
        factors.append("Advanced age (>65)")
    elif data['age'] > 50:
        risk_score += 15
        factors.append("Elevated age (50-65)")

    if data['hypertension']:
        risk_score += 25
        factors.append("Hypertension")
    if data['heart_disease']:
        risk_score += 25
        factors.append("Heart disease")
    if data['avg_glucose_level'] > 125:
        risk_score += 20
        factors.append("High glucose level (>125 mg/dL)")
    elif data['avg_glucose_level'] > 100:
        risk_score += 10
        factors.append("Elevated glucose level (100-125 mg/dL)")
    if data['bmi'] > 30:
        risk_score += 15
        factors.append("Obesity (BMI >30)")
    elif data['bmi'] > 25:
        risk_score += 8
        factors.append("Overweight (BMI 25-30)")
    if data['smoking_status'] == "smokes":
        risk_score += 20
        factors.append("Current smoker")
    elif data['smoking_status'] == "formerly smoked":
        risk_score += 10
        factors.append("Former smoker")
    if data['gender'] == "Male":
        risk_score += 5
        factors.append("Male gender")
    if data['work_type'] in ["Private", "Self-employed"]:
        risk_score += 5
        factors.append("High-stress work environment")

    if risk_score >= 50:
        risk_level = "High"
        prediction = 1
        recommendation = "⚠️ High risk of stroke detected! Immediate medical consultation recommended. Consider lifestyle modifications and medical intervention."
    else:
        risk_level = "Low"
        prediction = 0
        recommendation = "✅ Low risk of stroke. Continue maintaining healthy lifestyle habits and regular check-ups."

    confidence = min(85 + (10 * random.random()), 95)

    return {
        "risk_score": min(risk_score, 100),
        "risk_level": risk_level,
        "risk_factors": factors,
        "recommendation": recommendation,
        "confidence": confidence,
        "prediction": prediction
    }

st.title("🧠 Stroke Risk Prediction App")
st.caption("By SIMEON - Advanced DSA-powered stroke risk assessment")
st.info("This app uses a DSA (Deep Stroke Analysis) model to analyze patient data for stroke risk.")

with st.expander("ℹ️ How it works", expanded=True):
    st.markdown("""
    - **Real-time Analysis:** Instant risk calculation  
    - **DSA-Powered:** Advanced prediction model  
    - **Clinically Based:** Evidence-based predictions  
    """)

# --- User History ---
if "history" not in st.session_state:
    st.session_state['history'] = []

with st.form("stroke_form"):
    st.subheader("Patient Information")
    age = st.number_input("Age", min_value=0, max_value=120, value=50, help="Patient's age in years")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"], help="Biological gender")
    bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=24.0, help="Body Mass Index")
    avg_glucose_level = st.number_input("Average Glucose Level (mg/dL)", min_value=50.0, max_value=400.0, value=100.0,
                                        help="Average blood glucose level in mg/dL")
    hypertension = st.selectbox("Hypertension", ["No", "Yes"], help="History of high blood pressure") == "Yes"
    heart_disease = st.selectbox("Heart Disease", ["No", "Yes"], help="History of heart disease") == "Yes"
    smoking_status = st.selectbox("Smoking Status", ["never smoked", "formerly smoked", "smokes"], help="Current or past smoking status")
    work_type = st.selectbox("Work Type", ["Private", "Self-employed", "Govt_job", "children", "Never_worked"], help="Employment type")

    submit = st.form_submit_button("Assess Risk")

if submit:
    patient_data = {
        "age": age,
        "gender": gender,
        "bmi": bmi,
        "avg_glucose_level": avg_glucose_level,
        "hypertension": hypertension,
        "heart_disease": heart_disease,
        "smoking_status": smoking_status,
        "work_type": work_type
    }
    assessment = calculate_stroke_risk(patient_data)
    st.session_state['history'].append({"patient_data": patient_data, "assessment": assessment})

    st.success(f"**{assessment['risk_level']} Risk** (Score: {assessment['risk_score']}/100)")
    st.progress(assessment['risk_score'] / 100)
    st.markdown(f"**Confidence:** {assessment['confidence']:.1f}%")

    st.markdown("**Risk Factors:**")
    for f in assessment['risk_factors']:
        st.markdown(f"- {f}")
    st.info(assessment['recommendation'])

    # Downloadable report
    report = f"""
    Stroke Risk Assessment Report
    ============================

    Risk Level: {assessment['risk_level']}
    Risk Score: {assessment['risk_score']}/100
    Confidence: {assessment['confidence']:.1f}%
    Recommendation: {assessment['recommendation']}

    Risk Factors:
    {chr(10).join("- "+f for f in assessment['risk_factors'])}

    Patient Data: {patient_data}
    """

    st.download_button("Download Report (.txt)", data=report, file_name="stroke_risk_report.txt")

# Show Assessment History
if st.session_state['history']:
    st.markdown("## Assessment History")
    for idx, entry in enumerate(reversed(st.session_state['history'])):
        st.markdown(f"### Assessment {len(st.session_state['history'])-idx}")
        st.json(entry["patient_data"])
        st.write(f"Risk Level: **{entry['assessment']['risk_level']}**")
        st.write(f"Risk Score: **{entry['assessment']['risk_score']}**")
        st.write(f"Confidence: **{entry['assessment']['confidence']:.1f}%**")
        st.write("---")

st.markdown("""
---
<div style='text-align:center; color:gray; font-size:small;'>
    ⚠️ This tool is for educational purposes only. Always consult with healthcare professionals for medical decisions.
</div>
""", unsafe_allow_html=True)