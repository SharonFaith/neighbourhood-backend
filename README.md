# NEIGHBOURHOOD 
#### Live-Link
https://neighbourhood-back.herokuapp.com/api/users/
### Description:
This a Neighbourhood Web Application that provides a platform for residents of various neighbourhoods to interact with each other, and keep abreast of current activities in their neighbourhoods.
#### BDD As a User:
* First Sign in with the application to start using it.
* Receive a Email confirming signing up.
* Be able to specify a specific neighborhood.
* Access services offered in a selected neighborhood.
* Create Posts the neighborhood.
* Only view details of a single neighborhood.

### Contributors/Authors:
* Victor Maina(Scrum Master)
* Sharon Olago
* Jeffrey Mwai
* Martin Mandina

### Installation Technologies Required:
* Django
* Python
* Virtual environment

### SETUP & INSTALLATION INSTRUCTIONS:
 * Ensure that Python3.6 is installed.
 * Open Terminal.
 * Change working directory to preferred location where you want to clone directory.
 * Create a virtual environment on your working directory.
 * Switch to the virtual environment by command ```source <your virtual name>/bin/activate``` on the terminal. 
 * Install django and depedencies listed in the ```requirements.txt```
  * Create a .env file and add own credentials where appropriate

```
SECRET_KEY = '<Secret_key>'
DB_NAME = 'ProjectApp'
DB_USER = '<Username>'
DB_PASSWORD = '<password>'
DEBUG=False
DB_HOST='127.0.0.1'
MODE='dev' 
ALLOWED_HOSTS='*'
DISABLE_COLLECTSTATIC=1
EMAIL_USE_TLS=True
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='<email to send confirmation message>'
EMAIL_HOST_PASSWORD='<email password>'
CLOUD_NAME='<your cloud name>'
CLOUDINARY_API_KEY='<your cloud api_key>'
CLOUDINARY_API_SECRET='<your cloud api_secret>'
SENDGRID_API_KEY="<your sendgrid api_key>"
SENDGRID_EMAIL_ADDRESS='<your sendgrid email_address>'
```
* Lastly open the application on your browser by running python3 manage.py runserver

#### TECHNOLOGIES:
* Python3
* postgresql
* Django
* Bootstrap4
* CSS
* Heroku
* Django restframework
* djangorestframework-simplejwt

#### DEPENDECIES
* gunicorn
* Pillow
* cloudinary
* netlify

### CONTACT INFORMATION
1. Victor Maina 
* vk13runic@gmail.com
2. Sharon Olago
* sharonfaith15@gmail.com
3. Jeffrey Mwai
* jeffmwai3@gmail.com
4. Martin Mandina
* martinsmandina@gmail.com

#### License  & Copyright information
Copyright (c) 2020 **Victor Maina,Sharon Olago,Jeffrey Mwai,Martin Mandina,

[MIT License](./LICENSE)
<<<<<<< HEAD





  


=======
>>>>>>> 3ba96c5002929f9b28b0aa1251de0dd8acd9677e
