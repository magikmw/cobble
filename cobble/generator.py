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

    # parse the markup into html
    for a in articles:
        # print(a)
        articles[a] = mistune.markdown(articles[a])

    # render data into a template
    template_env = Environment(loader=FileSystemLoader('templates'))
    temp_article = template_env.get_template('article.html')

    # save the output files
    for a in articles:
        outpath = project_path+'/static/articles/'+ \
            os.path.basename((os.path.splitext(a)[0]+'.html'))
        open(outpath, 'w+').write(temp_article.render(contents=articles[a]))

    # [TODO] Special case for the index.html?
