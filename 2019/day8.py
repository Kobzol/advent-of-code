import cv2
import numpy as np

layers = []
width = 25
height = 6

with open("input.txt") as f:
    data = f.read()

index = 0
while index < len(data):
    layer = []
    for i in range(width * height):
        layer.append(int(data[index]))
        index += 1
    layers.append(layer)


def find_pixel(layers, i):
    for l in layers:
        if l[i] != 2:
            return l[i]
    assert False


image = np.zeros((height, width, 3), np.uint8)
for i in range(height):
    for j in range(width):
        pixel = find_pixel(layers, i * width + j)
        image[i, j] = 255 if pixel == 1 else 0

cv2.imshow("Test", image)
cv2.waitKey()
