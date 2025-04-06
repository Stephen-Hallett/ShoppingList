import os

import requests
import streamlit as st

st.header("What up again big dog")
st.write(requests.get(f"{os.environ['BACKEND_ENDPOINT']}/test").text)
