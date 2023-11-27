from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

video_id = 'ism-ctaSbw0'  # Replace with the actual video ID

try:
    # Retrieve the transcript and filter for English language
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_transcript(['en'])

    # Formatting the transcript to plain text
    formatter = TextFormatter()
    text_formatted = formatter.format_transcript(transcript.fetch())

    print(text_formatted)
except Exception as e:
    print("An error occurred:", e)
