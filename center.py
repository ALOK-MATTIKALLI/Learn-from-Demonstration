# this program gives the center of block b1 b2 and b3 using the .txt files 

import oakUtlis as oak
b1 = []
b2 = []
b3 = []

b1,b2,b3 = oak.findCenter()

print(b1)
print(b2)
print(b3)


# b = [[379, 306], [99, 25], [52, 43]]
# point_index = int(input('enter the point to be deleted 1st, 2nd, 3rd, etc\n'))-1
# # for i in range(len(b)-1):
# #     if b[i] == point:
# #         b.remove(point)
# #         break
# b.pop(point_index)
# print(b)