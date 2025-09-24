# Web Talk

This is a full-stack real-time chat application built with Python, FastAPI, Streamlit, Supabase, and WebSockets. It allows users to register, log in, and chat in real-time in both private and group chat rooms. Messages are stored in a database to maintain chat history, and real-time updates are delivered via WebSockets or Supabase Realtime subscriptions, ensuring a smooth and interactive user experience.

This project demonstrates modern web development concepts including authentication, database integration, real-time communication, and frontend-backend interaction, all implemented using free and open-source technologies.


### Features

* User registration and login
* Private/direct messaging
* Chat rooms for group discussions
* Real-time message updates
* Message history saved in the database
* Optional emoji support and typing indicators


### Project Structure

WEBTALK/
|
|---src/                #core application logic
|     |---logic.py      #Business logic and task
operations 
|     |__db.py          #DataBase Operations
|
|---api/                #Backend API
|     |__main.py        #FastAPI endpoints
|
|---frontend/           #Frontend application
|        |__app.py      #Streamlit web interface
|
|____requirements.txt    # Python Dependencies
|
|____READ.md             #Project documentation
|
|____.env                #Python Variables

### Quick Start



### Prerequisites

- Python 3.8 or higher
- Supabase account
- Git(Push,cloning)

#### 1. Clone or Download the Project
##### Option 1:Clone with Git
git clone <repository-url>

##### Option 2: Download and extract the ZIP file


#### 2. Install Dependencies
##### Install all required Python packages
pip install -r requirements.txt


#### 3. Set Up Supabase Database
1.Create a Supabase Project:

2.Create the Task Table:

- Go to the SQL Editor in your Supabase dashboard
- Run this SQL command:
- - -sql
        - creteert

3.Get Your Credentials:


#### 4. Configure Environment Variables
1.Create a `.env` file in the project root

2.Add your Supabase credentials to `.env`:
- SUPABASE_URL=your_project_url_here
- SUPABASE_KEY=your_anon_key_here

**Example:**
- SUPABASE_URL=https://anbdydhsdnxj.supabase.co
- SUPABASE_KEY=jhyjfrgykjklm.....


#### 5. Run the Application
##### Stremlit Frontend
streamlit run frontend/app.py

The app will open in your browser at `http://localhost:8501`

##### FastAPI Backend
cd api
python main.py

The API will be available at `http://localhost:8000`



### How to Use



### Technical Details



### Technologies Used

**Frontend**: Streamlit (Python web Framework)

**Backend**: FastAPI, Uvicorn (Python REST API framework)

**Database**: Supabase (PostgreSQL-based backend-as-a-service)

**Language**:Python 3.8+



### Key Components

1. **`src/db.py`**:Database operations 
    -Handles all CRUD operations with Supabase

2. **`src/logic.py`**:Business logic 
    -Task validation and processing


### Troubleshooting


### Common Issues

1.


### Future Enhancements
Ideas for extending this project:

1. **Emojis**:Allow users to send emojis in messages
2. **Audio/Video**:Add real-time audio/video communication between users
3. **Chatbot**:Introduce a bot user that can answer questions or moderate chats,could be a simple keyword-based bot or an AI-powered assistant.
Example features: automated replies, FAQs, or fun commands like /joke
4. **Notifications**:Add real-time browser or in-app notifications for new messages,could include desktop push notifications for web users

### Support

If you encounter any issues or have questions:
- Mobile no:9912283777
- Email:vishishta2805@gmail.com
