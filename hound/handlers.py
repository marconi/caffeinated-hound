"""
Hound: Caffeinated coffee watchdog

Watches root directory of coffee script files,
detects changes and new files then compiles them into
js files preserving directory structure.
"""

import os
import shutil
import logging
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Hound')


class CoffeeEventHandler(FileSystemEventHandler):

    def __init__(self, coffee_root, *args, **kwargs):
        super(CoffeeEventHandler, self).__init__(*args, **kwargs)
        self.coffee_root = coffee_root
        self.js_root = os.path.join(os.path.split(coffee_root)[0], 'js')

    def on_created(self, event):
        super(CoffeeEventHandler, self).on_created(event)
        if not event.is_directory:
            self._compile_coffee(event.src_path)

    def on_deleted(self, event):
        super(CoffeeEventHandler, self).on_created(event)
        if not event.is_directory:
            js_file = self._get_js_file(event.src_path)
            if os.path.exists(js_file):
                logger.info('Deleting %s' % js_file)
                os.unlink(js_file)
        else:
            js_path = event.src_path.replace('coffee', 'js')
            logger.info('Deleting %s' % js_path)
            shutil.rmtree(js_path)

    def on_modified(self, event):
        super(CoffeeEventHandler, self).on_created(event)
        if not event.is_directory:
            self._compile_coffee(event.src_path)

    def _compile_coffee(self, coffee_file):
        if not coffee_file.endswith('.coffee'):
            return

        logger.info('Compiling %s' % coffee_file)

        js_file = self._get_js_file(coffee_file)
        os.system('coffee -cp %(from)s > %(to)s' % {
            'from': coffee_file,
            'to': js_file
        })

    def _get_parent_js_path(self, coffee_file):
        parent_coffee_path = os.path.dirname(coffee_file)
        relative_coffee_path = parent_coffee_path.replace(self.coffee_root, '')[1:]
        parent_js_path = os.path.join(self.js_root, relative_coffee_path)
        if not os.path.exists(parent_js_path):
            os.makedirs(parent_js_path)
        return parent_js_path

    def _get_js_file(self, coffee_file):
        parent_js_path = self._get_parent_js_path(coffee_file)
        filename = os.path.splitext(os.path.basename(coffee_file))[0]
        return '%s.js' % os.path.join(parent_js_path, filename)
