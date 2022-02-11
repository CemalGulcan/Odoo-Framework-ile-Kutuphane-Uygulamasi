# -*- coding: utf-8 -*-
{
    'name': "Kütüphane Uygulaması",
    'summary': "Kütüphane uygulamasında kitap bilgileri tutulmakta , kitap kategorileri tutulmakta , kitap kiralanması yapılmakta ve bu bilgiler tutulmaktadır.",
    'description': """Basit Bir Kütüphane Yönetimi""",
    'author': "Cemal GÜLCAN",
    'website': "http://www.projem.com",
    'category': 'Yok',
    'version': 'İlk Sürüm',
    'depends': ['base', 'mail'],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/kitaplar.xml',
        'views/kategori.xml',
        'views/kiralama.xml',
    ],
}



