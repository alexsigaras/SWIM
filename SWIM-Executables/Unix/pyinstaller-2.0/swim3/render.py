# -*- coding: utf-8 -*-
#############################################
## (C)opyright by Dirk Holtwick            ##
## All rights reserved                     ##
#############################################

__version__ = "$Revision: 176 $"
__author__ = "$Author: kgrodzicki $"
__date__ = "$Date: 2011-01-15 10:11:47 +0100 (Fr, 15 July 2011) $"

"""
HTML/CSS to PDF converter
Test background image generation on the `portrait` and `landscape`
page.
"""

from cookbook import HTML2PDF
import sys, os


if __name__ == "__main__":    
    xhtml = open(sys.argv[1])
    try:
    	filename = sys.argv[2]
    	if not len(filename):
    		raise Exception
    except:
    	filename = sys.argv[1].split('.')[0] + '.pdf'
    HTML2PDF(xhtml.read(), filename)
    os.remove(sys.argv[1])
# def render(html_fn, filename):
#     #print html_fn
#     #xhtml = open(html_fn)
#     #print xhtml.read()
#     HTML2PDF(html_fn, filename)