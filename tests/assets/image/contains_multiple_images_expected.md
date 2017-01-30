<p>Here's another FSA to consider:</p>
<div>{% load static %}
<a data-featherlight="image" data-featherlight-close-on-click="anywhere" href="{% static 'main/images/finite-state-automata-no-trap-example.png' %}">
  <img class="responsive-img" src="{% static 'main/images/finite-state-automata-no-trap-example.png' %}" />
</a>
</div>
<p>It's fairly clear what it will accept: strings like "ab", "abab", "abababababab", and, of course {math}\epsilon{math end}.
But there are some missing transitions: if you are in state 1 and get a "b" there's nowhere to go.
If an input cannot be accepted, it will be rejected, as in this case. We could have put in a trap state to make this clear:</p>
<div>{% load static %}
<a data-featherlight="image" data-featherlight-close-on-click="anywhere" href="{% static 'main/images/finite-state-automata-trap-added-example.png' %}">
  <img class="responsive-img" src="{% static 'main/images/finite-state-automata-trap-added-example.png' %}" />
</a>
</div>
<p>But things can get out of hand. What if there are more letters in the alphabet? We'd need something like this:</p>
<div>{% load static %}
<a data-featherlight="image" data-featherlight-close-on-click="anywhere" href="{% static 'main/images/finite-state-automata-trap-added-extreme-example.png' %}">
  <img class="responsive-img" src="{% static 'main/images/finite-state-automata-trap-added-extreme-example.png' %}" />
</a>
</div>
<p>So, instead, we just say that any unspecified transition causes the input to be rejected (that is, it behaves as though it goes into a trap state). In other words, it's fine to use the simple version above, with just two transitions.</p>