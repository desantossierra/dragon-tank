from flask import Flask

#configuration
app = Flask(__name__)
app.config.from_object('dragon.ui.config.Config')


from dragon.ui.web import routes