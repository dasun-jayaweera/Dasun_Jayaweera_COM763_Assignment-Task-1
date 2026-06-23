import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ==========================================

# PAGE CONFIG

# ==========================================

st.set_page_config(
page_title="Telecom Churn Prediction Dashboard",
page_icon="📞",
layout="wide"
)

# ==========================================

# LOAD MODEL

# ==========================================

model = joblib.load("telecom_churn_model.pkl")

# ==========================================

# SIDEBAR

# ==========================================

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
"Select Page",
[
"Prediction Dashboard",
"About Project"
]
)

# ==========================================

# ABOUT PAGE

# ==========================================

if page == "About Project":
    st.title("ℹ️ About This Project")
    
    st.markdown("""
    ## Telecom Customer Churn Prediction System
    
    This project predicts whether a telecom customer is likely to leave
    the service provider using Machine Learning techniques.
    
    ### Dataset
    Telecom Churn Dataset (BigML)
    
    ### Algorithms Evaluated
    - Decision Tree
    - Random Forest
    - Support Vector Machine
    - Naive Bayes
    - K-Nearest Neighbors
    
    ### Selected Model
    Random Forest Classifier
    
    ### Model Performance
    - Accuracy: 92.54%
    - Precision: 93.13%
    - Recall: 92.54%
    - F1 Score: 91.36%
    
    ### Developed By
    Dasun Jayaweera
    
    MSc Computing
    """)

# ==========================================

# PREDICTION DASHBOARD

# ==========================================

