import yt_dlp
import tkinter as tk
from tkinter import ttk, messagebox
import threading

# Function to update progress bar
def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded_bytes = d.get('downloaded_bytes', 0)
        total_bytes = d.get('total_bytes', 1)
        percent = (downloaded_bytes / total_bytes) * 100
        progress_var.set(percent)
        root.update_idletasks()

# Function to download video or playlist
def download():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a video or playlist URL.")
        return

    progress_var.set(0)

    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[ext=mp4][height<=720]',
        'outtmpl': './video/playlist/%(playlist|Single_Videos)s/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'ignoreerrors': True,
        'progress_hooks': [progress_hook]
    }

    def run_download():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(url, download=True)

                # Check if it's a playlist or single video
                if 'entries' in result:
                    playlist_title = result.get('title', 'Playlist')
                    messagebox.showinfo("Success", f"Playlist '{playlist_title}' downloaded successfully!")
                else:
                    video_title = result.get('title', 'Unknown Video')
                    messagebox.showinfo("Success", f"Video '{video_title}' downloaded successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Download failed: {e}")

        root.after(2000, root.quit)  # Auto exit after 2 seconds

    # Run download in a new thread
    threading.Thread(target=run_download, daemon=True).start()

# GUI Setup
root = tk.Tk()
root.title("YouTube Video & Playlist Downloader")
root.geometry("500x250")

# URL Entry
tk.Label(root, text="Enter Video/Playlist URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Progress Bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, length=300, variable=progress_var)
progress_bar.pack(pady=10)

# Download Button
tk.Button(root, text="Download", command=download, bg="green", fg="white").pack(pady=20)

# Run the GUI
root.mainloop()
