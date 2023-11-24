import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='Startup Analysis')
df = pd.read_csv('startup_cleaned.csv')
df['vertical'] = df['vertical'].replace('ECommerce','Ecommerce')
df['vertical'] = df['vertical'].replace('eCommerce','Ecommerce')
df['city'] = df['city'].replace('Bangalore','Bengaluru')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

def load_overall_analysis():
    st.title("Overall Analysis")
    col1, col2, col3, col4 = st.columns(4)
    # overall invested money
    total = round(df['amount'].sum())
    # maximum amount invested in startup
    max_funding = round(df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(1).values[0])
    # avg funding in startup
    avg_funding = round(df.groupby('startup')['amount'].sum().mean())
    # total startup funded
    total_startup = df['startup'].nunique()

    with col1:
        st.metric("Total amount invested", str(total)+ " " + 'Cr')
    with col2:
        st.metric("Max", str(max_funding) + " " + 'Cr')
    with col3:
        st.metric("Avg",str(avg_funding) + " " + 'Cr')
    with col4:
        st.metric("Funded Startup", str(total_startup))

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df1 = df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df1 = df.groupby(['year','month'])['amount'].count().reset_index()
    temp_df1['x-axis'] = temp_df1['month'].astype(str) + ' - ' + temp_df1['year'].astype(str)

    fig4, ax4 = plt.subplots()
    ax4.plot(temp_df1['x-axis'], temp_df1['amount'])
    st.pyplot(fig4)


def load_investor_details(investor):
    # load recent 5 investment of investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','investors','round','amount']]

    # biggest investment
    big_df = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head().reset_index()

    # top sectors
    top_sectors = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(ascending=False).head(7)

    # stage wise investment
    stage = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()

    # top cities
    top_city = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().sort_values(ascending=False).head(7)

    # year wise
    year = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.title(investor)
    st.subheader("Most Recent Investment")
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Biggest Investment")
        st.bar_chart(data=big_df,x="startup",y='amount')

    with col2:
        st.subheader("Top Investment Sectors")
        fig, ax = plt.subplots()
        ax.pie(top_sectors.values, labels=top_sectors.index, autopct='%1.1f%%')
        st.pyplot(fig)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Stage Investment")
        fig1, ax1 = plt.subplots()
        ax1.pie(stage.values, labels=stage.index, autopct='%1.1f%%')
        st.pyplot(fig1)

    with col4:
        st.subheader("Investment in Top City")
        fig2, ax2 = plt.subplots()
        ax2.pie(top_city.values, labels=top_city.index, autopct='%1.1f%%')
        st.pyplot(fig2)

    st.subheader("Year wise Investment")
    fig3, ax3 = plt.subplots()
    ax3.plot(year.index, year.values)
    st.pyplot(fig3)

st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox("Select One",["Overall Analysis",'Startup','Investor'])

if(option == "Overall Analysis"):
    load_overall_analysis()
elif(option == 'Startup'):
    st.sidebar.selectbox("Startup",sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button("Find startup details")
    st.title("Startup Analysis")

else:
    selected_investor = st.sidebar.selectbox("Investor",sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button("Find Investor details")

    if btn2:
        load_investor_details(selected_investor)
