import streamlit as st
import os 
from openai_api import openai_api

st.set_page_config(layout="wide")

async def app():
    if "current_form" not in st.session_state:
        st.session_state["current_form"] = 1
    if "adventure_settings" not in st.session_state:
        st.session_state["adventure_settings"] = None
    if "character_settings" not in st.session_state:
        st.session_state["character_settings"] = {}

    if st.session_state["current_form"] == 1:
        await intro()
        

async def intro():
    st.title("Procedurally Generated Adventures")
    st.header("Create your own adventure!")
    image_loc = "assets/intro1.png"
    st.image(image_loc)
    created_by = "by Angel Jude Diones for CCS 229"
    intro_text = """ Welcome to to ProcGenA: Procedurally Generated Adventures. ProcGenA is a tool used to procedurally
    Generate adventures for your app. To use the app, start selecting the features of your character below.
    After doing so, proceed to give answer to sections of screens to finish your adventure.
    """
    st.subheader(created_by)
    st.write(intro_text)

    form1 = st.form("Intro")
    
    adventure_options = form1.selectbox("What type of story do you want?", ("Fantasy", "1930s", "Medieval"), placeholder ="Enter Genre")
    character_name = form1.text_input("What is your name?")
    character_sex = form1.selectbox("What is your sex?", ("Male", "Female"), placeholder ="Enter Sex")
    character_description = form1.text_input("Enter a description for your character")

    submit = form1.form_submit_button("Start your adventure now.")

    if submit:
        if adventure_options and character_name and character_sex and character_description:
            st.session_state["adventure_options"] = adventure_options
            st.session_state["character_settings"]["character_name"] = character_name
            st.session_state["character_settings"]["character_sex"] = character_sex
            st.session_state["character_settings"]["character_description"] = character_description
        else:
            if not adventure_options:
                form1.warning("Missing adventure options")
            if not character_name:
                form1.warning("Missing name")
            if not character_sex:
                form1.warning("Missing sex")
            if not character_description:
                form1.warning("Missing description")




if __name__ == "__main__":
    import asyncio
    asyncio.run(app())
