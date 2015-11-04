#smd_input_gui.
# TODO: not yet included in main program
# TODO: setter functions

#REF
# http://effbot.org/tkinterbook/grid.htm
#gets user input values for strut parameters 

import tkinter as Tk

# "internal" import of config (global vars)
import smd_cfg

### TODO: prototype for input parameters GUI
    
class GUIParamsDisplay():

    def __init__ (self, root, all_struts):

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
        self.all_struts = all_struts

        for strut in self.all_struts: #array of all strut objects

            #create the gui strip of param entry boxes for each
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
                                            height = 3, width = 6, command = self.get_all_strut_params)

        # grid  all sub-frames (side by side)

        self.name_frame.grid( row = 0, column = 0)

        #grid the individual struts' frames

        counter = 1
        for strut in self.all_struts:
            
            strut.GUIParams.my_frame.grid( row = 0, column = counter)
            counter = counter+1
            
        self.unit_frame.grid( row = 0, column = 3)

    def get_all_strut_params(self): #TODO, do I need to pass all vars?  or does self imply all associated

        all_strut_params = []
        for strut in self.all_struts:

            strut_params = strut.get_strut_params()
            all_strut_params.append(strut_params)

        return all_strut_params   # note, need to reconcile this with array "all_struts"
               #TODO: would be nice to have as a dict of dicts i.e. {"strut1params":{strut_params}, "strut2params"...etc}

        
#TODO: have this as part of strut object - now no need, it's linked to strut object?
class GUIParamsForAStrut():

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



##TESTING TODO: delete this when incorporated into main prog#########
#window = Tk.Tk()

##create ParamsDisplay

#my_ParamsDisplay = ParamsDisplay(window)
