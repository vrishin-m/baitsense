import easyocr
import sys
import nlp
import torch
torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_reader():
    if not hasattr(sys.modules[__name__], 'reader'):
        setattr(sys.modules[__name__], 'reader', easyocr.Reader(['en'], gpu=True))
    return getattr(sys.modules[__name__], 'reader')

def extract_text_from_image(image_path):
    """
    Extract text from an image using EasyOCR.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: The extracted text.
    """
    reader = get_reader()
    results = reader.readtext(image_path)
    extracted_texts = [text for _, text, _ in results]
    return ' '.join(extracted_texts)

def analyze(results):
    score =0
    return nlp.predict_examples(examples=[results])


if __name__ == '__main__':
    # Example usage
    image_path = r"C:\Users\mahad\Downloads\ali_a.png"
    results = extract_text_from_image(image_path)
    print(results)
    print(analyze(results))



