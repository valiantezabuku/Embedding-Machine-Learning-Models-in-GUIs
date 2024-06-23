import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import warnings
warnings.filterwarnings('ignore')


# Set page configuration
st.set_page_config(page_title="Dashboard", page_icon="📈",  layout="wide")

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

    # 1. Add CSS for title styling and zoom-in animation
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
                animation: zoom-in 3s ease-in-out;
            }
            .dashboard-title {
                font-size: 48px;
                font-weight: bold;
                color: #4b8bbe; /* Light blue */
                text-shadow: 2px 2px #d3e3f1; /* Subtle shadow for a 3D effect */
                margin-bottom: 10px;
                position: relative;
                display: inline-block;
            }
            .dashboard-title::before {
                content: "📊"; /* Adding an icon before the title */
                font-size: 48px;
                margin-right: 10px;
            }
            .dashboard-title::after {
                content: "";
                position: absolute;
                width: 100%;
                left: 0;
                bottom: -5px; /* Adjust this value as needed */
                border-bottom: 4px solid #4b8bbe;
            }
        </style>
    """, unsafe_allow_html=True)

    # Dashboard title
    st.title("Customer Churn Dashboard")          

    col1, col2 = st.columns(2)
    with col1:
        pass
    with col2:
        st.selectbox('Select the type of dashboard', options=['EDA', 'KPI'], key='selected_dashboard_type')


    # 2. Load your dataset
    data = pd.read_csv('Data/train.csv')


    # 3. Filters
    st.sidebar.subheader(" Dashboard Filters")

    # Create for Gender
    gender = st.sidebar.multiselect("Pick your Gender", data["gender"].unique())
    if not gender:
        filtered_data = data.copy()
    else:
        filtered_data = data[data["gender"].isin(gender)]

    # Create for payment type
    paymentmethod = st.sidebar.multiselect("Pick your Payment Method", data["paymentmethod"].unique())
    if paymentmethod:
        filtered_data = filtered_data[filtered_data["paymentmethod"].isin(paymentmethod)]

    # Create for Contract type
    contract = st.sidebar.multiselect("Pick your Contract", data["contract"].unique())
    if contract:
        filtered_data = filtered_data[filtered_data["contract"].isin(contract)]

    # 4. Define EDA Function
    def eda_dash():
        # Add CSS for EDA title animation
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
                    animation: zoom-in 3s ease-in-out;
                }
            </style>
        """, unsafe_allow_html=True)

        # Add an animated text
        st.write('<div class="zoom-in-animation"><h3>Delve into Eploratory Data Analysis Insights</h3></div>', unsafe_allow_html=True)

    # 4.1 Scatter Plot with conditional coloring
        scatter_plot = px.scatter(
            filtered_data,
            x='tenure',
            y='monthlycharges',
            color='churn',
            color_discrete_map={'yes': 'red', 'no': 'skyblue'},  
            title='Scatter Plot for Tenur vs Monthly charges'
        )

        # Update marker properties for better visualization
        scatter_plot.update_traces(marker=dict(size=10, opacity=0.8, line=dict(width=2, color='DarkSlateGrey')))
        # Display the chart using Streamlit
        st.plotly_chart(scatter_plot)


    # 4.2 Histograms
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(filtered_data, x="tenure", color="churn", marginal="box", nbins=50, title="Histogram for Tenure")
            st.plotly_chart(fig)
    
        with col2:
            # Churn by monthly charges
            fig = px.histogram(filtered_data, x="monthlycharges", color="churn", marginal="box", nbins=50, title="Histogram for Monthly Charges")
            st.plotly_chart(fig)

    # 4.3 Correlation Matrix and Heatmap for Numeric Variables
        # Separate numeric and categorical columns
        numeric_columns = filtered_data.select_dtypes(include=['number']).columns
        categorical_columns = filtered_data.select_dtypes(include=['object', 'category']).columns

        numeric_df = filtered_data[numeric_columns]
        numeric_correlation_matrix = numeric_df.corr()

        # Convert correlation matrix to Plotly's heatmap format
        fig = px.imshow(
            numeric_correlation_matrix.values,
            x=numeric_correlation_matrix.columns,
            y=numeric_correlation_matrix.columns,
            labels=dict(color="Correlation"),
            color_continuous_scale='RdBu',  # Use a suitable colorscale
            zmin=-1, zmax=1  
        )

        # Update layout of the heatmap
        fig.update_layout(
            title='Correlation Matrix Heatmap',
            xaxis_title="Numeric Variables",
            yaxis_title="Numeric Variables",
            width=800,
            height=600,
        )

        # Add annotations for correlation values
        annotations = []
        for i, row in enumerate(numeric_correlation_matrix.values):
            for j, value in enumerate(row):
                annotations.append(dict(x=numeric_correlation_matrix.columns[j], y=numeric_correlation_matrix.index[i],
                                        text=f"{value:.2f}", showarrow=False, font=dict(color='black')))

        fig.update_layout(annotations=annotations)

        st.plotly_chart(fig)
    
    # 4.4  Trend of average monthly charges by tenure
        avg_monthly_charges = filtered_data.groupby('tenure')['monthlycharges'].mean().reset_index()

        # Plotly line chart
        fig = px.line(avg_monthly_charges, x='tenure', y='monthlycharges', title='Average MonthlyCharges Trend by Tenure')
        fig.update_layout(
            xaxis_title='Tenure',
            yaxis_title='Average Monthly Charges',
            width=800,
            height=500,
        )

        # Display the chart 
        st.plotly_chart(fig)

        # Calculate churn rate by tenure
        churn_counts = filtered_data.groupby('tenure')['churn'].value_counts().unstack(fill_value=0)
        churn_counts['Churn Rate'] = churn_counts['Yes'] / churn_counts.sum(axis=1) * 100
        churn_counts = churn_counts.reset_index()

        # Plotly line chart
        fig = px.line(churn_counts, x='tenure', y='Churn Rate', title='Churn Rate by Tenure')
        fig.update_layout(
            xaxis_title='Tenure',
            yaxis_title='Churn Rate (%)',
            width=800,
            height=500,
        )

        # Display the chart using Streamlit
        st.plotly_chart(fig)




    # 5. Define KPI Function
    def kpi_dash():
        # 5.1 Add CSS for EDA title animation
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
                    animation: zoom-in 3s ease-in-out;
                }
            </style>
        """, unsafe_allow_html=True)
        # Add an animated text
        st.write('<div class="zoom-in-animation"><h3>Delve into Key Performance Indicators Insights</h3></div>', unsafe_allow_html=True)

        total_customers = len(filtered_data)
        churned_customers = (filtered_data['churn'] == 'Yes').sum()
        churn_rate = (churned_customers / total_customers) * 100
        avg_monthly_charge = filtered_data['monthlycharges'].mean()
        avg_total_charge = filtered_data['totalcharges'].mean()
        avg_tenure = filtered_data['tenure'].mean()

        # Define CSS for card visuals with background color and drop shadow
        st.write("""
            <style>
                .kpi-card {
                    background-color: #505050; 
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Shadow effect */
                    margin-bottom: 20px;
                    width: 300px; /* Set a fixed width for consistency */
                    display: inline-block;
                    margin-right: 20px;
                }
                .kpi-title {
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }
                .kpi-value {
                    font-size: 20px;
                    font-weight: bold;
                }
            </style>
        """, unsafe_allow_html=True)


    # 5.2 Display KPIs as card visuals with background color and drop shadow
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Customers 👫</div><div class='kpi-value'>{total_customers}</div></div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Churned Customers 🚶‍♂️🚶‍♀️</div><div class='kpi-value'>{churned_customers}</div></div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Churn Rate📈</div><div class='kpi-value'>{churn_rate:.2f}%</div></div>", unsafe_allow_html=True)

        col4, col5, col6 = st.columns(3)

        with col4:
            st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Avg Monthly Charge</div><div class='kpi-value'>${avg_monthly_charge:.2f}</div></div>", unsafe_allow_html=True)

        with col5:
            st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Avg Total Charge</div><div class='kpi-value'>${avg_total_charge:.2f}</div></div>", unsafe_allow_html=True)

        with col6:
            st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Avg Tenure (months)</div><div class='kpi-value'>{avg_tenure:.2f}</div></div>", unsafe_allow_html=True)



    # 5.3 Visualization section
        st.header("Churn")

    # Example visualization: Distribution of churn
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Distribution of Churn")
            churn_counts = filtered_data['churn'].value_counts()
            fig = px.pie(values=churn_counts, names=churn_counts.index)
            st.plotly_chart(fig)

        with col2:
            st.subheader("Churn by Contract")
            contract_churn_counts = filtered_data.groupby(['contract', 'churn']).size().unstack(fill_value=0)
            fig = px.pie(values=contract_churn_counts.sum(axis=1), names=contract_churn_counts.index)
            st.plotly_chart(fig)

    # Example visualization: Churn by payment method
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Churn by Payment Method")
            payment_churn_counts = filtered_data.groupby(['paymentmethod', 'churn']).size().reset_index(name='count')
            fig = px.bar(payment_churn_counts, x="paymentmethod", y="count", color="churn", barmode="group", hover_data={'count': True})
            st.plotly_chart(fig)

        # Example visualization: Churn by contract
        with col2:
            st.subheader("Churn by Contract")
            contract_churn_counts = filtered_data.groupby(['contract', 'churn']).size().reset_index(name='count')
            fig = px.bar(contract_churn_counts, x="contract", y="count", color="churn", barmode="group", hover_data={'count': True})
            st.plotly_chart(fig)


    # 5.4 Comparative Bar Graphs
        #Define function to add Data Labels
        def add_data_labels(ax):
            for p in ax.patches:
                ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='baseline', fontsize=10, color='black', xytext=(0, 1), 
                        textcoords='offset points')
                
        st.header("Distribution of Churn by Demography")

        col1, col2 = st.columns(2)

        with col1:
            # Churn by Partner
            st.subheader("Churn by Partner")
            partner_churn_counts = filtered_data.groupby(['partner', 'churn']).size().reset_index(name='count')
            fig = px.bar(partner_churn_counts, x="partner", y="count", color="churn")
            st.plotly_chart(fig)

        with col2:
            # Churn by Dependents
            st.subheader("Churn by Dependents")
            dependents_churn_counts = filtered_data.groupby(['dependents', 'churn']).size().reset_index(name='count')
            fig = px.bar(dependents_churn_counts, x="dependents", y="count" ,color="churn")
            st.plotly_chart(fig)

        col1, col2 = st.columns(2)

        with col1:
            # Churn by Senior Citizen
            st.subheader("Churn by Senior Citizen")
            seniorcitizen_churn_counts = filtered_data.groupby(['seniorcitizen', 'churn']).size().reset_index(name='count')
            fig = px.bar(seniorcitizen_churn_counts, x="seniorcitizen", y="count" ,color="churn")
            st.plotly_chart(fig)

        with col2:
            # Churn by Gender
            st.subheader("Churn by Gender")
            dependents_churn_counts = filtered_data.groupby(['churn', 'gender']).size().reset_index(name='count')
            fig = px.bar(dependents_churn_counts, x="churn", y="count" ,color="gender",orientation='v')
            st.plotly_chart(fig)

        # Additional Comparative Bar Graphs
        st.header("Churn Ditribution by Service Usage")

        col1, col2 = st.columns(2)
        with col1:
            # OnlineBackup vs InternetService vs Churn
            st.subheader("OnlineBackup vs InternetService")
            onlinebackup_churn_counts = filtered_data.groupby(['onlinebackup', 'churn']).size().reset_index(name='count')

            # Create the Plotly figure
            fig = px.bar(onlinebackup_churn_counts, x='onlinebackup', y='count', color='churn',
                        category_orders={'onlinebackup': filtered_data['onlinebackup'].value_counts().index.tolist()},
                        labels={'onlinebackup': 'Online Backup', 'count': 'No of internet service users'})
            # Display the figure in Streamlit
            st.plotly_chart(fig)

        with col2:
            # Phone Service vs MultipleLines vs Churn
            st.subheader("Phone Service vs MultipleLines vs Churn")
            phoneservice_churn_counts = filtered_data.groupby(['phoneservice', 'churn']).size().reset_index(name='count')
            # Create the Plotly figure
            fig = px.bar(phoneservice_churn_counts, x='phoneservice', y='count', color='churn',
                        category_orders={'phoneservice': filtered_data['phoneservice'].value_counts().index.tolist()},
                        labels={'phoneservice': 'Phone Service', 'count': 'count of MultipleLines'})
            # Display the figure in Streamlit
            st.plotly_chart(fig)

        col1, col2 = st.columns(2)
        with col1:    
            # Churn by Streaming Movies
            st.subheader("Churn by Streaming Movies")
            streamingmovies_churn_counts = filtered_data.groupby(['streamingmovies', 'churn']).size().reset_index(name='count')
            # Create the Plotly figure
            fig = px.bar(streamingmovies_churn_counts, x='streamingmovies', y='count', color='churn',
                        category_orders={'streamingmovies': filtered_data['streamingmovies'].value_counts().index.tolist()},
                        labels={'streamingmovies': 'Streaming Movies', 'count': 'count of Streaming Movies'})
            # Display the figure in Streamlit
            st.plotly_chart(fig)

        with col2: 
            # Churn by Online Security
            st.subheader("Online Security & InternetService")
            onlinesecurity_churn_counts = filtered_data.groupby(['onlinesecurity', 'churn']).size().reset_index(name='count')
            # Create the Plotly figure
            fig = px.bar(onlinesecurity_churn_counts, x='onlinesecurity', y='count', color='churn',
                        category_orders={'onlinesecurity': filtered_data['internetservice'].value_counts().index.tolist()},
                        labels={'streamingmovies': 'Streaming Movies', 'count': 'Count of InternetService'})
            # Display the figure in Streamlit
            st.plotly_chart(fig)

    if __name__ == "__main__":
        with st.sidebar:
            st.header("Overview")
            st.markdown("""
                This dashboard provides insights into customer churn data, helping you understand the factors influencing churn and make data-driven decisions to improve customer retention.
                """)

        if st.session_state['selected_dashboard_type'] == 'EDA':
            eda_dash()
        else:
            kpi_dash()

elif st.session_state['authentication_status'] is False:
    st.error('Wrong username/password')
elif st.session_state['authentication_status'] is None:
    st.info('Login to get access to the app')
    st.code("""
    Test Account
    Username: valiant
    Password: 123456
    """)

# st.write(st.session_state)
