# from youtube_transcript_api import YouTubeTranscriptApi
# from youtube_transcript_api.formatters import TextFormatter
# import re

# def get_video_id_from_url(url):
#     # Regular expression to extract the video ID from a YouTube URL
#     regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
#     match = re.search(regex, url)
#     return match.group(1) if match else None

# # Ask user for the YouTube video URL
# input_url = input("Enter the YouTube video URL: ")

# # Extract the video ID from the URL
# video_id = get_video_id_from_url(input_url)

# if video_id:
#     try:
#         # Retrieve the transcript and filter for English language
#         transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
#         transcript = transcript_list.find_transcript(['en'])

#         # Formatting the transcript to plain text
#         formatter = TextFormatter()
#         text_formatted = formatter.format_transcript(transcript.fetch())

#         print(text_formatted)
#     except Exception as e:
#         print("An error occurred:", e)
# else:
#     print("Invalid YouTube URL")

import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def youtube_video_search(query, api_key, max_results=5):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': max_results,
        'key': api_key
    }
    response = requests.get(search_url, params=params)
    
    if response.status_code != 200:
        return {"error": f"API request failed with status code {response.status_code}: {response.json()}"}
    
    data = response.json()
    if 'items' not in data:
        return {"error": "No items found in API response"}
    
    return data

def get_video_details(video_id, api_key):
    details_url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'snippet',
        'id': video_id,
        'key': api_key
    }
    response = requests.get(details_url, params=params)
    
    if response.status_code != 200:
        return {"error": f"API request failed with status code {response.status_code}: {response.json()}"}

    data = response.json()
    if 'items' not in data or not data['items']:
        return {"error": "No video details found"}
    
    return data

def get_full_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])
        formatter = TextFormatter()
        return formatter.format_transcript(transcript.fetch())
    except Exception as e:
        return f"An error occurred while fetching transcript: {e}"


def main():
    api_key = 'AIzaSyBDQykEA_vJuW-IwKiZBgBYqqIn4qd9nXE'  # Replace with your YouTube Data API key
    query = input("Enter your search query: ")
    results = youtube_video_search(query, api_key)

    if "error" in results:
        print(results["error"])
        return

    for i, item in enumerate(results['items'], start=1):
        print(f"{i}. Title: {item['snippet']['title']}, Video ID: {item['id']['videoId']}")

    try:
        choice = int(input("Select a video (1-5): "))
        selected_video = results['items'][choice - 1]
    except (IndexError, ValueError):
        print("Invalid selection")
        return

    video_details = get_video_details(selected_video['id']['videoId'], api_key)
    if "error" in video_details:
        print(video_details["error"])
        return

    video_description = video_details['items'][0]['snippet']['description']
    print(f"You selected: {selected_video['snippet']['title']}")
    print("Summary/Description:")
    print(video_description)

    transcript_choice = input("Do you want the full transcript of the video? (yes/no): ").lower()
    if transcript_choice == 'yes':
        full_transcript = get_full_transcript(selected_video['id']['videoId'])
        print("Full Transcript:")
        print(full_transcript)

if __name__ == "__main__":
    main()
