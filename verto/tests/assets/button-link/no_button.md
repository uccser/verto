Finally, you’re the top layer of the system. You use the program but you will (hopefully) never have to interact with the more complicated parts of the operating system such as driver software, let alone the hardware. In this way, you can use the computer without ever having to worry about these things.

{image filename="computer-layers.png" alt="The computer can be broken down into multiple layers, starting with the user, then the programs, then the operating system, then finally the hardware." caption="The computer can be broken down into multiple layers, starting with the user, then the programs, then the operating system, then finally the hardware."}

We call a system like this a *layered system*. You can have any number of layers you want but each layer can only communicate with the one directly below it. The operating system can directly access the hardware but a program running on the computer can't. You can use programs but hopefully will never have to access the hardware or the more complex parts of the operating system such as drivers. This again reduces the complexity of the system because each layer only needs to know about the layer directly below it, not any others.

Each layer in the system needs to provide an interface so that the layer above it can communicate with it. For example, a processor provides a set of instructions to the operating system; the operating system provides commands to programs to create or delete files on the hard drive; a program provides buttons and commands so that you can interact with it.

One layer knows nothing about the internal workings of the layer below; it only needs to know how to use the layer’s interface. In this way, the complexity of lower layers is completely hidden, or *abstracted*. Each layer represents a higher level of abstraction.

So each layer hides some complexity, so that as we go up the layers things remain manageable. Another advantage of having layers is that we can change one layer without affecting the others, as long as we keep the layer’s interface the same of course. For example, your browser’s code might change but you might never notice as long as the browser still looks and works the same as before. Of course, if the browser stops working or new buttons appear suddenly you know that something has changed.

Something about a button or more explicitly a button-link that you should not match.
