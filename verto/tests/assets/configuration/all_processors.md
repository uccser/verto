# Example Title

This is a sentence.

# Example Title 2

{comment This is a comment for other authors to read}

Check out this [resource](resource/134).

{panel type="teacher-note" title="Teacher Note" subtitle="Guides for Algorithms"}

This text is the panel's contents.

{panel end}

{image file-path="http://placehold.it/350x150" caption="Placeholder image" source="https://placehold.it/" hover-text="This is hover text" alignment="left"}

{boxed-text}

**Computer Science Report for 2.44**

Put your introduction to what bits are here.

{boxed-text end}

{button-link link="http://www.google.com" text="Visit Google"}

{conditional if condition="version == 'teacher'"}

This is text that only teachers should see.

{conditional end}

It's worth considering which {glossary-link term="algorithm"}algorithms{glossary-link end} should be used.

{iframe link="https://github.com/"}

{interactive name="binary-cards" type="iframe" parameters="digits=5&start=BBBBB"}

    scratch
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

{table-of-contents}

{video url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
