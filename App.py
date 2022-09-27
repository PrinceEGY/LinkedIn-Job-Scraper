from LinkedIn_Scrapping import LinkedIn
import streamlit as st
import os
from math import ceil
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import warnings
import requests
from bs4 import BeautifulSoup
import pandas as pd
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="LinkedIn Scraper",
    layout='wide'
)


def convert_df(df):
    return df.to_csv(index=False, encoding='utf-8')


side_bar = st.sidebar
results = st.container()


def get_inputs():
    with side_bar:
        st.markdown("""
                <style>
                h1{
                    font-size:3.5em !important;
                }
                label, input, textarea,button {
                    font-size:1.4em !important;
                },
                </style>
        """, unsafe_allow_html=True)
        st.title('LinkedIn Scraper',)
        jobs = st.text_area('Jobs (One job per row)',
                            placeholder="Job/Field Title...").split('\n')
        count_jobs = st.number_input(
            'Count per Job', step=1, min_value=1, value=25)
        loc = st.text_input('Location', placeholder="Country/City name...",)

        return {'search_list': jobs,
                'count_per_job': count_jobs,
                'location': loc
                }


with results:
    st.title('Results')
    user_inputs = get_inputs()
    with side_bar:
        is_clicked = st.button('Fetch Jobs!')

    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame()
    if 'logs' not in st.session_state:
        st.session_state.logs = ""

    st.dataframe(st.session_state.df)
    st.download_button(
        "Download CSV file",
        convert_df(st.session_state.df),
        "Jobs.csv",
        "text/csv",
        key='download-csv'
    )
    with st.expander('Logs', expanded=True):
        placeholder = st.empty()
        placeholder.code(st.session_state.logs)

    if is_clicked:
        a = LinkedIn([])
        a.search_list = user_inputs['search_list']
        a.count_per_job = user_inputs['count_per_job']
        try:
            a.location = user_inputs['location']
        except:
            pass

        for i in a.run():
            placeholder.empty()
            st.session_state.logs = i
            placeholder.code(st.session_state.logs)
        csv = convert_df(a._df)
        st.session_state.df = a._df
