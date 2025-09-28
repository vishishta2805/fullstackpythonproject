# app.py

import streamlit as st
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="💬 Web Talk App", layout="wide")

# ------------------ THEME / MODE ------------------
theme_choice = st.sidebar.selectbox("🎨 Select Theme", ["Light", "Dark"])

accent_color = "#D2A679"  # updated light brown

if theme_choice == "Dark":
    bg_color = "#0E1117"
    text_color = "#FAFAFA"
    input_bg = "#1E222B"
else:
    bg_color = "#FFFFFF"
    text_color = "#000000"
    input_bg = "#FFF8F0"

# ------------------ CSS STYLING ------------------
st.markdown(f"""
    <style>
    /* Page Background */
    .main {{background-color: {bg_color}; color: {text_color};}}

    /* Title */
    h1 {{color: {accent_color};}}

    /* All Buttons */
    div.stButton > button {{
        background-color: {accent_color} !important;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 8px 16px;
    }}
    div.stButton > button:hover {{
        background-color:#C49B6C !important;
        color: white !important;
    }}

    /* Form Submit Buttons */
    div.stForm button {{
        background-color: {accent_color} !important;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 8px 16px;
    }}
    div.stForm button:hover {{
        background-color:#C49B6C !important;
        color: white !important;
    }}

    /* Text Inputs & Textareas */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        background-color: {input_bg};
        color: {text_color};
        border: 3px solid {accent_color};
        border-radius: 8px;
        padding: 8px;
    }}

    /* Selectboxes */
    .stSelectbox>div>div>div>select {{
        background-color: {input_bg};
        color: {text_color};
        border: 3px solid {accent_color};
        border-radius: 8px;
        padding: 5px;
    }}

    /* Tabs */
    .stTabs [role="tablist"] button {{
        border-radius:10px;
        background-color:{input_bg};
        color:{text_color};
        border:3px solid {accent_color};
        font-weight:bold;
    }}

    /* Fetched message box */
    .fetched-msg {{
        border-left: 4px solid {accent_color};
        padding: 8px;
        margin-bottom: 5px;
        background-color: {input_bg};
        border-radius: 5px;
    }}
    </style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("💬 Web Talk")

# ------------------ UTILITIES ------------------
def handle_response(response):
    try:
        data = response.json()
    except Exception:
        st.error(f"❌ Server Error: {response.status_code} - {response.text}")
        return None
    if response.status_code in [200, 201]:
        st.success(data.get("Message", "✅ Success"))
        return data
    else:
        st.error(data.get("detail") or data.get("Message") or "❌ Something went wrong")
        return None

def fetch_users():
    try:
        response = requests.get(f"{BASE_URL}/users")
        if response.status_code == 200:
            data = response.json()
            return data.get("data") or data.get("users") or []
        else:
            st.error(f"❌ Failed to fetch users: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"❌ Error connecting to backend: {e}")
        return []

def fetch_rooms():
    try:
        response = requests.get(f"{BASE_URL}/rooms")
        if response.status_code == 200:
            data = response.json()
            return data.get("data", [])
        else:
            st.error(f"❌ Failed to fetch rooms: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"❌ Error connecting to backend: {e}")
        return []

# ------------------ USER MANAGEMENT ------------------
def user_management():
    st.header("👤 User Management")
    tab1, tab2, tab3 = st.tabs(["➕ Create", "🔍 Get", "⚙️ Update/Delete"])

    users_list = fetch_users()
    usernames = [u["username"] for u in users_list]

    # CREATE USER
    with tab1:
        username = st.text_input("Username")
        full_name = st.text_input("Full Name")
        email = st.text_input("Email (optional)")
        avatar_url = st.text_input("Avatar URL (optional)")
        if st.button("Create User"):
            if not username or not full_name:
                st.warning("⚠️ Username and Full Name are required!")
            else:
                data = {"username": username, "full_name": full_name, "email": email, "avatar_url": avatar_url}
                response = requests.post(f"{BASE_URL}/users", json=data)
                handle_response(response)

    # GET USER
    with tab2:
        if not usernames:
            st.info("⚠️ No users found. Please create one first.")
        else:
            user_selection = st.selectbox("Select User to Fetch", usernames)
            if st.button("Get User"):
                user_id = next((u["id"] for u in users_list if u["username"] == user_selection), None)
                if user_id:
                    response = requests.get(f"{BASE_URL}/users/{user_id}")
                    st.json(response.json())
                else:
                    st.error("❌ User not found.")

    # UPDATE / DELETE USER
    with tab3:
        if not usernames:
            st.info("⚠️ No users found. Please create one first.")
        else:
            user_selection = st.selectbox("Select User to Update/Delete", usernames)
            user_id = next((u["id"] for u in users_list if u["username"] == user_selection), None)

            if st.button("Delete User"):
                if user_id:
                    response = requests.delete(f"{BASE_URL}/users/{user_id}")
                    handle_response(response)
                else:
                    st.error("❌ User not found.")

            st.markdown("#### ✏️ Update User")
            updates = st.text_area("Enter updates as JSON (e.g., {\"full_name\": \"New Name\"})")
            if st.button("Update User"):
                if not updates.strip():
                    st.warning("⚠️ Please enter update JSON")
                else:
                    try:
                        update_data = json.loads(updates)
                        if user_id:
                            response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
                            handle_response(response)
                        else:
                            st.error("❌ User not found.")
                    except json.JSONDecodeError:
                        st.error("❌ Invalid JSON format.")

# ------------------ CHAT ROOM MANAGEMENT ------------------
def chat_room_management():
    st.header("💬 Chat Room Management")
    rooms_list = fetch_rooms()
    rooms_names = [r["name"] for r in rooms_list]
    users_list = fetch_users()
    usernames = [u["username"] for u in users_list]

    with st.form("create_room_form"):
        room_name = st.text_input("Room Name")
        creator_name = st.selectbox("Select Creator", usernames if usernames else ["No users available"])
        if st.form_submit_button("Create Room"):
            if not usernames:
                st.warning("⚠️ No users available. Please create a user first.")
            else:
                creator_id = next((u["id"] for u in users_list if u["username"] == creator_name), None)
                if not creator_id:
                    st.error("❌ Creator not found.")
                else:
                    data = {"name": room_name, "created_by": creator_id}
                    response = requests.post(f"{BASE_URL}/rooms", json=data)
                    handle_response(response)

    with st.form("add_user_form"):
        room_name_sel = st.selectbox("Select Room", rooms_names if rooms_names else ["No rooms available"])
        username_sel = st.selectbox("Select User to Add", usernames if usernames else ["No users available"])
        if st.form_submit_button("Add User to Room"):
            if not rooms_names or not usernames:
                st.warning("⚠️ You need at least one room and one user.")
            else:
                room_id = next((r["id"] for r in rooms_list if r["name"] == room_name_sel), None)
                user_id = next((u["id"] for u in users_list if u["username"] == username_sel), None)
                if room_id and user_id:
                    response = requests.post(f"{BASE_URL}/rooms/{room_id}/add_user/{user_id}")
                    handle_response(response)
                else:
                    st.error("❌ Room or User not found.")

# ------------------ MESSAGE MANAGEMENT ------------------
def message_management():
    st.header("✉️ Messages")
    users_list = fetch_users()
    usernames = [u["username"] for u in users_list]
    rooms_list = fetch_rooms()
    rooms_names = [r["name"] for r in rooms_list]

    with st.form("send_message_form"):
        room_name = st.selectbox("Room", rooms_names if rooms_names else ["No rooms available"])
        sender_name = st.selectbox("Sender", usernames if usernames else ["No users available"])
        content = st.text_area("Message Content")
        if st.form_submit_button("Send Message"):
            if not rooms_names or not usernames:
                st.warning("⚠️ Room or user list is empty.")
            else:
                room_id = next((r["id"] for r in rooms_list if r["name"] == room_name), None)
                sender_id = next((u["id"] for u in users_list if u["username"] == sender_name), None)
                if room_id and sender_id:
                    data = {"room_id": room_id, "sender_id": sender_id, "content": content}
                    response = requests.post(f"{BASE_URL}/messages", json=data)
                    handle_response(response)
                else:
                    st.error("❌ Room or Sender not found.")

    st.markdown("### 📩 Fetch Messages")
    room_name = st.selectbox("Select Room to Fetch Messages", rooms_names if rooms_names else ["No rooms available"])
    limit = st.number_input("Limit", value=10, min_value=1)
    offset = st.number_input("Offset", value=0, min_value=0)
    if st.button("Fetch Messages"):
        room_id = next((r["id"] for r in rooms_list if r["name"] == room_name), None)
        if room_id:
            response = requests.get(f"{BASE_URL}/messages/{room_id}?limit={limit}&offset={offset}")
            if response.status_code == 200:
                messages = response.json()
                for msg in messages.get("data", []):
                    sender_name = next((u["username"] for u in users_list if u["id"] == msg["sender_id"]), msg["sender_id"])
                    st.markdown(f'<div class="fetched-msg">[{sender_name}] {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                handle_response(response)
        else:
            st.error("❌ Room not found.")

# ------------------ USER STATUS ------------------
def status_management():
    st.header("📶 User Status")
    users_list = fetch_users()
    usernames = [u["username"] for u in users_list]

    if not usernames:
        st.info("⚠️ No users available. Create one first.")
        return

    user_name_sel = st.selectbox("Select User", usernames)
    status_val = st.selectbox("Status", ["online", "offline", "busy", "away"])
    if st.button("Update Status"):
        user_id = next((u["id"] for u in users_list if u["username"] == user_name_sel), None)
        if user_id:
            data = {"user_id": user_id, "status": status_val}
            response = requests.post(f"{BASE_URL}/status", json=data)
            handle_response(response)
        else:
            st.error("❌ User not found.")

    user_name_sel2 = st.selectbox("Select User to Fetch Status", usernames)
    if st.button("Get Status"):
        user_id = next((u["id"] for u in users_list if u["username"] == user_name_sel2), None)
        if user_id:
            response = requests.get(f"{BASE_URL}/status/{user_id}")
            if response.status_code == 200:
                st.write(f"📡 User Status: {response.json().get('status')}")
            else:
                handle_response(response)
        else:
            st.error("❌ User not found.")

# ------------------ MAIN NAVIGATION ------------------
menu = st.sidebar.radio("📌 Navigation", ["Users", "Chat Rooms", "Messages", "Status"])
if menu == "Users":
    user_management()
elif menu == "Chat Rooms":
    chat_room_management()
elif menu == "Messages":
    message_management()
elif menu == "Status":
    status_management()
