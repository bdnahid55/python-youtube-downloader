# /video_downloader_with_subs.py
import yt_dlp

playlist_url = input("Submit your playlist URL here: ")

def download_playlist(url):
    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[ext=mp4][height<=720]',
        'outtmpl': './video/playlist/%(playlist)s/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'ignoreerrors': True,
        'quiet': False,

        # Subtitle options
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'subtitlesformat': 'best',
        'embedsubtitles': True,
        'postprocessors': [{
            'key': 'FFmpegEmbedSubtitle'
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_dict = ydl.extract_info(url, download=True)

        if 'entries' in playlist_dict:
            playlist_title = playlist_dict.get('title', 'Untitled Playlist')
            print(f"Downloading playlist: {playlist_title}")
            for video in playlist_dict['entries']:
                if video:
                    video_title = video.get('title', 'Unknown Title')
                    print(f"Downloading video: {video_title}")
                    ydl.download([video['webpage_url']])
        else:
            print("No videos found in playlist.")

download_playlist(playlist_url)
