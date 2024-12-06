# Importa as funções necessárias para redirecionamento e manipulação de URLs no Flask
from flask import redirect, url_for
# Importa os DAOs ou classes para manipulação do banco de dados
from DAO import LivroDAO
# Importa a classe datetime para manipulação de datas
from datetime import datetime

# Define a classe LivroRepository, que segue o padrão Repository
class LivroRepository:
    # Método construtor da classe LivroRepository
    def __init__(self):
        # Cria uma instância do DAO responsável pela manipulação dos dados de livros
        self.livroDAO = LivroDAO()

    # Método para buscar todos os livros e retornar no formato JSON
    def searchBooksJSON(self):
        # Busca todos os livros no banco de dados utilizando o DAO
        livros = self.livroDAO.searchBooks()
        # Converte cada livro obtido para o formato JSON utilizando o método JSonificar
        livros_json = [livro.JSonificar() for livro in livros]
        # Retorna a lista de livros no formato JSON
        return livros_json

    # Método para adicionar um novo livro ao banco de dados
    def addBook(self, titulo, isbn, data_publicacao, numero_paginas, autor_id, categoria_id):
        # Chama o método do DAO para adicionar um novo livro no banco de dados
        sucesso = self.livroDAO.addBook(
            titulo, isbn, data_publicacao, numero_paginas, autor_id, categoria_id
        )
        # Verifica se a operação foi bem-sucedida
        if sucesso:
            # Caso a operação seja bem-sucedida, redireciona para a página de visualização de livros
            return redirect(url_for("bp_books.view_books"))
        # Caso a operação falhe, retorna uma mensagem de erro
        return "Erro ao adicionar o livro..."

    # Método para atualizar um livro existente no banco de dados
    def updateBook(self, id, titulo, isbn, data_publicacao, numero_paginas, autor_id, categoria_id):
        try:
            # Tenta converter a string da data de publicação para um objeto datetime.date
            data_publicacao_convertida = datetime.strptime(data_publicacao, '%Y-%m-%d').date()
        except ValueError as e:
            # Caso ocorra um erro na conversão da data, retorna uma mensagem de erro
            return f"Erro: Data de publicação inválida ({e})"

        try:
            # Chama o método do DAO para atualizar o livro com os novos dados
            sucesso = self.livroDAO.updateBook(
                id,
                titulo,
                isbn,
                data_publicacao_convertida,  # Passa a data convertida
                int(numero_paginas),  # Garante que o número de páginas seja um inteiro
                int(autor_id),  # Garante que o autor seja um número inteiro
                int(categoria_id)  # Garante que a categoria seja um número inteiro
            )
            if sucesso:
                # Se a atualização for bem-sucedida, retorna uma mensagem de sucesso
                return "Livro atualizado com sucesso!"
            else:
                # Se a atualização falhar, retorna uma mensagem de erro
                return "Erro ao atualizar o livro no banco de dados..."
        except Exception as e:
            # Em caso de erro ao processar a atualização, retorna o erro detalhado
            return f"Erro ao processar a atualização: {e}"

    # Método para obter um livro específico pelo seu ID
    def getBookById(self, id):
        # Chama o método do DAO para retornar o livro com o ID fornecido
        return self.livroDAO.getBookById(id)

    # Método para obter todos os autores cadastrados no sistema
    def getAutores(self):
        # Chama o método do DAO para retornar todos os autores
        return self.livroDAO.getAutores()

    # Método para obter todas as categorias cadastradas no sistema
    def getCategorias(self):
        # Chama o método do DAO para retornar todas as categorias
        return self.livroDAO.getCategorias()

    # Método para excluir um livro pelo ID
    def deleteBook(self, id):
        # Chama o método do DAO para excluir o livro com o ID fornecido
        sucesso = self.livroDAO.deleteBook(id)
        if sucesso:
            # Se a exclusão for bem-sucedida, retorna uma mensagem de sucesso
            return "Livro excluído com sucesso!"
        else:
            # Caso contrário, retorna uma mensagem de erro
            return "Erro ao excluir o livro..."

    # Método para realizar uma busca personalizada de livros
    def searchBooksCustom(self, titulo=None, autor_id=None, categoria_id=None, data_inicio=None, isbn=None):
        try:
            # Chama o método do DAO para realizar a busca personalizada com os parâmetros fornecidos
            livros = self.livroDAO.searchBooksCustom(titulo, autor_id, categoria_id, data_inicio, isbn)
            # Converte os livros encontrados para o formato JSON
            livros_json = [livro.JSonificar() for livro in livros]
            return livros_json
        except Exception as e:
            # Em caso de erro, retorna a mensagem de erro
            return f"Erro ao realizar a consulta personalizada: {e}"
