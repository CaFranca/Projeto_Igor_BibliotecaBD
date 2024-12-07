from database import database

class Livros(database.Model):
    # Definição das colunas da tabela 'livros'
    id = database.Column(database.Integer, primary_key=True)  # Chave primária
    titulo = database.Column(database.String(150), nullable=False)  # Título do livro
    isbn = database.Column(database.String(13), unique=True, nullable=False)  # ISBN único
    data_publicacao = database.Column(database.Date, nullable=True)  # Data de publicação do livro
    numero_paginas = database.Column(database.Integer, nullable=True)  # Número de páginas do livro
    
    # Foreign Key para a tabela 'Autores'
    autor_id = database.Column(database.Integer, database.ForeignKey("autores.id"), nullable=True)
    # Foreign Key para a tabela 'Categorias'
    categoria_id = database.Column(database.Integer, database.ForeignKey("categorias.id"), nullable=True)
    
    # Relacionamento com 'Autores' (muitos-para-um)
    autor = database.relationship("Autores", back_populates="livros", lazy=True)
    # Relacionamento com 'Categorias' (muitos-para-um)
    categoria = database.relationship("Categorias", back_populates="livros", lazy=True)
    
    # Método para transformar o objeto 'Livro' em JSON
    def JSonificar(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "isbn": self.isbn,
            "data_publicacao": self.data_publicacao.isoformat() if self.data_publicacao else None,
            "numero_paginas": self.numero_paginas,
            "autor": self.autor.nome if self.autor else "Autor não definido",
            "categoria": self.categoria.nome if self.categoria else "Categoria não definida"
        }
