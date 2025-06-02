# 🐍 Instalação do Flask (Backend)

Este documento fornece um guia básico para instalação e configuração do **Flask**, um microframework web em Python, utilizado para desenvolvimento de aplicações web.

---

## 🔧 Pré-requisitos

- **Python** instalado (versão 3.8 ou superior recomendada).

Verifique a instalação com o comando:

```bash
python --version
ou


python3 --version
🚀 Passos para instalação
Crie um ambiente virtual (recomendado):

No Windows:


python -m venv venv
venv\Scripts\activate
No Linux/macOS:


python3 -m venv venv
source venv/bin/activate
Instale o Flask:


pip install flask
(Opcional) Gere um arquivo requirements.txt para registrar as dependências do projeto:


pip freeze > requirements.txt
Execute sua aplicação Flask:

Forma direta:


python app.py
Ou usando o comando flask:



flask run 