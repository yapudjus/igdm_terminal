from contextlib import ExitStack
import random, json, datetime
from textual import events, on, log
from textual.app import App, ComposeResult, Widget
from textual.containers import Container, VerticalScroll, ScrollableContainer, Horizontal, Vertical
from textual.widgets import Button, Input, Footer, Placeholder, Markdown, RadioButton, Label, ListItem, ListView, Pretty, Static
from textual.reactive import var

class interface(App):
    CSS_PATH = "textual.tcss"
    BINDINGS = [
        ('/', 'jump_msg', 'jump to send'),
        ('home', 'jump_threadlist', 'to thread list')
    ]
    def compose(self) -> ComposeResult:
        lorem = 'Quod consequatur iste tempore et. Necessitatibus sunt occaecati officia sint. Eaque neque fugiat repellat. Ea incidunt et error animi a aliquid.Aliquid reprehenderit velit non ad non non rerum aperiam. Accusamus et culpa tenetur minima quas quis. Quod eveniet iusto quis saepe. Dolores minus natus sit quia modi suscipit iure similique. Voluptatem rerum sint ut optio nulla sequi illo.Perspiciatis nihil aut temporibus exercitationem minus quae excepturi. Ut nisi harum sunt hic. Et fugiat nostrum quo mollitia facilis alias dolores. Quis voluptate dolore distinctio autem temporibus.Assumenda nam quidem incidunt consequuntur a earum. Qui provident alias enim perspiciatis aperiam'.split(' ')
        with open('cache/saved_usernames.json', 'r') as file: 
            userlist = list()
            tmp = json.load(file)
            self.log(tmp)
            for i in tmp :
                userlist.append(tuple((i, tmp[i])))
        self._bodycontainer = Container(id='all')
        with self._bodycontainer :
            # with VerticalScroll(id='sidebar') :# docked left bar
            self._Sidebar = ListView(id='sidebar')
            status_list = ['online', 'dnd', 'offline', 'away']
            self.threads = []
            with self._Sidebar:
                for i in range(25):
                    usr= random.choice(userlist)
                    self.threads.append(self.Threadentry(
                        id=f'threadinstaid-{i}', 
                        threadid=usr[0],
                        selected=False, 
                        hovered=False, 
                        username=usr[1], 
                        status=random.choice(status_list), 
                        lastmsg=str(' '.join(random.choices(lorem, k=random.randint(1, len(lorem)))))
                    ))
                for thread in self.threads:
                    for items in thread.compose(): yield items

            self._msgthread = Vertical(id='msgthread')
            with self._msgthread : # active message tab
                self._messagebox = VerticalScroll(id="messages", disabled=False)
                with self._messagebox: # message list
                    self.msglist = []
                    for i in range(4):
                        self.msglist.append(self.MessageEntry(
                            msgid=str(i),
                            username=random.choice(userlist)[1],
                            msgcontent=str(' '.join(random.choices(lorem, k=random.randint(1, len(lorem))))),
                            msgtime=f'{str(random.randint(0,24)).zfill(2)}:{str(random.randint(0,59)).zfill(2)}:{str(random.randint(0,59)).zfill(2)}'
                        ))
                    for message in self.msglist:
                        for item in message.compose() : yield item
                    self.log(self.app._compose_stacks)
                yield Input(id='msginput', placeholder='➔ message to send')
                
        yield Footer()

    def action_jump_msg(self) -> None:
        """jump to msg input"""
        self.query_one(selector='#msginput').focus()
    
    def action_jump_threadlist(self) -> None:
        """jump to threadlist"""
        self.query_one(selector='#sidebar').focus()
    
    @on(Input.Submitted, '#msginput')
    def InputSubmitHandler(self) -> None:
        qres = self.query_one("#messages")
        # self.log(qres)
        # self.log(f'{self.ancestors_with_self(self=qres)}')
        msginput = self.query_one(selector='#msginput')
        msginput.value = 'SENDING...'
        self.sendMSG(value=msginput.value)
        self._messages__ancestorlist:list = self.query_one('#messages').ancestors_with_self
        self.appendMSG(len(self.msglist)-1)
        msginput.value = ''
    
    def sendMSG(self, value) -> None:
        self.msglist.append(self.MessageEntry(
            msgcontent=value,
            msgid=str(len(self.msglist)),
            username='you',
            msgtime=self.rendertime()
        ))
    
    def appendMSG(self, id) -> None:
        # for item in self.msglist[id].compose(): self.mount(item, after=f'#msg-{int(id)-1}'
        # with self.query_one('#messages'): 
        # self.mount_all([Placeholder('tes')], before='#messages')
        with ExitStack() as stack :
            
            for i in reversed(self._messages__ancestorlist[:-2]) : stack.enter_context(i)
            self.mount_all(self.msglist[id].testcomp(), before='#messages')
        
    def rendertime(self) -> str:
        return str(datetime.datetime.now().strftime('%H:%M:%S'))

    class MessageEntry():
        def __init__(self, msgid:str, username:str, msgtime:str, msgcontent:str):
            self.msgid = msgid
            self.msgtime = msgtime
            self.msgvalue = msgcontent
            self.username = username
        
        def testcomp(self) -> ComposeResult:
            res = []
            with Horizontal(classes='message', id=f'msg-{self.msgid}', disabled=False):
                with Horizontal(classes='horizontal-1'):
                    res.append(Label(
                        id=f'message-{self.msgid}-username', 
                        classes='username',
                        renderable=self.username
                        ))
                    res.append(Label(
                        classes='separator1',
                        renderable='@'
                        ))
                    res.append(Label(
                        id=f'message-{self.msgid}-time', 
                        classes='time',
                        renderable=self.msgtime
                        ))
                with Horizontal(classes='horizontal-2'):
                    res.append(Label(
                        classes='separator1',
                        renderable='➟'
                    ))
                    res.append(Label(
                        classes='message-content',
                        id=f'message-{self.msgid}-content', 
                        renderable=self.msgvalue,
                        shrink=True
                    ))
            return res

        def compose(self) :
            with ListItem(classes='message', id=f'msg-{self.msgid}', disabled=False):
                with Horizontal(classes='horizontal-1'):
                    yield Label(
                        id=f'message-{self.msgid}-username', 
                        classes='username',
                        renderable=self.username
                        )
                    yield Label(
                        classes='separator1',
                        renderable='@'
                        )
                    yield Label(
                        id=f'message-{self.msgid}-time', 
                        classes='time',
                        renderable=self.msgtime
                        )
                with Horizontal(classes='horizontal-2'):
                    yield Label(
                        classes='separator1',
                        renderable='➟'
                    )
                    yield Label(
                        classes='message-content',
                        id=f'message-{self.msgid}-content', 
                        renderable=self.msgvalue,
                        shrink=True
                    )
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