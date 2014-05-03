# -*- coding: UTF-8 -*-

"""Build static pages and return in some form to the builder to save as file
"""

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

from datetime import datetime

import mistune
from jinja2 import Environment, FileSystemLoader

from util import get_output_path, parse_tags_to_dict

_SUB_TEMPLATES = ["_head.html", "_header.html", '_menu.html', '_footer.html']
_TEMPLATES = ["article.html"]

class Article(object):
    """Represents an article.
    Given a raw string, parse the markdown and extract tags.

    string: the raw data from an .md file to be parsed
    """
    def __init__(self, string):
        # [0] is tags, [1:] is the content ('\n\n'.join() it!)
        split_string = string.split('\n\n')

        self.content = mistune.markdown('\n\n'.join(split_string[1:]))

        tag_dict = parse_tags_to_dict(split_string[0].split('\n'))

        if tag_dict:
            # [TODO] Implement else cases where this data is pulled from contents/os
            if 'title' in tag_dict:
                self.title = tag_dict['title']
            if 'date' in tag_dict:
                self.date = datetime.strptime(tag_dict['date'], "%Y-%m-%d %H:%M")
            if 'url' in tag_dict:
                self.url = tag_dict['url']

def generate_articles(files, project_path):
    """Given a list of files, template and destination, output static articles

    files: list of files (absolute paths)
    project_path: path under which all folders are
    """

    articles = []
    for f in files:
        articles.append(Article(open(f).read()))

    # render data into a template
    template_env = Environment(loader=FileSystemLoader('templates'))
    sub_templates = {}
    for tmp in _SUB_TEMPLATES:
        sub_templates[tmp] = template_env.get_template(tmp)
    temp_article = template_env.get_template('article.html')

    # render subtemplates
    filenames = []
    for art in articles:
        filenames.append(art.url)
    # if 'index.html' in filenames: filenames.remove('index.html')
    # [FIX] Find a way to remove the index.html from menu without not generating it.

    # head - read content's first highest title and put it in the template
    # print(filenames)
    temp_menu = sub_templates['_menu.html'].render(articles=filenames)
    # footer - put the .md file modification date here

    # save the output files
    for art in articles:
        open(get_output_path(art.url, 'articles', project_path), 'w+').write(
                temp_article.render(
                    contents=art.content,
                    head=sub_templates['_head.html'].render(),
                    header=sub_templates['_header.html'].render(),
                    menu=temp_menu,
                    footer=sub_templates['_footer.html'].render()
                ))

    # [TODO] Special case for the index.html?
