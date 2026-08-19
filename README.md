# EduLens

Plateforme intelligente de suivi et de prédiction de risque étudiant, disponible en version web (Flask) et bureau (PyQt6).

## 🎯 Fonctionnalités

- Gestion complète des profils étudiants (CRUD)
- Clustering K-Means pour regrouper les étudiants selon leurs profils
- Interface web (Flask) et interface bureau (PyQt6)
- Tableaux de bord de visualisation des données

## 🛠️ Stack technique

- **Backend / ML** : Python, scikit-learn (K-Means, Random Forest)
- **Web** : Flask
- **Desktop** : PyQt6
- **Base de données** : SQLite 

## 📦 Installation

```bash
# Cloner le repo
git clone https://github.com/Ali9104/edulens.git
cd edulens

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

## 🚀 Utilisation

**Version web (Flask) :**
```bash
python app.py
```
Puis ouvrir `http://localhost:5000` dans le navigateur.

**Version desktop (PyQt6) :**
```bash
python main_desktop.py
```

## 📊 Modèles ML

- **K-Means** : segmentation des étudiants en groupes selon leurs indicateurs de performance


## 📁 Structure du projet

```
edulens/
├── app.py                 # Point d'entrée version Flask
├── main_desktop.py        # Point d'entrée version PyQt6
├── models/                # Modèles ML (K-Means, Random Forest)
├── templates/              # Templates HTML (Flask)
├── static/                 # CSS / JS
├── requirements.txt
└── README.md
```

## 📸 Captures d'écran


## 👤 Auteur

**Ali Nouar** — Master Big Data, IA & Applications Avancées, Université Ibn Tofail
[LinkedIn](https://www.linkedin.com/in/ali-nouar-3b950a343/) · alinouar160@gmail.com
