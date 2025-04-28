import streamlit as st
import pyheif
from PIL import Image
import io
import zipfile

# Στήσιμο σελίδας με σκοτεινό στυλ
st.set_page_config(page_title="HEIC to JPG Cloud Converter", page_icon="📸", layout="centered")

# Custom CSS Styling
st.markdown(
    """
    <style>
    body {
        background-color: #0c111b;
        color: #f5f5f5;
    }
    .css-1d391kg {
        background-color: #0c111b;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        border: None;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        margin-top: 10px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
    }
    .css-1kyxreq, .css-ffhzg2 {
        background-color: #1c2230;
        border: 1px solid #2e374a;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Τίτλος και περιγραφή
st.title("📸 HEIC to JPG Converter")
st.write("Upload your HEIC images and get perfect JPGs instantly!")

# Upload HEIC αρχείων
uploaded_files = st.file_uploader("Choose HEIC files", type=["heic"], accept_multiple_files=True)

# Λογική μετατροπής με SPINNER
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
st.caption("Made with ❤️ | Free Cloud HEIC to JPG Converter by DS")
