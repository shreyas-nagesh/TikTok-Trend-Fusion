from transformers import AutoProcessor, MusicgenForConditionalGeneration
from diffusers import DiffusionPipeline

# Define a function to load and cache models
def load_models():
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small", attn_implementation="eager")
    pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    return processor, model, pipeline

# Script to load and cache the models
if __name__ == "__main__":
    # Load models when the package is imported
    processor, model, pipeline = load_models()