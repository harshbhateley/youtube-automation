import os
import google.generativeai as genai
import moviepy.editor as mp

# === Step 1: Configure Gemini ===
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# === Step 2: Generate a short motivational script ===
def generate_script(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini Error:", e)
        return "Keep going. One day, all your hard work will pay off."

# === Step 3: Create a video with solid background (no ImageMagick needed) ===
def create_video(script_text, output_file="output.mp4"):
    try:
        background = mp.ColorClip(size=(720, 1280), color=(0, 0, 0), duration=10)
        txt_clip = mp.TextClip(txt=script_text, fontsize=40, color='white', size=(680, None)).set_duration(10)
        txt_clip = txt_clip.set_position('center')
        final_video = mp.CompositeVideoClip([background, txt_clip])
        final_video.write_videofile(output_file, fps=24)
        print(f"✅ Video saved as {output_file}")
    except Exception as e:
        print("❌ Video Creation Error:", e)

# === Step 4: Run everything ===
if __name__ == "__main__":
    prompt = "Write a 60-word motivational script for a YouTube short about discipline and focus."
    print("📤 Sending prompt to Gemini...")
    script = generate_script(prompt)
    print("📜 Generated Script:\n", script)

    print("🎥 Creating video...")
    create_video(script)
