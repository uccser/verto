Imagine we have the following simple black and white image.

{image file-path="the-first-image.png" alt="Alt text for an image" caption="true"}

This is the first caption.

{image end}

{image file-path="Lipsum.png" caption="true" alt="A diamond shape made out of pixels"}

This is the second caption.

{image end}

{image file-path="pixel-diamond.png" alt="A diamond shape made out of pixels" caption="true"}

This is the third caption.

{image end}

One very simple way a computer can store this image in binary is by using a format where '0' means white and '1' means black (this is a "bit map", because we've mapped the pixels onto the values of bits). Using this method, the above image would be represented in the following way:
