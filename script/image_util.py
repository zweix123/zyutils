import cv2  # python3 -m pip install opencv-python


def cat(
    imgpath: str,
    height_range: tuple(int, int),
    weight_range: tuple(int, int),
    distimgpath: str,
) -> None:
    img = cv2.imread(imgpath)
    # height, width, _ = img.shape
    # 注意!, 这里因为懒我没有检测数值是否正确
    new_img = img[height_range[0] : height_range[1], weight_range[0] : weight_range[1]]
    cv2.imwrite("new_img.jpg", new_img)  # 不写了不写了, 意思意思得了
    # cv2.imshow("new_img", new_img)
    # cv2.waitKey(0)


def img_col_reverse_bw(imgpath):
    img = cv2.imread(imgpath, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dist = 255 - gray

    cv2.imshow("img", img)
    cv2.imshow("gray", gray)
    cv2.imshow("dst", dist)

    cv2.waitKey(0)


def img_col_reverse_co(imgpath):
    img = cv2.imread(imgpath, 1)
    dist = 255 - img

    cv2.imshow("img", img)
    cv2.imshow("dst", dist)
    cv2.waitKey(0)
