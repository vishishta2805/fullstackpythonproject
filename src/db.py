#db_manager.py
import os
from supabase import create_client
from dotenv import load_dotenv

#load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

#USERS
def create_user(user_id,username,full_name,email=None,avatar_url=None):
    response=supabase.table("users").insert({
        "id":user_id,
        "username":username,
        "full_name":full_name,
        "email":email,
        "avatar_url":avatar_url
    }).execute()
    return response

#fetch user profile by user_id
def get_user_by_id(user_id):
    return supabase.table("users").select("*").eq("id", user_id).single().execute()

def get_user_by_username(username):
    return supabase.table("users").select("*").eq("username", username).single().execute()

def update_user(user_id, updates: dict):
    return supabase.table("users").update(updates).eq("id", user_id).execute()

def delete_user(user_id):
    return supabase.table("users").delete().eq("id", user_id).execute()


#CHAT ROOMS
def create_chat_room(name,created_by,is_private=False):
    return supabase.table("chat_rooms").insert({
        "name":name,
        "created_by":created_by,
        "is_private":is_private
    }).execute()

def get_chat_room_by_id(room_id):
    return supabase.table("chat_rooms").select("*").eq("id","room_id").single().execute()

def list_chat_rooms():
    return supabase.table("chat_rooms").select("*").execute()

def delete_chat_room(room_id):
    return supabase.table("chat_rooms").delete().eq("id", room_id).execute()


#ROOM MEMBERSHIPS
def add_user_to_room(user_id,room_id):
    return supabase.table("room_members").insert({
        "user_id":user_id,
        "room_id":room_id
    }).execute()

def remove_user_from_room(user_id, room_id):
    return supabase.table("room_members").delete().eq("user_id", user_id).eq("room_id", room_id).execute()

def get_users_in_room(room_id):
    return supabase.table("room_members").select("user_id").eq("room_id", room_id).execute()

def get_rooms_for_user(user_id):
    return supabase.table("room_members").select("room_id").eq("user_id", user_id).execute()


#MESSAGES
def send_message(room_id,sender_id,content,message_type="text",reply_to_id=None):
    return supabase.table("messages").insert({
        "room_id":room_id,
        "sender_id":sender_id,
        "content":content,
        "message_type":message_type,
        "reply_to_id":reply_to_id
    }).execute()

def get_messages_for_room(room_id, limit=50, offset=0):
    return supabase.table("messages").select("*").eq("room_id", room_id).order("sent_at", desc=True).limit(limit).offset(offset).execute()

def edit_message(message_id, new_content):
    return supabase.table("messages").update({
        "content": new_content,
        "edited": True
    }).eq("id", message_id).execute()

def delete_message(message_id):
    return supabase.table("messages").delete().eq("id", message_id).execute()


#USER STATUS
def update_user_status(user_id, status):
    return supabase.table("user_status").upsert({
        "user_id": user_id,
        "status": status
    }).execute()

def get_user_status(user_id):
    return supabase.table("user_status").select("*").eq("user_id", user_id).single().execute()
