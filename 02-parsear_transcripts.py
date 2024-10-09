from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from tqdm import tqdm

prompt = """O texto a seguir é a transcrição de um vídeo do Youtube do canal Teo me Why, do Cientista de Dados Teo Calvo.

Os vídeos desse canal são aulas de assuntos relacionados a Ciencia de Dados, Estatística, Engenharia de Dados, etc.

Seu objetivo é resumir a transcrição abaixo, mencionando quais técnicas e ferramentas foram ensinadas na aula."""




load_dotenv(override=True)


GPT_MODEL = 'gpt-4o-mini'


def summarize_transcript(transcript: str, client):

    response = client.chat.completions.create(
    model = GPT_MODEL,


    messages=[
        {
        "role": "system",
        "content": [{"type": "text", "text": prompt}]
        },
        {
        "role": "user",
        "content": [{"type": "text", "text": transcript}]
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
    key = os.getenv("OPEN_AI_KEY")
    open_ai_client = OpenAI(api_key = key)



    # importar transcripts
    with open("data/transcripts.json", "r", encoding = 'utf-8') as f:
        dct_transcripts = json.load(f)

    output = []
    for transcript_data in tqdm(dct_transcripts):
        summary = summarize_transcript(transcript_data['transcript'], open_ai_client)
        output.append({'video_id': transcript_data['video_id'], 'summary': summary})

    with open('data/ai_summaries.json', 'w', encoding = 'utf-8') as file:
        json.dump(output, file, ensure_ascii = False) 


if __name__ == "__main__":
    main()