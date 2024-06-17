'''Arquivo responsavel pelas classes e funções'''

from datetime import datetime
from flask import session, render_template, redirect, request, jsonify, abort
from flask.views import MethodView
from pymysql import MySQLError, IntegrityError

from src.database import bancoBT


class Index(MethodView):
    """
    Classe responsavel pelas requisições da pagina inicial
    """

    def get(self):
        """
        renderiza o arquivo index.html
        """
        return render_template('public/index.html')


class Register(MethodView):
    """
    Classe responsavel pelas requisições da pagina do tipo de conta do usuario
    """

    def get(self):
        """
        renderiza o arquivo register.html
        """
        return render_template('public/register.html')


class FormClient(MethodView):
    """
    Classe para manipular requisições relacionadas a pagina de formulario cliente
    """

    def get(self):
        """
        Renderiza o arquivo cliente/form.html
        """
        return render_template('public/cliente/form.html')

    def post(self):
        """
        adiciona dados no banco de dados
        """
        # Obtém dados do formulário
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
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

        # Se o e-mail não estiver cadastrado, insere o novo registro
        try:
            cursor.execute("INSERT INTO cliente (nome, sobrenome,telefone, email, senha)"
                           "VALUES (%s, %s, %s, %s, %s)",
                           (name, lastname, phone, email, password))
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
    Classe para manipular requisições relacionadas a pagina de formulario cliente
    """

    def get(self):
        """
        Renderiza o arquivo pro/form.html
        """
        return render_template('public/pro/form.html')

    def post(self):
        """
        adiciona dados no banco de dados
        """
        # Obtém dados do formulário
        name = request.form.get('name')
        category = request.form.get('category')
        phone = request.form.get('phone')
        endereco = request.form.get('endereco')
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
            cursor.execute(
                "INSERT INTO profissional (nome, categoria, email, senha, telefone, endereco)"
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (name, category, email, password, phone, endereco))
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
    """

    def get(self):
        """
        Renderiza o arquivo public/login.html
        """
        return render_template('public/login.html')

    def post(self):
        """
        Confere se os dados de login existe no banco de dados.
        """
        email = request.form.get('email')
        senha = request.form.get('password')

        # verificar se o email e a senha corresponde ao usuario no banco de dados
        cursor = bancoBT.cursor()
        cursor.execute(
            "SELECT id, nome, sobrenome, email FROM cliente "
            "WHERE email = %s AND senha = %s", (email, senha))
        cliente_data = cursor.fetchone()

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
            "SELECT id, nome, categoria, email FROM profissional "
            "WHERE  email = %s AND senha = %s", (email, senha))
        profissional_data = cursor.fetchone()

        if profissional_data:

            profissional = {
                "id": profissional_data[0],
                "nome": profissional_data[1],
                "categoria": profissional_data[2],
                "email": profissional_data[3],
            }

            session['profissional_id'] = profissional['id']
            return redirect('/dashboardPro')
        cursor.close()

        error = "Credenciais inválidas. Por favor, verifique seu email e senha."
        return render_template('public/login.html', error=error)


class Logout(MethodView):
    '''
    Classe responsável por fazer o logout da conta
    '''

    def get(self):
        '''
        função responsavel por limpar os dados da sessao e realizar o logout
        '''
        # limpa os dados da sessao
        session.clear()
        # redireciona para a tela de login
        return redirect('/login')


class DashboardClient(MethodView):
    """
    Classe para manipular requisições relacionadas ao Dashboard do cliente
    """

    def get(self):
        """
        Renderiza o arquivo 'public/cliente/dashboard.html' e puxa dados do Banco de dados
        para ja renderizar a pagina com esses dados carregados
        """
        # controle de sessão
        cliente_id = session.get('cliente_id')

        if not cliente_id:
            session.clear()
            return redirect('/login')

        try:
            with bancoBT.cursor() as cursor:
                # Buscar todos os serviços
                cursor.execute(
                    "SELECT s.id, s.titulo, s.preco, s.tempo,"
                    "s.descricao,p.id,p.id, p.nome, p.categoria "
                    "FROM servico s "
                    "JOIN profissional p ON s.profissional_id = p.id"
                )
                services = cursor.fetchall()

                # Buscar todos os profissionais
                cursor.execute(
                    "SELECT id, nome, categoria FROM profissional"
                )
                pro = cursor.fetchall()

            return render_template(
                'public/cliente/dashboard.html', services=services, pro=pro
            )
        except MySQLError as e:
            abort(500, description=str(e))


