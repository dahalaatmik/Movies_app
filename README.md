# Movies_app
### A Simple Flask application with learning how to make dynamic website / web app. 

This application would be cosidered more of a micro-web app, this app uses python modules like FlaskForms, flask_wtf, wtforms, flask_bootstraps, requests, sqlalchemy. 

This is a record-keeping application where you directly upload to the website rather than just your profile so that the whole world can see and make changes if they want. All you have to do it go to the webapp, click add movie and type the name of the movie that you want. After which it will ask you the choose the specific movie if chapters exist. Then it will ask you for a rating and your review on it. after pressing ok, it will pop in the home page with a photo of it, description, date of realease and more in a card format, which flips to reveal other details about the movie. and the cards are stacked vertically without overlapping among them.

This app is deployed on movies-app-ihis.onrender.com

There were serval obstacles that I had to face during the deployment of this App ( my first deployment tho ) : 
- Didn't add evn-vars in the render itself and tried get .evn-variables from the github .evn file which as in the .gitignore. Adding the .evn-variables in the Render platform itself caused no problem
- flask_bootstrap, bootstrap-flask etc etc. was confusing so fixed with the correct module
- fix the default port issue that was render's requirement to run the web-app on the internet
- Added csrf protection to the app so that flask, flaskforms and wtforms are csrf protected over the internet. 