else:
    st.title("📞 Telecom Customer Churn Prediction Dashboard")
    
    st.write(
        "Predict whether a telecom customer is likely to churn using a trained Random Forest Machine Learning model."
    )
    
    # ==========================================
    # KPI CARDS
    # ==========================================
    
    kpi1, kpi2, kpi3 = st.columns(3)
    
    kpi1.metric(
        label="Model",
        value="Random Forest"
    )
    
    kpi2.metric(
        label="Accuracy",
        value="92.54%"
    )
    
    kpi3.metric(
        label="Dataset Records",
        value="667"
    )
    
    st.markdown("---")
    
    # ==========================================
    # TABS
    # ==========================================
    
    tab1, tab2 = st.tabs(
        [
            "👤 Customer Profile",
            "📞 Usage Statistics"
        ]
    )
    
    # ------------------------------------------
    # CUSTOMER PROFILE
    # ------------------------------------------
    
    with tab1:
    
        col1, col2 = st.columns(2)
    
        with col1:
    
            state = st.slider(
                "State (Encoded)",
                0,
                50,
                10
            )
    
            account_length = st.slider(
                "Account Length",
                1,
                250,
                100
            )
    
            area_code = st.selectbox(
                "Area Code",
                [408, 415, 510]
            )
    
        with col2:
    
            international_plan = st.selectbox(
                "International Plan",
                ["No", "Yes"]
            )
    
            voice_mail_plan = st.selectbox(
                "Voice Mail Plan",
                ["No", "Yes"]
            )
    
            number_vmail_messages = st.slider(
                "Number of Voicemail Messages",
                0,
                60,
                0
            )
    
    # ------------------------------------------
    # USAGE STATISTICS
    # ------------------------------------------
    
    with tab2:
    
        col1, col2 = st.columns(2)
    
        with col1:
    
            total_day_minutes = st.number_input(
                "Total Day Minutes",
                value=180.0
            )
    
            total_day_calls = st.number_input(
                "Total Day Calls",
                value=100
            )
    
            total_day_charge = st.number_input(
                "Total Day Charge",
                value=30.0
            )
    
            total_eve_minutes = st.number_input(
                "Total Evening Minutes",
                value=200.0
            )
    
            total_eve_calls = st.number_input(
                "Total Evening Calls",
                value=100
            )
    
            total_eve_charge = st.number_input(
                "Total Evening Charge",
                value=17.0
            )
    
        with col2:
    
            total_night_minutes = st.number_input(
                "Total Night Minutes",
                value=200.0
            )
    
            total_night_calls = st.number_input(
                "Total Night Calls",
                value=100
            )
    
            total_night_charge = st.number_input(
                "Total Night Charge",
                value=9.0
            )
    
            total_intl_minutes = st.number_input(
                "Total International Minutes",
                value=10.0
            )
    
            total_intl_calls = st.number_input(
                "Total International Calls",
                value=4
            )
    
            total_intl_charge = st.number_input(
                "Total International Charge",
                value=2.7
            )
    
            customer_service_calls = st.slider(
                "Customer Service Calls",
                0,
                10,
                1
            )
    
    # ==========================================
    # PREDICTION BUTTON
    # ==========================================
    
    if st.button("🔍 Predict Customer Churn"):
    
        international_plan = 1 if international_plan == "Yes" else 0
        voice_mail_plan = 1 if voice_mail_plan == "Yes" else 0
    
        input_data = pd.DataFrame([[
            state,
            account_length,
            area_code,
            international_plan,
            voice_mail_plan,
            number_vmail_messages,
            total_day_minutes,
            total_day_calls,
            total_day_charge,
            total_eve_minutes,
            total_eve_calls,
            total_eve_charge,
            total_night_minutes,
            total_night_calls,
            total_night_charge,
            total_intl_minutes,
            total_intl_calls,
            total_intl_charge,
            customer_service_calls
        ]], columns=[
            'State',
            'Account length',
            'Area code',
            'International plan',
            'Voice mail plan',
            'Number vmail messages',
            'Total day minutes',
            'Total day calls',
            'Total day charge',
            'Total eve minutes',
            'Total eve calls',
            'Total eve charge',
            'Total night minutes',
            'Total night calls',
            'Total night charge',
            'Total intl minutes',
            'Total intl calls',
            'Total intl charge',
            'Customer service calls'
        ])
    
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0]
    
        churn_prob = probability[1] * 100
        stay_prob = probability[0] * 100
    
        st.markdown("---")
    
        st.subheader("📈 Prediction Result")
    
        st.progress(int(churn_prob))
    
        col1, col2 = st.columns(2)
    
        col1.metric(
            "Churn Probability",
            f"{churn_prob:.2f}%"
        )
    
        col2.metric(
            "Stay Probability",
            f"{stay_prob:.2f}%"
        )
    
        if churn_prob < 30:
    
            st.success("🟢 Low Risk Customer")
    
        elif churn_prob < 70:
    
            st.warning("🟡 Medium Risk Customer")
    
        else:
    
            st.error("🔴 High Risk Customer")
    
        # --------------------------------------
        # Recommendations
        # --------------------------------------
    
        st.subheader("💡 Recommended Actions")
    
        if churn_prob >= 70:
    
            st.markdown("""
            - Offer customer retention discounts
            - Contact customer directly
            - Review service complaints
            - Provide premium support
            """)
    
        elif churn_prob >= 30:
    
            st.markdown("""
            - Send promotional offers
            - Monitor customer engagement
            - Recommend additional services
            """)
    
        else:
    
            st.markdown("""
            - Maintain customer relationship
            - Continue engagement campaigns
            - Offer loyalty rewards
            """)
    
        # --------------------------------------
        # Customer Summary
        # --------------------------------------
    
        st.subheader("📋 Customer Summary")
    
        summary = pd.DataFrame({
            "Feature": [
                "Account Length",
                "Area Code",
                "Day Minutes",
                "Customer Service Calls"
            ],
            "Value": [
                account_length,
                area_code,
                total_day_minutes,
                customer_service_calls
            ]
        })
    
        st.dataframe(
            summary,
            use_container_width=True
        )
    
    st.markdown("---")
    st.caption(
        "Telecom Customer Churn Prediction System | MSc Computing Project | Dasun Jayaweera"
)
