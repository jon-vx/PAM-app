from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "PAM BACKEND IS RUNNING"}
