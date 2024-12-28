import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

def process_image(image, canny_threshold1, canny_threshold2, epsilon):
    # Convert PIL image to OpenCV format
    image = np.array(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Edge detection
    edges = cv2.Canny(gray, canny_threshold1, canny_threshold2)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Simplify contours
    simplified_contours = [cv2.approxPolyDP(cnt, epsilon, closed=True) for cnt in contours]

    # Draw dots and numbers
    for i, cnt in enumerate(simplified_contours):
        for j, point in enumerate(cnt):
            x, y = point[0]
            cv2.circle(image, (x, y), 3, (0, 0, 255), -1)
            cv2.putText(image, str(j+1), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    return image

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
    processed_image_pil.save(buf, format="JPEG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download Processed Image",
        data=byte_im,
        file_name="dot_to_dot_image.jpg",
        mime="image/jpeg"
    )