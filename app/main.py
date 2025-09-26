from fastapi import FastAPI

app = FastAPI(title="Print Manager")

@app.get("/")
def root():
    return {"message": "Print Manager API is running 🚀"}