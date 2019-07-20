# shared
Shared utilities are tools which all of the different aspects of the
task-manager need to use. It is mainly used for thread synchronization,
standard tools for managing the screen, and the standard method for finding
resource files.

## Code

### shared.py
`shared.py` simply contains constants that are used for thread synchronization,
specifically for finding if the user wishes to quit the application and all
threads must clean up and shut down.

### utils.py
`utils.py` contains tools in which all of the other packages need in order to
manage the screen or otherwise do general tasks. By default this contains
things like finding resource files and clearing the screen before outputting to
it.

#### Constants
`_files` defines the defaults folder location where resource files are stored
inside a package, and can be modified as long as all packages follow the same
style

