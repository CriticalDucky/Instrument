LEDS_PER_NOTE = 13
LED_GROUPS = 12
LED_STRIP_SHIFT = LEDS_PER_NOTE * 4

def get_section_leds(section: int):
    start = (section - 1) * LEDS_PER_NOTE + 1
    end = section * LEDS_PER_NOTE

    return list(range(start, end + 1))

def get_section_center_leds(section: int, num_leds: int = 1): # Example: get_section_center_leds(1, 3) -> [6, 7, 8]
    center = (section - 1) * LEDS_PER_NOTE + 1 + (LEDS_PER_NOTE - num_leds) // 2

    return list(range(center, center + num_leds))

def offset_leds(leds: list, offset: int):
    return [led + offset for led in leds]

def pattern_leds(leds: list, size: int, gaps: int):
    new_leds = []

    for i in range(0, len(leds), size + gaps):
        new_leds += leds[i:i+size]

    return new_leds 

