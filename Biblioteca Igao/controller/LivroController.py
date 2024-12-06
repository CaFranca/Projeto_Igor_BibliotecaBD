from flask import Blueprint,request, render_template, redirect, url_for
from repository import LivroRepository
from datetime import datetime


# Criação de um Blueprint chamado "bp_books" para gerenciar rotas relacionadas a livros
livroController = Blueprint("bp_books", __name__)
# Instancia o repositório de livros
livroRepository = LivroRepository()




# Rota para adicionar um livro ao banco de dados
@livroController.route("/add", methods=['POST'])
def add_book():
    if request.method == "POST":
        titulo = request.form.get('titulo')
        isbn=request.form.get('isbn')

        data_publicacaoBruta=request.form.get('publicadoEm')
        data=datetime.strptime(data_publicacaoBruta, '%Y-%m-%d').date()
        data_publicacao= data

        numero_paginas=request.form.get('numeroPaginas')

        autor_id = request.form.get('autor_id')
        categoria_id = request.form.get('categoria_id')

        return livroRepository.addBook(titulo=titulo, isbn=isbn, data_publicacao=data_publicacao,numero_paginas=numero_paginas, autor_id=autor_id, categoria_id=categoria_id)
    return "Erro inesperado"

@livroController.route('/livros', methods=['GET'])
def view_books():
    # Obtém os parâmetros de pesquisa do request
    titulo = request.args.get('titulo', '').strip()
    autor_id = request.args.get('autor_id', '').strip()
    categoria_id = request.args.get('categoria_id', '').strip()
    data_inicio = request.args.get('data_inicio', '').strip()

    try:
        # Busca personalizada no repositório
        livros = livroRepository.searchBooksCustom(
            titulo=titulo, 
            autor_id=autor_id, 
            categoria_id=categoria_id, 
            data_inicio=data_inicio
        )
        
        # Obtém listas de autores e categorias para os filtros
        autores = livroRepository.getAutores()
        categorias = livroRepository.getCategorias()

        # Verifica se os dados de autores e categorias estão carregados corretamente
        if not autores:
            print("Nenhum autor encontrado.")
        if not categorias:
            print("Nenhuma categoria encontrada.")

        # Renderiza o template com os dados filtrados
        return render_template(
            'Livro/livros.html',
            livros=livros,
            autores=autores,
            categorias=categorias
        )
    
    except Exception as e:
        # Retorna uma mensagem de erro genérica e loga o erro (log para depuração)
        print(f"Erro ao carregar a página de livros: {e}")
        return "Ocorreu um erro ao carregar a página de livros.", 500


    ##return jsonify(livroRepository.searchBooksJSON())

@livroController.route('/editar/<int:id>', methods=['GET', 'POST'])
def edit_book(id):

    if request.method == 'POST':
        # Coleta os dados do formulário
        titulo = request.form.get('titulo')
        isbn = request.form.get('isbn')
        data_publicacao = request.form.get('data_publicacao')
        numero_paginas = request.form.get('numero_paginas')
        autor_id = request.form.get('autor_id')
        categoria_id = request.form.get('categoria_id')

        # Chama o método para atualizar o livro
        resultado = livroRepository.updateBook(id, titulo, isbn, data_publicacao, numero_paginas, autor_id, categoria_id)
        
        if "Erro" in resultado:
            return resultado  # Se falhou, retorna a mensagem de erro

        # Se sucesso, redireciona para a página de livros
        return redirect(url_for('bp_books.view_books'))

    # Se for GET, carrega os dados do livro para o formulário
    livro = livroRepository.getBookById(id)
    autores = livroRepository.getAutores()
    categorias = livroRepository.getCategorias()
    
    return render_template('Livro/LivroEdit.html', livro=livro, autores=autores, categorias=categorias)

@livroController.route('/excluir/<int:id>', methods=['GET', 'POST'])
def delete_book(id):
    resultado = livroRepository.deleteBook(id)
    
    if resultado.startswith("Erro"):
        # Retorna a mensagem de erro
        return resultado
    else:
        # Retorna a mensagem de sucesso
        return redirect(url_for('bp_books.view_books'))
        


# Rota inicial para renderizar uma página específica para livros
@livroController.route("/")
def books_home():
    return redirect(url_for('bp_books.view_books'))
