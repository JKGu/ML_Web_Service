from fastapi import FastAPI,File, UploadFile,HTTPException, Response
from fastapi.responses import FileResponse
import uvicorn
import pandas as pd
import numpy as np
import os,json
import models, preprocessing
from sklearn.model_selection import train_test_split
import joblib

app = FastAPI()
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
USERFILES = os.path.join(__location__,'UserFiles')
@app.get("/")
async def read_root():
    return {"message": "Welcome from the API"}

@app.post("/api/v0/upload/")
async def upload(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    path = os.path.join(USERFILES,file.filename)
    if os.path.exists(path):
        raise HTTPException(status_code=409, detail='File already exists')
    else:
        df.to_csv(path)
        info = {}
        info['columns'] = list(df.columns)
        info['labelColumnIndex'] = -1
        info['pipeline'] = ['Default Cleaning']
        path = os.path.join(USERFILES,f'{file.filename[:-4]}.json')
        with open(path, 'w') as outfile:
            json.dump(info, outfile)
        return {'UploadFile':file.filename}

@app.get('/api/v0/readfile/{filename}')
async def readFile(filename:str):
    try:
        path = os.path.join(USERFILES,f'{filename}')
        return FileResponse(path)
    except:
        raise HTTPException(status_code=404, detail='File not found or not accessible!')

@app.get('/api/v0/getinfo/{filename}')
async def getInfo(filename:str):
    path = os.path.join(USERFILES,f'{filename[:-4]}.json')
    try:
        with open(path) as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=404, detail='File not found or not accessible!')


@app.get("/api/v0/preprocess/{datafile}")
async def clean(datafile:str):
    try:
        df = pd.read_csv(datafile)
        df = preprocessing.sanitize(df)
        path = os.path.join(USERFILES,f'{datafile}')
        df.to_csv(path)
    except:
        raise HTTPException(status_code=404, detail='File not found or not accessible!')

@app.put("/api/v0/dropCol/{datafile}/{col}")
async def drop(datafile:str,col:str):
    try:
        
        df = pd.read_csv(datafile)
        df = df.drop(columns=[col])
        path = os.path.join(USERFILES,f'{datafile}')
        df.to_csv(path)
        path = os.path.join(USERFILES,f'{datafile[:-4]}.json')
        with open(path) as f:
            data = json.load(f)
        data['columns']= list(df.columns)
        data['pipeline'] = [f'DropCol,{col}']+data['pipeline']
        with open(path, 'w') as outfile:
            json.dump(data, outfile)
    except:
        raise HTTPException(status_code=404, detail='File not found or not accessible!')


@app.get("/api/v0/train/{filename}")
async def train(filename:str):
    try:
        df = pd.read_csv(filename)
        df = preprocessing.sanitize(df)
        train, test = train_test_split(df, test_size=0.2)
        X_train = train.iloc[:,0:-1]
        y_train = train.iloc[:,-1]
        X_test = test.iloc[:,0:-1]
        y_test = test.iloc[:,-1]
        tmpModel = models.train(X_train,y_train,'LR')
        eval = models.eval(y_test,models.predict(X_test,tmpModel))
        path = os.path.join(USERFILES,f'{filename[:-3]}pkl')
        models.saveModel(tmpModel,path)
        return {'evaluation':eval}
    except:
        raise HTTPException(status_code=400)

@app.post("/api/v0/predict/{filename}")
async def predict(filename:str,file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        df = preprocessing.sanitize(df)
        path = os.path.join(USERFILES,f'{filename[:-3]}pkl')
        loaded_model = joblib.load(path)
        result = models.predict(df,loaded_model)
        path = os.path.join(USERFILES,f'{filename}_result.csv')
        np.savetxt(path,result,delimiter=',')
        return FileResponse(path)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))




if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)