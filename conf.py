import sys
import os

extensions = [
    'sphinx.ext.autodoc',
    'sphinxcontrib.httpdomain'
]

templates_path = ['_templates']

source_suffix = ['.rst', '.md']

master_doc = 'index'

#project = u'InfinniPlatform'
#copyright = u'2016, Infinnity Solutions'
#author = u'Infinnity Solutions'


#version = u'1.5.0'

#release = u'1.5.0'

language = 'ru'

exclude_patterns = []

pygments_style = 'sphinx'

todo_include_todos = False


html_theme = 'default'

html_static_path = ['_static']


htmlhelp_basename = 'InfinniPlatformdoc'

latex_elements = {

}

latex_documents = [
    (master_doc, 'InfinniPlatform.tex', u'InfinniPlatform Documentation',
     u'Infinnity Solutions', 'manual'),
]

man_pages = [
    (master_doc, 'infinniplatform', u'InfinniPlatform Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'InfinniPlatform', u'InfinniPlatform Documentation',
     author, 'InfinniPlatform', 'One line description of project.',
     'Miscellaneous'),
]
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright


on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
