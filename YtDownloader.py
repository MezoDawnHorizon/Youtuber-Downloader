import tkinter
import customtkinter
import yt_dlp
import threading
import os

def StartThreadMP4():
    # Create new thread for downlaod
    thread = threading.Thread(target=startDownloadMP4)
    thread.start() # starts the thread 

def StartThreadMP3():
    print("thread Created")
    # Create new thread for downlaod
    thread = threading.Thread(target=startDownloadMP3)
    thread.start() # starts the thread

def startDownloadMP4():
    try:
        url = link.get()
        selected_resolution = resolution.get()  # Fetch selected resolution (e.g., "1080")
        print(f"Selected resolution: {selected_resolution}")
        title.configure(text="Downloading...", text_color="white")
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads") # Gets the path to the user's Downloads folder
        # yt-dlp options for downloading the lowest resolution MP4 video
        ydl_opts = {
            'format': f'bestvideo[height<={selected_resolution}]+bestaudio[ext=m4a]/mp4',  # Download best video+audio in MP4 format
            'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),  # Save to a "downloads" folder
            'progress_hooks': [progress_hook],  # Add the progress hook here
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        title.configure(text="Download Completed!", text_color="green")    
    except:
        title.configure(text="Download Faild!", text_color="red")

def startDownloadMP3():
    try:
        url = link.get()
        title.configure(text="Downloading...", text_color="white")
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads") # Gets the path to the user's Downloads folder
        # yt-dlp options for downloading the highest resolution MP3 audio
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/mp3',  # Download best audio in MP3 format
            'postprocessors': [
                {  # Ensure it outputs as MP3
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ],
            'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),  # Save to a "downloads" folder
            'progress_hooks': [progress_hook],  # Add the progress hook here
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        title.configure(text="Download Completed!", text_color="green")   
    except:
        title.configure(text="Download Faild!", text_color="red")



# Set up the GUI window
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("400x265")
app.title("Youtube Downloader")
app.resizable(False, False)

# UI Stuff
title = customtkinter.CTkLabel(app, text="Put Youtube Link here")
title.pack(padx=10, pady=10)


# link box
URL_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=URL_var)
link.pack()

# Frame for Buttons
frame = customtkinter.CTkFrame(app)  # Create a frame
frame.pack(pady=10)  # Add the frame to the app

# Button
Download = customtkinter.CTkButton(frame, text="Download-MP4", command=StartThreadMP4)
Downloadmp3 = customtkinter.CTkButton(frame, text="Download-MP3", command=StartThreadMP3)
Download.pack(pady=10, side="left")
Downloadmp3.pack(pady=20, side="right")

# ComboBox
resolution = customtkinter.CTkComboBox(app, text_color="white", values=["1080", "720", "480", "360"], width=200, height=30)
resolution.set("1080")  # Set default resolution to 1080p
resolution.pack()

# progress bar
progress_frame = customtkinter.CTkFrame(app)  # Create a frame
progress_frame.pack(pady=10)  # Add the frame to the app
progress_text = customtkinter.CTkLabel(progress_frame, text="0%")
progress_text.pack()
progress_bar = customtkinter.CTkProgressBar(progress_frame, width=400)
progress_bar.pack()
progress_bar.set(0)  # Initialize to 0%
def progress_hook(d):
    """Update the progress bar and progress label."""
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes', 1)  # Avoid division by zero
        downloaded_bytes = d.get('downloaded_bytes', 0)
        progress = downloaded_bytes / total_bytes
        percentage = int(progress * 100)  # Convert progress to percentage

        # Update the progress bar
        progress_bar.set(progress)  
        
        # Update the progress label
        progress_text.configure(text=f"{percentage}%")
    
    elif d['status'] == 'finished':
        # Set progress to 100% when done
        progress_bar.set(1.0)
        progress_text.configure(text="100%")

# Run App
app.mainloop()