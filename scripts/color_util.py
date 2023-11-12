import colorsys

class GradientStop:
    def __init__(self, position, color):
        self.position = position
        self.color = color

class Gradient:
    def __init__(self):
        self.stops = []

    def add_stop(self, position, color):
        stop = GradientStop(position, color)
        self.stops.append(stop)

    def get_color_at_position(self, position):
        # Sort stops by position
        sorted_stops = sorted(self.stops, key=lambda stop: stop.position)

        # Find the two stops between which the position lies
        for i in range(len(sorted_stops) - 1):
            if sorted_stops[i].position <= position <= sorted_stops[i + 1].position:
                start_stop = sorted_stops[i]
                end_stop = sorted_stops[i + 1]
                break
        else:
            # If position is outside the stops, return a default color (e.g., black)
            return (0, 0, 0)

        # Interpolate the color
        t = (position - start_stop.position) / (end_stop.position - start_stop.position)
        interpolated_color = (
            int((1 - t) * start_stop.color[0] + t * end_stop.color[0]),
            int((1 - t) * start_stop.color[1] + t * end_stop.color[1]),
            int((1 - t) * start_stop.color[2] + t * end_stop.color[2])
        )

        return interpolated_color
    
rainbow = Gradient()

for i in range(0, 360, 60):
    rgb = colorsys.hsv_to_rgb(i/360, 1, 1)
    rainbow.add_stop(i/360, tuple(int(x * 255) for x in rgb))

rainbow.add_stop(1, (255, 0, 0))