# Turing
This is a quick implementation of a Turing machine in Python, Tkinter.
I wrote this code in order to work on finding Turing machines efficiently and test them. There are a lot of changes to be made to the code to make it much more efficient, plus new features to be added.

## Implementation
This program uses a serie of inputs set to 0, 1 or empty. The states define, for each value, what it has to be changed to, the direction to go in and the next state. At the start, every input is set to empty and the firstly created and used state is 'init'.
Empty can be represented with red, 0 with yellow and 1 with red.

## Usage
Upon executing the main file, two windows pop out, one is the set of inputs, the other one contains the entries for the states. For now, the console is still used a bit.
The inputs window has a row of 20 squares (size is customizable in the program) that each can take the three previous colors. It swaps between these colors on click. The 'start' button launches the simulation.
The states window first contains a frame labeled 'init' which defines the initial state. A state is defined in three rows, one for every slot possible. For each possibility, you have an other color case for what it will be replaced with, an arrow to indicate the direction the cursor will go in and an entry to specify the next state's name. The 'add state' button asks you in the console the name of the new state then creates a frame in the same window.
**Be careful of the state's name and make sure to fill the entry with one valid state name. They are executed upon starting the simulation (see the code explanation below).**
By default, three states are defined: 'init', the first to be executed; 'vrai', which concludes the program; 'puits', putting the program in an infinite loop.

## Exporting a set of states
*Soon!*

## Default examples
*Soon!*

## Code explained
### Machine creation
*Soon!*
### Function generation
For each state, a function is called, named 'State.genFunc'. It generates a multiple-line string that writes a function definition.
The function is named after the state's name. It takes for parameters the current row and the position of the cursor. It tests what the slot corresponds to, modifies the cursor accordingly, then returns the new list, the new position of the cursor and the next function.
The generated string is executed directly. The author has to be careful not to specify a wrong name for the states or an inexistant next state.
### Execution
After the 'start' button is pressed, three variables become primordial: 'func', 'slots' and 'cursor'.
These are modified every new iteration: the current function is called and replaced with its own returned values, alongside the row and the cursor.
A new row is created, displaying the new state.
