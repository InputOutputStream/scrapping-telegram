from telethon import TelegramClient
import re
from datetime import datetime
from collections import defaultdict
import os
from dotenv import load_dotenv

# Charger les variables du fichier .env
load_dotenv()

# Configuration depuis les variables d'environnement
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "nzuimanto")
MESSAGE_LIMIT = int(os.getenv("MESSAGE_LIMIT", 10000))
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "resultats_scraping.txt")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Noms à tracker
NAMES_TO_TRACK = [name.strip() for name in os.getenv("NAMES_TO_TRACK", "").split(",")]

# Noms obligatoires (doivent tous être présents dans le message)
REQUIRED_NAMES = [name.strip() for name in os.getenv("REQUIRED_NAMES", "").split(",")]

# Validation des configurations
def validate_config():
    """Vérifie que toutes les configurations requises sont présentes"""
    if not API_ID or not API_HASH or not PHONE_NUMBER:
        raise ValueError("❌ Erreur: API_ID, API_HASH et PHONE_NUMBER sont requis dans le fichier .env")
    if not CHANNEL_USERNAME:
        raise ValueError("❌ Erreur: CHANNEL_USERNAME est requis dans le fichier .env")
    if not NAMES_TO_TRACK or NAMES_TO_TRACK == ['']:
        raise ValueError("❌ Erreur: NAMES_TO_TRACK doit être configuré dans le fichier .env")
    print("✓ Configuration validée")

class MessageScraper:
    def __init__(self):
        self.results = defaultdict(lambda: {"messages": [], "total": 0})
    
    def extract_scores(self, text):
        """Extrait les noms et leurs scores associés du message"""
        scores = {}
        
        # Pattern pour matcher "Nom: chiffre"
        pattern = r"([A-Za-z\s]+):\s*(\d+)"
        matches = re.findall(pattern, text)
        
        for name, score in matches:
            name = name.strip()
            # Vérifier si le nom est dans notre liste
            for tracked_name in NAMES_TO_TRACK:
                if tracked_name.lower() in name.lower():
                    scores[tracked_name] = int(score)
                    break
        
        return scores
    
    def process_message(self, message_text, message_id, message_date):
        """Traite un message et extrait les données"""
        scores = self.extract_scores(message_text)
        
        # Vérifier que le message contient au moins Paul Biya ET Issa Tchiroma
        if "Paul Biya" in scores and "Issa Tchiroma" in scores:
            
            message_data = {
                "id": message_id,
                "date": message_date,
                "text": message_text,
                "scores": scores
            }
            
            # Ajouter les données pour chaque nom trouvé
            for name, score in scores.items():
                self.results[name]["messages"].append(message_data)
                self.results[name]["total"] += score
    
    async def scrape_channel(self):
        """Scrape le canal et traite les messages"""
        
        client = TelegramClient("session_name", int(API_ID), API_HASH)
        
        try:
            await client.start(phone=PHONE_NUMBER)
            print("✓ Connecté à Telegram")
            
            # Accéder au canal
            channel = await client.get_entity(CHANNEL_USERNAME)
            print(f"✓ Canal trouvé: {channel.title}")
            
            message_count = 0
            matching_messages = 0
            
            # Récupérer les messages du canal
            async for message in client.iter_messages(channel, limit=10000):
                if message.text:
                    message_count += 1
                    
                    # Vérifier s'il y a les deux noms requis
                    if "Paul Biya" in message.text and "Issa Tchiroma" in message.text:
                        self.process_message(
                            message.text,
                            message.id,
                            message.date
                        )
                        matching_messages += 1
            
            print(f"\n✓ {message_count} messages scannés")
            print(f"✓ {matching_messages} messages avec Paul Biya ET Issa Tchiroma trouvés\n")
            
            self.display_results()
            self.save_results()
            
        except Exception as e:
            print(f"✗ Erreur: {e}")
        finally:
            await client.disconnect()
    
    def display_results(self):
        """Affiche les résultats dans la console"""
        print("="*60)
        print("RÉSULTATS DU SCRAPING")
        print("="*60)
        
        for name in NAMES_TO_TRACK:
            if name in self.results and self.results[name]["messages"]:
                data = self.results[name]
                print(f"\n📊 {name}")
                print(f"   Nombre d'apparitions: {len(data['messages'])}")
                print(f"   Score total: {data['total']}")
        
        print("\n" + "="*60)
    
    def save_results(self, filename="resultats_scraping.txt"):
        """Sauvegarde les résultats dans un fichier"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write("RÉSULTATS DU SCRAPING TELEGRAM\n")
            f.write(f"Date d'export: {datetime.now()}\n")
            f.write("="*60 + "\n\n")
            
            # Résumé
            f.write("RÉSUMÉ\n")
            f.write("-"*60 + "\n")
            for name in NAMES_TO_TRACK:
                if name in self.results and self.results[name]["messages"]:
                    data = self.results[name]
                    f.write(f"{name}: {data['total']} (apparitions: {len(data['messages'])})\n")
            
            f.write("\n" + "="*60 + "\n\n")
            
            # Détail des messages
            f.write("DÉTAIL DES MESSAGES\n")
            f.write("-"*60 + "\n\n")
            
            for name in NAMES_TO_TRACK:
                if name in self.results and self.results[name]["messages"]:
                    f.write(f"\n📌 {name} - Total: {self.results[name]['total']}\n")
                    f.write("-"*60 + "\n")
                    
                    for msg in self.results[name]["messages"]:
                        f.write(f"Message ID: {msg['id']}\n")
                        f.write(f"Date: {msg['date']}\n")
                        f.write(f"Scores: {msg['scores']}\n")
                        f.write(f"Texte:\n{msg['text']}\n")
                        f.write("-"*60 + "\n")
        
        print(f"✓ Résultats sauvegardés dans: {filename}")
    
    def check_required_names(self, message_text):
        """Vérifie que tous les noms requis sont présents"""
        for name in REQUIRED_NAMES:
            if name not in message_text:
                return False
        return True

async def main():
    try:
        validate_config()
        print(f"\n📊 Configuration chargée:")
        print(f"   Canal: @{CHANNEL_USERNAME}")
        print(f"   Limite: {MESSAGE_LIMIT} messages")
        print(f"   Noms à tracker: {', '.join(NAMES_TO_TRACK)}")
        print(f"   Noms requis: {', '.join(REQUIRED_NAMES)}\n")
        
        scraper = MessageScraper()
        await scraper.scrape_channel()
    except ValueError as e:
        print(f"\n{e}")
        print("\n⚠️ Veuillez configurer votre fichier .env correctement")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())