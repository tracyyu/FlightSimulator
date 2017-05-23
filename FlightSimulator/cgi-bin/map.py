#!/usr/bin/env python

import globals
from jinja2 import Environment, FileSystemLoader
#import cgi
import cgitb
cgitb.enable()

class IndexPage:

    _templateFile = "map.html"
    _templateObj = None

    def __init__(self):

        # initialize global variables
        globals.init();

        #create an environment routed to the template path  
        t_env = Environment(loader=FileSystemLoader(globals.TEMPLATE_DIR))
        
        # get the templates in the template directory
        self._templateObj = t_env.get_template(self._templateFile)
   

    def getPage(self):
        t_rtnHtml = ""
        t_rtnHtml += "Content-Type: text/html; charset=utf-8\r\n\r\n"
        t_rtnHtml += self._templateObj.render()
        return t_rtnHtml


if __name__ == '__main__':
    
    # create an instance of the IndexPage
    t_index = IndexPage()
    print t_index.getPage()

