# api/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from src.db import supabase

# ------------------ Import from src ------------------
from src.logic import UserManager, ChatRoomManager, MessageManager, UserStatusManager

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
    username: str
    full_name: str
    email: str = None
    avatar_url: str = None

class UserUpdate(BaseModel):
    username: str = None
    full_name: str = None
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

class MessageUpdate(BaseModel):
    content: str

class UserStatusUpdate(BaseModel):
    user_id: str
    status: str

# ------------------ USER Endpoints ------------------
@app.post("/users")
def create_user_endpoint(user: UserCreate):
    return users.create_user(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        avatar_url=user.avatar_url
    )

@app.get("/users/{user_id}")
def get_user_by_id_endpoint(user_id: str):
    return users.get_user_by_id(user_id)

@app.put("/users/{user_id}")
def update_user_endpoint(user_id: str, updates: UserUpdate):
    return users.update_user(user_id, updates.dict(exclude_unset=True))

@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: str):
    return users.delete_user(user_id)

@app.get("/users")
def get_all_users():
    return users.list_users()


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
    return messages.send_message(
        msg.room_id, msg.sender_id, msg.content, msg.message_type, msg.reply_to_id
    )

@app.get("/messages/{room_id}")
def get_messages_for_room_endpoint(room_id: str, limit: int = 50, offset: int = 0):
    return messages.get_messages_for_room(room_id, limit, offset)

@app.put("/messages/{message_id}")
def edit_message_endpoint(message_id: str, updates: MessageUpdate):
    return messages.edit_message(message_id, updates.content)

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

# ------------------ Run with Uvicorn ------------------
if __name__ == "__main__":
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)
