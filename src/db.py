# src/db.py
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# ---------------- USERS ----------------
def create_user(user_id, username, full_name, email=None, avatar_url=None):
    try:
        response = supabase.table("users").insert({
            "id": user_id,
            "username": username,
            "full_name": full_name,
            "email": email,
            "avatar_url": avatar_url
        }).execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

def get_user_by_id(user_id):
    try:
        response = supabase.table("users").select("*").eq("id", user_id).single().execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

def get_user_by_username(username):
    try:
        response = supabase.table("users").select("*").eq("username", username).single().execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

def update_user(user_id, updates: dict):
    try:
        response = supabase.table("users").update(updates).eq("id", user_id).execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

def delete_user(user_id):
    try:
        response = supabase.table("users").delete().eq("id", user_id).execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

# ---------------- CHAT ROOMS ----------------
def create_chat_room(name, created_by, is_private=False):
    try:
        response = supabase.table("chat_rooms").insert({
            "name": name,
            "created_by": created_by,
            "is_private": is_private
        }).execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

def get_chat_room_by_id(room_id):
    try:
        response = supabase.table("chat_rooms").select("*").eq("id", room_id).single().execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

def list_chat_rooms():
    try:
        response = supabase.table("chat_rooms").select("*").execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

def delete_chat_room(room_id):
    try:
        response = supabase.table("chat_rooms").delete().eq("id", room_id).execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

# ---------------- ROOM MEMBERS ----------------
def add_user_to_room(user_id, room_id):
    try:
        response = supabase.table("room_members").insert({
            "user_id": user_id,
            "room_id": room_id
        }).execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

def remove_user_from_room(user_id, room_id):
    try:
        response = supabase.table("room_members").delete().eq("user_id", user_id).eq("room_id", room_id).execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

def get_users_in_room(room_id):
    try:
        response = supabase.table("room_members").select("user_id").eq("room_id", room_id).execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

def get_rooms_for_user(user_id):
    try:
        response = supabase.table("room_members").select("room_id").eq("user_id", user_id).execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

# ---------------- MESSAGES ----------------
def send_message(room_id, sender_id, content, message_type="text", reply_to_id=None):
    try:
        response = supabase.table("messages").insert({
            "room_id": room_id,
            "sender_id": sender_id,
            "content": content,
            "message_type": message_type,
            "reply_to_id": reply_to_id
        }).execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

def get_messages_for_room(room_id, limit=50, offset=0):
    try:
        response = supabase.table("messages").select("*").eq("room_id", room_id).order("sent_at", desc=True).limit(limit).offset(offset).execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

def edit_message(message_id, new_content):
    try:
        response = supabase.table("messages").update({
            "content": new_content,
            "edited": True
        }).eq("id", message_id).execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

def delete_message(message_id):
    try:
        response = supabase.table("messages").delete().eq("id", message_id).execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

# ---------------- USER STATUS ----------------
def update_user_status(user_id, status):
    try:
        response = supabase.table("user_status").upsert({
            "user_id": user_id,
            "status": status
        }).execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}

def get_user_status(user_id):
    try:
        response = supabase.table("user_status").select("*").eq("user_id", user_id).single().execute()
        return {"data": getattr(response, "data", None), "error": getattr(response, "error", None)}
    except Exception as e:
        return {"data": None, "error": str(e)}
