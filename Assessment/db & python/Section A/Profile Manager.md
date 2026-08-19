Theme: Social Media Profile Manager

Section A: 
Conceptual Understanding

1. Explain the Django Request-Response cycle and how it differs from a standard Python script execution.

In a Social Media Profile Manager, when a user opens a profile, the browser sends a request to Django. Django checks the URL, runs the view, gets the profile details from the database, and shows the profile page to the user.

Difference: A normal Python program runs line by line and then stops. Django keeps running and waits for requests from users. When it gets a request, it processes it and sends a response.

===================================================================================

2. Explain why Django Model Fields (CharField, IntegerField) are more robust for profile data than Python dynamic typing.

Django Model Fields like CharField and IntegerField are useful for storing profile data because they define the correct type of data.

For example, in a Social Media Profile Manager, we can use CharField for username and IntegerField for age.

They also provide validation and help keep the database data organized.

Difference: Python dynamic typing allows a variable to store different types of values, but Django Model Fields provide a fixed data type and better data control.

===================================================================================

3. Explain how Django Forms handle automated input validation for usernames and age ranges.

In a Social Media Profile Manager, Django Forms automatically check whether the user enters valid data.

For example, it can check that the username is not empty and the age is within a valid range, such as 18 to 100.

If the data is wrong, Django shows an error message and asks the user to correct it.

In short: Django Forms make input validation easy and reduce the need to write validation code manually.

===================================================================================

4. Explain how to implement conditional logic in Django Templates to toggle account visibility.

In a Social Media Profile Manager, we can use Django's {% if %} condition to check whether an account is public or private.

For example, if the account is public, we show the profile details. If it is private, we show "This account is private."

{% if profile.is_public %}
    <p>Profile is Public</p>
{% else %}
    <p>This account is Private</p>
{% endif %}

In short: Django Template {% if %} is used to show different content based on the account's visibility.

==================================================================================

5. Explain the difference between iterating through a Python list and a Django QuerySet.

A Python list stores data directly in memory, while a Django QuerySet gets data from the database using Django ORM.

For example, a Python list can contain profile names, while a QuerySet can contain profiles fetched from the database.

In short: A list is used for normal Python data, while a QuerySet is used to work with database data.

===================================================================================

6. Explain why the Django ORM is preferred over Python dictionaries for persistent profile storage.

In a Social Media Profile Manager, Django ORM is preferred because it stores profile data permanently in a database.

A Python dictionary stores data temporarily in memory, so the data can be lost when the program stops.

Django ORM also makes it easy to add, update, delete, and search profile data.

In short: Django ORM is better for permanent profile storage, while a dictionary is mainly useful for temporary data.

===================================================================================