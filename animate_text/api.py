from diffusers import DiffusionPipeline
import torch


# Define a function to get the acceleration device to be used by the pipeline
def get_accel_device() -> str:
    """
    Returns the acceleration device to be used by the pipeline.

    Args:
        None

    Returns:
        str: Acceleration device to be used by the pipeline

    Examples:
        >>> get_accel_device() -> "cuda"
    """
    if torch.cuda.is_available():
        return "cuda"  # Use CUDA if available
    elif torch.backends.mps.is_available():
        return "mps"  # Use MPS if available
    else:
        return "cpu"  # Fall back to CPU if no other options are available


# Define a function to generate an image from a given description
def generate_image(desc: str) -> None:
    """
    Generates an image from a given description.

    Args:
        desc (str): Description of the image to be generated

    Returns:
        None

    Examples:
        >>> generate_image("a photo of spiderman eating broccoli")
    """
    # Load the Stable Diffusion v1.5 model
    pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")

    # Get the acceleration device to use for the pipeline
    device = get_accel_device()
    pipe = pipe.to(device)

    # Recommended if your computer has less than 64 GB of RAM
    pipe.enable_attention_slicing()

    # Set the prompt and generate the image
    prompt = desc
    image = pipe(prompt).images[0]
    image.save("gen_img.png")  # Save the generated image to a file
