from fastapi import FastAPI

app = FastAPI()

users = []

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return {"status": "success", "data": user}
    return {"status": "error", "message": "User not found"}