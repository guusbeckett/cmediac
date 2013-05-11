#!/usr/bin/env python

import urwid
import os
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
        
class Menu(urwid.WidgetWrap):
    def __init__(self, caption, choices):
        header = urwid.AttrMap(urwid.Text(caption, align='center'), 'heading')
        self._w = urwid.AttrMap(urwid.ListBox(urwid.SimpleFocusListWalker([header, urwid.Divider()] + choices)), 'options', focus_map)
        
class MediaButton(MenuButton):
    def __init__(self, media):
        super(MediaButton, self).__init__(media.title, self.selected)
        self.media = media
       
    def selected(self, button):
        subprocess.Popen(['omxplayer', self.media.get_url()])
        
class PluginButton(MenuButton):
    def __init__(self, plugin):
        self.plugin = plugin
        super(PluginButton, self).__init__(plugin.name, self.selected)
        
    def selected(self, button):
        media_buttons = [MediaButton(media) for media in self.plugin.get_media()]
        columns.contents = columns.contents[0:] + [(Menu(self.plugin.name, media_buttons), columns.options('weight', 24))]
        columns.focus_position = 1

def exit_program(button):
    raise urwid.ExitMainLoop()

plugin_buttons = [MenuButton('Exit', exit_program)]

for filepath in os.listdir('plugins'):
    filepath = 'plugins/' + filepath
    modname, extension = os.path.splitext(os.path.split(filepath)[-1])
    
    if extension == '.py':
        module = imp.load_source(modname, filepath)
        
        if hasattr(module, 'Plugin'):
            plugin = module.Plugin()
            plugin_buttons.append(PluginButton(plugin))

columns = urwid.Columns([], dividechars=1)
columns.contents.append((Menu('cmediac', plugin_buttons), columns.options('given', 24)))
urwid.MainLoop(columns, palette).run()