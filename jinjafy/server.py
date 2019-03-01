import connexion
from jinjafy import jinjafy

"""
/render/revealjs_2d?source=<source>&theme=moon

"""


def hello():
    print("Hello there")


def render(template, source, theme="simple"):

    with open(source) as meta:
        output = jinjafy(template, meta, to="revealjs", theme=theme)
        return output


def init_app():

    app = connexion.App(__name__, specification_dir='.')
    app.add_api('jinjafy-oapi3.yaml')
    return app


app = init_app()

if __name__ == "__main__":
    app.run(port=8080)
