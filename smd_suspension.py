#### Spring, Damper, Suspension Classes

import smd_cfg

#TODO:test to confirm all cfg globals working here!

class Spring():
    
    def __init__(self, spring_const, free_length):
        
        self.spring_const = spring_const
        self.free_length = free_length

        print("init spring, spring_const = ", spring_const, "free_length = ", free_length)


    #TODO: finish setter function, where should/shouldn't it overlap with init?

    def set_params(self, spring_const, free_length):

        self.spring_const = spring_const

        self.free_length = free_length


    def get_params(self):

        spring_params = [self.spring_const, self.free_length]

        return spring_params
    
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

    
    #TODO: setter function as above for spring
    def set_DC (self, damper_const):

        self.damper_const = damper_const

    def get_DC (self):

        return self.damper_const
    
    def calcDamperForce(self, vel): #

        damper_force = -(vel * self.damper_const)

        return damper_force

# car suspension strut, collection of Spring, mass, Damper
class Suspension():
    #Suspension( str name, str colour for tk representations,  arr applied_force, bool ):
    def __init__(self, name, colour, applied_force, is_rear):

        self.name = name # string, eg "F", "R". this is used to pass to GUI labels
        self.colour = colour
        self.is_rear = is_rear
        
        self.mass = smd_cfg.df_mass

        # Suspension object inits its own Spring and Damper objects                 
        self.spring = Spring(smd_cfg.df_sr, smd_cfg.df_fl) ### default values
        self.damper = Damper(smd_cfg.df_dc)
        self.vel = smd_cfg.df_vel
        self.applied_force = applied_force

        #global g
        #self.g = smd_cfg.g # neessary to copy global? no harm but also no need?

        self.gravity_force = smd_cfg.g * self.mass                 
                         
        # length starts at equm length according to spring
        # NOTE APPLIED FORCE SET TO ZERO FOR THIS SPECIFIC FUNC CALL
        self.length = self.spring.calcSpringEqumLength(self.gravity_force,0)#, self.applied_force) add later when app force is fn of time
        print("self.length in init", self.length)

        #TODO: fully implement this dict as a way to record phys model output 
        self.record = {"length":[], "total_force":[], "force_on_road":[], "vel":[], "time":[]}

        #TODO, put time = 0 defaults manualy into array here? else plots don't have anything to read from
        telem = self.calcSuspensionPosition()

        for key in telem:
            value = telem[key] ###TODOTODO
            self.record[key].append(value)

    def blank_all_records(self):
        # replaces record dict with blank - used to scrub all results from previous physics model
        # in order to then run a new one 
        self.record = {"length":[], "total_force":[], "force_on_road":[], "vel":[], "time":[]}
        
        
        
    # I don't like the name for this method... maybe suspensionTimeStep?
    def calcSuspensionPosition(self): #TODO check all cfg globals


        #print("calcSP, time_step", smd_config.time_step, "elapsed_time", elapsed_time)

        # calc forces, first find spring and damper forces
        self.spring_force = self.spring.calcSpringForce(self.length)

        #print("spr force in calcSP", self.spring_force)

        self.damper_force = self.damper.calcDamperForce(self.vel)
        #print("damp force in calcSP", self.damper_force)

        # now find resultant of all forcces
        # note lookup of specific time's index in applied_force list
        #print("calcSuspensionPosition using applied_force index ", int(elapsed_time/time_step) )
        
        self.applied_force_now = self.applied_force[int(smd_cfg.elapsed_time/smd_cfg.time_step)]
        
        self.total_force = self.applied_force_now + self.gravity_force + self.spring_force + self.damper_force
                            
        self.force_on_road = self.spring_force + self.damper_force

        #print("grav force in calcSP", self.gravity_force)
        #print("app force in calcSP", self.applied_force)
        
        # now can find the acceleration
        self.accel = self.total_force/self.mass
        #print("accel", self.accel)

        # now velocity
        self.vel = self.vel + (self.accel * smd_cfg.time_step)
        #print("vel", self.vel)
        
        # now new length
        self.length = self.length + (self.vel * smd_cfg.time_step)

        #return dict of various values                 
        telem = {'total_force': self.total_force, 'length' : self.length, 'vel' : self.vel,
               'time' : smd_cfg.elapsed_time, 'force_on_road': self.force_on_road}

        return telem


    ##### TODO Nov 15: test this!!! Do I need to calc equm length here?
    def set_strut_params(self, params):
        ### params = {"mass":, "free_length":, "spring_rate":, "damp_const":}
        print("updating strut params in Suspension")
        self.mass = params["mass"]

        self.spring.set_params(params["spring_rate"], params["free_length"])

        self.length = self.spring.calcSpringEqumLength(self.gravity_force,self.applied_force[0])##TODO CHECK Jan 16

        self.damper.set_DC(params["damp_const"])     


#TODO: implement as superclass, then subs are 2-wheel chassis, 4 wh chassis     
class Chassis(): # "abstract parent class"
    pass

class HalfCar(Chassis):

    def __init__(self, wheelbase, fcolour, rcolour,
                 applied_force, opposite_applied_force):

        self.wheelbase = wheelbase
        self.fcolour = fcolour
        self.rcolour = rcolour
        self.applied_force = applied_force
        self.opposite_applied_force = opposite_applied_force

        #create struts at F&R extremity of wheelbase

        self.front_st = Suspension( "F", self.fcolour, self.applied_force, False)
        self.rear_st = Suspension( "R", self.rcolour, self.opposite_applied_force, True)
            
        self.all_struts = [self.front_st, self.rear_st] 

        
        
# TODO Nov 15, create setter fn that takes output from inpit_gui getter fn, passes params to each strut's setter fn
    
