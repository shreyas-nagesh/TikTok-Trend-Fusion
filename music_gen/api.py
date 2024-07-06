import os
import scipy
import numpy as np
from transformers import AutoProcessor, MusicgenForConditionalGeneration


def gen_api(desc: str, output_file_name: str, audio_length: int) -> None:
    """
    Generate audio from a textual description and save it as a .wav file.

    This function uses a pre-trained model to generate audio data based on the provided
    textual description and saves it to a specified .wav file.

    Parameters:
    desc (str): Description based on which the audio will be generated.
    output_file_name (str): Name of the output file (without extension) where the generated audio will be saved.
    audio_length (int): Length of the audio in multiples of 5 seconds.

    Returns:
    None

    Example:
    >>> gen_api("A Russian ballet with synths.", "music", 2)
    This will create a file named 'music.wav' containing the generated audio of length 10 seconds.
    """

    # Load the pre-trained processor and model
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained(
        "facebook/musicgen-small", attn_implementation="eager"
    )

    # Process the input description text
    inputs = processor(
        text=[desc],  # Input text description
        padding=True,  # Apply padding
        return_tensors="pt",  # Return as PyTorch tensors
    )

    # Generate audio values using the model
    audio_values = model.generate(**inputs, max_new_tokens=256)

    # Get the sampling rate from the model's configuration
    sampling_rate = model.config.audio_encoder.sampling_rate

    # Extend the generated audio to match the specified length
    audio = audio_values[0, 0].numpy()
    audio = np.tile(audio, audio_length)

    # Write the generated audio to a .wav file
    scipy.io.wavfile.write(output_file_name + ".wav", rate=sampling_rate, data=audio)
