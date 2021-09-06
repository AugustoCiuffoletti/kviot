# kviot: providing a secure deep-sleep

*kviot* is a component of an IoT infrastructure that implements three functions:

- provide a WiFi access point for edge units, sensors and actuators
- implement a secure checkpoint repository for edge units
- provide a UTC reference to the edge units

The last two functions are strictly related with the management of the duty-cycle of peripheral units.

## Energy footprint, duty cycle, and deep sleep

In an IoT system keeping as low as possible the energy consumed by peripheral is relevant for the success of the project. From such parameter depend battery replacement times, the size of solar panels used for unattended installations, and the quantity of waste produced in terms of exhausted batteries.

To reduce the energy consumption the system is designed to have a low duty cycle, which is the fraction of time during which edge devices are operational. When the operation of the unit is not needed, for instance if the system requires one measurement every hour from a given sensor, the unit enters an idle state, thus reducing power consumption during that time. An edge unit that is operational for 1 minute every hour has a duty cycle of 1/60, or 16.6%.

A low duty cycle is effective if power consumption during the idle period is really low, as near to zero as possible. Modern microcontrollers provide this feature, sometimes called *deep sleep*, but the same feature can be implemented using external components.

During a deep sleep period all functions un-powered, with the exception of the module in charge of waking up the microcontroller. The power consumption of such a component is typically a few percents of that of the microcontroller.

Among the modules that are un-powered during a *deep-sleep* period there are the SRAM memory of the microcontroller, where data are stored, and the system clock, that provides a time reference for the programs. When the component leaves a *deep-sleep* period such devices are clean: time starts from zero, and there are no data in memory: a *deep-sleep* clears the microcontroller memory.

However, the RTC memory provides some support to limit this effect: the timer module contains a small memory, to store the very basic data, and the timing function may serve to implement a time reference. However such features are quite limited, and do not cover basic requirements such as perform an operation every day with the precision of one minute, or compute an average of the last 100 measurement. For this the microcontroller must be assited by an external sorage and time reference. This is the task for the *kviot* server. 