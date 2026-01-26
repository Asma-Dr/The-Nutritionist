from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permettre les requêtes CORS

# Stockage temporaire des utilisateurs (en mémoire)
users = []

@app.route('/api/users/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validation des champs requis
    required_fields = ['username', 'email', 'password', 'poids', 'taille', 'age']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Le champ {field} est requis'}), 400

    username = data['username']
    email = data['email']
    password = data['password']
    poids = data['poids']
    taille = data['taille']
    age = data['age']

    # Validation du mot de passe
    if len(password) < 6:
        return jsonify({'error': 'Le mot de passe doit contenir au moins 6 caractères'}), 400

    # Vérifier si l'utilisateur existe déjà
    for user in users:
        if user['email'] == email:
            return jsonify({'error': 'Cet email est déjà utilisé'}), 400

    # Créer l'utilisateur
    new_user = {
        'id': len(users) + 1,
        'username': username,
        'email': email,
        'password': password,  # En production, il faudrait hasher le mot de passe
        'poids': float(poids),
        'taille': int(taille),
        'age': int(age),
        'created_at': datetime.now().isoformat()
    }

    users.append(new_user)

    print(f'✅ Nouvel utilisateur inscrit: {new_user["email"]}')

    # Retourner l'utilisateur sans le mot de passe
    response_user = {k: v for k, v in new_user.items() if k != 'password'}
    return jsonify(response_user), 200

@app.route('/api/users/login', methods=['POST'])
def login():
    data = request.get_json()

    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email et mot de passe requis'}), 400

    email = data['email']
    password = data['password']

    # Trouver l'utilisateur
    for user in users:
        if user['email'] == email and user['password'] == password:
            print(f'✅ Utilisateur connecté: {email}')
            # Retourner l'utilisateur sans le mot de passe
            response_user = {k: v for k, v in user.items() if k != 'password'}
            return jsonify(response_user), 200

    return jsonify({'error': 'Email ou mot de passe incorrect'}), 401

@app.route('/api/users', methods=['GET'])
def get_users():
    # Retourner tous les utilisateurs sans les mots de passe
    safe_users = [{k: v for k, v in user.items() if k != 'password'} for user in users]
    return jsonify(safe_users), 200

if __name__ == '__main__':
    print("🚀 Serveur backend Python démarré sur http://localhost:5000")
    print("📝 Endpoint inscription: POST /api/users/register")
    print("🔐 Endpoint connexion: POST /api/users/login")
    print("👥 Liste utilisateurs: GET /api/users")
    app.run(debug=True, port=5000, host='0.0.0.0')