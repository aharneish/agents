import os
from pathlib import Path
from PIL import Image
from moviepy.editor import ImageSequenceClip, AudioFileClip
from mutagen.mp3 import MP3
from tqdm import tqdm

def create_gif():
    """
    This function creates a GIF from a series of images in the './img' folder.
    """
    img_folder = './img'
    gif_path = './In_a_future.gif'

    # Get list of .jpg and .png images in img folder
    images = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if f.endswith(('.jpg', '.png'))]

    # Check if images exist
    if not images:
        print("Error: No images found in img folder")
        return

    # Open images and create GIF
    try:
        with Image.open(images[0]) as img:
            # Use tqdm for loading images
            append_images = [Image.open(img).convert("RGBA") for img in tqdm(images[1:], desc="Loading images for GIF")]
            img.save(gif_path, save_all=True, append_images=append_images, duration=100, loop=0)
        print("GIF created successfully!")
    except Exception as e:
        print(f"Error creating GIF: {e}")

def create_video():
    """
    Create a video from images and an audio file.
    """
    folder_path = './'
    img_folder = './img'
    audio_path = os.path.join(folder_path, "Movie_audio.mp3")
    video_path = os.path.join(folder_path, "In_a_future.mp4")

    # Check if audio file exists
    if not os.path.exists(audio_path):
        print(f"Error: {audio_path} does not exist")
        return

    # Read audio file length
    try:
        song = MP3(audio_path)
        audio_length = round(song.info.length)
    except Exception as e:
        print(f"Error reading audio file: {e}")
        return

    # Get list of .jpg and .png images in img folder
    path_images = Path(img_folder)
    images = list(path_images.glob('*.jpg')) + list(path_images.glob('*.png'))

    # Check if images exist
    if not images:
        print("Error: No images found")
        return

    # Resize images and store resized paths
    resized_image_paths = []
    for image_name in tqdm(images, desc="Resizing images for video"):
        try:
            image = Image.open(image_name).resize((800, 800), Image.LANCZOS)
            resized_image_path = os.path.join(img_folder, f"resized_{image_name.stem}.png")
            image.save(resized_image_path)
            resized_image_paths.append(resized_image_path)
        except Exception as e:
            print(f"Error resizing image: {e}")
            return

    # Calculate duration per image for video
    duration_per_image = audio_length / len(resized_image_paths)

    # Create video from images and add audio
    try:
        # Create a video clip from the image sequence
        clip = ImageSequenceClip(resized_image_paths, fps=1/duration_per_image)
        
        # Attach audio to the video
        audio = AudioFileClip(audio_path)
        clip = clip.set_audio(audio)
        
        # Save the final video
        clip.write_videofile(video_path, codec='libx264')
        print("Video created successfully!")
    except Exception as e:
        print(f"Error creating video: {e}")

create_gif()
create_video()