import base64
import cv2
import numpy as np

# fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
# video=cv2.VideoWriter('testvideo.mp4',fourcc,1,(128,128))

def b64_decode_img(b64Img: str):
    b64Img = b64Img.replace("data:image/png;base64,", "")
    print(b64Img)
    imgdata = base64.b64decode(b64Img)

    nparr = np.frombuffer(imgdata, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # cv2.imwrite("testing.jpg", img_np)
    print(img_np.shape)
    # cv2.imshow("picogym", img_np)
    # filename = 'testing.jpg'  # I assume you have a way of picking unique filenames
    # with open(filename, 'wb') as f:
    #     f.write(imgdata)
    # video.write(img_np)

if __name__ == "__main__":
    # for i in range(10):
    #     b64_decode_img("iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAABmJLR0QA/wD/AP+gvaeTAAADr0lEQVR4nO2aP44TMRhHv0TTb7sXQIgLIG2xuQE03AUOwDGgo0FIXCIp0tBzAYoUNDmBKUgGx/k8Y8cJXu3vPWm04xn/2/Gzxx5nYWbBQJZl7wqYmQV707sKsnQXIHwxs/0nCz++9a6KJF0FCL9fmr3d/Q28WFn48LVndWQJXY9fr0PY78LH95/71kP0WBxOLOwPPfHA4u7evZbG9a7F12NycV59D/bz3eIsPtyepdm/hkkbLQ6nDb24u3evzRGnO0Lj92OIA2kPbSUW43h+7TKgjRMBSnpwDV5+uVcG9GFyFRA3UtpgYb9zr5lNi+Slg36Mk0DQpPuHIOgLAoiDAOIggDgIIA4CiIMA4gzrzXYMrB4fLA2b2XgtF47x0t/iflqXXHyYZml2+uCO5/EDXj0+nIWnaLkfl1Waloa/nMHstBfVMjVitOZXkwYJLmMwa+tBuR7ZIkFtfY7lIUE9Z5PAY8PF79r1ZnvSoHMPe67x0/teOC0vV7+S8iAPm0HijHOAuEd7M+1cj59bReTyyuVZsipJ43t1j9Onf737Xh2m/p9c+pJVSW3+aX5zq7C0PlP1W+YSpCuD3DDrzdq9VUUpc/ldmkdpfp4Q3vO4dCWTe75TeKuwa83bmj8Epe/r0jRp+vjd3vpOr+mltfmVpG/NPzcixeFrrbSGiXjF1NhYMoy1zua9ES2WoHaVUjsildS/pj7eaHGtVdYy996pnfXXzNrnmMqvNH5reTUS1pZ/yQiRjpC17ZErk1WAOGwGiYMA4iCAOAggDgKIgwDiDLW/AKr99u/ll9Lybby1PiXf7p816802mFko/Zue5+556bwjl1dp+bX3p+queCwPEjwp+71v37UbOC3lKTH+JvDWD6H12/vct/KWDZinJP//ZhwBYub2lNO4Xh5eHA9v76EFrz5zu3lzew/PeYRgL0AcloHiIIA4CCAOAoiDAOIggDgIIA4CiIMA4iCAOAggDgKIgwDiIIA4CCAOAoiDAOIggDgIIA4CiIMA4iCAOAggDgKIgwDiIIA4CCAOAoiDAOIggDgIIA4CiIMA4iCAOAggDgKIgwDiIIA4CCAOAoiDAOIggDgIIA4CiIMA4iCAOAggDgKIgwDiIIA4CCAOAoiDAOIggDgIIA4CiIMA4iCAOAggDgKIgwDiIIA4CCAOAoiDAOIggDgIIA4CiIMA4iCAOAggDgKIgwDiIIA4CCAOAoiDAOIggDgIIA4CiIMA4iCAOAggDgKIgwDiIIA4fwASonFs+i+CqAAAAABJRU5ErkJggg==")
    # video.release()
    pass