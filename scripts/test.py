blink_gradient_1_stops = [
    (0, (0, 0, 0)),
    (20, (0, 255, 124)),
    (32, (0, 249, 255)),
    (35, (0, 249, 255)),
    (44, (0, 198, 255)),
    (59, (145, 0, 255)),
    (100, (0, 0, 0))
]
for idx, tup in enumerate(blink_gradient_1_stops):
    position = tup[0]
    color = tup[1]

    print(position, color)