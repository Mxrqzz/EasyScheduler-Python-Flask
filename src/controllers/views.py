'''Arquivo responsavel pelas classes e funções'''

import os
from flask import session, render_template, redirect, request, jsonify, abort, current_app as app
from flask.views import MethodView
from pymysql import MySQLError, IntegrityError
from werkzeug.utils import secure_filename

from src.database import bancoBT


class Index(MethodView):
    """
    Classe para manipular requisições relacionadas a pagina inicial
    Essa classe herda de MethodView, permintindo que ela seja usada com uma view
    em um aplicativo Flask

    Métodos:
    - get() Método para lidar com requisições GET para a pagina inicial

    """

    def get(self):
        """
        Manipula requisições GET para a pagina inicial.

        Retorna:
        render_template: Uma renderização do template 'public/index.html'
        """
        return render_template('public/index.html')


class Register(MethodView):
    """
     Classe para manipular requisições relacionadas a pagina de escolha do tipo de conta
     Essa classe herda de MethodView, permintindo que ela seja usada com uma view
     em um aplicativo Flask

     Métodos:
     - get() Método para lidar com requisições GET para a pagina de escolha do tipo de conta

     """

    def get(self):
        """
        Manipula requisições GET para a pagina de escolha do tipo de conta que deseja criar.

        Retorna:
        render_template: Uma renderização do template 'public/index.html'
        """
        return render_template('public/register.html')


class FormClient(MethodView):
    """
    Classe para manipular requisições relacionadas a pagina de formulario cliente
    Essa classe herda de MethodView, permintindo que ela seja usada com uma view
    em um aplicativo Flask

    Métodos:
    - get() Método para lidar com requisições GET para a pagina de formulario do cliente
    - post() Método para lidar com requisições POST do formulário de cliente
    """

    def get(self):
        """
        Manipula requisições GET para a pagina de formulario do cliente.

        Retorna:
        render_template: Uma renderização do template 'public/cliente/registerCliente.html'
        """
        return render_template('public/cliente/form.html')

    def post(self):
        """
        Manipula requisições POST para o formulário de cliente.

        Retorna:
        redirect: Redireciona para a página inicial após o registro ou exibe uma mensagem de erro.
        """
        # Obtém dados do formulário
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')

        # Verifica se o email já está cadastrado como cliente
        cursor = bancoBT.cursor()
        try:
            cursor.execute("SELECT * FROM cliente WHERE email = %s", (email,))
            existing_client = cursor.fetchone()
            if existing_client:
                cursor.close()
                return jsonify({"error": "Email ja cadastrado. Por favor utilize outro"})
        except MySQLError:
            bancoBT.rollback()
            cursor.close()
            abort(500)

        # Verifica se o email já está cadastrado como profissional
        cursor = bancoBT.cursor()
        try:
            cursor.execute(
                "SELECT * FROM profissional WHERE email = %s", (email,))
            existing_pro = cursor.fetchone()
            if existing_pro:
                cursor.close()
                return jsonify({"error": "Email ja cadastrado. Por favor utilize outro"})
        except MySQLError:
            bancoBT.rollback()
            cursor.close()
            abort(500)

        # Se o e-mail não estiver cadastrado em nenhuma das tabelas, inserir o novo registro
        try:
            cursor.execute("INSERT INTO cliente (nome, sobrenome, email, senha)"
                           "VALUES (%s, %s, %s, %s)",
                           (name, lastname, email, password))
            bancoBT.commit()
            cursor.close()
            return redirect('/')
        except IntegrityError:
            bancoBT.rollback()
            cursor.close()
            return jsonify({"error": "Falha ao cadastrar cliente, verifique os dados fornecidos."})
        except MySQLError:
            bancoBT.rollback()
            cursor.close()
            abort(500)  # Erro interno do servidor


