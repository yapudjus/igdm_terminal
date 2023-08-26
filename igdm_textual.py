import random
from textual import events, on
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll, ScrollableContainer, Horizontal
from textual.widgets import Button, Input, Footer, Placeholder, Markdown, RadioButton, Label, ListItem, ListView
from textual.reactive import var

class interface(App):
    CSS_PATH = "textual.tcss"
    def compose(self) -> ComposeResult:
        with Container(id='all') :
            # with VerticalScroll(id='sidebar') :# docked left bar
            self._Sidebar = ListView(id='sidebar')
            status_list = ['online', 'dnd', 'offline', 'away']
            self.threads = []
            with self._Sidebar:
                for i in range(10):
                    self.threads.append(self.Threadentry(
                        id=f'thread-{i}',
                        threadid=f'threadinstaid-{i}', 
                        selected=False, 
                        hovered=False, 
                        username='username here', 
                        status=random.choice(status_list), 
                        lastmsg='last message here'
                    ))
                    yield self.threads[-1]
                    # with ListItem(classes='threadbox', id=f'thread-{i}'):
                    #     with Horizontal(classes='name-div', id=f'thread-{i}-name-div'):
                    #         status = random.choice(status_list)
                    #         yield Label(classes=f'onlinestatus {status}', id=f'thread-{i}-online-status', renderable='▶')
                    #         yield Label(classes=f'name {status}', id=f'thread-{i}-name', renderable='user name here')
                    #     yield Label(classes='lastmsg', id=f'thread-{i}-last', renderable='last message here')
            with Container(id='msgthread') : # active message tab
                with ScrollableContainer(id="messages"): # message list
                    yield Placeholder()
                with Container(id='msgdiv') : # message box and send button
                    yield Input(id='msginput')
                    yield Button('SEND', id='sendbtn')
        yield Footer()

    class Threadentry(ListItem) :
        def __init__(self, threadid:str, selected:bool, hovered:bool, username:str, status:str, lastmsg:str, id:str):
            self._id=id
            self.threadid:str=threadid
            self.username:str=username
            self._lastmsg:str=lastmsg
            self._status:str=status
            self.selected:bool=selected
            self.hovered:bool=hovered

        class status(object):
            def __init__(self):
                self._observers = []
                self._status = ''
            @property
            def lastmsg(self) -> str: return self._lastmsg

            @lastmsg.setter
            def lastmsg(self, value) -> None:
                self._status = value

                for callback in self._observers:
                    callback(self._lastmsg)

            def bind_to(self, callback): self._observers.append(callback)

        def compose(self) -> ComposeResult :
            with ListItem(classes='threadbox', id=f'thread-{i}'):
                        with Horizontal(classes='name-div', id=f'thread-{i}-name-div'):
                            yield Label(classes=f'onlinestatus {self.status}', id=f'thread-{i}-online-status', renderable='▶')
                            yield Label(classes=f'name {self.status}', id=f'thread-{i}-name', renderable=self.username)
                        yield Label(classes='lastmsg', id=f'thread-{i}-last', renderable=self.lastmsg)

    @on(ListView.Selected, selector='sidebar')
    def sidebar_handler(self):
        pass


if __name__ == '__main__' :
    interface().run()