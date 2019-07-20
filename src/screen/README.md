# screen
The screen package defines the different ways in which the task manager can
interact with the screen. By default, it contains how the task-manager accepts
user input, how the task list and banner are output to the screen, and how data
is rewritten to the screen when it is resized.

## Code

### inputs.py
`inputs.py` handles user input, and translates user-input characters and
strings into the corresponding commands. Most of the mappings from inputs ->
commands are abstracted out of this file by using factories, so this file
mostly just handles parsing the user input and passing it over to the
corresponding factories in order to execute user-desired actions.

#### Constants
`_task_path` is the file containing the `yaml` formatted task list. `inputs.py`
uses this file as storage in order update the task-list when saved or closed.

#### Extensions
`_string_actions` is a list of the character inputs that require string input.
For example, if you wanted to add a new task, you would need to type in an
entire string and want to ignore the character inputs that would generally map
to other commands.

### outputs.py
`outputs.py` handles how the banner and task-list are physically printed to the
screen, and is generally called from `inputs.py` to update the screen after a
user-requested action.

#### Constants
`_default_color` is the default color to set the banner to, and can be changed
to any valid color
`banner_path` is the file containing the ASCII banner
`_task_path` is the file containing the `yaml` formatted task list.
`outputs.py` uses this load the initial task list on start in order to print it
out. 

### resize.py
`resize.py` is essentially a spin-lock that waits for the screen size to
change, and refreshes the screen if it identifies that has occurred.
