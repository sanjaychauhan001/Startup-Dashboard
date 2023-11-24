import streamlit as st
import pandas as pd


st.title("Startup Dashboard")
st.header("I am learning streamlit")
st.subheader("And i loving it")
st.write("this is normal text")

st.markdown("""
### My favorite movies
- 3 idiots
- Tere Naam
- Tum Bin
""")

st.code("""
def square(num):
    return num**2
x = suare(5)
""")

st.latex('x^2+y^2+2xy')

df = pd.DataFrame({
    'name':['sanjay','ajay',"anish"],
    'age':[23,33,44],
    'marks':[22,36,88]
})

st.dataframe(df)
st.metric('Revenue',"10 lakhs", "+5%")

st.json({
    'name':['sanjay','ajay',"anish"],
    'age':[23,33,44],
    'marks':[22,36,88]
})

st.sidebar.title("side bar ka title")

st.image('photo.jpeg')

col1, col2 = st.columns(2)

with col1:
    st.image('photo.jpeg')

with col2:
    st.image('photo.jpeg')

st.error("Login failled")
st.success('Login successful')
st.warning("warning message")
st.info("info message")

email = st.text_input("Enter email")
num = st.number_input("enter the age")
st.date_input("Enter the reg date")

email = st.text_input("Enter Email")
password = st.text_input("Enter Password")
gender = st.selectbox('Select Gender',['Male','Female','Others'])
btn = st.button("Login")

if btn:
    if(email == 'sanjayonlyforyou123@gmail.com' and password == '12345'):
        st.write(gender)
        st.success("Login successful")
        st.balloons()
    else:
        st.error("Login failed")
