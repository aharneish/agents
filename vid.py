import os
from pathlib import Path
from PIL import Image
from moviepy.editor import ImageSequenceClip, AudioFileClip
from tqdm import tqdm  # Import tqdm

def create_gif():
    """
    This function creates a GIF from a series of images in the './img' folder.
    """
    img_folder = './img'
    gif_path = './In_a_future.gif'

    # Get list of images in img folder
    images = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if f.endswith('.jpg') or f.endswith('.png')]

    # Check if images exist
    if not images:
        print("Error: No images found in img folder")
        return

    # Open images and create GIF
    try:
        with Image.open(images[0]) as img:
            # Use tqdm for progress tracking while loading images
            append_images = [Image.open(img).convert("RGBA") for img in tqdm(images[1:], desc="Loading images for GIF")]
            img.save(gif_path, save_all=True, append_images=append_images, duration=100, loop=0)
    except Exception as e:
        print(f"Error creating GIF: {e}")

def create_video():
    """
    Create a video from images and an audio file.
    """
    folder_path = './img'
    audio_path = os.path.join(folder_path, "Movie_audio.mp3")
    video_path = os.path.join(folder_path, "In_a_future.mp4")

    # Glob images
    path_images = Path(folder_path)
    images = list(path_images.glob('*.png'))

    # Check if images exist
    if not images:
        print("Error: No images found")
        return

    # Resize images and save resized paths
    resized_image_paths = []
    for image_name in tqdm(images, desc="Resizing images for video"):
        try:
            image = Image.open(image_name).resize((800, 800), Image.LANCZOS)
            resized_image_path = os.path.join(folder_path, f"resized_{os.path.basename(image_name)}")
            image.save(resized_image_path)
            resized_image_paths.append(resized_image_path)
        except Exception as e:
            print(f"Error resizing image: {e}")
            return

    # Save images as a video
    try:
        # Use tqdm for progress tracking during video creation
        clip = ImageSequenceClip(resized_image_paths, fps=1)  # Adjust fps as needed
        if os.path.exists(audio_path):
            audio = AudioFileClip(audio_path)
            clip = clip.set_audio(audio)
        clip.write_videofile(video_path)
    except Exception as e:
        print(f"Error creating video: {e}")

create_gif()
create_video()