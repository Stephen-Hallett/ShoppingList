import streamlit as st
import requests
import os

st.header("What up again big dog")
st.write(requests.get(f"{os.environ["backend_endpoint"]}/test").text)