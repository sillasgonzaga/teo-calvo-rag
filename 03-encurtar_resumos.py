from dotenv import load_dotenv
from openai import OpenAI
import os
import json
from tqdm import tqdm

load_dotenv(override=True)


INPUT_FILE = 'data/ai_summaries.json'
GPT_MODEL = 'gpt-4o-mini'
key = os.getenv("OPEN_AI_KEY")
open_ai_client = OpenAI(api_key = key)


def load_data(file_path):
    with open(file_path, 'r') as file:
        video_data = json.load(file)
    return video_data

def shorten_video_summary(video_summary: str, open_ai_client):
    system_prompt = "Resuma e formate o texto abaixo em um único parágrafo."
    response = open_ai_client.chat.completions.create(
    model = GPT_MODEL,


    messages=[
        {
        "role": "system",
        "content": [{"type": "text", "text": system_prompt}]
        },
        {
        "role": "user",
        "content": [{"type": "text", "text": video_summary}]
        }
    ],
    temperature=0,
    max_tokens=2560,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    return response.choices[0].message.content


def main():
    # carregar dados
    lst_transcripts = load_data(INPUT_FILE)

    output = []
    for tr_data in tqdm(lst_transcripts):
        short_summary = shorten_video_summary(tr_data['summary'], open_ai_client)
        output.append({'video_id': tr_data['video_id'], 'short_summary': short_summary})
    

    with open('data/ai_short_summaries.json', 'w', encoding = 'utf-8') as file:
        json.dump(output, file, ensure_ascii = False) 

if __name__ == "__main__":
    main()