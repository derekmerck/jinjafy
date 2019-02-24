import logging
from pprint import pformat
import jinja2
import pypandoc
import click
import yaml

epilog = """
\b
Example: 

$ jinjafy example/revealjs_template.md example/sample_data.yaml -o slides.html -f md -t revealjs
"""


@click.command(epilog=epilog)
@click.argument("template",     type=click.File("r"))
@click.argument("meta",         type=click.File("r"))
@click.option("--output", "-o", type=click.File("w"))
@click.option("--format", "-f", "_format", help="Use Pandoc to convert from format (ie, md)")
@click.option("--to", "-t",     help="Use Pandoc to convert to format (ie, html)")
@click.option("--extra-args",   help="Use Pandoc to convert with extra args (ie, --ATX_FORMAT)")
def jinjafy(template, meta, output, _format, to, extra_args):
    """Process TEMPLATE with Jinja2 using data from META and save to optional OUTPUT.
    Optionally convert to output format using Pandoc with FROM/TO parameters."""

    _meta = yaml.safe_load(meta)
    logging.debug(pformat(_meta))

    env = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
    _template = env.from_string(template.read())

    # logging.debug(_template)
    _output = _template.render(_meta)

    if _format:
        if to == "revealjs":
            extra_args = ["-s",
                          "-V", "revealjs-url=https://revealjs.com",
                          "-V", "theme=white",
                          "--slide-level=3"]
        _output = pypandoc.convert_text(_output, to, format=_format, extra_args=extra_args)

    if output:
        output.write(_output)
    else:
        click.echo(_output)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    jinjafy()
