import streamlit as st
import os 
import random
from openai_api import openai_api 

st.set_page_config(layout="wide")

async def app():
    """
    This async function initializes the app
    Ensures that all variables relevant to the storytelling process exists
    The output expected is a text file for the summary of the story
    """
    if "current_form" not in st.session_state:
        st.session_state["current_form"] = 1
    if "adventure_options" not in st.sessions_state:
        st.sessions_state["adventure_options"] = None
    if "character_settings" not in st.session_state:
        st.session_state["character_settings"] = {}
    if "message_history" not in st.session_state:
        st.session_state["message_history"] = []
    if "story_scenes" not in st.session_state:
        st.session_state["story_scenes"] = {
            "Fantasy": {
                "Town": ["Tavern", "Bazaar", "Garden"],
                "Quest Giver": ["Mysterious Man", "Babbling Man", "Shadowy Figure"],
                "Adventure": ["Lost Treasure", "In Distress", "Missing Person"],
                "Antagonist": ["Zombie", "Monster"],
                "Conclusion": ["Character Dies", "Character Celebrates"]
            },
            "1930s": {
                "Town": ["Restaurant", "Speakeasy"],
                "Quest Giver": ["Strange Man", "Mobster"],
                "Adventure": ["Drive Along", "Collection", "Angry Customer"],
                "Antagonist": ["Gangster", "Vigilante"],
                "Conclusion": ["User Dies", "User Celebrates"]
            }
        }
    if "story_settings" not in st.session_state:
        st.session_state["story_settings"] = {}

    if st.session_state["current_form"] == 1:
        await intro()
    elif st.session_state["current_form"] == 2:
        await scene_1()
    elif st.session_state["current_form"] == 3:
        await scene_2()
    elif st.session_state["current_form"] == 4:
        await scene_3()
    elif st.session_state["current_form"] == 5:
        await scene_4()
    elif st.session_state["current_form"] == 6:
        await scene_5()


async def intro():
    """
    This function introduces the user the application

    Inputs
    adventure_options(string): Genre of the story

    character_name(string): User's name

    character_sex(string): A user's sex

    character_description(string): A user's description
    """
    st.title("Procedurally Generated Adventures")
    st.subheader("Create your own adventure!")
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
    
    adventure_options = form1.selectbox("What type of story do you want?", ("Fantasy", "1930s"), placeholder ="Enter Genre")
    character_name = form1.text_input("What is your name?")
    character_sex = form1.selectbox("What is your sex?", ("Male", "Female"), placeholder ="Enter Sex")
    character_description = form1.text_input("Enter a description for your character")

    submit = form1.form_submit_button("Start your adventure now.")
    story = st.session_state["story_scenes"]

    if submit:
        if adventure_options and character_name and character_sex and character_description:
            st.session_state["adventure_options"] = adventure_options
            st.session_state["character_settings"]["character_name"] = character_name
            st.session_state["character_settings"]["character_sex"] = character_sex
            st.session_state["character_settings"]["character_description"] = character_description
            st.session_state["story_settings"]["town_loc"] = random.choice(story[st.session_state["adventure_options"]]["Town"])
            loc = st.session_state["story_settings"]["town_loc"]
            st.session_state["message_history"].append({"role": "user", "content": f"Generate a scene in {adventure_options} where is in Town and I stumble upon a {loc}."})
            st.session_state["message_history"].append({"role": "system", "content": "You are a story generation assistant called ProcGenA that creates a scene based on a requested scene"})
            st.session_state["message_history"].append({"role": "system", "content": f"You will address the user character as {character_name}. The user's sex is {character_sex}. Some information about the user is {character_description}"})
            st.session_state["message_history"].append({"role": "system", "content": f"You will not hint at the user's next quest."})
            st.session_state["message_history"].append({"role": "system", "content": f"You will ask the user what the user wants to do at the end of the scene you generate"})
            response = await openai_api.call_openai(st.session_state["message_history"])
            st.session_state["message_history"].append({"role": "assistant", "content": f"{response}"})
            st.session_state["open_ai_response"] = response
            st.session_state["current_form"] = 2
            await scene_1()

        else:
            if not adventure_options:
                form1.warning("Missing adventure options")
            if not character_name:
                form1.warning("Missing name")
            if not character_sex:
                form1.warning("Missing sex")
            if not character_description:
                form1.warning("Missing description")

