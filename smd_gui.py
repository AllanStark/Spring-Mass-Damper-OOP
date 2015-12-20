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

        self.car = car            
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
                          # INitial testing would appear not to.

        
        print("plotting telem")
        self.all_struts = self.car.all_struts # TODO this should update if car changes.

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

        print("finshed plotting telem") # TODO this prints but mpl doesn't always update...

    def clear_telem(self): # clears all plotted data
        self.a.clear()
        self.b.clear()
        self.c.clear()
        print ("cleared telem")
        

class SuspDisplay():
    """TKinter cartoon of 2 suspension struts"""                                     

    def __init__(self, car, root):
                #(self, Chassis, tk Frame)

        self.all_struts = car.all_struts
        
        self.root = root
        self.my_frame = Tk.Frame (self.root, width = 600, height = 500)
        
        self.my_canvas = Tk.Canvas(self.my_frame, width = 600, height = 500, background = "white" )

        self.front_padding = 100 # number of pix padding from edge of canvas to front of car
        self.ground_plane = 500 # number of pixels for ground (remember origin is TOP so LARGER means LOWER DOWN)

         # in pix##TODO: follow this up, deleting numbers in expressions, replace with this var from Chassis class
        self.scale = 200 # scale strut, body etc length by this number of pix
        self.body_length = car.wheelbase * self.scale
        
        self.lst_of_colours = ["red", "blue", "green", "yellow"]

        self.i = 0
        for strut in self.all_struts:
            colour = self.lst_of_colours[self.i]
            strut.line = StrutLine(strut, colour, self)
            self.i = self.i + 1

        # TODO: tidy up body_line,
        # best to take from the relevant StrutLine objects - need a get fn in StrutLine?

        for strut in self.all_struts:
            if (strut.is_rear == False):
                self.front_strut_top = strut.line.get_strut_top_coords() # (x,y)

            elif (strut.is_rear == True):
                self.rear_strut_top = strut.line.get_strut_top_coords() #(x,y)

            else:
                print("strut is_rear error")
                
        self.body_line = BodyLine("black", self)
            #self.front_strut_top[0], self.front_strut_top[1],
             #                                        self.rear_strut_top[0], self.front_strut_top[1],
              #                                       fill = "black", width = 10)

        self.my_canvas.grid(row = 0, column =0)

        self.anim_button = Tk.Button(master = self.my_frame, text = "Animate", height = 6, width = 12, \
                                     activebackground = "red", repeatdelay = 500, repeatinterval = 25, \
                                     command = self.animate)
        self.anim_button.grid(row = 1, column = 0)


    def animate(self): 
                
        #TODO, as above, check if some things best as class vars.
        
        # Can't have 1 ms redraw freq, freq of monitor is not 1000 Hz!!!
        anim_frame_freq = 20 #ms between frame updates

        
        # Case where phys model not yet run, a strut will only have 1 value in its records (the initial length, other param, etc)
        # this checks the first strut (index zero) for length of array, and does not animate if it is zero or 1
        if ( len(self.all_struts[0].record["length"]) <= 1):
            print ("phys model not yet run - nothing to animate")

        else: # case where model has run and there is telemetry to animate
            print ("animating")    
            for index in range(0, int(smd_cfg.max_time/smd_cfg.time_step),1):
                #print("Index in loop - all increments", index)

                if (index%anim_frame_freq == 0):
                    #print("Index in anim loop", index)
                    #TODO: check this works, set StrutLine objects' coords with new strut length
                    for strut in self.all_struts:
                        #print("Len of strut.record", len(strut.record["length"]))
                        #print(strut.record["length"])
                    
                        strut.line.set_strut_top_coords(strut.record["length"][index])

                    # Now set the BodyLine coords from the strut top coords
                    self.body_line.set_coords()


                    #delay between animating (i.e. framerate)

                    self.my_canvas.after(anim_frame_freq)
                    self.my_canvas.update()


