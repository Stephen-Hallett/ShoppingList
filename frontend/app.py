import streamlit as st
import requests
import os

st.header("What up again big dog")
test = st.text_input("Endpoint")

st.write(f"{os.environ["backend_endpoint"]}/test")
st.write(f"{test}/test")
st.write(requests.get(f"{test}/test").text)