from model import Livros, Autores, Categorias
from database import database
from datetime import datetime

class LivroDAO:
    @staticmethod
    def searchBooks():
        # Retorna todos os livros do banco de dados
        return Livros.query.all()

    @staticmethod
    def addBook(titulo, isbn, data_publicacao, numero_paginas, autor_id, categoria_id):
        try:
            # Cria um novo objeto Livro
            novo_livro = Livros(
                titulo=titulo,
                isbn=isbn,
                data_publicacao=data_publicacao,
                numero_paginas=numero_paginas,
                autor_id=autor_id,
                categoria_id=categoria_id,
            )
            # Adiciona o livro ao banco de dados
            database.session.add(novo_livro)
            # Confirma a transação
            database.session.commit()
            return True
        except Exception as e:
            # Em caso de erro, desfaz a transação
            database.session.rollback()
            print(f"Erro ao adicionar livro: {e}")
            return False

    @staticmethod
    def updateBook(id, titulo, isbn, data_publicacao, numero_paginas, autor_id, categoria_id):
        try:
            # Converte a data_publicacao para um objeto datetime.date, se necessário
            if isinstance(data_publicacao, str):
                data_publicacao = datetime.strptime(data_publicacao, "%Y-%m-%d").date()
            
            # Busca o livro pelo ID
            livro = Livros.query.get(id)
            if livro:
                # Atualiza os campos do livro
                livro.titulo = titulo
                livro.isbn = isbn
                livro.data_publicacao = data_publicacao
                livro.numero_paginas = numero_paginas
                livro.autor_id = autor_id
                livro.categoria_id = categoria_id
                # Confirma a transação
                database.session.commit()
                return True
            return False
        except Exception as e:
            # Em caso de erro, desfaz a transação
            database.session.rollback()
            print(f"Erro ao atualizar livro: {e}")
            return False

    @staticmethod
    def getBookById(id):
        # Retorna o livro pelo ID
        return Livros.query.get(id)

    @staticmethod
    def getAutores():
        # Retorna todos os autores
        return Autores.query.all()

    @staticmethod
    def getCategorias():
        # Retorna todas as categorias
        return Categorias.query.all()

    @staticmethod
    def deleteBook(id):
        try:
            # Busca o livro pelo ID
            livro = Livros.query.get(id)
            if livro:
                # Exclui o livro
                database.session.delete(livro)
                # Confirma a transação
                database.session.commit()
                return True
            return False
        except Exception as e:
            # Em caso de erro, desfaz a transação
            database.session.rollback()
            print(f"Erro ao excluir livro: {e}")
            return False

    @staticmethod
    def searchBooksCustom(titulo=None, autor_id=None, categoria_id=None, data_inicio=None, isbn=None):
        # Cria a consulta básica para livros
        query = Livros.query
        
        # Filtro por título, se fornecido
        if titulo:
            query = query.filter(Livros.titulo.like(f"%{titulo}%"))
        
        # Filtro por autor, se fornecido
        if autor_id:
            query = query.filter(Livros.autor_id == autor_id)
        
        # Filtro por categoria, se fornecido
        if categoria_id:
            query = query.filter(Livros.categoria_id == categoria_id)
        
        # Filtro por data de publicação, se fornecida
        if data_inicio:
            query = query.filter(Livros.data_publicacao >= data_inicio)

        # Filtro por ISBN, se fornecido
        if isbn:
            query = query.filter(Livros.isbn.like(f"%{isbn}%"))
        
        # Retorna a lista de livros conforme os filtros
        return query.all()
