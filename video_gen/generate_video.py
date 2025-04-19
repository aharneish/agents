from video_gen.model_loader import load_text2video_pipeline
from modelscope.outputs import OutputKeys
import os

def generate_video_from_textfile(text_file_path="split_output.txt", output_path="generated_video.mp4"):
    if not os.path.exists(text_file_path):
        raise FileNotFoundError(f"❌ {text_file_path} not found!")

    print("📖 Reading script from", text_file_path)
    with open(text_file_path, "r", encoding="utf-8") as f:
        text = f.read()

    pipeline = load_text2video_pipeline()

    print("🎬 Generating video from script...")
    result = pipeline({"text": text})

    video = result[OutputKeys.OUTPUT_VIDEO]

    os.rename(video, output_path)
    print(f"✅ Video saved as {output_path}")
