import os
from typing import Dict, List

import moviepy.editor as mp
import speech_recognition as sr
from llamaapi import LlamaAPI


def llama_api_summary_tag(desc: str) -> str:
    """
    Generate a summary and tags/keywords for a given text using the LlamaAPI.

    Parameters:
    desc (str): The input text to be summarized and tagged.

    Returns:
    str: The summarized text along with tags/keywords.
    """
    llama = LlamaAPI(
        "LL-vc1xoxRAiBZbaAVEhMGkYyHc1PEn0uw8elJirZRKZwcqosPJj38B8idwX0aT0Dvi"
    )

    # API Request JSON structure
    api_request_summarize_tags = {
        "model": "llama3-8b",
        "messages": [
            {
                "role": "system",
                "content": "Summarize the sentences in less than 80 words. Give the top tags/keywords for this summarized text (at least one tag for each sentence) along with the summarized text.",
            },
            {"role": "user", "content": desc},
        ],
    }

    # Make the API request and handle the response
    response_summary_tag = llama.run(api_request_summarize_tags)
    return response_summary_tag.json()["choices"][0]["message"]["content"]


def text_cleaning(input_text: str):
    """
    Clean and extract the summary and tags from the input text.

    Parameters:
    input_text (str): The raw input text containing the summary and tags.

    Returns:
    tuple: A tuple containing the cleaned summary and tags.
    """
    # Define delimiters for extracting summary and tags
    summary_start = "Here is a summary of the text in under 80 words:\n\n"
    summary_end = "\n\nTop tags/keywords:\n\n"
    tags_start = "\n\nTop tags/keywords:\n\n"

    # Extract the summary text
    summary_text = input_text[
        input_text.find(summary_start) + len(summary_start): input_text.find(
            summary_end
        )
    ].strip()

    # Extract the tags text
    tags_text = input_text[input_text.find(
        tags_start) + len(tags_start):].strip()
    tags_text = tags_text.replace("* ", "").replace("\n*", "\n").strip()

    return summary_text, tags_text


def transcribe_audio_from_video(video_file):
    """
    Transcribe audio from a given video file using Google Speech Recognition.

    Parameters:
    video_file (str): The path to the video file.

    Returns:
    str: The transcribed text from the video.
    """
    # Load the video file
    video = mp.VideoFileClip(video_file)

    # Extract audio from the video
    audio = video.audio
    audio.write_audiofile("temp_audio.wav")

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load and transcribe the audio file
    audio_file = sr.AudioFile("temp_audio.wav")
    with audio_file as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)

    return text


def t4_api(video_files: List[str]) -> Dict:
    """
    Main function to process multiple video files, transcribe their audio,
    and summarize the transcriptions with tags/keywords.

    Parameters:
    video_files (List[str]): A list of paths to video files.

    Returns:
    Dict: A dictionary containing the summarized text and tags.
    """
    all_transcriptions = []

    # Process each video file
    for video_file in video_files:
        # Transcribe audio from the video
        transcription = transcribe_audio_from_video(video_file)
        all_transcriptions.append(transcription)
        print(f"Transcription for {video_file}:\n{transcription}\n")

        # Clean up temporary audio file
        os.remove("temp_audio.wav")

    # Combine all transcriptions into one text
    all_transcriptions_text = "\n\n".join(all_transcriptions)

    # Summarize the combined transcriptions and extract tags
    summary_tag = llama_api_summary_tag(all_transcriptions_text)
    summary_text, tags_text = text_cleaning(summary_tag)

    return {
        "summary": summary_text,
        "tags": tags_text,
    }
