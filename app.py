from optparse import Values
from tkinter.font import names
import streamlit as st
import plotly.express as px
import plotly.express as go
import pandas as pd
from googleapiclient.discovery import build
import json
from google.oauth2 import service_account
from streamlit_option_menu import option_menu
from PIL import Image

st.set_page_config(layout="centered")

with st.sidebar:
    choose = option_menu("Main Menu", ["About", "Financial Advice", "Contact"],
                         icons=['house', 'file-slides','person lines fill'],
                         menu_icon="list", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )
    
    logo = Image.open(r'C:\Users\Qadir\Desktop\consumerfinancialburea.png')
profile = Image.open(r'C:\Users\Qadir\Desktop\medium_profile.png')

if choose == "About":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">About the Creator</p>', unsafe_allow_html=True)    
    with col2:               # To display brand log
        st.image(logo, width=130 )
    
    st.write("We’re the Consumer Financial Protection Bureau, a U.S. government agency dedicated to making sure you are treated fairly by banks, lenders and other financial institutions..\n\nTo read more about this, please visit their Medium blog at: https://www.consumerfinance.gov/")    
    st.image(profile, width=700 )
    
elif choose=='Financial Advice':
    st.markdown(""" <style> .font {
    font-size:25px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Watch a short demo of the Financial bureau...</p>', unsafe_allow_html=True)
    video_file = open('Demo.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)    
    
elif choose == "Contact":
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Contact Form</p>', unsafe_allow_html=True)
    with st.form(key='columns_in_form2',clear_on_submit=True): #set clear_on_submit=True so that the form will be reset/cleared once it's submitted
        #st.write('Please help us improve!')
        Name=st.text_input(label='Please Enter Your Name') #Collect user feedback
        Email=st.text_input(label='Please Enter Email') #Collect user feedback
        Message=st.text_input(label='Please Enter Your Message') #Collect user feedback
        submitted = st.form_submit_button('Submit')
        if submitted:
            st.write('Thanks for your contacting us. We will respond to your questions or inquiries as soon as possible!')

# Read data from your csv file (I have save google sheet data into it)
df=pd.read_csv("myfirstdata.csv")
print(df)

st.title("Consumer Financial Complaints Dashboard")

st.header("Complaint Details")

# will select the state in the select box
state = st.selectbox('Select Filter Here:',options = df['state'].unique())
df_select = df.query("state == @state")


col2, col3,col4 = st.columns(3)

with col2:
    #Here it will sum the number of complaints
    total_no_complaints = pd.to_numeric(df_select['complaint_id']).sum()
    st.subheader('Total Complaints')
    st.text(total_no_complaints)

with col3:
    #Here it will sum the number of total complaints closed
    total_complaints_with_closed_status = pd.to_numeric(df_select.loc[df['company_response'] == 'Closed with explanation', 'complaint_id']).sum()
    st.subheader('Total Complaints Closed')
    st.text(total_complaints_with_closed_status)

with col4:
    #here it will sum the complaints in progress
    total_complaints_with_in_progress = pd.to_numeric(df_select.loc[df['company_response'] == 'In progress', 'complaint_id']).sum()
    st.subheader('Complaints with in progress')
    st.text(total_complaints_with_in_progress)
#This is the container where 
with st.container():
    col5, col6 = st.columns(2)
    with col5:
        st.subheader('Number of Complaints by Product')
        pie_figure = px.pie(df_select, values='complaint_id', names='submitted_via', color_discrete_sequence=px.colors.sequential.RdBu)
        col5.plotly_chart(pie_figure, use_container_width=True)
    with col6:
        st.subheader('Number of Complaints by Category')
        pie_figure1 = px.pie(df_select, values='complaint_id', names='submitted_via', color_discrete_sequence=px.colors.sequential.RdBu)
        col6.plotly_chart(pie_figure1, use_container_width=True)
        
        