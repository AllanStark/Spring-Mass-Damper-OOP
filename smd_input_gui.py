# smd_input_gui.

# TODO: setter functions

#REF
# http://effbot.org/tkinterbook/grid.htm
# gets user input values for strut parameters

import tkinter as Tk

# "internal" import of config (global vars)
import smd_cfg
import smd_physicsloop

class GUIParamsDisplay():
    # Master frame for gui that holds user input parameters

    def __init__ (self, root, car):

        self.root = root

        self.my_frame = Tk.Frame(self.root, width = 300, height = 200, background = 'white')

        self.my_frame.grid(row = 0, column = 0)

        # frame components - LH frame with nemss of params
        
        self.name_frame = Tk.Frame(master = self.my_frame)
        
        # parameter name labels
        self.loc_label = Tk.Label(master = self.name_frame, text = "Location")
        self.mass_label = Tk.Label(master = self.name_frame, text = "Mass on axle")
        self.FL_label = Tk.Label(master = self.name_frame, text = "Free length")
        self.SR_label = Tk.Label(master = self.name_frame, text = "Spring Rate")
        self.DC_label = Tk.Label(master = self.name_frame, text = "Damping Constant")

        self.loc_label.grid(row = 0, column = 0)
        self.mass_label.grid(row = 1, column = 0)
        self.FL_label.grid(row = 2, column =0)
        self.SR_label.grid(row = 3, column = 0)
        self.DC_label.grid(row = 4, column = 0)

        # CENTRE frames for individual struts with param values
        #TODO: take this from global?array to hold all struts
        self.car = car
        self.all_struts = car.all_struts

        for strut in self.all_struts: #array of all strut objects

            # create the gui frame holding param entry boxes for each strut
            strut.GUIParams = GUIParamsForAStrut(strut, self.my_frame)
        
        # paramter unit label - RH frame with units
        self.unit_frame = Tk.Frame(master = self.my_frame)

        self.loc_u_label = Tk.Label(master = self.unit_frame)
        self.mass_u_label = Tk.Label(master = self.unit_frame, text = "kg")
        self.FL_u_label = Tk.Label(master = self.unit_frame, text = "m")
        self.SR_u_label = Tk.Label(master = self.unit_frame, text = "N/m")
        self.DC_u_label = Tk.Label(master = self.unit_frame, text = "N/m/s")

        self.loc_u_label.grid( row = 0, column = 0)
        self.mass_u_label.grid( row = 1, column = 0)
        self.FL_u_label.grid( row = 2, column = 0)
        self.SR_u_label.grid( row = 3, column = 0)
        self.DC_u_label.grid( row = 4, column = 0)

        #Button to confirm input values

        self.params_confirm_btn = Tk.Button(master = self.my_frame, text = "Commit",
                                            height = 3, width = 6, command = self.update_all_strut_params)
        self.params_confirm_btn.grid( row = 0, column = 4)

        # grid  all sub-frames (side by side)

        self.name_frame.grid( row = 0, column = 0)

        #grid the individual struts' frames

        counter = 1
        for strut in self.all_struts:
            
            strut.GUIParams.my_frame.grid( row = 0, column = counter)
            counter = counter+1
            
        self.unit_frame.grid( row = 0, column = 3)

    def update_all_strut_params(self): #TODO, do I need to pass all vars?  or does self imply all associated

        all_strut_params = []
        for strut in self.all_struts:

            # get
            strut_params = strut.GUIParams.get_strut_params()
            # set (fn in Suspension)
            strut.set_strut_params(strut_params)

            # TODO set the SuspDisplay cartoon here, or wait until after phys model?

        smd_physicsloop.physics_loop(self.car)
        # TODO, potentially set the SuspDiaplay cartoon here to starting values from the phys model run.

        # Telemetry graphs, clear all old plots and then plot current telem
        smd_cfg.my_SuspPlot.clear_telem() 
        smd_cfg.my_SuspPlot.plot_telem() # TODO; not plotting until mouseover graph area!


class GUIParamsForAStrut():
    # This is a frame for a strut's parameters with input text boxes, labels etc.
    # Several of these can sit in the overall frame

    def __init__ (self, strut, root):

        self.root = root
        self.location = strut.name # e.g. F or R (str)

        self.my_frame = Tk.Frame(self.root, width = 300, height = 200, background = 'red')
        self.my_frame.grid(row = 0, column = 0)

        # TODO: check - get values from actual strut object
        self.mass = strut.mass # kg
        self.fl = strut.spring.get_params()[1] # m
        self.sr = strut.spring.get_params()[0] # N/m
        self.dc = strut.damper.get_DC()  # N/m/s
        
        # define entry boxes here (should I use textvariables here?)
        
        self.loc_label = Tk.Label(master = self.my_frame, text = self.location)
        self.M_entry = Tk.Entry(master = self.my_frame)
        self.FL_entry = Tk.Entry(master = self.my_frame)
        self.SR_entry = Tk.Entry(master = self.my_frame)
        self.DC_entry = Tk.Entry(master = self.my_frame)

        #grid them all
        self.loc_label.grid( row = 0, column = 0)
        self.M_entry.grid( row = 1, column = 0)
        self.FL_entry.grid( row = 2, column = 0)
        self.SR_entry.grid( row = 3, column = 0)
        self.DC_entry.grid( row = 4, column = 0)

        #set defaults
        self.M_entry.insert( 0, self.mass )
        self.FL_entry.insert( 0, self.fl )
        self.SR_entry.insert( 0, self.sr )
        self.DC_entry.insert( 0, self.dc )        
        
    def get_strut_params(self): # returns a dict of the params for this strut

        self.M = float( self.M_entry.get() )
        self.FL = float( self.FL_entry.get() )
        self.SR = float( self.SR_entry.get() )
        self.DC = float( self.DC_entry.get() )

        self.params = {"mass":self.M, "free_length":self.FL, "spring_rate":self.SR, "damp_const":self.DC}       
        
        return self.params




