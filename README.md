
codex/create-.env.example-documentation

## Configuration des variables d'environnement

Copiez le fichier `.env.example` fourni à la racine du projet puis renommez-le en `.env` :

```bash
cp .env.example .env
```

Remplissez ensuite les valeurs requises :
- `DISCORD_TOKEN` : le token de votre bot Discord
- `EMAIL_ADDRESS` et `EMAIL_PASSWORD` : identifiants du compte qui enverra les résumés
- `RECIPIENT_EMAIL` : destinataire principal
- `TEST_RECIPIENT_EMAIL` : adresse de test pour les commandes de vérification

=======


# RPI_discordbot_coalffj
Bot discord qui résume les nouveau message du serveur Coalition FFJ et les envois par mail sur coalition_ffj@femmesdedroit.be (mailing list)

├─ requirements.txt                                             (librairies python nécessaires)
├─ Dockerfile                                                   (configuration du conteneur)
├─ railway.toml                                                 (configuration railway)
├─ .env                                                         (variables d'environnement et tokens secret)
├─ bot/
│       ├─ core.py                                              (script principal)
│       ├─ channel_lists.py                                     (gestion des canaux importants / exclus)
│       ├─ summarizer.py                                        (fonctionnalités de résumé)
│       ├─ discord_bot_commands.py                              (commandes du bot via Discord)
│       ├─ mails_managment.py                                   (fonctions pour gérer les envois de mails prod/test)
│
├─ tests/
│  ├─ test_env.py                                               (fonctions de tests et controle)
│  ├─ test_channel_lists.py
│  ├─ test_summarizer.py
│  ├─ test_mails.py
│  └─ test_bot_integration.py
│
├─ data/
│   ├─ important_channels.txt                   (liste des canaux important - messages intégrals)
│   ├─ excluded_channels.txt                    (liste des canaux non surveillés)
│   ├─ daily_summary.txt                        (daily report)
│   └─ weekly_summary.txt                       (weekly report)
├─ init_bot_stack.sh                            (installation rapide de Docker et lancement de la stack)

## Lancement rapide

Sur un Raspberry Pi ou toute machine fraîchement installée :

```bash
chmod +x init_bot_stack.sh
./init_bot_stack.sh
```

Le script installe Docker et docker-compose, clone ce dépôt puis démarre la stack Docker.

