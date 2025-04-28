import pyheif
from PIL import Image
import io
import zipfile

st.set_page_config(page_title="HEIC to JPG Cloud Converter", page_icon="📸", layout="centered")

st.title("📸 HEIC to JPG Cloud Converter")
st.write("Upload your HEIC images and get perfect JPGs instantly!")

uploaded_files = st.file_uploader("Choose HEIC files", type=["heic"], accept_multiple_files=True)

if uploaded_files:
    output_images = []

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

st.markdown("---")
st.caption("Made with ❤️ - Free Cloud HEIC to JPG Converter by Uomoathens")
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <a href="https://paypal.me/uomoathens?country.x=GR&locale.x=en_US" target="_blank">
            <button style="padding:12px 30px; background-color:#0070ba; color:white; border:none; border-radius:10px; font-size:18px; cursor:pointer;">
                ❤️ Donate via PayPal
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
