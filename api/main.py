# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os
import uvicorn

# Add src folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from logic import UserManager, ChatRoomManager, MessageManager, UserStatusManager

# ------------------ App Setup ------------------
app = FastAPI(title="Web Talk API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ Managers ------------------
users = UserManager()
rooms = ChatRoomManager()
messages = MessageManager()
status = UserStatusManager()

# ------------------ Pydantic Models ------------------
class UserCreate(BaseModel):
    user_id: str
    username: str
    full_name: str
    email: str = None
    avatar_url: str = None

class ChatRoomCreate(BaseModel):
    name: str
    created_by: str
    is_private: bool = False

class MessageCreate(BaseModel):
    room_id: str
    sender_id: str
    content: str
    message_type: str = "text"
    reply_to_id: str = None

class UserStatusUpdate(BaseModel):
    user_id: str
    status: str

class Student(BaseModel):
    student_id: int
    name: str
    email: str

# In-memory student store
student_store = {}

# ------------------ USER Endpoints ------------------
@app.post("/users")
def create_user_endpoint(user: UserCreate):
    return users.create_user(**user.dict())

@app.get("/users/{user_id}")
def get_user_by_id_endpoint(user_id: str):
    return users.get_user_by_id(user_id)

@app.put("/users/{user_id}")
def update_user_endpoint(user_id: str, updates: dict):
    return users.update_user(user_id, updates)

@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: str):
    return users.delete_user(user_id)

# ------------------ CHAT ROOM Endpoints ------------------
@app.post("/rooms")
def create_chat_room_endpoint(room: ChatRoomCreate):
    return rooms.create_chat_room(room.name, room.created_by, room.is_private)

@app.get("/rooms")
def list_chat_rooms_endpoint():
    return rooms.list_chat_rooms()

@app.get("/rooms/{room_id}")
def get_chat_room_by_id_endpoint(room_id: str):
    return rooms.get_chat_room_by_id(room_id)

@app.delete("/rooms/{room_id}")
def delete_chat_room_endpoint(room_id: str):
    return rooms.delete_chat_room(room_id)

@app.post("/rooms/{room_id}/add_user/{user_id}")
def add_user_to_room_endpoint(room_id: str, user_id: str):
    return rooms.add_user_to_room(user_id, room_id)

@app.post("/rooms/{room_id}/remove_user/{user_id}")
def remove_user_from_room_endpoint(room_id: str, user_id: str):
    return rooms.remove_user_from_room(user_id, room_id)

@app.get("/rooms/{room_id}/users")
def get_users_in_room_endpoint(room_id: str):
    return rooms.get_users_in_room(room_id)

# ------------------ MESSAGE Endpoints ------------------
@app.post("/messages")
def send_message_endpoint(msg: MessageCreate):
    return messages.send_message(msg.room_id, msg.sender_id, msg.content, msg.message_type, msg.reply_to_id)

@app.get("/messages/{room_id}")
def get_messages_for_room_endpoint(room_id: str, limit: int = 50, offset: int = 0):
    return messages.get_messages_for_room(room_id, limit, offset)

@app.put("/messages/{message_id}")
def edit_message_endpoint(message_id: str, updates: dict):
    new_content = updates.get("content")
    return messages.edit_message(message_id, new_content)

@app.delete("/messages/{message_id}")
def delete_message_endpoint(message_id: str):
    return messages.delete_message(message_id)

# ------------------ USER STATUS Endpoints ------------------
@app.post("/status")
def update_user_status_endpoint(data: UserStatusUpdate):
    return status.update_user_status(data.user_id, data.status)

@app.get("/status/{user_id}")
def get_user_status_endpoint(user_id: str):
    return status.get_user_status(user_id)

# ------------------ STUDENT Endpoints ------------------
@app.post("/students")
def add_student(student: Student):
    if student.student_id in student_store:
        raise HTTPException(status_code=400, detail="Student ID already exists")
    student_store[student.student_id] = student
    return {"Success": True, "Message": "Student added successfully"}

@app.get("/students")
def get_students():
    return {"students": list(student_store.values())}

@app.put("/students/{student_id}")
def update_student(student_id: int, updates: dict):
    if student_id not in student_store:
        raise HTTPException(status_code=404, detail="Student not found")
    student_data = student_store[student_id].dict()
    student_data.update(updates)
    student_store[student_id] = Student(**student_data)
    return {"Success": True, "Message": "Student updated successfully"}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in student_store:
        raise HTTPException(status_code=404, detail="Student not found")
    del student_store[student_id]
    return {"Success": True, "Message": "Student deleted successfully"}

# ------------------ Run Uvicorn ------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
