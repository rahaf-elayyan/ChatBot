import streamlit as st # the UI builder
import requests # the tool that takes user's message from streamlit and gives it to the FastAPI server

st.title("Pilot Chatbot")

# session_state persists data between reruns of the app, runs the python code from top to bottom everytime, acts as the app's memory within a session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages
for msg in st.session_state.messages: 
    with st.chat_message(msg["role"]): # roles for messages in memory vault
        st.write(msg["content"])

# The input box at the bottom
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Send to backend and get response
    response = requests.post(
        "http://localhost:8000/chat",
        json={"message": user_input}
    )
    print("Status code:", response.status_code)
    print("Raw response:", response.text)
    reply = response.json()["reply"]

    # Add assistant response to history and display it
    st.session_state.messages.append({"role": "assistant", "content": "reply"})
    with st.chat_message("assistant"):
        st.write(reply)