# CategoriaDAO

from model import Categorias
from database import database

class CategoriaDAO:
    # Busca todas as categorias
    @staticmethod
    def searchCategories():
        return Categorias.query.all()

    # Busca categorias por nome
    @staticmethod
    def searchCategoriesByName(nome):
        return Categorias.query.filter(Categorias.nome.ilike(f'%{nome}%')).all()

    # Adiciona uma nova categoria
    @staticmethod
    def addCategory(nome):
        try:
            nova_categoria = Categorias(nome=nome)
            database.session.add(nova_categoria)
            database.session.commit()
            return True
        except Exception as e:
            database.session.rollback()
            print(f"Erro ao adicionar categoria: {e}")
            return False

    # Atualiza uma categoria existente
    @staticmethod
    def updateCategory(id, nome):
        categoria = Categorias.query.get(id)
        if categoria:
            categoria.nome = nome
            try:
                database.session.commit()
                return True
            except Exception as e:
                database.session.rollback()
                print(f"Erro ao atualizar categoria: {e}")
                return False
        return "Erro: Categoria não encontrada"

    # Deleta uma categoria existente
    @staticmethod
    def deleteCategory(id):
        categoria = Categorias.query.get(id)
        if categoria:
            try:
                database.session.delete(categoria)
                database.session.commit()
                return True
            except Exception as e:
                database.session.rollback()
                print(f"Erro ao excluir categoria: {e}")
                return False
        return "Erro: Categoria não encontrada"

    # Obtém uma categoria pelo ID
    @staticmethod
    def getCategoryById(id):
        return Categorias.query.get(id)
