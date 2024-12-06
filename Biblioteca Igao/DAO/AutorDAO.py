from model import Autores
from database import database
from datetime import datetime

class AutorDAO:
    @staticmethod
    def searchAutores():
        # Retorna todos os autores do banco de dados
        return Autores.query.all()

    @staticmethod
    def addAutor(nome, data_nascimento, nacionalidade):
        try:
            # Cria um novo objeto Autor
            novo_autor = Autores(
                nome=nome,
                data_nascimento=data_nascimento,
                nacionalidade=nacionalidade
            )
            # Adiciona o autor ao banco de dados
            database.session.add(novo_autor)
            # Confirma a transação
            database.session.commit()
            return True
        except Exception as e:
            # Em caso de erro, desfaz a transação
            database.session.rollback()
            print(f"Erro ao adicionar autor: {e}")
            return False

    @staticmethod
    def updateAutor(id, nome, data_nascimento, nacionalidade):
        try:
            # Busca o autor pelo ID
            autor = Autores.query.get(id)
            if autor:
                # Atualiza os campos do autor
                autor.nome = nome
                autor.data_nascimento = data_nascimento
                autor.nacionalidade = nacionalidade
                # Confirma a transação
                database.session.commit()
                return True
            return False
        except Exception as e:
            # Em caso de erro, desfaz a transação
            database.session.rollback()
            print(f"Erro ao atualizar autor: {e}")
            return False

    @staticmethod
    def getAutorById(id):
        # Retorna o autor pelo ID
        return Autores.query.get(id)

    @staticmethod
    def deleteAutor(id):
        try:
            # Busca o autor pelo ID
            autor = Autores.query.get(id)
            if autor:
                # Exclui o autor
                database.session.delete(autor)
                # Confirma a transação
                database.session.commit()
                return True
            return False
        except Exception as e:
            # Em caso de erro, desfaz a transação
            database.session.rollback()
            print(f"Erro ao excluir autor: {e}")
            return False
