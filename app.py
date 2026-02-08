"""
Sheet-Editor AI Agent - Main Streamlit Application
Natural language Excel/CSV editor with structured command execution
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime
from llm_helper import LLMHelper
from executor import Executor

# Page config
st.set_page_config(
    page_title="Sheet-Editor AI Agent",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Dark Theme (matching BNC project)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #0a0a0a 100%);
        background-attachment: fixed;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20% 30%, rgba(255, 255, 255, 0.03), transparent),
            radial-gradient(2px 2px at 60% 70%, rgba(255, 255, 255, 0.03), transparent),
            radial-gradient(1px 1px at 50% 50%, rgba(255, 255, 255, 0.02), transparent);
        background-size: 200% 200%;
        background-position: 0% 0%;
        animation: drift 20s ease infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes drift {
        0%, 100% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #e0e0e0 !important;
        font-weight: 600;
    }
    
    h1 {
        font-weight: 700;
        letter-spacing: -1px;
    }
    
    p, li, label, div {
        color: #b0b0b0 !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0a 0%, #000000 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    [data-testid="stSidebar"] * {
        color: #b0b0b0 !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #e0e0e0 !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
        color: white !important;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 12px 28px;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.2);
    }

    .stButton button:focus, .stButton button:active {
        border-color: rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1) !important;
        background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%) !important;
        color: white !important;
        outline: none !important;
    }
    
    /* Input Styling - WHITE BORDERS */
    .stTextInput > div[data-baseweb="input"],
    .stTextArea > div[data-baseweb="textarea"],
    .stNumberInput > div[data-baseweb="input"],
    .stDateInput > div[data-baseweb="input"] {
        border-color: rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        background: rgba(20, 20, 20, 0.8) !important;
        color: #FAFAFA !important;
    }
    
    .stTextInput > div[data-baseweb="input"]:focus-within,
    .stTextArea > div[data-baseweb="textarea"]:focus-within,
    .stNumberInput > div[data-baseweb="input"]:focus-within,
    .stDateInput > div[data-baseweb="input"]:focus-within {
        border-color: rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.1) !important;
        outline: none !important;
    }
    
    /* Text Input contents */
    .stTextInput input,
    .stNumberInput input {
        color: #FAFAFA !important;
        caret-color: white !important;
    }
    
    /* TextArea - WHITE BORDERS */
    .stApp .stTextArea > div[data-baseweb="textarea"] {
        border-color: rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        background: rgba(20, 20, 20, 0.8) !important;
    }

    .stApp .stTextArea > div[data-baseweb="textarea"]:focus-within {
        border-color: rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.2) !important;
        outline: none !important;
    }
    
    .stApp .stTextArea textarea {
        background: transparent !important;
        color: #FAFAFA !important;
        caret-color: white !important;
    }

    /* Chat Input - WHITE BORDERS */
    .stApp [data-testid="stChatInput"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        position: sticky !important;
        bottom: 0 !important;
        z-index: 100 !important;
        display: flex !important;
        align-items: center !important;
        min-height: 70px !important;
    }
    
    .stApp [data-testid="stChatInput"] > div {
        background: transparent !important; 
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        min-height: 56px !important;
        width: 100% !important;
        box-shadow: none !important;
    }
    
    .stApp [data-testid="stChatInput"]:focus-within > div {
        border-color: rgba(255, 255, 255, 0.9) !important;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.2) !important;
        background: transparent !important;
    }    
    
    .stApp [data-testid="stChatInput"] [data-baseweb="base-input"],
    .stApp [data-testid="stChatInput"] [data-baseweb="input"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Override ALL nested divs and forms */
    .stApp [data-testid="stChatInput"] div,
    .stApp [data-testid="stChatInput"] form,
    .stApp [data-testid="stChatInput"] > div > div {
        background: transparent !important;
    }

    .stApp [data-testid="stChatInput"] textarea,
    .stApp [data-testid="stChatInput"] textarea:invalid,
    .stApp [data-testid="stChatInput"] textarea:required {
        background: transparent !important;
        color: #FAFAFA !important;
        border: none !important;
        border-color: transparent !important;
        border-radius: 12px !important;
        padding: 0 20px !important;
        font-size: 15px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        outline: none !important;
        box-shadow: none !important;
        resize: none !important;
        flex: 1 !important;
        min-height: 56px !important;
        max-height: 56px !important;
        height: 56px !important;
        line-height: 63px !important;
        caret-color: white !important;
    }

    .stApp [data-testid="stChatInput"] textarea:focus:invalid,
    .stApp [data-testid="stChatInput"] textarea:focus:required {
        box-shadow: none !important;
        border-color: transparent !important;
        outline: none !important;
    }
    
    .stApp [data-testid="stChatInput"] textarea:focus {
        box-shadow: none !important;
        border: none !important;
        outline: none !important;
        border-color: transparent !important;
    }
    
    /* Kill all red borders */
    input, textarea, select, [data-baseweb="select"], [role="listbox"], [data-baseweb="input"] {
        caret-color: white !important;
        accent-color: white !important;
    }

    .stApp div[data-baseweb="input"],
    .stApp div[data-baseweb="select"],
    .stApp div[data-baseweb="base-input"] {
        border-color: rgba(255,255,255,0.2) !important;
        box-shadow: none !important;
    }

    .stApp div[data-baseweb="input"]:focus-within,
    .stApp div[data-baseweb="select"]:focus-within,
    .stApp div[data-baseweb="base-input"]:focus-within {
        border-color: rgba(255,255,255,0.8) !important;
        box-shadow: 0 0 10px rgba(255,255,255,0.1) !important;
    }

    input:invalid,
    input:out-of-range,
    input:required {
        box-shadow: none !important;
        outline: none !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    input:invalid:focus,
    input:out-of-range:focus,
    input:required:focus {
        border-color: rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 0 10px rgba(255,255,255,0.1) !important;
    }
    
    [data-testid="stChatInput"] textarea::placeholder {
        color: #606060 !important;
        opacity: 1 !important;
    }
    
    /* Center placeholder text vertically */
    [data-testid="stChatInput"] textarea {
        display: flex !important;
        align-items: center !important;
    }
    
    /* Chat submit button - CENTERED */
    [data-testid="stChatInput"] button,
    [data-testid="stChatInputSubmitButton"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 12px 0 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 8px !important;
        min-height: 40px !important;
        height: 40px !important;
        width: 40px !important;
        flex-shrink: 0 !important;
        align-self: center !important;
        color: white !important;
    }
    
    [data-testid="stChatInput"] > div > div:last-child {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        height: 100% !important;
    }
    
    [data-testid="stChatInput"] button:hover {
        background: rgba(99, 102, 241, 0.1) !important;
        color: rgba(99, 102, 241, 1) !important;
    }
    
    [data-testid="stChatInput"] button svg {
        color: inherit !important;
    }
    
    input, textarea {
        caret-color: white !important;
    }
    
    *:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(20, 20, 20, 0.8) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }

    .stSelectbox > div > div:focus-within {
        border-color: rgba(255, 255, 255, 0.5) !important;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1) !important;
    }
    
    .stFileUploader > div {
        background: rgba(20, 20, 20, 0.6) !important;
        border: 2px dashed rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
    }

    .stFileUploader > div:focus-within {
        border-color: rgba(255, 255, 255, 0.5) !important;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1) !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(40, 167, 69, 0.15) 0%, rgba(34, 139, 58, 0.15) 100%) !important;
        border: 1px solid rgba(40, 167, 69, 0.3) !important;
        border-radius: 8px !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.15) 0%, rgba(255, 152, 0, 0.15) 100%) !important;
        border: 1px solid rgba(255, 193, 7, 0.3) !important;
        border-radius: 8px !important;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(220, 53, 69, 0.15) 0%, rgba(176, 42, 55, 0.15) 100%) !important;
        border: 1px solid rgba(220, 53, 69, 0.3) !important;
        border-radius: 8px !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(23, 162, 184, 0.15) 0%, rgba(19, 132, 150, 0.15) 100%) !important;
        border: 1px solid rgba(23, 162, 184, 0.3) !important;
        border-radius: 8px !important;
    }
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        margin: 30px 0;
    }
    
    code {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #cccccc !important;
        padding: 3px 8px;
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_df' not in st.session_state:
    st.session_state.uploaded_df = None
if 'executor' not in st.session_state:
    st.session_state.executor = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'llm_helper' not in st.session_state:
    st.session_state.llm_helper = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = None

# Sidebar - API Configuration (copied from BNC)
with st.sidebar:
    st.markdown("### AI Configuration")
    
    provider = "groq"  # Fixed to Groq for this version
    
    st.markdown("**Model**")
    model = "openai/gpt-oss-20b"
    st.caption("openai/gpt-oss-20B (Groq)")
    
    st.markdown("**API Key**")
    groq_api_key = st.text_input(
        "Enter Groq API Key",
        type="password",
        help="Get your API key from console.groq.com"
    )
    
    if groq_api_key:
        try:
            if 'llm_helper' not in st.session_state or st.session_state.llm_helper is None:
                st.session_state.llm_helper = LLMHelper(api_key=groq_api_key, model=model)
                st.success("API Connected")
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")
    
    st.markdown("---")
    
    # File info
    if st.session_state.uploaded_df is not None:
        st.markdown("### Current File")
        st.markdown(f"**Name:** {st.session_state.file_name}")
        st.markdown(f"**Rows:** {len(st.session_state.uploaded_df)}")
        st.markdown(f"**Columns:** {len(st.session_state.uploaded_df.columns)}")
        
        if st.button("Clear & Upload New"):
            st.session_state.uploaded_df = None
            st.session_state.executor = None
            st.session_state.chat_history = []
            st.session_state.file_name = None
            st.rerun()


# Main content
st.title("Sheet-Editor AI Agent")
st.markdown("*Natural language Excel/CSV editor with intelligent command execution*")

# File upload section
if st.session_state.uploaded_df is None:
    st.markdown("### Upload Your File")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=["csv", "xlsx", "xls"],
        help="Supported formats: CSV, XLSX, XLS"
    )
    
    if uploaded_file is not None:
        try:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.session_state.uploaded_df = df
            st.session_state.file_name = uploaded_file.name
            st.session_state.executor = Executor(df)
            st.success(f"Loaded {uploaded_file.name}: {len(df)} rows, {len(df.columns)} columns")
            st.rerun()
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    
else:
    # Show current file
    df = st.session_state.executor.get_dataframe()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### Current Data: {st.session_state.file_name}")
    
    with col2:
        st.markdown(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Editable data preview
    st.markdown("#### Edit Data (click cells to edit)")
    st.caption("Click any cell to edit directly. Changes are saved automatically.")
    
    # Use data_editor for manual edits
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",  # Allow adding/deleting rows
        height=400,
        key="data_editor"
    )
    
    # Detect if user made manual edits
    if not edited_df.equals(df):
        # User edited the data manually
        st.session_state.executor.df = edited_df.copy()
        st.session_state.executor.df_history.append(edited_df.copy())
        st.success("Manual edits saved! Use Undo button to revert if needed.")
        st.rerun()
    
    st.markdown("---")
    
    # Chat interface
    st.markdown("### Chat with Your Data")
    
    # Display chat history
    for msg in st.session_state.chat_history:
        role = msg["role"]
        content = msg["content"]
        timestamp = msg.get("timestamp", "")
        
        if role == "user":
            st.markdown(f"**You** ({timestamp}):")
            st.markdown(f"> {content}")
        else:
            st.markdown(f"**AI** ({timestamp}):")
            
            # Show command if present
            if "command" in msg:
                cmd = msg["command"]
                action = cmd.get("action", "")
                
                if action == "insight":
                    st.info(msg["response"])
                elif action == "error":
                    st.error(f"{cmd.get('error', 'Unknown error')}")
                else:
                    st.markdown(f"**Command:** `{action}`")
                    if "reasoning" in cmd:
                        st.caption(cmd["reasoning"])
                    
                    # Show result
                    if msg.get("status") == "success":
                        st.success(f"{msg.get('message', 'Success')}")
                    else:
                        st.error(f"{msg.get('message', 'Failed')}")
            else:
                st.markdown(content)
    
    # Voice Input Section (above chat input)
    st.markdown("---")
    
    # Initialize voice transcript in session state
    if 'voice_transcript' not in st.session_state:
        st.session_state.voice_transcript = None
    
    col1, col2 = st.columns([1, 5])
    
    with col1:
        st.markdown("**Voice Input**")
        audio_bytes = st.audio_input("Record your query")
    
    with col2:
        st.caption("Tap to start recording, tap again to stop. Text will appear in the chat box below.")
    
    # Process voice input
    if audio_bytes is not None:
        with st.spinner("Transcribing..."):
            try:
                from audio_transcriber import get_transcriber
                
                transcriber = get_transcriber()
                result = transcriber.transcribe(audio_bytes)
                
                if result["success"]:
                    st.session_state.voice_transcript = result["text"]
                    st.success(f"Transcribed! ({result['duration']:.1f}s)")
                    st.info(f"**Transcript:** {result['text']}")
                else:
                    st.error(result["error"])
                    st.session_state.voice_transcript = None
                    
            except ImportError:
                st.error("Speech-to-text not available. Install: `pip install faster-whisper`")
                st.session_state.voice_transcript = None
            except Exception as e:
                st.error(f"Transcription error: {str(e)}")
                st.session_state.voice_transcript = None
    
    # If there's a pending transcript, display it for copy/paste
    if st.session_state.voice_transcript:
        st.markdown("**Copy Message:**")
        st.code(st.session_state.voice_transcript, language=None)
    
    # Chat input
    user_input = st.chat_input("Ask a question or give a command...")
    
    if user_input:
        # Check API key
        if not groq_api_key or st.session_state.llm_helper is None:
            st.error("Please enter your Groq API key in the sidebar")
        else:
            # Add user message
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input,
                "timestamp": timestamp
            })
            
            # Get DataFrame context
            df_context = {
                "columns": list(df.columns),
                "shape": df.shape,
                "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                "preview": df.head(3).to_dict(orient='records')
            }
            
            # Generate command
            with st.spinner("Generating command..."):
                command = st.session_state.llm_helper.generate_command(
                    user_input,
                    df_context,
                    conversation_history=st.session_state.chat_history[:-1]
                )
            
            
            # Debug: validate response type
            if not isinstance(command, (dict, list)):
                st.error(f"LLM returned unexpected type: {type(command)}")
                st.error(f"Content: {command}")
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"Error: LLM returned {type(command)} instead of dict or list",
                    "status": "error",
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                st.rerun()
            
            # Normalize to array for processing
            commands = command if isinstance(command, list) else [command]
            
            # Validate each command has action field
            for cmd in commands:
                if not isinstance(cmd, dict) or "action" not in cmd:
                    st.error(f"Command missing 'action' field")
                    st.error(f"Received: {cmd}")
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"Error: Command missing 'action' field. Got: {cmd}",
                        "status": "error",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                    st.rerun()
            
            # Track execution results
            all_results = []
            
            # Execute each command
            for idx, cmd in enumerate(commands):
                step_num = f"Step {idx+1}/{len(commands)}: " if len(commands) > 1 else ""
                
                if cmd.get("action") == "insight":
                    # Handle insight questions
                    response = cmd.get("response", "I don't have enough information to answer that.")
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response,
                        "command": cmd,
                        "response": response,
                        "status": "insight",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                    all_results.append({"status": "insight", "message": response})
                    
                else:
                    # Execute operation
                    result = st.session_state.executor.execute(cmd)
                    
                    # Update message with step number
                    message = step_num + result.get("message", "")
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": message,
                        "command": cmd,
                        "status": result.get("status"),
                        "message": message,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                    all_results.append(result)
                    
                    # If any command fails, stop execution
                    if result.get("status") == "error":
                        break
            
            # Add summary if multiple commands
            if len(commands) > 1:
                success_count = sum(1 for r in all_results if r.get("status") == "success")
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"Completed {success_count}/{len(commands)} operations",
                    "status": "summary",
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
            
            st.rerun()
    
    # Download section
    st.markdown("---")
    st.markdown("### Download Modified File")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CSV download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"modified_{st.session_state.file_name.replace('.xlsx', '').replace('.xls', '')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Excel download
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        
        st.download_button(
            label="Download as XLSX",
            data=buffer.getvalue(),
            file_name=f"modified_{st.session_state.file_name.replace('.csv', '')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col3:
        # Undo button
        if st.button("Undo Last Change"):
            if st.session_state.executor.undo():
                st.success("Undone")
                st.rerun()
            else:
                st.warning("Nothing to undo")

# Footer
st.markdown("---")
st.caption("Sheet-Editor AI Agent | Powered by Groq (openai/gpt-oss-20B)")
