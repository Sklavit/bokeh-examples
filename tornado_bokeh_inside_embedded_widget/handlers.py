# coding=utf-8
from collections import defaultdict
from datetime import datetime
from random import randint
import random

import bokeh
import bokeh.application as bokeh_app
import tornado.web
from bokeh.application.handlers import FunctionHandler
from bokeh.document import Document
from bokeh.embed import autoload_server
from bokeh.layouts import column, widgetbox
from bokeh.models import ColumnDataSource, Button, TableColumn, DateFormatter, DataTable
from tornado import gen

data_by_user = defaultdict(lambda: dict(file_names=[], dates=[], downloads=[]))
doc_by_user_str = dict()
source_by_user_str = dict()

data = dict(x=[], y=[])

class SecondHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("second_page_template.html")

    @gen.coroutine
    def post(self, *args, **kwargs):
        user_str = str(self.current_user)

        data['x'] = random.sample(range(10), 10)
        data['y'] = random.sample(range(10), 10)

        data_by_user[user_str] = data

        source = source_by_user_str[user_str]

        @gen.coroutine
        def update():
            source.data = data

        doc = doc_by_user_str[user_str]  # type: Document
        
        # Bryan Van de Ven @bryevdv Feb 27 22:23
        # @Sklavit actually I can see why next_tick_callback would be needed from another request handler. 
        # We had other threads in mind but it's also the case that nothing triggering your other request handler 
        # would acquire a bokeh document lock, so you need to request one by using next_tick_callback
        doc.add_next_tick_callback(update)  

        self.render('second_page_template.html')


class MainHandler(tornado.web.RequestHandler):
    @staticmethod
    def modify_doc(doc):
        source = ColumnDataSource(dict(x=[], y=[]))

        columns = [
            TableColumn(field="x", title="X"),
            TableColumn(field="y", title="Y"),
        ]

        data_table = DataTable(source=source, columns=columns)

        user_str = doc.session_context.id
        doc_by_user_str[user_str] = doc
        source_by_user_str[user_str] = source
        
        doc.add_root(widgetbox(data_table))

    _bokeh_app = None

    @classmethod
    def get_bokeh_app(cls):
        if cls._bokeh_app is None:
            cls._bokeh_app = bokeh.application.Application(FunctionHandler(MainHandler.modify_doc))
        return cls._bokeh_app

    @gen.coroutine
    def get(self):
        user_str = str(self.current_user)
        script = autoload_server(model=None, session_id=user_str,  # NOTE: MUST be string
                                 app_path='/bokeh/app',
                                 url='http://localhost:5006')

        self.render(
                'main_page_template.html', active_page='inks_upload',
                script=script
        )
