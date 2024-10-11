import requests

def ocr_space_file(filename, api_key='K82784981688957', language='eng'):
    """
    Function to call the OCR.space API and get text from an image.
    
    :param filename: Path to the image file.
    :param api_key: Your API key for OCR.space.
    :param language: Language for OCR processing.
    :return: The text extracted from the image or None if an error occurred.
    """
    url = 'https://api.ocr.space/parse/image'

    # Prepare the request payload
    payload = {
        'apikey': "K82784981688957",
        'language': language,
        'isOverlayRequired': False
    }

    # Read the image file and send the request
    try:
        with open(filename, 'rb') as f:
            response = requests.post(url, files={'file': f}, data=payload)
        
        # Print the raw response for debugging
        print("Raw response:", response.text)

        # Parse the response
        result = response.json()

        # Check if OCR was successful
        if result.get('IsErroredOnProcessing'):
            print(f"Error: {result['ErrorMessage']}")
            return None

        # Extract the text
        return result.get('ParsedResults')[0].get('ParsedText')

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    image_path = 'images/WhatsApp Image 2024-10-12 at 3.46.44 AM.jpeg'  # Replace with your image path
    api_key = 'YOUR_API_KEY'  # Replace with your OCR.space API key
    extracted_text = ocr_space_file(image_path, api_key)
    
    if extracted_text:
        print("Extracted Text:")
        print(extracted_text)
