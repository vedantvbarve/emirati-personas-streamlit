import time
import streamlit as st
import pandas as pd
import os
import glob
import requests

# ====== CONFIGURATION ======
FASTAPI_URL = "https://emirati-personas-api-2l5aaarlka-ww.a.run.app"  # <-- CHANGE THIS

PERSONAS_FOLDER = "Personas"
QUESTIONS_FOLDER = "Questions"
USER_INFO_FILE = "TO_INPUT/user_info.txt"
TRAITS_FILE = "TO_INPUT/traits.txt"
LANGUAGES_FILE = "TO_INPUT/languages.txt"

# ====== DATA LOADING FUNCTIONS ======
def load_user_info():
    username = "User"
    user_gender = "unknown"
    try:
        with open(USER_INFO_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.lower().startswith('name:'):
                username = line.split(':', 1)[1].strip()
            elif line.lower().startswith('gender:'):
                user_gender = line.split(':', 1)[1].strip().lower()
    except Exception:
        pass
    return username, user_gender

def load_traits():
    try:
        with open(TRAITS_FILE, 'r', encoding='utf-8') as f:
            traits = [line.strip() for line in f if line.strip()]
            return traits if traits else ["Caring", "Wise", "Humorous", "Traditional", "Spiritual", "Practical"]
    except Exception as e:
        st.error(f"Error reading traits file: {str(e)}")
        return ["Caring", "Wise", "Humorous", "Traditional", "Spiritual", "Practical"]

def load_languages():
    try:
        with open(LANGUAGES_FILE, 'r', encoding='utf-8') as f:
            languages = [line.strip() for line in f if line.strip()]
            return languages if languages else ["English", "Arabic"]
    except Exception as e:
        st.error(f"Error reading languages file: {str(e)}")
        return ["English", "Arabic"]

def get_persona_files():
    persona_files = []
    patterns = ['*.txt']
    for pattern in patterns:
        persona_files.extend(glob.glob(os.path.join(PERSONAS_FOLDER, pattern)))
    return persona_files

def extract_relationship_from_filename(filename):
    base_name = os.path.basename(filename).replace('.txt', '')
    return base_name.replace('_', ' ')

def extract_bot_details_from_content(content):
    botname = "Assistant"
    origin = "United Arab Emirates"
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('- Name: '):
            name_part = line.replace('- Name: ', '', 1)
            botname = name_part.split(',')[0].strip()
        elif line.startswith('Name: '):
            name_part = line.replace('Name: ', '', 1)
            botname = name_part.split(',')[0].strip()
        elif 'Name:' in line:
            name_part = line.split('Name:')[1].strip()
            botname = name_part.split(',')[0].strip()
        if line.startswith('Origin: '):
            origin = line.replace('Origin: ', '', 1).strip()
        elif line.startswith('- Origin: '):
            origin = line.replace('- Origin: ', '', 1).strip()
        elif 'Origin:' in line:
            origin = line.split('Origin:')[1].strip()
        elif line.startswith('From '):
            origin = line.replace('From ', '', 1).strip()
    return botname, origin

def load_persona_content(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        st.error(f"Error reading persona file: {str(e)}")
        return ""

def load_questions(relationship_type):
    question_file = os.path.join(QUESTIONS_FOLDER, f"{relationship_type}_questions.txt")
    try:
        with open(question_file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        st.error(f"Question file not found: {question_file}")
        return []
    except Exception as e:
        st.error(f"Error reading questions: {str(e)}")
        return []

def filter_persona_by_traits(persona_content, selected_traits):
    if not selected_traits:
        return persona_content
    lines = persona_content.split('\n')
    filtered_lines = []
    basic_keywords = ['name:', 'origin:', 'from', 'age:', 'background:', 'location:']
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in basic_keywords):
            filtered_lines.append(line)
            continue
        if any(trait.lower() in line_lower for trait in selected_traits):
            filtered_lines.append(line)
    return '\n'.join(filtered_lines) if filtered_lines else persona_content

# ====== FASTAPI CALL ======
def call_fastapi_chat(bot_id, message, previous_conversation, gender, username, language):
    payload = {
        "message": message,
        "previous_conversation": previous_conversation,
        "gender": gender,
        "username": username,
        "language": language
    }
    try:
        response = requests.post(
            f"{FASTAPI_URL}/chat/{bot_id}",
            json=payload,
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("answer", "No answer"), data.get("latency", None)
        else:
            return f"API Error: {response.status_code} - {response.text}", None
    except Exception as e:
        return f"Error: {str(e)}", None

# ====== SESSION STATE INITIALIZATION ======
if "user_info_loaded" not in st.session_state:
    st.session_state.username, st.session_state.user_gender = load_user_info()
    st.session_state.user_info_loaded = True

if "available_traits" not in st.session_state:
    st.session_state.available_traits = load_traits()
if "available_languages" not in st.session_state:
    st.session_state.available_languages = load_languages()

defaults = {
    'selected_persona': None,
    'selected_persona_key': None,
    'botname': "Assistant",
    'bot_origin': "Unknown origin",
    'relationship': "mentor",
    'questions': [],
    'previous_conversation': "",
    'user_questions': [],
    'persona_content': "",
    'user_input': "",
    'selected_traits': [],
    'selected_language': "English",
    'persona_selected': False,
    'setup_completed': False
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ====== MAIN LOGIC ======
def process_user_question():
    user_question = st.session_state.user_input
    if user_question.strip():
        response, response_time = call_fastapi_chat(
            st.session_state.selected_persona_key,
            user_question,
            st.session_state.previous_conversation,
            st.session_state.user_gender,
            st.session_state.username,
            st.session_state.selected_language
        )
        st.session_state.user_questions.append({
            "question": user_question,
            "answer": response,
            "time": time.time(),
            "response_time": response_time
        })
        st.session_state.previous_conversation += f"\n{user_question}\n{response}"
    st.session_state.user_input = ""

# PHASE 1: PERSONA SELECTION (ALWAYS SHOW AT TOP)
persona_files = get_persona_files()
if persona_files:
    with st.container():
        col1, col2 = st.columns([5, 1])
        with col1:
            persona_options = persona_files
            persona_labels = [os.path.basename(f).replace('.txt','') for f in persona_files]
            current_index = 0
            if st.session_state.selected_persona in persona_files:
                current_index = persona_files.index(st.session_state.selected_persona)
                 
            st.markdown('<span style="font-size:2em; font-weight:bold;">🎯 Persona</span>', unsafe_allow_html=True)
            st.markdown('<style> div[data-testid="stSelectbox"] {margin-top: -1.2em;} </style>', unsafe_allow_html=True)
            selected_file = st.selectbox(
                "",
                persona_options,
                format_func=lambda x: os.path.basename(x).replace('.txt',''),
                index=current_index,
                key="persona_selectbox",
                label_visibility="collapsed"
            )
        with col2:
            if st.button("🔀 Change Startup", key="change_setup_btn"):
                st.session_state.setup_completed = False
                st.rerun()
    # If persona changed, reset setup
    if selected_file != st.session_state.selected_persona:
        st.session_state.selected_persona = selected_file
        st.session_state.persona_content = load_persona_content(selected_file)
        st.session_state.botname, st.session_state.bot_origin = extract_bot_details_from_content(st.session_state.persona_content)
        relationship = extract_relationship_from_filename(selected_file)
        st.session_state.relationship = relationship
        st.session_state.questions = load_questions(relationship.split()[-1])
        st.session_state.user_questions = []
        st.session_state.previous_conversation = ""
        st.session_state.user_input = ""
        st.session_state.setup_completed = False
        # Set persona key for API (assumes filename is like "female_friend.txt")
        st.session_state.selected_persona_key = os.path.basename(selected_file).replace('.txt', '')
        st.rerun()
else:
    st.error(f"No persona files found in {PERSONAS_FOLDER} directory!")
    st.stop()

# PHASE 2: SETUP CONFIGURATION
if not st.session_state.setup_completed:
    st.title("🔧 Persona Configuration")
    st.markdown(f"### Configuring: {st.session_state.botname} ({st.session_state.bot_origin})")
    st.markdown("---")
    st.subheader("📋 Select Personality Traits")
    st.markdown("**Choose one or more traits you want the AI persona to focus on:**") 

    traits = st.session_state.available_traits
    if "traits_toggle" not in st.session_state:
        st.session_state.traits_toggle = False
    all_selected = set(st.session_state.selected_traits) == set(traits)
    toggle_label = "Deselect All" if all_selected else "Select All"
    if st.button(toggle_label, key="toggle_traits_btn"):
        if all_selected:
            st.session_state.selected_traits = []
        else:
            st.session_state.selected_traits = traits.copy()
        st.session_state.traits_toggle = not all_selected
        st.rerun()

    cols = st.columns(3)
    updated_traits = []
    for i, trait in enumerate(traits):
        with cols[i % 3]:
            checked = trait in st.session_state.selected_traits
            new_checked = st.checkbox(trait, key=f"setup_trait_{i}", value=checked)
            if new_checked:
                updated_traits.append(trait)
    st.session_state.selected_traits = updated_traits

    if st.session_state.selected_traits:
        st.success(f"✅ {len(st.session_state.selected_traits)} trait(s) selected: {', '.join(st.session_state.selected_traits)}")
    else:
        st.warning("⚠️ No traits selected - all traits will be used by default") 

    st.markdown("---")
    st.subheader("🌐 Select Language")
    st.markdown("**Choose the language for conversations:**")
    if st.session_state.available_languages:
        current_index = 0
        if st.session_state.selected_language in st.session_state.available_languages:
            current_index = st.session_state.available_languages.index(st.session_state.selected_language)
        selected_language = st.selectbox(
            "",
            options=st.session_state.available_languages,
            index=current_index,
            key="setup_language"
        )
        st.success(f"✅ Language selected: {selected_language}")
    else:
        st.error("❌ No languages found. Please ensure languages.txt exists in TO_INPUT folder.")
        selected_language = "English"
    st.markdown("---") 
     
    st.subheader("👤 Personalize Your Experience")
    with st.container():
        st.markdown("""
        <style>
        div[data-testid="stTextInput"] > div > input {
            margin-top: -8px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            user_name_input = st.text_input(
                label="Your Name:",
                value=st.session_state.username,
                key="setup_username"
            )
            st.write("")
        with col2:
            st.write("")
            user_gender_input = st.selectbox(
                label="Your Gender:",
                options=["Male", "Female", "Other", "Prefer not to say"],
                index=["male", "female", "other", "prefer not to say"].index(st.session_state.user_gender.lower()) if st.session_state.user_gender.lower() in ["male", "female", "other", "prefer not to say"] else 3,
                key="setup_usergender"
            )
            st.write("")
        st.session_state.username = user_name_input
        st.session_state.user_gender = user_gender_input.lower() 
        
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Done - Start Chatting!", type="primary", use_container_width=True):
            st.session_state.selected_traits = st.session_state.selected_traits if st.session_state.selected_traits else st.session_state.available_traits
            st.session_state.selected_language = selected_language
            st.session_state.setup_completed = True
            if not st.session_state.selected_traits:
                st.info("No traits selected - using all traits as default")
            st.success("🎉 Setup completed! Starting chat...")
            time.sleep(1)
            st.rerun()
    st.markdown("---")
    st.subheader("📄 To Review: Current Selections")
    
    if st.session_state.selected_traits: 
        st.info(f"**Traits:** {', '.join(st.session_state.selected_traits)}")
    else:
        st.warning("**No traits selected** - all traits will be used by default")
    st.info(f"**Language:** {selected_language}")
    st.stop()

# PHASE 3: MAIN CHAT INTERFACE
if st.session_state.selected_persona and st.session_state.questions:
    st.title(f"{st.session_state.botname} ({st.session_state.bot_origin}) {st.session_state.relationship.title()} Q&A") 
    st.markdown(f"**Traits chosen:** {', '.join(st.session_state.selected_traits)}")
    st.markdown(f"**Language:** {st.session_state.selected_language}")
    st.markdown("---")
    st.text_input(
        "Ask a question:",
        value=st.session_state.user_input,
        key="user_input",
        on_change=process_user_question
    )
    st.subheader("Conversation History")
    if st.session_state.user_questions:
        for qa in st.session_state.user_questions:
            st.markdown(f"**You**: {qa['question']}")
            st.markdown(f"**{st.session_state.botname}**: {qa['answer']}")
            response_time = qa.get("response_time", None)
            if response_time is not None:
                st.markdown(
                    f"<div style='text-align: right; color: #666; font-size: 0.95em;'>Time taken: {response_time:.4f} seconds</div>",
                    unsafe_allow_html=True
                )
            st.markdown("") 
    else:
        st.write("*No conversation history yet. Start by asking a question!*")
else:
    if not st.session_state.questions:
        st.error("No questions found for selected relationship type!")
    else:
        st.error(f"Error loading persona: {st.session_state.selected_persona}")
