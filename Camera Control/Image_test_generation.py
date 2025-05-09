from tracking import Pixel
from tracking import Image
import random
def create_images(x, y, threshold) -> list[list]:
    image_lst = []
    for j in range(y):
        image_lst.append([])
        for i in range(x):
            pixel_type = random.randint(0, 9)
            # Dark pixels
            if pixel_type == 0:
                #print("Zero")
                image_lst[j].append(0)
            # Below threshold pixel
            elif pixel_type < 9:
                #print("Low")
                # random.random produces a float in the interval [0, 1)
                image_lst[j].append(random.random() * threshold)
            # Produces a pixel of brightness between 1 and 1.5 times the threshold
            elif pixel_type == 9:
                #print("High")
                image_lst[j].append((random.random() / 2 + 1) * threshold)
    return image_lst

image = create_images(5, 5, 10)

for row in image:
    print(row)

img_object = Image(image, 10)

print("\nObject attributes:")
print(f"Size x = {img_object.size_x}")
print(f"Size y = {img_object.size_y}")
print(f"Threshold = {img_object.threshold}")

print("\nFiltered pixels:")
print(img_object.filter_threshold())

print("\nFiltered Image:")
clear_obj, clear_lst = img_object.clear_image()
for row in clear_lst:
    print(row)

print("\nAdjacent pixels:")
for pixel in img_object.filter_threshold():
    print(f"Pixel: {pixel}")
    print(f"Adjacent pixels: {img_object.adjacent_pixels(pixel, [])}")