"""
Press 'F', 'B', 'L', 'R', 'U', 'D' (or lowercase) to rotate the
corresponding face clockwise (counterclockwise).
"""

from vpython import *

# Map keypresses to corresponding face colors and rotation axes.
faces = {'r': (color.red, (1, 0, 0)),
         'l': (color.orange, (-1, 0, 0)),
         'u': (color.white, (0, 1, 0)),
         'd': (color.yellow, (0, -1, 0)),
         'f': (color.green, (0, 0, 1)),
         'b': (color.blue, (0, 0, -1))}

# Create colored stickers on each face, one cubie at a time.
stickers = []
for face_color, axis in faces.values():
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):

            # Start with all stickers on the top face, then rotate them "down"
            # to the appropriate face.
            sticker = box(color=face_color, pos=vec(x, y, 1.5),
                          length=0.98, height=0.98, width=0.05)
            cos_angle = dot(vec(0, 0, 1), vec(*axis))
            pivot = (cross(vec(0, 0, 1), vec(*axis))
                     if cos_angle == 0 else vec(1, 0, 0))
            sticker.rotate(angle=acos(cos_angle), axis=pivot,
                           origin=vec(0, 0, 0))
            stickers.append(sticker)
    scene.lights.append(distant_light(direction=vec(*axis),
                                      color=color.gray(0.3)))

# Get keyboard moves and rotate the corresponding face.
fps = 24
while True:
    key = scene.waitfor('keydown').key
    if key.lower() in faces:
        face_color, axis = faces[key.lower()]
        angle = ((pi / 2) if key.islower() else -pi / 2)
        for r in arange(0, angle, angle / fps):
            rate(fps)
            for sticker in stickers:
                if dot(sticker.pos, vec(*axis)) > 0.5:
                    sticker.rotate(angle=angle / fps, axis=vec(*axis),
                                   origin=vec(0, 0, 0))
