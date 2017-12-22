Here's another FSA to consider:

{image file-path="finite-state-automata-no-trap-example.png" hover-text="hover text is me" alt="FSA with missing transitions" source="example.com"}

It's fairly clear what it will accept: strings like "ab", "abab", "abababababab", and, of course {math}\epsilon{math end}.
But there are some missing transitions: if you are in state 1 and get a "b" there's nowhere to go.
If an input cannot be accepted, it will be rejected, as in this case. We could have put in a trap state to make this clear:

{image file-path="finite-state-automata-trap-added-example.png" source="example.com" alt="FSA with missing transitions" hover-text="also some hover text"}

But things can get out of hand. What if there are more letters in the alphabet? We'd need something like this:
