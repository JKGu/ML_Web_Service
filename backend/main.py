from fastapi import FastAPI,File, UploadFile
from fastapi.responses import FileResponse
import uvicorn
import pandas as pd
import csv
from io import StringIO, BytesIO
import models
app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome from the API"}

@app.post("/upload/")
async def upload(csv_file: UploadFile = File(...)):
    df = pd.read_csv(csv_file.file)
    df.head().to_csv('new.csv')
    return FileResponse("new.csv")
    return {"csv":df.columns}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)