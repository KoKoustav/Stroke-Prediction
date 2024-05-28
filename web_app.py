import numpy as np
import pickle
import streamlit as st

load_model = pickle.load(open('trained_model.sav','rb'))



def preprocess_input(gender, age, hypertension, heart_disease, ever_married, residence_type, glucose_level, bmi, work_type, smoking_status):
    # Convert categorical values to numerical representations
    gender = 1 if str(gender).lower() == 'male' else 0
    hypertension = 1 if str(hypertension).lower() == 'yes' else 0
    heart_disease = 1 if str(heart_disease).lower() == 'yes' else 0
    ever_married = 1 if str(ever_married).lower() == 'yes' else 0
    residence_type = 1 if str(residence_type).lower() == 'urban' else 0

    # Convert input values to float
    glucose_level = float(glucose_level) if str(glucose_level).strip() != '' else 0.0
    bmi = float(bmi) if str(bmi).strip() != '' else 0.0

    work_type_index = ['Neverworked', 'Private', 'Self-employed', 'Govt_job', 'Children'].index(str(work_type))
    smoking_status_index = ['Smokes', 'Formerly smoked', 'Never smoked'].index(str(smoking_status))

    x = np.zeros(14)  # Assuming 13 features, modify if needed

    x[0] = gender
    x[1] = age
    x[2] = hypertension
    x[3] = heart_disease
    x[4] = ever_married
    x[5] = residence_type
    x[6] = glucose_level
    x[7] = bmi

    if work_type_index >= 0:
        x[8 + work_type_index] = 1
    if smoking_status_index >= 0:
        x[13 - len(['Smokes', 'Formerly smoked', 'Never smoked']) + smoking_status_index] = 1

    return x

def stroke_prediction(input_values):
    prediction = load_model.predict([input_values])

    if prediction[0] == 1:
        return "Have stroked probability in future. Based on the input information, the prediction indicates a potential risk of stroke. It's essential to consult with a healthcare professional for a thorough evaluation and personalized advice. Early detection and appropriate measures can significantly impact health outcomes. Please seek medical attention to discuss this prediction further."
    else:
        return "Don't have stroked probability in future. According to the prediction based on the provided information, there is currently no indication of a risk for stroke. However, it's important to remember that this is a predictive model and not a substitute for professional medical advice. Regular check-ups and a healthy lifestyle contribute to overall well-being. If you have any concerns or experience changes in your health, it's advisable to consult with a healthcare professional."

def main():
    st.title("Stroke Prediction Web App")

    gender = st.selectbox("Enter your gender", options=['Male', 'Female'])
    age = st.text_input("Enter your age")
    hypertension = st.selectbox("Do you have hypertension?", options=['Yes', 'No'])
    heart_disease = st.selectbox("Do you have heart disease?", options=['Yes', 'No'])
    ever_married = st.selectbox("Are you married?", options=['Yes', 'No'])
    residence_type = st.selectbox("What is your Residence type?", options=['Urban', 'Rural'])
    glucose_level = st.text_input("What is your glucose level? (If you don't know, put 0 as value)")
    bmi = st.text_input("What is your BMI level? (If you don't know, put 0 as value)")
    work_type = st.selectbox("What is your work type?", options=['Neverworked', 'Private', 'Self-employed', 'Govt_job', 'Children'])
    smoking_status = st.selectbox("Do you smoke?", options=['Smokes', 'Formerly smoked', 'Never smoked'])

    hypertension = 1 if hypertension == 'Yes' else 0
    heart_disease = 1 if heart_disease == 'Yes' else 0
    ever_married = 1 if ever_married == 'Yes' else 0   
    gender = 1 if gender == 'Male' else 0   
    residence_type = 1 if residence_type == 'Urban' else 0

    stroke = ''

    if st.button("Stroke Risk Result"):
        input_values = preprocess_input(gender, age, hypertension, heart_disease, ever_married, residence_type, glucose_level, bmi, work_type, smoking_status)
        stroke = stroke_prediction(input_values)

    st.success(stroke)

if __name__ == '__main__':
    main()

