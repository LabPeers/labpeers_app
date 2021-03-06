{% extends "base.html" %}
{% load staticfiles %}
{% load static %}

{% block content %}


<body class="w3-theme-l5">



<!-- Page Container -->
<div class="w3-container w3-content" style="max-width:1400px;margin-top:20px">    
  <!-- The Grid -->
  <div class="w3-row">
    <!-- Left Column -->
    <div class="w3-col m3">
      <!-- Profile -->
      <div class="w3-card w3-round w3-white">
        <div class="w3-container">
         <h4 class="w3-center">My Profile</h4>
         <!--<p class="w3-center"><img src="https://www.w3schools.com/w3images/avatar3.png" class="w3-circle" style="height:106px;width:106px" alt="Avatar"></p>-->
         <!--<p class="w3-center"><img src="{{ user.userprofile.image.url }}" class="w3-circle" style="height:106px;width:106px" alt=""></p>-->
         <!--<p class="w3-center"><img src="{% url image %}" class="w3-circle" style="height:106px;width:106px" alt=""></p>-->
         <!--
         <form method="post" action='' enctype="multipart/form-data">{% csrf_token %}
         {{ p_form }}
         <input type='submit' class='btn btn=default' value='Update profile picture' />
         </form>-->
         
         <!--<img src="{% static 'default.png' %}" alt="Hi!" style="width:170px;height:170px;border:0;"/>-->
         <!--<img src="{% static 'profile_pics/Foto_NikolaEgetenmeyer1.jpg' %}"/>-->
         <hr>
         <p><i class="fa fa-user-circle-o fa-fw w3-margin-right w3-text-theme"></i> Username: {{ user.username }}</p>
         <p><i class="fa fa-address-book-o fa-fw w3-margin-right w3-text-theme"></i> First name: {{ user.first_name }}</p>
         <p><i class="fa fa-address-book-o fa-fw w3-margin-right w3-text-theme"></i> Last name: {{ user.last_name }}</p>
         <p><i class="fa fa-envelope-o fa-fw w3-margin-right w3-text-theme"></i>Email: {{ user.email }}</p>
        </div>
      </div>
      <br>
      

      
      
      <!-- Alert Box -->
      <div class="w3-container w3-display-container w3-round w3-theme-l4 w3-border w3-theme-border w3-margin-bottom w3-hide-small">
        <span onclick="this.parentElement.style.display='none'" class="w3-button w3-theme-l3 w3-display-topright">
          <i class="fa fa-remove"></i>
        </span>
        <p><strong>Did you know?</strong></p>
        <p>You can edit or remove your current projects in your List of Projects!</p>
      </div>
    
    <!-- End Left Column -->
    </div>
    

    
  <!-- End Grid -->
  </div>
  
<!-- End Page Container -->
</div>
<br>


{% endblock %}
