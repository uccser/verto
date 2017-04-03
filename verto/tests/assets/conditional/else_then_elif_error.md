{conditional if condition="version == 'teacher'"}

This is text that only teachers should see.

{conditional else}

This is text that everyone else should see.

{conditional elif condition="version == 'instructor'"}

This is text that only instuctors should see.

{conditional end}
