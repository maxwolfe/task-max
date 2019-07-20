# gadgets
Gadgets are utilities other than the main task manager that share the same
screen. By default, the only gadget available is a clock, where the constant
glyphs corresponding to how the time can be represented is stored in
`clock_glyphs.py`.

## Code

### clock\_output.py
`clock_output.py` defines how the clock is represented on the screen and how it
is updated.

#### Constants
`_default_color` represents the color the clock will be presented as by default
(if it is not in a pre-defined range)
`_24_hour_clock` is a boolean that defines if the clock should use 24-hour
notation or 12-hour notation.

#### Extensions
`_color_ranges` is an extensible list that defines the color the clock should
be for a pre-determined range of time. You may extend an arbitrary amount of
color ranges, but only the first match will be considered.

