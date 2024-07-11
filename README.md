# TrendTok

TrendTok is an innovative project designed to inspire content creators by generating new TikTok video ideas. Utilizing cutting-edge generative AI, this app provides short descriptions of novel video ideas, AI-generated music tracks, and visual templates to enhance the creative process. By analyzing existing trending TikTok videos, TrendTok helps creators develop unique and engaging content.

## Features

- **Trending Video Analysis**: Scrapes trending TikTok videos using Selenium and BeautifulSoup, supplemented by third-party APIs for comprehensive data collection.
- **Text Summarization**: Uses Python libraries such as Speech Recognition, Moviepy Editor, and Pytesseract (OCR) to process and summarize text from video content.
- **Idea Generation**: Leverages the Llama3 language model to generate new video ideas based on summarized data.
- **Audio Cue Generation**: Employs MusicGen to create original music tracks inspired by the generated video ideas.
- **Image Generation**: Utilizes Stable Diffusion to produce high-quality images as visual elements for the new video ideas.
- **Web App Integration**: Interactive frontend built with HTML, Bootstrap, and JavaScript, and backend powered by Flask, hosted on GCP for reliability and scalability.

## Technology Stack

- **Web Scraping**: Selenium, BeautifulSoup
- **Data Processing**: Python, Speech Recognition, Moviepy Editor, Pytesseract
- **Generative AI Models**: Llama3, MusicGen, Stable Diffusion
- **Frontend**: HTML, Bootstrap, JavaScript
- **Backend**: Flask
- **Hosting and Infrastructure**: Google Cloud Platform (GCP), Docker

## Installation

1. Clone the repository:
   ```bash
   $ git clone https://github.com/srivarshan-s/TikTok-Trend-Fusion.git
   $ cd TikTok-Trend-Fusion
   ```

2. Install the required dependencies:
   ```bash
   $ pip install -r requirements.txt
   ```

3. Set up environment variables for GCP and API keys (if any).

4. Run the Flask app:
   ```bash
   $ python app.py
   ```

## Usage

1. Access the web app through the local server.
2. Input the necessary parameters to start the data collection and idea generation process.
3. View and utilize the generated video ideas, music tracks, and visual templates.

## Challenges

- **Data Access**: Overcame restricted API access to TikTok data by utilizing web scraping, third-party APIs, public data repositories, and manual data collection.
- **Model Availability**: Dealt with limited availability of open-source generative models by finding suitable alternatives for music and image generation.
- **Compute Power**: Addressed high compute requirements by using lighter models and cloud-based APIs.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
