# 🗳️ Telegram Election Results Scraper

Un outil Python développé pour suivre en temps réel les résultats de l'élection présidentielle camerounaise de 2025, en analysant automatiquement les publications du canal Telegram de l'influenceur Nzui Manto.

## 📖 Contexte

Lors de l'élection présidentielle au Cameroun, l'influenceur **Nzui Manto** partageait sur son canal Telegram les résultats provenant de différents bureaux de vote à travers le pays. 

Face au volume important de messages et à la nécessité d'avoir une vue d'ensemble rapide des tendances, cet outil a été créé pour :
- 📊 Extraire automatiquement les scores de chaque candidat
- 🔢 Calculer les totaux cumulés en temps réel
- 📈 Suivre l'évolution des tendances sans calculs manuels

## ⚙️ Fonctionnement

Le script analyse les messages du canal qui contiennent les résultats des bureaux de vote, généralement sous ce format :
```
Bureau de vote XYZ
Paul Biya: 450
Issa Tchiroma: 320
[autres candidats...]
```

Il extrait les scores, les cumule et génère un rapport complet.

## 🛠 Prérequis

- Python 3.7+
- Un compte Telegram
- Identifiants API Telegram (API_ID et API_HASH)

## 📦 Installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/votre-username/scrapping-telegram.git
cd scrapping-telegram
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install telethon python-dotenv
```

## ⚙️ Configuration

### 1. Obtenir vos identifiants Telegram API

1. Visitez [https://my.telegram.org](https://my.telegram.org)
2. Connectez-vous avec votre numéro
3. Section "API Development Tools"
4. Créez une application
5. Récupérez `API_ID` et `API_HASH`

### 2. Configurer le fichier .env

```bash
cp .env.template .env
```

Personnalisez selon vos besoins :

```env
# Vos identifiants Telegram
API_ID=votre_api_id
API_HASH=votre_api_hash
PHONE_NUMBER=+237XXXXXXXXX

# Canal à analyser (défaut: nzuimanto)
CHANNEL_USERNAME=nzuimanto

# Nombre de messages à scanner
MESSAGE_LIMIT=10000

# Candidats à suivre (séparés par virgules)
NAMES_TO_TRACK=Paul Biya,Issa Tchiroma,Candidat3

# Candidats devant obligatoirement apparaître ensemble
# (utile pour filtrer uniquement les messages de résultats complets)
REQUIRED_NAMES=Paul Biya,Issa Tchiroma

# Fichier de sortie
OUTPUT_FILE=resultats_election.txt

# Niveau de log
LOG_LEVEL=INFO
```

## 🚀 Utilisation

```bash
python script.py
```

**Première utilisation :**
- Un code de vérification sera envoyé sur Telegram
- Entrez-le dans le terminal
- La session sera sauvegardée pour les prochaines fois

## 📊 Exemple de Résultats

```
======================================
RÉSULTATS DU SCRAPING
======================================

📊 Paul Biya
   Nombre d'apparitions: 127
   Score total: 58,450

📊 Issa Tchiroma
   Nombre d'apparitions: 127
   Score total: 32,180

======================================
```

Le fichier détaillé inclut :
- Liste chronologique des messages analysés
- Scores par bureau de vote
- Métadonnées (ID message, date, heure)

## 🎯 Cas d'Usage

### Pendant l'élection
Suivre l'évolution des tendances en temps réel sans calculs manuels :
```bash
# Lancer toutes les 30 minutes pour avoir des mises à jour
python script.py
```

### Après l'élection
Analyser rétrospectivement les données pour :
- Vérifier la cohérence des résultats publiés
- Faire des analyses statistiques
- Étudier la chronologie des publications

## 🔧 Personnalisation

### Adapter à d'autres canaux
Modifiez simplement `CHANNEL_USERNAME` dans le `.env`

### Suivre d'autres candidats
Ajustez `NAMES_TO_TRACK` avec les noms exacts tels qu'ils apparaissent dans les messages

### Modifier le format d'extraction
Le pattern regex dans `extract_scores()` peut être adapté si le format des messages change :
```python
pattern = r"([A-Za-z\s]+):\s*(\d+)"
```

## ⚠️ Limitations

- Le script ne fonctionne que sur des **canaux publics** ou des canaux dont vous êtes membre
- Les résultats dépendent du format des messages publiés par la source
- Nécessite une connexion Internet stable
- Respect des limites de débit (rate limits) de l'API Telegram

## 🔐 Sécurité

- ⚠️ Ne partagez **JAMAIS** votre fichier `.env`
- 🔒 Le fichier `session_name.session` contient vos identifiants de connexion
- 🚫 Ajoutez `.env` et `*.session` au `.gitignore` (déjà fait)

## 📝 Note Légale

Cet outil a été développé à des fins d'analyse personnelle et éducative. L'utilisateur est responsable de :
- Respecter les conditions d'utilisation de Telegram
- Se conformer aux lois locales sur la protection des données
- Utiliser les informations de manière responsable et éthique

## 🤝 Contribution

Ce projet est un exemple concret d'automatisation appliquée à un besoin réel. N'hésitez pas à :
- Proposer des améliorations
- Adapter le code à d'autres contextes (sports, sondages, etc.)
- Partager vos retours d'expérience

## 📜 Licence

Apache License 2.0 - Voir [LICENSE](LICENSE)

---

**Développé pendant l'élection présidentielle camerounaise de 2025**  
*"Quand la programmation rencontre la citoyenneté active"*
