import logging
import click
from pathlib import Path
import yaml
from jinjafy import jinjafy, IncludeLoader
from jinjafy import Jinjafier, Pandoc

epilog = """
\b
Example: 

$ jinjafy revealjs_2d examples/sample_presentation.yaml -o slides.html -t revealjs --theme night
"""

# jinjafy cv.md merck_cv.yaml --to=md --verbose --bibliography=../../Documents/My\ Library.yaml --to=docx --output="merck_cv.docx"


@click.command(epilog=epilog)
@click.argument("template",     type=click.STRING)
@click.argument("meta",         type=click.File("r"))
@click.option("--verbose", "-v", help="Set logging to DEBUG", default=False, is_flag=True)
@click.option("--to", "-t",     help="Use Pandoc to convert to format (ie, html)")
@click.option("--theme",        help="Theme name", default="simple")
@click.option("--bibliography", help="Bibliography csl file", type=click.File("r"))
@click.option("--extra-args",   help="Use Pandoc to convert with extra args")
@click.option("--output", "-o", type=click.STRING, default=None)
def jinjafy_cli(template, meta, verbose, to, theme, bibliography, extra_args, output):
    """Process TEMPLATE with Jinja2 using data from META and save to optional OUTPUT.
    Optionally convert to output format using Pandoc with TO parameter."""

    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    J = Jinjafier(template)
    _output = J.render(meta, bibliography)
    # click.echo(_output)

    # _output = jinjafy(template, meta, to,
    #                   theme=theme, bibliography=bibliography,
    #                   extra_args=extra_args, outfile=output)

    bib_name = None
    if bibliography:
        bib_name = bibliography.name

    if to:
        _input = {"body": {"content": _output, "format": "md"}}

        P = Pandoc()
        _output = P.convert(_input, target_format=to,
                            bibliography=bib_name,
                            theme=theme,
                            extra_args=extra_args,
                            outfile=output)

    if not output:
        click.echo(_output)


def main():
    jinjafy_cli(auto_envvar_prefix='JINJAFY')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
