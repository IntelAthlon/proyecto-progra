import json
import os


class PlayerProgress:
    def __init__(self, file_path='data/player_progress.json'):
        self.file_path = file_path
        self.progress = self.load_progress()

    def load_progress(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        else:
            return self.create_default_progress()

    def create_default_progress(self):
        return {
            "easy": {f"level{i}": False for i in range(1, 6)},
            "medium": {f"level{i}": False for i in range(1, 6)},
            "hard": {f"level{i}": False for i in range(1, 6)}
        }

    def save_progress(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.progress, f, indent=2)

    def update_level_progress(self, difficulty, level, completed):
        if difficulty in self.progress and level in self.progress[difficulty]:
            self.progress[difficulty][level] = completed
            self.save_progress()
        else:
            raise ValueError(f"Invalid difficulty '{difficulty}' or level '{level}'")

    def is_level_completed(self, difficulty, level):
        if difficulty in self.progress and level in self.progress[difficulty]:
            return self.progress[difficulty][level]
        else:
            raise ValueError(f"Invalid difficulty '{difficulty}' or level '{level}'")

    def get_completed_levels(self, difficulty):
        if difficulty in self.progress:
            return [level for level, completed in self.progress[difficulty].items() if completed]
        else:
            raise ValueError(f"Invalid difficulty '{difficulty}'")

    def reset_progress(self):
        self.progress = self.create_default_progress()
        self.save_progress()


# Example usage
if __name__ == "__main__":
    progress = PlayerProgress()

    # Update a level's progress
    progress.update_level_progress("easy", "level1", True)

    # Check if a level is completed
    print(progress.is_level_completed("easy", "level1"))  # Should print True

    # Get all completed levels for a difficulty
    print(progress.get_completed_levels("easy"))  # Should print ["level1"]

    # Reset all progress
    progress.reset_progress()