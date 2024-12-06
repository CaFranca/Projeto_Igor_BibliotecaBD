from flask import Flask
# Importa a configuração do banco de dados e as funções para inicialização
from database import database, init_database
from controller.AutorController import authorController
from controller.LivroController import livroController
from controller.CategoriasController import categoryController
from controller.Iniciocontroller import padraoController


app = Flask(__name__)


init_database(app)

# O parâmetro `url_prefix="/authors"` define que todas as rotas nesse blueprint terão o prefixo "/authors"
# Por exemplo, "/authors/<id>" para visualizar um autor específico
app.register_blueprint(authorController, url_prefix="/authors")

# O prefixo "/books" agrupa as rotas sob o contexto de livros, como "/books/<id>"
app.register_blueprint(livroController, url_prefix="/books")

# O prefixo "/categories" facilita a organização das rotas, por exemplo, "/categories/<id>"
app.register_blueprint(categoryController, url_prefix="/categories")

# O prefixo "/" significa que as rotas do `padraoController` serão acessíveis na raiz do site
app.register_blueprint(padraoController, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True)
