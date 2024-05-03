# Configuration file for the Sphinx documentation builder.

# -- Project information

import os
import sys

sys.path.insert(0, os.path.abspath('../src/'))
project = 'bitbox'
copyright = '2024, kal'
author = 'Kvolts'

release = ''
# version = '0.1.0'

# -- General configuration

# extensions = ['sphinx.ext.autodoc', 
#               'sphinx.ext.todo', 
#               'sphinx.ext.doctest',
#               'sphinx.ext.autosummary',
#               'sphinx.ext.viewcode',
#               'sphinx.ext.napoleon']

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    "sphinx.ext.githubpages", # ? 
    "sphinx.ext.viewcode", # ? 


]

# sphinx.ext.autodoc
autoclass_content = "both"
autodoc_member_order = "bysource"

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

# templates_path = ['_templates']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'


html_show_sourcelink = False