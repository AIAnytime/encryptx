import streamlit as st
from cryptography.fernet import Fernet
from PIL import Image
import io

# Set page configuration
st.set_page_config(
    page_title="Image Encryption App",
    page_icon="🔒",
    layout="wide"
)

# Function to generate a key
def generate_key():
    return Fernet.generate_key()

# Function to encrypt the image
def encrypt_image(image_bytes, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(image_bytes)
    return encrypted_data

# Function to decrypt the image
def decrypt_image(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data

# Streamlit app
st.markdown("<h1 style='text-align: center; color: blue;'>Image Encryption for Secure Internet Transfer</h1>", unsafe_allow_html=True)

st.write("This app allows you to upload an image, encrypt it for secure transfer, and then download the encrypted image.")

# Initialize session state for the key and encrypted image
if 'key' not in st.session_state:
    st.session_state.key = None
if 'encrypted_image' not in st.session_state:
    st.session_state.encrypted_image = None

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        uploaded_file.seek(0)  # Reset the file pointer to the start
        image_bytes = uploaded_file.read()
        
    with col2:
        if st.session_state.key is None:
            st.session_state.key = generate_key()
        if st.session_state.encrypted_image is None:
            st.session_state.encrypted_image = encrypt_image(image_bytes, st.session_state.key)
        
        st.write("Image encrypted successfully!")
        
        st.download_button(label="Download Encrypted Image", data=st.session_state.encrypted_image, file_name="encrypted_image.bin", mime="application/octet-stream")
        
        st.write("Save this key securely to decrypt the image later:")
        st.code(st.session_state.key.decode())
        
        decrypt = st.checkbox("Decrypt image (For demonstration purposes)")
        
        if decrypt:
            try:
                decrypted_image_bytes = decrypt_image(st.session_state.encrypted_image, st.session_state.key)
                decrypted_image = Image.open(io.BytesIO(decrypted_image_bytes))
                st.image(decrypted_image, caption='Decrypted Image.', use_column_width=True)
            except Exception as e:
                st.error(f"Error decrypting image: {e}")

# Run the app with: streamlit run image_encryption_app.py
