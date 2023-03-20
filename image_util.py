# Intro

+ 模块`cv2`的名字是`opencv-python`

# 图片裁剪
```python
import cv2


def cat(
    imgpath: str,
    height_range: tuple(int, int),
    weight_range: tuple(int, int),
    distimgpath: str
) -> None:
    img = cv2.imread(imgpath)
    # height, width, _ = img.shape
    # 注意!, 这里因为懒我没有检测数值是否正确
    new_img = img[height_range[0]: height_range[1], weight_range[0]: weight_range[1]]
    cv2.imwrite("new_img.jpg", new_img)  # 不写了不写了, 意思意思得了
    # cv2.imshow("new_img", new_img)
    # cv2.waitKey(0)
```

+ `imread`有两个参数，第二个参数即读取模式（默认1彩色，0灰度模式，-1alpha）
	对应着返回值的`shape`属性即为长宽和模式

# 颜色翻转
保存方案见[这里](#图片裁剪)
## 黑白
```python
import cv2


def img_col_reverse_bw(imgpath):
    img = cv2.imread(imgpath, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dist = 255 - gray
    
    cv2.imshow('img', img)
    cv2.imshow('gray', gray)
    cv2.imshow('dst', dist)
    
    cv2.waitKey(0)
```
## 彩色
```python
def img_col_reverse_co(imgpath):
    img = cv2.imread(imgpath, 1)
    dist = 255 - img
    
    cv2.imshow('img', img)
    cv2.imshow('dst', dist)
    cv2.waitKey(0)
```