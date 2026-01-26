const express = require('express');
const cors = require('cors');
const app = express();
const port = 8080;

// Middleware
app.use(cors());
app.use(express.json());

// Stockage temporaire des utilisateurs (en mémoire)
let users = [];

// Endpoint d'inscription
app.post('/api/users/register', (req, res) => {
    const { username, email, password, poids, taille, age } = req.body;

    // Validation basique
    if (!username || !email || !password || !poids || !taille || !age) {
        return res.status(400).json({ error: 'Tous les champs sont requis' });
    }

    if (password.length < 6) {
        return res.status(400).json({ error: 'Le mot de passe doit contenir au moins 6 caractères' });
    }

    // Vérifier si l'utilisateur existe déjà
    const existingUser = users.find(user => user.email === email);
    if (existingUser) {
        return res.status(400).json({ error: 'Cet email est déjà utilisé' });
    }

    // Créer l'utilisateur
    const newUser = {
        id: users.length + 1,
        username,
        email,
        password, // En production, il faudrait hasher le mot de passe
        poids: parseFloat(poids),
        taille: parseInt(taille),
        age: parseInt(age),
        createdAt: new Date()
    };

    users.push(newUser);

    console.log('Nouvel utilisateur inscrit:', newUser);

    res.status(200).json({
        id: newUser.id,
        username: newUser.username,
        email: newUser.email,
        poids: newUser.poids,
        taille: newUser.taille,
        age: newUser.age
    });
});

// Endpoint de connexion
app.post('/api/users/login', (req, res) => {
    const { email, password } = req.body;

    if (!email || !password) {
        return res.status(400).json({ error: 'Email et mot de passe requis' });
    }

    // Trouver l'utilisateur
    const user = users.find(u => u.email === email && u.password === password);

    if (!user) {
        return res.status(401).json({ error: 'Email ou mot de passe incorrect' });
    }

    console.log('Utilisateur connecté:', user.email);

    res.status(200).json({
        id: user.id,
        username: user.username,
        email: user.email,
        poids: user.poids,
        taille: user.taille,
        age: user.age
    });
});

// Endpoint pour obtenir tous les utilisateurs (pour debug)
app.get('/api/users', (req, res) => {
    res.json(users);
});

// Démarrer le serveur
app.listen(port, () => {
    console.log(`🚀 Serveur backend démarré sur http://localhost:${port}`);
    console.log(`📝 Endpoint inscription: POST http://localhost:${port}/api/users/register`);
    console.log(`🔐 Endpoint connexion: POST http://localhost:${port}/api/users/login`);
    console.log(`👥 Liste utilisateurs: GET http://localhost:${port}/api/users`);
});