"""!
@file lab3.py
Runs a real and simulated dynamic response to a step response and plots the results.
This program allows for the user to input a desired Kp value and, with a connected
and encoder, will produce a step response for the position of the motor.

This program demonstrates a way to make a simple GUI with a plot in it. It uses Tkinter,
an old-fashioned and ugly but useful GUI library which is included in Python by default.

This file is based loosely on an example found at
https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html

@author Spluttflob (original)
@date   2023-12-24 Original program, based on example from above listed source
@copyright (c) 2023 by Spluttflob and released under the GNU Public Licenes V3
"""

import tkinter
import serial
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


def plot_output(plot_axes, plot_canvas, xlabel, ylabel, Kp_var):
    """!
    Collects data from the test run when Run Test is clicked by reseting the step_response
    program on the microcontroller and reading the printed data to the connected COM Port. Then plots
    the collected data and produces a plot for theoretical data on the same canvas.
    @param plot_axes The plot axes supplied by Matplotlib
    @param plot_canvas The plot canvas, also supplied by Matplotlib
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param Kp_var The text entry object for Kp
    """
    
    # Real test data is read through the USB-serial
    # port and processed to make two lists, xlist and ylist
    
    # States COM device (May vary with different computers)
    com_port = 'COM5'
    
    # Tries to open the defined serial port and run data, and if it can not, will print error
    try:
        serial_port = serial.Serial(com_port, baudrate=115200, timeout=1)
    except serial.SerialException as error:
        print(f"could not open serial port '{com_port}': {error}")
    else:     
        # Uses readline() method to open file as read and run exceptions
        xlist = [] # List of x-values
        ylist = [] # List of y-values
        
        # Writes (Ctrl-B, Ctrl-C, Ctrl-D) to reset the serial port and rerun main on microcontroller
        
        serial_port.write(b'\x02')
        serial_port.write(b'\x03')
        serial_port.write(b'\x04')
        # Waits for "Input" to be prompted by microcontroller
        while True:
            line = serial_port.readline().decode('utf-8').strip()
            #print(f"1 Current Line is {line}")
            if line == "Input":
                #Kp = input("Input Kp: ")
                Kp = Kp_var.get()
                serial_port.write(f'{Kp}\r\n'.encode())
                break
        # Waits for "Invalid" or "Valid" to be prompted by microcontroller
        while True:
            line = serial_port.readline().decode('utf-8').strip()
            #print(f"2 Current Line is {line}")
            if line == "Invalid":
                #Kp = input("Input a valid Kp: ")
                #serial_port.write(f'{Kp}\r\n'.encode())
                Kp_var.set("Invalid Input")
                return
            elif line == "Valid":
                break
        # Waits for the printed out position
        while True:
            # Catches any errors in converting Bytes to Strings
            try:
                # Reads each line printed by the serial port
                line = serial_port.readline().decode('utf-8').strip()
                #print(f"3 Current Line is {line}")
                # Skips processing any blank lines
                if line == '':
                    # print("no input")
                    pass
                if line == 'End':
                    # print("broke out")
                    break
                #print(line)
                line = line.split(',') # Separates each comma separated value
                line = line[:2] # Limits the number of values per line to 2
                for i, value in enumerate(line):
                    value = value.split('#') # Separates out comments
                    line[i] = value[0] # Reads non-commented value to list
                    
                # Tests both values for string or float values
                try: # Tries to convert each pair of values into a float
                    for value in line:
                        value = float(value)
                except ValueError: # For non-float values
                    #print("Skipped line:", line)
                    pass
                else:
                    xlist.append(float(line[0])) # Adds passed float value to x-values
                    ylist.append(float(line[1])) # Adds passed float value to y-values
            except Exception as error:
                    print(error)
            
        # Closes the serial port
        serial_port.close()
        
        # Draw the experimental plot.
        plot_axes.plot(xlist, ylist)
        plot_axes.set_xlabel(xlabel)
        plot_axes.set_ylabel(ylabel)
        plot_axes.grid(True)
        plot_canvas.draw()        


def tk_matplot(plot_function, xlabel, ylabel, title):
    """!
    Create a TK window with one embedded Matplotlib plot.
    This function makes the window, displays it, and runs the user interface
    until the user closes the window. The plot function, which must have been
    supplied by the user, should draw the plot on the supplied plot axes and
    call the draw() function belonging to the plot canvas to show the plot. 
    @param plot_function The function which, when run, creates a plot
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param title A title for the plot; it shows up in window title bar
    """
    # Create the main program window and give it a title
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    # Create a Matplotlib 
    fig = Figure()
    axes = fig.add_subplot()

    # Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()
    
    # Create an input box
    Kp_var=tkinter.StringVar()
    Kp_label = tkinter.Label(master=tk_root,
                             text = 'Input Kp:')
    Kp_entry = tkinter.Entry(master=tk_root,
                             textvariable = Kp_var)
    
    # Create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas,
                                                              xlabel, ylabel, Kp_var))

    # Arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=5)
    toolbar.grid(row=1, column=0, columnspan=5)
    Kp_label.grid(row=2, column=0)
    Kp_entry.grid(row=2, column=1)
    button_run.grid(row=2, column=2)
    button_clear.grid(row=2, column=3)
    button_quit.grid(row=2, column=4)

    # This function runs the program until the user decides to quit
    tkinter.mainloop()


# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program
if __name__ == "__main__":
    tk_matplot(plot_output,
               xlabel="Time (ms)",
               ylabel="Position (counts)",
               title="Step Response")

