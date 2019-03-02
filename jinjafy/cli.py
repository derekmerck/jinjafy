import logging
import click
import yaml
from jinjafy import jinjafy

epilog = """
\b
Example: 

$ jinjafy revealjs_2d example/sample_presentation.yaml -o slides.html -t revealjs --theme night
"""


@click.command(epilog=epilog)
@click.argument("template",     type=click.STRING)
@click.argument("meta",         type=click.File("r"))
@click.option("--to", "-t",     help="Use Pandoc to convert to format (ie, html)")
@click.option("--theme",        help="Theme name", default="simple")
@click.option("--extra-args",   help="Use Pandoc to convert with extra args")
@click.option("--output", "-o", type=click.File("w"))
def jinjafy_cli(template, meta, to, theme, extra_args, output):
    """Process TEMPLATE with Jinja2 using data from META and save to optional OUTPUT.
    Optionally convert to output format using Pandoc with TO parameter."""

    meta = yaml.safe_load(meta)
    _output = jinjafy(template, meta, to, theme=theme, extra_args=extra_args)

    if output:
        output.write(_output)
    else:
        click.echo(_output)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    jinjafy_cli()
