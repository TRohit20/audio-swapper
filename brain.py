import os
from urllib.parse import parse_qs, urlparse
from moviepy.editor import AudioFileClip
from pytube import YouTube
from openai import OpenAI
from dotenv import load_dotenv
import goslate

load_dotenv()

def extract_audio(url: str) -> [str,str]:

    yt = YouTube(url)

    # Extract the video_id from the url
    query = urlparse(url).query
    params = parse_qs(query)
    video_id = params["v"][0]

    # Get the first available audio stream and download it
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(output_path="tmp/")

    # Convert the downloaded audio file to mp3 format
    audio_path = os.path.join("tmp/", audio_stream.default_filename)
    audio_clip = AudioFileClip(audio_path)
    audio_clip.write_audiofile(os.path.join("tmp/", f"{video_id}.mp3"))

    # Delete the original audio stream
    os.remove(audio_path)

    return f"tmp/{video_id}.mp3", video_id

def extract_transcript_from_audio(file_path, video_id):
        
        print("Transcription in process")

        # The path of the transcript
        transcript_filepath = f"tmp/{video_id}.txt"

        # Get the size of the file in bytes
        file_size = os.path.getsize(file_path)

        # Convert bytes to megabytes
        file_size_in_mb = file_size / (1024 * 1024)

        # Check if the file size is less than 25 MB
        if file_size_in_mb < 25:
            with open(file_path, "rb") as audio_file:
                client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
                transcript = client.audio.transcriptions.create(model= "whisper-1",file= audio_file, response_format="text")
                
                # Writing the content of transcript into a txt file
                with open(transcript_filepath, 'w') as transcript_file:
                    transcript_file.write(transcript)

            # Deleting the mp3 file
            # os.remove(file_path)
            return transcript_filepath
        else:
            print("Please provide a smaller audio file (less than 25mb).")

        print("exiting transcription function")

def translate_to_hindi(file_path: str):
    translator = goslate.Goslate()
    with open(file_path, "r") as file:
        content = file.read()
        translation = translator.translate(content, 'hi')
    
    translated_file_path = file_path.replace(".txt", "_translated.txt")
    with open(translated_file_path, 'w') as translated_file:
        translated_file.write(translation)
    
    return translated_file_path
