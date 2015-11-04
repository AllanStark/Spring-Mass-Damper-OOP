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

    #TODO: change the init to blank plot
        #  then def a new fn which plots telem data from the relevant Suspension.record

                      #(arr, arr, arr, tk frame)
    def __init__(self, car, root):

                     
        self.all_struts = car.all_struts
        self.applied_force = car.applied_force
        self.opposite_applied_force = car.opposite_applied_force

        #TODO: check, is this iffy, cleaner way possible?
        self.lst_of_applied_forces = [self.applied_force, self.opposite_applied_force]
        self.root = root

        self.my_frame = Tk.Frame (self.root, width = 600, height = 400, background = "white") ##TODO - check this is displaying

        self.f = Figure(figsize=(5,4), dpi=100)
        self.a = self.f.add_subplot(311) #length vs time
        self.b = self.f.add_subplot(312) #force on road vs time
        self.c = self.f.add_subplot(313) #app force vs time

        self.lst_of_colours = ["r", "b", "g", "y"]


        self.a.set_xlabel("time/s") 
        self.a.set_ylabel("Length /m")
        self.a.set_title("Suspension Length Plot")

            
        self.b.set_xlabel("time/s")
        self.b.set_ylabel("Force /N")
        self.b.set_title("Suspension Force Plot")

        
        self.c.set_xlabel("time/s")
        self.c.set_ylabel("Force /N")
        self.c.set_title("Applied Force Plot (load transfer etc)")


        # a tk.Drawing Area to place the subplots in
        self.canvas = FigureCanvasTkAgg(self.f, master=self.my_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)  ###TODO - Tk has no attr "TOP"... maybe try packing to Frame

        self.toolbar = NavigationToolbar2TkAgg( self.canvas, self.my_frame )
        self.toolbar.update()
        #self.canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1) 

        
    def plot_telem(self): # TODO: check that "self.all_struts" points to car,
                          # i.e if you change car, does it update record here?

        # Populate sublot a (length vs time) with telemetry data
        self.i = 0
        for strut in self.all_struts:
            self.a.plot(strut.record["time"], strut.record["length"], self.lst_of_colours[self.i])
            self.i = self.i+1
        # Populate sublot b (F on road vs time)
        self.i = 0
        for strut in self.all_struts:
            self.b.plot(strut.record["time"], strut.record["force_on_road"], self.lst_of_colours[self.i])
            self.i = self.i+1
        # Populate subplot c (app F vs time)
        self.i = 0
        for strut in self.all_struts:
            self.c.plot(strut.record["time"], self.lst_of_applied_forces[self.i], self.lst_of_colours[self.i])
            self.i = self.i+1

        

class SuspDisplay():
    """TKinter cartoon of 2 suspension struts"""

    #TODO: again, pass in array of all struts, init should draw start positins only                                     

    def __init__(self, car, root):
                #(self, Chassis, tk Frame)

        self.all_struts = car.all_struts
        
        self.root = root
        self.my_frame = Tk.Frame (self.root, width = 600, height = 500)
        
        self.my_canvas = Tk.Canvas(self.my_frame, width = 600, height = 500, background = "white" )

        self.front_padding = 100 # number of pix padding from edge of canvas to front of car
        self.ground_plane = 500 # number of pixels for bottom of strut leg line(remember origin is TOP so LARGER means LOWER

        self.body_length = 500 # in pix##TODO: follow this up, deleting numbers in expressions, replace with this var
        self.scale = 200 # scale strut length by this number of pix

        self.lst_of_colours = ["red", "blue", "green", "yellow"]

        self.i = 0
        for strut in self.all_struts:
            colour = self.lst_of_colours[self.i]
            strut.line = StrutLine(strut, colour, self)
            self.i = self.i + 1

        # TODO: tidy up body_line, exactly what coords does it draw from????
        # best to take from the relevant StrutLine objects - need a get fn in StrutLine?
        self.body_line = self.my_canvas.create_line( 100, (500-self.susp_length_1), 500, (500-self.susp_length_2), fill = "black", width = 10)

        self.my_canvas.grid(row = 0, column =0)

        self.anim_button = Tk.Button(master = self.my_frame, text = "Animate", height = 6, width = 12, \
                                     activebackground = "red", repeatdelay = 500, repeatinterval = 25, \
                                     command = self.animate)
        self.anim_button.grid(row = 1, column = 0)

        
