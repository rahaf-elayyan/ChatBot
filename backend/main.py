from fastapi import FastAPI # the app builder/ core of the project
from fastapi.middleware.cors import CORSMiddleware # acts like the middleman between the backend and frontend since they will be running on differernt ports
from pydantic import BaseModel # the inspector, a tool that makes sure the data is formatted in the way it should be , and rejects any data that might contain any errors
from dotenv import load_dotenv # secretly loads the variables in the .env file into the computer's temporary environment
import os # python tool for interacting with our operating system to load things from the environment into our code.
from google import genai # the tool that talks to gemini 
from google.genai import types


#Load environment variables from .env
load_dotenv()

#API key configuration/ connecting to the brain of the chatbot
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY")) # grabs the api key from .env file and hands it to the GOOGLE AI library for authentication

# Create the FASTAPI app
app = FastAPI()

# CORS middleware (considerable the outer gate) -  allows frontend to talk to the backend. Without it, browsers block the requaets because they're both running on different ports.
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"], # tells the backend to only accept requests from this address / frontend's address(3000)
    allow_methods=["*"], # allowed actions (all, usually post or get , but because this is a test run locally)
    allow_headers = ["*"] # allowed baggage, when a request is sent, it includes hidden headers. * allows frontend to send whatever header it wants
)

# Defines the shape of data the frontend will send
class ChatRequest(BaseModel):
    message: str

# Endpoint
@app.post("/chat") # tells FASTAPI to create a specific URL that only accepts POST requests(GET is for reading the webpage), POST is for sending data
async def chat(request: ChatRequest): # asynchronous, lets the server pause the task while waiting for gemeini to finish generating a reply, and answer other messages rahter than freezing up, while specifying the type of message that is accepted
    response = client.models.generate_content(
        model = "gemini-2.0-flash-lite",
        contents = request.message) # takes the exact message typed and hands it to Gemini and waits for a response
    return{"reply": response.text} # translates it into JSON format, extracts the answer, and send it back to the front labelled as reply
