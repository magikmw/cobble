# -*- coding: UTF-8 -*-

"""Build static pages and return in some form to the builder to save \
as file"""

"""This file is part of Cobble.

Cobble is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Cobble is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Cobble; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import os

import mistune
from jinja2 import Environment, FileSystemLoader

from util import get_html_path

_SUB_TEMPLATES = ["_head.html", "_header.html", '_menu.html', '_footer.html']
_TEMPLATES = ["article.html"]

def generate_articles(files, project_path):
    """Given a list of files, template and destination, output static articles

    files: list of files (absolute paths)
    project_path: path under which all folders are
    """

    # for each file, extract the data
    # [TODO] Figure out the metadata thing
    articles = {}
    for f in files:
        articles[f] = open(f).read()

    # parse the markup into html, change the keys to .html too
    html_articles = {}
    for a in articles:
        html_path = get_html_path(a, 'articles', project_path)
        html_articles[html_path] = mistune.markdown(articles[a])

    # render data into a template
    template_env = Environment(loader=FileSystemLoader('templates'))
    sub_templates = {}
    for tmp in _SUB_TEMPLATES:
        sub_templates[tmp] = template_env.get_template(tmp)
    temp_article = template_env.get_template('article.html')

    # render subtemplates
    filenames = []
    for a in html_articles:
        filenames.append(os.path.basename(a))
    if 'index.html' in filenames: filenames.remove('index.html')
    menu = sub_templates['_menu.html'].render(articles=filenames)

    # save the output files
    for a in html_articles:
        open(a, 'w+').write(temp_article.render(
            contents=html_articles[a],
            head=sub_templates['_head.html'].render(),
            header=sub_templates['_header.html'].render(),
            menu=menu,
            footer=sub_templates['_footer.html'].render()
            ))

    # [TODO] Special case for the index.html?
