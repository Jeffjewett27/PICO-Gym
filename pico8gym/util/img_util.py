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

def draw_transparent_rect(img, pos1, pos2, color, opacity):
    sub_img = img[pos1[1]:pos2[1], pos1[0]:pos2[0]]
    white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255

    res = cv2.addWeighted(sub_img, 1 - opacity, white_rect, opacity, 1.0)

    # Putting the image back to its position
    img[pos1[1]:pos2[1], pos1[0]:pos2[0]] = res


def draw_controls(img: np.array, controls: int):
    padding = 3
    margin = 2
    btnSize = 8
    w, h, _ = img.shape
    def buttonCoords(r, c):
        x2 = w - padding - (btnSize + margin) * r
        y2 = w - padding - (btnSize + margin) * c
        x1 = x2 - btnSize
        y1 = y2 - btnSize
        return x1, y1, x2, y2
    buttons = [
        (2, 0, 0),
        (0, 0, 0),
        (1, 1, 0),
        (1, 0, 0),
        (3, 0, 1),
        (3, 1, 1)
    ]
    for i in range(len(buttons)):
        button = buttons[i]
        x1, y1, x2, y2 = buttonCoords(button[0], button[1])
        opacity = 0.8 if controls & 2**i else 0.2
        # cv2.rectangle(img, (x1, y1), (x2, y2), color=(255, 255, 255), thickness=cv2.FILLED)
        draw_transparent_rect(img, (x1, y1), (x2, y2), (200, 200, 200), opacity)

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