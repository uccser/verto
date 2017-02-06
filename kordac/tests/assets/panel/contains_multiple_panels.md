{panel type="extra-for-experts" summary="Algorithm complexity"}
The formal term for working out the cost of an algorithm is [algorithm analysis](https://en.wikipedia.org/wiki/Analysis_of_algorithms),
and we often refer to the cost as the algorithm's *complexity*.
The most common complexity is the "time complexity" (a rough idea of how long it takes to run),
but often the "space complexity" is of interest - how much memory or disk space will the algorithm use up when it's running?

There's more about how the cost of an algorithm is described in industry,
using a widely agreed on convention called 'Big-O Notation',
in the ["The whole story!"](chapters/algorithms.html#the-whole-story) section at the end of this chapter.
{panel end}

{panel type="teacher-note" summary="Presenting searching in the classroom"}

The present searching game in this section is split into two parts, the first corresponds to the Linear Search algorithm (also known as Sequential Search) and the second corresponds to {glossary-link term="Binary Search"}Binary Search{glossary-link end}. We recommend you play through the levels yourself for a while, or after reading this description. It is based on the [CS Unplugged Battleships game](http://csunplugged.com/searching-algorithms) which can be used as a classroom activity to enforce the lessons in this chapter (the hashing activity is not used for the present searching game). The

To run this as a classroom activity get all the students to play each section of the game at the same time and then when they have all finished have a discussion about the results. After students have finished the first part ask them questions like "Did anyone find the pet on the first go?", "Did anyone only find it after checking every other present?", or find the average number of presents students had to open to find the pet (this should be around 5 for the first level and around 10 for the second).

While they are playing the second part some may have trouble finding the correct algorithm to find the pet. If they are finding these levels confusing you can give them a hint like "Why don't you start by opening the present in the centre" and when they do ask them "What does the number you found tell you about all the numbers before it?" if the number is smaller than the one they are looking for, or "all the numbers after it?" if the number is bigger than the one they are looking for.

When students have finished ask them questions like "Where you able to find the pet even though you had less lives? What strategy did you use to find the pet?", we have found that many students will have ended up doing a binary search (or similar) without even knowing what a binary search is! Explaining these algorithms to students is likely to be easier now that they have seen them in action.
{panel end}

{panel type="curiosity" summary="How is Bozo search different from Linear search?"}
If you watched the video at the beginning of the chapter you might be thinking that what you did in the present searching game sounds more like Bozo Search than Linear Search, but actually Bozo Search is even sillier than this! If you were doing a Bozo Search then after unwrapping a present and finding a monster inside, you would wrap the present back up and try another one at random! This means you might end up checking the same present again and again and again and you might never find the pet, even with a small number of presents!
{panel end}

{panel type="teacher-note" summary="Teaching binary search with a phone book"}
The binary search algorithm can be demonstrated with a phone book or dictionary: choose a name, then open it at the *middle* page of the book (students might point out that you could guess how far through to open it, but insist on starting in the middle).
If you can spare the book, rip it in half at the chosen page, and ask the class which of the two halves contains the name (the ones before the middle, or the ones after).
If you don't have replacement books available, you can still proceed by just holding up the chosen half, but it will be more memorable for students when they see the problem literally divided in half.
Throw away the half that can't contain the name, pointing out that hundreds of pages have been eliminated by one decision. Repeat this on the remaining half, ripping that in half, then half again, and so on. On the board you can work out the number of pages left; for example, if there were 512 pages in the phone book, after the first rip there are 256, then 128, then 64, 32, 16, 89, 4, 2 and finally just one page. That's  9 pages that were examined to get down to the desired page. (Note that it's easiest to pick numbers that are powers of 2 i.e. 512, 1024, 2048, otherwise you have to deal with halving odd numbers, which works fine, but is a bit distracting).

The power of binary search becomes obvious when you ask how long it would take to search a book twice as large. The first rip on the larger book will reduce it to the original problem, so, for example, a book of 1024 pages requires 10 rips instead of the 9 used for 512 pages. A million page phone book (1,048,576 pages to be precise) is reduced to 1 page by only 20 rips (students will probably think that it will be a lot more, but they can work it out by halving 1,048,576 20 times). A billion pages requires only 30 rips - again, have students work this out for themselves, as it is surprising. You could point out that a billion-page phone book could hold every name in the world, and in fact a social network site could have a billion users on it, so searching for someone on a billion-user system could be done *by hand* looking at just 30 names. The catch? They need to be in sorted order, but sorting things into order is easy too if you use the right algorithm. (In practice large systems use a variation of this kind of searching, but this demonstrates how a very fast algorithm is possible on very large amounts of data, such as those used by search engines or social networks).
{panel end}

{panel type="spoiler" summary="How does doubling the number of boxes affect the number of checks required?"}
The answer to the above question is that the maximum number of checks for Linear Search would double, but the maximum number for Binary Search would only increase by one.
{panel end}

{panel type="project" summary="Code to   run linear and binary search for yourself"}
The following files will run linear and binary search in various languages; you can use them to generate random lists of values and measure how long they take to find a given value.
Your project is to measure the amount of time taken as the number of items (*n*) increases; try drawing a graph showing this.
- [Scratch](files/linear-binary-search-scratch.zip) - [Download Scratch here](https://scratch.mit.edu/scratch2download/)
- [Python (Version 2)](files/linear-binary-search-python2.py) - [Download Python 2 here](https://www.python.org/downloads/)
- [Python (Version 3)](files/linear-binary-search-python3.py) - [Download Python 3 here](https://www.python.org/downloads/)
{panel end}

{panel type="teacher-note" summary="Why are we also covering sorting?"}
Our main points have already been made --- what an algorithm is, how to estimate its cost, and that the cost isn't always proportional to the amount of data.
However, it's good to reinforce this with some different algorithms.
Sorting algorithms are useful to study because they illustrate many of the key issues that come up in algorithms, and there are some good contrasts, particularly between quicksort (which is fast and is widely used) and selection or insertion sort (which become very slow as the number of items sorted increases).
{panel end}

{panel type="teacher-note" summary="Answer for box analysis"}
For a list of 8 objects (like in the interactive) it should take 7 comparisons to find the lightest, 6 to find the next lightest, 5 to find the next, then 4, then 3, then 2, and then 1 to sort the final two boxes. In total this is 7+6+5+4+3+2+1 = 28 comparisons. If there had been 9 boxes it would have taken 8+7+6+5+4+3+2+1 = 36 comparisons. 20 boxes will take 190. Going from 1000 boxes up to 1001 will require 1000 extra comparisons, even though only 1 box has been added. Selection sort will always take
{math}(n\times(n-1))/2{math end} comparisons to sort *n* items into order.

For example: To calculate the number of comparisons required for 20 boxes, using {math}(n\times(n-1))/2{math end} where *n* = 20:

(20*(20-1))/2

= (20*19)/2

= 380/2

= 190 comparisons

Some students may recognise this formula as Gauss' trick (see [the anecdotes about Gauss on Wikipedia](https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss#Anecdotes). One way of expressing this trick for the above example is that 20 boxes would require summing the numbers 1+2+3+...+17+18+19. If we write the numbers backwards (19+18+17+...3+2+1) then it would be the same sum. Now if we add these two lists together, pairing up the corresponding numbers, we get (1+19)+(2+18)+(3+17)+...+(17+3)+(18+2)+(19+1). Each pair in this sum adds up to 20, and there are 19 pairs, so adding the two lists together is just 20x19. Since both lists add up to the same amount, the original sum is a half of that, or 20x19/2, which is 190 comparisons, which is what we got from the formula above. If students can follow this reasoning then they can easily work out the comparisons needed for a large number of boxes, and the don't have to use the "magic" formula given above. There's a visual explanation in [this video](http://www.numberphile.com/videos/one_to_million.html) and more examples on [this page](http://nzmaths.co.nz/gauss-trick-staff-seminar).
{panel end}

{panel type="teacher-note" summary="This section could be skipped"}
This algorithm is useful and commonly taught, although for the purpose of teaching the principles of algorithms, it's doesn't add a lot to what we've just covered with selection sort, so could be skipped.
However, if you have time, it's worth looking at for extra examples.
{panel end}

{panel type="project" summary="Code to run selection sort and quicksort for yourself"}
The following files will run selection sort and quicksort in various languages; you can use them to generate random lists of values and measure how long they take to be sorted.
Note how long these take for various amounts of input (*n*), and show it in a table or graph.
You should notice that the time taken by Quicksort is quite different to that taken by selection sort.
- [Scratch](files/selection-quicksort-scratch.zip) - [Download Scratch here](https://scratch.mit.edu/scratch2download/)
- [Python (Version 2)](files/selection-quicksort-python2.py) - [Download Python 2 here](https://www.python.org/downloads/)
- [Python (Version 3)](files/selection-quicksort-python3.py) - [Download Python 3 here](https://www.python.org/downloads/)
{panel end}

{panel type="curiosity" summary="Why are there so many different programming languages?"}
So if we know how to define an algorithm, why are there so many programming languages?
Programming languages are often created or adapted to express algorithms clearly for a specific problem domain.
For example, it is easier to read mathematical algorithms in Python than Scratch.
Similarly, data flow algorithms are clearer in visual programming languages like LabVIEW than Python.
{panel end}

{panel type="extra-for-experts" summary="Examples of Big O notation"}
Here are some Big O examples:
- {math}O(1){math end} - An algorithm with {math}O(1){math end} complexity will always execute in the same amount of time regardless of how much data you give it to process. For example, finding the smallest value in a sorted list is always easy.
- {math}O(n){math end} - The amount of time an algorithm with {math}O(n){math end} complexity will take to execute will increase roughly linearly with (i.e. in direct proportion to) the amount of data you give it to process. The high-score algorithm was {math}O(n){math end}, and so was the linear search.
- {math}O(n^{2}){math end} - The performance of an algorithm with this complexity is roughly proportional to the square of the size of the input data set. Selection sort and insertion sort take {math}O(n^{2}){math end} time. That's not very good value - 10 times the amount of input will take 100 times as long!
- {math}O(2^{n}){math end} - The amount of time an algorithm with this complexity will take to complete will double with each additional element added to the data set! We haven't seen these kinds of situations in this chapter, but they are common, and are a theme of the Complexity and Tractability chapter. Algorithms that are this slow can be almost impossible to use!
{panel end}
