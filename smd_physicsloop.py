#~~~~~~~~~ PHYSICS MODEL LOOP FUNCTION ~~~~~~~~~~~~#

#loop that runs the model, calling calcSuspensionPosition for each time step
# TODO: 
#     Refactor how it summons struts, pass all struts as a tuple? DONE
#     
#      Should make strut_n_data part of Suspension class?  Then can just pass the strut_n objects
#      and access the strut_n_data that way. DONE

import smd_cfg


## (LIST all_struts [Suspension OBJECTS]), 
def physics_loop(car):

    #TODO - is this best placed here???scrub all of any prev phys loop results to give this loop a clean slate
    for strut in car.all_struts:
        strut.blank_all_records()
        
    smd_cfg.elapsed_time = 0
    print("In phys loop, initial elapsed time = ", smd_cfg.elapsed_time)
    
    while (smd_cfg.elapsed_time < smd_cfg.max_time): # would a for loop help the cfg to update?

        #TODO - record telemetry needs implementing in Suspension class
        for strut in car.all_struts:

            #do physics loop
            telem = strut.calcSuspensionPosition()

            #TODOTODOTODO
            strut.record['total_force'].append(telem['total_force'])
            strut.record['force_on_road'].append(telem['force_on_road'])
            strut.record['length'].append(telem['length'])
            strut.record['vel'].append(telem['vel'])
            #time is appended from inside calcSuspensionPosition should I use global directly here instead?
            strut.record['time'].append(telem['time']) #

        # now all struts done, time step has finished, so incr time
        smd_cfg.elapsed_time = smd_cfg.elapsed_time + smd_cfg.time_step
        #print("In Phys Loop, updated elapsed time to", smd_cfg.elapsed_time)
        
    print("physics loop finished")

