"""Example Static HTML file output."""

from pathlib import Path

import plotly.express as px
from bs4 import BeautifulSoup
from dash_charts.utils_app import STATIC_URLS
from dash_charts.utils_static import WritePlotlyHTML, write_div

if __name__ == '__main__':
    soup = BeautifulSoup('', features='lxml')
    tag = soup.new_tag('h1')
    tag.attrs['class'] = 'header-h1'
    tag.string = 'Test Header'
    soup.append(tag)

    figure_1 = px.scatter(x=range(10), y=range(10))
    figure_2 = px.scatter(x=[*range(10)][::-1], y=range(10))

    # Write actual HTML content of interest
    filename = Path(__file__).parent / 'tmp.html'
    stylesheets = [STATIC_URLS['dash']]
    with WritePlotlyHTML(filename, stylesheets) as output:
        output.write(soup.prettify())
        write_div(figure_1, output)
        write_div(figure_2, output)
