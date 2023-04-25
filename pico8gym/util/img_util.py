import base64
import time
import cv2
import numpy as np
from PIL import Image
from term_image.image import AutoImage
import os

# fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
# video=cv2.VideoWriter('testvideo.mp4',fourcc,1,(128,128))

def b64_decode_img(b64Img: str):
    b64Img = b64Img.replace("data:image/png;base64,", "")
    if len(b64Img) == 0:
        return np.array([])
    imgdata = base64.b64decode(b64Img)

    nparr = np.frombuffer(imgdata, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_np

def fancy_print_image(img):
    if np.size(img) == 0:
        return
    os.system('cls' if os.name == 'nt' else 'clear')
    pilImg = Image.fromarray(img[:,:,::-1], 'RGB')
    consoleImg = AutoImage(pilImg)
    print(consoleImg)

def save_image(filename, img):
    if img is None:
        return
    cv2.imwrite(filename, img)

if __name__ == "__main__":
    img = cv2.imread("testing.jpg")
    img = cv2.resize(img, (32,32))
    fancy_print_image(img)

    for _ in range(100):
        time.sleep(0.1)
        img = np.roll(img, 10, 0)
        fancy_print_image(img)