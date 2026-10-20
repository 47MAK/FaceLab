# FaceLab — AI Face Filter Studio

## 1. Project Overview

FaceLab is a Python-based face-filter prototype built with Streamlit and OpenCV. It detects faces in uploaded images and applies filters such as sunglasses, crowns, and moustaches.

The project also explores a Generative AI extension for prompt-based portrait editing using the Gemini API. The image-generation integration was attempted, but could not be verified end-to-end because the selected model returned a `429 RESOURCE_EXHAUSTED` error due to unavailable free-tier quota.

**Project status:** Computer-vision prototype working; generative image editing is a proposed extension with an attempted API integration.

## 2. Features

- Upload a portrait through a web interface.
- Detect faces using OpenCV Haar Cascade.
- Apply transparent PNG filters relative to detected face positions.
- Preview original and processed images.
- Download processed images.
- Explore a prompt-based AI portrait-editing workflow.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| OpenCV | Face detection and image processing |
| Pillow (PIL) | Creating and manipulating PNG filter assets |
| NumPy | Image-array operations and alpha blending |
| Google GenAI SDK | Attempted Gemini API integration |
| python-dotenv | Loading API credentials from `.env` |

## 4. Project File Explanation

### `app.py`
The main Streamlit application. It creates the interface, allows users to upload images, select application modes, view processed results, and download outputs. It connects the Instant Filters functionality to the optional AI Portrait Studio workflow.

### `face_filter.py`
Contains the face-filtering logic. It uses OpenCV's Haar Cascade classifier to detect faces and positions transparent PNG overlays according to each detected face's bounding box. Alpha blending combines the filter with the original image.

### `generate_assets.py`
Generates the transparent PNG assets used by the application, including sunglasses, crowns, and moustaches. These are programmatically created graphics rather than outputs from a generative image model.

### `ai_portrait.py`
Contains the attempted Gemini API integration for prompt-based image editing. It prepares the image and text prompt, sends a request to the configured model, and processes generated image output when available. Successful generation has not been verified because the model's free-tier quota was unavailable.

### `filters/`
Stores the transparent PNG overlays applied to detected faces.

### `requirements.txt`
Lists the Python packages required to install and run the project.

### `.env`
Stores the Gemini API key locally. This file must not be committed to GitHub.

### `.gitignore`
Excludes virtual environments, secrets, Python cache files, and other files that should not be tracked by Git.

### `screenshots/`

## 5. Implementation Approach

1. **Image input:** The user uploads a portrait through Streamlit.
2. **Face detection:** OpenCV Haar Cascade identifies faces and returns their bounding boxes.
3. **Filter selection:** The user selects a filter such as sunglasses, crown, or moustache.
4. **Overlay positioning:** The application calculates the overlay's size and position relative to the detected face.
5. **Alpha blending:** The transparent PNG is blended with the original image.
6. **Output:** The application displays the processed image and provides a download option.

## 6. Proposed Generative AI Architecture

A future version can use a pretrained image-editing model to support natural-language instructions such as "add sunglasses" or "give the portrait a fantasy crown."

**Proposed pipeline:**

User Image + Text Prompt → Input Validation → Face Detection and Region Identification → Pretrained Image-Editing Model → Output Validation → Streamlit Preview → Download

The model would use the uploaded image and prompt to generate an edited portrait. Face detection can help identify the target region, while output validation can check that an image was returned successfully.

The Gemini integration was explored as an implementation of this concept, but the end-to-end generative workflow remains unverified. A compatible model with accessible inference capacity is required to complete it.

## 7. Setup Instructions

### Prerequisites
- Python 3.10 or later
- pip
- VS Code or another Python editor

### Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd "FaceLab"
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate the filter assets if they are not already present:

```bash
python generate_assets.py
```

Run the application:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

### Optional Gemini Configuration

Create a local `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Do not upload this file or expose your API key. The Instant Filters feature should be tested independently of Gemini availability.

## 8. Open-Source Models, Repositories and Libraries

- **OpenCV:** https://github.com/opencv/opencv
- **Streamlit:** https://github.com/streamlit/streamlit
- **Pillow:** https://github.com/python-pillow/Pillow
- **NumPy:** https://github.com/numpy/numpy
- **Google GenAI Python SDK:** https://github.com/googleapis/python-genai
- **OpenCV Haar Cascade:** `haarcascade_frontalface_default.xml`, distributed with OpenCV's Haar Cascade resources.

The prototype uses an existing pretrained Haar Cascade detector. No custom model was trained. The generative image-editing model remains an intended extension rather than a verified working feature.

## 9. Limitations and Future Improvements

- Haar Cascade detection may fail under poor lighting, unusual angles, or partial occlusion.
- Sticker positioning may need adjustment for different face orientations.
- Generative image editing depends on an accessible compatible model and its resource limits.
- Future work includes better face landmarks, more filters, improved image handling, and integration with a verified pretrained image-editing model.

## 10. Conclusion

FaceLab demonstrates a working computer-vision face-filtering prototype and documents a proposed extension using Generative AI. It explores how existing libraries and pretrained models can be combined to build an interactive image-editing application without training a model from scratch.

## 11. Application Screenshots

### 1. FaceLab Interface
Shows the Streamlit application interface, image upload option, and available face-filter modes.

