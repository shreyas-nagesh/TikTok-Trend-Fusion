from flask import Flask, render_template, request, jsonify, url_for, session, send_from_directory
from flask_bootstrap import Bootstrap
from music_gen.api import gen_api
from summariser.llama_api import llama_api
from tiktok_to_text.api import t4_api
from tiktok_videos.download import download_videos
from animate_text.api import generate_image
import json
import os
import secrets

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = secret_key
Bootstrap(app)


@app.route('/')
def home():
    trending_tags = ["MakeupTutorial", "BeautyHacks", "SkincareRoutine",  "TravelVlog", "HiddenGems",
                     "TravelTips", "Foodie", "RecipeOfTheDay", "CookingHacks", "OOTD", "FashionInspo",
                     "StyleTips", "AI", "MachineLearning", "TechInnovation"]

    return render_template('index.html', trending_tags=trending_tags)


def extract_value_from_json(json_string):
    try:
        data = json.loads(json_string)
        if isinstance(data, list) and len(data) > 0 and "value" in data[0]:
            return data[0]["value"]
        else:
            return None
    except json.JSONDecodeError:
        return None


@app.route('/search', methods=['POST'])
def search():
    search_tags = extract_value_from_json(request.form.get('search_tags'))
    output_dir = os.path.join('static', 'video', search_tags)

    # Download videos for the given tags
    video_files = download_videos(search_tags, output_dir)

    video_urls = [url_for('static', filename=os.path.join(
        'video', search_tags, os.path.basename(video))) for video in video_files]

    # Convert video URLs to absolute paths
    base_dir = os.path.abspath(os.path.dirname(__file__))
    absolute_video_paths = [os.path.join(
        base_dir, url.lstrip('/')) for url in video_files]

    session['video_urls'] = absolute_video_paths
    return render_template('video.html', video_urls=video_urls)


@ app.route('/generate_idea', methods=['POST'])
def generate_idea():
    video_urls = session.get('video_urls', [])

    text_summary = t4_api(video_urls)

    # Get the idea and song descriptions from the Llama API
    idea_description, song_description = llama_api(text_summary)

    print("Idea Description:", idea_description)
    print("Song Description:", song_description)

    # Extract the "Trend Name"
    trend_name_start = idea_description.find(
        "Trend Idea:") + len("Trend Idea:")
    trend_name_end = idea_description.find("Trend Concept:")
    trend_name = idea_description[trend_name_start:trend_name_end].strip().strip(
        '"')

    print("Trend Name:", trend_name)

    # Extract the "Video Idea"
    video_idea_start = idea_description.find(
        "Trend Concept:") + len("Trend Concept:")
    video_idea = idea_description[video_idea_start:].strip()
    video_idea_lines = video_idea.split('\n')
    formatted_video_idea = '\n'.join(line.strip() for line in video_idea_lines)

    print("Trend Idea:", formatted_video_idea)

    # Store song description in session for later use
    session['idea'] = trend_name
    session['tags'] = text_summary["tags"]
    session['song_description'] = song_description
    session['concept'] = formatted_video_idea

    return jsonify(idea=trend_name, concept=formatted_video_idea)


@ app.route('/generate_media', methods=['POST'])
def generate_media():
    song_description = session.get('song_description', '')
    tags = session.get('tags', '')

    if not song_description or not tags:
        return jsonify(error="Missing data for generating media"), 400

    # Generate the image using the tags
    output_img_path = os.path.join('static', 'gen_img', f"{tags[0]}.png")
    generate_image(tags, output_img_path)
    img_url = url_for('static', filename=f'gen_img/{tags[0]}.png')

    # Generate the audio using the song description
    output_file_path = gen_api(song_description, 'new_audio', 6)

    audio_url = url_for(
        'static', filename=f'audio/{os.path.basename(output_file_path)}')

    return jsonify(audio_url=audio_url, img_url=img_url)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)
