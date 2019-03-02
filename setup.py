from setuptools import setup, find_packages

setup(
    name='jinjafy',
    version='0.2.1',
    packages=find_packages(),
    package_data={'jinjafy': ['extras/*.txt', 'templates/*']},
    install_requires=[
        'Click',
        'pypandoc',
        'pyyaml',
        'jinja2'
    ],
    entry_points='''
        [console_scripts]
        jinjafy=jinjafy.cli:jinjafy_cli
        jinjafy-rest=jinjafy.server:app.run
    ''',
)