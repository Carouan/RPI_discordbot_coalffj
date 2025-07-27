#!/bin/bash
set -e

# Installation des paquets nécessaires
sudo apt update && sudo apt install -y docker.io docker-compose git

# Clonage du projet
REPO_URL="https://github.com/Carouan/RPI_discordbot_coalffj.git"
TARGET_DIR="discord-bot"

if [ ! -d "$TARGET_DIR" ]; then
    git clone "$REPO_URL" "$TARGET_DIR"
fi
cd "$TARGET_DIR"

# Lancement de la stack
sudo docker compose up -d --build
