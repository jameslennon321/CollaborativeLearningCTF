import math

def distance(a, b):
	return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def normalized_move(a, action, speed):
	delta = action.value
	magnitude = math.sqrt(delta[0]**2 + delta[1]**2)

	if magnitude == 0:
		return a

	return (a[0] + delta[0]*speed/magnitude, a[1] + delta[1]*speed/magnitude)

def make_in_range(pos, width, height):
	return (max(min(pos[0], width), 0),
		    max(min(pos[1], height), 0))
