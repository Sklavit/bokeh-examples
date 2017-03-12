# coding=utf-8
from bokeh.server.server import Server

def get_bokeh_server(io_loop, bokeh_applications: dict):
    server = Server(bokeh_applications,
                    io_loop=io_loop, allow_websocket_origin=['localhost:8888'])

    return server