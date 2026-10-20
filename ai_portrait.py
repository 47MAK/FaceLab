
import os
from io import BytesIO

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image


load_dotenv()

MODEL_NAME = "gemini-3.1-flash-image"


def transform_portrait(
    image: Image.Image,
    prompt: str,
) -> tuple[Image.Image, str]:
    """
    Transform an uploaded portrait using Gemini image generation.

    Args:
        image: Input portrait as a PIL Image.
        prompt: User's description of the desired transformation.

    Returns:
        Generated PIL image and an optional model text response.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Gemini API key not found. Add GEMINI_API_KEY to your .env file."
        )

    if not prompt or not prompt.strip():
        raise ValueError("Please enter a transformation prompt.")

    # Initialize the Gemini client.
    client = genai.Client(api_key=api_key)

    # Prepare the uploaded image.
    input_image = image.convert("RGB")

    # Ask Gemini to transform the provided portrait.
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            (
                "Edit the provided portrait according to the user's request. "
                "Preserve the person's recognizable identity and natural "
                "facial features where possible. Apply the requested style "
                "to the existing image rather than creating an unrelated person. "
                "Return the transformed image.\n\n"
                f"User request: {prompt.strip()}"
            ),
            input_image,
        ],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
        ),
    )

    generated_image = None
    text_response = ""

    # The response can contain text, an image, or both.
    for part in response.parts:
        if part.text:
            text_response += part.text + "\n"

        if part.inline_data is not None:
            if part.inline_data.mime_type.startswith("image/"):
                generated_image = Image.open(
                    BytesIO(part.inline_data.data)
                ).convert("RGB")
                break

    if generated_image is None:
        raise RuntimeError(
            "Gemini did not return an image. Try a different prompt "
            "or check model availability and API limits."
        )

    return generated_image, text_response.strip()
