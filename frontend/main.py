import requests
import streamlit as st
import pandas as pd
import io
url = 'http://localhost:8080'
data = st.file_uploader("Upload Dataset",type=["csv","txt"])
if data is not None:
    files = {'csv_file':data.getvalue()}
    res = requests.post(f'{url}/upload', files=files)
    #st.json(res.json())
    df = pd.read_csv(io.StringIO(res.content.decode('utf-8')))
    st.dataframe(df)
    df.to_csv('new2.csv')
