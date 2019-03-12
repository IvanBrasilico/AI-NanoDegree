import unittest

from pyannotate_runtime import collect_types

module = 'busca.tests.patio_test'

if __name__ == '__main__':
    collect_types.init_types_collection()
    with collect_types.collect():
        unittest.main(module)
    collect_types.dump_stats('type_info.json')

""""
After run:

pyannotate -w busca/classes/patio.py
mypy busca/classes/patio.py

"""
