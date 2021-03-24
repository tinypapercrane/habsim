import datetime
from . import util
import math
import random
import bisect
import numpy as np
from windfile import WindFile
from datetime import timedelta, datetime
EARTH_RADIUS = float(6.371e6)


class Trajectory(list):
    # superclass of list
    def __init__(self, data=list()):
        super().__init__(data)
        self.data = data

    def duration(self):
        '''
        Returns duration in hours, assuming the first field of each tuple is a UNIX timestamp.
        '''
        # these are datetime objects, call .seconds()
        # rolls over with days
        return (self.data[len(self.data) - 1].time - self.data[0].time).total_seconds() / 3600

    def length(self):
        '''
        Distance travelled by trajectory in km.
        '''
        res = 0
        for i, j in zip(self[:-1], self[1:]):
            res += i.location.distance(j.location)
        return res

    def interpolate(self, time):
        # find where it is between locations
        # return location and altitude
        pass

class Record:
    def __init__(self, time, location, alt, vrate, airvector, windvector, groundelev):
        self.time = time
        self.location = location
        self.alt = alt
        # naming
        self.ascent_rate = vrate
        self.air_vector = airvector
        self.wind_vector = windvector
        #added 3/23
        self.groundelev = groundelev

class Location(tuple): # subclass of tuple, override __iter__
    # unpack lat and lon as two arguments when passed into a function, *
    EARTH_RADIUS = 6371.0

    # super class
    # dont store instance variables
    # define getter functions
    def __new__(self, lat, lon):
        print("new")
        return tuple.__new__(Location, (lat, lon))

    # def __init__(self, lat, lon):
    #     print("constructor")
    #     self.lat = lat
    #     self.lon = lon

    def getLon(self):
        return self[1]

    def getLat(self):
        return self[0]

    def distance(self, other):
        # change to indices
        return self.haversine(self[0], self.lon, other.lat, other.lon)

    def haversine(self, lat1, lon1, lat2, lon2):
        '''
        Returns great circle distance between two points.
        '''
        # what will happen if distance called between invalid point (lat out of bounds)
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2-lat1
        dlon = lon2-lon1

        a = math.sin(dlat/2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return EARTH_RADIUS * c

class ElevationFile:
    # res may not be 120
    resolution = 120 ## points per degree

    def __init__(self, path): # store
        self.data = np.load(path, 'r')

    def elev(self, lat, lon): # return elevation
        x = int(round((lon + 180) * resolution))
        y = int(round((90 - lat) * resolution)) - 1
        return max(0, data[y, x])

class Balloon:
    def __init__(self, lat, lon, alt, time, ascent_rate=0, air_vector=(0,0), elev, groundelev):
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.time = time
        self.ascent_rate = ascent_rate
        self.air_vector = np.array(air_vector)
        self.history = []
        #added 3/23
        self.elev = elev
        self.groundelev = groundelev

    def set_airvector(u, v):
        self.air_vector = np.array([u, v])

    # bearing of the airvector
    def set_bearing(self, bearing, airspeed: float):
        self.ascent_rate = ascent_rate
        # airspeed * sin(bearing), airspeed *cos(bearing) (make 0 degrees be the north pole)

    def update(self, loc=None, elev=None, alt=None, time=None, ascent_rate=0, air_vector=(0,0), wind_vector, groundelev):
        record = Record(time=time or self.time, loc=loc or (self.lat, self.lon), alt=alt or self.alt, ascent_rate=ascent_rate or self.ascent_rate, air_vector=air_vector or self.air_vector, wind_vector=wind_vector or self.wind_vector, groundelev=groundelev or self.groundelev)

#testing
#wf = WindFile("2021012806_01.npz")
#print(wf.get(30, 120, 50, 1612143049))
class Simulator:
    def __init__(self, wind_file):
        self.wind_file = wind_file
        #edited 3/23
    def step(self, balloon, step_size: float):
        if not balloon.elev:
            balloon.elev = self.elev.getElevation(balloon.loc)
        if not balloon.windvector:
            balloon.windvector = self.windfile.get(balloon.lat, balloon.lon, balloon.alt, balloon.time)
        #windvector = self.wind_file.get(balloon.lat, balloon.lon, balloon.alt, balloon.time)
        distance_moved = (windvector + balloon.air_vector) * step_size
        balloon.alt = balloon.ascent_rate * step_size
        balloon.time += timedelta(seconds=step_size)
        dlat, dlon = self.lin_to_angular_velocities(balloon.lat, balloon.lon, *distance_moved) 
        balloon.lat += dlat
        balloon.lon += dlon
        new_loc = balloon.lat, balloon.lon
        balloon.history.append((balloon.lat, balloon.lon))
        balloon.update(new_loc, elev=self.elev.getElevation(new_loc), wind_vector=self.windfile.get(new_loc), balloon.time, balloon.ascent_rate, balloon.airvector, balloon.windvector)
        return balloon.lat, balloon.lon
		

    def lin_to_angular_velocities(self, lat, lon, u, v): 
        dlat = math.degrees(v / EARTH_RADIUS)
        dlon = math.degrees(u / (EARTH_RADIUS * math.cos(math.radians(lat))))
        return dlat, dlon

    def simulate(self, balloon, step_size, target_alt=None, dur=None): 
        if step_size < 0:
            raise Exception("step size cannot be negative")
        if (target_alt and dur) or not (target_alt or dur):
            raise Exception("Trajectory simulation must either have a max altitude or specified duration, not both")
        step_history = [(balloon.lat, balloon.lon)]
        if not dur:
            dur = ((target_alt - balloon.alt) / balloon.ascent_rate) / 3600
        end_time = balloon.time + timedelta(hours=dur)
        while balloon.time < end_time:
            if balloon.time + timedelta(seconds=step_size) >= end_time:
                step_size = (end_time - balloon.time).seconds
            newLocation = step(balloon, step_size)
            total_airtime += step_size
            step_history.append(newLoaction)
        return step_history

#testing output code below this point
balloon = Balloon(0, 30, 40, datetime.utcfromtimestamp(1612143049))
simulate = Simulator(wf)
for i in range(1000):
    simulate.step(balloon, 1)
print(balloon.history)