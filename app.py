import time
import streamlit as st
from utils import load_chain

# Custom image for the app icon and the assistant's avatar
company_logo = 'https://media.discordapp.net/attachments/866031156490928148/1214666163695652894/1517433440935.png?ex=65f9f104&is=65e77c04&hm=1e2f65b660d5b5f23cdb9d044b72519c258350f81d4e776da12b5997441fcf57&=&format=webp&quality=lossless'
gif_url = 'https://media.discordapp.net/attachments/882079780734894081/1214678320411844670/pikeghost.gif?ex=65f9fc57&is=65e78757&hm=620c7c72743b8090338bad27e8fa7d60442a0219abf5753204845d7acf412677&=&width=499&height=499'

# Configure streamlit page
st.set_page_config(
    page_title="PikeBot",
    page_icon=company_logo
)

# Initialize LLM chain in session_state
if 'chain' not in st.session_state:
    st.session_state['chain']= load_chain()

# Initialize chat history
if 'messages' not in st.session_state:
    # Start with first message from assistant
    st.session_state['messages'] = [{"role": "assistant", 
                                  "content": "Hi human! I am Dr Pike's smart AI. Do you have any questions about SWIFT?"}]

# Display chat messages from history on app rerun
# Custom avatar for the assistant, default avatar for user
for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"], avatar=company_logo):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat logic
if query := st.chat_input("Ask me anything"):
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)
        
    # Check for specific keywords in the query
    sensitive_keywords = ["admin", "phone number", "password", "next", "can", "please", "will", "Wi-Fi", "SSID", "Credentials", "Fragnite"]
    if any(keyword in query.lower() for keyword in sensitive_keywords):
        # Display the GIF without sending the query to the chain
        with st.chat_message("assistant", avatar=company_logo):
            st.image(gif_url, caption="Oops, let's not talk about that here!")
            
        # Add a generic assistant message to chat history to maintain flow
        st.session_state.messages.append({"role": "assistant", "content": "Oops, let's not talk about that here!"})
    else:
        # Process query normally if no sensitive keywords are found
        with st.chat_message("assistant", avatar=company_logo):
            message_placeholder = st.empty()
            # Send user's question to our chain
            result = st.session_state['chain']({"question": query})
            response = result['answer']
            full_response = ""
            
            # Simulate stream of response with milliseconds delay
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            
            # Add assistant message to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})