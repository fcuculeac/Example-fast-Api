from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}


@app.get("/posts")
def get_posts():
    return {"data": "this is your posts."}


@app.post("/posts")
def get_posts(payload: dict = Body(...)):
    print(f"payload = {payload}")
    return {"new_post": f"title={payload['title']}, content={payload['content']}"}
