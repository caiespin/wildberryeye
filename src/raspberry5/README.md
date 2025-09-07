# WildBerryEye
This project contains both frontend and backend. The user should open two terminals for running frontend and backend seperately.
## In the Backend
- Create your venv with system packages enabled:
` $ python3 -m venv --system-site-packages venv `

- Activate it:
`$ source venv/bin/activate`

- Install Pacakes
`$ pip install -r requirements.txt`

- Run Flask App
`$ python3 app.py`

### Backend Default Port: 5000

## In the Frontend
- Install nvm:

`$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash`
`$ source ~/.bashrc`

- Install Node package (version > node.20+)

`$ nvm install node`

- Set it as default
`$ nvm alias default node`
- Check Version
` $ node -v`
` $ npm -v`

- Install all Packages
`$ npm install`

- Run
`$ npm start`

### Frontend Default port: 3000

## Edit the IP Address in the Code Package

Change the IP address in those files with your local IP Address:

backend/app.py: line 184(host)

frontend/components/Calendar.js
 - line 13 & 22 (fetch)

frontend/components/ImageCapture.js
 - line 11 & 18 (downloadUrl)

frontend/components/VideoCapture.js
 - line 13, 24 & 29 (fetch)
