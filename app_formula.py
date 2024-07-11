import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import base64
import os
import vertexai
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    Part,
)
from vertexai.preview.language_models import ChatModel
from PIL import Image
import requests
from io import BytesIO

PROJECT_ID = "lloyds-genai24lon-2705" # Your Google Cloud Project ID
LOCATION = "europe-west2"
vertexai.init(project=PROJECT_ID, location=LOCATION)

# On the terminal run: streamlit run --server.runOnSave true sl1.py
# Set page title and favicon
st.set_page_config(
    page_title="GCP Hackathon Team 5",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        max-width: 1200px;
        margin: auto;
        padding: 2rem;
    }
    .stTabs {
        margin: 2rem 0;
    }
    .stTabs li {
        display: inline-block;
        margin-right: 1rem;
    }
    .stTabs li:last-child {
        margin-right: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Store DataFrame in session state
session_state = st.session_state
if "df" not in session_state:
    session_state.df = None

# Main function
def main():
    # Logo and title
    # response = requests.get("https://eatsleepworkrepeat.com/wp-content/uploads/2022/02/lloyds-bank.png")
    # img = Image.open(BytesIO(response.content))
    img = 'logo.png'
    st.image(img, width=200)
    st.title('GCP Hackathon - Team 5 - Data quality checks')

    # Add text under the title
    st.write("This is a Streamlit app for uploading and analyzing CSV data.")

    # Tabs
    tabs = ["Input", "Profile report", "Written report"]
    # selected_tab = st.sidebar.radio("Tab", tabs)
    tab1, tab2, tab3 = st.tabs(tabs)

    # if selected_tab == "Input":
    with tab1:
        # File upload
        # st.sidebar.subheader("Input Options")
        # uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=['csv'])
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        # Load and cache DataFrame
        if uploaded_file is not None:
            session_state.df = pd.read_csv(uploaded_file)

        # Display DataFrame
        if session_state.df is not None:
            st.subheader('Uploaded CSV Data:')
            st.write(session_state.df)

    # elif selected_tab == "Output":
    with tab2:
        # Generate data profiling report using pandas_profiling
        if session_state.df is not None:
            st.subheader('Data Profiling Report:')
            profile = generate_report(session_state.df)

            # Provide a link to open the report
            st.markdown(get_download_link(profile), unsafe_allow_html=True)
        else:
            st.warning("Please upload a CSV file in the 'Input' tab.")

    with tab3:
        if session_state.df is not None:
            st.subheader('This is the report for your data.')
            text_model_pro, multimodal_model_pro = load_models()
            st.write("Using Gemini 1.0 Pro - Text only model")
            st.subheader("Generate a story")

            # Story premise
            character_name = st.text_input(
                "Enter character name: \n\n", key="character_name", value="Mittens"
            )
            character_type = st.text_input(
                "What type of character is it? \n\n", key="character_type", value="Cat"
            )
            character_persona = st.text_input(
                "What personality does the character have? \n\n",
                key="character_persona",
                value="Mitten is a very friendly cat.",
            )
            character_location = st.text_input(
                "Where does the character live? \n\n",
                key="character_location",
                value="Andromeda Galaxy",
            )
            story_premise = st.multiselect(
                "What is the story premise? (can select multiple) \n\n",
                [
                    "Love",
                    "Adventure",
                    "Mystery",
                    "Horror",
                    "Comedy",
                    "Sci-Fi",
                    "Fantasy",
                    "Thriller",
                ],
                key="story_premise",
                default=["Love", "Adventure"],
            )
            creative_control = st.radio(
                "Select the creativity level: \n\n",
                ["Low", "High"],
                key="creative_control",
                horizontal=True,
            )
            length_of_story = st.radio(
                "Select the length of the story: \n\n",
                ["Short", "Long"],
                key="length_of_story",
                horizontal=True,
            )

            if creative_control == "Low":
                temperature = 0.30
            else:
                temperature = 0.95

            max_output_tokens = 2048

            prompt = f"""Write a {length_of_story} story based on the following premise: \n
            character_name: {character_name} \n
            character_type: {character_type} \n
            character_persona: {character_persona} \n
            character_location: {character_location} \n
            story_premise: {",".join(story_premise)} \n
            If the story is "short", then make sure to have 5 chapters or else if it is "long" then 10 chapters.
            Important point is that each chapters should be generated based on the premise given above.
            First start by giving the book introduction, chapter introductions and then each chapter. It should also have a proper ending.
            The book should have prologue and epilogue.
            """
            # prompt = f"""Tell me if the data look right with {df['posted_day_ago']}. \n
            # What do they look like? \n
            # Are there any nans? \n
            # Are there numbers? \n
            # """
            config = {
                "temperature": 0.8,
                "max_output_tokens": 2048,
            }

            generate_t2t = st.button("Generate my story", key="generate_t2t")
            if generate_t2t and prompt:
                # st.write(prompt)
                with st.spinner("Generating your story using Gemini 1.0 Pro ..."):
                    first_tab1, first_tab2 = st.tabs(["Story", "Prompt"])
                    with first_tab1:
                        response = get_gemini_pro_text_response(
                            text_model_pro,
                            prompt,
                            generation_config=config,
                        )
                        if response:
                            st.write("Your story:")
                            st.write(response)
                    with first_tab2:
                        st.text(prompt)


def generate_report(df):
    return ProfileReport(df, explorative=True)

# Function to generate a download link for the report
def get_download_link(profile):
    report_path = "data_profiling_report.html"
    profile.to_file(report_path)
    with open(report_path, "rb") as file:
        data = file.read()
        encoded_data = base64.b64encode(data).decode()
        href = f"<a href='data:file/html;base64,{encoded_data}' download='data_profiling_report.html'>Download HTML report</a>"
        return href

@st.cache_resource
def load_models():
    """
    Load the generative models for text and multimodal generation.

    Returns:
        Tuple: A tuple containing the text model and multimodal model.
    """
    text_model_pro = GenerativeModel("gemini-1.0-pro")
    multimodal_model_pro = GenerativeModel("gemini-1.0-pro-vision")
    return text_model_pro, multimodal_model_pro

def get_gemini_pro_text_response(
    model: GenerativeModel,
    prompt: str,
    generation_config,
    stream: bool = True,
):
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    responses = model.generate_content(
        prompt,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=stream,
    )

    final_response = []
    for response in responses:
        try:
            # st.write(response.text)
            final_response.append(response.text)
        except IndexError:
            # st.write(response)
            final_response.append("")
            continue
    return " ".join(final_response)

def get_gemini_pro_vision_response(
    model, prompt_list, generation_config={}, stream: bool = True
):
    generation_config = {"temperature": 0.1, "max_output_tokens": 2048}
    responses = model.generate_content(
        prompt_list, generation_config=generation_config, stream=stream
    )
    final_response = []
    for response in responses:
        try:
            final_response.append(response.text)
        except IndexError:
            pass
    return "".join(final_response)

def create_session():
    chat_model = ChatModel.from_pretrained("chat-bison@001")
    chat = chat_model.start_chat()
    return chat

def response(chat, message):
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40
    }
    result = chat.send_message(message, **parameters)
    return result.text

# Run the app
if __name__ == '__main__':
    main()