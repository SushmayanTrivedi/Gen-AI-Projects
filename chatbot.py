from pandasai import SmartDataframe
from langchain_groq.chat_models import ChatGroq
# from pandasai.callbacks import StdoutCallback
import streamlit as st
import pandas as pd
import os
from streamlit_extras.stateful_button import button
import subprocess

file_formats = {
    "csv": pd.read_csv,
    "xls": pd.read_excel,
    "xlsx": pd.read_excel,
    "xlsm": pd.read_excel,
    "xlsb": pd.read_excel,
    "feather": pd.read_feather
}

def clear_submit():
    """
    Clear the Submit Button State
    Returns:

    """
    st.session_state["submit"] = False


@st.cache_data(ttl="2h")
def load_data(uploaded_file):
    try:
        ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
    except:
        ext = uploaded_file.split(".")[-1]
    if ext in file_formats:
        return file_formats[ext](uploaded_file)
    else:
        st.error(f"Unsupported file format: {ext}")
        return None


st.set_page_config(page_title="PandasAI ", page_icon="🐼", layout='wide')
st.title("🐼 PandasAI: Chat with CSV")

uploaded_file = st.file_uploader(
    "Upload a Data file",
    type=list(['CSV', 'XLSX']),
    help="Various File formats are Support",
    on_change=clear_submit,
)

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
    except:
        df = pd.read_csv(uploaded_file)
    st.subheader("Data Preview")
    st.dataframe(df)

api_key = st.sidebar.text_input("Groq API Key",
                                        type="password",
                                        placeholder="Paste your Groq API key here (gq-...)")

with st.sidebar:
        st.markdown("---")
        st.markdown("Made by Mr. Sushmayan Trivedi")
        st.markdown("---")


if "messages" not in st.session_state or st.sidebar.button("Clear conversation history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
tab1, tab2 = st.tabs(['Chat-based Reporting', 'AI Created Dashboard'])
with tab1:
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


    if prompt := st.chat_input(placeholder="What is this data about?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        if not api_key: 
            st.info("Please add your Groq API key to continue.")

        #PandasAI groq Model
        llm = ChatGroq(model_name = 'llama-3.2-90b-text-preview',api_key = api_key)
        sdf = SmartDataframe(df, config = {"llm": llm,
                                            "enable_cache": False,
                                            "conversational": True,
                                            # "callback": StdoutCallback()
                                            })

        with st.chat_message("assistant"):
            print(st.session_state.messages)
            response = sdf.chat(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            if ".png" in response:
                st.image(r"E:\Python\chatenv\Scripts\exports\charts\temp_chart.png", caption=idea)
            else:    
                st.write(response)
            
with tab2:
    theme = st.text_input("Explain the Theme of Dashboard you want to generate")
    gen = button("Generate", key="dashboard_gen")
    if gen:
        if uploaded_file:
            if not api_key: 
                st.info("Please add your Groq API key to continue.")
            else:
                llm2 = ChatGroq(model_name = 'llama-3.2-90b-text-preview',api_key = api_key)
                story1= f"""Provide 9 prompts for vizualization of 9 different plots out of these columns only: {list(df.columns)}in form of a comma separated list. for example if the theme is "Employee Attrition" 
                then the output can be ["Plot a bar chart of "Attrition" columns vs "Salary" (binned) column.", "Plot a bar chart of "Attrition" columns vs "Experience" (binned) column.".... and so on 9 times].
                Remember to only generate the plotting ideas out of the given columns. Do not use any extra column. you must stick to the given column names. Only give the list as output. Don't give anything.
                 IMPORTANT: **The Final output must only have the list of 9 prompts and nothing else.**
                 IMPORTANT: **AVOID LINE CHART IF YOU DON'T HAVE A TIME SERIES IN THE X-AXIS AND YOU ARE NOT ABSOLUETLY SURE ABOUT THE PLOT VALIDITY**
                 IMPORTANT: **YOU MUST USE YOUR BUSINESS UNDERSTANDING TO GIVE BUSINESS RELEVANT AND MEANINGFUL PLOTS ONLY.**"""
                response2 = llm2.invoke(story1)
                ideas= list(response2.content.split(","))
                col1, col2, col3 = st.columns(3)
                with col1:
                    for idea in ideas[0:3]:
                        sdf2 = SmartDataframe(df, config = {"llm": llm2,
                                                    "enable_cache": False,
                                                    "conversational": True,
                                                    # "callback": StdoutCallback()
                                                    })
                        idea = idea + "Make sure the labels are visible and are non-overlapping. the plot must look professional and clean"
                        response3 = sdf2.chat(idea)
                        st.image(r"E:\Python\chatenv\Scripts\exports\charts\temp_chart.png", caption=idea)
                        subprocess.run(['taskkill', '/IM', 'Microsoft.Photos.exe', '/F'])
                with col2:
                    for idea in ideas[3:6]:
                        sdf2 = SmartDataframe(df, config = {"llm": llm2,
                                                    "enable_cache": False,
                                                    "conversational": True,
                                                    # "callback": StdoutCallback()
                                                    })
                        idea = idea + "Make sure the labels are visible and are non-overlapping. the plot must look professional and clean"
                        response3 = sdf2.chat(idea)
                        st.image(r"E:\Python\chatenv\Scripts\exports\charts\temp_chart.png", caption=idea)
                        subprocess.run(['taskkill', '/IM', 'Microsoft.Photos.exe', '/F'])
                with col3:
                    for idea in ideas[6:9]:
                        sdf2 = SmartDataframe(df, config = {"llm": llm2,
                                                    "enable_cache": False,
                                                    "conversational": True,
                                                    # "callback": StdoutCallback()
                                                    })
                        idea = idea + "Make sure the labels are visible and are non-overlapping. the plot must look professional and clean"
                        response3 = sdf2.chat(idea)
                        st.image(r"E:\Python\chatenv\Scripts\exports\charts\temp_chart.png", caption=idea)
                        subprocess.run(['taskkill', '/IM', 'Microsoft.Photos.exe', '/F'])
        else:
            st.info("Please Upload a file first")
            
                    
        
    