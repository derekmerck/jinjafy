from setuptools import setup, find_packages

setup(
    name='jinjafy',
    version='0.2',
    packages=find_packages(),
    package_data={'jinjafy': ['extras/*.txt']},
    install_requires=[
        'Click',
        'pypandoc',
        'pyyaml',
        'jinja2'
    ],
    entry_points='''
        [console_scripts]
        jinjafy=jinjjafy.cli:jinjafy_cli
    ''',
)