import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import io

def convert_to_dotted_image(image, dot_distance=10, dot_size=2, dot_color='black'):
    # Convert image to grayscale
    gray_image = image.convert('L')
    
    # Create a new image with white background
    dotted_image = Image.new('RGB', gray_image.size, 'white')
    draw = ImageDraw.Draw(dotted_image)
    
    # Get the pixel data of the grayscale image
    pixels = np.array(gray_image)
    
    # Draw dots on the new image based on the pixel intensity
    for y in range(0, gray_image.height, dot_distance):
        for x in range(0, gray_image.width, dot_distance):
            if pixels[y, x] < 128:  # Darker pixels will have dots
                draw.ellipse((x-dot_size, y-dot_size, x+dot_size, y+dot_size), fill=dot_color)
    
    return dotted_image

st.title("Advanced Image to Dotted Image Converter")
st.write("Upload an image to convert it to a dotted image for children to connect and complete.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    dot_distance = st.slider("Dot Distance", min_value=5, max_value=50, value=10)
    dot_size = st.slider("Dot Size", min_value=1, max_value=10, value=2)
    dot_color = st.color_picker("Dot Color", value='#000000')
    
    st.write("Converting image...")
    dotted_image = convert_to_dotted_image(image, dot_distance, dot_size, dot_color)
    
    st.image(dotted_image, caption='Dotted Image', use_column_width=True)
    
    # Save the dotted image
    buffered = io.BytesIO()
    dotted_image.save(buffered, format="JPEG")
    st.download_button(
        label="Download Dotted Image",
        data=buffered,
        file_name="dotted_image.jpg",
        mime="image/jpeg"
    )