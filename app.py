import streamlit as st
from google import genai

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

PERSONA = (
    "You are Big-O Bot, a friendly and patient computer science tutor helping a "
    "complete beginner understand Time Complexity and Big-O notation. Always use "
    "simple, everyday language and relatable analogies before introducing any "
    "technical terms or math. Keep explanations short (under 150 words) unless "
    "asked for more detail. Be encouraging and never condescending, even if the "
    "learner gets something wrong."
)

st.set_page_config(page_title="Big-O Bot - AI Learning Buddy", page_icon="🎓")
st.title("🎓 Big-O Bot — AI Learning Buddy")
st.caption("Your friendly tutor for Time Complexity & Big-O Notation")

topic = st.text_input("Enter a Topic", value="Time Complexity")

option = st.selectbox(
    "Choose Activity",
    [
        "Explain Concept",
        "Real-Life Example",
        "Generate Quiz",
        "Evaluate My Answer",
        "Full Session (Explain + Example + Quiz)"
    ]
)

learner_answer = ""
if option == "Evaluate My Answer":
    learner_answer = st.text_area("Type your answer here")

if st.button("Generate"):
    if topic == "":
        st.warning("Please enter a topic.")
    else:
        if option == "Explain Concept":
            prompt = f"{PERSONA}\n\nExplain {topic} in simple language for a beginner."
        elif option == "Real-Life Example":
            prompt = f"{PERSONA}\n\nGive one clear, real-life, non-technical example of {topic}, and explain how it maps to the concept."
        elif option == "Generate Quiz":
            prompt = f"{PERSONA}\n\nCreate 5 multiple-choice quiz questions on {topic} for a beginner. Include 4 options each, mark the correct answer, and briefly explain why."
        elif option == "Evaluate My Answer":
            if learner_answer.strip() == "":
                st.warning("Please type your answer first.")
                st.stop()
            prompt = f"{PERSONA}\n\nA learner gave this answer about {topic}: '{learner_answer}'. Evaluate if it's correct, explain why, and give one tip to improve."
        else:
            prompt = (
                f"{PERSONA}\n\nTeach {topic} to a beginner. Include: (1) a simple "
                f"explanation, (2) one real-life example, and (3) a short 5-question quiz "
                f"with answers. Present all three clearly labeled."
            )

        with st.spinner("Big-O Bot is thinking..."):
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )
        st.write(response.text)
