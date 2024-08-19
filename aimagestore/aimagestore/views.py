import os
import requests
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.http import JsonResponse

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OpenAI API Key is not found. Please set OPENAI_API_KEY environment variable.")

api_url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {openai_api_key}",
    "Content-Type": "application/json"
}


def truncate_to_last_sentence(text):
    last_punctuation = max(text.rfind('.'), text.rfind('!'), text.rfind('?'))

    if last_punctuation != -1:
        return text[:last_punctuation + 1]
    else:
        return text


def chat_with_bot(request):
    user_input = request.GET.get('message', '')
    if user_input:
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            "max_tokens": 200,
            "temperature": 0.5,
        }

        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            response_text = response_data['choices'][0]['message']['content'].strip()

            response_text = truncate_to_last_sentence(response_text)
        else:
            response_text = "Sorry, something went wrong with the API request."
    else:
        response_text = "I didn't get that. Can you please rephrase?"

    return JsonResponse({'response': response_text})


def home(request):
    trans = _('Hello!')
    return render(request, 'aimagestore/home.html', {'trans': trans})
