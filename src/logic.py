# src/logic.py
from src.db import (
    create_user, get_user_by_id, get_user_by_username, update_user, delete_user,
    create_chat_room, get_chat_room_by_id, list_chat_rooms, delete_chat_room,
    add_user_to_room, remove_user_from_room, get_users_in_room, get_rooms_for_user,
    send_message, get_messages_for_room, edit_message, delete_message,
    update_user_status, get_user_status
)

# ---------------- USERS ----------------
class UserManager:
    def __init__(self, db=None):
        self.db = db  # optional, if you want to pass DatabaseManager instance

    def create_user(self, user_id, username, full_name, email=None, avatar_url=None):
        if not user_id or not username or not full_name:
            return {"Success": False, "Message": "User ID, username, and full name are required."}
        result = create_user(user_id, username, full_name, email, avatar_url)
        return {"Success": True, "Message": "User created successfully"} if result.get("status_code") == 201 else {"Success": False, "Message": f"Error: {result.get('error')}"}

    def get_user_by_id(self, user_id):
        return get_user_by_id(user_id)

    def update_user(self, user_id, updates: dict):
        result = update_user(user_id, updates)
        return {"Success": True, "Message": "User updated successfully"} if result.get("status_code") == 200 else {"Success": False, "Message": f"Error: {result.get('error')}"}

    def delete_user(self, user_id):
        result = delete_user(user_id)
        return {"Success": True, "Message": "User deleted successfully"} if result.get("status_code") == 200 else {"Success": False, "Message": f"Error: {result.get('error')}"}


# ---------------- CHAT ROOMS ----------------
class ChatRoomManager:
    def __init__(self, db=None):
        self.db = db

    def create_chat_room(self, name, created_by, is_private=False):
        if not name or not created_by:
            return {"Success": False, "Message": "Room name and creator are required."}
        result = create_chat_room(name, created_by, is_private)
        return {"Success": True, "Message": "Chat room created"} if result.get("status_code") == 201 else {"Success": False, "Message": f"Error: {result.get('error')}"}

    def add_user_to_room(self, user_id, room_id):
        result = add_user_to_room(user_id, room_id)
        return {"Success": True, "Message": "User added to room"} if result.get("status_code") == 201 else {"Success": False, "Message": f"Error: {result.get('error')}"}

    def remove_user_from_room(self, user_id, room_id):
        result = remove_user_from_room(user_id, room_id)
        return {"Success": True, "Message": "User removed from room"} if result.get("status_code") == 200 else {"Success": False, "Message": f"Error: {result.get('error')}"}

    def get_users_in_room(self, room_id):
        return get_users_in_room(room_id)

    def get_rooms_for_user(self, user_id):
        return get_rooms_for_user(user_id)

    def list_chat_rooms(self):
        return list_chat_rooms()


# ---------------- MESSAGES ----------------
class MessageManager:
    def __init__(self, db=None):
        self.db = db

    def send_message(self, room_id, sender_id, content, message_type="text", reply_to_id=None):
        if not room_id or not sender_id or not content:
            return {"Success": False, "Message": "Room ID, sender ID, and content are required."}
        result = send_message(room_id, sender_id, content, message_type, reply_to_id)
        return {"Success": True, "Message": "Message sent"} if result.get("status_code") == 201 else {"Success": False, "Message": f"Error: {result.get('error')}"}

    def get_messages_for_room(self, room_id, limit=50, offset=0):
        return get_messages_for_room(room_id, limit, offset)

    def edit_message(self, message_id, new_content):
        result = edit_message(message_id, new_content)
        return {"Success": True, "Message": "Message updated"} if result.get("status_code") == 200 else {"Success": False, "Message": f"Error: {result.get('error')}"}

    def delete_message(self, message_id):
        result = delete_message(message_id)
        return {"Success": True, "Message": "Message deleted"} if result.get("status_code") == 200 else {"Success": False, "Message": f"Error: {result.get('error')}"}


# ---------------- USER STATUS ----------------
class UserStatusManager:
    def __init__(self, db=None):
        self.db = db

    def update_user_status(self, user_id, status):
        result = update_user_status(user_id, status)
        return {"Success": True, "Message": "User status updated"} if result.get("status_code") in [200, 201] else {"Success": False, "Message": f"Error: {result.get('error')}"}

    def get_user_status(self, user_id):
        return get_user_status(user_id)
