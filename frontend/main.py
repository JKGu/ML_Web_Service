import requests
import streamlit as st
import pandas as pd
import io
url = 'http://localhost:8080'
data = st.file_uploader("Upload Dataset",type=["csv","txt"])

if data is not None:
    st.write(data.name)
    files = {'file':data}
    requests.post(f'{url}/api/v0/upload', files=files)
    requests.get(f'{url}/api/v0/preprocess/{data.name}')
    #res = requests.post(f'{url}/upload', files=files)

    #df = pd.read_csv(io.StringIO(res.content.decode('utf-8')))
    #st.dataframe(df)
    #df.to_csv('new2.csv')
