import unittest
from src.nonogram import Nonogram

class TestNonogram(unittest.TestCase):

    def test_crear_tablero(self):
        nonograma = Nonogram(5, 5)  # Crear un nonograma de 5x5
        self.assertEqual(nonograma.filas, 5)
        self.assertEqual(nonograma.columnas, 5)

    def test_validar_jugada_valida(self):
        nonograma = Nonogram(5, 5)

        self.assertTrue(nonograma.validar_jugada(2, 3, "negro"))

    def test_validar_jugada_invalida(self):
        nonograma = Nonogram(5, 5)

        self.assertFalse(nonograma.validar_jugada(1, 1, "negro"))

if __name__ == '__main__':
    unittest.main()