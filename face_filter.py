
import cv2
import numpy as np
from pathlib import Path


# Directory containing the transparent PNG overlays.
FILTER_DIR = Path(__file__).parent / "filters"

# OpenCV's pretrained Haar Cascade face detector.
CASCADE_PATH = (
    cv2.data.haarcascades
    + "haarcascade_frontalface_default.xml"
)


def overlay_png(
    image: np.ndarray,
    overlay: np.ndarray,
    x: int,
    y: int,
    width: int,
    height: int,
) -> np.ndarray:
    """Resize a transparent PNG and blend it onto an RGB image."""

    if width <= 0 or height <= 0:
        return image

    overlay = cv2.resize(
        overlay,
        (width, height),
        interpolation=cv2.INTER_AREA,
    )

    # Clip the overlay to the image boundaries.
    image_h, image_w = image.shape[:2]

    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(image_w, x + width)
    y2 = min(image_h, y + height)

    if x1 >= x2 or y1 >= y2:
        return image

    # Corresponding region of the resized overlay.
    overlay_x1 = x1 - x
    overlay_y1 = y1 - y
    overlay_x2 = overlay_x1 + (x2 - x1)
    overlay_y2 = overlay_y1 + (y2 - y1)

    sticker = overlay[
        overlay_y1:overlay_y2,
        overlay_x1:overlay_x2,
    ]

    # Separate colour and transparency channels.
    sticker_rgb = sticker[:, :, :3].astype(np.float32)
    alpha = sticker[:, :, 3:4].astype(np.float32) / 255.0

    region = image[y1:y2, x1:x2].astype(np.float32)

    # Alpha blending preserves the background through transparent pixels.
    blended = (
        alpha * sticker_rgb
        + (1.0 - alpha) * region
    )

    image[y1:y2, x1:x2] = np.clip(
        blended, 0, 255
    ).astype(np.uint8)

    return image


def apply_face_filter(
    image: np.ndarray,
    filter_type: str = "Sunglasses",
):
    """
    Detect faces with Haar Cascade and apply a transparent PNG filter.

    Args:
        image: Input image as a NumPy array in RGB format.
        filter_type: Sunglasses, Crown, or Moustache.

    Returns:
        Processed RGB image and a status message.
    """

    if image is None or image.size == 0:
        raise ValueError("The input image is empty.")

    # Map the UI selection to its PNG asset.
    asset_names = {
        "Sunglasses": "sunglasses.png",
        "Crown": "crown.png",
        "Moustache": "moustache.png",
    }

    if filter_type not in asset_names:
        raise ValueError(f"Unsupported filter: {filter_type}")

    asset_path = FILTER_DIR / asset_names[filter_type]

    # IMREAD_UNCHANGED preserves the PNG transparency channel.
    overlay = cv2.imread(
        str(asset_path),
        cv2.IMREAD_UNCHANGED,
    )

    if overlay is None:
        raise FileNotFoundError(
            f"Filter asset not found: {asset_path}. "
            "Run generate_assets.py to create the PNG files."
        )

    if overlay.ndim != 3 or overlay.shape[2] != 4:
        raise ValueError(
            f"{asset_path.name} must be an RGBA PNG "
            "with a transparency channel."
        )

    # OpenCV loads PNG colour channels as BGRA; convert to RGBA.
    overlay = cv2.cvtColor(
        overlay, cv2.COLOR_BGRA2RGBA
    )

    # Convert the source image to grayscale for face detection.
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

    if face_cascade.empty():
        raise RuntimeError(
            "Could not load the Haar Cascade face detector."
        )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60),
    )

    if len(faces) == 0:
        return image, "No face detected. Try a clear, front-facing photo."

    result = image.copy()

    for (x, y, w, h) in faces:
        if filter_type == "Sunglasses":
            # Fit the glasses across the approximate eye region.
            sticker_w = int(w * 1.12)
            sticker_h = int(sticker_w * overlay.shape[0] / overlay.shape[1])

            sticker_x = x - int(w * 0.06)
            sticker_y = y + int(h * 0.28)

        elif filter_type == "Crown":
            # Place the crown above the forehead.
            sticker_w = int(w * 1.05)
            sticker_h = int(sticker_w * overlay.shape[0] / overlay.shape[1])

            sticker_x = x - int(w * 0.025)
            sticker_y = y - int(sticker_h * 0.78)

        else:  # Moustache
            # Place the moustache around the approximate mouth region.
            sticker_w = int(w * 0.82)
            sticker_h = int(sticker_w * overlay.shape[0] / overlay.shape[1])

            sticker_x = x + int(w * 0.09)
            sticker_y = y + int(h * 0.59)

        result = overlay_png(
            result,
            overlay,
            sticker_x,
            sticker_y,
            sticker_w,
            sticker_h,
        )

    return result, f"Applied {filter_type} to {len(faces)} face(s)."
