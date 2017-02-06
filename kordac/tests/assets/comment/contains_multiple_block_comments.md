{comment}
.. xhtml5 Eventually this could use a parameter so there's one version with no tabs, and a later one with them.
{comment end}

{button link="http://www.csfieldguide.org.nz/releases/1.9.9/_static/widgets/COMPRESSION/LWZ/public_html/index.html" text="View compression interactive"}

{comment}
.. xjrm (or Rhem): pasting text in that is too big causes it to be rejected. It would be nicer if the pasted text is truncated to the maximum length.
{comment end}

You can also enter your own text by clicking on the "Text" tab.
You could paste in some text of your own to see how many characters can be replaced with references.

The references are actually two numbers: the first says how many characters to count back to where the previous phrase starts, and the second says how long the referenced phrase is.
Each reference typically takes about the space of one or two characters, so the system makes a saving as long as two characters are replaced.
The options in the interactive above allow you to require the replaced length to be at least two, to avoid replacing a single character with a reference.
Of course, all characters count, not just letters of the alphabet, so the system can also refer back to the white spaces between words.
In fact, some of the most common sequences are things like a full stop followed by a space.

This approach also works very well for black and white images, since sequences like "10 white pixels" are likely to have occurred before.
Here are some of the bits from the example earlier in this chapter; you can paste them into the interactive above to see how many pointers are needed to represent it.

```
011000010000110
100000111000001
000001111100000
000011111110000
000111111111000
001111101111100
011111000111110
111110000011111
```

In fact, this is essentially what happens with GIF and PNG images; the pixel values are compressed using the Ziv-Lempel algorithm, which works well if you have lots of consecutive pixels the same colour. But it works very poorly with photographs, where pixel patterns are very unlikely to be repeated.

{comment}
.. xtcb extra for experts: compress "aaaaaaaaaa". how can it decode?

.. xtcb  Project
.. Students should try an algorithm [zip, gzip etc.] on several different text files, image files, sound files, and video files.
.. What would happen if text compression was lossy? (I think this should be a part of their merit discussion)
{comment end}