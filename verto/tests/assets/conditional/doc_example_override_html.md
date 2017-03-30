{conditional if condition="version == 'teacher'"}

This is text that only teachers should see.

{conditional elif condition="version == 'instructor'"}

This is text that only instuctors should see.

{conditional elif condition="version == 'coordinator'"}

This is text that only coordinators should see.

{conditional end}
