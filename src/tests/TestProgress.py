import unittest

from src.logic.ProgressTracker import ProgressTracker
import os


class TestProgress(unittest.TestCase):
    """
    Clase de prueba unitaria para la clase ProgressTracker.

    Métodos:
        test_un_nivel_completo(): Prueba si un nivel se marca como completo correctamente.
        test_validar_cantidad_niveles_comp(): Prueba si se valida correctamente la cantidad de niveles completados.
    """
    def test_un_nivel_completo(self):
        """
        Prueba si un nivel se marca como completo correctamente.
        """
        os.makedirs(os.path.dirname("data/tests/progressTest1.json"), exist_ok=True)
        progress = ProgressTracker("data/tests/progressTest1.json")
        progress.mark_level_complete("easy", "level1")
        self.assertTrue(progress.is_level_complete("easy", "level1"))

    def test_validar_cantidad_niveles_comp(self):
        """
        Prueba si se valida correctamente la cantidad de niveles completados.
        """
        os.makedirs(os.path.dirname("data/tests/progressTest2.json"), exist_ok=True)
        progress = ProgressTracker("data/tests/progressTest2.json")
        progress.mark_level_complete("easy", "level1")
        progress.mark_level_complete("easy", "level2")
        self.assertEqual(progress.get_category_progress("easy"), 2)


if __name__ == '__main__':
    unittest.main()
