import urwid

palette = [
    (None,  'light gray', 'black'),
    ('heading', 'black', 'light gray'),
    ('line', 'black', 'light gray'),
    ('options', 'dark gray', 'black'),
    ('focus heading', 'white', 'dark red'),
    ('focus line', 'black', 'dark red'),
    ('focus options', 'black', 'light gray'),
    ('selected', 'white', 'dark blue')
]

focus_map = {
    'heading': 'focus heading',
    'options': 'focus options',
    'line': 'focus line'
}

class MenuButton(urwid.Button):
    def __init__(self, text):
        super(MenuButton, self).__init__(text)
        self._w = urwid.AttrMap(self._w, None, 'selected')

class Menu(urwid.ListBox):
    def __init__(self, caption, choices):
        header = urwid.AttrMap(urwid.Text(caption, align='center'), 'heading')
        super(Menu, self).__init__(urwid.SimpleFocusListWalker([header, urwid.Divider()] + choices))

def main():
    columns = urwid.Columns([], dividechars=1)
    
    columns.contents.append((urwid.AttrMap(Menu('Plugins', [MenuButton('Uitzending Gemist'), MenuButton('YouTube')]), 'options', focus_map),
                             columns.options('given', 24)))
    columns.contents.append((urwid.AttrMap(Menu('YouTube', [MenuButton('Problems with Zero - Numberphile'), MenuButton('Infite Primes - Numberphile')]), 'options', focus_map),
                             columns.options('weight', 24)))
    
    urwid.MainLoop(columns, palette).run()
    
if __name__ == '__main__':
    main()