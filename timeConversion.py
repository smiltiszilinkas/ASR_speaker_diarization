def time_to_miliseconds(time_str):
    # Split the string at ':'
    time_parts = time_str.split(':')
    
    # Convert minutes, seconds, and miliseconds to integers
    minutes = int(time_parts[0])
    seconds = int(time_parts[1])
    miliseconds = int(time_parts[2])
    
    # Calculate the total miliseconds
    total_seconds = minutes * 60 + seconds
    total_miliseconds = total_seconds * 1000 + miliseconds
    
    return total_miliseconds

def seconds_to_miliseconds(seconds_str):
    # convert to integer
    seconds = int(seconds_str)
    # calculate total miliseconds 
    total_miliseconds = seconds * 1000
    return total_miliseconds