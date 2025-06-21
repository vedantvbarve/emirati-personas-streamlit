# Sri Lankan Personas Streamlit App

---
**Link:** https://srilankan-personas-culturevo.streamlit.app/

---

## Overview

This repository contains a Streamlit application that simulates conversations with Sri Lankan personas, such as mentors, friends, and family members, using Google Gemini (GenAI) models. The app allows users to:

- Select a persona from a set of text files.
- Generate bulk Q&A CSVs based on predefined question sets.
- Engage in individual, interactive conversations with the persona.
- Download generated Q&A as CSV files.
- View a complete, chronologically ordered conversation history, including both bulk and individual interactions.

The app is designed for flexibility, supporting both structured (bulk) and free-form (chat) interactions, and maintains full conversational context throughout the session.

**Update:** The application now features enhanced personalization and streamlined setup workflows to deliver more tailored interactions.

---

## Features

- **Persona Selection:** Choose from multiple persona files, each with unique background and personality traits.
- **Bulk Q&A Generation:** Automatically generate answers to a set of predefined questions, with progress tracking and the ability to pause/resume generation.
- **Interactive Chat:** Ask individual questions at any time; the app maintains context and integrates these into the ongoing conversation.
- **Downloadable Results:** Download all generated Q&A as a CSV file, with the download button always available after generation.
- **Conversation History:** See a full transcript of all individual and bulk interactions, with clear visual separation and status messages for bulk mode events.
- **User Personalization:** User name and gender are loaded from a `user_info.txt` file at the repo root, ensuring responses are tailored. This will serve as the default name and gender. Concurrently, a feature that has been implemented is the flexibity to enter in a custom name and gender for a more personalized experience.
- **Automatic Persona Extraction:** Bot name and origin are extracted from each `[persona files].txt` file in the `Personas` folder, ensuring responses are tailored. The assumption made is: the lines with name and origin begin with `Name: ` and `Origin: ` respectively.
- **Robust Error Handling:** The app gracefully handles missing files, malformed question files, and API errors, and provides clear user feedback. 
- **Persona Customization:** The app allows you to choose specific personality traits (e.g., "Traditional", "Humorous") to shape responses, as well as select conversation language (English/Sinhala/Tamil/Hindi) for authentic interactions. One of the features provided is to allow you to directly select/deselect all trait options.
- **Refined Interface:** 
  - Streamlined Setup: Intuitive persona → traits → language configuration flow
  - Clear setup progression indicators
  - Responsive layout adjustments

---

## Deployment Instructions

### 1. Prerequisites

- Python 3.8 or higher
- Streamlit
- Required Python packages (see below)
- Google Gemini API key

### 2. Folder Structure

```
repo-root/
│
├── README.md
├── Personas/
│   └── [persona files].txt
├── Questions/
│   └── [relationship]_questions.txt
├── TO_INPUT/             
│   ├── traits.txt        
│   ├── languages.txt     
│   └── user_info.txt   
├── r_optimized.py
└── requirements.txt
└── to_run.py (one-time use)
```

- **Personas/**: Contains persona description files (e.g., `male_mentor.txt`).
- **Questions/**: Contains question files for each relationship type (e.g., `mentor_questions.txt`), with one question per line (no brackets or quotes).
- **TO_INPUT/**: Configuration files.
  - `traits.txt`: Customizable traits list. One trait per line.
  - `languages.txt`: Bot-supported languages.
  - `user_info.txt`: User name and gender in the format
    ```
    Name: YourName
    Gender: yourgender
    ```
- **r_optimized.py**: The main Streamlit app file. 
- **requirements.txt**: The libraries needed to run the code. 
- **to_run.py**: The code required to convert the string array-like text in the `Questions/[relationship]_questions.txt` to 1 question/line.

### 3. Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should include at least:

```
streamlit
pandas
llama-index-llms-google
google-generativeai
```

### 4. Google Gemini API Key

- Obtain an API key for Google Gemini (GenAI).
- Set it as an environment variable or directly in the code (not recommended for production).

### 5. Running the App

From the repo root, run:

```bash
streamlit run r_optimized.py
```

The app will open in your browser.

---

## Common Setbacks and Solutions

| Issue                                      | Solution                                                                                   |
|---------------------------------------------|--------------------------------------------------------------------------------------------|
| **Debug output in app**                     | Remove or comment out all `st.write` debug lines in the code.                           |
| **Questions file not parsed correctly**     | Ensure each question is on its own line, with no brackets, quotes, or commas. Run `to_run.py` to aid with this. |
| **Array-format question files**             | Use the provided script to convert Python array format to plain text, one question per line. |
| **CSV download button disappears**          | Place the download button outside the generation button logic, and use session state to persist the filename. |
| **User info hardcoded**                     | Store user name and gender in `user_info.txt` and load them at app startup.             |
| **Bulk and individual Q&A context lost**    | The app maintains a unified `previous_conversation` variable for all interactions.       |
| **KeyError or NameError in Q&A timing**     | Always check for the presence of keys before accessing them, and ensure all required modules (e.g., `time`) are imported. | 
| **Forking and deployment**                  | Forking the repo creates an independent copy; changes in forks do not affect the original app unless merged.|

---

## Deployment on Streamlit Cloud

1. **Push your repo to GitHub.**
2. **Go to [Streamlit Community Cloud](https://share.streamlit.io/).**
3. **Click "New app", select your repo and branch, and set the main file to `r_optimized.py`.**
4. **Set your Google Gemini API key as a secret or environment variable in the Streamlit Cloud settings.**
5. **Deploy.**

**Note:** If you fork this repo and deploy your own version, your changes will not affect the original app unless you submit a pull request and it is merged.

---

## Positive Outcomes

- **Deeper Personalization:** Trait combinations create unique interaction styles 
- **Cultural Authenticity:** Language support enhances regional authenticity 
- **Efficiency Gains:** Optimized processing reduces latency 
- **User Empowerment:** Intuitive setup puts users in control of their experience

---

## Troubleshooting

- **App crashes with `SyntaxError` or `KeyError`:** Check that all files are in the correct format and all required keys are present in dictionaries.
- **CSV download button not visible:** Ensure the download button code is outside the generation logic and uses session state.
- **Bulk/individual Q&A context not maintained:** Do not reset `st.session_state.previous_conversation` except when changing persona.
- **Missing configuration files:** Verify all files exist in TO_INPUT/
- **Persona or question files not found:** Verify folder names and file paths match those in the code.

---

## Initial Files

- https://drive.google.com/drive/folders/1PRcLBgJC-oo8AAK_AiXcaC6o-kTxF8lV?usp=drive_link
- https://docs.google.com/document/d/1XB_2fwlsus_5RaGftEjeSmUdfzqXzqbjjVRg_uN9OXg/edit?usp=sharing

---

## License

This project is provided for educational and research purposes. See `LICENSE` for details. 
