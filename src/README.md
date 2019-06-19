# src
The `src/` directory contains all of the source code for the task manager, as
well as relevant data files.  

## Layout
The `src/` directory contains several packages which correspond to different
functionalities of the task manager. The file that controls all of these
diferent functionalities is `app.py`.

### app.py
`app.py` primarily acts as a thread controller which is used to define and run
different threads which correspond to different aspects of the task-manager
that write to the screen simultaneously. These threads are easily extensible by
adding an tuple to the `actions` list containing the function to run as a
thread as well as the desired parameters. The threads created by default are
listed below:

1. The banner printer in charge of printing the banner on the top of the
   screen.
2. The resize daemon which checks to see if the screen has been resized and
   refreshes it if that is the case
3. The clock which constantly updates itself at the bottom of the screen
4. The input handler which listens for user input and displays the desired
   aspects of the task tree corresponding to that user input 

### Packages
The `src/` directory also contains several packages which hold the logic of
various aspects of the task-manager. These packages will have their own
documentation with greater detail but briefly can be understood as:

1. `colors`: The color manager which parses user-modifyable color files in
   order to choose colors for all different aspects of the task manager.
2. `gadgets`: A package containing dynamic gadgets that appear on the screen
   alongside the task manager. As the banner is static, the only dynamic gadget
by default is the clock.
3. `screen`: The source of control for parsing input and dislaying static
   output, or input-dependent output to the screen. Examples of static output
are the banner, and of input-dependent output are the task manager and the
resize configuration
4. `shared`: A package defining shared utilities and resources between the
   various aspects of the task manager. Things like thread synchronization and
common utilities for finding configuration files are placed here.
5. `tasks`: This package defines the base classes that define tasks, and
   actions that can be taken against these tasks through user input. These base
classes can be extended, similarly to how the default task hierarchy and action
list extends these base classes.

