import streamlit as st
from PIL import Image, ImageDraw
import numpy as np

def convert_to_dotted_image(image, dot_distance=10):
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
                draw.ellipse((x-1, y-1, x+1, y+1), fill='black')
    
    return dotted_image

st.title("Image to Dotted Image Converter")
st.write("Upload an image to convert it to a dotted image for children to connect and complete.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    st.write("Converting image...")
    dotted_image = convert_to_dotted_image(image)
    
    st.image(dotted_image, caption='Dotted Image', use_column_width=True)
    
    # Save the dotted image
    dotted_image.save("dotted_image.jpg")
    st.write("Dotted image saved as dotted_image.jpg")