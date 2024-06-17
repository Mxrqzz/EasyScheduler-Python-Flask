'''Arquivo responsável pelo Dicionario de rotas'''

from src.controllers.views import (
    Index, Register, FormClient, FormPro, Login, Logout, DashboardClient, DashboardPro,
    PerfilCliente, PerfilPro, UpdateUserC, UpdateUserP, Services, Horarios, Agendamento,
    Agenda,
)

index = Index.as_view('index')
register = Register.as_view('register')
formClient = FormClient.as_view('formClient')
formPro = FormPro.as_view('formPro')
login = Login.as_view('login')
logout = Logout.as_view('logout')
dashboardClient = DashboardClient.as_view('dashboardClient')
dashboardPro = DashboardPro.as_view('dashboardPro')
perfilCliente = PerfilCliente.as_view('perfilCliente')
perfilPro = PerfilPro.as_view('perfilPro')
updateUserC = UpdateUserC.as_view('updateUserC')
updateUserP = UpdateUserP.as_view('updateUserP')
services = Services.as_view('services')
horarios = Horarios.as_view('horarios')
agendamento = Agendamento.as_view('agendamento')
agenda = Agenda.as_view('agenda')


routes = {
    "index_route": "/",
    "index": index,

    "register_route": "/register",
    "register": register,

    "formClient_route": "/formClient",
    "formClient": formClient,

    "formPro_route": "/formPro",
    "formPro": formPro,

    "login_route": "/login",
    "login": login,

    "logout_route": "/logout",
    "logout": logout,

    "dashboardClient_route": "/dashboardClient",
    "dashboardClient": dashboardClient,

    "dashboardPro_route": "/dashboardPro",
    "dashboardPro": dashboardPro,

    "perfilCliente_route": "/perfilCliente",
    "perfilCliente": perfilCliente,

    "perfilPro_route": "/perfilPro",
    "perfilPro": perfilPro,

    "updateUserC_route": "/updateUserC",
    "updateUserC": updateUserC,

    "updateUserP_route": "/updateUserP",
    "updateUserP": updateUserP,

    "services_route": "/services",
    "services": services,

    "horarios_route": "/horarios",
    "horarios": horarios,

    "agendamento_route": "/agendamento",
    "agendamento": agendamento,

    "agenda_route": "/agenda",
    "agenda": agenda,

}
