from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:98M66k51h39$@localhost/makitDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle de la table `transactions_togo`
class TransactionTogo(db.Model):
    __tablename__ = 'transactions_togo'  # Table pour le Togo
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    montant = db.Column(db.Float, nullable=False)
    frais = db.Column(db.Float, nullable=False, default=0)
    benefice = db.Column(db.Float, nullable=False)
    type_transfert = db.Column(db.String(50), nullable=False)  # "Envoi" ou "Retrait"

    def calculer_benefice(self):
        # Cas spécial pour le "Retrait"
        if self.type_transfert == "Retrait":
            self.frais = 0  # Les frais sont nuls pour un retrait

        # Liste de tuples pour stocker les intervalles et les bénéfices correspondants
        intervalles_benefices = [
            (600000, float('inf'), lambda m: m * 0.03),
            (300000, 600000, lambda m: 11100),
            (210000, 300000, lambda m: 8100),
            (150000, 210000, lambda m: 6000),
            (102000, 150000, lambda m: 5100),
            (60000, 102000, lambda m: 3600),
            (30000, 60000, lambda m: 2400),
            (6000, 30000, lambda m: 1500),
            (0, 6000, lambda m: 900),
        ]

        # Trouver l'intervalle correspondant au montant
        for min_montant, max_montant, calcul_benefice in intervalles_benefices:
            if min_montant < self.montant <= max_montant:
                self.benefice = calcul_benefice(self.montant) - self.frais
                return self.benefice

        # Si aucun intervalle n'est trouvé (cas par défaut)
        self.benefice = 900 - self.frais
        return self.benefice

# Modèle de la table `transactions_cote_ivoire`
class TransactionCoteIvoire(db.Model):
    __tablename__ = 'transactions_cote_ivoire'  # Table pour la Côte d'Ivoire
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    montant = db.Column(db.Float, nullable=False)
    frais = db.Column(db.Float, nullable=False, default=0)
    benefice = db.Column(db.Float, nullable=False)
    type_transfert = db.Column(db.String(50), nullable=False)  # "Envoi" ou "Retrait"

    def calculer_benefice(self):
        # Cas spécial pour le "Retrait"
        if self.type_transfert == "Retrait":
            self.frais = 0  # Les frais sont nuls pour un retrait

        # Liste de tuples pour stocker les intervalles et les bénéfices correspondants
        intervalles_benefices = [
            (600000, float('inf'), lambda m: m * 0.035),
            (300000, 600000, lambda m: 14400),
            (210000, 300000, lambda m: 10800),
            (150000, 210000, lambda m: 8100),
            (102000, 150000, lambda m: 6600),
            (60000, 102000, lambda m: 4500),
            (30000, 60000, lambda m: 2700),
            (6000, 30000, lambda m: 1500),
            (0, 6000, lambda m: 900),
        ]

        # Trouver l'intervalle correspondant au montant
        for min_montant, max_montant, calcul_benefice in intervalles_benefices:
            if min_montant < self.montant <= max_montant:
                self.benefice = calcul_benefice(self.montant) - self.frais
                return self.benefice

        # Si aucun intervalle n'est trouvé (cas par défaut)
        self.benefice = 900 - self.frais
        return self.benefice

# Modèle de la table `transactions_niger`
class TransactionNiger(db.Model):
    __tablename__ = 'transactions_niger'  # Table pour le Niger
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    montant = db.Column(db.Float, nullable=False)
    frais = db.Column(db.Float, nullable=False, default=0)
    benefice = db.Column(db.Float, nullable=False)
    type_transfert = db.Column(db.String(50), nullable=False)  # "Envoi" ou "Retrait"

    def calculer_benefice(self):
        # Cas spécial pour le "Retrait"
        if self.type_transfert == "Retrait":
            self.frais = 0  # Les frais sont nuls pour un retrait

        # Liste de tuples pour stocker les intervalles et les bénéfices correspondants
        intervalles_benefices = [
            (600000, float('inf'), lambda m: m * 0.035),
            (300000, 600000, lambda m: 14400),
            (210000, 300000, lambda m: 10800),
            (150000, 210000, lambda m: 8100),
            (102000, 150000, lambda m: 6600),
            (60000, 102000, lambda m: 4500),
            (30000, 60000, lambda m: 2700),
            (6000, 30000, lambda m: 1500),
            (0, 6000, lambda m: 900),
        ]

        # Trouver l'intervalle correspondant au montant
        for min_montant, max_montant, calcul_benefice in intervalles_benefices:
            if min_montant < self.montant <= max_montant:
                self.benefice = calcul_benefice(self.montant) - self.frais
                return self.benefice

        # Si aucun intervalle n'est trouvé (cas par défaut)
        self.benefice = 900 - self.frais
        return self.benefice

