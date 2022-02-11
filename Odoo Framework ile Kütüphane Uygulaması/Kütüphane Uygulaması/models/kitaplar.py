# -*- coding: utf-8 -*-
from odoo import models, fields, _
from odoo.exceptions import UserError


class Kitaplar(models.Model):
    _name = 'kitap'   # Veritabanında kitap adında tablo oluşturur.
    _description = 'Kütüphane Uygulaması' # Odoo'da ki uygulama adı belirlenir.

 # Kitap adında oluşturulan tablonun attribute(özellikleri) değerleri belirlenir.
 # 'fields' ile alanlar yani attribute'lar oluşturulur. Eklenecek attribute tipine göre noktadan sonraki kısım değişebilir.

    name = fields.Char('Kitap Adı', required=True) #Kitap adını tutan attribute. (Char tipinde)
    yayinlanma_tarihi = fields.Date('Yayınlanma Tarihi') #Yayınlanma Tarihini tutan attribute. (Date tipinde)
    mevcut = fields.Boolean(default=True) # Kitabın mevcut olup olmadığı bilgisini tutan attribute. (Bool türünde)
    yazar_id = fields.Many2many('res.partner', string='Yazar') # Kitabın yazarını tutan attribute. (Many2many olmasının sebebi kullanılan res.partner'in diğer modellerde de kullanulacak olması.)
    state = fields.Selection( # O andaki durumu tutan attribute. (Selection kullanıldı çünkü birden fazla durum mevcut olucak ve seçim yapılıcak.)
        [('mevcut', 'Mevcut'),
         ('kiralık', 'Kiralık'),
         ('kayıp', 'Kayıp')],
        'State', default="mevcut")
    kitap_ucreti = fields.Float('Kitap Fiyatı') #kitap fiyatını tutan attribute.
    kategori_id = fields.Many2one('kitap.kategorisi' , string='Kategori') # kategoriyi tutan id attribute. Başka modellerde kullanılacağı için Many2one kullanıldı.

    def mevcut_durum(self): # Fonksiyona gönderilen kaydın durumunun mevcut yapıldığı fonksiyon.
        self.ensure_one() # ensure.one() fonksiyona gönderilen kaydın mevcut olup olmadığını kontrol eder aksi taktirde hata dönndürür.
        self.state = 'mevcut' # Fonksiyona gönderilen kaydın durumunu mevcut yapar.

    def kiralık_durumu(self): # Fonksiyona gönderilen kaydın durumunun kiralık yapıldığı fonksiyon.
        self.ensure_one()
        self.state = 'kiralık'

    def kayıp_durumu(self): # Fonksiyona gönderilen kaydın durumunun kayıp yapıldığı fonksiyon.
        self.ensure_one()
        self.state = 'kayıp'

    def kitap_kirala(self): # Fonksiyona gönderilen kaydın kiralanmasını sağlayan fonksiyon.
        self.ensure_one()
        if self.state != 'mevcut':
            raise UserError(_('Kitap Kiralanamaz'))
        kiralama_as_superuser = self.env['kitap.kiralama'].sudo() #kitap.kiralama modelinin bilgilerine ulaşmak için "self.env" kullanılır. Ayrıca sudo() fonksiyonu ile kullanıcıya yetkilendirme yaparız.
        kiralama_as_superuser.create({ # Kitap Kiralama Kaydı Oluşturur.
            'kitap_id': self.id,
            'kiralık_id': self.env.user.partner_id.id,
        })


