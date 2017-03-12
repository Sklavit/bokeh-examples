# Tornado HTTP web page with embedded Bokeh widget which communicates with other page of the same application

Tornado HTTP web page with embedded Bokeh widget which communicates with other page of the same application.

## Features

* Full Tornado server
* Bokeh server is started from Tornado server and is executed in the same ioloop
* Embedded Bohek widget by `autoload_server`
* 2 web page communication:
  * one page is data source
  * the second one (with bokeh widgte) is data receiver
* communicated data is bound to `user_id`

## References
https://github.com/bokeh/bokeh/blob/0.12.4/examples/howto/server_embed/tornado_embed.py
http://bokeh.pydata.org/en/latest/docs/user_guide/embed.html#server-data
http://bokeh.pydata.org/en/latest/docs/user_guide/server.html#embedding-bokeh-server-as-a-library
http://bokeh.pydata.org/en/latest/docs/reference/embed.html#bokeh.embed.autoload_server

## Requirement
[conda environment description](environment.yml)
