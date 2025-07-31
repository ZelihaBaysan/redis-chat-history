import redis
import os
from dotenv import load_dotenv

# Ortam değişkenlerini yükle (gerekirse)
load_dotenv()

# Redis'e bağlan
redis_client = redis.Redis.from_url("redis://localhost:6379")

# İstediğin oturum key'ini belirt (örneğin: session_1234)
chat_store_key = input("Hangi oturum key'ini çekmek istiyorsun? (örnek: session_1): ")

# Redis'ten ilgili listeyi çek
chat_list = redis_client.lrange(chat_store_key, 0, -1)

if not chat_list:
    print(f"Hiç kayıt bulunamadı: {chat_store_key}")
else:
    with open("redis_chat_history.txt", "w", encoding="utf-8") as f:
        f.write(f"SOHBET GEÇMİŞİ ({chat_store_key})\n")
        f.write("-" * 50 + "\n")
        for msg in chat_list:
            decoded = msg.decode("utf-8")
            f.write(decoded + "\n")
    print("Sohbet geçmişi 'redis_chat_history.txt' dosyasına yazıldı.")