# Créer la base de données et les tables
with app.app_context():
    db.create_all()

#######################
# Routes pour le Togo #
#######################

@app.route('/add_transaction_togo', methods=['POST'])
def add_transaction_togo():
    data = request.json
    montant = data.get('montant')
    frais = data.get('frais', 0)  # Frais par défaut à 0
    type_transfert = data.get('type_transfert')  # "Envoi" ou "Retrait"

    if montant is None or type_transfert is None:
        return jsonify({"error": "Montant et type de transfert sont requis"}), 400

    if type_transfert == "Retrait":
        montant *= 60  # Multiplier par 60 pour les retraits

    new_transaction = TransactionTogo(
        montant=montant,
        frais=frais,
        type_transfert=type_transfert
    )
    new_transaction.calculer_benefice()  # Calculer le bénéfice
    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({"message": "Transaction ajoutée avec succès !", "id": new_transaction.id}), 201

@app.route('/get_history_togo', methods=['GET'])
def get_history_togo():
    transactions = TransactionTogo.query.all()
    history = [{
        "id": t.id,
        "date": t.date.strftime('%Y-%m-%d %H:%M:%S'),
        "montant": t.montant,
        "frais": t.frais,
        "benefice": t.benefice,
        "type_transfert": t.type_transfert
    } for t in transactions]
    return jsonify(history), 200

# Route pour modifier une transaction pour le Togo
@app.route('/update_transaction_togo/<int:id>', methods=['PUT'])
def update_transaction_togo(id):
    data = request.json
    transaction = TransactionTogo.query.get_or_404(id)

    montant = data.get('montant')
    frais = data.get('frais')
    type_transfert = data.get('type_transfert')

    if montant is not None:
        transaction.montant = montant
    if frais is not None:
        transaction.frais = frais
    if type_transfert is not None:
        transaction.type_transfert = type_transfert

    transaction.calculer_benefice()  # Recalculer le bénéfice
    db.session.commit()

    return jsonify({"message": "Transaction mise à jour avec succès !"}), 200

# Route pour supprimer une transaction pour le Togo
@app.route('/delete_transaction_togo/<int:id>', methods=['DELETE'])
def delete_transaction_togo(id):
    transaction = TransactionTogo.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction supprimée avec succès !"}), 200

###############################
# Routes pour la Côte d'Ivoire #
###############################

@app.route('/add_transaction_cote_ivoire', methods=['POST'])
def add_transaction_cote_ivoire():
    data = request.json
    montant = data.get('montant')
    frais = data.get('frais', 0)  # Frais par défaut à 0
    type_transfert = data.get('type_transfert')  # "Envoi" ou "Retrait"

    if montant is None or type_transfert is None:
        return jsonify({"error": "Montant et type de transfert sont requis"}), 400

    if type_transfert == "Retrait":
        montant *=60  # Multiplier par 60 pour les retraits
        frais = 0  # Frais à 0 pour les retraits

    new_transaction = TransactionCoteIvoire(
        montant=montant,
        frais=frais,
        type_transfert=type_transfert
    )
    new_transaction.calculer_benefice()  # Calculer le bénéfice
    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({"message": "Transaction ajoutée avec succès !", "id": new_transaction.id}), 201

@app.route('/get_history_cote_ivoire', methods=['GET'])
def get_history_cote_ivoire():
    transactions = TransactionCoteIvoire.query.all()
    history = [{
        "id": t.id,
        "date": t.date.strftime('%Y-%m-%d %H:%M:%S'),
        "montant": t.montant,
        "frais": t.frais,
        "benefice": t.benefice,
        "type_transfert": t.type_transfert
    } for t in transactions]
    return jsonify(history), 200

