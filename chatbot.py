import streamlit as st
import requests
import json
from typing import List, Dict
import datetime
import base64
import pandas as pd
from pathlib import Path
import markdown
import pygments
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
        self.timestamp = datetime.datetime.now()

    def to_dict(self) -> Dict:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }

class ChatBot:
    def __init__(self, model: str = "llama2"):
        self.model = model
        self.api_base = "http://localhost:11434/api"
        self.messages: List[Message] = []

    def generate_streaming_response(self, prompt: str, params: Dict):
        self.messages.append(Message("user", prompt))
        conversation = [msg.to_dict() for msg in self.messages]
        
        try:
            response = requests.post(
                f"{self.api_base}/chat",
                json={
                    "model": self.model,
                    "messages": conversation,
                    "stream": True,
                    **params
                },
                stream=True
            )
            response.raise_for_status()
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    if json_response.get("done", False):
                        break
                    content = json_response.get("message", {}).get("content", "")
                    full_response += content
                    yield content
            
            self.messages.append(Message("assistant", full_response))
            
        except requests.exceptions.RequestException as e:
            yield f"Error: {str(e)}"

def format_markdown(text: str) -> str:
    """Format text with markdown and syntax highlighting."""
    formatted = markdown.markdown(text, extensions=['fenced_code', 'tables'])
    
    # Find code blocks and apply syntax highlighting
    import re
    code_block_pattern = r'<pre><code class="([^"]*)">([^<]*)</code></pre>'
    
    def highlight_code(match):
        lang, code = match.groups()
        try:
            lexer = get_lexer_by_name(lang)
            formatter = HtmlFormatter(style='monokai')
            highlighted = pygments.highlight(code, lexer, formatter)
            return f'<div class="highlight">{highlighted}</div>'
        except:
            return match.group(0)
    
    formatted = re.sub(code_block_pattern, highlight_code, formatted)
    return formatted

def export_conversation() -> str:
    """Export conversation history as JSON."""
    if not st.session_state.messages:
        return ""
    
    export_data = {
        "metadata": {
            "model": st.session_state.chatbot.model,
            "export_time": datetime.datetime.now().isoformat()
        },
        "messages": st.session_state.messages
    }
    return json.dumps(export_data, indent=2)

def import_conversation(json_str: str) -> bool:
    """Import conversation history from JSON."""
    try:
        data = json.loads(json_str)
        st.session_state.messages = data["messages"]
        st.session_state.chatbot.model = data["metadata"]["model"]
        return True
    except:
        return False

def get_download_link(export_data: str, filename: str) -> str:
    """Generate download link for conversation export."""
    b64 = base64.b64encode(export_data.encode()).decode()
    return f'<a href="data:application/json;base64,{b64}" download="{filename}">Download Conversation</a>'

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = ChatBot()

def main():
    st.set_page_config(
        page_title="Advanced Local Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    # Add custom CSS for code highlighting
    st.markdown("""
        <style>
            .highlight { background-color: #272822; padding: 10px; border-radius: 5px; }
            .highlight pre { margin: 0; }
            .user-message { background-color: #f0f2f6; }
            .assistant-message { background-color: #ffffff; }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("Hey, I am Local Chatbot with Ollama by Ashutosh!")
    
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### Model Settings")
        available_models = ["llama2", "mistral", "codellama", "neural-chat"]
        selected_model = st.selectbox("Choose a model", available_models, index=0)
        
        st.markdown("### Model Parameters")
        col1, col2 = st.columns(2)
        with col1:
            temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
            top_k = st.slider("Top K", 1, 100, 40)
        with col2:
            top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.1)
            repeat_penalty = st.slider("Repeat Penalty", 1.0, 2.0, 1.1, 0.1)
        
        context_length = st.slider("Context Length", 512, 4096, 2048, 128)
        
        st.markdown("### Conversation Management")
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Clear History", type="primary"):
                st.session_state.messages = []
                st.session_state.chatbot = ChatBot(selected_model)
                st.rerun()
        with col4:
            if st.button("Export Chat", type="secondary"):
                export_data = export_conversation()
                st.markdown(get_download_link(export_data, "conversation.json"), unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Import Conversation", type="json")
        if uploaded_file:
            content = uploaded_file.getvalue().decode()
            if import_conversation(content):
                st.success("Conversation imported successfully!")
                st.rerun()
            else:
                st.error("Failed to import conversation!")
    
    # Update model if changed
    if st.session_state.chatbot.model != selected_model:
        st.session_state.chatbot = ChatBot(selected_model)
        st.session_state.messages = []
    
    # Chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(format_markdown(message["content"]), unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Model parameters
        params = {
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "repeat_penalty": repeat_penalty,
            "num_ctx": context_length
        }
        
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            for response_chunk in st.session_state.chatbot.generate_streaming_response(prompt, params):
                full_response += response_chunk
                response_placeholder.markdown(format_markdown(full_response + "▌"), unsafe_allow_html=True)
            
            response_placeholder.markdown(format_markdown(full_response), unsafe_allow_html=True)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    import streamlit.runtime.scriptrunner as scriptrunner
    if not hasattr(scriptrunner, 'get_script_run_ctx'):
        def get_script_run_ctx():
            return None
        scriptrunner.get_script_run_ctx = get_script_run_ctx
    
    main()
