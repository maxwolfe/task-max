# task-max
Organizing ourselves effectively is one of the most challenging problems we
face, regardless of our occupation or background. `task-max` is a highly
customizable tree-based organizational system which links tasks by their
dependencies (or children in a tree). This project provides a basic outline for
the core functionalities of an organizational tool and allows for easy
customization through inheritable or otherwise modifyable classes sufficiently
isolated from the core functionality.

## Installation
`git clone https://www.github.com/maxwolfe/task-max`

## Basic Usage
1. Create a virtual environment:

`virtualenv -p python3.5 venv`

2. Access your virtual environment:

`source venv/bin/activate`

3. Install required libraries:

`pip install -r requirements.txt`

4. Execute task-max:

`python task-max`

## Outline
`task-max` consists of 4 core components:

1. Threads which control what is written to different, customizable quadrants
   of the screen .

2. Color pairs representing the foreground and background that can be used to
   easily control the color of various aspects of the output.

3. A task hierarchy which can be used to define the dictionary-formatted
   task-list as well as customize different behaviors for tasks at different
depths of the tree.

4. An I/O handler which converts user input into modifications to the task-list
   by interacting with the classes representing different nodes of the task
tree.

## Customization
Each directory in the `src/` folder will have a corresponding `README.md` file specifying details of the contents of that directory. It will also contain useful information on which files are meant for cusomization and how to make customizations smoothly interact with the core functionality.

As a rule of thumb, the `# EXTEND:` Tag will be placed over classes or data structures that are meant to be extended and the `# MODIFY:` Tag will be placed over constants and data structures which are meant to be modified for custom functionality.