## TODO - lots here!!!!!
class StrutLine(): # the line that represents a strut in the animation TODO: fully implement

    def __init__ (self, strut, colour, master):
                 #(self, Strut, string, SuspDisplay)
        self.strut = strut
        self.master = master
        self.colour = colour # "red", "blue", "green", "yellow"
                             # note different format from MPL's "r", "b", etc

        # Assign initial coordinates:  only want "x plus body length" if rear strut
        #DEBUG:when prog first started, record.["length"] = []
        print("SMD_GUI strut len =", self.strut.record["length"])

        if (self.strut.is_rear == False):  #Front strut case
                        # coords are x1, y1, x2, y2.  Origin is TOP LEFT of Canvas
            print("creating front strut line")
            self.line = self.master.my_canvas.create_line( self.master.front_padding,
                                                       self.master.ground_plane,

                                                       self.master.front_padding,
                                                       (self.master.ground_plane - (self.master.scale*(self.strut.record["length"][0]))),

                                                       fill = self.colour, width = 20 )
            print("front strut line initial coords", self.master.my_canvas.coords(self.line))

        elif self.strut.is_rear == True:  #Rear strut case
            print("creating rear strut line")
            self.line = self.master.my_canvas.create_line( (self.master.front_padding + self.master.body_length),
                                                       self.master.ground_plane,

                                                       (self.master.front_padding + self.master.body_length),
                                                       (self.master.ground_plane - (self.master.scale*(self.strut.record["length"][0]))),

                                                       fill = self.colour, width = 20 )
            print("rear strut line initial coords", self.master.my_canvas.coords(self.line))
        else:
            print("Strut is_rear error")

                
        ##### TODO: need getter and setter etc
    def get_strut_top_coords(self): # used to get strut top coords to pass to BodyLine, so body stays attached to top of strut

        coords = self.master.my_canvas.coords(self.line)
        #print ("getting coords from strut line ", coords) #TODOTODO -error - empty array on startup!!!!
        strut_top = [coords[2],coords[3]] #x,y 

        return strut_top
        
    def set_strut_top_coords(self, strut_length): # used to update coords from telemetry in order to animate strut
                            #(self, flt self.strut.record["length"][i])
        #TODO need to retrieve coords from telemetry ...   self.strut.record["length"][foo]
                
        #### coords, for reference, most don't change
        x0 = self.master.my_canvas.coords(self.line)[0] ####
        y0 = self.master.my_canvas.coords(self.line)[1] ####
        x1 = self.master.my_canvas.coords(self.line)[2] ####
                
        y1 = self.master.ground_plane - (self.master.scale*strut_length)        
        
        self.master.my_canvas.coords(self.line, x0, y0, x1, y1) #Canvas.coords( line, x0, y0 etc....)
        

class BodyLine():

    def __init__(self, colour, master):

        self.master = master
        self.colour = colour

        self.master.all_struts###TODO, get front and rear str
        self.strut_top_lst = [] #x0, y0, x1, y1

        for strut in self.master.all_struts:
                strut_top = strut.line.get_strut_top_coords()

                for coord in strut_top:
                    self.strut_top_lst.append(coord)
        
                
        self.line = self.master.my_canvas.create_line( self.strut_top_lst[0], self.strut_top_lst[1],
                                                       self.strut_top_lst[2], self.strut_top_lst[3],
                                                       fill = self.colour, width = 20 )

            #####TODO: need getter and setter etc
    #def get_coords(self):
        # TODO - is this necessary in current scope of code?

    def set_coords(self):
        self.strut_top_lst = [] #new empty array each time
        for strut in self.master.all_struts:
            strut_top = strut.line.get_strut_top_coords()

            for coord in strut_top:
                self.strut_top_lst.append(coord)
        #TODO: now set the BodyLine coords, remember Canvas.coords(LineID, x0,y0 etc)
        self.master.my_canvas.coords(self.line, self.strut_top_lst[0], self.strut_top_lst[1], self.strut_top_lst[2], self.strut_top_lst[3])
    
