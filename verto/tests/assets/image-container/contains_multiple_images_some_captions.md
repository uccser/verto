Here's another FSA to consider:

{image file-path="finite-state-automata-no-trap-example.png" caption="true" alt="FSA with missing transitions"}

Reputation precedes me.

{image end}

It's fairly clear what it will accept: strings like "ab", "abab", "abababababab", and, of course {math}\epsilon{math end}.
But there are some missing transitions: if you are in state 1 and get a "b" there's nowhere to go.
If an input cannot be accepted, it will be rejected, as in this case. We could have put in a trap state to make this clear:

{image file-path="finite-state-automata-trap-added-example.png" caption="true" alt="FSA with missing transitions"}

I wanna be your end game

{image end}

{image file-path="finite-state-automata-trap-added-extreme-example.png" alt="FSA with missing transitions"}

So, instead, we just say that any unspecified transition causes the input to be rejected (that is, it behaves as though it goes into a trap state). In other words, it's fine to use the simple version above, with just two transitions.
