from setuptools import setup, find_packages

setup(
    name='jinjafy',
    version='0.3.0',
    packages=find_packages(),
    package_data={'jinjafy': ['extras/*.txt', 'templates/*']},
    install_requires=[
        'Click',
        'pypandoc',
        'pyyaml',
        'jinja2',
        'ruamel.yaml',
        'connexion',
        'attr'
    ],
    entry_points='''
        [console_scripts]
        jinjafy=jinjafy.cli:main
        jinjafy-rest=jinjafy.server:app.run
    ''',
)