class FormPro(MethodView):
    """
    Classe para manipular requisições relacionadas a pagina de formulario profissional
    Essa classe herda de MethodView, permintindo que ela seja usada com uma view
    em um aplicativo Flask

    Métodos:
    - get() Método para lidar com requisições GET para a pagina de formulario do profissional
    - post() Método para lidar com requisições POST do formulário de profissional
    """

    def get(self):
        """
        Manipula requisições GET para a pagina de formulario do profissional.

        Retorna:
        render_template: Uma renderização do template'public/profissional/registerprofissional.html'
        """
        return render_template('public/pro/form.html')

    def post(self):
        """
        Manipula requisições POST para o formulário de profissional.

        Retorna:
        redirect: Redireciona para a página inicial após o registro ou exibe uma mensagem de erro.
        """
        # Obtém dados do formulário
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')

        # Verifica se o email já está cadastrado como profissional
        cursor = bancoBT.cursor()
        try:
            cursor.execute("SELECT * FROM cliente WHERE email = %s", (email,))
            existing_client = cursor.fetchone()
            if existing_client:
                cursor.close()
                return jsonify({"error": "Email ja cadastrado. Por favor utilize outro"})
        except MySQLError:
            bancoBT.rollback()
            cursor.close()
            abort(500)

        # Verifica se o email já está cadastrado como profissional
        cursor = bancoBT.cursor()
        try:
            cursor.execute(
                "SELECT * FROM profissional WHERE email = %s", (email,))
            existing_pro = cursor.fetchone()
            if existing_pro:
                cursor.close()
                return jsonify({"error": "Email ja cadastrado. Por favor utilize outro"})
        except MySQLError:
            bancoBT.rollback()
            cursor.close()
            abort(500)

        # Se o e-mail não estiver cadastrado em nenhuma das tabelas, inserir o novo registro
        try:
            cursor.execute("INSERT INTO profissional (nome, sobrenome, email, senha)"
                           "VALUES (%s, %s, %s, %s)",
                           (name, lastname, email, password))
            bancoBT.commit()
            cursor.close()
            return redirect('/')
        except IntegrityError:
            bancoBT.rollback()
            cursor.close()
            return jsonify({"error": "Falha ao cadastrar pro, verifique os dados fornecidos."})
        except MySQLError:
            bancoBT.rollback()
            cursor.close()
            abort(500)  # Erro interno do servidor


class Login(MethodView):
    """
    Classe para manipular requisições relacionadas a pagina de login
    Essa classe herda de MethodView, permintindo que ela seja usada com uma view
    em um aplicativo Flask
    Métodos:
    - get() Método para lidar com requisições GET para a pagina de login
    """

    def get(self):
        """
        Manipula requisições GET para a pagina de login
        Retorna:
        render_template: Uma renderização do template 'public/login.html'
        """
        return render_template('public/login.html')

    def post(self):
        """
        Manipula requisições POST do formulário de login.
        Retorna:
        redirect: Redireciona para a página de dashboard se o login for bem-sucedido,
        caso contrário, redireciona para a página de login com uma mensagem de erro.
        """
        email = request.form.get('email')
        senha = request.form.get('password')

        # verificar se o email e a senha corresponde ao usuario no banco de dados
        cursor = bancoBT.cursor()
        cursor.execute(
            "SELECT * FROM cliente WHERE email = %s AND senha = %s", (email, senha))
        cliente_data = cursor.fetchone()

        error = ""

        if cliente_data:

            cliente = {
                "id": cliente_data[0],
                "nome": cliente_data[1],
                "sobrenome": cliente_data[2],
                "email": cliente_data[3],
            }

            # inicia sessão do cliente
            session['cliente_id'] = cliente['id']
            return redirect('/dashboardClient')

        cursor.execute(
            "SELECT * FROM profissional WHERE email = %s AND senha = %s", (email, senha))
        profissional_data = cursor.fetchone()

        if profissional_data:

            profissional = {
                "id": profissional_data[0],
                "nome": profissional_data[1],
                "sobrenome": profissional_data[2],
                "email": profissional_data[3],
            }

            session['profissional_id'] = profissional['id']
            return redirect('/dashboardPro')
        cursor.close()

        error = "Credenciais inválidas. Por favor, verifique seu email e senha."
        return render_template('public/login.html', error=error)


class Logout(MethodView):
    '''Classe responsável por fazer o logout da conta'''

    def get(self):
        '''função responsavel por limpar os dados da sessao e realizar o logout'''
        # limpa os dados da sessao
        session.clear()
        # redireciona para a tela de login
        return redirect('/login')


# SEM CONTROLE DE SESSAO
class DashboardClient(MethodView):
    """
    Classe para manipular requisições relacionadas a pagina inicial do cliente
    Essa classe herda de MethodView, permintindo que ela seja usada com uma view
    em um aplicativo Flask
    Métodos:
    - get() Método para lidar com requisições GET para a pagina inicial do cliente
    """

    def get(self):
        """
        Manipula requisições GET para a pagina inicial do cliente.
        Retorna:
        render_template: Uma renderização do template 'public/cliente/dashboard.html'
        """
        try:
            with bancoBT.cursor() as cursor:
                # Buscar todos os serviços
                cursor.execute(
                    "SELECT s.titulo, s.preco, s.tempo, s.descricao, p.nome, p.sobrenome "
                    "FROM servico s "
                    "JOIN profissional p ON s.profissional_id = p.id"
                )
                services = cursor.fetchall()

                # Buscar todos os profissionais
                cursor.execute(
                    "SELECT id, nome, sobrenome FROM profissional"
                )
                pro = cursor.fetchall()

            return render_template(
                'public/cliente/dashboard.html', services=services, pro=pro
            )
        except MySQLError as e:
            abort(500, description=str(e))


