import yt_dlp

playlist_url = input("Submit your playlist URL here: ")

def download_playlist(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best[ext=mp4]',  # Ensures highest resolution video in MP4 format
        'outtmpl': './video/playlist/%(playlist)s/%(title)s.%(ext)s',  # Save videos in a directory with playlist name
        'merge_output_format': 'mp4',  # Ensure the output format is MP4
        'ignoreerrors': True,  # Ignore errors for deleted or private videos in the playlist
        'quiet': False  # Print all messages to stdout
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_dict = ydl.extract_info(url, download=True)
        
        if 'entries' in playlist_dict:
            playlist_title = playlist_dict['title']
            print(f"Downloading playlist: {playlist_title}")
            for video in playlist_dict['entries']:
                video_title = video['title']
                print(f"Downloading video: {video_title}")
                ydl.download([video['url']])
        else:
            print("No videos found in playlist.")

download_playlist(playlist_url)
