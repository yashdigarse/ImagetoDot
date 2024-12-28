import streamlit as st
import cv2
import numpy as np
from PIL import Image

def process_image(image):
    # Convert PIL image to OpenCV format
    image = np.array(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Simplify contours
    simplified_contours = [cv2.approxPolyDP(cnt, epsilon=5, closed=True) for cnt in contours]

    # Draw dots and numbers
    for i, cnt in enumerate(simplified_contours):
        for j, point in enumerate(cnt):
            x, y = point[0]
            cv2.circle(image, (x, y), 3, (0, 0, 255), -1)
            cv2.putText(image, str(j+1), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    return image

st.title("Dot-to-Dot Image Converter")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Processing...")

    processed_image = process_image(image)
    st.image(processed_image, caption='Processed Image.', use_column_width=True)