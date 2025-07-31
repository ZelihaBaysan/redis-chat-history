import redis

# Redis'e bağlan
redis_client = redis.Redis.from_url("redis://localhost:6379")

# session_ ile başlayan key'leri ara
keys = redis_client.keys("session_*")

# Byte olarak gelir, string'e çevir
session_keys = [key.decode("utf-8") for key in keys]

# Raporla
if not session_keys:
    print("Hiç session bulunamadı.")
else:
    print(f"{len(session_keys)} adet session bulundu:\n")
    for key in session_keys:
        print(f"- {key}")
