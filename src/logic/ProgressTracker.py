import json
import os

class ProgressTracker:
    def __init__(self, progress_file="data/player_progress.json"):
        self.progress_file = progress_file
        self.progress = self.load_progress()

    def load_progress(self):
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {}

    def save_progress(self):
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f)

    def mark_level_complete(self, category, level_name):
        if category not in self.progress:
            self.progress[category] = {}
        self.progress[category][level_name] = True
        self.save_progress()

    def is_level_complete(self, category, level_name):
        return self.progress.get(category, {}).get(level_name, False)

    def get_category_progress(self, category):
        category_progress = self.progress.get(category, {})
        return len(category_progress)
