import urwid
import os
import glob
import imp

palette = [
    (None,  'light gray', 'black'),
    ('heading', 'black', 'light gray'),
    ('line', 'black', 'light gray'),
    ('options', 'dark gray', 'black'),
    ('focus heading', 'white', 'dark red'),
    ('focus line', 'black', 'dark red'),
    ('selected', 'white', 'dark blue')
]

focus_map = {
    'heading': 'focus heading',
    'line': 'focus line'
}

class MenuButton(urwid.Button):
    def __init__(self, text):
        super(MenuButton, self).__init__(text)
        self._w = urwid.AttrMap(self._w, None, 'selected')
        
class Plugin(MenuButton):
    def __init__(self, filename):
        name = os.path.basename(filename)[:-3]
        fp, pathname, description = imp.find_module(name, [os.path.dirname(filename)])
        plugin = imp.load_module(name, fp, pathname, description)
        super(Plugin, self).__init__(plugin.get_name())

class Menu(urwid.WidgetWrap):
    def __init__(self, caption, choices):
        header = urwid.AttrMap(urwid.Text(caption, align='center'), 'heading')
        self._w = urwid.AttrMap(urwid.ListBox(urwid.SimpleFocusListWalker([header, urwid.Divider()] + choices)), 'options', focus_map)

def main():
    columns = urwid.Columns([], dividechars=1)
    
    plugins = []
    
    for filename in glob.glob('plugins/*.py'):
        plugins.append(Plugin(filename))
    
    columns.contents.append((Menu('cmediac', [MenuButton('Exit')] + plugins), columns.options('given', 24)))
#   columns.contents.append((urwid.AttrMap(Menu('YouTube', [MenuButton('Problems with Zero - Numberphile'), MenuButton('Infite Primes - Numberphile')]), 'options', focus_map),
#                            columns.options('weight', 24)))
    
    urwid.MainLoop(columns, palette).run()
    
if __name__ == '__main__':
    main()