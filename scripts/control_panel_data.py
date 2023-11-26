data = {
    'octave': 4, # 2, 3, 4, 5, 6
    'chord': 'None', # 'Major', 'Minor', 'None'
    'inversion': 'Root', # '1st Inv', '2nd Inv', 'Root'
    'hold': False,
    'instrument': 0 # Instrument index number
}

# Ensures that no new keys are accidentally added to the data dictionary
def get_data(key):
    global data

    if key in data:
        return data[key]
    else:
        raise KeyError(f'Key "{key}" not found in data dictionary')
    
def set_data(key, value):
    global data
        
    if key in data:
        data[key] = value
    else:
        raise KeyError(f'Key "{key}" not found in data dictionary')