# TODO: again, import strut1.record etc and plot data from here.
    def animate(self): 

        #TODO, as above, check if some things best as class vars.
        
        #careful, can't have 1 ms redraw freq, freq of monitor is not 1000 Hz!!!
        anim_frame_freq = 20 #ms between frame updates
    
        for index in range(0, int(smd_cfg.max_time/smd_cfg.time_step),1):

            if (index%anim_frame_freq == 0):
                #todo -NEW STUFF - need setter fn in StrutLine
                for strut in self.all_struts:
                    strut.line.set(#FOO~)
                self.susp_length_1 = 200*(self.lst_length_1[index])
                self.susp_length_2 = 200*(self.lst_length_2[index])

                #delay between animating (i.e. framerate)

                self.my_canvas.after(anim_frame_freq) #
                
                self.my_canvas.coords(self.susp_line_1, 100, 500, 100, 500-self.susp_length_1 )
                self.my_canvas.coords(self.susp_line_2, 500, 500, 500, 500-self.susp_length_2 )
                self.my_canvas.coords(self.body_line, 100, (500-self.susp_length_1), 500, (500-self.susp_length_2))
                self.my_canvas.update()


## TODO - lots here!!!!!
class StrutLine(): # the line that represents a strut in the animation TODO: fully implement

    def __init__ (self, strut, colour, master):

        self.strut = strut
        self.master = master
        self.colour = colour # "red", "blue", "green", "yellow"
                             # note different format from MPL's "r", "b", etc

        # TODO: only want x "plus body length if rear strut""
        #DEBUG - when prog first started, record.["length"] = []
        print("SMD_GUI strut len =", self.strut.record["length"])

                # coords are x1, y1, x2, y2.  Origin is TOP LEFT of Canvas
        self.line = self.master.my_canvas.create_line( self.master.front_padding, self.master.ground_plane,
                                                       self.master.front_padding, (self.master.ground_plane - (self.master.scale*(self.strut.record["length"][0]))),
                                                       fill = self.colour, width = 20 )


        ##### TODO: need getter and setter etc
    def get_strut_top_coords(self): # used to get strut top coords to pass to BodyLine, so body stays attached to top of strut

        coords = master.coords(self)
        print ("getting coords from strut line ", coords)
        strut_top = [coords(2),coords(3)] #x,y 

        return strut_top
        
    def set_coords(self): # used to update coords from telemetry in order to animate strut
        
        #TODO need to retrieve coords from telemetry
        x0 = coords[0]
        y0 = coords[1]
        x1 = coords[2]
        y1 = coords[3]

        
        self.master.coords(self, x0, y0, x1, y1) #Canvas.coords( line, x0, y0 etc....)
        

class BodyLine():

    def __init__(self, colour, master):

        self.master = master
        self.colour = colour

        self.master.all_struts###TODO, get front and rear str
        self.strut_top_lst = [] #x0, y0, x1, y1

        for strut in self.master.all_struts:
                strut_top = strut.line.get_strut_top_coords()

                for coord in strut_top:
                    self.strut.top.lst.append(coord)
        
                
        self.line = self.master.my_canvas.create_line( self.strut_top_lst[0], self.strut_top_lst[1],
                                                       self.strut_top_lst[2], self.strut_top_lst[3],
                                                       fill = self.colour, width = 20 )

            #####TODO: need getter and setter etc
    def get_coords(self):
        # TODO - is this necessary in current scope of code?

    def set_coords(self):
        self.strut_top_lst = [] #new empty array each time
        for strut in self.master.all_struts:
            strut_top = strut.line.get_strut_top_coords()

            for coord in strut_top:
                self.strut_top_lst.append(coord)
        #TODO: now set the BodyLine coords, remember you do Canvas.coords(LineID, x0,y0 etc)
        self.master.coords(self, self.strut_top_lst[0], self.strut_top_lst[1], self.strut_top_lst[2], self.strut_top_lst[3])
    
