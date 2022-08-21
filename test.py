
from blessed import Terminal
while True:
    print(Terminal().width)
    print(Terminal().height)


# map gen:

# import numpy as np
# from perlin_noise import PerlinNoise
# import matplotlib.pyplot as plt
#
# width = 100
# height = 100
#
# #replace with own eventually, this is not random
# noise = PerlinNoise(octaves=10)
# pic = [[noise([i/width, j/height]) for j in range(width)] for i in range(height)]
#
# plt.imshow(pic, cmap='gray')
# plt.show()
#
# tree_map = np.zeros((height,width))
# print(tree_map)
# for i in range(width):
#     for j in range(height):
#         pixel = pic[i][j]
#         if pixel > 0.1:
#             tree_map[j,i]=1
#
# plt.imshow(tree_map, cmap='gray')
# plt.show()
