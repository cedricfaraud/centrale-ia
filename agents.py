import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# --- Clients API gratuits ---
groq = OpenAI(
    api_key=os.environ("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

deepseek = OpenAI(
    api_key=os.environ("DEEPSEEK_API_KEY"),
    base_url=""https://api.deepseek.com/v1",
)

gemini = OpenAI(
    api_key=os.environ("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# --- Agents IA gratuits ---

def orchestrateur(prompt: str) -> str:
    r = groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content

def architecte(prompt: str) -> str:
    r = groq.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content

def dev(prompt: str) -> str:
    r = deepseek.chat.completions.create(
        model="deepseek-reasoner",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content

def po(prompt: str) -> str:
    r = groq.chat.completions.create(
        model="mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content

def ivvq(prompt: str) -> str:
    r = groq.chat.completions.create(
        model="phi-3-mini-4k-instruct",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content
