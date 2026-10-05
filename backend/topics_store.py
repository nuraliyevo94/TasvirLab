import json
from pathlib import Path
from typing import List, Dict, Any
from backend.config import Config, SAMPLE_TOPICS

TOPICS_FILE = Config.STATIC_DIR / "custom_topics.json"

class TopicsStore:
    """Tavsiya etilgan namunaviy mavzularni dinamik boshqarish va saqlash ombori."""

    @staticmethod
    def get_all_topics() -> List[Dict[str, Any]]:
        if TOPICS_FILE.exists():
            try:
                with open(TOPICS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        return data
            except Exception as e:
                print(f"[TopicsStore] O'qishda xatolik: {e}")
        return list(SAMPLE_TOPICS)

    @staticmethod
    def save_topics(topics: List[Dict[str, Any]]) -> bool:
        try:
            TOPICS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(TOPICS_FILE, "w", encoding="utf-8") as f:
                json.dump(topics, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[TopicsStore] Saqlashda xatolik: {e}")
            return False

    @staticmethod
    def add_topic(topic_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        topics = TopicsStore.get_all_topics()
        if not topic_data.get("id"):
            import uuid
            topic_data["id"] = f"topic_{uuid.uuid4().hex[:8]}"
        topics.insert(0, topic_data)
        TopicsStore.save_topics(topics)
        return topics

    @staticmethod
    def delete_topic(topic_id_or_title: str) -> List[Dict[str, Any]]:
        topics = TopicsStore.get_all_topics()
        topics = [
            t for t in topics
            if str(t.get("id")) != str(topic_id_or_title) and t.get("title") != topic_id_or_title
        ]
        TopicsStore.save_topics(topics)
        return topics
