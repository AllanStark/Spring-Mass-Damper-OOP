# JLW 17 Feb 15 attempt at OOP design for Spring-Mass-Damper model
# Edit Mar 15 -
# Edit 5 May 15 ~ refactored applied force code



import time

from smd_suspension import *
import smd_gui 

###~~~~~~APPLIED FORCE~~~~~~#####

#this array is the applied force to use at each time step
# needs to have as many indices as there are time steps
## see also Suspension __init__ where initial applied_force is set to zero for
## calcSpringEqumLength method (at t=0, spring is at equm length commensurate with the mass)

def setup_applied_force_arr (start1, ramp1, end1, start2, ramp2, end2): 
    """ force pattern is /^^^^^\ takes all ints, start and end are times in INDICES
    ramp is slope (Newtons/index), plateau """

    # TODO do I need to define globals for max_time etc here? also check ramps dovetail with plateau    
    applied_force = [0]*int(max_time/time_step) # Newtons note NEGATIVE is DOWN

    #~~~~~~~~~#set up applied force as func of time, ramp function, level, ramp back down
    for i in range (start1,end1,1): # (0, 400) RAMPING UP

        applied_force[i] = (-ramp1)*i

    plateau_force = applied_force[end1-1]

    for i in range(end1,start2,1): # PLATEAU at final value of ramp up 

        applied_force[i] = plateau_force

    for i in range (start2,end2,1): #(1500,2000) RAMPING DOWN

        applied_force[i] = plateau_force -(ramp2*(i-start2))
        
    #~~~~~~~~~#finished setting up applied_force list
    
    print("len of applied force array ", len(applied_force) )

    # placeholder* for second strut taking opposite force to first i.e. as load is transferred
    opposite_applied_force = [-x for x in applied_force]

    return (applied_force, opposite_applied_force)




########   RUN THE PROGRAM   #################
    
######## run the program (should this be in a class of its own?)####

###        PARAMETERS       #TODO: put in a config file as global across all modules? ###
    
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
damper_const_2 = 2000

damp_ratio_1 = damper_const_1/(2*(spring_const*mass)**0.5)
damp_ratio_2 = damper_const_2/(2*(spring_const*mass)**0.5)

print("damp_ratio_1", damp_ratio_1)
print("damp_ratio_2", damp_ratio_2)
                     




###~~~~~~~~~~~~~~TEST THE MODEL WITH SOME SUSPENSION STRUTS~~~~~~~~~~~~~~~~###

###create applied force arrays

forces = setup_applied_force_arr(0,5,400,1500,-4,2000)


applied_force = forces[0]
opposite_applied_force = forces[1]

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


#     PHYSICS MODEL LOOP       # put this as Suspension.physics_loop???

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

# run the GUI function

smd_gui.myplot(lst_time_1, lst_length_1, lst_time_2, lst_length_2, lst_force_on_road_1, \
       lst_force_on_road_2, applied_force, opposite_applied_force)

# run the anmation

my_SuspDisplay = smd_gui.SuspDisplay(lst_length_1, lst_length_2, max_time, elapsed_time, time_step)

    


