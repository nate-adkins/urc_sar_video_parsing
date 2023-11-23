from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import youtube_dl, time


def make_text_file(file_path, video_id):

    def edit_file_path(file_path: str):
        replacements = {
            " " : "",
            "(" : "",
            ")" : "",
            "|" : "",
            "-" : "",
        }
        for old, new in replacements.items():
            file_path = file_path.replace(old,new)
        return file_path

    file_path = edit_file_path(file_path)
    file_path = 'transcript_txt_files/' + file_path + ".txt"
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception:
        print(f"Subtitles are disabled for the video, or no transcript was found {video_id}. Skipping.")
        return
    
    lines_to_write = []
    for entry in transcript:
        lines_to_write.append(f"{entry['text']}\n")
    try:
        with open(file_path, 'w+') as new_file:
            new_file.writelines(lines_to_write)
    except Exception:
        print(f"File error, skipping")
        return


def get_playlist_video_info(playlist_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        videos_infos: set[tuple] = set()
        result = ydl.extract_info(playlist_url, download=False)
        if 'entries' in result:
            for entry in result['entries']:
                videos_infos.add ( (entry.get('title'),entry.get('id')) )
            return videos_infos
        else:
            print("Error: No entries found in the playlist.")
    
def main():

    playlist_urls = [
        'https://www.youtube.com/playlist?list=PL8VXKzY8zO8Cle1ltnLs2RgtIoTcVrej7',
        'https://www.youtube.com/playlist?list=PLePCRhtF7zrlzh5kXzE2bESCGdsBx5Oow',
        'https://www.youtube.com/playlist?list=PLdPXMBV9SaMoP2EnJLIJ2HZFd8eI51q1B',
        'https://www.youtube.com/playlist?list=PLH_v4Qj_GKVcIn2oxwAfCaYctuWWM7MGf',
        'https://www.youtube.com/playlist?list=PLDjFZI4B9-rf74VsseicguMce2tkQ21Tf',
        'https://www.youtube.com/playlist?list=PLfMVUdvyZKfYL3RMu0c1OvKN38Y9pFq-w',
        'https://www.youtube.com/playlist?list=PLdPXMBV9SaMpVcYexiFF7-EaW9RBycxgt',
        'https://www.youtube.com/playlist?list=PLGGb8VbYzyu3FD16khYW5ryE8mNWLUkp4',
        'https://www.youtube.com/playlist?list=PLoLCkGATi6LTnTwVfXQ-nz6MdpMJ9lYqF'
    ]

    start_time = time.time()
    for url in playlist_urls:
        videos_info = get_playlist_video_info(url)
        for video in videos_info:
            make_text_file(video[0],video[1])
    end_time = time.time()
    total_time = end_time - start_time

    print(f'The transcript generation took {total_time} seconds')

if __name__ == '__main__':
    main()
