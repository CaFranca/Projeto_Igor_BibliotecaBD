from flask import Blueprint, request, render_template, redirect, url_for, flash
from repository import LivroRepository
from datetime import datetime
import logging

# Configuração do logging
logging.basicConfig(level=logging.ERROR)

# Criação de um Blueprint chamado "bp_books" para gerenciar rotas relacionadas a livros
livroController = Blueprint("bp_books", __name__)
# Instancia o repositório de livros
livroRepository = LivroRepository()

# Rota para adicionar um livro ao banco de dados
@livroController.route("/add", methods=['POST'])
def add_book():
    if request.method == "POST":
        titulo = request.form.get('titulo')
        isbn = request.form.get('isbn')

        data_publicacaoBruta = request.form.get('publicadoEm')
        try:
            data_publicacao = datetime.strptime(data_publicacaoBruta, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de data inválido.', 'danger')
            return redirect(url_for('bp_books.view_books'))

        numero_paginas = request.form.get('numeroPaginas')
        autor_id = request.form.get('autor_id')
        categoria_id = request.form.get('categoria_id')

        # Validação dos campos obrigatórios
        if not titulo or not isbn or not data_publicacao or not numero_paginas or not autor_id or not categoria_id:
            flash('Todos os campos devem ser preenchidos', 'danger')
            return redirect(url_for('bp_books.view_books'))

        # Adiciona o livro
        resultado = livroRepository.addBook(titulo=titulo, isbn=isbn, data_publicacao=data_publicacao, numero_paginas=numero_paginas, autor_id=autor_id, categoria_id=categoria_id)
        
        if "Erro" in resultado:
            flash(f'Erro ao adicionar livro: {resultado}', 'danger')
        else:
            flash('Livro adicionado com sucesso!', 'success')
        return redirect(url_for('bp_books.view_books'))
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
            flash("Nenhum autor encontrado.", 'warning')
        if not categorias:
            flash("Nenhuma categoria encontrada.", 'warning')

        # Verifica se a pesquisa não retornou livros
        if not livros:
            flash("Nenhum livro encontrado com os critérios fornecidos.", 'info')

        # Renderiza o template com os dados filtrados
        return render_template(
            'Livro/livros.html',
            livros=livros,
            autores=autores,
            categorias=categorias
        )
    
    except Exception as e:
        # Loga o erro e retorna uma mensagem de erro genérica
        logging.error(f"Erro ao carregar a página de livros: {e}", exc_info=True)
        flash('Ocorreu um erro ao carregar a página de livros.', 'danger')
        return "Ocorreu um erro ao carregar a página de livros.", 500

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

        # Validação dos campos obrigatórios
        if not titulo or not isbn or not data_publicacao or not numero_paginas or not autor_id or not categoria_id:
            flash('Todos os campos devem ser preenchidos', 'danger')
            return redirect(url_for('bp_books.edit_book', id=id))

        # Chama o método para atualizar o livro
        resultado = livroRepository.updateBook(id, titulo, isbn, data_publicacao, numero_paginas, autor_id, categoria_id)
        
        if "Erro" in resultado:
            flash(f'Erro ao atualizar livro: {resultado}', 'danger')
        else:
            flash('Livro atualizado com sucesso!', 'success')

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
        flash(f'Erro ao excluir livro: {resultado}', 'danger')
    else:
        flash('Livro excluído com sucesso!', 'success')
    
    return redirect(url_for('bp_books.view_books'))

# Rota inicial para renderizar uma página específica para livros
@livroController.route("/")
def books_home():
    return redirect(url_for('bp_books.view_books'))
