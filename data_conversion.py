import sys
import json
import cv2
import numpy

filename = sys.argv[1]
frame = cv2.imread('converted_frames/' + filename)
frame_data = []

# change the data to be represented as a 0 or a 1
for i in range(frame.size // frame[0].size):
    row = []
    # this is the colormap of our image
    # 1 - white; 0 - black
    for j in range(frame[0].size // 3):
        if (frame[i][j][0] == 255):
            row.append(1)
        else:
            row.append(0)
    frame_data.append(row)

def is_perimeter(y, x):
    if y-1 > 0:
        if frame_data[y-1][x] == 0:
            return True
    if y+1 < len(frame_data):
        if frame_data[y+1][x] == 0:
            return True
    if x-1 > 0:
        if frame_data[y][x-1] == 0:
            return True
    if x+1 < len(frame_data[0]):
        if frame_data[y][x+1] == 0:
            return True
    return False

# we are keeping a hashmap of our islands in the form of color:size
islands = {}
color = 2

# now we will do dfs on the frame data and detect the edges
visited = set()
stack = []
for y in range(len(frame_data)):
    for x in range(len(frame_data[0])):
        if (y,x) in visited:
            continue
        visited.add((y,x))
        if frame_data[y][x] != 0:
            # size of the current island
            size = 0
            stack.append((y,x))
            while len(stack) > 0:
                #instead of creating a new tuple and checking visited.contains(tuple), do frame_data == 1?
                if y-1 > 0 and (y-1,x) not in visited:
                    if frame_data[y-1][x] != 0:
                        stack.append((y-1,x))
                if y+1 < len(frame_data) and (y+1,x) not in visited:
                    if frame_data[y+1][x] != 0:
                        stack.append((y+1,x))
                if x-1 > 0 and (y,x-1) not in visited:
                    if frame_data[y][x-1] != 0:
                        stack.append((y,x-1))
                if x+1 < len(frame_data[0]) and (y,x+1) not in visited:
                    if frame_data[y][x+1] != 0:
                        stack.append((y,x+1))
                coords = stack.pop()
                visited.add(coords)
                y, x = coords[0], coords[1]
                # do orthogonal adjacency check and recolor node if it's on the perimeter
                if is_perimeter(y, x) == True:
                    frame_data[y][x] = color
                    size += 1
            islands[color] = size
            color += 1
            #TODO: make sure the coordinates are linked to the island colors




# this goes from binary representation back to rgb
# set frame_data[y][x] > 1 instead of = 1 for edge detection!
new_frame = numpy.zeros((len(frame_data), len(frame_data[0]), 3), int)
for y in range(len(frame_data)):
    for x in range(len(frame_data[0])):
        if frame_data[y][x] > 1:
            new_frame[y][x] = [255,153,238]

cv2.imwrite('outlines/perimeter_'+filename, new_frame)

print(islands)
