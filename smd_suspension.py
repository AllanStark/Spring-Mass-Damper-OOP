#### Spring, Damper, Suspension Classes

import smd_config
#TODO:need to chase all globals here!

class Spring():
    
    def __init__(self, spring_const, free_length):
        
        self.spring_const = spring_const
        self.free_length = free_length

        print("init spring, spring_const = ", spring_const, "free_length = ", free_length)

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

    def calcDamperForce(self, vel): #

        damper_force = -(vel * self.damper_const)

        return damper_force

# car suspension strut, collection of Spring, mass, Damper
class Suspension():
                    # flt, flt, array[floats], flt, flt, flt
    def __init__(self, mass, vel, applied_force, spring_const, free_length, damper_const):

        self.mass = mass

        # Suspension object inits its own Spring and Damper objects                 
        self.spring = Spring(spring_const, free_length) ### should object name be capital "Spring"
        self.damper = Damper(damper_const)
        self.vel = vel
        self.applied_force = applied_force

        #global g
        self.g = smd_config.g # neessary to copy global? no harm but also no need?

        self.gravity_force = self.g * self.mass                 
                         
        # length starts at equm length according to spring
        # NOTE APPLIED FORCE SET TO ZERO FOR THIS SPECIFIC FUNC CALL
        self.length = self.spring.calcSpringEqumLength(self.gravity_force,0)#, self.applied_force) add later when app force is fn of time
        print("self.length in init", self.length)

    # I don't like the name for this method... maybe suspensionTimeStep?
    def calcSuspensionPosition(self, elapsed_time): #TODO globals

        #TODO: elapsed time not updating?!??!!? almost like phys loo isn't sending back to config
        #bodged by using a local
        #print("calcSP, time_step", smd_config.time_step, "elapsed_time", elapsed_time)

        # calc forces, first find spring and damper forces
        self.spring_force = self.spring.calcSpringForce(self.length)

        #print("spr force in calcSP", self.spring_force)

        self.damper_force = self.damper.calcDamperForce(self.vel)
        #print("damp force in calcSP", self.damper_force)

        # now find resultant of all forcces
        # note lookup of specific time's index in applied_force list
        #print("calcSuspensionPosition using applied_force index ", int(elapsed_time/time_step) )

        self.total_force = self.applied_force[int(elapsed_time/smd_config.time_step)]+ self.gravity_force + self.spring_force + self.damper_force
                            
        self.force_on_road = self.spring_force + self.damper_force

        #print("grav force in calcSP", self.gravity_force)
        #print("app force in calcSP", self.applied_force)
        
        # now can find the acceleration
        self.accel = self.total_force/self.mass
        #print("accel", self.accel)

        # now velocity
        self.vel = self.vel + (self.accel * smd_config.time_step)
        #print("vel", self.vel)
        
        # now new length
        self.length = self.length + (self.vel * smd_config.time_step)

        # now update elapsed time NO! NOW UPDATED IN PHYSICS LOOP MODULE
        #smd_config.elapsed_time = smd_config.time_step + smd_config.elapsed_time
        #print("elapsed_time inside calcSuspensionPosition", elapsed_time)

        #return dict of various values                 
        return{'total_force': self.total_force, 'length' : self.length,
               'time' : elapsed_time, 'force_on_road': self.force_on_road}
    
