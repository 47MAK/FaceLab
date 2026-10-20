
import streamlit as st
import numpy as np
from PIL import Image
from io import BytesIO

from face_filter import apply_face_filter
from ai_portrait import transform_portrait


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="FaceLab | AI Face Filters",
    page_icon="😎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 750;
        letter-spacing: -1px;
        margin-bottom: 0;
    }

    .subtitle {
        color: #9CA3AF;
        font-size: 1rem;
        margin-top: 0.35rem;
        margin-bottom: 1.8rem;
    }

    div[data-testid="stImage"] img {
        border-radius: 12px;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        border-radius: 10px;
        min-height: 42px;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">😎 FaceLab</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Your selfie. Your style. Your filters.'
    '</div>',
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("✨ Studio")

    mode = st.radio(
        "Choose a mode",
        ["Instant Filters", "AI Portrait Studio"],
    )

    uploaded_file = st.file_uploader(
        "Upload your selfie",
        type=["jpg", "jpeg", "png"],
    )

    if mode == "Instant Filters":
        filter_type = st.selectbox(
            "Choose your filter",
            ["Sunglasses", "Crown", "Moustache"],
        )

    st.divider()


# --------------------------------------------------
# IMAGE UPLOAD
# --------------------------------------------------

if uploaded_file is None:
    st.markdown("### Start creating")
    st.write("Upload a photo from the sidebar to get started.")
    st.stop()

try:
    original_image = Image.open(uploaded_file).convert("RGB")
    original_array = np.array(original_image)

except Exception:
    st.error("Could not open this image. Please upload a valid image.")
    st.stop()


# --------------------------------------------------
# MODE 1: INSTANT FILTERS
# --------------------------------------------------

if mode == "Instant Filters":

    try:
        processed_array, message = apply_face_filter(
            original_array.copy(),
            filter_type,
        )

        st.markdown(f"### Your look: {filter_type}")

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown("**Original**")
            st.image(
                original_image,
                use_container_width=True,
            )

        with col2:
            st.markdown("**Your result**")
            st.image(
                processed_array,
                use_container_width=True,
            )

        if message.startswith("No face detected"):
            st.warning(message)

        else:
            output_buffer = BytesIO()

            Image.fromarray(processed_array).save(
                output_buffer,
                format="PNG",
            )

            st.download_button(
                "⬇ Download your creation",
                data=output_buffer.getvalue(),
                file_name="facelab_result.png",
                mime="image/png",
                use_container_width=True,
            )

    except Exception as error:
        st.error(f"Could not apply the filter: {error}")


# --------------------------------------------------
# MODE 2: AI PORTRAIT STUDIO
# --------------------------------------------------

else:
    st.markdown("### ✨ AI Portrait Studio")

    prompt = st.text_area(
        "Describe your transformation",
        placeholder=(
            "Example: Transform this portrait into a cinematic "
            "cyberpunk scene with neon blue and purple lighting. "
            "Keep the person recognizable."
        ),
        max_chars=500,
        height=110,
    )

    generate_clicked = st.button(
        "✨ Generate AI Portrait",
        type="primary",
        use_container_width=True,
    )

    # Identify the current upload so results aren't shown for
    # a different image.
    image_id = (
        uploaded_file.name,
        uploaded_file.getvalue(),
    )

    if generate_clicked:

        if not prompt.strip():
            st.warning("Please enter a transformation prompt.")

        else:
            try:
                with st.spinner(
                    "Creating your AI portrait. Please wait..."
                ):
                    generated_image, _ = transform_portrait(
                        original_image,
                        prompt.strip(),
                    )

                st.session_state["ai_result"] = generated_image
                st.session_state["ai_image_id"] = image_id
                st.session_state["ai_prompt"] = prompt.strip()

            except Exception as error:
                st.error(
                    "Could not generate the portrait. "
                    "Check your API key, model availability, "
                    "internet connection, and usage limits."
                )
                st.caption(str(error))

    # Display the generated image only for the matching upload.
    if (
        "ai_result" in st.session_state
        and st.session_state.get("ai_image_id") == image_id
    ):
        generated_image = st.session_state["ai_result"]

        st.markdown("#### Your generated portrait")

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown("**Original**")
            st.image(
                original_image,
                use_container_width=True,
            )

        with col2:
            st.markdown("**AI-generated result**")
            st.image(
                generated_image,
                use_container_width=True,
            )

        output_buffer = BytesIO()

        generated_image.save(
            output_buffer,
            format="PNG",
        )

        st.download_button(
            "⬇ Download AI Portrait",
            data=output_buffer.getvalue(),
            file_name="facelab_ai_portrait.png",
            mime="image/png",
            use_container_width=True,
        )
