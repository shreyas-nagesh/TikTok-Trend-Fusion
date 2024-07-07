import cv2
import pytesseract


def ocr_image(file_path):
    """
    Perform OCR (Optical Character Recognition) on an image file.

    Parameters:
    - file_path (str): Path to the image file.

    Returns:
    - str: Extracted text from the image.
    """
    try:
        # Step 1: Load the image using OpenCV
        img = cv2.imread(file_path)

        # Step 2: Perform OCR using Pytesseract
        text = pytesseract.image_to_string(img)

        # Step 3: Return the extracted text, stripping any leading/trailing whitespace
        return text.strip()

    except Exception as e:
        # Handle any exceptions that occur during image processing
        return f"Error processing image: {str(e)}"


def read_text(img_path: str) -> str:
    """
    Read text from an image file using OCR.

    Parameters:
    - img_path (str): Path to the image file.

    Returns:
    - str: Extracted text from the image.
    """
    # Step 1: Call ocr_image function to perform OCR and get extracted text
    extracted_text = ocr_image(img_path)

    # Step 2: Print the extracted text for demonstration purposes
    print("Extracted Text:")

    # Step 3: Return the extracted text
    return extracted_text


# Example usage:
if __name__ == "__main__":
    image_path = "/path/to/your/image.jpg"  # Replace with your image file path
    extracted_text = read_text(image_path)
    print(extracted_text)
