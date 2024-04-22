data = {
    'octave': 4, # 2, 3, 4, 5, 6
    'chord': 'None', # 'Major', 'Minor', 'None'
    'inversion': 0, # 0, 1, 2
    'instrument': 0, # Instrument index number
    'library': 0, # Library index number
    'play': False,
    'stop': False,
}

# Ensures that no new keys are accidentally added to the data dictionary
def get_data(key):
    # print(data)

    if key in data:
        return data[key]
    else:
        raise KeyError(f'Key "{key}" not found in data dictionary')
    
def set_data(key, value):
    # print(data)
        
    if key in data:
        data[key] = value
    else:
        raise KeyError(f'Key "{key}" not found in data dictionary')