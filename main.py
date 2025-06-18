import os
import google.generativeai as genai
import moviepy.editor as mp
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# === Step 1: Configure Gemini ===
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# === Step 2: Generate a short script using Gemini ===
def generate_script(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")  # ✅ Correct model
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini Error:", e)
        return "Keep going. One day, all your hard work will pay off."

# === Step 3: Create a basic vertical video ===
def create_video(script_text, output_file="output.mp4"):
    try:
        background = mp.ColorClip(size=(720, 1280), color=(0, 0, 0), duration=10)
        txt_clip = mp.TextClip(script_text, fontsize=40, color='white', size=(680, None), method='caption', align='center')
        txt_clip = txt_clip.set_position('center').set_duration(10)
        final_video = mp.CompositeVideoClip([background, txt_clip])
        final_video.write_videofile(output_file, fps=24)
    except Exception as e:
        print("❌ Video Creation Error:", e)

# === Step 4: Upload to YouTube ===
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
            'tags': ['motivation', 'ai shorts', 'gemini'],
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    media = MediaFileUpload(file_path)

    try:
        response = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media
        ).execute()
        print("✅ Uploaded: https://youtube.com/watch?v=" + response['id'])
    except Exception as e:
        print("❌ YouTube Upload Error:", e)

# === Step 5: Run everything ===
if __name__ == "__main__":
    prompt = "Write a 60-word motivational script for a YouTube Short about never giving up."
    print("📤 Sending prompt to Gemini...")
    script = generate_script(prompt)
    print("📜 Generated Script:\n", script)

    print("🎥 Creating video...")
    create_video(script)

    print("📤 Uploading video to YouTube...")
    upload_to_youtube("output.mp4", "Never Give Up | AI Motivation", "This short was created automatically using Gemini AI and Python.")
