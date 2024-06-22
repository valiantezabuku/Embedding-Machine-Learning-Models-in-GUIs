import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


# Set page configuration
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="🔮",
    layout="wide"
)

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status,username = authenticator.login(location='sidebar')


if st.session_state['authentication_status']:
    authenticator.logout(location='sidebar')


    # Add a header to the app
    st.markdown("# 🚀 Welcome to Customer Churn Prediction App!")


    # Add CSS for animation
    st.write("""
        <style>
            @keyframes zoom-in {
                0% {
                    transform: scale(0);
                }
                100% {
                    transform: scale(1);
                }
            }
            .zoom-in-animation {
                animation: zoom-in 1.5s ease-in-out;
            }
        </style>
    """, unsafe_allow_html=True)

    # Add an animated text
    st.write('<div class="zoom-in-animation"><h3>Unleash the power of machine learning to predict customer churn!</h3></div>', unsafe_allow_html=True)


    # Home Page Content
    st.markdown("## About This App")
    st.markdown("""
        The Customer Churn Prediction App is designed to help businesses in the telecommunications industry predict whether a customer is likely to churn (leave the service). By leveraging machine learning techniques, this app provides valuable insights into customer behavior, allowing companies to take proactive measures to improve customer retention.
        """)

    st.markdown("## Key Features")
    st.markdown("""
        - **Data Exploration:** Explore and visualize customer data to identify key patterns and trends that influence churn.
        - **Model Training:** Train various machine learning models, such as Logistic Regression, Random Forest, and XGBoost, to predict customer churn.
        - **Model Evaluation:** Evaluate model performance using metrics like accuracy, precision, recall, and F1-score, and visualize results using ROC curves.
        - **Feature Importance:** Analyze feature importances to understand the drivers of customer churn.
        - **User-Friendly Interface:** Interact with the app through an intuitive and engaging user interface.
        """)

    st.markdown("## How It Works")
    st.markdown("""
        1. **Data Collection:** Gather customer data from various sources.
        2. **Data Preprocessing:** Clean and preprocess the data for model training.
        3. **Model Training:** Train multiple machine learning models to predict churn.
        4. **Model Evaluation:** Evaluate model performance using various metrics.
        5. **Deployment:** Deploy the best-performing model to make real-time predictions.
        """)

    st.markdown("## Benefits")
    st.markdown("""
        - **Improve Customer Retention:** Identify at-risk customers and take proactive measures to retain them.
        - **Optimize Marketing Strategies:** Tailor marketing efforts to target customers who are likely to churn.
        - **Enhance Business Performance:** Reduce churn rates and increase customer lifetime value.
        """)

    # Footer
    st.markdown("""
        ---
        © 2024 Customer Churn Prediction Project. All rights reserved.
    """)


elif st.session_state['authentication_status'] is False:
    st.error('Wrong username/password')
elif st.session_state['authentication_status'] is None:
    st.info('Login to get access to the app')
    st.code("""
    Test Account
    Username: valiant
    Password: 123456
    """)

st.write(st.session_state)

