import json
import os

class PostCache:
    def __init__(self, cache_file='cache.json'):
        self.cache_file = cache_file
        self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                data = json.load(f)
                self.post_ids = set(data.get("post_ids", []))
        else:
            self.post_ids = set()

    def is_cached(self, post_id: str) -> bool:
        return post_id in self.post_ids

    def add(self, post_id: str):
        self.post_ids.add(post_id)

    def save(self):
        with open(self.cache_file, 'w') as f:
            json.dump({"post_ids": list(self.post_ids)}, f, indent=2)
