# Importa o SQLAlchemy para gerenciar a conexão com o banco de dados
from flask_sqlalchemy import SQLAlchemy

# Cria a instância do SQLAlchemy para interagir com o banco de dados
database = SQLAlchemy()

# Função para configurar e inicializar o banco de dados na aplicação Flask
def init_database(app):
    # Define a URI do banco de dados SQLite local
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Biblioteca.db"
    
    # Inicializa o SQLAlchemy com o contexto da aplicação
    with app.app_context():
        database.init_app(app)  # Conecta o SQLAlchemy à aplicação
        database.create_all()  # Cria as tabelas no banco de dados
