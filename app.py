import streamlit as st
import pyheif
from PIL import Image
import io
import zipfile

# Page config with title
st.set_page_config(
    page_title="HEIC to JPG Online Converter | Free HEIC to JPEG",
    page_icon="📸",
    layout="centered"
)

# Custom CSS Styling
st.markdown(
    """
    <style>
    body {
        background-color: #0c111b;
        color: #f5f5f5;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        margin-top: 10px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main Title with Keywords
st.title("📸 Free Online HEIC to JPG Converter")
st.markdown(
    """
    Welcome to the best free **HEIC to JPG Converter** online!  
    Instantly **convert HEIC files to high-quality JPG** images without installing any software.  
    Upload your HEIC files, convert them to JPEG format easily, and download them as a ZIP archive.  
    Perfect for iPhone and iPad users who need to quickly **convert HEIC to JPG online**!
    """,
    unsafe_allow_html=True
)

# Subheader for clarity
st.header("🔄 Convert your HEIC images to JPG in seconds")

# File uploader
uploaded_files = st.file_uploader(
    "**Select your HEIC files to upload**",
    type=["heic"],
    accept_multiple_files=True
)

# File processing
if uploaded_files:
    output_images = []

    with st.spinner('🔄 Converting HEIC files to JPG, please wait...'):
        for uploaded_file in uploaded_files:
            try:
                heif_file = pyheif.read(uploaded_file.read())
                image = Image.frombytes(
                    heif_file.mode,
                    heif_file.size,
                    heif_file.data,
                    "raw",
                    heif_file.mode,
                    heif_file.stride,
                )
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG', quality=95)
                img_byte_arr.seek(0)
                output_images.append((uploaded_file.name.replace('.heic', '.jpg'), img_byte_arr))
            except Exception as e:
                st.error(f"Error converting {uploaded_file.name}: {e}")

    if output_images:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for filename, img_data in output_images:
                zip_file.writestr(filename, img_data.read())

        zip_buffer.seek(0)

        st.success("✅ Your HEIC images have been converted to JPG successfully!")

        st.download_button(
            label="📥 Download All JPGs as ZIP",
            data=zip_buffer,
            file_name="converted_jpgs.zip",
            mime="application/zip"
        )
else:
    st.info("Drag & drop your HEIC files or click to select them.")

# Divider
st.markdown("---")

# Donation Button
st.markdown(
    """
    <div style="text-align: center; margin-top: 20px;">
        <a href="https://paypal.me/uomoathens?country.x=GR&locale.x=en_US" target="_blank">
            <button style="background-color:#007BFF; color:white; border:none; border-radius:10px; font-size:18px; padding:12px 30px; cursor:pointer;">
                Support this Free HEIC to JPG Tool ❤️
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Footer
st.markdown("---")
st.caption("Made with ❤️ by DS | Convert HEIC to JPG | Free Online HEIC Converter")


# Divider
st.markdown("---")

# 📋 Quick SEO Links Section
st.markdown(
    """
    ### 📋 Quick Links - Free HEIC to JPG Conversion

    Looking for the best way to **convert HEIC to JPG**? Explore these resources:

    - [Convert HEIC to JPG Online](https://heic-to-jpg-converter-ll9daajzws8bphhqssvwf6.streamlit.app/)
    - [Free HEIC Converter Tool](https://heic-to-jpg-converter-ll9daajzws8bphhqssvwf6.streamlit.app/)
    - [High-Quality HEIC to JPEG Conversion](https://heic-to-jpg-converter-ll9daajzws8bphhqssvwf6.streamlit.app/)
    - [Drag and Drop HEIC to JPG](https://heic-to-jpg-converter-ll9daajzws8bphhqssvwf6.streamlit.app/)
    - [Online HEIC to JPG Free Tool](https://heic-to-jpg-converter-ll9daajzws8bphhqssvwf6.streamlit.app/)

    Fast, free, and secure HEIC to JPG conversion in seconds — no sign-up required!
    """,
    unsafe_allow_html=True
)

# Footer
st.markdown("---")
st.caption("Made with ❤️ by DS | Free Online HEIC to JPG Converter | Best Free HEIC to JPEG Tool")

