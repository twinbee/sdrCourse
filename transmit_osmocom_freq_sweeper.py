f = None

def sweeper(prob_lvl, f_min, f_max, step_size):
    global f
    if f is None:
        print("Initializing frequency to f_min:", f_min)
        f = f_min
    if prob_lvl:
        f += step_size
        print("Stepped frequency to:", f)
    if f >= f_max:
        print("Frequency wrapped to f_min:", f_min)
        f = f_min
    return f
