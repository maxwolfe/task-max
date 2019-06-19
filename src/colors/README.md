# colors
The color manager which parses user-modifyable color files in order to choose
colors for all different aspects of the task manager.

## Code

### color.py
`color.py` defines how colors are loaded into curses and then later referenced. Colors are defined by their 256 bit code and mapped by a custom string. An example of this is:

```
Epic:
  name: Epic
  colorId: 129
```

#### Constants
`_default` represents the color to use by default if a bad key, or no key is
given. Note that this uses the string key value, and no the 256 bit code
corresponding the color.
`_bg_default` represents the 256 bit code of the default background color
`select_default` represents the 256 bit code of the default background color to
use when highlighting (or selecting) a task

#### Extensions
`_strategy_list` is extensible by adding a tuple entry containing a file
containing `colorId` and `name` pairs for colors to load, and a strategy for
interpreting that file as a dictoinary.

### strategy.py
`strategy.py` defines the methods to parse custom files for `colorId` and
`name` pairs. 

#### Extensions
The `LoadStrategy` class can be extended in order to define how to parse a
custom file format.
