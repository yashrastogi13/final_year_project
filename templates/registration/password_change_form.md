{% extends 'base.html' %}

{% block content %}
    <div style="padding-left: 20px;">
        <h1>Password change</h1>
        <p>
            Please enter your old password, for security's sake, and then enter your
            new password twice so we can verify you typed it in correctly.
        </p>
        <form method="POST">
            {% csrf_token %}
            {{form.as_p}}
            <button type="Submit" class="btn btn-dark">Change my password</button>
        </form>
    </div>
{% endblock content %}
