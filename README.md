# Lab4
 Group 18's Lab 4
 
The main purpose of this project is to apply cooperative task management to operate two setups of encoder-motor-controller systems to set their position and proportional gain independently of each other.This is done through an interface between a PC and STM32 microcontroller. 
This project contains the main.py, lab4.py, motor_driver.py, encoder_reader.py, and motor_control.py programs. As made previously, the module, motor_driver.py, creates the class "MotorDriver" which initializes the GPIO pins as PWM outputs for one motor and allows the PWM duty cycle to be set, and the module, encoder_reader.py, creates the class "Encoder" which initializes the timers/counters required for on motor encoder using provided channel pins and a timer/counter and allows the absolute position (accounting for overflow and underflow) to be read and zeroed. The module, motor_control.py, creates the class "MotorControl" which creates a proportional gain controller, allowing for PWM effort to be calculated and returned to be used by the motor based off of user input Kp and desired motor position. 
The program, main.py, is ran on the microcontroller and contains the three class modules to run the step response for motor position. This program implements the cotask module to allow for cooperative tasks for each motor set to be operated seperately, but at the same time. The program, lab3.py, is ran on the PC and contains a GUI to input a position setpoint and Kp value for each motor set's step response to be ran and plotted.

One test that was conducted prior to adjusting the GUI to set the position setpoint and Kp values was to test for the smallest possible task timing without affecting the effectiveness of the controller. The period of this task timing that we determined was the smallest without losing controller effectiveness was 25ms, as seen in Figure 1.

![Minimum Input Period](https://github.com/Cadre1/Lab4/assets/55156855/a421cfda-80c9-42af-abf0-d619554a3031)

Figure 1. Smallest Task Timing without Losing Controller Effectiveness

The next two figures, Figure 2 and 3, show that increasing the period too much - from 20ms and 25ms for blue and orange, respectively, to 40ms and 45ms for blue and orange, respectively - makes the response significantly less smooth since the controller is only ran periodically to adjust the motor.

![Dual Step Responses](https://github.com/Cadre1/Lab4/assets/55156855/6307fb36-73d6-4841-b59e-4533332be3e4)

Figure 2. 20ms and 25ms Task Timing Step Response Effectiveness

![Dual Step Responses(40,45ms)](https://github.com/Cadre1/Lab4/assets/55156855/eab9818c-d935-4d83-ba66-46c7cb78a581)

Figure 3. 40ms and 45ms Task Timing Step Response Effectiveness
