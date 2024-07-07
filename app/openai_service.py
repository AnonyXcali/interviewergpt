import requests
import os
from flask import Response, stream_with_context

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'

def get_openai_response(prompt):
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a coding interview preparation assistant that helps the user to prepare for interviews for companies like FAANG."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
    return response.json()


def get_openai_response_stream(prompt):
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a coding interview preparation assistant that helps the user to prepare for interviews for companies like FAANG."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150,
        "stream": True  # Enable streaming mode
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, stream=True)

    def generate():
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                yield f"data: {decoded_line}\n\n"
        yield "event: end\ndata: end\n\n"  # Indicate end of the stream

    return Response(stream_with_context(generate()), content_type='text/event-stream')