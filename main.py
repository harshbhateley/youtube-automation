import os
import google.generativeai as genai
import moviepy.editor as mp
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# === Load Gemini API key from Railway environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# === Step 1: Generate script using Gemini
def generate_script(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()

# === Step 2: Create a video using MoviePy
def create_video(script_text, output_file="output.mp4"):
    background = mp.ColorClip(size=(720, 1280), color=(0, 0, 0), duration=10)
    txt_clip = mp.TextClip(script_text, fontsize=40, color='white', size=(680, None), method='caption', align='center')
    txt_clip = txt_clip.set_position('center').set_duration(10)
    final_video = mp.CompositeVideoClip([background, txt_clip])
    final_video.write_videofile(output_file, fps=24)

# === Step 3: Upload video to YouTube
def upload_to_youtube(file_path, title, description):
    creds = {
        "installed": {
            "client_id": os.getenv("YOUTUBE_CLIENT_ID"),
            "client_secret": os.getenv("YOUTUBE_CLIENT_SECRET"),
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }

    flow = InstalledAppFlow.from_client_config(creds, scopes=["https://www.googleapis.com/auth/youtube.upload"])
    credentials = flow.run_console()

    youtube = build('youtube', 'v3', credentials=credentials)

    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['motivation', 'shorts'],
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    media = MediaFileUpload(file_path)

    response = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    ).execute()

    print("✅ Video uploaded: https://youtube.com/watch?v=" + response['id'])

# === Run the full automation ===
if __name__ == "__main__":
    prompt = "Write a short 60-word motivational script for a YouTube short about never giving up."
    script = generate_script(prompt)
    print("📜 Generated Script:\n", script)

    create_video(script)
    upload_to_youtube("output.mp4", "Never Give Up | Shorts Motivation", "This video was created using Gemini AI.")
