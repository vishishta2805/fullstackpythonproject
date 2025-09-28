# src/logic.py
from src.db import (
    create_user as db_create_user, get_user_by_id, get_user_by_username, update_user, delete_user,
    create_chat_room, get_chat_room_by_id, list_chat_rooms, delete_chat_room,
    add_user_to_room, remove_user_from_room, get_users_in_room, get_rooms_for_user,
    send_message, get_messages_for_room, edit_message, delete_message,
    update_user_status, get_user_status
)
import uuid
import pprint
from src.db import supabase

# ---------------- USERS ----------------
class UserManager:
    def __init__(self, db=None):
        self.db = db

    def create_user(self, username, full_name, email=None, avatar_url=None):
        if not username or not full_name:
            return {"Success": False, "Message": "Username and full name are required."}

        user_id = str(uuid.uuid4())

        try:
            result = db_create_user(user_id, username, full_name, email, avatar_url)
            pprint.pprint(result)
            if result.get("error"):
                return {"Success": False, "Message": f"Error: {result['error']}"}
            return {"Success": True, "Message": "User created successfully", "user_id": user_id}
        except Exception as e:
            return {"Success": False, "Message": f"Unexpected error: {e}"}

    def get_user_by_id(self, user_id):
        try:
            result = get_user_by_id(user_id)
            if result.get("error"):
                return {"Success": False, "Message": f"Error: {result['error']}"}
            return {"data": result.get("data"), "count": len(result.get("data") or [])}
        except Exception as e:
            return {"Success": False, "Message": f"Unexpected error: {e}"}

    def update_user(self, user_id, updates: dict):
        try:
            result = update_user(user_id, updates)
            if result.get("error"):
                return {"Success": False, "Message": f"Error: {result['error']}"}
            return {"Success": True, "Message": "User updated successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Unexpected error: {e}"}

    def delete_user(self, user_id):
        try:
            result = delete_user(user_id)
            if result.get("error"):
                return {"Success": False, "Message": f"Error: {result['error']}"}
            return {"Success": True, "Message": "User deleted successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Unexpected error: {e}"}
        
    def list_users(self):
        try:
            response = supabase.table("users").select("*").execute()
            return {"Success": True, "users": response.data}
        except Exception as e:
            return {"Success": False, "Message": str(e)}


    def get_all_users_from_db():
        response = supabase.table("users").select("*").execute()
        return response.data


# ---------------- CHAT ROOMS ----------------
class ChatRoomManager:
    def __init__(self, db=None):
        self.db = db

    def create_chat_room(self, name, created_by, is_private=False):
        if not name or not created_by:
            return {"Success": False, "Message": "Room name and creator are required."}
        try:
            result = create_chat_room(name, created_by, is_private)
            if result.get("error"):
                return {"Success": False, "Message": f"Error: {result['error']}"}
            return {"Success": True, "Message": "Chat room created", "room_id": result["data"][0]["id"]}
        except Exception as e:
            return {"Success": False, "Message": f"Unexpected error: {e}"}

    def add_user_to_room(self, user_id, room_id):
        try:
            result = add_user_to_room(user_id, room_id)
            if result.get("error"):
                return {"Success": False, "Message": f"Error: {result['error']}"}
            return {"Success": True, "Message": "User added to room"}
        except Exception as e:
            return {"Success": False, "Message": f"Unexpected error: {e}"}

    def remove_user_from_room(self, user_id, room_id):
        try:
            result = remove_user_from_room(user_id, room_id)
            if result.get("error"):
                return {"Success": False, "Message": f"Error: {result['error']}"}
            return {"Success": True, "Message": "User removed from room"}
        except Exception as e:
            return {"Success": False, "Message": f"Unexpected error: {e}"}

    def get_users_in_room(self, room_id):
        try:
            result = get_users_in_room(room_id)
            if result.get("error"):
                return {"Success": False, "Message": f"Error: {result['error']}"}
            return {"data": result.get("data")}
        except Exception as e:
            return {"Success": False, "Message": f"Unexpected error: {e}"}

    def get_rooms_for_user(self, user_id):
        try:
            result = get_rooms_for_user(user_id)
            if result.get("error"):
                return {"Success": False, "Message": f"Error: {result['error']}"}
            return {"data": result.get("data")}
        except Exception as e:
            return {"Success": False, "Message": f"Unexpected error: {e}"}

    def list_chat_rooms(self):
        try:
            result = list_chat_rooms()
            if result.get("error"):
                return {"Success": False, "Message": f"Error: {result['error']}"}
            return {"data": result.get("data")}
        except Exception as e:
            return {"Success": False, "Message": f"Unexpected error: {e}"}

# ---------------- MESSAGES ----------------
class MessageManager:
    def __init__(self, db=None):
        self.db = db

    def send_message(self, room_id, sender_id, content, message_type="text", reply_to_id=None):
        if not room_id or not sender_id or not content:
            return {"Success": False, "Message": "Room ID, sender ID, and content are required."}
        try:
            result = send_message(room_id, sender_id, content, message_type, reply_to_id)
            if result.get("error"):
                return {"Success": False, "Message": f"Error: {result['error']}"}
            return {"Success": True, "Message": "Message sent", "message_id": result["data"][0]["id"]}
        except Exception as e:
            return {"Success": False, "Message": f"Unexpected error: {e}"}

    def get_messages_for_room(self, room_id, limit=50, offset=0):
        try:
            result = get_messages_for_room(room_id, limit, offset)
            if result.get("error"):
                return {"Success": False, "Message": f"Error: {result['error']}"}
            return {"data": result.get("data")}
        except Exception as e:
            return {"Success": False, "Message": f"Unexpected error: {e}"}

    def edit_message(self, message_id, new_content):
        try:
            result = edit_message(message_id, new_content)
            if result.get("error"):
                return {"Success": False, "Message": f"Error: {result['error']}"}
            return {"Success": True, "Message": "Message updated"}
        except Exception as e:
            return {"Success": False, "Message": f"Unexpected error: {e}"}

    def delete_message(self, message_id):
        try:
            result = delete_message(message_id)
            if result.get("error"):
                return {"Success": False, "Message": f"Error: {result['error']}"}
            return {"Success": True, "Message": "Message deleted"}
        except Exception as e:
            return {"Success": False, "Message": f"Unexpected error: {e}"}

# ---------------- USER STATUS ----------------
class UserStatusManager:
    def __init__(self, db=None):
        self.db = db

    def update_user_status(self, user_id, status):
        try:
            result = update_user_status(user_id, status)
            if result.get("error"):
                return {"Success": False, "Message": f"Error: {result['error']}"}
            return {"Success": True, "Message": "User status updated"}
        except Exception as e:
            return {"Success": False, "Message": f"Unexpected error: {e}"}

    def get_user_status(self, user_id):
        try:
            result = get_user_status(user_id)
            if result.get("error"):
                return {"Success": False, "Message": f"Error: {result['error']}"}
            return {"data": result.get("data")}
        except Exception as e:
            return {"Success": False, "Message": f"Unexpected error: {e}"}
