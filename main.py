import os
import google.generativeai as genai
import moviepy.editor as mp
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# === Step 1: Configure Gemini ===
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# === Step 2: Generate script ===
def generate_script(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini Error:", e)
        return "Keep going. One day, all your hard work will pay off."

# === Step 3: Create video using basic MoviePy (no ImageMagick) ===
def create_video(script_text, output_file="output.mp4"):
    try:
        background = mp.ColorClip(size=(720, 1280), color=(0, 0, 0), duration=10)
        txt_clip = mp.TextClip(txt=script_text, fontsize=40, color='white', size=(680, None)).set_duration(10)
        txt_clip = txt_clip.set_position('center')
        final_video = mp.CompositeVideoClip([background, txt_clip])
        final_video.write_videofile(output_file, fps=24)
    except Exception as e:
        print("❌ Video Creation Error:", e)

# === Step 4: Upload to YouTube using saved credentials.json ===
def upload_to_youtube(file_path, title, description):
    try:
        credentials = Credentials.from_authorized_user_file("token.json", scopes=["https://www.googleapis.com/auth/youtube.upload"])
        youtube = build("youtube", "v3", credentials=credentials)

        request_body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["motivation", "ai shorts", "gemini"],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public"
            }
        }

        media = MediaFileUpload(file_path)

        response = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media
        ).execute()

        print("✅ Uploaded: https://youtube.com/watch?v=" + response["id"])
    except Exception as e:
        print("❌ YouTube Upload Error:", e)

# === Step 5: Run Everything ===
if __name__ == "__main__":
    prompt = "Write a 60-word motivational script for a YouTube short about resilience."
    script = generate_script(prompt)
    print("📜 Generated Script:\n", script)

    create_video(script)
    upload_to_youtube("output.mp4", "Stay Resilient | AI Motivation", "Auto-generated using Gemini AI and Python.")
