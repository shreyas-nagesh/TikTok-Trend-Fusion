from llamaapi import LlamaAPI


def llama_api(desc: str) -> str:
    llama = LlamaAPI(
        'LL-vc1xoxRAiBZbaAVEhMGkYyHc1PEn0uw8elJirZRKZwcqosPJj38B8idwX0aT0Dvi')

    # API Request JSON Cell
    api_request_idea = {
        "model": "llama3-8b",
        "messages": [
            {
                "role": "system",
                "content": "You are a TikTok trend idea generator which can come up with a new trend idea. Your response should include a title starting with 'Trend Idea:', followed by a concise description starting with 'Trend Concept:'."
            },
            {
                "role": "user",
                "content": desc["tags"],
            },
        ],
        "max_tokens": 250,
        "stream": False
    }

    api_request_song = {
        "model": "llama3-8b",
        "messages": [
            {"role": "system", "content": "You are a tiktok trend generator which can take tags and generate audio cues to be given to a Music generator model. Your response includes only the audio description for a 5 second clip. It is very concise."},
            {"role": "user", "content": desc["tags"]},
        ]
    }

    # Make your request and handle the response
    response_idea = llama.run(api_request_idea)
    response_song = llama.run(api_request_song)
    return response_idea.json()['choices'][0]['message']['content'], response_song.json()['choices'][0]['message']['content']
