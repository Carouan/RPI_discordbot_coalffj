# Déploiement conteneurisé et automatisé d’un bot Discord Python sur Raspberry Pi avec CI/CD : Approche systémique et reproductible à visée doctorale

Ce document propose une approche avancée, orientée recherche, pour le déploiement automatisé d’un agent Discord écrit en Python sur une architecture ARM comme le Raspberry Pi. L’intégration complète de conteneurs Docker, la mise en œuvre de pipelines CI/CD, ainsi que la supervision continue via des outils libres, font de ce guide un canevas adaptable pour la mise en œuvre de microservices orientés événementiels. L’ensemble respecte les standards des environnements GLO (Gratuits, Libres, Open-source) et répond aux exigences d'une infrastructure de recherche ou de prototypage reproductible.

---

## 1. Architecture générale : fondements et finalité

Le paradigme retenu repose sur l’orchestration de conteneurs par **Docker Compose**, permettant de garantir l’indépendance des services, leur résilience, ainsi que leur interopérabilité. L’architecture vise les objectifs suivants :

- **Intégration continue automatisée** : toute modification apportée au dépôt déclenche un redéploiement sans intervention manuelle.
- **Observabilité native** : chaque composant est supervisé de façon granulaire pour détecter anomalies et interruptions de service.
- **Portabilité et reproductibilité** : l’ensemble de l’environnement est modélisé sous forme déclarative, facilitant le clonage sur tout hôte ARM/Linux.

Les modules suivants sont intégrés :

- **Docker Compose** pour l’agencement des conteneurs.
- **Gitea** (ou GitHub) pour le versionnement distribué.
- **Woodpecker CI** pour la chaîne CI/CD entièrement libre.
- **Uptime Kuma** comme solution d’observabilité légère et efficace.
- **Webhooks Discord** pour l'intégration de feedback utilisateur en temps réel.

---

## 2. Modélisation du dépôt et conteneurisation de l’agent

### Schéma d’organisation

```
.
├── docker-compose.yml
├── bot
│   ├── main.py
│   ├── requirements.txt
│   └── .env
├── .woodpecker.yml
└── README.md
```

### Dépendances du bot

```text
# requirements.txt
discord.py
python-dotenv
```

### Image Docker de l’agent Discord

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

Ce fichier Dockerfile assure un environnement isolé, optimisé pour ARMv7/v8. Il permet une installation déterministe des dépendances Python, en cohérence avec les bonnes pratiques de la science ouverte.

### Orchestration `docker-compose.yml`

```yaml
version: '3.8'
services:
  bot:
    build: ./bot
    env_file: ./bot/.env
    restart: always

  gitea:
    image: gitea/gitea:latest
    volumes:
      - ./data/gitea:/data
    ports:
      - "3000:3000"
      - "222:22"
    restart: always

  woodpecker-server:
    image: woodpeckerci/woodpecker-server:latest
    environment:
      - WOODPECKER_OPEN=true
      - WOODPECKER_GITEA=true
      - WOODPECKER_GITEA_URL=http://gitea:3000
      - WOODPECKER_GITEA_CLIENT=xxx
      - WOODPECKER_GITEA_SECRET=yyy
    volumes:
      - ./data/woodpecker:/var/lib/woodpecker
    ports:
      - "8000:8000"
    restart: always

  woodpecker-agent:
    image: woodpeckerci/woodpecker-agent:latest
    environment:
      - WOODPECKER_SERVER=woodpecker-server:9000
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    restart: always

  uptime-kuma:
    image: louislam/uptime-kuma:latest
    ports:
      - "3001:3001"
    volumes:
      - ./monitoring/uptime-kuma:/app/data
    restart: always
```

Cette configuration formalise une infrastructure distribuée en multi-conteneurs, avec résilience intégrée et couplage faible entre les services.

---

## 3. Intégration et livraison continues (CI/CD)

### Configuration de pipeline `.woodpecker.yml`

```yaml
pipeline:
  deploy:
    image: docker:cli
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    commands:
      - docker compose down
      - docker compose build
      - docker compose up -d
```

### Chaînage du processus CI/CD

1. **Gitea** déclenche un **webhook** suite à un `git push`.
2. Le **serveur Woodpecker** reçoit la requête, et assigne un job à un **agent CI**.
3. L’agent reconstruit l’image, arrête l’ancienne instance et déploie la nouvelle.
4. Une notification finale peut être émise sur Discord via un webhook REST.

