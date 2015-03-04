# JLW 17 Feb 15 attempt at OOP design for Spring-Mass-Damper model

from matplotlib import pyplot as plt

#### WORK IN PROGRESS

class Spring():
    
    def __init__(self, spring_const, free_length):
        
        self.spring_const = spring_const
        self.free_length = free_length

        print("init spring, spring_const = ", spring_const, "free_length = ", free_length)

    def calcSpringForce(self, length): #
        
        spring_force = ((self.free_length - length) * self.spring_const)

        return spring_force

    # usually, applied_force will be zero at start, equm will just be spring acting under gravity_force
                         
    def calcSpringEqumLength(self, gravity_force, applied_force):

        equm_length =  self.free_length + ((gravity_force + applied_force)/self.spring_const)

        print("gravity_force", gravity_force)

        return equm_length

class Damper():
    
    def __init__(self, damper_const):
                         
        self.damper_const = damper_const

    def calcDamperForce(self, vel): #

        damper_force = -(vel * self.damper_const)

        return damper_force

# car suspension strut, collection of Spring, mass, Damper
class Suspension():

    def __init__(self, g, mass, vel, initial_applied_force, spring_const, free_length, damper_const):

        self.mass = mass

        # Suspension object inits its own Spring and Damper objects                 
        self.spring = Spring(spring_const, free_length) ### should object name be capital "Spring"
        self.damper = Damper(damper_const)
        self.vel = vel
        self.applied_force = initial_applied_force
        self.g = g
        self.gravity_force = self.g * self.mass                 
                         
        # length starts at equm length according to spring
        # NOTE APPLIED FORCE SET TO ZERO FOR THIS SPECIFIC FUNC CALL
        self.length = self.spring.calcSpringEqumLength(self.gravity_force,0)#, self.applied_force) add later when app force is fn of time
        print("self.length in init", self.length)

    # I don't like the name for this method... maybe suspensionTimeStep?
    def calcSuspensionPosition(self, time_step, elapsed_time):

        # calc forces, first find spring and damper forces
        self.spring_force = self.spring.calcSpringForce(self.length)

        #print("spr force in calcSP", self.spring_force)

        self.damper_force = self.damper.calcDamperForce(self.vel)
        #print("damp force in calcSP", self.damper_force)

        # now find resultant of all forcces                 
        self.total_force = self.applied_force + self.gravity_force + self.spring_force + self.damper_force
        self.force_on_road = self.spring_force + self.damper_force
        #print("grav force in calcSP", self.gravity_force)
        #print("app force in calcSP", self.applied_force)
        
        # now can find the acceleration
        self.accel = self.total_force/self.mass
        #print("accel", self.accel)

        # now velocity
        self.vel = self.vel + (self.accel * time_step)
        #print("vel", self.vel)
        
        # now new length
        self.length = self.length + (self.vel * time_step)

        # now update elapsed time
        elapsed_time = time_step + elapsed_time
        #print("elapsed_time inside calcSuspensionPosition", elapsed_time)

        #return dict of various values                 
        return{'total_force': self.total_force, 'length' : self.length,
               'time' : elapsed_time, 'force_on_road': self.force_on_road}


######## run the program (should this be in a class of its own?)####

### PARAMETERS###
    
# model will run until max_time sec
max_time = 3

#elapsed_time starts at zero
elapsed_time = 0

time_step = 0.001 #sec
                         
g = -9.81 #gravity accel m/s/s note NEGATIVE because DOWN

###### note these parameters are for a generic setup
###### feel free to use these in the strut_1 and strut_2 objects below
###### or enter individual argiments for each object as you wish
mass = 300 #kg

vel = 0

## this is a fudge for constant applied force, which suddenly appears after t=0
## need to implement a proper time-dependant function
## see also Suspension __init__ where initial applied force is set to zero for
## calcSpringEqumLength method

initial_applied_force = -1000 # Newtons note NEGATIVE because DOWN

spring_const = 30000 # N/m

free_length = 1 # m

damper_const = 2000 # N/m/s

### create some objects to test things with ###

        ##Suspension(g, mass, vel, initial_applied_force, spring_const, free_length, damper_const)
strut_1 = Suspension(g, mass, vel, initial_applied_force, spring_const, free_length, damper_const)
strut_2 = Suspension(g, mass, vel, initial_applied_force, spring_const, free_length, 4000) 

### output params in list (time step increments)
#in future make these part of the Suspension class?
#would save need for repetitive typing?
lst_total_force_1 = []
lst_force_on_road_1 = []
lst_length_1 = []
lst_time_1 = []

lst_total_force_2 = []
lst_force_on_road_2 = []
lst_length_2 = []
lst_time_2 = []

#loop that runs the model, calling calcSuspensionPosition for each time step
while (elapsed_time < max_time):

    #print("elapsed_time", elapsed_time)

    dct_output_1 = strut_1.calcSuspensionPosition(time_step, elapsed_time)

    dct_output_2 = strut_2.calcSuspensionPosition(time_step, elapsed_time)
    
    #print("dct_output", dct_output)

    # append relevant arrays using output from the dct
    lst_total_force_1.append(dct_output_1['total_force'])
    lst_force_on_road_1.append(dct_output_1['force_on_road'])

    lst_length_1.append(dct_output_1['length'])

    lst_time_1.append(dct_output_1['time'])

    # append relevant arrays using output from the dct
    lst_total_force_2.append(dct_output_2['total_force'])
    lst_force_on_road_2.append(dct_output_2['force_on_road'])

    lst_length_2.append(dct_output_2['length'])

    lst_time_2.append(dct_output_2['time'])

    # update elapsed_time in this loop

    elapsed_time = dct_output_1['time']


plt.figure(1)

plt.subplot(211)
plt.plot(lst_time_1, lst_length_1, "r")
plt.plot(lst_time_2, lst_length_2, "b")
plt.xlabel("time/s")
plt.ylabel("Length /m")
plt.title("Suspension Length Plot")


plt.subplot(212)
plt.plot(lst_time_1, lst_force_on_road_1, "r")
plt.plot(lst_time_2, lst_force_on_road_2, "b")
plt.xlabel("time/s")
plt.ylabel("Force /N")
plt.title("Suspension Force Plot")

plt.show()
