# JLW 17 Feb 15 attempt at OOP design for Spring-Mass-Damper model
# Edit Mar 15 - 

from matplotlib import pyplot as plt

import time

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
                    # flt, flt, flt, array[floats], flt, flt, flt
    def __init__(self, g, mass, vel, applied_force, spring_const, free_length, damper_const):

        self.mass = mass

        # Suspension object inits its own Spring and Damper objects                 
        self.spring = Spring(spring_const, free_length) ### should object name be capital "Spring"
        self.damper = Damper(damper_const)
        self.vel = vel
        self.applied_force = applied_force
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
        # note lookup of specific time's index in applied_force list
        #print("calcSuspensionPosition using applied_force index ", int(elapsed_time/time_step) )

        self.total_force = self.applied_force[int(elapsed_time/time_step)] + self.gravity_force + self.spring_force + self.damper_force
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




########   RUN THE PROGRAM   #################
    
######## run the program (should this be in a class of its own?)####

###        PARAMETERS        ###
    
# model will run until max_time sec
max_time = 5 #sec

#elapsed_time starts at zero
elapsed_time = 0 #sec

time_step = 0.001 #sec

#num_of_steps = int(max_time/time_step)
                         
g = -9.81 #gravity accel m/s/s note NEGATIVE because DOWN

###### note these parameters are for a generic setup
###### feel free to use these in the strut_1 and strut_2 objects below
###### or enter individual argiments for each object as you wish
mass = 300 #kg

vel = 0

spring_const = 30000 # N/m

free_length = 1 # m

damper_const_1 = 1000 # N/m/s
damper_const_2 = 6000

damp_ratio_1 = damper_const_1/(2*(spring_const*mass)**0.5)
damp_ratio_2 = damper_const_2/(2*(spring_const*mass)**0.5)

print("damp_ratio_1", damp_ratio_1)
print("damp_ratio_2", damp_ratio_2)
                     

###           APPLIED FORCE         #####

#this array is the applied force to use at each time step
# needs to have as many indices as there are time steps
## see also Suspension __init__ where initial applied_force is set to zero for
## calcSpringEqumLength method (at t=0, spring is at equm length commensurate with the mass)

applied_force = [0]*int(max_time/time_step) # Newtons note NEGATIVE is DOWN

#~~~~~~~~~#set up applied force as func of time, ramp function, level, ramp back down
for i in range (0,500,1):

    applied_force[i] = -4*i

for i in range(500,1500,1):

    applied_force[i] = -2000

for i in range (1500,2000,1):

    applied_force[i] = (-2000 +4*((i)-1500) )
#~~~~~~~~~#finished setting up applied_force list
    
print("len of applied force array ", len(applied_force) )

# placeholder* for second strut taking opposite force to first i.e. as load is transferred
opposite_applied_force = [-x for x in applied_force]


###         TEST THE MODEL WITH SOME SUSPENSION STRUTS  ###

### create some objects to test things with ###

        ##Suspension(g, mass, vel, applied_force, spring_const, free_length, damper_const)
strut_1 = Suspension(g, mass, vel, applied_force, spring_const, free_length, damper_const_1)
strut_2 = Suspension(g, mass, vel, opposite_applied_force, spring_const, free_length, damper_const_2) 

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


#     PHYSICS MODEL LOOP       #

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

print("physics loop finished")

    


#### OUTPUT SUSPENSION LENGTH AND FORCE PLOTS - matplotlib


def myplot():

    plt.figure(1)

    plt.subplot(311)
    plt.plot(lst_time_1, lst_length_1, "r")
    plt.plot(lst_time_2, lst_length_2, "b")
    plt.xlabel("time/s")
    plt.ylabel("Length /m")
    plt.title("Suspension Length Plot")


    plt.subplot(312)
    plt.plot(lst_time_1, lst_force_on_road_1, "r")
    plt.plot(lst_time_2, lst_force_on_road_2, "b")
    plt.xlabel("time/s")
    plt.ylabel("Force /N")
    plt.title("Suspension Force Plot")

    plt.subplot(313)
    plt.plot(lst_time_1, applied_force, "r")
    plt.plot(lst_time_2, opposite_applied_force, "b")
    plt.xlabel("time/s")
    plt.ylabel("Force /N")
    plt.title("Applied Force Plot (load transfer etc)")

    plt.show()

myplot()

    
    


###    PROTOTYPE TKINTER ANIMATION    ####

### To do: arrange this properly, OOP

from tkinter import *
#### put this in an init function
root = Tk()
my_frame = Frame (root, width = 600, height = 600)
my_frame.grid (row = 0, column = 0)
my_canvas = Canvas(my_frame, width = 600, height = 600, background = "white" )




susp_length_1 = 200*lst_length_1[0]
susp_length_2 = 200*lst_length_2[0]

susp_line_1 = my_canvas.create_line( 100, 500, 100, (500-susp_length_1), fill = "red", width = 20 ) 
susp_line_2 = my_canvas.create_line( 500, 500, 500, (500-susp_length_2), fill = "blue", width = 20 )

body_line = my_canvas.create_line( 100, (500-susp_length_1), 500, (500-susp_length_2), fill = "black", width = 10)

my_canvas.grid(row = 0, column =0)

def animate(): #temporary placeholder* to display 2 struts at once, sort this out OOP etc

    #careful, can't have 1 ms redraw freq, of monitor is not 1000 Hz!!!
    anim_frame_freq = 20 #ms between frame updates
    
    for index in range(0, int(max_time/time_step),1):

        if (index%anim_frame_freq == 0):
            
            susp_length_1 = 200*(lst_length_1[index])
            susp_length_2 = 200*(lst_length_2[index])

            #delay between animating (i.e. framerate)
            my_canvas.after(anim_frame_freq) # 
            my_canvas.coords(susp_line_1, 100, 500, 100, 500-susp_length_1 )
            my_canvas.coords(susp_line_2, 500, 500, 500, 500-susp_length_2 )
            my_canvas.coords(body_line, 100, (500-susp_length_1), 500, (500-susp_length_2))
            my_canvas.update()

while True:
    animate_keypress = input("enter n to quit or any other key to animate")
    if(animate_keypress == "n"):
        break
    else:
        animate()


root.mainloop()
