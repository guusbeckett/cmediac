import urwid
import os
import glob
import imp
import subprocess

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
    def __init__(self, text, callback):
        super(MenuButton, self).__init__(text)
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(self._w, None, 'selected')
        
class Media(MenuButton):
    def __init__(self, plugin, item):
        super(Media, self).__init__(item[0], self.selected_media)
        self.plugin = plugin
        self.url = item[1]
       
    def selected_media(self, button):
        subprocess.Popen(['mplayer', self.plugin.get_media(self.url)])
        
class Plugin(MenuButton):
    def __init__(self, filename):
        name = os.path.basename(filename)[:-3]
        fp, pathname, description = imp.find_module(name, [os.path.dirname(filename)])
        self.plugin = imp.load_module(name, fp, pathname, description)
        super(Plugin, self).__init__(self.plugin.get_name(), self.selected_plugin)
        
    def selected_plugin(self, button):
        menu_items = []
        
        for item in self.plugin.get_links():
            menu_items.append(Media(self.plugin, item))
        
        if len(columns.contents) > 1:
            del columns.contents[1]

        columns.contents.append((Menu(self.plugin.get_name(), menu_items), columns.options('weight', 24)))
        columns.focus_position = 1

class Menu(urwid.WidgetWrap):
    def __init__(self, caption, choices):
        header = urwid.AttrMap(urwid.Text(caption, align='center'), 'heading')
        self._w = urwid.AttrMap(urwid.ListBox(urwid.SimpleFocusListWalker([header, urwid.Divider()] + choices)), 'options', focus_map)

def exit_program(button):
    raise urwid.ExitMainLoop()

plugins = [Plugin(filename) for filename in glob.glob('plugins/*.py')]

columns = urwid.Columns([], dividechars=1)
columns.contents.append((Menu('cmediac', [MenuButton('Exit', exit_program)] + plugins), columns.options('given', 24)))
urwid.MainLoop(columns, palette).run()