from flask import Blueprint, render_template, redirect, url_for, request
from repository import CategoriaRepository

# Criação de um Blueprint chamado "bp_categories" para gerenciar rotas relacionadas a categorias
categoryController = Blueprint("bp_categories", __name__)
# Instancia o repositório de categorias
categoryRepository = CategoriaRepository()

# Rota para adicionar uma nova categoria ao banco de dados
@categoryController.route("/add", methods=['GET', 'POST'])
def add_category():
    if request.method == "POST":
        nome = request.form.get('categoria')  # Coleta o nome da categoria
        if nome:
            sucesso = categoryRepository.addCategory(nome)
            if sucesso:
                return redirect(url_for('bp_categories.view_categories'))  # Redireciona após a adição
            return "Erro ao adicionar categoria"
        return "Nome da categoria não fornecido"
    
    return redirect(url_for('bp_inicio.index'))  # Exibe formulário de adição de categoria

# Rota para visualizar todas as categorias
@categoryController.route('/categorias', methods=['GET'])
def view_categories():
    nome = request.args.get('nome', '')  # Parâmetro de busca opcional pelo nome da categoria

    # Chama o método de busca com o nome, tratando para não enviar vazio
    categorias = categoryRepository.searchCategories(nome)
    
    # Renderiza o template com as categorias filtradas
    return render_template('Categorias/categorias.html', categorias=categorias)

# Rota para editar uma categoria existente
from flask import redirect, render_template, request, url_for

@categoryController.route('/editar/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    # Carrega a categoria pelo ID
    categoria = categoryRepository.getCategoryById(id)

    if not categoria:
        return f"Erro: Categoria com ID {id} não encontrada."  # Caso a categoria não seja encontrada

    if request.method == 'POST':
        nome = request.form.get('categoria')
        if nome:
            # Tenta atualizar a categoria e verifica se foi bem-sucedido
            if not categoryRepository.updateCategory(id, nome):
                return "Erro: Falha ao atualizar a categoria."  # Caso a atualização falhe

            # Se a atualização for bem-sucedida, redireciona
            return redirect(url_for('bp_categories.view_categories'))

        return "Nome da categoria não fornecido."  # Retorna mensagem de erro se o nome não for fornecido

    # Renderiza o template de edição com a categoria carregada
    return render_template('Categorias/CategoriaEdit.html', categoria=categoria)


# Rota para excluir uma categoria
@categoryController.route('/excluir/<int:id>', methods=['POST', 'GET'])
def delete_category(id):
    # Tenta excluir a categoria
    resultado = categoryRepository.deleteCategory(id)

    if resultado:  # Se for True, a categoria foi excluída com sucesso
        return redirect(url_for('bp_categories.view_categories'))  # Redireciona para a lista de categorias
    else:  # Se for False, ocorreu um erro ao excluir
        return "Erro ao excluir a categoria", 400  # Retorna a mensagem de erro com código 400

