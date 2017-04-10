Scratch is great for kids you can create simple code like:

```scratch
when flag clicked
say [Hi]
```

Which then easily builds into:

```scratch
when flag clicked
say [Hi]
move (foo) steps
turn ccw (9) degrees
```

Finally they can create complex code like so:

```scratch
when flag clicked
clear
forever
pen down

if <<mouse down?> and <touching [mouse-pointer v]?>> then
switch costume to [button v]
else
add (x position) to [list v]
end

move (foo) steps
turn ccw (9) degrees
```
