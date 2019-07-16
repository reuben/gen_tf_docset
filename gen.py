import argparse
import fnmatch
import misaka
import os
import pygments
import shutil

from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

replace_with_style = '<p>page_type: reference<br>\n<style>{% include &quot;site-assets/css/style.css&quot; %}</style>'

class HighlighterRenderer(misaka.HtmlRenderer):
    def blockcode(self, text, lang):
        if not lang:
            lang = 'text'
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except:
            lexer = get_lexer_by_name('text', stripall=True)
        formatter = HtmlFormatter()
        return pygments.highlight(text, lexer, formatter)

    def table(self, header, body):
        return '<table class="table">\n' + header + '\n' + body + '\n</table>'


def main(markdown_root, html_root):
    renderer = misaka.Markdown(HighlighterRenderer(flags=('hard-wrap',)),
        extensions=('fenced-code', 'no-intra-emphasis', 'tables', 'autolink', 'space-headers', 'strikethrough', 'superscript'))

    root_len = len(markdown_root)
    for root, dirnames, filenames in os.walk(markdown_root):
        for filename in fnmatch.filter(filenames, '*.md'):
            md_file = os.path.join(root, filename)
            out_file = os.path.splitext(md_file)[0] + '.html'

            # Remove markdown root from path and append to HTML output root
            out_file = os.path.join(html_root, out_file[root_len:])

            # If destination folder does not exist, create it
            out_dir = os.path.dirname(out_file)
            if not os.path.exists(out_dir):
                os.makedirs(os.path.dirname(out_file))

            # Render Markdown and write it
            with open(md_file, 'r') as fin, open(out_file, 'w') as fout:
                rendered = renderer(fin.read())
                # Replace initial metadata with link to our style
                style_link = '<link rel="stylesheet" href="' + ('../' * (len(out_file.split(os.sep)) - 2)) + 'style.css"/>\n'
                if rendered[:len(replace_with_style)] == replace_with_style:
                    rendered = rendered[len(replace_with_style):] + '<p>'
                rendered = style_link + rendered
                fout.write(rendered)

    shutil.copy(os.path.join(markdown_root, '_toc.yaml'), html_root)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('markdown_root', help='Root dir with TensorFlow generated Markdown docs')
    parser.add_argument('html_root', help='Root dir to save rendered HTML files.')
    args = parser.parse_args()
    main(args.markdown_root, args.html_root)
