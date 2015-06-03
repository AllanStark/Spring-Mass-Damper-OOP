# JLW 17 Feb 15 attempt at OOP design for Spring-Mass-Damper model
# Edit Mar 15 -
# Edit 5 May 15 ~ refactored applied force code
# Edit 3 June 15 - refactored into more modules, GUI integrated


import time

import tkinter as Tk

from smd_suspension import *
import smd_gui
import smd_config
from applied_force import setup_applied_force_arr





########   RUN THE PROGRAM   #################
    


#~~~~~~~~~~ SET "CROSS-MODULE GLOBAL" CONFIG PARAMETERS ~~~~~~~~~~~
    
# model will run until max_time sec

smd_config.max_time = 5 #sec

#TODO: elapsed_time starts at zero... note this updates to smd_config OK!!! But the physics loop didn't
#problem updating the smd_config module from within a loop?

smd_config.elapsed_time = 0 #sec

smd_config.time_step = 0.001 #sec
                         
smd_config.g = -9.81 #gravity accel m/s/s note NEGATIVE because DOWN



#~~~~~~~~~ Parameters for 2 struts ~~~~~~~~~~

# note these parameters are for a generic setup
# feel free to use these in the strut_1 and strut_2 objects below
# or enter individual argiments for each object as you wish

mass = 300 #kg

vel = 0 #m/s

spring_const = 30000 # N/m

free_length = 1 # m

damper_const_1 = 1500 # N/m/s
damper_const_2 = 4000

damp_ratio_1 = damper_const_1/(2*(spring_const*mass)**0.5)
damp_ratio_2 = damper_const_2/(2*(spring_const*mass)**0.5)

print("damp_ratio_1", damp_ratio_1)
print("damp_ratio_2", damp_ratio_2)
                     




###~~~~~~~~~~~~~~TEST THE MODEL WITH SOME SUSPENSION STRUTS~~~~~~~~~~~~~~~~###

### Create applied force arrays

forces = setup_applied_force_arr(0,10,200,500,-4,1000)


applied_force = forces[0]
opposite_applied_force = forces[1]

#~~~~~~~~~~ Create 2 struts (Suspension objects) to test things with ~~~~~~~~~~


        ##Suspension( mass, vel, applied_force, spring_const, free_length, damper_const)
strut_1 = Suspension( mass, vel, applied_force, spring_const, free_length, damper_const_1)
strut_2 = Suspension( mass, vel, opposite_applied_force, spring_const, free_length, damper_const_2) 

### output params in list (time step increments, each index is a new time step)
#in future make these part of the Suspension class?
#would save need for repetitive typing?
lst_total_force_1 = []
lst_force_on_road_1 = []
lst_length_1 = []
lst_time_1 = []

#strut_1_data = {} #summarises all "lst_foo" above, for this strut 

strut_1_data = {'lst_total_force_1':lst_total_force_1, 'lst_force_on_road_1':lst_force_on_road_1,
                'lst_length_1':lst_length_1, 'lst_time_1': lst_time_1}

lst_total_force_2 = []
lst_force_on_road_2 = []
lst_length_2 = []
lst_time_2 = [] # uneccessary dup;ication... only need one "time" reference

#strut_2_data = {}
strut_2_data = {'lst_total_force_2':lst_total_force_2, 'lst_force_on_road_2':lst_force_on_road_2,
                'lst_length_2':lst_length_2, 'lst_time_2': lst_time_2}


#~~~~~~~~~ PHYSICS MODEL LOOP FUNCTION ~~~~~~~~~~~~#

#loop that runs the model, calling calcSuspensionPosition for each time step
# TODO: couldn't use smd_config.elapsed_time, it wouldn't update? Almost like it wouldn't
# publish back to the config file while the loop was still running, therefore no update
# between iterations.
#     this now uses config.globals, also refactor how it summons struts, pass all struts as a tuple?
#     Put physics model in own module?
#      Should make strut_n_data part of Suspenion class?  Then can just pass the strut_n objects
#      and access the strut_n_data that way.

def physics_loop(strut_1, strut_1_data, strut_2, strut_2_data):

    elapsed_time = 0
    
    while (elapsed_time < smd_config.max_time):

        #print("elapsed_time", elapsed_time)

        dct_output_1 = strut_1.calcSuspensionPosition(elapsed_time)
        #print("dct_output_1", dct_output_1)

        dct_output_2 = strut_2.calcSuspensionPosition(elapsed_time)

        #TODO: this is not updating when smd_config.elasped_time is used FIND OUT WHY?!?!?!?
        # Therefore I put in a local elapsed_time
        elapsed_time = elapsed_time + smd_config.time_step
        #print("Phys Loop elapsed_time", elapsed_time)
        
        #print("in Phys Loop, time_step =", smd_config.time_step, type (smd_config.time_step) )
    
        #print("dct_output", dct_output)

        # append relevant arrays using output from the dct
        strut_1_data["lst_total_force_1"].append(dct_output_1['total_force'])
        strut_1_data["lst_force_on_road_1"].append(dct_output_1['force_on_road'])

        strut_1_data["lst_length_1"].append(dct_output_1['length'])
        
        strut_1_data["lst_time_1"].append(dct_output_1['time'])

        # append relevant arrays using output from the dct
        strut_2_data["lst_total_force_2"].append(dct_output_2['total_force'])
        strut_2_data["lst_force_on_road_2"].append(dct_output_2['force_on_road'])

        strut_2_data["lst_length_2"].append(dct_output_2['length'])

        strut_2_data["lst_time_2"].append(dct_output_2['time'])

        # update elapsed_time in this loop
      
        smd_config.elapsed_time = dct_output_1['time']

    print("physics loop finished")

    return  strut_1_data, strut_2_data



#~~~~~~~~~~~~ RUN THE PHYSICS LOOP FUNCTION

strut_1_data, strut_2_data = physics_loop(strut_1,strut_1_data, strut_2, strut_2_data)



#~~~~~~~~~~~~ Run the GUI function

#open a TKinter root window
root = Tk.Tk()

#call the plots

my_SuspPlot = smd_gui.SuspPlot(strut_1_data, strut_2_data, applied_force, opposite_applied_force, root)

my_SuspPlot.my_frame.grid(row = 0, column = 0)

# create the suspdisplay (cartoon) object, call its animate func

my_SuspDisplay = smd_gui.SuspDisplay(strut_1_data["lst_length_1"], strut_2_data["lst_length_2"], root)

my_SuspDisplay.my_frame.grid (row = 0, column = 1)

my_SuspDisplay.animate()

root.mainloop()


