import subprocess
import shlex
from playsound import playsound
from youtubesearchpython import VideosSearch
from g4f.client import Client
import json

client = Client()

def download(song_name: str):

    videosSearch = VideosSearch(song_name)

    url = videosSearch.result()['result'][0]['link']

    if not url:
        raise ValueError("URL cannot be empty")

    # Command to download the audio
    command = f'yt-dlp --extract-audio --audio-format mp3 --output "{song_name}.mp3" "{url}"'

    try:
        # Split the command to ensure compatibility across platforms
        process = subprocess.run(shlex.split(command), check=True, capture_output=True, text=True)
        print("Download successful!\n", process.stdout)
    except subprocess.CalledProcessError as e:
        print("An error occurred:\n", e.stderr)

    playsound(f"{song_name}.mp3")

def recommend(init_song: str):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"You are the world's best and most advanced song recommendation engine that recommends the next 30 songs by just taking the first song as an input. Give me the next songs to play after {init_song} Only respond in a list that can be parsed through python with strings with song names. Don't write anything else. Don't write '''python or anything out of the []"}]
    )
    res=response.choices[0].message.content
    playlist=json.loads(res)
    return playlist

# Example usage
name=input('search: ')

download(name)
mix=recommend(name)
print(mix)

for i in mix:
    download(i)