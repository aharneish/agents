from huggingface_hub import snapshot_download
from modelscope.pipelines import pipeline
import pathlib


def load_text2video_pipeline():
    """
    Downloads and loads the DAMO Text-to-Video Synthesis model from HuggingFace using ModelScope.
    Returns a ready-to-use text-to-video pipeline.
    """
    model_dir = pathlib.Path("weights")

    if not model_dir.exists():
        print("⬇️ Downloading DAMO Text-to-Video Synthesis model from HuggingFace...")
        snapshot_download(
            repo_id="damo-vilab/modelscope-damo-text-to-video-synthesis",
            repo_type="model",
            local_dir=model_dir,
            local_dir_use_symlinks=False
        )
    else:
        print("✅ Model already downloaded at:", model_dir)

    # Load the pipeline from the local model weights
    print("⚙️ Loading model pipeline from local weights...")
    text2video_pipe = pipeline(
        task="text-to-video-synthesis",
        model=str(model_dir)
    )

    return text2video_pipe