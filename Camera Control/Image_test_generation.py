import random
def create_images(x, y, threshold) -> list[list]:
    image_lst = []
    for j in range(y):
        image_lst.append([])
        for i in range(x):
            pixel_type = random.randint(0, 9)
            # Below threshold pixel
            if pixel_type == 0:
                print("Zero")
                image_lst[j].append(0)
            elif pixel_type < 9:
                print("Low")
                # random.random produces a float in the interval [0, 1)
                image_lst[j].append(random.random() * threshold)
            # Produces a pixel of brightness between 1 and 1.5 times the threshold
            elif pixel_type == 9:
                print("High")
                image_lst[j].append((random.random() / 2 + 1) * threshold)
    return image_lst

image = create_images(6, 6, 10)
for row in image:
    print(row)