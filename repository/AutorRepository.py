# Importa as funções necessárias para redirecionamento e manipulação de URLs no Flask
from flask import redirect, url_for
# Importa o DAO para manipulação dos dados
from DAO import AutorDAO

class AutorRepository:
    # Método construtor
    def __init__(self):
        # Cria uma instância do DAO responsável pela manipulação dos dados
        self.autorDAO = AutorDAO()

    # Método para buscar todos os autores e retornar no formato JSON
    def searchAutoresJSON(self):
        # Busca todos os autores usando o método do DAO
        autores = self.autorDAO.searchAutores()
        # Converte os autores para o formato JSON
        autores_json = [autor.JSonificar() for autor in autores]
        # Retorna a lista de autores em JSON
        return autores_json

    # Método para adicionar um novo autor ao banco de dados
    def addAutor(self, nome, data_nascimento, nacionalidade):
        sucesso = self.autorDAO.addAutor(nome, data_nascimento, nacionalidade)
        if sucesso:
            return redirect(url_for("bp_autores.view_autores"))
        return "Erro ao adicionar o autor..."

    # Método para atualizar um autor existente
    def updateAutor(self, id, nome, data_nascimento, nacionalidade):
        try:
            # Atualiza o autor utilizando o DAO
            sucesso = self.autorDAO.updateAutor(id, nome, data_nascimento, nacionalidade)
            if sucesso:
                return "Autor atualizado com sucesso!"
            else:
                return "Erro ao atualizar o autor no banco de dados..."
        except Exception as e:
            return f"Erro ao processar a atualização: {e}"

    # Método para buscar um autor pelo ID
    def getAutorById(self, id):
        return self.autorDAO.getAutorById(id)

    # Método para excluir um autor
    def deleteAutor(self, id):
        sucesso = self.autorDAO.deleteAutor(id)
        if sucesso:
            return "Autor excluído com sucesso!"
        else:
            return "Erro ao excluir o autor..."

