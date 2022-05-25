import math

_length = 3000
_width = 2000
_robot_width = 150
_x = 0
_y = 0
_theta = 0
side = ""

def initialisation(color):
    global _length
    global _width
    global _robot_width
    global _x
    global _y
    global _theta
    global side

    side = color
    
    if side == "YELLOW":
        _x = 700
        _y = 150
        _theta = 0
    else :
        _x = 700
        _y = 2850
        _theta = 0

def move_position(distance):
    global _x
    global _y
    global _theta
    global side

    x = distance * math.sin(math.radians(_theta))
    
    y = distance * math.cos(math.radians(_theta))

    if side != "YELLOW" :
        y = - y
        x = - x
    
    _y += y
    _x += x

    

def move_angle(angle):
    global _theta
    global side

    if side != "YELLOW" :
        angle = - angle


    _theta += angle

    if _theta < -360:
        _theta = _theta % -360
    elif _theta > 360:
        _theta =_theta % 360
    if _theta > 180:
        _theta = _theta - 360
    elif _theta < -180:
        _theta = 360 + _theta
    #_theta = _theta % 360 - 180


def capteur_av():
    global _length
    global _width
    global _robot_width
    global _x
    global _y
    global _theta
    global side

    if side == "YELLOW" :
        if _theta <= 45 and _theta >= -45:
            _y = _length - _robot_width
        elif _theta > 45 and _theta <= 135:
            _x = _width - _robot_width
        elif _theta < -45 and _theta >= -135:
            _x = _robot_width
        elif (_theta < -135 and _theta >= -180) or (_theta > 135 and _theta <= 180) :
            _y = _robot_width
    
    else :
        if _theta <= 45 and _theta >= -45:
            _y = _robot_width
        elif _theta > 45 and _theta <= 135:
            _x = _robot_width
        elif _theta < -45 and _theta >= -135:
            _x = _width - _robot_width
        elif (_theta < -135 and _theta >= -180) or (_theta > 135 and _theta <= 180) :
            _y = _length - _robot_width

        


def capteur_arr():
    global _length
    global _width
    global _robot_width
    global _x
    global _y
    global _theta
    global side

    if side != "YELLOW" :
        if _theta <= 45 and _theta >= -45:
            _y = _length - _robot_width
        elif _theta > 45 and _theta <= 135:
            _x = _width - _robot_width
        elif _theta < -45 and _theta >= -135:
            _x = _robot_width
        elif (_theta < -135 and _theta >= -180) or (_theta > 135 and _theta <= 180) :
            _y = _robot_width
    
    else :
        if _theta <= 45 and _theta >= -45:
            _y = _robot_width
        elif _theta > 45 and _theta <= 135:
            _x = _robot_width
        elif _theta < -45 and _theta >= -135:
            _x = _width - _robot_width
        elif (_theta < -135 and _theta >= -180) or (_theta > 135 and _theta <= 180) :
            _y = _length - _robot_width


if __name__ == "__main__":
    initialisation("YELLOW")
    print(_x,_y,_theta)
    move_position(450)
    move_position(-30)
    move_angle(-140)
    move_angle(-60)
    print(_x,_y,_theta)
    move_position(50)
    move_angle(-160)
    print(_x,_y,_theta)
    move_angle(450)
    move_position(50)
    print(_x,_y,_theta)
    capteur_av()
    move_angle(50)
    capteur_arr()
    print(_x,_y,_theta)


