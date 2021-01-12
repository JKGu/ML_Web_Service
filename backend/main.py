from fastapi import FastAPI,File, UploadFile,HTTPException
from fastapi.responses import FileResponse
import uvicorn
import pandas as pd
import os
from io import StringIO, BytesIO
import models, preprocessing

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
    df.to_csv(path)
    return {'UploadFile':file.filename}

@app.get("/api/v0/preprocess/{datafile}")
async def clean(datafile:str):
    try:
        df = pd.read_csv(datafile)
        df = preprocessing.sanitize(df)
        path = os.path.join(USERFILES,f'{datafile}')
        df.to_csv(path)
    except:
        raise HTTPException(status_code=404, detail='File not found or not accessible!')

@app.get("/api/v0/train/")
async def train():
    pass

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)