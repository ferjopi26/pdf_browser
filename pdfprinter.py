#!/usr/bin/python
# -*- coding: utf-8 -*-

from unicodedata import east_asian_width
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Poppler', '0.18')
from gi.repository import Poppler
from gi.repository import Gtk, Gdk

class PDFPrinter:
    def __init__(self, filename, jobname, width, height):
        self.width = width
        self.height = height

        self.document = Poppler.Document.new_from_file (filename, None)
        
        papersize = Gtk.PaperSize.new_custom("cc", "cc", width, height, Gtk.Unit.POINTS)
        
        setup = Gtk.PageSetup()
        setup.set_paper_size(papersize)
        
        po = Gtk.PrintOperation()
        po.set_default_page_setup(setup)
        po.set_use_full_page(True)
        po.set_job_name(jobname)
        po.set_show_progress(True)
        po.set_n_pages(self.document.get_n_pages())
        po.connect("draw_page", self.draw_page)
        po.run(Gtk.PrintOperationAction.PRINT_DIALOG, None)
        
    def draw_page (self, operation, context, page_num):
        page = self.document.get_page(page_num)
        page.render_for_printing(context.get_cairo_context())
