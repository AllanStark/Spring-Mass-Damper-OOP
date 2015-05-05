Spring-Mass-Damper OOP JLW Mar 2015

This was written as an OOP exercise for myself.  A simple model of a suspension strut with a spring and damper seemed something that would be intuitive to code using OOP.

This program models two spring-mass-damper systems (suspension struts) with additional force being applied to the top of the suspension strut (this is a mimic for load transfer during braking/accelerating).

Caveats:  At the moment each SMD system is just that - there are no "tyres" (though this would not be too much trouble to implement as another SMD also included within a strut), at which point this would basically be a "quarter-car model".

The two instances of objects from the Suspension class were initially done to check that objects were instantiating properly and separately, and for fun to allow plotting of a couple of comparison graphs in matplotlib.  So by setting all parameters the same for both objects, with the exception of e.g damping coefficient, it is possible to see what the effect of different settings are.

The two Suspension objects are not coupled in any way i.e this is not a half-car model.  It is possible to set some complementary arguments e.g. 

strut_1 has applied_force = 1000 N
strut_2 has applied_force = -1000 N

(This is a crude modelling of 1000 N of load transfer between the struts)


~~~ Update Mar 15 ~~~

Applied force updated as a function of t, with strut 2 having -applied force of strut 1 (to simulate load transfer). Applied force is a ramp up, level, ramp down function.

Added prototype Tkinter animation - TODO need to get this in a proper framed layout with graphs and text-box input params.

~~~ Update 5 May 15 ~~~
Minor refactoring of applied force


 
