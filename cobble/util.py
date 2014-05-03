# -*- coding: UTF-8 -*-

"""File for all the small utility functions useful across the module.
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

import os # path

def setup_dirs(project_path):
    """Setup the project dir and all subdirs (static/, blog/, css/, font/...)"""
    # Do nothing if all the dirs exist
    pass

def abs_file_paths(directory):
    """Return a list of absolute paths of files in a given directory"""
    paths = []
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            paths.append(os.path.abspath(os.path.join(dirpath, f)))

    return sorted(paths)

def get_output_path(filename, static_type, project_path):
    return project_path+'/static/'+static_type+'/'+filename

def parse_tags_to_dict(taglist):
    """Given a list of tag line strings, return a dict with tag:value pairs"""

    if taglist:

        tag_dict = {}
        for pair in taglist:
            split_pair = pair.split(': ')
            tag_dict[split_pair[0].lower()] = split_pair[1]

        return tag_dict
