from database import database

class Categorias(database.Model):
    # Definição das colunas da tabela 'categorias'
    id = database.Column(database.Integer, primary_key=True)  # Chave primária
    nome = database.Column(database.String(50), nullable=False)  # Nome da categoria
    
    # Relacionamento com 'Livros' (um-para-muitos)
    livros = database.relationship("Livros", back_populates="categoria", lazy=True)
    
    # Método para transformar o objeto 'Categoria' em JSON
    def JSonificar(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "livros": [livro.JSonificar() for livro in self.livros]  # Lista de livros da categoria em JSON
        }
