objects = {}

def get_name(x):
    i = 0
    s = x.__class__.__name__ + '_'
    while(True):
        name = s + str(i)
        if name in objects:
            i += 1
    objects[name] = x
    return name
    