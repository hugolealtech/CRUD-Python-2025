from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do SQLite em memória
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Modelo de dados
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    quantidade = db.Column(db.Integer, default=1)

    def to_dict(self): #está ligado ao flask e cria recebe os dados e retorna em JSON para a API
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'quantidade': self.quantidade
        }


# Cria as tabelas no banco de dados em memória
with app.app_context():
    db.create_all()


# Rotas da API

# POST - Criar um novo item
@app.route('/itens', methods=['POST'])
def criar_item():
    dados = request.get_json()

    if not dados or 'nome' not in dados:
        return jsonify({'erro': 'Dados inválidos ou nome não fornecido'}), 400

    novo_item = Item(
        nome=dados['nome'],
        descricao=dados.get('descricao', ''),
        quantidade=dados.get('quantidade', 1)
    )

    db.session.add(novo_item)
    db.session.commit()

    return jsonify(novo_item.to_dict()), 201


# GET - Listar todos os itens
@app.route('/itens', methods=['GET'])
def listar_itens():
    itens = Item.query.all()
    return jsonify([item.to_dict() for item in itens]), 200


# GET - Obter um item específico
@app.route('/itens/<int:item_id>', methods=['GET'])
def obter_item(item_id):
    item = Item.query.get(item_id)

    if item is None:
        return jsonify({'erro': 'Item não encontrado'}), 404

    return jsonify(item.to_dict()), 200


# PUT - Atualizar um item
@app.route('/itens/<int:item_id>', methods=['PUT'])
def atualizar_item(item_id):
    item = Item.query.get(item_id)

    if item is None:
        return jsonify({'erro': 'Item não encontrado'}), 404

    dados = request.get_json()

    if 'nome' in dados:
        item.nome = dados['nome']
    if 'descricao' in dados:
        item.descricao = dados['descricao']
    if 'quantidade' in dados:
        item.quantidade = dados['quantidade']

    db.session.commit()

    return jsonify(item.to_dict()), 200


# DELETE - Remover um item
@app.route('/itens/<int:item_id>', methods=['DELETE'])
def remover_item(item_id):
    item = Item.query.get(item_id)

    if item is None:
        return jsonify({'erro': 'Item não encontrado'}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({'mensagem': 'Item removido com sucesso'}), 200


if __name__ == '__main__':
    app.run(debug=True)