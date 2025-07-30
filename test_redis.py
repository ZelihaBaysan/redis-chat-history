import json
import redis
from dotenv import load_dotenv
import os
import time

load_dotenv()

# Redis bağlantısı
r = redis.Redis(
    host=os.getenv("UPSTASH_REDIS_HOST"),
    port=int(os.getenv("UPSTASH_REDIS_PORT", 6379)),
    password=os.getenv("UPSTASH_REDIS_PASSWORD"),
    ssl=True,
    decode_responses=True
)

# Test verileri
conversation_id = "twd_daryl_dixon"
messages = [
    {"user": "Daryl kimdir?", "bot": "Daryl Dixon, The Walking Dead dizisinde Norman Reedus tarafından canlandırılan bir karakterdir. Usta bir okçu ve avcıdır."},
    {"user": "En bilindik özelliği nedir?", "bot": "Motosikleti ve çaprazbow'uyla tanınır. Ayrıca sadık, içe dönük ama son derece becerikli bir hayatta kalanıdır."},
    {"user": "Kardeşi hakkında ne söylersin?", "bot": "Merle Dixon, Daryl'in abisidir. Başlarda sorunlu bir karakter olsa da Daryl ile karmaşık bir ilişkileri vardır."},
    {"user": "Daryl'in en unutulmaz sahneleri?", "bot": "1) Çaprazbow'la walker avladığı sahneler\n2) Beth'le birlikte geçirdiği bölümler\n3) Whisperers'a karşı verdiği mücadele"},
    {"user": "Daryl herhangi bir romantik ilişki yaşadı mı?", "bot": "Daryl dizide çoğunlukla romantik ilişkilerden uzak durmuştur. Ancak Carol ve Leah ile derin bağları olmuştur."},
    {"user": "En sevdiği sözü nedir?", "bot": "\"You're gonna be fine.\" (İyi olacaksın) - Sıklıkla grup üyelerini sakinleştirmek için kullanır."},
    {"user": "Daryl'in geçmişi hakkında ne biliyoruz?", "bot": "Zor bir çocukluk geçirmiştir. Alkolik bir baba ve kayıp bir annesi vardı. Merle ile birlikte büyüdüler."}
]

# Mesajları Redis'e ekleme
for msg in messages:
    message_data = {
        "timestamp": int(time.time()),
        "user": msg["user"],
        "bot": msg["bot"],
        "metadata": {"source": "TWD Fan Sohbeti"}
    }
    r.rpush(f"chat:{conversation_id}", json.dumps(message_data))
    time.sleep(1)  # Timestamp'lerin farklı olması için

print(f"✅ {len(messages)} mesaj '{conversation_id}' konuşmasına eklendi!")