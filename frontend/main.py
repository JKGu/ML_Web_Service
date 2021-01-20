import requests
import streamlit as st
import pandas as pd
import io, json
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('Agg')
import seaborn as sns

url = 'http://localhost:8080'


st.title('Machine Learning Web Service')

data = st.file_uploader('Upload your dataset',type=['csv','txt'])
if data is None:
    st.warning('Please upload a dataset.')
else:
    #Upload the dataset
    files = {'file':data}
    res = requests.post(f'{url}/api/v0/upload', files=files)
    if res.status_code == 200:
        st.write(f'{data.name} uploaded successfully')
    else:
        st.write(res.content)
    #Read dataset from backend
    res = requests.get(f'{url}/api/v0/readfile/{data.name}/')
    if res.status_code == 200:
        df = pd.read_csv(io.StringIO(res.content.decode('utf-8')))
        st.dataframe(df.head())
    else:
        st.write(res.content)
    if st.button('Refresh dataset'):
        res = requests.get(f'{url}/api/v0/readfile/{data.name}/')
        if res.status_code == 200:
            df = pd.read_csv(io.StringIO(res.content.decode('utf-8')))

    #Activity Select
    activites = ['Exploratory Data Analysis','Data Preparation','Model Training','Prediction']
    choice = st.selectbox('Select activity',activites)
    

    if choice == 'Exploratory Data Analysis':
        st.header('Exploratory Data Analysis')
        if st.checkbox("Show shape"):
            st.write(df.shape)
        if st.checkbox("Show Columns"):
            all_columns = df.columns.to_list()
            st.write(all_columns)
        if st.checkbox("Select Columns To Show"):
            selected_columns = st.multiselect("Select Columns",all_columns)
            new_df =  df[selected_columns]
            st.dataframe(new_df)
        if st.checkbox("Show Summary"):
            st.write(df.describe())
        if st.checkbox("Show Value Counts"):
            st.write(df.iloc[:,-1].value_counts())
        if st.checkbox("Correlation with Seaborn"):
            st.write(sns.heatmap(df.corr(),annot=True))
            st.pyplot()
        if st.checkbox("Pie Chart"):
            all_columns = df.columns.to_list()
            columns_to_plot = st.selectbox("Select 1 Column ",all_columns)
            pie_plot = df[columns_to_plot].value_counts().plot.pie(autopct="%1.1f%%")
            st.write(pie_plot)
            st.pyplot()

    elif choice == 'Data Preparation':
        st.header('Data Preparation')
        res = requests.get(f'{url}/api/v0/getinfo/{data.name}')
        info = json.loads(res.text)
        pipelineList = info['pipeline']
        st.write(f'Your Pipeline:{pipelineList}')


        dropCol = st.selectbox('Drop A Column',info['columns'])
        if dropCol is not None:
            requests.put(f'{url}/api/v0/dropCol/{data.name}/{dropCol}')
            res = requests.get(f'{url}/api/v0/getinfo/{data.name}')
            info = json.loads(res.text)
        if st.button('Sanitize Everything'):
            requests.get(f'{url}/api/v0/preprocess/{data.name}')

    elif choice == 'Model Training':
        st.header('Model Training')
        if st.button('Train'):
            res = requests.get(f'{url}/api/v0/train/{data.name}')
            if res.status_code == 200:
                st.success('Training completed and model saved!')
                info = json.loads(res.text)
                eval = info['evaluation']
                st.text(f'Model Summary:{eval}')
            else:
                st.error(res.content)

    elif choice == 'Prediction':
        st.header('Prediction')
        predict = st.file_uploader('Upload your dataset for prediction',type=['csv','txt'])
        if predict is not None:
            predict = {'file':predict}
            res = requests.post(f'{url}/api/v0/predict/{data.name}', files=predict)
            if res.status_code == 200:
                df = pd.read_csv(io.StringIO(res.content.decode('utf-8')))
                st.dataframe(df)
            else:
                st.write(res.content)