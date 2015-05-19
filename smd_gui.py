##### SMD_GUI

#####OUTPUT SUSPENSION LENGTH AND FORCE PLOTS - matplotlib

from matplotlib import pyplot as plt
from tkinter import *



def myplot(lst_time_1, lst_length_1, lst_time_2, lst_length_2, lst_force_on_road_1, \
           lst_force_on_road_2, applied_force, opposite_applied_force):

    plt.figure(1)

    plt.subplot(311)
    plt.plot(lst_time_1, lst_length_1, "r")
    plt.plot(lst_time_2, lst_length_2, "b")
    plt.xlabel("time/s")
    plt.ylabel("Length /m")
    plt.title("Suspension Length Plot")


    plt.subplot(312)
    plt.plot(lst_time_1, lst_force_on_road_1, "r")
    plt.plot(lst_time_2, lst_force_on_road_2, "b")
    plt.xlabel("time/s")
    plt.ylabel("Force /N")
    plt.title("Suspension Force Plot")

    plt.subplot(313)
    plt.plot(lst_time_1, applied_force, "r")
    plt.plot(lst_time_2, opposite_applied_force, "b")
    plt.xlabel("time/s")
    plt.ylabel("Force /N")
    plt.title("Applied Force Plot (load transfer etc)")

    plt.show()    


###    PROTOTYPE TKINTER ANIMATION    ####

### To do: arrange this properly, OOP

class SuspDisplay():



    def __init__(self,lst_length_1, lst_length_2, max_time, elapsed_time, time_step):

            #TODO : might be better to make things like max_time global between modules
            # can't just "global" this, need a config.py module
            # http://effbot.org/pyfaq/how-do-i-share-global-variables-across-modules.htm
        
            #### put this in an init function
        self.lst_length_1 = lst_length_1
        self.lst_length_2 = lst_length_2
        self.max_time = max_time
        self.elapsed_time = elapsed_time
        self.time_step = time_step


        # TODO sort these out, class vars, inst vars, what?!?!?
        # at moment have just "selfed" everything - inst vars
        self.root = Tk()
        self.my_frame = Frame (self.root, width = 600, height = 600)
        self.my_frame.grid (row = 0, column = 0)
        self.my_canvas = Canvas(self.my_frame, width = 600, height = 600, background = "white" )

        self.susp_length_1 = 200*self.lst_length_1[0]
        self.susp_length_2 = 200*self.lst_length_2[0]

        self.susp_line_1 = self.my_canvas.create_line( 100, 500, 100, (500-self.susp_length_1), fill = "red", width = 20 ) 
        self.susp_line_2 = self.my_canvas.create_line( 500, 500, 500, (500-self.susp_length_2), fill = "blue", width = 20 )

        self.body_line = self.my_canvas.create_line( 100, (500-self.susp_length_1), 500, (500-self.susp_length_2), fill = "black", width = 10)

        self.my_canvas.grid(row = 0, column =0)

        SuspDisplay.animate(self)

    def animate(self): #temporary placeholder* to display 2 struts at once, sort this out OOP etc

        #TODO, as above, check if some things best as class vars.
        #careful, can't have 1 ms redraw freq, of monitor is not 1000 Hz!!!
        anim_frame_freq = 20 #ms between frame updates
    
        for index in range(0, int(self.max_time/self.time_step),1): #need selfs here else won't run

            if (index%anim_frame_freq == 0):
            
                self.susp_length_1 = 200*(self.lst_length_1[index])
                self.susp_length_2 = 200*(self.lst_length_2[index])

                #delay between animating (i.e. framerate)

                self.my_canvas.after(anim_frame_freq) # 
                self.my_canvas.coords(self.susp_line_1, 100, 500, 100, 500-self.susp_length_1 )
                self.my_canvas.coords(self.susp_line_2, 500, 500, 500, 500-self.susp_length_2 )
                self.my_canvas.coords(self.body_line, 100, (500-self.susp_length_1), 500, (500-self.susp_length_2))
                self.my_canvas.update()

        while True:
            animate_keypress = input("enter n to quit or any other key to animate")
            if(animate_keypress == "n"):
                break
            else:
                SuspDisplay.animate(self)


        self.root.mainloop()
