from llamaapi import LlamaAPI

def llama_api(desc: str) -> str:
    llama = LlamaAPI('LL-hnLAldQnBSQkOtMJcXBNfIRagQyCCKyMFDwL96NhNdNdhj0UIP1DdF8v3AGpRuxK')

    # API Request JSON Cell
    api_request_json = {
    "model": "llama3-8b",
    "messages": [
        {"role": "system", "content": "You are a tiktok trend generator which can summarise ideas and come up with something new outputting only an example. Your generated text will be used to generate music with MusicGen."},
        {"role": "user", "content": desc},
    ]
    }

    # Make your request and handle the response
    response = llama.run(api_request_json)
    return response.json()['choices'][0]['message']['content']