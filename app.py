import streamlit as st
from brain import extract_audio

with st.sidebar:
    st.markdown("### Audio Swapper")

    st.markdown("## What's Audio Swapper ?")
    st.markdown("""<div style="text-align: justify;">Extract audio of a video, convert the audio into a regional language like Hindi and merge back into the video. <br></div>""", unsafe_allow_html=True)

st.markdown("# Audio Swapper")
# st.markdown("### Enter a YT Video URL")
URL = st.text_input("Enter a Video URL:", placeholder="https://www.youtube.com/watch?v=************")
button = st.button("Extract Audio!")

if button:
    with st.spinner("Extracting Audio"):
        audio = extract_audio(url=URL)
