import yt_dlp
from typing import List, Tuple
import json
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from xml.etree import ElementTree
from tqdm import tqdm

teo_channel_url = 'https://www.youtube.com/@teomewhy'

def get_video_ids_from_channel(channel_url) -> Tuple[str, List[str]]:
    video_ids = []
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Only extract information without downloading
        'force_generic_extractor': False,  # Allow specialized extractors
        'skip_download': True,  # No downloading
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Attempting to extract video information from the channel URL
            results = ydl.extract_info(channel_url, download=False)
            try:
                video_metadatas = results['entries'][0]['entries']
            except KeyError:
                video_metadatas = results['entries']
            # Extracting video IDs
            video_ids = [v.get('id') for v in video_metadatas]
            channel_id = results.get('channel_id', '')
        except yt_dlp.utils.DownloadError as e:
            # Handling the case where the channel URL is invalid or the channel no longer exists
            print(f"Error: Unable to download API page for {channel_url}: {e}")
            channel_id = ''
            video_ids = []

    return channel_id, video_ids

def extract_transcript_as_text(video_id: str) -> str:
    error = None
    try:
        transcript = list(YouTubeTranscriptApi.list_transcripts(video_id))[0]
        transcript_dict = transcript.fetch()
        transcript_text = [t['text'] for t in transcript_dict]
        transcript_text = '\n'.join(transcript_text)
    # if transcripts are not available, store in file
    except TranscriptsDisabled as e:
        error = "TranscriptsDisabled"
        transcript_text = None
    except NoTranscriptFound:
        error = "NoTranscriptFound"
        transcript_text = None
    except ElementTree.ParseError:
        error = "XMLError"
        transcript_text = None
    
    return transcript_text, error



def main():
    channel_id, video_ids = get_video_ids_from_channel(channel_url=teo_channel_url)
    
    # extract transcripts
    print(f'Extracting transcripts for {len(video_ids)} videos')


    output = []
    for video_id in tqdm(video_ids):
        transcript, error = extract_transcript_as_text(video_id)
        if transcript:
            output.append({'video_id': video_id, 'transcript': transcript})
    
    print(f'Saving valid transcripts for {len(output)} videos')
    with open('data/transcripts.json', 'w', encoding = 'utf-8') as file:
        json.dump(output, file, ensure_ascii=False)


if __name__ == "__main__":
    main()
