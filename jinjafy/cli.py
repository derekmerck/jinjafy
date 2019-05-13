import logging
import click
import yaml
from jinjafy import jinjafy, IncludeLoader

epilog = """
\b
Example: 

$ jinjafy revealjs_2d examples/sample_presentation.yaml -o slides.html -t revealjs --theme night
"""


@click.command(epilog=epilog)
@click.argument("template",     type=click.STRING)
@click.argument("meta",         type=click.File("r"))
@click.option("--to", "-t",     help="Use Pandoc to convert to format (ie, html)")
@click.option("--theme",        help="Theme name", default="simple")
@click.option("--bibliography", help="Bibliography csl file")
@click.option("--extra-args",   help="Use Pandoc to convert with extra args")
@click.option("--output", "-o", type=click.STRING)
def jinjafy_cli(template, meta, to, theme, bibliography, extra_args, output):
    """Process TEMPLATE with Jinja2 using data from META and save to optional OUTPUT.
    Optionally convert to output format using Pandoc with TO parameter."""

    meta = yaml.load(meta, Loader=IncludeLoader)
    _output = jinjafy(template, meta, to,
                      theme=theme, bibliography=bibliography,
                      extra_args=extra_args, outfile=output)

    if not output:
        click.echo(_output)


def main():
    jinjafy_cli(auto_envvar_prefix='JINJAFY')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
