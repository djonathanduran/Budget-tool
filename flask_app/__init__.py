from flask import Flask, app
app = Flask(__name__)

app.secret_key = "thisistheseceretkey"