# SEM CONTROLE DE SESSAO
class DashboardPro(MethodView):
    """
    Classe para manipular requisições relacionadas a pagina inicial do profissional
    Essa classe herda de MethodView, permintindo que ela seja usada com uma view
    em um aplicativo Flask
    Métodos:
    - get() Método para lidar com requisições GET para a pagina inicial do profissional
    """

    def get(self):
        """
        Manipula requisições GET para a pagina inicial do profissional.
        Retorna:
        render_template: Uma renderização do template 'public/pro/dashboard.html'
        """
        return render_template('public/pro/dashboard.html')


class PerfilCliente(MethodView):
    """
    Classe para manipular requisições relacionadas a pagina de perfil do cliente
    Essa classe herda de MethodView, permintindo que ela seja usada com uma view
    em um aplicativo Flask
    Métodos:
    - get() Método para lidar com requisições GET para a pagina de perfil do cliente
    """

    def get(self):
        """
        Manipula requisições GET para a pagina perfil do cliente.
        Retorna:
        render_template: Uma renderização do template 'public/cliente/perfil.html'
        """
        cliente_id = session.get('cliente_id')
        if cliente_id:
            cursor = bancoBT.cursor()
            cursor.execute(
                "SELECT nome, sobrenome, email, photo FROM cliente WHERE id = %s", (cliente_id,))
            cliente_data = cursor.fetchone()
            cursor.close()

            if cliente_data:
                nome = cliente_data[0]
                sobrenome = cliente_data[1]
                email = cliente_data[2]
                photo = cliente_data[3] or 'https://via.placeholder.com/200'

                return render_template('public/cliente/perfil.html',
                                       id=cliente_id, nome=nome, sobrenome=sobrenome,
                                       email=email, photo=photo)
            else:
                return redirect('/login')
        else:
            return redirect('/login')


# SEM CONTROLE DE SESSAO
class UpdateUserC(MethodView):
    '''Classe responsável por atualizar dados do usuario'''

    def post(self):
        '''Função que altera nome, sobrenome e foto do cliente'''
        cliente_id = session.get('cliente_id')
        if not cliente_id:
            return redirect('/login')

        nome = request.form.get('name')
        sobrenome = request.form.get('lastname')
        photo = request.files.get('photo')

        cursor = bancoBT.cursor()

        try:
            if not nome or not sobrenome:
                cursor.execute(
                    "SELECT nome, sobrenome FROM cliente WHERE id = %s", (cliente_id))
                cliente_data = cursor.fetchone()
                if cliente_data:
                    if not nome:
                        nome = cliente_data[0]
                    if not sobrenome:
                        sobrenome = cliente_data[1]

                # verifica se o arquivo foi enviado
                if photo:
                    filename = secure_filename(photo.filename)
                    photo.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], filename))
                    photo_path = os.path.join(
                        app.config['UPLOAD_FOLDER'], filename)
                else:
                    photo_path = None

                cursor.execute(
                    "UPDATE cliente SET nome = %s, sobrenome = %s, photo=%s WHERE id = %s",
                    (nome, sobrenome, photo_path, cliente_id)
                )
            else:
                cursor.execute(
                    "UPDATE cliente SET nome = %s, sobrenome =%s, WHERE id = %s",
                    (nome, sobrenome, cliente_id)
                )
            bancoBT.commit()
            return redirect('/perfilCliente')
        except (MySQLError, IntegrityError) as db_error:
            bancoBT.rollback()
            abort(500, description=str(db_error))
        except (IOError, OSError) as file_error:
            bancoBT.rollback()
            abort(500, description=str(file_error))
        finally:
            cursor.close()


class PerfilPro(MethodView):
    """
    Classe para manipular requisições relacionadas a pagina de perfil do profissional
    Essa classe herda de MethodView, permintindo que ela seja usada com uma view
    em um aplicativo Flask
    Métodos:
    - get() Método para lidar com requisições GET para a pagina de perfil do profissional
    """

    def get(self):
        """
        Manipula requisições GET para a pagina inicial do profissional.
        Retorna:
        render_template: Uma renderização do template 'public/pro/perfil.html'
        """
        pro_id = session.get('profissional_id')
        if pro_id:
            cursor = bancoBT.cursor()
            cursor.execute(
                "SELECT nome, sobrenome, email, photo FROM profissional WHERE id = %s",
                (pro_id,))
            pro_data = cursor.fetchone()
            cursor.close()

            if pro_data:
                nome = pro_data[0]
                sobrenome = pro_data[1]
                email = pro_data[2]
                photo = pro_data[3] or 'https://via.placeholder.com/200'

                return render_template(
                    'public/pro/perfil.html', id=pro_id, nome=nome,
                    sobrenome=sobrenome, email=email, photo=photo
                )
            else:
                return redirect('/login')
        else:
            return redirect('/login')


