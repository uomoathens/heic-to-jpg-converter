import streamlit as st
import pyheif
from PIL import Image
import io
import zipfile

# Στήσιμο σελίδας
st.set_page_config(page_title="HEIC to JPG Cloud Converter", page_icon="📸", layout="centered")

# Custom CSS Styling για ΤΕΤΡΑΓΩΝΟ και Highlight Drag Box
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
    .drag-container {
        border: 2px dashed #cccccc;
        border-radius: 12px;
        padding: 5vw;
        text-align: center;
        background-color: #1c2230;
        color: #cccccc;
        margin-bottom: 20px;
        max-width: 90%;
        margin-left: auto;
        margin-right: auto;
        transition: background-color 0.3s, border-color 0.3s;
    }
    .drag-container:hover {
        background-color: #26324b;
        border-color: #66afe9;
    }
    .drag-container:active {
        background-color: #2b3b57;
        border-color: #66afe9;
    }
    .drag-container * {
        cursor: default !important;
    }
    @media (max-width: 768px) {
        .drag-container {
            padding: 8vw;
            font-size: 4vw;
        }
    }
    @media (max-width: 480px) {
        .drag-container {
            padding: 10vw;
            font-size: 5vw;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Τίτλος και περιγραφή
st.title("📸 HEIC to JPG Cloud Converter")
st.write("Upload your HEIC images and get perfect JPGs instantly!")

# Κουτί Drag & Drop
st.markdown('<div class="drag-container">Drag & Drop your HEIC files here 👇</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Choose HEIC files",
    type=["heic"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# Λογική μετατροπής
if uploaded_files:
    output_images = []

    with st.spinner('🔄 Converting your images, please wait...'):
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

        st.success("✅ Conversion complete!")
        st.download_button(
            label="📥 Download All JPGs as ZIP",
            data=zip_buffer,
            file_name="converted_jpgs.zip",
            mime="application/zip"
        )
else:
    st.info("Please upload HEIC files to start the conversion.")

# Γραμμή χωρισμού
st.markdown("---")

# Κουμπί Donate
st.markdown(
    """
    <div style="text-align: center; margin-top: 20px;">
        <a href="https://paypal.me/uomoathens?country.x=GR&locale.x=en_US" target="_blank">
            <button style="background-color:#007BFF; color:white; border:none; border-radius:10px; font-size:18px; padding:12px 30px; cursor:pointer;">
                Donate via PayPal
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Footer
st.markdown("---")
st.caption("Made with ❤️ | Free Cloud HEIC to JPG Converter by uomoathens")
