import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

def process_image(image, canny_threshold1, canny_threshold2, epsilon):
    # Convert PIL image to OpenCV format
    image = np.array(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Create an alpha channel with full transparency
    alpha_channel = np.ones(gray.shape, dtype=gray.dtype) * 255

    # Edge detection
    edges = cv2.Canny(gray, canny_threshold1, canny_threshold2)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Simplify contours
    simplified_contours = [cv2.approxPolyDP(cnt, epsilon, closed=True) for cnt in contours]

    # Draw dots
    for cnt in simplified_contours:
        for point in cnt:
            x, y = point[0]
            cv2.circle(alpha_channel, (x, y), 3, (0, 0, 0), -1)  # Draw black dots on alpha channel

    # Merge the grayscale image with the alpha channel
    transparent_image = cv2.merge([gray, gray, gray, alpha_channel])

    return transparent_image

st.title("Advanced Dot-to-Dot Image Converter")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")

    st.sidebar.header("Adjust Parameters")
    canny_threshold1 = st.sidebar.slider("Canny Threshold 1", 0, 255, 50)
    canny_threshold2 = st.sidebar.slider("Canny Threshold 2", 0, 255, 150)
    epsilon = st.sidebar.slider("Contour Approximation Epsilon", 1, 30, 5)

    st.write("Processing...")
    processed_image = process_image(image, canny_threshold1, canny_threshold2, epsilon)
    st.image(processed_image, caption='Processed Image.', use_column_width=True)

    # Convert processed image to PIL format for download
    processed_image_pil = Image.fromarray(processed_image)
    buf = io.BytesIO()
    processed_image_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download Processed Image",
        data=byte_im,
        file_name="dot_to_dot_image.png",
        mime="image/png"
    )