Cette démarche repose sur une boucle de rétroaction continue, essentielle à tout cycle DevOps reproductible.

---

## 4. Supervision applicative et notifications

### Uptime Kuma comme solution GLO

Uptime Kuma est intégré à l’infrastructure pour fournir une métrique de disponibilité précise. Ses fonctionnalités incluent :

- Tests HTTP, TCP, Ping configurables.
- Alertes configurables par webhook, email, Telegram, etc.
- Historique exportable des incidents pour analyse a posteriori.

Accessible via : `http://localhost:3001`

### Intégration d’un webhook Discord

```bash
curl -H "Content-Type: application/json" \
     -X POST \
     -d '{"content": "✅ Déploiement du bot terminé avec succès."}' \
     https://discord.com/api/webhooks/xxx/yyyy
```

Cela permet de documenter le fonctionnement du processus dans un canal Discord privé ou dédié à la supervision.

---

## 5. Déploiement initial reproductible

```bash
# Clonage du dépôt
$ git clone https://github.com/monutilisateur/discord-bot.git
$ cd discord-bot

# Lancement des services
$ docker compose up -d --build
```

Interfaces accessibles :

- **Gitea** → [http://localhost:3000](http://localhost:3000)
- **Woodpecker CI** → [http://localhost:8000](http://localhost:8000)
- **Uptime Kuma** → [http://localhost:3001](http://localhost:3001)

---

## 6. Pistes de développement et amélioration continue

- Mise en place d’un **reverse proxy** avec Let’s Encrypt (Traefik ou Caddy) pour gestion SSL automatique.
- Ajout de **tests unitaires automatisés** exécutés dans le pipeline CI.
- Centralisation des logs via **Loki + Promtail** (en alternative GLO à ELK).
- Sauvegarde automatisée des volumes Docker (ex. avec Restic).
- Intégration à une **architecture orientée microservices** avec événements MQTT ou Redis.

---

## 7. Tests unitaires et validation continue

La robustesse du bot peut être renforcée par l'intégration de tests unitaires. Utilisez `unittest` ou `pytest` pour créer des tests automatisés dans un fichier `test_core.py`. Exemple :

```python
import unittest
from unittest.mock import patch
from core import handle_event

class TestBot(unittest.TestCase):
    def test_handle_event(self):
        event = {"type": "MESSAGE_CREATE", "content": "ping"}
        response = handle_event(event)
        self.assertEqual(response, "pong")
```

Ce test peut être intégré dans le pipeline CI avec une étape de test avant le build :

```yaml
pipeline:
  test:
    image: python:3.11
    commands:
      - pip install -r bot/requirements.txt
      - python -m unittest discover -s bot
```

---

## 8. Interface de supervision web personnalisée

Pour exposer des métriques ou logs du bot à l’utilisateur ou à l’administrateur, une interface peut être générée avec **NiceGUI** (GLO). Exemple minimal :

```python
from nicegui import ui

@ui.page("/")
def main():
    ui.label("Statut du bot : en ligne ✅")
    ui.button("Redémarrer", on_click=lambda: print("Redémarrage..."))

ui.run()
```

Cette interface peut être intégrée dans `docker-compose.yml` en tant que service supplémentaire accessible sur un autre port.

---

## 9. Script Bash d’initialisation

Voici un script `init_bot_stack.sh` permettant d’automatiser le déploiement depuis un Raspberry Pi ou une machine fraîchement installée :

```bash
#!/bin/bash

# Installation des paquets nécessaires
sudo apt update && sudo apt install -y docker.io docker-compose git

# Clonage du projet
git clone https://github.com/monutilisateur/discord-bot.git
cd discord-bot

# Lancement de la stack
sudo docker compose up -d --build
```

Ce script peut être placé dans le dépôt et référencé dans le README.md pour initier rapidement une nouvelle machine ou un nouveau contributeur.

---

## Conclusion scientifique

Ce dispositif représente une implémentation rigoureuse de pratiques DevOps modernes, intégrant des outils libres dans une logique d'automatisation, d'isolation des services et de portabilité. L’intégration de pipelines CI/CD, la surveillance temps réel et la conteneurisation du code permettent d’envisager des itérations rapides, une haute disponibilité, ainsi qu’un transfert aisé des connaissances et des ressources. Ce guide constitue une base méthodologique pour des travaux de recherche ou de déploiement académique dans les domaines de l’IA embarquée, de l’automatisation distribuée ou de la gouvernance numérique éthique.

