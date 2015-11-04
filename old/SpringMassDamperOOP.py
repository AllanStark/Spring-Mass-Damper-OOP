# JLW 17 Feb 15 attempt at OOP design for Spring-Mass-Damper model
# Edit Mar 15 -
# Edit 5 May 15 ~ refactored applied force code
# Edit 3 June 15 - refactored into more modules, GUI integrated
# Edit 18 June 15 - physics loop moved into own module, fixed cfg globals updating.

import time

import tkinter as Tk

from smd_suspension import *
import smd_gui
import smd_cfg
from applied_force import setup_applied_force_arr
from smd_physicsloop import physics_loop


#TODO: fully implement input gui
import smd_input_gui


########   RUN THE PROGRAM   #################
    


#~~~~~~~~~~ SET "CROSS-MODULE GLOBAL" CONFIG PARAMETERS ~~~~~~~~~~~
    
# model will run until max_time sec

smd_cfg.max_time = 5 #sec

smd_cfg.elapsed_time = 0 #sec

smd_cfg.time_step = 0.001 #sec
                         
smd_cfg.g = -9.81 #gravity accel m/s/s note NEGATIVE because DOWN



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
#TODO: in future make these part of the Suspension class?  The can just pass strut objects (from Suspension)
#into phys model?  then phys model can just operate on strut_1.data.
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
lst_time_2 = [] # TODO: eliminate uneccessary duplication?.. only need one "time" reference

#strut_2_data = {}
strut_2_data = {'lst_total_force_2':lst_total_force_2, 'lst_force_on_road_2':lst_force_on_road_2,
                'lst_length_2':lst_length_2, 'lst_time_2': lst_time_2}


#~~~~~~~~~~~~ RUN THE PHYSICS LOOP FUNCTION

strut_1_data, strut_2_data = physics_loop(strut_1,strut_1_data, strut_2, strut_2_data)



#~~~~~~~~~~~~ INITIALISE ALL GUI COMPONENTS

#open a TKinter root window
root = Tk.Tk()

#call the plots
my_ParamsDisplay = smd_input_gui.ParamsDisplay(root) #TODO: fully implement

my_ParamsDisplay.my_frame.grid( row = 0, column = 1)

my_SuspPlot = smd_gui.SuspPlot(strut_1_data, strut_2_data, applied_force, opposite_applied_force, root)

my_SuspPlot.my_frame.grid(row = 0, column = 0, rowspan = 2)

# create the suspdisplay (cartoon) object, call its animate func

my_SuspDisplay = smd_gui.SuspDisplay(strut_1_data["lst_length_1"], strut_2_data["lst_length_2"], root)

my_SuspDisplay.my_frame.grid (row = 1, column = 1)

my_SuspDisplay.animate()

root.mainloop()