class DashboardPro(MethodView):
    """
    Classe para manipular requisições relacionadas ao Dashboard do Profissional
    """

    def get(self):
        """
        Renderiza o arquivo 'public/pro/dashboard.html' e puxa dados do Banco de dados
        para ja renderizar a pagina com esses dados carregados
        """
        profissional_id = session.get('profissional_id')

        if not profissional_id:
            session.clear()
            return redirect('/login')

        query = """
        SELECT
            a.data_agendamento,
            c.nome AS cliente_nome,
            c.sobrenome AS cliente_sobrenome,
            c.telefone AS cliente_telefone,
            s.titulo AS servico_titulo,
            s.tempo AS duracao_servico,
            ADDTIME(a.data_agendamento, s.tempo) AS hora_fim
        FROM
            agendamento a
        JOIN
            cliente c ON a.cliente_id = c.id
        JOIN
            agendamento_servico ags ON a.id = ags.agendamento_id
        JOIN
            servico s ON ags.servico_id = s.id
        WHERE
            a.profissional_id = %s
        ORDER BY
            a.data_agendamento;
        """

        cursor = bancoBT.cursor()

        cursor.execute(query, (profissional_id,))
        agendamentos = cursor.fetchall()

        return render_template('public/pro/dashboard.html',
                               profissional_id=profissional_id,
                               agendamentos=agendamentos)


