import streamlit as st
import pandas as pd
import joblib

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Telecom Churn Prediction Dashboard",
    page_icon="📞",
    layout="wide"
)

# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load("model.pkl")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Prediction Dashboard",
        "About Project"
    ]
)

# =====================================================
# ABOUT PAGE
# =====================================================

if page == "About Project":

    st.title("ℹ️ About This Project")

    st.markdown("""
    ## Telecom Customer Churn Prediction System

    This project predicts whether a telecom customer is likely to churn using Machine Learning techniques.

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

    MSc Computing Project
    """)

# =====================================================
# DASHBOARD PAGE
# =====================================================

else:

    st.title("📞 Telecom Customer Churn Prediction Dashboard")

    st.info(
        "This system predicts customer churn risk using a trained Random Forest Machine Learning model."
    )

    # KPI Cards

    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Model", "Random Forest")
    k2.metric("Accuracy", "92.54%")
    k3.metric("Dataset Size", "667")
    k4.metric("Features", "19")

    st.markdown("---")

    # Input Tabs

    tab1, tab2 = st.tabs(
        ["👤 Customer Profile", "📞 Usage Statistics"]
    )

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
                "Voicemail Messages",
                0,
                60,
                0
            )

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

    st.markdown("---")

    if st.button("🔍 Predict Customer Churn", use_container_width=True):

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

        st.subheader("📈 Prediction Results")

        st.progress(min(int(churn_prob), 100))

        c1, c2 = st.columns(2)

        c1.metric(
            "Churn Probability",
            f"{churn_prob:.2f}%"
        )

        c2.metric(
            "Stay Probability",
            f"{stay_prob:.2f}%"
        )

        if churn_prob < 30:
            st.success("🟢 Low Risk Customer")

        elif churn_prob < 70:
            st.warning("🟡 Medium Risk Customer")

        else:
            st.error("🔴 High Risk Customer")

        # Recommendations

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

        # Customer Snapshot

        st.subheader("📋 Customer Snapshot")

        s1, s2, s3, s4 = st.columns(4)

        s1.metric("Account Length", account_length)
        s2.metric("Area Code", area_code)
        s3.metric("Day Minutes", total_day_minutes)
        s4.metric("Service Calls", customer_service_calls)

        # Usage Analysis

        chart_df = pd.DataFrame(
            {
                "Minutes": [
                    total_day_minutes,
                    total_eve_minutes,
                    total_night_minutes,
                    total_intl_minutes
                ]
            },
            index=[
                "Day",
                "Evening",
                "Night",
                "International"
            ]
        )

        st.subheader("📊 Usage Analysis")

        st.bar_chart(chart_df)

        # AI Insights

        st.subheader("🤖 AI Insights")

        if customer_service_calls > 3:
            st.warning(
                "High number of customer service calls detected."
            )

        if total_day_minutes > 250:
            st.info(
                "Heavy daytime usage pattern detected."
            )

        if international_plan == 1:
            st.info(
                "Customer subscribes to an international plan."
            )

        # Download Report

        result_df = pd.DataFrame({
            "Prediction": [
                "Churn" if prediction == 1 else "Stay"
            ],
            "Churn Probability (%)": [
                round(churn_prob, 2)
            ],
            "Stay Probability (%)": [
                round(stay_prob, 2)
            ]
        })

        csv = result_df.to_csv(index=False)

        st.download_button(
            label="📥 Download Prediction Report",
            data=csv,
            file_name="prediction_report.csv",
            mime="text/csv"
        )

    st.markdown("---")

    st.caption(
        "Telecom Customer Churn Prediction System | MSc Computing Project | Dasun Jayaweera"
    )
