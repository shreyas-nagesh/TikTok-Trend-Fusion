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
