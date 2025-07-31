import os
import uuid
from dotenv import load_dotenv
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.storage.chat_store.redis import RedisChatStore
from llama_index.llms.ollama import Ollama
import redis

# 1. Ortam değişkenlerini yükle
load_dotenv()

# 2. Redis bağlantısı
redis_client = redis.Redis.from_url("redis://localhost:6379")
redis_chat_store = RedisChatStore(redis_client=redis_client)

# 3. Yerel LLM (Ollama modeli)
llm = Ollama(model="gemma3n")  # Model adını kendi sistemine göre ayarla

# 4. Dinamik oturum key'i oluştur
chat_store_key = f"session_{uuid.uuid4()}"

# 5. Chat memory (Redis'e bağlı)
memory = ChatMemoryBuffer.from_defaults(
    chat_store=redis_chat_store,
    chat_store_key=chat_store_key,
    token_limit=3000
)

# 6. Chat engine (Belgesiz, sadece model ve hafıza ile)
chat_engine = SimpleChatEngine.from_defaults(
    llm=llm,
    memory=memory,
    system_prompt="Sen zeki bir asistan olarak kendi bilgine dayanarak cevap veriyorsun. Sohbet Redis'e kaydediliyor."
)

# 7. Sohbet döngüsü
print(f"Sohbet motoru hazır! (Oturum anahtarı: {chat_store_key})")
print("Çıkmak için Ctrl+C\n")

while True:
    try:
        user_input = input("Kullanıcı: ")
        response = chat_engine.chat(user_input)
        print(f"Asistan: {response}")
    except KeyboardInterrupt:
        print("\nSohbet sonlandırıldı.")
        break
