# smd_gui

""" Suspension length and force plots - matplotlib
    Cartoon - Tkinter Canvas"""

import tkinter as Tk

from numpy import arange, sin, pi

# matplotlib including mpl into tkinter bits
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler

from matplotlib.figure import Figure


# "internal" import of config (global vars)
import smd_cfg


class SuspPlot():
    """ matplotlib plots"""

    #TODO: Better to refactor this to accept strut_n_data as args, where can have any
    # number of struts.  need to get strut_n_data into part of
    # strut object (instance of Suspension)
    
    def __init__(self, strut_1_data, strut_2_data, applied_force, opposite_applied_force, root):

        self.lst_time_1 = strut_1_data["lst_time_1"]
        print("len lst_time_1", len(self.lst_time_1))
              
        self.lst_length_1 = strut_1_data["lst_length_1"]
        self.lst_time_2 = strut_2_data["lst_time_2"]
        self.lst_length_2 = strut_2_data["lst_length_2"]
        self.lst_force_on_road_1 = strut_1_data["lst_force_on_road_1"]
        self.lst_force_on_road_2 = strut_2_data["lst_force_on_road_2"]
        self.applied_force = applied_force
        print("len applied_force", len(self.applied_force))
        self.opposite_applied_force = opposite_applied_force

        self.root = root

        self.my_frame = Tk.Frame (self.root, width = 600, height = 400, background = "white") ##TODO - check this is displaying

        self.f = Figure(figsize=(5,4), dpi=100)
        self.a = self.f.add_subplot(311)
        self.b = self.f.add_subplot(312)
        self.c = self.f.add_subplot(313)

        self.a.plot(self.lst_time_1, self.lst_length_1, "r")
        self.a.plot(self.lst_time_2, self.lst_length_2, "b")
        self.a.set_xlabel("time/s") 
        self.a.set_ylabel("Length /m")
        self.a.set_title("Suspension Length Plot")


        self.b.plot(self.lst_time_1, self.lst_force_on_road_1, "r")
        self.b.plot(self.lst_time_2, self.lst_force_on_road_2, "b")
        self.b.set_xlabel("time/s")
        self.b.set_ylabel("Force /N")
        self.b.set_title("Suspension Force Plot")


        self.c.plot(self.lst_time_1, self.applied_force, "r")
        self.c.plot(self.lst_time_2, self.opposite_applied_force, "b")
        self.c.set_xlabel("time/s")
        self.c.set_ylabel("Force /N")
        self.c.set_title("Applied Force Plot (load transfer etc)")


        # a tk.Drawing Area
        self.canvas = FigureCanvasTkAgg(self.f, master=self.my_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)  ###TODO - Tk has no attr "TOP"... maybe try packing to Frame

        self.toolbar = NavigationToolbar2TkAgg( self.canvas, self.my_frame )
        self.toolbar.update()
        #self.canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1) 

        ##TODO:  may need to put all this in a frame, frame has self. root as master, then canvas has self. frame as master
        ## then in main prog outside of this class, can .pack or .grid the frame as a whole to position everything in one go


class SuspDisplay():
    """TKinter cartoon of 2 suspension struts"""

    #TODO: this would be more difficult to refactor, more than 2 struts would
    #look better with 3D model..... also this only needs the lst_length_n args
    # could still import strut_n_data and pick the length values from the dict?
    # or just keep like this as it's aonly 2 args???                                     

    def __init__(self,lst_length_1, lst_length_2, root):

            #TODO : DONE-CHECK might be better to make things like max_time global between modules
            # can't just "global" this, need a config.py module
            # http://effbot.org/pyfaq/how-do-i-share-global-variables-across-modules.htm
        
        self.lst_length_1 = lst_length_1
        self.lst_length_2 = lst_length_2
        #global max_time  #TODO: unnecessary to create "self" version of globals.
        #self.max_time = smd_config.max_time

        #global time_step
        #self.time_step = smd_config.time_step


        # TODO sort these out, class vars, inst vars, what?!?!?
        # at moment have just "selfed" everything - inst vars
        self.root = root
        self.my_frame = Tk.Frame (self.root, width = 600, height = 500)
        
        self.my_canvas = Tk.Canvas(self.my_frame, width = 600, height = 500, background = "white" )

        self.susp_length_1 = 200*self.lst_length_1[0]
        self.susp_length_2 = 200*self.lst_length_2[0]

        self.susp_line_1 = self.my_canvas.create_line( 100, 500, 100, (500-self.susp_length_1), fill = "red", width = 20 ) 
        self.susp_line_2 = self.my_canvas.create_line( 500, 500, 500, (500-self.susp_length_2), fill = "blue", width = 20 )

        self.body_line = self.my_canvas.create_line( 100, (500-self.susp_length_1), 500, (500-self.susp_length_2), fill = "black", width = 10)

        self.my_canvas.grid(row = 0, column =0)

        self.anim_button = Tk.Button(master = self.my_frame, text = "Animate", height = 6, width = 12, \
                                     activebackground = "red", repeatdelay = 500, repeatinterval = 25, \
                                     command = self.animate)
        self.anim_button.grid(row = 1, column = 0)

        

    def animate(self): 

        #TODO, as above, check if some things best as class vars.
        
        #careful, can't have 1 ms redraw freq, of monitor is not 1000 Hz!!!
        anim_frame_freq = 20 #ms between frame updates
    
        for index in range(0, int(smd_cfg.max_time/smd_cfg.time_step),1):

            if (index%anim_frame_freq == 0):
            
                self.susp_length_1 = 200*(self.lst_length_1[index])
                self.susp_length_2 = 200*(self.lst_length_2[index])

                #delay between animating (i.e. framerate)

                self.my_canvas.after(anim_frame_freq) #
                
                self.my_canvas.coords(self.susp_line_1, 100, 500, 100, 500-self.susp_length_1 )
                self.my_canvas.coords(self.susp_line_2, 500, 500, 500, 500-self.susp_length_2 )
                self.my_canvas.coords(self.body_line, 100, (500-self.susp_length_1), 500, (500-self.susp_length_2))
                self.my_canvas.update()

        # OBSOLETE cmd line interface anim, before gui button coded
        #while True:
         #   animate_keypress = input("enter n to quit or any other key to animate")
          #  if(animate_keypress == "n"):
           #     break
            #else:
             #   SuspDisplay.animate(self)


        
