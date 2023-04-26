#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Poppler', '0.18')
from gi.repository import Gtk, Gdk
from gi.repository import Poppler
from datetime import datetime
import os

class PdfProperties(object):
    def __init__(self, filename) -> None:
        super(PdfProperties, self).__init__()

        sinais = {
            "on_btn_fechar_clicked":self.fechar,
            "on_win_properties_destroy":self.fechar,
        }

        self.path = os.getcwd()

        self.filename = filename
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.path + "/pdf_properties.glade")

        self.win_properties = self.builder.get_object("win_properties")
        
        self.builder.connect_signals(sinais)

        screen = Gdk.Screen.get_default()

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(self.path + '/style.css')

        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.document_properties()

        self.win_properties.show()

    def document_properties(self):
        document = Poppler.Document.new_from_file (self.filename, None)

        md_date = ["-", "-", "-"]

        n_pages = document.get_n_pages()
        autor = document.get_author()
        creation_date = f"{datetime.fromtimestamp(document.get_creation_date())}"
        c_date = creation_date.split(" ")
        cr_date = c_date[0].split("-")
        creator = document.get_creator()
        if document.get_modification_date() > 0:
            modification_date = f"{datetime.fromtimestamp(document.get_modification_date())}"
            m_date = modification_date.split(" ")
            md_date = m_date[0].split("-")
        pdf_version = document.get_pdf_version_string()
        producer = document.get_producer()
        subject = document.get_subject()
        title = document.get_title()
        
        entry_document = self.builder.get_object("entry_document")
        store_properties = self.builder.get_object("store_properties")

        entry_document.set_text(self.filename)

        store_properties.append(["Autor", autor])
        store_properties.append(["Versão", pdf_version])
        store_properties.append(["Criador", creator])
        store_properties.append(["Produtor", producer])
        store_properties.append(["Data de Criação", f"{cr_date[2]}/{cr_date[1]}/{cr_date[0]}"])
        store_properties.append(["Data de Modificação", f"{md_date[2]}/{md_date[1]}/{md_date[0]}"])
        store_properties.append(["Assunto", subject])
        store_properties.append(["Título", title])
        store_properties.append(["Páginas", f"{n_pages}"])
        
    def fechar(self, widget):
        self.win_properties.destroy()