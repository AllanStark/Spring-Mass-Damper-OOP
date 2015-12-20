# smd_cfg.py

# define all globals

# model will run until max_time sec in increments of time_step
# 123 are dummy values, never used as they will be overwritten by main program
# they are here as an error catcher
# if you see 123 anywhere the value overwrite hasn't worked

max_time = 123
elapsed_time = 123  # problems with this updating to zero, but not updating
                    # in physics loop cycle?!?!?
time_step = 123
g = 123

# default values (for when prog first opens- all struts have these values)
df_mass = 300 # kg mass on strut
df_fl = 1     # m length
df_sr = 40000 # N/m spring rate
df_dc = 1000 # N/m/s damper constant
df_vel = 0 # m/s initial strut vel

wheelbase = 666 #m wheelbase

# global gui objects to enable cross module comms
my_ParamsDisplay = None
my_SuspPlot = None

my_SuspDisplay = None

