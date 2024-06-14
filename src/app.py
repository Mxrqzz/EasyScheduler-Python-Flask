'''Arquivo as rotas são definidas'''

from flask import Flask
from src.routes.routes import routes

app = Flask(__name__)
app.secret_key = '7355608'
app.config['UPLOAD_FOLDER'] = 'static/uploads'


app.add_url_rule(routes["index_route"], view_func=routes["index"])

app.add_url_rule(routes["register_route"], view_func=routes["register"])

app.add_url_rule(routes["formClient_route"], view_func=routes["formClient"])

app.add_url_rule(routes["formPro_route"], view_func=routes["formPro"])

app.add_url_rule(routes["login_route"], view_func=routes["login"])

app.add_url_rule(routes["logout_route"], view_func=routes["logout"])

app.add_url_rule(routes["dashboardClient_route"], view_func=routes["dashboardClient"])

app.add_url_rule(routes["dashboardPro_route"], view_func=routes["dashboardPro"])

app.add_url_rule(routes["perfilCliente_route"], view_func=routes["perfilCliente"])

app.add_url_rule(routes["perfilPro_route"], view_func=routes["perfilPro"])

app.add_url_rule(routes["updateUserC_route"], view_func=routes["updateUserC"])

app.add_url_rule(routes["updateUserP_route"], view_func=routes["updateUserP"])

app.add_url_rule(routes["services_route"], view_func=routes["services"])

app.add_url_rule(routes["horarios_route"], view_func=routes["horarios"])

app.add_url_rule(routes["agendamento_route"], view_func=routes["agendamento"])

