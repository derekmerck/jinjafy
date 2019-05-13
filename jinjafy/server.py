from pathlib import Path
import os
import logging
import connexion
import requests
import yaml
from jinjafy import jinjafy

"""
Example:

/render/revealjs_2d?source=<source>&theme=moon

"https://raw.githubusercontent.com/derekmerck/jinjafy/master/examples/sample_presentation.yaml"

"""

def hello():
    print("Hello there")


def render(template, source, theme="simple"):

    meta = {}

    # Maybe an online resource
    if source.startswith("http"):
        response = requests.get(source)
        _source = response.content
        meta = yaml.safe_load(_source)

    # Otherwise it is in a local content store
    else:
        logging.warning(os.path.join(".", source))
        if Path( os.path.join(".", source) ).is_file():
            with open( os.path.join(".", source) ) as f:
                meta = yaml.safe_load(f)
            logging.warning("Failed ot find meta")

    if not meta:
        return "Failed to find meta", 500

    output = jinjafy(template, meta, to="revealjs", theme=theme)
    print(output)
    return output, 200


def init_app():

    app = connexion.App(__name__, specification_dir='.')
    app.add_api('jinjafy-oapi3.yaml')
    return app


app = init_app()

if __name__ == "__main__":
    app.run(port=8080)
