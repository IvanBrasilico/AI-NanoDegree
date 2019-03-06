from setuptools import find_packages, setup

setup(
    name='busca',
    description='Busca Patio',
    version='0.0.1',
    url='https://github.com/IvanBrasilico/busca',
    license='GPL',
    author='Ivan Brasilico',
    author_email='brasilico.ivan@gmail.com',
    packages=find_packages(),
    install_requires=[
        'jupyter',
        'numpy',
        'matplotlib',
        'scikit-learn'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite="tests",
    package_data={
    },
    extras_require={
        'dev': [
            'alembic',
            'autopep8',
            'bandit',
            'coverage',
            'flake8',
            'flake8-quotes',
            'flake8-docstrings',
            'flake8-todo',
            'isort',
            'mypy',
            'pylint',
            'pytest',
            'pytest-cov',
            'pytest-mock',
            'radon',
            'testfixtures',
            'tox'
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.6',
    ],
)
