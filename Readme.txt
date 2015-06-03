Spring-Mass-Damper OOP JLW Mar 2015

This was written as an OOP exercise for myself.  A simple model of a suspension strut with a spring and damper seemed something that would be intuitive to code using OOP.

This program models two spring-mass-damper systems (suspension struts) with additional force being applied to the top of the suspension strut (this is a mimic for load transfer during braking/accelerating).

Caveats:  At the moment each SMD system is just that - there are no "tyres" (though this would not be too much trouble to implement as another SMD also included within a strut), at which point this would basically be a "quarter-car model" per strut.


~~~ Update Mar 15 ~~~

Applied force updated as a function of t, with strut 2 having -applied force of strut 1 (to simulate load transfer). Applied force is a ramp up, level, ramp down function.

Added prototype Tkinter animation - TODO need to get this in a proper framed layout with graphs and text-box input params.

~~~ Update 5 May 15 ~~~
Minor refactoring of applied force

~~~ Update 19 May 15 ~~~
Refactored into separate modules.  Clarity somewhat improved by this but need to look at globalising some variables, and a lot of improvement/additions needed on OO structure.

~~~Update 3 June 15 ~~~
More separation into modules.  smd_config.py used for cross-module globals. Problem with having smd_config.elapsed_time update within physics model loop.  Put elapsed_time as a local in the loop for the time being - need to test cfg updating with a simple example.

GUI - Matplotlib graphs and Tkinter animation now in one window with animate button. 


 
