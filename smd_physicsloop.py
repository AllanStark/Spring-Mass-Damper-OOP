#~~~~~~~~~ PHYSICS MODEL LOOP FUNCTION ~~~~~~~~~~~~#

#loop that runs the model, calling calcSuspensionPosition for each time step
# TODO: 
#     Refactor how it summons struts, pass all struts as a tuple?
#     
#      Should make strut_n_data part of Suspension class?  Then can just pass the strut_n objects
#      and access the strut_n_data that way.

import smd_cfg

def physics_loop(strut_1, strut_1_data, strut_2, strut_2_data):

    smd_cfg.elapsed_time = 0
    print("In phys loop, initial elapsed time = ", smd_cfg.elapsed_time)
    
    while (smd_cfg.elapsed_time < smd_cfg.max_time): # would a for loop help the cfg to update?

        #print("Start of Phys Loop cycle, elapsed_time", smd_cfg.elapsed_time)

        dct_output_1 = strut_1.calcSuspensionPosition()
        #print("dct_output_1", dct_output_1)

        dct_output_2 = strut_2.calcSuspensionPosition()

        #TODO: this is not updating when smd_config.elasped_time is used FIND OUT WHY?!?!?!?
        # Therefore I put in a local elapsed_time
        
        smd_cfg.elapsed_time = smd_cfg.elapsed_time + smd_cfg.time_step
        #print("In Phys Loop, updated elapsed time to", smd_cfg.elapsed_time)
        
        #print("in Phys Loop, time_step =", smd_cfg.time_step, type (smd_cfg.time_step) )
    
        #print("dct_output", dct_output)

        # append relevant arrays using output from the dct
        strut_1_data["lst_total_force_1"].append(dct_output_1['total_force'])
        strut_1_data["lst_force_on_road_1"].append(dct_output_1['force_on_road'])

        strut_1_data["lst_length_1"].append(dct_output_1['length'])
        
        strut_1_data["lst_time_1"].append(dct_output_1['time'])

        # append relevant arrays using output from the dct
        strut_2_data["lst_total_force_2"].append(dct_output_2['total_force'])
        strut_2_data["lst_force_on_road_2"].append(dct_output_2['force_on_road'])

        strut_2_data["lst_length_2"].append(dct_output_2['length'])

        strut_2_data["lst_time_2"].append(dct_output_2['time'])
        
        
    print("physics loop finished")

    return  strut_1_data, strut_2_data
