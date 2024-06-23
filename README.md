# Building a Streamlit Web Application for Customer Churn Prediction

## 📚 Table of Contents

1. [Introduction](#-introduction)
2. [Project Overview](#-project-overview)
   - [The Importance of Customer Churn Prediction](#the-importance-of-customer-churn-prediction)
   - [Machine Learning Models](#machine-learning-models)
   - [Dataset and Model](#dataset-and-model)
3. [Streamlit Web Application](#-streamlit-web-application)
   - [Home Page](#home-page)
   - [Data Page](#data-page)
   - [Visualize Page](#visualize-page)
   - [Predict Page](#predict-page)
   - [History Page](#history-page)
4. [Conclusion](#-conclusion)
5. [Authors](#-authors)
6. [Show your support](#-show-your-support)
7. [Acknowledgments](#-acknowledgments)
8. [License](#-license)


## 📄 Introduction

Customer churn is a significant concern for many large companies, especially in the telecommunications sector. Churn directly impacts revenue, making it crucial for businesses to predict and mitigate it effectively. In this project, I developed a web application using Streamlit that predicts customer churn based on various features. This application provides an intuitive interface for exploring data, visualizing trends, and making predictions using machine learning models.

---

## 🏗️ Project Overview

### The Importance of Customer Churn Prediction

Customer churn prediction is vital for businesses aiming to improve customer retention and optimize marketing strategies. By identifying at-risk customers, companies can take proactive measures to retain them, ultimately enhancing business performance and increasing customer lifetime value.

### Machine Learning Models

The best-performing models, Logistic Regression and AdaBoost, from my analysis were deployed in this Streamlit web application to make these predictions accessible and actionable for business users. These models were evaluated based on various metrics, such as accuracy, precision, recall, and F1-score. The best-performing models were then selected for deployment in the Streamlit web application.

### Dataset and Model

The dataset used contains customer information, including demographics, account information, and services subscribed. The primary task was to build a model to predict whether a customer would churn (leave the service) or not. I followed the CRISP-DM framework for this project, involving data cleaning, exploration, feature engineering, model training, and evaluation.

---

## 💻 Streamlit Web Application

To create an interactive and user-friendly interface for the churn prediction models, I built a Streamlit web application. The application is structured into several pages: Home, Data, Visualize, Predict, and History, with Home being the main page. Below, I provide an overview of each page and its functionality.

### 🏠 Home Page

The Home page serves as an introduction to the application. It provides an overview of the project, explaining the importance of churn prediction and how the application can help users understand and predict customer churn. The page sets the context and guides users on how to navigate through the app.

### 📊 Data Page

The Data page allows users to explore the dataset used for building the churn prediction model. Users can view the dataset, filter it based on specific criteria, and gain insights into the data distribution. This page helps users familiarize themselves with the data and understand the various features involved in the prediction.

### 📈 DashBoard Page

The Visualize page enables users to create visualizations to explore relationships and trends in the data. For instance, users can visualize the distribution of customers across different tenures, payment methods, or monthly charges. This helps identify patterns and correlations that may influence customer churn.

### 🔍 Predict Page

The Predict page allows users to input customer data and receive churn predictions from the machine learning model. Users can input data manually through forms or upload a CSV file for batch predictions. This page provides a user-friendly interface for making real-time predictions, displaying whether a customer is likely to churn and the associated probability.

### 📜 History Page

The History page displays a record of all predictions made by the user. It includes the input data and the corresponding predictions, providing a reference for analysis and tracking. This feature is useful for monitoring trends and reviewing past predictions.

---

## 🔚 Conclusion

By developing this Streamlit web application, I have made customer churn prediction accessible and actionable for business users. The application provides an intuitive interface for exploring data, visualizing trends, and making predictions using machine learning models. This project demonstrates the power of integrating data science and web development to solve real-world business problems.


#### 👥 Authors

**Owner:** Adiru Valiant Ezabuku

Email: vezabuku09@gmail.com

Linkedin Account: [Linkedin](https://www.linkedin.com/in/valiant-ezabuku/)

**Contributors**

Gabriel Okundaye

Brain Kimagut

#### ⭐️ Show your support

If you like this project kindly show some love, give it a 🌟 **STAR** 🌟

#### 🙏 Acknowledgments

I extend my heartfelt thanks to all my tutors at Azubi Africa and my dedicated team members for their guidance, support, and hard work throughout this project. Their expertise, insights, and collaboration significantly contributed to shaping the analysis and outcomes.

#### 📝 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

