import random
from textual import events, on, log
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll, ScrollableContainer, Horizontal
from textual.widgets import Button, Input, Footer, Placeholder, Markdown, RadioButton, Label, ListItem, ListView, Pretty
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
                    for items in self.threads[-1].compose(): yield items
                    # with ListItem(classes='threadbox', id=f'thread-{i}'):
                    #     with Horizontal(classes='name-div', id=f'thread-{i}-name-div'):
                    #         status = random.choice(status_list)
                    #         yield Label(classes=f'onlinestatus {status}', id=f'thread-{i}-online-status', renderable='▶')
                    #         yield Label(classes=f'name {status}', id=f'thread-{i}-name', renderable='user name here')
                    #     yield Label(classes='lastmsg', id=f'thread-{i}-last', renderable='last message here')
                    log(self.threads[0])
            with Container(id='msgthread') : # active message tab
                with ScrollableContainer(id="messages"): # message list
                    yield Placeholder()
                with Container(id='msgdiv') : # message box and send button
                    yield Input(id='msginput')
                    yield Button('SEND', id='sendbtn')
        yield Footer()

    class Threadentry() :
        def __init__(self, threadid:str, selected:bool, hovered:bool, username:str, status:str, lastmsg:str, id:str):
            self.id=id
            self._name:str = username
            self.threadid:str=threadid
            self.username:str=username
            self.lastmsg:str=lastmsg
            self.status:str = status
            self.selected:bool=selected
            self.hovered:bool=hovered

        # class Status(object):
        #     def __init__(self):
        #         self._observers = []
        #         self._status = ''
        #     @property
        #     def status(self) -> str: return self._status

        #     @status.getter(self)
        #     def status(self) -> str: return self._status

        #     @status.setter
        #     def status(self, value) -> None:
        #         self._status = value
        #         for callback in self._observers:
        #             callback(self._status)

        #     def bind_to(self, callback): self._observers.append(callback)

        def compose(self) -> ComposeResult :
            with ListItem(classes='threadbox', id=f'{self.id}'):
                        with Horizontal(classes='name-div', id=f'{self.id}-name-div'):
                            yield Label(classes=f'onlinestatus {self.status}', id=f'{self.id}-online-status', renderable='▶')
                            yield Label(classes=f'name {self.status}', id=f'{self.id}-name', renderable=self.username)
                        yield Label(classes='lastmsg', id=f'{self.id}-last', renderable=self.lastmsg)

    @on(ListView.Selected, selector='sidebar')
    def sidebar_handler(self):
        pass


if __name__ == '__main__' :
    interface().run()