import colorsys
import copy
import math

# def average_hsv(hsv_list):
#     if not hsv_list:
#         return 0, 0, 0
    
#     total_weight = 0
#     weighted_x_sum = 0  # For hue x-component
#     weighted_y_sum = 0  # For hue y-component
#     weighted_saturation_sum = 0
#     max_value = 0
    
#     for hsv in hsv_list:
#         h, s, v = hsv
#         weight = v  # Weight by value
        
#         # Skip completely black or zero-value colors
#         if v <= 0:
#             continue
            
#         # Convert hue to x,y coordinates on a unit circle
#         h_rad = h * (math.pi / 180)  # Convert degrees to radians
#         x = math.cos(h_rad)
#         y = math.sin(h_rad)
        
#         total_weight += weight
#         weighted_x_sum += x * weight
#         weighted_y_sum += y * weight
#         weighted_saturation_sum += s * weight
#         max_value = max(max_value, v)
    
#     if total_weight == 0:
#         return 0, 0, 0
        
#     # Calculate average x,y coordinates
#     avg_x = weighted_x_sum / total_weight
#     avg_y = weighted_y_sum / total_weight
    
#     # Convert back to hue angle
#     average_hue = math.atan2(avg_y, avg_x) * (180 / math.pi)
    
#     # Ensure hue is in range 0-360
#     average_hue = (average_hue + 360) % 360
    
#     average_saturation = weighted_saturation_sum / total_weight
    
#     return average_hue, average_saturation, max_value


# Provide a list or tuple of HSV tuples
def average_hsv(hsv_list):
    total_weight = 0
    weighted_hue_sum = 0
    weighted_saturation_sum = 0
    max_value = 0

    for hsv in hsv_list:
        h, s, v = hsv
        weight = v
        total_weight += weight
        weighted_hue_sum += h * weight
        weighted_saturation_sum += s * weight
        max_value = max(max_value, v)

    if total_weight == 0:
        return 0, 0, 0

    average_hue = weighted_hue_sum / total_weight
    average_saturation = weighted_saturation_sum / total_weight

    return average_hue, average_saturation, max_value

class GradientStop:
    def __init__(self, position, color):
        self.position = position
        self.color = color

class Gradient:
    def __init__(self):
        self.stops = []
        self.brightness = 1.0  # Default brightness

    def add_stop(self, position, color):
        stop = GradientStop(position, color)
        self.stops.append(stop)

    def set_brightness(self, brightness):
        if not 0.0 <= brightness <= 1.0:
            raise ValueError("Brightness must be in the range [0.0, 1.0]")
        self.brightness = brightness

    def get_rgb_at_position(self, position):
        # Clamp position to [0.0, 1.0]

        position = max(0.0, min(1.0, position))

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

        # Adjust brightness
        adjusted_color = tuple(int(c * self.brightness) for c in interpolated_color)

        return adjusted_color

    def get_hsv_at_position(self, position):
        rgb = self.get_rgb_at_position(position)
        return colorsys.rgb_to_hsv(*rgb)
    
rainbow = Gradient()

for i in range(0, 360, 60):
    rgb = colorsys.hsv_to_rgb(i/360, 1, 1)
    rainbow.add_stop(i/360, tuple(int(x * 255) for x in rgb))

# blink_gradient_1_stops = [
#     (0, (0, 0, 0)),
#     (20, (0, 255, 124)),
#     (32, (0, 249, 255)),
#     (35, (0, 249, 255)),
#     (44, (0, 198, 255)),
#     (59, (145, 0, 255)),
#     (100, (0, 0, 0))
# ]

# Shift the white peak slightly to the left
# blink_grayish_cyan_stops = [
#     (0, (0, 0, 0)),
#     (18, (120, 180, 190)),
#     (28, (180, 220, 230)),
#     (35, (255, 255, 255)),  # Shifted peak left
#     (44, (255, 255, 255)),  # Extended white area, slightly earlier
#     (52, (180, 220, 230)),
#     (67, (120, 180, 190)),
#     (100, (0, 0, 0))
# ]

grayscale_stops = [
    (0, (0, 0, 0)),          # Black
    (16, (179, 179, 179)),   # 70% Gray
    (25, (255, 255, 255)),   # White Peak Start
    (39, (255, 255, 255)),   # White Peak End
    (52, (230, 230, 230)),   # 90% Gray
    (100, (0, 0, 0))         # Black
]


blink_gradient_1 = Gradient()
on_gradient_1 = Gradient()
off_gradient_1 = Gradient()

for idx, tup in enumerate(grayscale_stops):
    position = tup[0]
    color = tup[1]

    blink_gradient_1.add_stop(position / 100, color)

    if idx <= 2:
        on_gradient_1.add_stop(position / grayscale_stops[2][0], color)
    else:
        offset = grayscale_stops[3][0]
        off_gradient_1.add_stop((position - offset) / (100 - offset), color)

blink_gradient_1_dimmed = copy.deepcopy(blink_gradient_1)
on_gradient_1_dimmed = copy.deepcopy(on_gradient_1)
off_gradient_1_dimmed = copy.deepcopy(off_gradient_1)

# blink_gradient_1_dimmed.set_brightness(0.5)
# on_gradient_1_dimmed.set_brightness(0.5)
# off_gradient_1_dimmed.set_brightness(0.5)
