def read_rectangles(file):
    with open(file) as f:
        frame_count = 0
        result = {}
        for line in f:
            values = [value for value in line.split(' ')]
            values.pop()
            result[f'frame{frame_count}'] = [int(value) for value in values]
            frame_count += 1

    dict = {
        'frame count': frame_count,
        'template': '[x, y, w, h]',
        'data': result
    }
    
    return dict
    
    
def read_landmarks(file):
    with open(file) as f:
        frame_count = 0
        result = {}
        for line in f:
            values = [value for value in line.split(' ')]
            values.pop()
            result[f'frame{frame_count}']={}
            i = 0
            while i < len(values):
                result[f'frame{frame_count}'][f'l{int(i/2)}']=[values[i], values[i+1]]
                i += 2
            frame_count += 1

    dict = {
        'frame count': frame_count,
        'template': '51 (x,y) landmarks',
        'data': result
    }
    
    return dict


def read_pose(file):
    with open(file) as f:
        frame_count = 0
        result = {}
        for line in f:
            #first three are translation ignore middle three last three are angles
            values = [value for value in line.split(' ')]
            values = values[0:3] + values[6:]
            values.pop()
            result[f'frame{frame_count}'] = values
            frame_count += 1

    dict = {
        'frame count': frame_count,
        'template': '[Tx, Ty, Tz, Rx, Ry, Rz]',
        'data': result
    }

    return dict

    
def read_expression(file):
    with open(file) as f:
        frame_count = 0
        result = {}
        for line in f:
            values = [value for value in line.split(' ')]
            values.pop()
            result[f'frame{frame_count}']=values
            frame_count += 1

    dict = {
        'frame count': frame_count,
        'template': '[expression coefficients]',
        'data': result
    }
    
    return dict


def read_canonical_landmarks(file):
    with open(file) as f:
        frame_count = 0
        result = {}
        for line in f:
            values = [value for value in line.split(' ')]
            values[-1] = values[-1].replace('\n','')
            result[f'frame{frame_count}']={}
            i = 0
            while i < len(values):
                result[f'frame{frame_count}'][f'l{int(i/3)}']=[values[i], values[i+1], values[i+2]]
                i += 3
            frame_count += 1

    dict = {
        'frame count': frame_count,
        'template': '51 (x,y,z) landmarks',
        'data': result
    }
    
    return dict