from setuptools import setup

setup(
    name='jinjafy',
    version='0.1',
    py_modules=['jinjafier'],
    install_requires=[
        'Click',
        'pypandoc',
        'pyyaml',
        'jinja2'
    ],
    entry_points='''
        [console_scripts]
        jinjafy=jinjafier:jinjafy
    ''',
)