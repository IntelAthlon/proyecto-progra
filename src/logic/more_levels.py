import json
import os


def load_levels_and_categories():
    categories = {}
    levels_dir = "data/levels"

    # Crear el directorio si no existe
    os.makedirs(levels_dir, exist_ok=True)

    # Si el directorio está vacío, generar niveles por defecto
    if not os.listdir(levels_dir):
        generate_default_levels(levels_dir)

    for category in os.listdir(levels_dir):
        category_path = os.path.join(levels_dir, category)
        if os.path.isdir(category_path):
            categories[category] = []
            for level_file in os.listdir(category_path):
                if level_file.endswith('.json'):
                    with open(os.path.join(category_path, level_file), 'r') as f:
                        level_data = json.load(f)
                        categories[category].append({
                            'name': os.path.splitext(level_file)[0],
                            'grid': level_data['grid'],
                            'row_clues': level_data['row_clues'],
                            'col_clues': level_data['col_clues']
                        })
    return categories


def generate_default_levels(levels_dir):
    from src.logic.generator import generate_nonogram

    difficulties = ['easy', 'medium', 'hard']
    for difficulty in difficulties:
        difficulty_dir = os.path.join(levels_dir, difficulty)
        os.makedirs(difficulty_dir, exist_ok=True)

        for i in range(5):  # Generar 5 niveles por dificultad
            size = 5 if difficulty == 'easy' else 10 if difficulty == 'medium' else 15
            new_level = generate_nonogram(size, size, difficulty)

            level_file = os.path.join(difficulty_dir, f"level_{i + 1}.json")
            with open(level_file, 'w') as f:
                json.dump(new_level, f)