# agents_to_video_local.py

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import os
import shutil
import time
import subprocess
import json
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

# Step 0: Use Ollama model to extract scenes locally
def extract_scenes_from_script(script_text, model="hf.co/unsloth/Llama-3.2-3B-Instruct-GGUF:Q4_K_M"):
    print("Extracting scene descriptions using Ollama model locally...")
    prompt = f"""
You are a creative assistant. Break the following movie script into structured scenes.
For each scene, include:
- Scene number
- Visual setting (background/environment)
- Characters involved
- Mood/style
- One key dialogue line (optional)
- A single-line cinematic text-to-video prompt

Script:
{script_text}
"""

    try:
        result = subprocess.run([
            "ollama", "run", model
        ], input=prompt.encode(), capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error running Ollama:", e.stderr.decode())
        return []

    output = result.stdout.decode("utf-8")
    print("Raw scene output:\n", output)

    try:
        scenes = json.loads(output)
    except:
        scenes = []
        scene_lines = output.strip().split("\n")
        for idx, line in enumerate(scene_lines):
            scenes.append({"scene": idx + 1, "prompt": line})
    return scenes

# Initialize ModelScope video generation pipeline
print("Loading ModelScope Text2Video Pipeline...")
text2video = pipeline(Tasks.text_to_video_synthesis, model='damo/text-to-video-synthesis')

# Directory to store all generated video clips
output_dir = "generated_video_scenes"
os.makedirs(output_dir, exist_ok=True)

# Step 1: Read script from file instead of predefined string
script_file = "split_output.txt"
if os.path.exists(script_file):
    with open(script_file, "r", encoding="utf-8") as f:
        script = f.read()
    print(f"Loaded script from {script_file}")
else:
    print(f"Script file '{script_file}' not found. Exiting.")
    exit(1)

# Step 2: Extract scenes using Ollama local model
scenes = extract_scenes_from_script(script)

# Step 3: Generate video clips for each scene
scene_paths = []

for idx, scene in enumerate(scenes):
    prompt = scene.get("prompt")
    print(f"[Scene {idx+1}] Generating video for prompt: {prompt}")
    try:
        result = text2video({"text": prompt})
        src_path = result['output_path']
        dest_path = os.path.join(output_dir, f"scene_{idx+1}.mp4")
        shutil.move(src_path, dest_path)

        # Optional: Add subtitle overlay with scene prompt
        video = VideoFileClip(dest_path)
        subtitle = TextClip(prompt, fontsize=24, color='white', bg_color='black', size=video.size)
        subtitle = subtitle.set_duration(video.duration).set_position(('center', 'bottom'))
        final_clip = CompositeVideoClip([video, subtitle])
        final_path = os.path.join(output_dir, f"scene_{idx+1}_with_subs.mp4")
        final_clip.write_videofile(final_path, codec='libx264', fps=24)
        scene_paths.append(final_path)

    except Exception as e:
        print(f"Failed to generate scene {idx+1}: {e}")
    time.sleep(2)

# Step 4: Combine all scenes into a single movie
print("Combining all video scenes into a single movie...")
clips = [VideoFileClip(path) for path in scene_paths if os.path.exists(path)]
if clips:
    final_video = concatenate_videoclips(clips)
    final_output_path = os.path.join(output_dir, "final_movie.mp4")
    final_video.write_videofile(final_output_path, codec='libx264', fps=24)
    print(f"Movie generation complete. Saved at: {final_output_path}")
else:
    print("No clips available to merge. Check previous errors.")