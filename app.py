import streamlit as st
from brain import extract_audio, extract_transcript_from_audio, translate_to_hindi

with st.sidebar:
    st.markdown("### Audio Swapper")

    st.markdown("## What's Audio Swapper ?")
    st.markdown("""<div style="text-align: justify;">Extract audio of a video, convert the audio into a regional language like Hindi and merge back into the video. <br></div>""", unsafe_allow_html=True)

st.markdown("# Audio Swapper")
# st.markdown("### Enter a YT Video URL")
URL = st.text_input("Enter a Video URL:", placeholder="https://www.youtube.com/watch?v=************")
button = st.button("Extract Transcript!")

if button:
    with st.spinner("Extracting Audio"):
        audio_file_path, video_id = extract_audio(url=URL)
        transcript_filepath = extract_transcript_from_audio(file_path=audio_file_path,video_id=video_id)
        translated_text_filepath = translate_to_hindi(transcript_filepath)
        st.markdown(translated_text_filepath)

