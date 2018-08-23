Play-mario-automatically
=====

Use "Artificial mental retardation" to play Super Mario Bros(1985/FC)
-----

This is my first personal work.

At the beginning of the August 2018, it was influenced by a neural network called Mariflow,
I decided to write a script that could pass the Super Mario Bros (1985/FC).

This script doesn't have complex code, doesn't read the map, doesn't evolve automatically,
so I call it "Artificial mental retardation".

I used Cheat Engine for constant testing, got some key data from the RAM map,
and let "Artificial mental retardation" read the RAM map through the Windows API to get Mario's state.

Then I use PyUserInput to achieve the "Artificial mental retardation" control of Mario.

"Artificial Mental retardation"'s working mode is similar to "mouse walks the maze",
accelerate to the right, keep trying, and if Mario dies or hits a wall, read file,
keep cycling, until it pass the target checkpoint.

Certain checkpoints are mazes,like 8-4,
at present "Artificial mental retardation" failed to pass them
I will continue to update the algorithm to through them.
