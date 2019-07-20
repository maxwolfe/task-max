# tasks
The Tasks package contains most of the logic for how tasks are represented and
interacted with, and how user-defined actions modify the task-list.

## Code

### action\_factory.py
`action_factory.py` defines how user inputs map to actions, or functions that
can be run on the highlighted task at the time of input (or ignore the current
task and interact globally).

#### Extensions
`_mappings` is a list of character to action mappings that defines what action
should be called based on the user-input. This can be extended with any single
character and action (which are defined in `actions.py`

### actions.py
`actions.py` defines a list of objects which describe how to implement a
certain action. They take in a list of parameters (the highlighted task and
optionally a user-input string) and initialize a function to be called with
`.do_action()` and the parameters for that function.

#### Extensions
Action objects can be easiy added by extending the `Action` base class and
initializing the object with a function to call with `do_action()` and the
appropriate parameters.

### strategy.py
`strategy.py` contains different strategies which can be interchanged to
implement functionalities which can be done in many different ways. By default,
a strategy exists for selected a new task based on the user input (what is the
new task they want to select?).

#### Extensions
Strategy objects can be created by implementing functionality required for that
task, for example for selecting you need to be able to find certain other tasks
based on your current location in order to effectively implement all desired
user actions.

### task\_factory.py
`task_factory.py` defines the task-hierarchy, and how to dynamically generate a
subtask based on the currently selected task. 

#### Extensions
`_hierarchy` can be extended by defining the depth at which task object or task
factory operates. For example, by default we start with an `Epic` object which
can create `Sprint` object subtasks. But a `Sprint` object can have either a
`FastTask` object or a `Blocker` object as a subtask, so uses a `FastFactory`
in order to dynamically create the appropriate object based on the context

### task\_list.py
`task_list.py` defines how the `yaml` configuration is used to generate a
task-list (or tree), and how a user can then interact with that tree.

#### Constants
`_selection_strategy` can be modified to determine the algorithms used to find
the next task to select based on the current task and the users input

### tasks.py
`tasks.py` contains the `Task` and `Factory` objects that define the types of
tasks at each depth of the tree. The `Task` object defines how `yaml`
configurations are translated into usable objects, and the `Factory` object
defines how to dynamically determine what kind of task to generate based on the
current task and user input.

#### Constants
`_color` is the default color a task will appear as, and can be modified to any
valid color
`_priority` is the default priority of a task (starting at 0) which corresponds
to the tasks depth (0 is highest depth)
`_selection_strategy` can be modified to determine the algorithms used to find
the next task to select based on the current task and the users input

#### Extensions
`_required_args` is a list of attributes that must exist for each task object
By default these attributes define the tasks description, if it is currently
selected, and if it is currently open
`_supported_args` are optional arguments that can define other traits of a
task, for example if it is blocking other tasks

##### Extending Arguments
As you extend the list of arguments, you also must extend the attribute
functions for the `Task` object. This can be done either in `__init__` or by
creating properties.

##### Extending Tasks and Factories
By inheriting from `Task` or `Factory` you can create an arbitrary amount of
kinds of tasks at each depth of the task-list. This generally requires only
minor configuration of a few variables.
