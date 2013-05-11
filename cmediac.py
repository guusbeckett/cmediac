#!/usr/bin/env python

import urwid
import os
import imp
import subprocess
import configparser

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

CONFIG_PATH = ".cmediac/config"
PLUGIN_PATHS = [".cmediac/plugins", "plugins"]

class MenuButton(urwid.Button):
    def __init__(self, text, callback):
        super(MenuButton, self).__init__(text)
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(self._w, None, 'selected')
        
class Menu(urwid.WidgetWrap):
    def __init__(self, caption, choices):
        header = urwid.AttrMap(urwid.Text(caption, align='center'), 'heading')
        self._w = urwid.AttrMap(urwid.ListBox(urwid.SimpleFocusListWalker([header, urwid.Divider()] + choices)), 'options', focus_map)

class ItemButton(MenuButton):
    def __init__(self, item):
        super(ItemButton, self).__init__(item.title, self.selected)
        self.item = item
       
    def selected(self, button):
        if hasattr(self.item, 'get_items'):
            buttons = [ItemButton(item) for item in self.item.get_items()]
            categories = [item for item in self.item.get_items() if hasattr(item, 'get_items')]
            columns.contents = columns.contents[:columns.focus_position+1] + [(Menu(self.item.title, buttons), columns.options('weight' if len(categories) == 0 else 'given', 20))]
            columns.focus_position += 1
        else:
            subprocess.Popen([config.get('settings', 'player', fallback='omxplayer'), self.item.get_url()])
        
class PluginButton(MenuButton):
    def __init__(self, plugin):
        self.plugin = plugin
        super(PluginButton, self).__init__(plugin.title, self.selected)
        
    def selected(self, button):
        category_buttons = [ItemButton(category) for category in self.plugin.get_items()]
        columns.contents = columns.contents[:1] + [(Menu(self.plugin.title, category_buttons), columns.options('given', 20))]
        columns.focus_position = 1

def exit_program(button):
    raise urwid.ExitMainLoop()

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

plugin_buttons = [MenuButton('Exit', exit_program)]

for path in [path for path in PLUGIN_PATHS if os.path.exists(path)]:
    for filepath in os.listdir(path):
        filepath = path + '/' + filepath
        modname, extension = os.path.splitext(os.path.split(filepath)[-1])
        
        if extension == '.py':
            module = imp.load_source(modname, filepath)
            
            if hasattr(module, 'Plugin'):
                plugin = module.Plugin(config)
                plugin_buttons.append(PluginButton(plugin))

columns = urwid.Columns([], dividechars=1)
columns.contents.append((Menu('cmediac', plugin_buttons), columns.options('given', 15)))
urwid.MainLoop(columns, palette).run()