import os
import streamlit as st
from groq import Groq
import clipboard

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="English -> LinkedIn")

st.title("English → LinkedIn")
st.text("Convert text into LinkedIn Slop")

input_text = st.text_area("Enter your sentence:")

STYLE_PROMPT = """
Convert the given text into an exaggerated LinkedIn-style post.

Rules:
- Add unnecessary storytelling (if possible)
- Use corporate buzzwords
- Add fake emotional depth
- Include a "lesson" or "insight" (if possible)
- Use line breaks for drama
- Add 2–5 emojis max
- Keep it cringe but readable
- Add multiple hashtags
"""

def generate_slop(text: str) -> str | None:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": STYLE_PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=0.9,
        max_tokens=1000,
    )
    return response.choices[0].message.content


if st.button("Convert"):
    if not input_text.strip():
        st.warning("Enter some text")
        st.stop()
    with st.spinner("Generating slop..."):
        output = generate_slop(input_text)
    if output is None:
        st.error("A problem occured, please try again.")
        st.stop()

    st.markdown("### Output:")
    with st.container(border=True):
        st.markdown(output)
    if st.button("Copy 📋"):
        clipboard.copy(output)
