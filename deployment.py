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
)


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
                            placeholder="Job/Field Title...")
        count_jobs = st.number_input(
            'Count per Job', step=1, min_value=1, value=25)
        loc = st.text_input('Location', placeholder="Country/City name...",)

        return [jobs, count_jobs, loc]


with results:
    user_inputs = get_inputs()
    with side_bar:
        is_clicked = st.button('Fetch Jobs!')

    st.write(user_inputs)
    st.write(is_clicked)
    if is_clicked:
        # a = LinkedIn(*user_inputs)
        # a.run()
        st.write(user_inputs)
