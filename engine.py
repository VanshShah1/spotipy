import subprocess
import shlex
from playsound import playsound
from youtubesearchpython import VideosSearch
from g4f.client import Client
import json

client = Client()

def search(song_name: str):

    videosSearch = VideosSearch(song_name, limit = 2)

    return videosSearch.result()['result'][0]['link']

def recommend(song_name: str):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"You are the world's best and most advanced song recommendation engine that recommends the next 30 songs by just taking the first song as an input. Give me the next songs to play after {song_name} Only respond in a list that can be parsed through python with strings with song names. Don't write anything else. Don't write '''python or anything out of the []"}]
    )
    res=response.choices[0].message.content
    playlist=json.loads(res)
    return playlist

def download(url):
    """
    Downloads audio from the given URL using yt-dlp and saves it as an MP3 file.

    Args:
        url (str): The URL of the video to download the audio from.

    Returns:
        None
    """
    if not url:
        raise ValueError("URL cannot be empty")

    # Command to download the audio
    command = f'yt-dlp --extract-audio --audio-format mp3 --output "output.mp3" "{url}"'

    try:
        # Split the command to ensure compatibility across platforms
        process = subprocess.run(shlex.split(command), check=True, capture_output=True, text=True)
        print("Download successful!\n", process.stdout)
    except subprocess.CalledProcessError as e:
        print("An error occurred:\n", e.stderr)

# Example usage
name=input('search: ')
link=search(name)
download(link)
playsound("output.mp3")