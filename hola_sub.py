from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re

def get_video_id_from_url(url):
    # Regular expression to extract the video ID from a YouTube URL
    regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

# Ask user for the YouTube video URL
input_url = input("Enter the YouTube video URL: ")

# Extract the video ID from the URL
video_id = get_video_id_from_url(input_url)

if video_id:
    try:
        # Retrieve the transcript and filter for English language
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])

        # Formatting the transcript to plain text
        formatter = TextFormatter()
        text_formatted = formatter.format_transcript(transcript.fetch())

        # Save the transcript to a text file
        with open(f"{video_id}_transcript.txt", "w") as file:
            file.write(text_formatted)

        print(f"Transcript saved as {video_id}_transcript.txt")
    except Exception as e:
        print("An error occurred:", e)
else:
    print("Invalid YouTube URL")
