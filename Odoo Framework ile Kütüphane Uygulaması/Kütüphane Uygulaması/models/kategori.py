# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class KitapKategorisi(models.Model):
    _name = 'kitap.kategorisi' # Veritabanında kitap.kategorisi adında tablo oluşturur.

    _parent_store = True # Kategorinin olup olmadığının bilgisini tutan değişken.
    _parent_name = "parent_id" #Üst Kategori Adını tutan değişken.

    name = fields.Char('Kategori') #Kategori adını tutan attribute. (Char tipinde)
    parent_id = fields.Many2one( # Üst Kategori İd'sini tutan attribute.
        'kitap.kategorisi',
        string='Üst Kategori',
        ondelete='restrict',
        index=True
    )
    child_ids = fields.One2many( #Alt Kategori İd'sini tutan attribute.
        'kitap.kategorisi', 'parent_id',
        string='Alt Kategori')
    parent_path = fields.Char(index=True)  # Üst Kategori Bilgilerini Tutan Değişken

    @api.constrains('parent_id') # @api.constrains ile fonksiyon create,write v.b gibi işlemleri çağırabilir.
    def _check_hierarchy(self): #Üst ve Alt Kategori Bağlılığını Kontrol Eden Fonksiyon
        if not self._check_recursion(): # Eğer alt kategori üst kategoriye bağlı değilse durumu
            raise models.ValidationError('Hatalı Giriş ! Kategori Bulunmaktadır.') # Hata Mesajı