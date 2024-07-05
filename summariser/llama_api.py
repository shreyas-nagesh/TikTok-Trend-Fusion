from llamaapi import LlamaAPI

def llama_api(desc: str) -> str:
    llama = LlamaAPI('LL-hnLAldQnBSQkOtMJcXBNfIRagQyCCKyMFDwL96NhNdNdhj0UIP1DdF8v3AGpRuxK')

    # API Request JSON Cell
    api_request_idea = {
    "model": "llama3-8b",
    "messages": [
        {"role": "system", "content": "You are a tiktok trend generator which can summarise ideas and come up with something new and generate a concise concept."},
        {"role": "user", "content": desc},
    ]
    }

    api_request_song = {
    "model": "llama3-8b",
    "messages": [
        {"role": "system", "content": "You are a tiktok trend generator which can take tags and generate audio cues to be given to a Music generator model. Your response includes only the audio description for a 5 second clip. It is very concise."},
        {"role": "user", "content": desc},
    ]
    }

    # Make your request and handle the response
    response_idea = llama.run(api_request_idea)
    response_song = llama.run(api_request_song)
    return response_idea.json()['choices'][0]['message']['content'], response_song.json()['choices'][0]['message']['content']