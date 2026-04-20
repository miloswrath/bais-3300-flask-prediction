Create a new flask app for the front end
Create a new Flask web application to serve web pages (use a templates folder and base.html & index.html) 

On index.html create a web form that collects user input using drop downs for each option.

Set the form action to /predict and the method to POST

Set each input as required.

Set an empty value with the text to choose a value.

In app.py, edit the api_url variable to point to your API server running on Azure that you have previously created.


Run your ML API on Azure
Replace your requirements.txt file with this:

Flask==3.1.0
flask-cors==5.0.1
joblib==1.4.2
scikit-learn==1.6.1
gunicorn  
Using Thunderclient, connect to your API server running on your laptop. Pass the same variable values you used to test your .pkl file locally. You should receive back the same value you received when it ran locally.

 

Test your front end app on your local laptop
Run your front end application on your local laptop.

Are all of your fields required? Do they each return a required indicator if it is not selected?

Do the numeric values and category names match for each of your inputs? You will need to manually review your HTML code and the map you created when building an API server (notes.txt).

Do each of your inputs have an empty value with text to make a choice?

Is a predicted salary returned when you enter selections in your form?

Does the predicted salary in this web form match the predicted salary returned using Thunderclient?

 

Format your front end application using Bootstrap 5.3
For a more aesthetic and responsive application, let's use Bootstrap 5.3. You can manually code it using the Bootstrap documentation and your previous Bootstrap assignment. Or you can use Chat or other AI to style it with Bootstrap. Just make sure to specify Bootstrap 5.3. Some of the returned code like links to CSS and JS will go in base.html and the actual form styling tags will go in index.html.

After you have it working, perform all of the above tests as well as test it for responsiveness when your resize your browser window.

 

Put your front end application on Azure
When your front end application is appropriately styled and working correctly, put it on Azure.

After it is loaded on Azure, visit your frontend application using the url on the Overview page.

Run your tests again.

 

Deliverables
Upload the URL of your front end application running on Azure.

Upload the URL to your GitHub repository for your front end application.

Upload the URL to your GitHub repository for your API server.
