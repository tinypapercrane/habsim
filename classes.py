from windfile import WindFile
import math
import numpy
EARTH_RADIUS = float(6.371e6)

class Balloon:
	# self.lat, self.lon, self.vrate, self.alt, self.time [datetime]
	# self.airvector -> m/s (2-tuple)
	# self.history = [Location, Location, Location, Location]
	# self.history = [{‘lat’: 37, ...}, {‘lat’: 39, ...}, {‘lat’: 41, ...}]
    # self.history = Trajectory	


    def __init__(self, lat, lon, alt, time, ascent_rate=0, air_vector=None):
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.time = time
        self.ascent_rate = ascent_rate
        self.airvector = airvector
        self.history = []
    
    #converts these two numbers into a numpy array to represent the airvector
    def set_airvector(u, v):


    #write this one to convert airvector that's passed in (could be None), and if it's not none, convert it to a numpy array
    # also set the ascent_rate (self.vrate = vrate)
    def set_bearing(self, bearing, airspeed: float):
        NotImplemented 

#testing
wf = WindFile("2021012806_01.npz")
print(wf.get(30, 120, 50, 1612143049))

class Simulator:
    def __init__(self, wind_file):
        self.wind_file = wind_file
    # try to add airvector functionality
    def step(self, balloon, step_size: float):
        # get the wind at the location of the balloon
		# advance the location of the balloon
		# append the location to balloon.history
        windvector = self.wind_file.get(balloon.lat, balloon.lon, balloon.alt, balloon.time)
        distance_moved = (windvector * step_size)
        balloon.alt = balloon.vrate * step_size
        balloon.time += step_size
        dlat, dlon = self.lin_to_angular_velocities(balloon.lat, balloon.lon, *distance_moved) 
        balloon.lat += dlat
        balloon.lon += dlon
        balloon.history.append((balloon.lat, balloon.lon))
        return balloon.lat, balloon.lon
		

    def lin_to_angular_velocities(self, lat, lon, u, v): 
        dlat = math.degrees(v / EARTH_RADIUS)
        dlon = math.degrees(u / (EARTH_RADIUS * math.cos(math.radians(lat))))
        return dlat, dlon

	# do next, then try to add airvector functionality
    # step_size is on seconds
    # the original balloon.time + duration gives the final time taht simulation should finish
    def simulate(self, balloon, step_size, target=None, dur=None): 
        #NotImplemented
        if step_size < 0:
            raise Exception("step size cannot be negative")
        if until != None and dur != None:
            raise Exception("Trajectory simulation must either have a max altitude or specified duration, not both")
        list = [(balloon.lan, balloon.lon)]
        # if a is true, check if b is true (try to figure out this logic)
        # Shorten the step size on the last call to get close as possible to until or dur, 
        # get some other variable besides dur to keep track of total time spent in the air
        # instead of doing ballon.alt < target, try to calculate time in air, and use that as dur
        while balloon.alt > 0 and balloon.alt < target or balloon.time < dur:
            newLocation = step(balloon, step_size)
            list.append(newLoaction)

        #since on the last call the criteria for looping will be broken, this slice of 
        # the list eliminates the last history element
        #return a list that starts with the original location, and with every step call you add a new location
        return list

        # returns trajectory
        # call step repeatedly until either
		# 1) the balloon crashes
		# 2) if until is specified, the balloon reaches until (alt in meters)
		# 3) if dur is specified, after dur hours
		# throw an error if specified both
		# throw an error if step_size is negative or if dur is negative
        #throw an error if the vrate is going in the wromng direction/ won't ever hit target

#testing output code blow this point
balloon = Balloon(0, 30, 40, 1612143049)
simulate = Simulator(wf)
for i in range(1000):
    simulate.step(balloon, 1)
print(balloon.history)



