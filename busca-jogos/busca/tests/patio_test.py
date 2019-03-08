"""Unit tests para o modulo simulador de patio.

"""
import unittest

from busca.classes.patio import Container, Patio, Pilha


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
        # print(position)
        assert position is False

    def test_time_mean(self):
        p = Pilha('TESTE')
        p.stack(self.c1)
        p.stack(self.c2)
        assert p.time_mean() == (self.c1.time_to_leave + self.c2.time_to_leave) / 2

    def test_remove(self):
        p = Pilha('TESTE')
        position1 = p.stack(self.c1)
        position2 = p.stack(self.c2)
        coluna, altura = p.position_totuple(position1)
        locked = p.up_locked(coluna, altura)
        assert locked is True
        success = p.remove(position1, self.c1)
        assert success is False
        assert p.is_position_free(position1) == (False, False)
        success = p.remove(position1, self.c2)
        assert success is False
        assert p.is_position_free(position1) == (False, False)
        success = p.remove(position2, self.c2)
        assert success is True
        assert p.is_position_free(position2) == ('A', '2')
        coluna, altura = p.position_totuple(position1)
        locked = p.up_locked(coluna, altura)
        assert locked is False

    def test_has_space(self):
        p = Pilha('TESTE')
        assert p.has_space() is True
        position1 = p.stack(self.c1)
        assert p.has_space() is True
        for r in range(29):
            p.stack(Container(str(r)))
        assert p.has_space() is False
        assert p.stack(self.c2) is False


class TestPatio(unittest.TestCase):
    def setUp(self):
        self.c1 = Container('001', 1)
        self.c2 = Container('002', 3)
        self.patio = Patio('TESTE')

    def test_Patio(self):
        assert self.patio._nome == 'TESTE'
        assert isinstance(self.patio._pilhas, dict)
        assert isinstance(self.patio._containers, dict)
        assert isinstance(self.patio._history, dict)

    def test_add_pilha(self):
        self.patio.add_pilha('P01')
        assert isinstance(self.patio._pilhas['P01'], Pilha)
        assert self.patio._pilhas['P01']._nome == 'P01'

    def test_stack(self):
        self.test_add_pilha()
        posicao = self.patio.stack(self.c1, 'P01')
        pilha = self.patio._pilhas['P01']
        coluna, altura = pilha.position_totuple(posicao)
        assert isinstance(pilha._pilha[coluna][altura], Container)
        assert pilha._pilha[coluna][altura]._numero == '001'
        # Pilha inexistente
        posicao = self.patio.stack(self.c1, 'P02')
        assert posicao is False
        # Posicao ocupada
        posicao = self.patio.stack(self.c1, 'P01', 'A1')
        assert posicao is False


if __name__ == '__main__':
    import timeit
    all_times = []
    for classe in [TestContainer, TestPatio, TestPilha]:
        functions = [func for func in dir(classe) if 'test_' in func]
        for function in functions:
            # print(f'classe:{classe.__name__} function:{function}')
            setup_code = f'''
test = {classe.__name__}()
test.setUp()
            '''
            test_code = f'test.{function}()'
            times = timeit.repeat(setup=setup_code,
                                  stmt=test_code,
                                  repeat=3,
                                  number=1000,
                                  globals=globals())
            all_times.append((
                min(times),
                f'Time {classe.__name__} {function} {min(times)}'
            ))
    for time, descricao in sorted(
            all_times, key=lambda x: x[0]):
        print(descricao)