class PerfilCliente(MethodView):
    """
    Classe para manipular requisições relacionadas ao Perfil do Cliente
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
                "SELECT nome, sobrenome, telefone, email, senha "
                "FROM cliente WHERE id = %s", (cliente_id,))
            cliente_data = cursor.fetchone()
            cursor.close()

            if cliente_data:
                nome = cliente_data[0]
                sobrenome = cliente_data[1]
                telefone = cliente_data[2]
                email = cliente_data[3]
                senha = cliente_data[4]

                return render_template('public/cliente/perfil.html',
                                       id=cliente_id, nome=nome, sobrenome=sobrenome,
                                       telefone=telefone, email=email, senha=senha)
            else:
                return redirect('/login')
        else:
            return redirect('/login')


class UpdateUserC(MethodView):
    '''Classe responsável por atualizar dados do usuario'''

    def post(self):
        '''Função que altera nome, sobrenome, telefone e email do cliente'''
        cliente_id = session.get('cliente_id')
        if not cliente_id:
            return redirect('/login')

        nome = request.form.get('name')
        sobrenome = request.form.get('lastname')
        telefone = request.form.get('phone')
        email = request.form.get('email')

        cursor = bancoBT.cursor()

        try:
            # Recupera dados existentes, se necessário
            if not nome or not sobrenome or not telefone or not email:
                cursor.execute(
                    "SELECT nome, sobrenome, telefone, email FROM cliente WHERE id = %s", 
                    (cliente_id,)
                )
                cliente_data = cursor.fetchone()
                if cliente_data:
                    if not nome:
                        nome = cliente_data[0]
                    if not sobrenome:
                        sobrenome = cliente_data[1]
                    if not telefone:
                        telefone = cliente_data[2]
                    if not email:
                        email = cliente_data[3]

            # Atualiza os dados do cliente
            cursor.execute(
                "UPDATE cliente SET nome = %s, sobrenome = %s, telefone = %s, email = %s "
                "WHERE id = %s",
                (nome, sobrenome, telefone, email, cliente_id)
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
    Classe para manipular requisições relacionadas ao Perfil do Profissional
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
                "SELECT nome, categoria, telefone, email FROM profissional WHERE id = %s",
                (pro_id,))
            pro_data = cursor.fetchone()
            cursor.close()

            if pro_data:
                nome = pro_data[0]
                categoria = pro_data[1]
                telefone = pro_data[2]
                email = pro_data[3]

                return render_template(
                    'public/pro/perfil.html', id=pro_id, nome=nome,
                    categoria=categoria, email=email, telefone=telefone
                )
            else:
                return redirect('/login')
        else:
            return redirect('/login')


class UpdateUserP(MethodView):
    '''Classe responsável por atualizar dados do Profissional'''

    def post(self):
        '''Função que altera nome, sobrenome, telefone e email do profissional'''
        profissional_id = session.get('profissional_id')
        if not profissional_id:
            return redirect('/login')

        nome = request.form.get('name')
        categoria = request.form.get('category')
        telefone = request.form.get('phone')
        email = request.form.get('email')

        cursor = bancoBT.cursor()

        try:
            # Recupera dados existentes, se necessário
            if not nome or not categoria or not telefone or not email:
                cursor.execute(
                    "SELECT nome, categoria, telefone, email FROM profissional WHERE id = %s", 
                    (profissional_id,)
                )
                profissional_data = cursor.fetchone()
                if profissional_data:
                    if not nome:
                        nome = profissional_data[0]
                    if not categoria:
                        categoria = profissional_data[1]
                    if not telefone:
                        telefone = profissional_data[2]
                    if not email:
                        email = profissional_data[3]

            # Atualiza os dados do profissional
            cursor.execute(
                "UPDATE profissional SET nome = %s, categoria = %s, telefone = %s, email = %s " 
                "WHERE id = %s",(nome, categoria, telefone, email, profissional_id)
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
                    "SELECT nome, categoria FROM profissional WHERE id = %s",
                    (pro_id,)
                )
                pro_data = cursor.fetchone()

                cursor.execute(
                    "SELECT titulo, preco, tempo, descricao "
                    "FROM servico WHERE profissional_id = %s",
                    (pro_id,)
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
        '''
        Função que realiza o cadastro de serviços do profissional
        '''
        titulo = request.form.get('service')
        preco = request.form.get('price')
        tempo = request.form.get('time')
        descricao = request.form.get('description')
        profissional_id = request.form.get('profissional_id')

        if not all([titulo, preco, tempo, descricao, profissional_id]):
            return jsonify({"error": "Todos os campos são obrigatórios"}), 400

        cursor = None
        try:
            cursor = bancoBT.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM servico WHERE titulo = %s AND profissional_id = %s",
                (titulo, profissional_id)
            )
            if cursor.fetchone()[0] > 0:
                return jsonify({"error": "Serviço já cadastrado."}), 409

            cursor.execute(
                "INSERT INTO servico (titulo, preco, tempo, descricao, profissional_id) "
                "VALUES (%s, %s, %s, %s, %s)",
                (titulo, preco, tempo, descricao, profissional_id)
            )
            bancoBT.commit()
            return redirect('/services')
        except IntegrityError as e:
            bancoBT.rollback()
            return jsonify({"error": f"Erro de integridade: {str(e)}"}), 500
        except MySQLError as e:
            bancoBT.rollback()
            return jsonify({"error": f"Falha ao cadastrar serviço, erro do MySQL: {str(e)}"}), 500
        except Exception as e:
            bancoBT.rollback()
            return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500
        finally:
            if cursor:
                cursor.close()


class Horarios(MethodView):
    '''Classe horarios'''

    def get(self):
        """
        Manipula requisições GET para a pagina de horarios do profissionais.

        Retorna:
        render_template: Uma renderização do template 'public/pro/horarios.html'
        """
        pro_id = session.get('profissional_id')

        if not pro_id:
            return redirect('/login')

        dia_semana = [
            ('domingo', 'Domingo'),
            ('segunda', 'Segunda'),
            ('terca', 'Terça'),
            ('quarta', 'Quarta'),
            ('quinta', 'Quinta'),
            ('sexta', 'Sexta'),
            ('sabado', 'Sábado')
        ]

        horas_form = {}
        with bancoBT.cursor() as cursor:
            for dia_form, dia_sql in dia_semana:
                cursor.execute("""
                    SELECT fechado, hora_inicio, hora_fim FROM horarios
                    WHERE profissional_id = %s AND dia_semana = %s
                """, (pro_id, dia_sql))
                resultado = cursor.fetchone()

                if resultado:
                    fechado, hora_inicio, hora_fim = resultado
                else:
                    fechado, hora_inicio, hora_fim = True, '00:00:00', '00:00:00'

                horas_form[dia_form] = {
                    'fechado': fechado,
                    'hora_inicio': hora_inicio,
                    'hora_fim': hora_fim
                }
        return render_template('public/pro/horarios.html', id=pro_id, horarios=horas_form)

    def post(self):
        '''
        Pega os dados dos horarios e adiciona ao banco de dados.
        '''
        dia_semana = [
            ('domingo', 'Domingo'),
            ('segunda', 'Segunda'),
            ('terca', 'Terça'),
            ('quarta', 'Quarta'),
            ('quinta', 'Quinta'),
            ('sexta', 'Sexta'),
            ('sabado', 'Sábado')
        ]

        cursor = bancoBT.cursor()

        profissional_id = request.form.get('profissional_id')

        horas_form = {}
        for dia_form, dia_sql in dia_semana:
            fechado = dia_form not in request.form
            hora_inicio = request.form.get(
                f'{dia_form}-start', '00:00:00') if not fechado else '00:00:00'
            hora_fim = request.form.get(
                f'{dia_form}-end', '00:00:00') if not fechado else '00:00:00'

            horas_form[dia_form] = {
                'fechado': fechado,
                'hora_inicio': hora_inicio,
                'hora_fim': hora_fim
            }

            cursor.execute("""
                SELECT * FROM horarios WHERE profissional_id = %s AND dia_semana = %s
            """, (profissional_id, dia_sql))
            horario_existente = cursor.fetchone()

            if horario_existente:
                cursor.execute("""
                    UPDATE horarios
                    SET fechado = %s, hora_inicio = %s, hora_fim = %s
                    WHERE profissional_id = %s AND dia_semana = %s
                """, (fechado, hora_inicio, hora_fim, profissional_id, dia_sql))
            else:
                cursor.execute("""
                    INSERT INTO horarios (profissional_id, dia_semana, fechado, hora_inicio, hora_fim)
                    VALUES (%s, %s, %s, %s, %s)
                """, (profissional_id, dia_sql, fechado, hora_inicio, hora_fim))

        bancoBT.commit()
        cursor.close()

        return render_template('public/pro/horarios.html', id=profissional_id, horarios=horas_form)


class Agendamento(MethodView):
    '''
    Classe responsável pela tela de agendamento
    '''

    def get(self):
        '''
        Renderiza o arquivo do agendamento
        '''
        cliente_id = session.get('cliente_id')

        if not cliente_id:
            return redirect('/login')

        prof_id = request.args.get('profissional_id')

        if not prof_id:
            return redirect('/dashboardClient')

        cursor = bancoBT.cursor()

        cursor.execute(
            "SELECT nome, categoria, telefone, endereco FROM profissional WHERE id = %s", (
                prof_id,)
        )

        dados_pro = cursor.fetchone()

        cursor.execute(
            "SELECT dia_semana, fechado, hora_inicio, hora_fim FROM horarios "
            "WHERE profissional_id = %s", (
                prof_id,)
        )

        horarios_result = cursor.fetchall()

        dias_semana = ['Domingo', 'Segunda', 'Terça',
                       'Quarta', 'Quinta', 'Sexta', 'Sábado']
        horarios_pro = {dia: {'fechado': True, 'hora_inicio': None,
                              'hora_fim': None} for dia in dias_semana}

        for horario in horarios_result:
            dia_semana, fechado, hora_inicio, hora_fim = horario
            horarios_pro[dia_semana] = {
                'fechado': fechado,
                'hora_inicio': hora_inicio,
                'hora_fim': hora_fim
            }

        cursor.execute(
            "SELECT id, titulo, preco, tempo, descricao FROM servico WHERE profissional_id = %s", (
                prof_id,)
        )
        services = cursor.fetchall()

        cursor.execute(
            "SELECT data_agendamento, s.tempo FROM agendamento a JOIN agendamento_servico ags "
            "ON a.id = ags.agendamento_id JOIN servico s ON ags.servico_id = s.id "
            "WHERE a.profissional_id = %s", (
                prof_id,)
        )

        agendamentos = cursor.fetchall()

        horarios_indisponiveis = []
        for agendamento in agendamentos:
            data_agendamento, tempo = agendamento
            horario_inicio = data_agendamento.strftime("%d/%m %H:%M")
            horario_fim = (data_agendamento + tempo).strftime("%H:%M")
            horarios_indisponiveis.append(
                f"{horario_inicio} - {horario_fim}")

        return render_template(
            'public/cliente/agendamento.html',
            cliente_id=cliente_id,
            dados_pro=dados_pro,
            horarios_pro=horarios_pro,
            services=services,
            horarios_indisponiveis=horarios_indisponiveis,
            prof_id=prof_id
        )

    def post(self):
        '''
        Insere dados no banco de dados
        '''
        data_agendamento = request.form.get('data_agendamento')
        hora_agendamento = request.form.get('hora_agendamento')
        servico_id = request.form.get('servico')
        cliente_id = request.form.get('cliente_id')
        prof_id = request.form.get('profissional_id')

        # Debugging prints
        print(f"data_agendamento: {data_agendamento}")
        print(f"hora_agendamento: {hora_agendamento}")
        print(f"servico_id: {servico_id}")
        print(f"cliente_id: {cliente_id}")
        print(f"profissional_id: {prof_id}")

        # Validações básicas
        if (
                not data_agendamento or
                not hora_agendamento or
                not servico_id or
                not cliente_id or
                not prof_id):
            abort(400, description="Preencha todos os campos")

        data_hora_agendamento = f"{data_agendamento} {hora_agendamento}:00"

        # Converte a data de agendamento para um objeto datetime
        data_obj = datetime.strptime(data_agendamento, "%Y-%m-%d")
        # Nome do dia da semana em inglês
        dia_semana_en = data_obj.strftime("%A")

        # Mapeamento do nome dos dias da semana de inglês para português
        dias_semana = {
            'Sunday': 'Domingo',
            'Monday': 'Segunda',
            'Tuesday': 'Terça',
            'Wednesday': 'Quarta',
            'Thursday': 'Quinta',
            'Friday': 'Sexta',
            'Saturday': 'Sábado'
        }

        dia_semana = dias_semana.get(dia_semana_en)

        # Capturar os horários do profissional para o dia da semana específico
        cursor = bancoBT.cursor()
        cursor.execute(
            "SELECT fechado, hora_inicio, hora_fim FROM horarios "
            "WHERE profissional_id = %s AND dia_semana = %s", (
                prof_id, dia_semana)
        )

        horario_profissional = cursor.fetchone()

        if not horario_profissional:
            abort(400, description="Horário não encontrado para o profissional")

        fechado, hora_inicio, hora_fim = horario_profissional

        # Se o dia estiver fechado, retornar erro
        if fechado:
            abort(400, description="O profissional não atende neste dia")

        # Converter hora_inicio e hora_fim para datetime.time
        hora_inicio_time = (datetime.min + hora_inicio).time()
        hora_fim_time = (datetime.min + hora_fim).time()

        hora_agendamento_time = datetime.strptime(
            hora_agendamento, "%H:%M").time()
        if hora_agendamento_time < hora_inicio_time or hora_agendamento_time > hora_fim_time:
            abort(400, description="Horário fora do período de atendimento")

        # Verificar se o horário está disponível considerando a duração do serviço
        cursor.execute(
            "SELECT tempo FROM servico WHERE id = %s", (servico_id,)
        )
        servico_tempo = cursor.fetchone()[0]

        data_hora_inicio = datetime.strptime(
            data_hora_agendamento, "%Y-%m-%d %H:%M:%S")
        data_hora_fim = data_hora_inicio + servico_tempo

        cursor.execute(
            "SELECT data_agendamento, s.tempo FROM agendamento a JOIN agendamento_servico ags "
            "ON a.id = ags.agendamento_id JOIN servico s ON ags.servico_id = s.id "
            "WHERE a.profissional_id = %s",
            (prof_id,)
        )

        agendamentos = cursor.fetchall()

        for agendamento in agendamentos:
            agendamento_inicio, agendamento_tempo = agendamento
            agendamento_fim = agendamento_inicio + agendamento_tempo

            if (data_hora_inicio < agendamento_fim and data_hora_fim > agendamento_inicio):
                abort(400, description="Horário indisponível")

        # Inserir novo agendamento
        cursor.execute(
            "INSERT INTO agendamento (data_agendamento, cliente_id, profissional_id) "
            "VALUES (%s, %s, %s)",
            (data_hora_agendamento, cliente_id, prof_id)
        )
        agendamento_id = cursor.lastrowid

        # Inserir na tabela agendamento_servico
        cursor.execute(
            "INSERT INTO agendamento_servico (agendamento_id, servico_id) VALUES (%s, %s)",
            (agendamento_id, servico_id)
        )

        print(f"dia: {dia_semana}")

        bancoBT.commit()

        return redirect('/agenda')


class Agenda(MethodView):
    '''
    Tela responsavel pela tela agenda
    '''

    def get(self):
        '''
        renderiza o agenda.html
        '''
        cliente_id = session.get('cliente_id')

        if not cliente_id:
            return redirect('/login')

        cursor = bancoBT.cursor()

        query = """
        SELECT 
            a.data_agendamento,
            p.nome AS profissional_nome,
            p.categoria AS profissional_categoria,
            s.titulo AS servico_titulo,
            s.tempo AS duracao_servico,
            ADDTIME(a.data_agendamento, s.tempo) AS hora_fim
        FROM 
            agendamento a
        JOIN 
            profissional p ON a.profissional_id = p.id
        JOIN 
            agendamento_servico ags ON a.id = ags.agendamento_id
        JOIN 
            servico s ON ags.servico_id = s.id
        WHERE 
            a.cliente_id = %s
        ORDER BY 
            a.data_agendamento;
        """

        cursor.execute(query, (cliente_id,))
        agendamentos = cursor.fetchall()

        return render_template('public/cliente/agenda.html', agendamentos=agendamentos)
