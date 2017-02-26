{conditional if="version == 'teacher'"}

This is text that only teachers should see.

{conditional elif="version == 'instructor'"}

This is text that only instuctors should see.

{conditional elif="version == 'coordinator'"}

This is text that only coordinators should see.

{conditional else}

This is text that everyone else should see.

{conditional end}
