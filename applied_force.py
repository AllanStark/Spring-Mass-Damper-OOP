import smd_cfg

#~~~~~~~ APPLIED FORCE ~~~~~~#

# this returns an array of the applied force to use at each time step
# needs to have as many indices as there are time steps
## see also Suspension __init__ where initial applied_force is set to zero for
## calcSpringEqumLength method (at t=0, spring is at equm length commensurate with the mass)

def setup_applied_force_arr (start1, ramp1, end1, start2, ramp2, end2): 
    """ force pattern is /^^^^^\ takes all ints, start and
    end are times in INDICES ramp is slope (Newtons/index),
    plateau is implied between end1 and start2.  Returns a 2-tuple
    of applied force """

    
    applied_force = [0]*int(smd_cfg.max_time/smd_cfg.time_step) # Newtons note NEGATIVE is DOWN

    #~~~~~~~~~#set up applied force as func of time, ramp function, level, ramp back down
    for i in range (start1,end1,1): # (0, 400) RAMPING UP

        applied_force[i] = (-ramp1)*i

    plateau_force = applied_force[end1-1]

    for i in range(end1,start2,1): # PLATEAU at final value of ramp up 

        applied_force[i] = plateau_force

    for i in range (start2,end2,1): #(1500,2000) RAMPING DOWN

        applied_force[i] = plateau_force -(ramp2*(i-start2))
        
    #~~~~~~~~~#finished setting up applied_force list
    
    print("len of applied force array ", len(applied_force) )

    # placeholder* for second strut taking opposite force to first i.e. as load is transferred
    opposite_applied_force = [-x for x in applied_force]

    return (applied_force, opposite_applied_force)
