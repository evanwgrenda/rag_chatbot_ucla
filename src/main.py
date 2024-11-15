import streamlit as st
import openai
import os
from dotenv import load_dotenv
from datetime import datetime
from template import PROMPT_TEMPLATE

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Configure OpenAI client
client = openai.OpenAI(api_key=api_key)

# Configure Streamlit page
st.set_page_config(
    page_title="UCLA Post-Op Care Assistant", 
    page_icon="🏥", 
    layout="wide"
)

# Initialize session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_chatbot_response(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Using GPT-4 Turbo
            messages=[
                {"role": "system", "content": PROMPT_TEMPLATE},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("🏥 UCLA Post-Op Care Assistant")

# Sidebar with information
with st.sidebar:
    st.header("Important Information")
    st.warning("For Emergencies Call 911")
    st.info("""
    **Urgent Issues (Off hours/weekends)**
    Call: (310) 206-6766
    Ask for: Plastic Surgery Resident
    
    **Weekday Issues (8AM-5PM)**
    Call: (310) 794-7616
    Email: estayton@mednet.ucla.edu
    """)
    
    # Add date/time filter for message history
    st.header("Message History")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
user_input = st.chat_input("Type your question here...")

# Add a loading state
if user_input:
    with st.spinner('Getting response...'):
        # Add user message to history
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input,
            "timestamp": datetime.now()
        })
        
        # Get and add assistant response to history
        response = get_chatbot_response(user_input)
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "timestamp": datetime.now()
        })

# Display message history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

# Footer
st.markdown("---")
st.markdown("*This is an AI assistant. For medical emergencies, please call 911 or contact the clinic directly.*")