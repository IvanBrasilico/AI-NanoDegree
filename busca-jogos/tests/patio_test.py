"""Unit tests para o modulo simulador de patio.

"""
import unittest

from classes.patio import Container, Pilha


class TestContainer(unittest.TestCase):

    def test_container(self):
        c = Container('001', 2)
        assert c.time_to_leave == 2
        assert c._numero == '001'
        assert isinstance(c, Container)
        assert str(c) == '001'


class TestPilha(unittest.TestCase):
    def setUp(self):
        self.c1 = Container('001', 1)
        self.c2 = Container('002', 3)

    def tearDown(self):
        pass

    def test_pilha(self):
        p = Pilha('TESTE')
        assert p._nome == 'TESTE'
        assert p._pilha is not None
        assert isinstance(p._pilha, dict)

    def test_position_totuple(self):
        p = Pilha('TESTE')
        coluna, altura = p.position_totuple('A1')
        assert (coluna, altura) == ('A', '1')

    def test_getcontainerinposition(self):
        p = Pilha('TESTE')
        position = p.stack(self.c1)
        c = p.get_containerinposition(position)
        assert c == self.c1

    def test_side_locked(self):
        p = Pilha('TESTE')
        position1 = p.stack(self.c1, 'A1')
        position2 = p.stack(self.c2, 'B1')
        coluna, altura = p.position_totuple(position1)
        locked = p.side_locked(coluna, altura)
        assert locked is True
        coluna, altura = p.position_totuple(position2)
        locked = p.side_locked(coluna, altura)
        assert locked is False

    def test_up_locked(self):
        p = Pilha('TESTE')
        position1 = p.stack(self.c1)
        position2 = p.stack(self.c2)
        coluna, altura = p.position_totuple(position1)
        locked = p.up_locked(coluna, altura)
        assert locked is True
        coluna, altura = p.position_totuple(position2)
        locked = p.up_locked(coluna, altura)
        assert locked is False

    def test_posicao_inexistente(self):
        p = Pilha('TESTE')
        with self.assertRaises(KeyError):
            position = p.stack(self.c1, 'A9')


    def test_posicao_invalida(self):
        p = Pilha('TESTE')
        position = p.stack(self.c1, 'A2')
        print(position)
        assert position is False
