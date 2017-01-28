<p>Imagine we have the following simple black and white image.</p>
<div class="row">
<div class="content col s12 m8 offset-m2 center-align" content="">
<div>{% load static %}
<a data-featherlight="image" data-featherlight-close-on-click="anywhere" href="{% static 'main/images/pixel-diamond.png' %}">
  <img class="responsive-img" src="{% static 'main/images/pixel-diamond.png' %}" />
</a>
</div>
</div>
</div>
<p>One very simple way a computer can store this image in binary is by using a format where '0' means white and '1' means black (this is a "bit map", because we've mapped the pixels onto the values of bits). Using this method, the above image would be represented in the following way:</p>