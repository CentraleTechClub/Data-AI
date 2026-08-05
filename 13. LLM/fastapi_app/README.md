Assistant local FastAPI

Prérequis
- Python 3.10+
- `pip install fastapi uvicorn transformers torch`

Téléchargement du modèle Gemma
- L'application fonctionne uniquement avec un modèle local déjà présent dans `assets/gemma-3-1b-it`.
- Si le modèle n'est pas encore téléchargé, vous devez d'abord créer un compte Hugging Face.
- Pour Gemma, il peut aussi falloir accepter la licence de la page du modèle avant de pouvoir récupérer les poids.
- Si Hugging Face demande une authentification, créez un token d'accès en lecture et stockez-le dans `.env` sous la forme `HF_TOKEN=hf_...`.
- Le fichier `.env` ne doit pas être versionné.

Démarrage rapide
1. Depuis la racine du dépôt, lancez :
```bash
pip install -r requirements.txt  # optionnel si vous créez ce fichier
uvicorn Workshop_7.fastapi_app.main:app --reload --host 0.0.0.0 --port 8000
```
2. Ouvrez http://localhost:8000 dans votre navigateur.

Si le modèle Gemma doit encore être récupéré, faites d'abord la procédure Hugging Face suivante :
1. Créez un compte sur https://huggingface.co/
2. Ouvrez la page du modèle Gemma utilisé par le cours et acceptez la licence si elle est proposée
3. Allez dans `Settings` puis `Access Tokens`
4. Créez un token `Read`
5. Ajoutez-le dans votre `.env` :
```bash
HF_TOKEN=hf_votre_token
```
6. Téléchargez le modèle dans `assets/gemma-3-1b-it` avant de lancer l'application

Structure de l'application
- `main.py` : application FastAPI, montage de `/static`, rendu des templates et chargement du modèle depuis `assets/gemma-3-1b-it`.
- `templates/index.html` : page unique avec formulaire et affichage du résultat.
- `static/style.css` : styles de application.
- `assets/` : dossier attendu pour le modèle, non versionné ici.

Remarques
- L'application détecte CUDA et choisit le device automatiquement. Modifiez `device` dans `main.py` pour forcer CPU ou GPU.
- Si le dossier du modèle est volumineux, gardez-le hors de Git et pointez `MODEL_PATH` vers un emplacement externe.
- Pour un déploiement sans `--reload`, retirez l'option et exécutez l'application derrière un gestionnaire de processus.

