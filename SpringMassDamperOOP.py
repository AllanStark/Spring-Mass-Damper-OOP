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
    
# generics for phys loop etc

smd_cfg.max_time = 5 #sec

smd_cfg.elapsed_time = 0 #sec

smd_cfg.time_step = 0.001 #sec
                         
smd_cfg.g = -9.81 #gravity accel m/s/s note NEGATIVE because DOWN


# default strut values (for when prog first opens- all struts have these values)
smd_cfg.df_mass = 300 # kg mass on strut
smd_cfg.df_fl = 1     # m length
smd_cfg.df_sr = 40000 # N/m spring rate
smd_cfg.df_dc = 1000 # N/m/s damper constant
smd_cfg.df_vel = 0 # m/s initial strut velocity
smd_cfg.wheelbase = 1.5 # m wheelbase



###~~~~~~~~~~~~~~TEST THE MODEL WITH SOME SUSPENSION STRUTS~~~~~~~~~~~~~~~~###

### Create applied force arrays

forces = setup_applied_force_arr(0,10,200,500,-4,1000)


applied_force = forces[0]
opposite_applied_force = forces[1]


#~~~~~~~~~~ Create HalfCar( 2 struts (Suspension objects) to test things with ~~~~~~~~~~
my_halfcar = HalfCar(smd_cfg.wheelbase, "r", "b", applied_force, opposite_applied_force)
#TODO: get default values from inputGUI?
        ##Suspension( str name, str colour for mpl representations,  arr applied_force):





#~~~~~~~~~~~~ INITIALISE ALL GUI COMPONENTS
# TODO: need to change args to default plots here!!!!
# should this mainloop be in a separate file or class?
# also how do i run mainloop but keep doing other things - threading READ UP?

#open a TKinter root window
root = Tk.Tk()

#call the plots #TODO: pass in my_halfcar etc... get all_struts that way
# Pass in my_halfcar.all_struts, or whole of my_halfcar? depends on scope of fn.
my_ParamsDisplay = smd_input_gui.GUIParamsDisplay(root, my_halfcar.all_struts) #TODO: check

my_ParamsDisplay.my_frame.grid( row = 0, column = 1)

#TODO: update now using HalofCar class??????
my_SuspPlot = smd_gui.SuspPlot(my_halfcar, root)

my_SuspPlot.my_frame.grid(row = 0, column = 0, rowspan = 2)

# create the suspdisplay (cartoon) object, call its animate func

#TODO: update now the data is prat of the strut obj.  Also what should this plot as df??????
my_SuspDisplay = smd_gui.SuspDisplay(my_halfcar, root) #Todo: ADJUST ARGs IN SMD_GUI

my_SuspDisplay.my_frame.grid (row = 1, column = 1)

#my_SuspDisplay.animate()

root.mainloop()


