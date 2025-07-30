import json
import redis
from dotenv import load_dotenv
import os
import time
from typing import List, Dict

class RedisChatReader:
    def __init__(self):
        load_dotenv()
        
        self.redis = redis.Redis(
            host=os.getenv("UPSTASH_REDIS_HOST"),
            port=int(os.getenv("UPSTASH_REDIS_PORT", 6379)),
            password=os.getenv("UPSTASH_REDIS_PASSWORD"),
            ssl=True,
            decode_responses=True
        )
        self.chat_key_pattern = "chat:*"

    def find_conversations(self) -> List[str]:
        """Redis'teki tüm konuşma anahtarlarını bulur"""
        return sorted(self.redis.keys(self.chat_key_pattern), key=lambda x: self.redis.llen(x), reverse=True)

    def get_conversation_messages(self, conversation_key: str) -> List[Dict]:
        """Bir konuşmadaki tüm mesajları getirir"""
        messages = self.redis.lrange(conversation_key, 0, -1)
        return [json.loads(msg) for msg in messages]

    def print_all_chats(self, max_messages=10):
        """Tüm konuşmaları ve mesajları gösterir (sınırlı sayıda)"""
        print("\n" + "="*60)
        print("📖 REDİS SOHBET GEÇMİŞİ (En aktif konuşmalar üstte)")
        print("="*60)
        
        conversations = self.find_conversations()
        
        if not conversations:
            print("\n❌ Hiç sohbet bulunamadı!")
            return

        for conv_key in conversations:
            conv_name = conv_key[5:]  # 'chat:' önekini kaldırır
            messages = self.get_conversation_messages(conv_key)
            msg_count = len(messages)
            
            print(f"\n💬 Konuşma: {conv_name} (Toplam {msg_count} mesaj)")
            print("-"*50)
            
            for i, msg in enumerate(messages[:max_messages]):
                print(f"\n[{i+1}] {time.strftime('%d.%m.%Y %H:%M', time.localtime(msg['timestamp']))}")
                print(f"   👤 {msg['user']}")
                print(f"   🤖 {msg['bot']}")
                if msg.get("metadata"):
                    print(f"   ℹ️ {msg['metadata']}")
                
            if msg_count > max_messages:
                print(f"\n... ve {msg_count-max_messages} mesaj daha")

        print("\n" + "="*60)
        print(f"Toplam {len(conversations)} konuşma bulundu")
        print("="*60)

if __name__ == "__main__":
    print("🔄 Redis Sohbet Okuyucu Başlatılıyor...\n")
    reader = RedisChatReader()
    
    try:
        while True:
            reader.print_all_chats()
            print("\n🔄 15 saniye sonra yenilenecek... (Çıkmak için Ctrl+C)")
            time.sleep(15)
    except KeyboardInterrupt:
        print("\n❌ Program sonlandırıldı")