# SEM CONTROLE DE SESSAO
class UpdateUserP(MethodView):
    '''
    Classe responsável por atualizar dados do usuario
    '''

    def post(self):
        '''
        Função que altera nome, sobrenome e foto do profissional
        '''
        pro_id = session.get('profissional_id')
        if not pro_id:
            return redirect('/login')

        nome = request.form.get('name')
        sobrenome = request.form.get('lastname')
        photo = request.files.get('photo')

        cursor = bancoBT.cursor()

        try:
            if not nome or not sobrenome:
                cursor.execute(
                    "SELECT nome, sobrenome FROM profissional WHERE id = %s", (pro_id))
                pro_data = cursor.fetchone()
                if pro_data:
                    if not nome:
                        nome = pro_data[0]
                    if not sobrenome:
                        sobrenome = pro_data[1]

                # verifica se o arquivo foi enviado
                if photo:
                    filename = secure_filename(photo.filename)
                    photo.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], filename))
                    photo_path = os.path.join(
                        app.config['UPLOAD_FOLDER'], filename)
                else:
                    photo_path = None

                cursor.execute(
                    "UPDATE profissional SET nome = %s, sobrenome = %s, photo=%s WHERE id = %s",
                    (nome, sobrenome, photo_path, pro_id)
                )
            else:
                cursor.execute(
                    "UPDATE profissional SET nome = %s, sobrenome =%s, WHERE id = %s",
                    (nome, sobrenome, pro_id)
                )
            bancoBT.commit()
            return redirect('/perfilPro')
        except (MySQLError, IntegrityError) as db_error:
            bancoBT.rollback()
            abort(500, description=str(db_error))
        except (IOError, OSError) as file_error:
            bancoBT.rollback()
            abort(500, description=str(file_error))
        finally:
            cursor.close()


class Services(MethodView):
    '''
    Classe responsável pelo cadastro de Serviços do profissional
    '''

    def get(self):
        '''
        Função que realiza a renderização do service.html
        '''
        pro_id = session.get('profissional_id')
        if pro_id:
            with bancoBT.cursor() as cursor:
                cursor.execute(
                    "SELECT nome, sobrenome FROM profissional WHERE id = %s",
                    (pro_id,)
                )
                pro_data = cursor.fetchone()

                cursor.execute(
                    "SELECT titulo, preco, tempo,descricao FROM servico WHERE profissional_id = %s",
                    (pro_id)
                )
                services = cursor.fetchall()

            if pro_data:
                nome = pro_data[0]
                sobrenome = pro_data[1]

                return render_template(
                    'public/pro/service.html', id=pro_id, nome=nome, sobrenome=sobrenome,
                    services=services
                )
            else:
                return redirect('/login')
        else:
            return redirect('/login')

    def post(self):
        """
        Função que manipula as requisições POST para o formulário de serviços.

        Retorna:
        redirect: Redireciona para a página de serviços após a inserção
        ou exibe uma mensagem de erro.
        """
        # Obtém dados do formulário
        titulo = request.form.get('service')
        preco = request.form.get('price')
        tempo = request.form.get('time')
        descricao = request.form.get('description')
        profissional_id = request.form.get('profissional_id')

        # Verifica se todos os campos necessários foram preenchidos
        if not all([titulo, preco, tempo, descricao, profissional_id]):
            return jsonify({"error": "Todos os campos são obrigatórios."})

        try:
            with bancoBT.cursor() as cursor:
                # Insere o novo serviço no banco de dados
                cursor.execute(
                    "INSERT INTO servico (titulo, preco, tempo, descricao, profissional_id) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (titulo, preco, tempo, descricao, profissional_id)
                )
                bancoBT.commit()
            return redirect('/services')
        except IntegrityError as e:
            bancoBT.rollback()
            return jsonify({"error": f"Erro de integridade: {str(e)}"})
        except MySQLError as e:
            bancoBT.rollback()
            return jsonify({"error": f"Falha ao cadastrar serviço, erro do MySQL: {str(e)}"})
        except Exception as e:
            bancoBT.rollback()
            return jsonify({"error": f"Erro inesperado: {str(e)}"})


class Horarios(MethodView):
    '''Classe horarios'''

    def get(self):
        """
        Manipula requisições GET para a pagina de horarios do profissionais.

        Retorna:
        render_template: Uma renderização do template 'public/pro/horarios.html'
        """
        return render_template('public/pro/horarios.html')
    
    def post(self):
        '''
        pega os dados dos horarios
        '''
        