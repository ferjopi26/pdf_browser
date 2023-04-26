#!/usr/bin/python
# -*- coding: utf-8 -*-

from turtle import width
import gi
gi.require_version('Poppler', '0.18')
gi.require_version('Gtk', '3.0')
from gi.repository import Poppler
from gi.repository import Gtk, Gdk
from pdf_properties import PdfProperties
from pdfprinter import PDFPrinter
import os
import cairo

class PdfBrowser(object):
    def __init__(self) -> None:
        super(PdfBrowser, self).__init__()

        sinais = {
            "on_itm_abrir_activate":self.abrir,
            "on_itm_imprimir_activate":self.imprimir,
            "on_itm_sair_activate":self.sair,
            "on_mainwindow_destroy":self.sair,
            "on_page_selector_value_changed":self.changed,
            "on_mnu_properties_activate":self.properties,
        }

        self.path = os.getcwd()

        self.current_page = 0

        self.filename = ""
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.path + "/pdf_browser.glade")

        self.main_window = self.builder.get_object("mainwindow")

        self.dwg = self.builder.get_object("dwg")
        self.page_selector = self.builder.get_object("page_selector")
        self.label_max_page = self.builder.get_object("label_max_page")
        
        self.builder.connect_signals(sinais)

        self.dwg.connect("draw", self.draw)

        screen = Gdk.Screen.get_default()

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(self.path + '/style.css')

        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.main_window.show()

    def open_pdf_document(self, filename):
        self.uri = "file:" + filename
        
        title = filename.split('/')
        title.reverse()
        self.main_window.set_title(title[0])

        self.document = Poppler.Document.new_from_file (self.uri, None)
        self.n_pages = self.document.get_n_pages()
        self.current_page = self.document.get_page(0)
        self.width, self.height = self.current_page.get_size()

        self.dwg.width = self.width
        self.dwg.height = self.height

        adjustment = Gtk.Adjustment()
        adjustment.configure(1, 1, self.n_pages, 1, 10, 0)
        self.page_selector = self.builder.get_object("page_selector")
        self.page_selector.set_adjustment(adjustment)
        self.page_selector.connect("value-changed", self.changed)
        self.label_max_page.set_text(f"{self.n_pages} Páginas")

        self.page_selector.grab_focus()

    def draw(self, widget, cr):
        if self.current_page == 0:
            return
        width, height = self.current_page.get_size()
        
        self.dwg.set_size_request(int(width), int(height))
        
        self.current_page.render(cr)
    
    def abrir(self, widget):
        dialog = Gtk.FileChooserDialog(title="Abrir Documento PDF", parent=self.main_window, action=Gtk.FileChooserAction.OPEN)

        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        filter_pdf = Gtk.FileFilter()
        filter_pdf.set_name("Documentos pdf")
        filter_pdf.add_pattern("*.pdf")
        dialog.add_filter(filter_pdf)

        filter_pdf = Gtk.FileFilter()
        filter_pdf.set_name("Documentos PDF")
        filter_pdf.add_pattern("*.PDF")
        dialog.add_filter(filter_pdf)

        dialog.set_local_only(False)
        dialog.set_current_folder(self.path)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.path = dialog.get_current_folder()
            self.filename = dialog.get_filename()
            self.open_pdf_document(self.filename)
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def sair(self, widget):
        Gtk.main_quit()

    def imprimir(self, widget):
        try:
            PDFPrinter(self.uri, self.main_window.get_title(), self.dwg.width, self.dwg.height)
        except:
            return
        
    def changed(self, widget):
        self.current_page = self.document.get_page(widget.get_value_as_int() - 1)
        self.dwg.queue_draw()

    def properties(self, widget):
        if self.filename == "":
            return
        uri = "file:" + self.filename
        PdfProperties(uri)

    def main(self):
        Gtk.main()

pdf_browser = PdfBrowser()
pdf_browser.main()
