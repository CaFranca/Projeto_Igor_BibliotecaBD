from database import database

class Autores(database.Model):
    # Definição das colunas da tabela 'autores'
    id = database.Column(database.Integer, primary_key=True)  # Chave primária
    nome = database.Column(database.String(100), nullable=False)  # Nome do autor
    data_nascimento = database.Column(database.Date, nullable=True)  # Data de nascimento do autor
    nacionalidade = database.Column(database.String(50), nullable=False)  # Nacionalidade do autor
    
    # Relacionamento com 'Livros' (um-para-muitos)
    livros = database.relationship("Livros", back_populates="autor", lazy=True)
    
    # Método para transformar o objeto 'Autor' em JSON
    def JSonificar(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "data_nascimento": self.data_nascimento.isoformat() if self.data_nascimento else None,
            "nacionalidade": self.nacionalidade,
            "livros": [livro.JSonificar() for livro in self.livros]  # Lista de livros do autor em JSON
        }
