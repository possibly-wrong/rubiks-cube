"""
Press 'x', 'y', 'z' (or uppercase) to rotate the corresponding face
counterclockwise (clockwise).

Set solve_cube=True and press 's' to make a move toward the solved cube.
Set draw_axes=True to draw axis arrows.
Set draw_labels=True to draw labels on cubies and cubicles.
"""

solve_cube = False
draw_axes = False
draw_labels = False

from vpython import *
import numpy as np
from rubik2 import *
import time
import itertools

# Load or compute spanning tree of the cube graph.
if solve_cube:
    print('Loading cube graph...')
    try:
        p = np.loadtxt('rubik2.dat', dtype='int32')
    except OSError:
        print('Computing cube graph...')
        tic = time.time()
        g = cubegraph()
        print('Elapsed time (sec):', time.time() - tic)
        print('Solving cube...')
        tic = time.time()
        solved = packcube((np.arange(7), np.zeros(7, dtype='int32')))
        p, d = bfs(g, solved)
        print('Elapsed time (sec):', time.time() - tic)
        np.savetxt('rubik2.dat', p, fmt='%d')
        print('Diameter of cube graph:', max(d), 'moves')

# Start with the solved cube state.
cube = (arange(7), np.zeros(7, dtype='int32'))
moves = ['x', 'X', 'y', 'Y', 'z', 'Z']

# Map keypresses to corresponding face colors and rotation axes.
faces = {'x': (color.red, (1, 0, 0)),
         'X': (color.orange, (-1, 0, 0)),
         'y': (color.white, (0, 1, 0)),
         'Y': (color.yellow, (0, -1, 0)),
         'z': (color.green, (0, 0, 1)),
         'Z': (color.blue, (0, 0, -1))}

# Create colored stickers on each face, one cubie at a time.
stickers = []
for face_color, axis in faces.values():
    for x in (-0.5, 0.5):
        for y in (-0.5, 0.5):

            # Start with all stickers on the top face, then rotate them "down"
            # to the appropriate face.
            sticker = box(color=face_color, pos=vec(x, y, 1),
                          length=0.98, height=0.98, width=0.05)
            cos_angle = dot(vec(0, 0, 1), vec(*axis))
            pivot = (cross(vec(0, 0, 1), vec(*axis))
                     if cos_angle == 0 else vec(1, 0, 0))
            sticker.rotate(angle=acos(cos_angle), axis=pivot,
                           origin=vec(0, 0, 0))
            stickers.append(sticker)
    scene.lights.append(distant_light(direction=vec(*axis),
                                      color=color.gray(0.3)))

# Optionally draw axis arrows.
if draw_axes:
    for axis in ('x', 'y', 'z'):
        face_color, axis = faces[axis]
        arrow(axis=2 * vec(*axis), color=face_color, shaftwidth=0.1)

# Optionally draw labels on cubies and cubicles.
if draw_labels:
    for x, y, z in itertools.product((0, 1), repeat=3):
        n = x + 2 * y + 4 * z
        text(text=str(n), align='center', color=color.gray(0.25),
             pos=vec(2 * x - 1, y - 0.5, z - 0.5),
             axis=vec(0, (0.5 - z) * (x - 0.5), (y - 0.5) * (x - 0.5)),
             up=vec(0, 0.5 - y, 0.5 - z),
             height=0.25)
        cubie = text(text=str(n), align='center', color=color.gray(0.75),
                     pos=vec(2 * x - 1, 1.5 * (y - 0.5), 1.5 * (z - 0.5)),
                     axis=vec(0, (0.5 - z) * (x - 0.5), (y - 0.5) * (x - 0.5)),
                     up=vec(0, 0.5 - y, 0.5 - z),
                     height=0.25)
        stickers.append(cubie)
        
# Get keyboard moves and rotate the corresponding face.
fps = 24
while True:
    key = scene.waitfor('keydown').key

    # Press 's' to solve the cube: find the keypress that moves to the
    # "predecessor" or next cube state on the path to the solution.
    if key.lower() == 's':
        v = p[packcube(cube)]
        if v != -1:
            next_cubes = [packcube(movecube(cube, move)) for move in cubemoves]
            key = moves[next_cubes.index(v)]

    # Visually rotate the face and update the current vertex in the cube graph.
    if key.lower() in faces:
        face_color, axis = faces[key.lower()]
        angle = ((pi / 2) if key.islower() else -pi / 2)
        for r in arange(0, angle, angle / fps):
            rate(fps)
            for sticker in stickers:
                if dot(sticker.pos, vec(*axis)) > 0.25:
                    sticker.rotate(angle=angle / fps, axis=vec(*axis),
                                   origin=vec(0, 0, 0))
        cube = movecube(cube, cubemoves[moves.index(key)])
