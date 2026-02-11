from pathlib import Path
import cv2
import numpy as np


def preprocess_image(path: str) -> str:
    input_path = Path(path)
    image = cv2.imread(str(input_path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        return path

    denoised = cv2.fastNlMeansDenoising(image)
    resized = cv2.resize(denoised, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    thresh = cv2.adaptiveThreshold(resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, 11)

    out_path = input_path.with_name(input_path.stem + "_clean.png")
    cv2.imwrite(str(out_path), thresh)
    return str(out_path)
