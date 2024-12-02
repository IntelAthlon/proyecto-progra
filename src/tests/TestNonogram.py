import unittest

import pygame

from src.Nonogram import Nonogram

class TestNonogram(unittest.TestCase):

    def test_crear_tablero(self):
        pygame.font.init()
        nonograma = Nonogram([[1, 1, 1, 1, 1],[1, 0, 0, 0, 1],[1, 0, 1, 0, 1],[1, 0, 0, 0, 1],[1, 1, 1, 1, 1]],[[5], [1, 1], [1, 1, 1], [1, 1], [5]],
    [[5], [1, 1], [1, 1, 1], [1, 1], [5]])  # Crear un nonograma de 5x5
        self.assertEqual(len(nonograma.player_grid), 5)
        self.assertEqual(len(nonograma.player_grid[0]), 5)

    def test_validar_solucionado(self):
        pygame.font.init()
        nonograma = Nonogram([[1, 1, 1, 1, 1],[1, 0, 0, 0, 1],[1, 0, 1, 0, 1],[1, 0, 0, 0, 1],[1, 1, 1, 1, 1]],[[5], [1, 1], [1, 1, 1], [1, 1], [5]],
    [[5], [1, 1], [1, 1, 1], [1, 1], [5]])
        for i in range(5):
            nonograma.set_cell(0, i, 1)
            nonograma.set_cell(4, i, 1)
        for i in range(3):
            nonograma.set_cell(i+1, 0, 1)
            nonograma.set_cell(i+1, 4, 1)
        nonograma.set_cell(2, 2, 1)
        self.assertTrue(nonograma.is_solved())


if __name__ == '__main__':
    unittest.main()