import os
from google import genai
from dotenv import load_dotenv
load_dotenv()
import requests

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

def call_gemini(prompt, max_tokens=300):
    from google import genai
    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY not set in .env")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


def call_openai_chat(prompt, max_tokens=300, temperature=0.2):
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set in .env")
    import openai
    openai.api_key = OPENAI_API_KEY
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini" if hasattr(openai, 'gpt') else "gpt-4o",
        messages=[{"role":"system","content":"You are a concise e-commerce analytics assistant."},{"role":"user","content":prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return resp['choices'][0]['message']['content']

'''def call_openrouter(prompt, model="gpt-4o-mini", max_tokens=300):
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set in .env")
    url = "https://api.openrouter.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    data = {"model": model, "messages":[{"role":"system","content":"You are a concise e-commerce analytics assistant."},{"role":"user","content":prompt}], "max_tokens":max_tokens}
    r = requests.post(url, json=data, headers=headers)
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']

def call_gemini(prompt, max_tokens=300):
    try:
        import google.generativeai as genai
    except Exception as e:
        raise RuntimeError("google-generativeai package not available. Install and set GOOGLE_API_KEY.") from e
    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY not set in .env")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = "gemini-pro"
    response = genai.generate_text(model=model, prompt=prompt, max_output_tokens=max_tokens)
    if hasattr(response, "text"):
        return response.text
    return response.candidates[0].output'''

def call_llm(prompt, provider_priority=('google','openai')):
    last_exc = None
    for p in provider_priority:
        try:
            if p == 'google' and GOOGLE_API_KEY:
                return call_gemini(prompt)
            if p == 'openai' and OPENAI_API_KEY:
                return call_openai_chat(prompt)
        except Exception as e:
            last_exc = e
            continue
    raise RuntimeError("No LLM available or all providers failed.") from last_exc
