import random
from statistics import mean

class Plotter:
    def __init__(self,data):
        self.data = data
        self.t = 1
        self.dict = []
        self.u_x = 0
        self.u_y = 0

    #adding positions obtained to the dictionary
    def position(self,v_x, v_y):
        a = (v_x/1000, v_y/1000)
        self.dict.append(a)

    #Calculation of the positions
    def plotter_math(self,id):
        di_x = self.data.getAccel(id,'acc_x_g')
        di_y = self.data.getAccel(id,'acc_y_g')
        self.t = 1
        self.dict = []
        self.u_x = 0
        self.u_y = 0
        i = 0
        t = 1
        n = (len(di_x) - 1)
        v_x = 0
        v_y = 0
        while i <= n:

            a_x = di_x[i] #current accels from csv file
            a_y = di_y[i]

           #print("u_x previous value is ",self.u_x)
            s_x = (self.u_x*t)+(0.5*(a_x*t)) # we get displacemnt s
            #print("s_x calculated value",s_x)
            s_y = (self.u_y*t)+(0.5*(a_y*t))

            v_x += s_x
            v_y += s_y

            self.position(v_x, v_y) #stores all calulated cordinates in dict list
            #print("v_x sent to dict is",v_x)
            ##print(v_x,",",v_y)###uncomment this for #printing the values
            #print("-------------------------")
            self.u_x = a_x
            self.u_y = a_y

            i+=1

        return(self.dict)

    #Normalizing the coordinates obtained
    def normalize(self, coords_x, coords_y):
        starting_x = coords_x[0]
        starting_y = coords_y[0]

        final_x = coords_x[len(coords_x) - 1]
        final_y = coords_y[len(coords_y) - 1]

        average_x = (starting_x + final_x) / 2
        average_y = (starting_y + final_y) / 2

        rand_x = random.randint(-1, 1)
        rand_y = random.randint(-1, 1)

        for i in range(len(coords_x)):
            coords_x[i] = coords_x[i] - average_x + rand_x

        for i in range(len(coords_y)):
            coords_y[i] = coords_y[i] - average_y + rand_y

        return coords_x, coords_y


    #Average of coordinates
    def plot(self,cowid):
            _data = self.plotter_math(cowid)
            AVG_RES = 160
            coords_x = []
            coords_y = []
            for coord in _data:

                coords_x.append(coord[0])
                coords_y.append(coord[1])

            i = 0
            _cordxavg = []
            _cordxavgcache = []

            for n in range(0,len(coords_x)):
                _cordxavgcache.append(coords_x[n]) #append current coord to cache
                i += 1

                if i % AVG_RES == 0: #every AVG_RES of mesurments
                    i = 0
                    _cordxavg.append(mean(_cordxavgcache)) #append avg of cache to variable _cordxavg
                    _cordxavgcache = [] #clear cache

            i = 0
            _cordyavg = []
            _cordyavgcache = []

            for n in range(0,len(coords_y)):
                _cordyavgcache.append(coords_y[n]) #append current coord to cache
                i += 1

                if i % AVG_RES == 0: #every AVG_RES of mesurments
                    i = 0
                    _cordyavg.append(mean(_cordyavgcache)) #append avg of cache to variable _cordxavg
                    _cordyavgcache = [] #clear cache

            _cordxavg, _cordyavg = self.normalize(_cordxavg, _cordyavg)

            return(_cordxavg,_cordyavg)