async def scene_1():
    """
    This function returns the first scene in the world
    Asks the user what the user will do in the situation
    """
    st.subheader(f"In World")
    st.markdown(st.session_state["open_ai_response"])
    form2 = st.form(f"In World")
    action = form2.text_input("What will you do?")
    submit2 = form2.form_submit_button("Confirm your action")
    story = st.session_state["story_scenes"]

    if submit2:
        quest_giver = random.choice(story[st.session_state["adventure_options"]]["Quest Giver"])
        quest = random.choice(story[st.session_state["adventure_options"]]["Adventure"])
        st.session_state["story_settings"]["quest_giver"] = quest_giver
        st.session_state["story_settings"]["quest"] = quest
        st.session_state["message_history"].append({"role": "user", "content": action})
        st.session_state["message_history"].append({"role": "system", "content": f"Based on the user input generate a scene where the user eventually stumbles upon {quest_giver} after the user's action. The {quest_giver} will give a quest on {quest} which the user will always accept."})
        st.session_state["message_history"].append({"role": "system", "content": f"You will ask the user what the user wants to do to prepare at the end of the scene you generate"})
        response = await openai_api.call_openai(st.session_state["message_history"])
        st.session_state["message_history"].append({"role": "assistant", "content": f"{response}"})
        st.session_state["open_ai_response"] = response
        st.session_state["current_form"] = 3
        await scene_2()
    else:
        form2.warning("Missing Action")

async def scene_2():
    """
    This function returns the second scene or the quest acceptance scene
    Asks the user what the user will do to prepare for the quest
    """
    st.subheader(f"In Adventure")
    st.markdown(st.session_state["open_ai_response"])
    form3 = st.form(f"In Adventure")
    action = form3.text_input("What will you do?")
    submit3 = form3.form_submit_button("Confirm your action")
    story = st.session_state["story_scenes"]

    if submit3:
        antagonist = random.choice(story[st.session_state["adventure_options"]]["Antagonist"])
        st.session_state["story_settings"]["antagonist"] = antagonist
        quest = st.session_state["story_settings"]["quest"]
        st.session_state["message_history"].append({"role": "user", "content": action})
        st.session_state["message_history"].append({"role": "system", "content": f"Based on the user input generate a scene the user then goes on to do {quest}. During the user's travels, he comes upon the {antagonist}"})
        st.session_state["message_history"].append({"role": "system", "content": f"The encounter will only have the {antagonist} and user merely meet each other"})
        st.session_state["message_history"].append({"role": "system", "content": f"You will ask the user what the user wants to do to defeat the {antagonist} the end of the scene you generate"})
        response = await openai_api.call_openai(st.session_state["message_history"])
        st.session_state["message_history"].append({"role": "assistant", "content": f"{response}"})
        st.session_state["open_ai_response"] = response
        st.session_state["current_form"] = 4
        await scene_3()
    else:
        form3.warning("Missing Action")

async def scene_3():
    """
    This function returns the third scene or the battle scene
    Asks the user what the user will do to defeat the antagonist
    """
    st.subheader("Battle")
    st.markdown(st.session_state["open_ai_response"])
    form4 = st.form(f"Battle")
    action = form4.text_input("What will you do?")
    submit4 = form4.form_submit_button("Confirm your action")
    story = st.session_state["story_scenes"]

    if submit4:
        conclusion = random.choice(story[st.session_state["adventure_options"]]["Conclusion"])
        quest = st.session_state["story_settings"]["quest"]
        antagonist = st.session_state["story_settings"]["antagonist"]
        st.session_state["story_settings"]["conclusion"] = conclusion
        st.session_state["message_history"].append({"role": "user", "content": action})
        st.session_state["message_history"].append({"role": "system", "content": f"Do not ask for user input"})
        st.session_state["message_history"].append({"role": "system", "content": f"Based on user input knowing that the input is merely an attempt, generate an outcome of the battle with user and {antagonist} with the conclusion that the user {conclusion}"})
        if conclusion == "User Celebrates":
            st.session_state["message_history"].append({"role": "system", "content": f"Continue the story of the user completing {quest} and then returning to the town and celebrating"})
        st.session_state["message_history"].append({"role": "system", "content": f"Conclude the quest"})
        response = await openai_api.call_openai(st.session_state["message_history"])
        st.session_state["message_history"].append({"role": "assistant", "content": f"{response}"})
        st.session_state["open_ai_response"] = response
        st.session_state["current_form"] = 5
        await scene_4()
    else: 
        form4.warning("Missing Action")

async def scene_4():
    """
    This function returns the conclusion
    Asks the user what the user will do to defeat the antagonist
    Allows the user to see a summary
    """
    st.subheader("Conclusion")
    st.markdown(st.session_state["open_ai_response"])
    form5 = st.form("Conclusion")
    submit5 = form5.form_submit_button("See Summary")


    if submit5:
        st.session_state["message_history"].append({"role": "user", "content": "Make a summary of the full story created from scenes."})
        response = await openai_api.call_openai(st.session_state["message_history"])
        st.session_state["message_history"].append({"role": "assistant", "content": f"{response}"})
        st.session_state["open_ai_response"] = response
        st.session_state["current_form"] = 6
        await scene_5()

async def scene_5():
    """
    This function returns the summary
    There is a download button for the story
    """
    st.subheader("Summary")
    st.markdown(st.session_state["open_ai_response"])
    st.download_button("Download Story", st.session_state["open_ai_response"])
    

if __name__ == "__main__":
    import asyncio
    asyncio.run(app())
