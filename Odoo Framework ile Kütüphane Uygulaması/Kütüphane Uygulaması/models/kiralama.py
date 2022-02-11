# -*- coding: utf-8 -*-
from odoo import models, fields, api


class KitapKiralama(models.Model):
    _name = 'kitap.kiralama' # Veritabanında kitap.kiralama adında tablo oluşturur.
    _inherit = ['mail.thread'] # Odoo 'nun bünyesinde bulundurduğu hazır bir modülden miras alınır.

    kitap_id = fields.Many2one('kitap', 'Kitap', required=True) #Kitap ID'sini tutan attribute.
    kiralık_id = fields.Many2one('res.partner', 'Kiralanan Kişi', required=True) #Kiralanma ID'sini tutan attribute.
    state = fields.Selection([('devam', 'Devam Eden'), ('iade', 'İade Edilen')], # Kitabın durumunu tutan attribute.
                             'Durum', default='devam', required=True)
    kiralanma_tarihi = fields.Date(default=fields.Date.today) #Kiralanma Tarihini tutan attribute.
    iade_tarihi = fields.Date() # İade tarihini tutan attribute.

    @api.model
    def create(self, vals): # Kiralık kaydı oluşturan fonksiyon.
        kitap_kontrolü = self.env['kitap'].browse(vals['kitap_id']) #İstenilen kitabı(vals['kitap_id']) "kitap modülü" içinde arar ve döndürür.
        kitap_kontrolü.kiralık_durumu() #Kitabın kiralık olup olmadığı kontrolü yapılır.
        res = super(KitapKiralama, self).create(vals) # ORM yöntemlerini geçersiz kıldığım için super kullandım. Burda satırdaki amaç yeni bir kullanıcı oluşturmak.
        res.message_subscribe(partner_ids=[res.kiralık_id.id]) # oluşturulan yeni bir kullanıcıyı 'message_subscribe' methodu ile kayıt ettirdim ve bilgiler partner_ids'in içine attım.
        return res

    def book_return(self): # İade edilecek kitap için oluşturulan fonksiyon.
        self.ensure_one() # ensure.one() fonksiyona gönderilen kaydın mevcut olup olmadığını kontrol eder aksi taktirde hata dönndürür.
        self.kitap_id.mevcut_durum() # Kitabın mevcut durumu öğrenilir.
        self.write({ # İade edilen kitap için değerler güncellenir.
            'state': 'iade',
            'iade_tarihi': fields.Date.today()
        })
