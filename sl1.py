import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import base64

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
    st.image("logo.png", width=200)
    st.title('GCP Hackathon - Team 5 - Data quality checks')

    # Add text under the title
    st.write("This is a Streamlit app for uploading and analyzing CSV data.")

    # Tabs
    tabs = ["Input", "Output"]
    # selected_tab = st.sidebar.radio("Tab", tabs)
    tab1, tab2 = st.tabs(tabs)

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


# Function to generate data profiling report

# Function to generate data profiling report
# @st.cache_resource
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

# Run the app
if __name__ == '__main__':
    main()