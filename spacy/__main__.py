# coding: utf8
from __future__ import print_function
# NB! This breaks in plac on Python 2!!
#from __future__ import unicode_literals

if __name__ == '__main__':
    import plac
    import sys
    from spacy.cli import download, link, info, package, train, convert, model
    from spacy.cli import profile
    from spacy.util import prints

    commands = {
        'download': download,
        'link': link,
        'info': info,
        'train': train,
        'convert': convert,
        'package': package,
        'model': model,
        'profile': profile,
    }
    if len(sys.argv) == 1:
        prints(', '.join(commands), title="Available commands", exits=1)
    command = sys.argv.pop(1)
    sys.argv[0] = 'spacy %s' % command
    if command in commands:
        plac.call(commands[command])
    else:
        prints(
            "Available: %s" % ', '.join(commands),
            title="Unknown command: %s" % command,
            exits=1)
