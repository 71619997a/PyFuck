PyFuck
======

A brainfuck interpreter written in python, including some extra functions.

TO COMPILE: cd to this directory, and
python pyfuck.py 

SHORT USAGE STUFF:
+ increments current mem
- decrements "	       "
. prints     "	       "
, inputs to  "	       "
> moves pointer forward
< moves pointer back (this will wrap)
[ starts a loop
] ends   "    "

NEW COMMANDS:

_ prints the mem area around pointer
: starts/ends a function
@ ends program

FUNCTIONS:
also "subroutines". these are defined in subroutines.pbf in this format

::function name::function body[::]
::next function name::next function body[::]
and so on...
when program is run, this checks for :function name: and replaces inline with function body