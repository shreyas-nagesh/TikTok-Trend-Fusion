import scipy
from transformers import AutoProcessor, MusicgenForConditionalGeneration


def gen_api(desc: str, output_file_name: str) -> None:
    """
    Generate audio from a textual description and save it as a .wav file.

    This function uses a pre-trained model from the 'facebook/musicgen-small' to generate
    audio data based on the provided textual description. The generated audio is then
    saved to a specified output file in .wav format.

    Parameters:
    desc (str): A string containing the description based on which the audio will be generated.
    output_file_name (str): The name of the output file (without extension) where the generated audio will be saved.

    Returns:
    None: This function does not return any value. It writes the generated audio to a file.

    Example:
    >>> gen_api("A calm and soothing piano melody.", "output_audio")
    This will create a file named 'output_audio.wav' containing the generated audio.
    """

    # Load the pre-trained processor and model from the 'facebook/musicgen-small' model
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

    # Process the input description text to get the input tensors for the model
    inputs = processor(
        text=[desc],  # Input text description
        padding=True,  # Apply padding to the input text
        return_tensors="pt",  # Return the input as PyTorch tensors
    )

    # Generate audio values using the model with the processed inputs
    audio_values = model.generate(**inputs, max_new_tokens=256)

    # Get the sampling rate from the model's configuration
    sampling_rate = model.config.audio_encoder.sampling_rate

    # Write the generated audio values to a .wav file
    scipy.io.wavfile.write(
        output_file_name + ".wav", rate=sampling_rate, data=audio_values[0, 0].numpy()
    )
