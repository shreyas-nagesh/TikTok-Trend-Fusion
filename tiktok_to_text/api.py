import os
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

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
        "LL-5jGRFRsV3TctJy0qMVwno5LKiAoWEHreyTZVCbNrUJVaUp3AcAB3HqiRH1dCpzSi"
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
    name = video_file.split('.')[0].split('/')[-1]
    audio.write_audiofile(f"temp_audio{name}.wav")

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load and transcribe the audio file
    audio_file = sr.AudioFile(f"temp_audio{name}.wav")
    with audio_file as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(
            audio_data, language='en')

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
    def process_video(video_file):
        # Transcribe audio from the video
        transcription = transcribe_audio_from_video(video_file)
        print(f"Transcription for {video_file}:\n{transcription}\n")

        return transcription

    all_transcriptions = []

    # Use ThreadPoolExecutor to parallelize the processing of video files
    with ThreadPoolExecutor() as executor:
        future_to_video = {executor.submit(process_video, video_file): video_file for video_file in video_files}
        for future in as_completed(future_to_video):
            video_file = future_to_video[future]
            try:
                transcription = future.result()
                all_transcriptions.append(transcription)
            except Exception as e:
                print(f"Exception occurred while processing {video_file}: {e}")

    # Combine all transcriptions into one text
    all_transcriptions_text = "\n\n".join(all_transcriptions)

    # Summarize the combined transcriptions and extract tags
    summary_tag = llama_api_summary_tag(all_transcriptions_text)
    summary_text, tags_text = text_cleaning(summary_tag)

    # Clean up temporary audio file
    name = [video_file.split('.')[0].split('/')[-1] for video_file in video_files]
    for i in name:
        os.remove(f"temp_audio{i}.wav")

    return {
        "summary": summary_text,
        "tags": tags_text,
    }