# Route pour modifier une transaction pour la Côte d'Ivoire
@app.route('/update_transaction_cote_ivoire/<int:id>', methods=['PUT'])
def update_transaction_cote_ivoire(id):
    data = request.json
    transaction = TransactionCoteIvoire.query.get_or_404(id)

    montant = data.get('montant')
    frais = data.get('frais')
    type_transfert = data.get('type_transfert')

    if montant is not None:
        transaction.montant = montant
    if frais is not None:
        transaction.frais = frais
    if type_transfert is not None:
        transaction.type_transfert = type_transfert

    transaction.calculer_benefice()  # Recalculer le bénéfice
    db.session.commit()

    return jsonify({"message": "Transaction mise à jour avec succès !"}), 200

# Route pour supprimer une transaction pour la Côte d'Ivoire
@app.route('/delete_transaction_cote_ivoire/<int:id>', methods=['DELETE'])
def delete_transaction_cote_ivoire(id):
    transaction = TransactionCoteIvoire.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction supprimée avec succès !"}), 200


#######################
# Routes pour le Niger #
#######################

@app.route('/add_transaction_niger', methods=['POST'])
def add_transaction_niger():
    data = request.json
    montant = data.get('montant')
    frais = data.get('frais', 0)  # Frais par défaut à 0
    type_transfert = data.get('type_transfert')  # "Envoi" ou "Retrait"

    if montant is None or type_transfert is None:
        return jsonify({"error": "Montant et type de transfert sont requis"}), 400

    if type_transfert == "Retrait":
        montant *= 60  # Multiplier par 60 pour les retraits
        frais = 0  # Frais à 0 pour les retraits

    new_transaction = TransactionNiger(
        montant=montant,
        frais=frais,
        type_transfert=type_transfert
    )
    new_transaction.calculer_benefice()  # Calculer le bénéfice
    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({"message": "Transaction ajoutée avec succès !", "id": new_transaction.id}), 201

@app.route('/get_history_niger', methods=['GET'])
def get_history_niger():
    transactions = TransactionNiger.query.all()
    history = [{
        "id": t.id,
        "date": t.date.strftime('%Y-%m-%d %H:%M:%S'),
        "montant": t.montant,
        "frais": t.frais,
        "benefice": t.benefice,
        "type_transfert": t.type_transfert
    } for t in transactions]
    return jsonify(history), 200

# Route pour modifier une transaction pour le Niger
@app.route('/update_transaction_niger/<int:id>', methods=['PUT'])
def update_transaction_niger(id):
    data = request.json
    transaction = TransactionNiger.query.get_or_404(id)

    montant = data.get('montant')
    frais = data.get('frais')
    type_transfert = data.get('type_transfert')

    if montant is not None:
        transaction.montant = montant
    if frais is not None:
        transaction.frais = frais
    if type_transfert is not None:
        transaction.type_transfert = type_transfert

    transaction.calculer_benefice()  # Recalculer le bénéfice
    db.session.commit()

    return jsonify({"message": "Transaction mise à jour avec succès !"}), 200

# Route pour supprimer une transaction pour le Niger
@app.route('/delete_transaction_niger/<int:id>', methods=['DELETE'])
def delete_transaction_niger(id):
    transaction = TransactionNiger.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction supprimée avec succès !"}), 200


# Route pour récupérer toutes les transactions
@app.route('/get_all_transactions', methods=['GET'])
def get_all_transactions():
    transactions_togo = TransactionTogo.query.all()
    transactions_cote_ivoire = TransactionCoteIvoire.query.all()
    transactions_niger = TransactionNiger.query.all()

    all_transactions = []
    for t in transactions_togo:
        all_transactions.append({
            "pays": "Togo",
            "id": t.id,
            "date": t.date.strftime('%Y-%m-%d %H:%M:%S'),
            "montant": t.montant,
            "frais": t.frais,
            "benefice": t.benefice,
            "type_transfert": t.type_transfert
        })
    for t in transactions_cote_ivoire:
        all_transactions.append({
            "pays": "Côte d'Ivoire",
            "id": t.id,
            "date": t.date.strftime('%Y-%m-%d %H:%M:%S'),
            "montant": t.montant,
            "frais": t.frais,
            "benefice": t.benefice,
            "type_transfert": t.type_transfert
        })
    for t in transactions_niger:
        all_transactions.append({
            "pays": "Niger",
            "id": t.id,
            "date": t.date.strftime('%Y-%m-%d %H:%M:%S'),
            "montant": t.montant,
            "frais": t.frais,
            "benefice": t.benefice,
            "type_transfert": t.type_transfert
        })

    return jsonify(all_transactions), 200

# Démarrer l'application Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)