import unittest

from pyannotate_runtime import collect_types

def run_tests(module='__main__'):
    unittest.main(module)

if __name__ == '__main__':
    collect_types.init_types_collection()
    with collect_types.collect():
        run_tests('busca.tests.patio_test')
    collect_types.dump_stats('type_info.json')

""""
After run:

pyannotate -w busca/classes/patio.py
mypy busca/classes/patio.py

"""