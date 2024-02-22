"""! @file main.py
This program sets up the pins and timers required for a "MotorDriver" and an "Encoder" object and then sets up a "MotorControl" object.
It then waits for an input Kp value in which it will use to run a step response for the motor's position.
The motor will have its PWM duty cycle set based off of the returned motor position from the encoder and passed through the proportional controller.
The results of the step response are printed to the COM port to be read by "lab3.py"
"""

import motor_control
import motor_driver
import encoder_reader
import utime

if __name__ == "__main__":
    # Motor setup from Lab1
    
    # Initializing the Motor Pins and Timers
    a_pin = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    in1pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    in2pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    a_timer = pyb.Timer(3, freq=1000)

    # Creating the Motor Driver Object
    moe = motor_driver.MotorDriver(a_pin, in1pin, in2pin, a_timer)
    moe.enable()
    
    # Encoder setup from Lab2

    # Initializing the Encoder Counter and Pins
    timer_C = pyb.Timer(8, period=65535, prescaler=0)
    pinC6 = pyb.Pin(pyb.Pin.board.PC6)
    pinC7 = pyb.Pin(pyb.Pin.board.PC7)
    
    # Creating the Encoder Object
    enc = encoder_reader.Encoder(pinC6, pinC7, timer_C)
    
    # Motor Controller setup
    
    # Initialize Kp and setpoint
    Kp = 0
    setpoint = 0
    
    # Creating the Motor Controller Object
    moe_con = motor_control.MotorControl(Kp, setpoint)
    
    # Prints "Input" to be read by "lab3.py"
    print("Input")
    while True:
        try:
            # Waits for an input Kp to be .write() to the shell
            val = input()
            print(f"Input is: {val}")
            print(f"Input type is: {type(val)}")
            Kp = float(val)
            print(f"Final Input type is: {type(Kp)}")
            print(f"Final float value is: {Kp}")
        except:
            # Returns "Invalid" if the input value is invalid
            print("Invalid")
        else:
            # Otherwise returns "Valid" if the input value is valid
            print("Valid")
            break
    
    # Sets the setpoint and Kp
    setpoint = 16000
    moe_con.set_Kp(Kp)
    moe_con.set_setpoint(setpoint)
    
    # Runs the closed-loop motor position step response
    time_interval = 1000 # 1 second overall run time
    start_time = utime.ticks_ms()
    end_time = utime.ticks_add(start_time,time_interval)
    curr_time = start_time
    while utime.ticks_diff(end_time,curr_time) > 0:
        curr_time = utime.ticks_ms()
        pos = enc.read_position()
        PWM = moe_con.run(pos)
        moe.set_duty_cycle(PWM)
        utime.sleep_ms(10)
    print("Start")
    moe_con.print_step_response(start_time)
    print("End")
    moe.disable()
