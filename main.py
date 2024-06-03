'''Arquivo responsável por iniciar o Servidor Flask'''

from src.app import app

HOST = 'localhost'
PORT = 4000
DEBUG = True

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
