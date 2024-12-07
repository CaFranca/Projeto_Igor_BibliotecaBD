# CategoriaRepository

from DAO import CategoriaDAO

class CategoriaRepository:
    def __init__(self):
        self.categoriaDAO = CategoriaDAO()

    # Busca todas as categorias
    def searchCategories(self, nome=''):
        if nome:
            return self.categoriaDAO.searchCategoriesByName(nome)
        return self.categoriaDAO.searchCategories()

    # Busca categorias e retorna no formato JSON
    def searchCategoriesJSON(self, nome=''):
        categorias = self.searchCategories(nome)
        categorias_json = [categoria.JSonificar() for categoria in categorias]
        return categorias_json

    # Adiciona uma nova categoria
    def addCategory(self, nome):
        sucesso = self.categoriaDAO.addCategory(nome)
        return sucesso

    # Atualiza uma categoria existente
    def updateCategory(self, id, nome):
        sucesso = self.categoriaDAO.updateCategory(id, nome)
        return sucesso

    # Deleta uma categoria existente
    def deleteCategory(self, id):
        sucesso = self.categoriaDAO.deleteCategory(id)
        return sucesso

    # Obtém uma categoria pelo ID
    def getCategoryById(self, id):
        return self.categoriaDAO.getCategoryById(id)
