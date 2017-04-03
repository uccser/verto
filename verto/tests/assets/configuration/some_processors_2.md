# Another Example Title

{image file-path="totally-legit-image.png"}

This is a sentence.

Here's another FSA to consider:

{image file-path="finite-state-automata-no-trap-example.png" alt="FSA with missing transitions"}

It's fairly clear what it will accept: strings like "ab", "abab", "abababababab", and, of course {math}\epsilon{math end}.
But there are some missing transitions: if you are in state 1 and get a "b" there's nowhere to go.
If an input cannot be accepted, it will be rejected, as in this case. We could have put in a trap state to make this clear:

{image file-path="finite-state-automata-trap-added-example.png" alt="FSA with missing transitions"}

But things can get out of hand. What if there are more letters in the alphabet? We'd need something like this:

{image file-path="finite-state-automata-trap-added-extreme-example.png" alt="FSA with missing transitions"}

So, instead, we just say that any unspecified transition causes the input to be rejected (that is, it behaves as though it goes into a trap state). In other words, it's fine to use the simple version above, with just two transitions.

{glossary-link term="hello"}{glossary-link end}

The most precise way of giving a set of instructions is in the form of a
{glossary-link term="algorithm" reference-text="computer program"}program{glossary-link end},
which is a specific implementation of an algorithm, written in a specific programming language, with a very specific result for any particular input.

Because algorithms exist even if they aren't turned in to programs, we won't need to look at programs at all for this topic, unless you particularly want to.

{glossary-link term="algorithm" reference-text="algorithm cost"}{glossary-link end}

They also happen to be great for illustrating some of the key concepts that arise with algorithms.

{glossary-link term="algorithm" reference-text="searching algorithms"}{glossary-link end}

{glossary-link term="algorithm" reference-text="sorting algorithms"}{glossary-link end}
