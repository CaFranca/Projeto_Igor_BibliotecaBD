from flask import Blueprint, render_template, request, redirect, url_for
from repository import AutorRepository
from datetime import datetime

# Cria o blueprint para a rota de autores
authorController = Blueprint('bp_autores', __name__)

# Instancia o repositório de autores
autor_repo = AutorRepository()

# Exibe todos os autores
@authorController.route("/autores", methods=["GET"])
def view_autores():
    # Obtém todos os autores no formato JSON
    autores_json = autor_repo.searchAutoresJSON()
    return render_template("Autor/autores.html", autores=autores_json)

# Adiciona um novo autor
@authorController.route("/autores/adicionar", methods=["POST"])
def add_autor():
    nome = request.form.get("nome")

    data_nascimentoBruta = request.form.get("data_nascimento")
    data = datetime.strptime(data_nascimentoBruta, '%Y-%m-%d').date()
    data_nascimento = data

    nacionalidade = request.form.get("nacionalidade")
    
    # Chama o repositório para adicionar um novo autor
    autor_repo.addAutor(nome, data_nascimento, nacionalidade)
    return redirect(url_for('bp_autores.view_autores'))  # Redireciona para a lista de autores

# Edita um autor existente
@authorController.route("/autores/editar/<int:id>", methods=["GET", "POST"])
def edit_autor(id):
    if request.method == "POST":
        nome = request.form.get("nome")
        data_nascimentoBruta = request.form.get("data_nascimento")
        data_nascimento = datetime.strptime(data_nascimentoBruta, '%Y-%m-%d').date()  # Converte a data
        nacionalidade = request.form.get("nacionalidade")
        
        # Chama o repositório para atualizar o autor
        autor_repo.updateAutor(id, nome, data_nascimento, nacionalidade)
        return redirect(url_for('bp_autores.view_autores'))  # Redireciona para a lista de autores
    
    # Recupera os dados do autor para edição
    autor = autor_repo.getAutorById(id)
    return render_template("Autor/AutorEdit.html", autor=autor)

# Exclui um autor
@authorController.route("/autores/excluir/<int:id>", methods=["GET"])
def delete_autor(id):
    # Chama o repositório para excluir o autor
    autor_repo.deleteAutor(id)
    return redirect(url_for('bp_autores.view_autores'))  # Redireciona para a lista de autores

@authorController.route("/")
def index():

    return redirect(url_for('bp_autores.view_autores'))