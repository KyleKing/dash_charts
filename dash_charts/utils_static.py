"""Generate static HTML reports."""

import io
import re
from pathlib import Path

import plotly.io
from bs4 import BeautifulSoup

# TODO: Add BootStrap CDN and methods for creating rows/columns


def write_div(figure, path_or_file_object, is_div=True, **html_kwargs):
    """Write Plotly figure as HTML to specified file.

    Args:
        figure: Plotly figure (can be from `create_figure` for custom charts)
        path_or_file_object: *string* path or file object
        is_div: if True (default) will override html_kwargs to only write the minimum HTML needed
        html_kwargs: additional keyword arguments pass to output

    """
    for key in ['include_plotlyjs', 'full_html']:
        if key not in html_kwargs and is_div:
            html_kwargs[key] = False

    plotly.io.write_html(fig=figure, file=path_or_file_object, **html_kwargs)


def write_image(figure, path_or_file_object, image_format, **img_kwargs):
    """Write Plotly figure as an image to specified file.

    Args:
        figure: Plotly figure (can be from `create_figure` for custom charts)
        path_or_file_object: *string* path or file object
        image_format: one of `(png, jpg, jpeg, webp, svg, pdf)`
        img_kwargs: additional keyword arguments pass to output

    """
    plotly.io.write_image(fig=figure, file=path_or_file_object, format=image_format, **img_kwargs)


def format_boilerplate(external_stylesheets=None):
    """Return the boilerplate HTML for creating a static HTML file with Plotly figures and other HTML elements.

    Args:
        external_stylesheets: list of external stylesheets

    Returns:
        tuple: of the top and the bottom HTML content

    """
    if external_stylesheets is None:
        external_stylesheets = []
    # Capture necessary Plotly boilerplate HTML
    with io.StringIO() as output:
        write_div({}, output, is_div=False, include_mathjax='.js', validate=False)
        blank_plotly = BeautifulSoup(output.getvalue(), features='lxml')
    # Add the stylesheets to header

    # Remove the empty figure div and corresponding script
    plot_div = blank_plotly.find('div', attrs={'class': 'plotly-graph-div'})
    for script in blank_plotly.find_all('script')[::-1]:
        # Use the ID from the plot to identify which script needs to be removed
        if plot_div.attrs['id'] in script.prettify():
            script.decompose()
            break
    plot_div.decompose()
    # Remove the trailing elements
    bot_html_str = '\n</body>\n</html>'
    bot_html_re = r'<\/body>\s*<\/html>\s*$'
    return (re.sub(bot_html_re, '', blank_plotly.prettify(), count=1), bot_html_str)


class WritePlotlyHTML(io.StringIO):
    """Context manager for creating a static HTML file with Plotly figures and other HTML elements."""

    def __init__(self, filename, stylesheets=None):
        """Return the boilerplate HTML for creating a static HTML file with Plotly figures and other HTML elements.

        Args:
            filename: string or Path to the destination file
            stylesheets: list of external stylesheets

        """
        super().__init__()
        self.filename = Path(filename)
        self.stylesheets = stylesheets

    def __enter__(self):
        """Initialize the StringIO output with the initial HTML.

        Returns:
            dict: connection to sqlite database

        """
        self.output = super().__enter__()
        top_html, bot_html = format_boilerplate(external_stylesheets=self.stylesheets)
        self.bot_html = bot_html
        self.output.write(top_html)
        return self.output

    def __exit__(self, *args):
        """Close the HTML tags and write to the text file.

        Args:
            args: arguments passed to base class

        """
        self.output.write(self.bot_html)
        html_content = BeautifulSoup(self.output.getvalue(), features='lxml').prettify()
        self.filename.write_text(html_content)
        super().__exit__(*args)
