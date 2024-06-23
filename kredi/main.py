# -*- coding: utf-8 -*-

#main.py

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from widgetsGiris import Ui_Giris # Giriş ekranının arayüz sınıfı
from widgets import Ui_MainWindow # Ana ekranın arayüz sınıfı
#widgets dosyasının içindeki Ui_MainWindow class ını çağırdık.
from hakkinda import Ui_Hakkinda # Hakkında penceresinin arayüz sınıfı
import sqlite3  # SQLite veritabanı modülü


#program içindeki hakkında kısmını çalıştıracak kod
# Hakkında penceresini açan sınıf
class hakkinda(QtWidgets.QMainWindow,Ui_Hakkinda):
     def __init__(self):
         super(hakkinda, self).__init__()
         self.setupUi(self)

# Giriş ekranı sınıfı
class Login(QtWidgets.QMainWindow,Ui_Giris):
    global keyf
    global kahya
    def __init__(self):
        super(Login,self).__init__()
        self.setupUi(self)
        self.btnGiris.clicked.connect(self.giris) #Ekrandaki btnGiris isimli pushbutton'a basıldığı zaman giriş fonksiyonuna bağlanır.
     # Giriş fonksiyonu   
    def giris(self):
        
        kullanici_adi = self.lneKullaniciAdi.text() #lneKullaniciAdi lineEdit'ine basınca içine belirlenen kullanıcı adımızı yazmamızı sağlar.
        sifre = self.lneSifre.text() #lneSifre lineEdit'ine basınca içine belirlenen şifreyi yazmamızı sağlar.
        
        # Kullanıcı adı ve şifre kontrolü
        if kullanici_adi == "Hatice" and sifre =="1111": #eğer kullanici_adi Hatice ve sifre 1111 e denkse aşağıdaki kodlar çalışır.
            QtWidgets.QMessageBox.information(self,"Giriş","Giriş başarılı...") #Doğru bilgileri girdiğimiz için Giriş başarılı mesajını ekrana gelir.
            self.main_window  = MainWindow() # Ana pencere oluşturuluyor
            self.main_window.show()
            self.close()
        else:
            QtWidgets.QMessageBox().information(self,"Giriş","Kullanıcı adı veya şifre yanlış.") 
            #eğer kullanici_adi Hatice ve sifre 1111 e denk değilse Kullanıcı adı veya şifre yanlış mesajı ekrana gelir.
   # Ana pencere sınıfı 
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    global curs
    global conn
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self) 
        self.baglanti_olustur() # Veritabanı bağlantısı oluşturuluyor
        self.listele() # Kayıtlar listeleniyor
        self.btnEkle.clicked.connect(self.kayit_ekle)  # Ekle butonu bağlanıyor
        self.btnSil.clicked.connect(self.kayit_sil) # Sil butonu bağlanıyor
        self.btnGuncelle.clicked.connect(self.kayit_guncelle) # Güncelle butonu bağlanıyor
        self.tblwKayitlar.itemSelectionChanged.connect(self.doldur) # Tablo seçimi değişince doldur fonksiyonu çalışıyor
        self.btnAra.clicked.connect(self.kayit_ara) # Ara butonu bağlanıyor
        self.btnCikis.clicked.connect(self.cikis) # Çıkış butonu bağlanıyor
        self.menubar.triggered.connect(self.hakkinda_pencereyi_ac) # Hakkında menüsü bağlanıyor
        self.hakkinda_penceresi= hakkinda()
      
        
    # Hakkında penceresini açan fonksiyon
    def hakkinda_pencereyi_ac(self):
        self.hakkinda_penceresi.show()
    
    # Veri giriş kontrol fonksiyonu
    #Kullanıcının girdiği verilerin doğru formatta olup olmadığını kontrol eder.
    def veri_giris_kontrol(self, _KartSifresi, _KartNO, _Iban, _Ad, _Soyad, _TCK, _TelNo):
        if not _KartSifresi.isdigit():#isdigit() metodu, tüm karakterlerin rakam olup olmadığını kontrol eder.
            QMessageBox.warning(
                self, "UYARI", "Kart Şifresi yalnızca rakam içermelidir.") #Eğer _KartSifresi yalnızca rakamlardan oluşmuyorsa, bir uyarı mesajı gösterir ve False döner.
            return False
        if not _KartNO.replace(" ", "").isdigit():
            QMessageBox.warning(
                self, "UYARI", "Kart Numarası yalnızca rakam içermelidir.")
            return False
        if not _KartNO.replace(" ", "").isdigit(): #replace(" ", "") ifadesi, IBAN numarasındaki tüm boşlukları kaldırır.
            QMessageBox.warning(
                self, "UYARI", "IBAN yalnızca rakam içermelidir.")
            return False
        # Sporcu Adı Kontrol
        if not _Ad.replace(" ", "").isalpha():#isalpha() metodu, kalan karakterlerin yalnızca harflerden oluşup oluşmadığını kontrol eder
            QMessageBox.warning(self, "UYARI", "Ad yalnızca harf içermelidir")
            return False
        # Sporcu soyadı kontrol
        if not _Soyad.replace(" ", "").isalpha():
            QMessageBox.warning(
                self, "UYARI", "Soyad yalnızca harf içermelidir")
            return False
        if not _KartNO.replace(" ", "").isdigit():
            QMessageBox.warning(
                self, "UYARI", "TC Kimlik Numarası yalnızca rakam içermelidir.")
            return False
        if not _KartNO.replace(" ", "").isdigit():
            QMessageBox.warning(
                self, "UYARI", "Telefon Numarası yalnızca rakam içermelidir.")
            return False

        return True#Tüm kontroller yağıldığında True döner ve girdi verilerinin doğru formatta olduğunu belirtir.
        
   
    # Kayıt ekleme fonksiyonu
    def kayit_ekle(self):
        _lneKartSifresi=self.lneKartSifresi.text()
        _lneKartNO=self.lneKartNO.text()
        _lneIban=self.lneIban.text()
        _lneAd=self.lneAd.text()
        _lneSoyad=self.lneSoyad.text()
        _lneTCK=self.lneTCK.text()
        _lneTelNo=self.lneTelNo.text()
        
        if not self.veri_giris_kontrol(_lneKartSifresi, _lneKartNO, _lneIban, _lneAd, _lneSoyad, _lneTCK, _lneTelNo):
            return
        
        _dateSure=self.dateSure.date().toString('yyyy-MM')
        _cmbKartTuru = self.cmbKartTuru.currentText()
        _cmbCinsiyet = self.cmbCinsiyet.currentText()
        _spnCVC = self.spnCVC.value()
        _spnBakiye = self.spnBakiye.value()
        _spnBorcMiktari = self.spnBorcMiktari.value()
        _spnMinOdeme = self.spnMinOdeme.value()
        _spnNakitAvans = self.spnNakitAvans.value()
        _cwOdemeTarihi = self.cwOdemeTarihi.selectedDate().toString(QtCore.Qt.ISODate)
        
#VERİTABANIII------------------------------------------------------------------
#78. satır hatalı olabilir(kredi kısmı) 98 DEKİ HATA YUKARIDAKİ DATESURE yi tanımlamadığım için olabilir
        try:
            self.curs.execute("INSERT INTO kredi                                                        \
                              (KartSifresi,KartNO,Iban,Ad,Soyad,TCK,TelNo,Sure,KartTuru,Cinsiyet,CVC,Bakiye,BorcMiktari,MinOdeme,NakitAvans,OdemeTarihi)  \
                                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",  \
                                      #Bu kısım, SQL sorgusunun parametrelerini belirtir
                                      (_lneKartSifresi,_lneKartNO,_lneIban,_lneAd,_lneSoyad,_lneTCK,_lneTelNo,_dateSure,_cmbKartTuru,_cmbCinsiyet,_spnCVC,_spnBakiye,_spnBorcMiktari,_spnMinOdeme,_spnNakitAvans,_cwOdemeTarihi))
                                        # Bu kısım, SQL sorgusundaki ? işaretlerinin yerine geçecek parametrelerin listesidir.
            self.conn.commit()
            QMessageBox.information(self,"BİLGİ","Kayıt Başarıyla eklendi..")
            self.listele()
        except sqlite3.Error as e:
            QMessageBox.critical(self,"Hata","Kayıt eklenirken hata "+str(e)) 
            #kullanıcıya bir hata mesajı gösterir. Burada, hata mesajı olarak Kayıt eklenirken hata ifadesi ve hata mesajı e eklenir.
     
    # Veritabanı bağlantısı oluşturma fonksiyonu
    def baglanti_olustur(self):
        try:
            #Veritabanı oluştur
            self.conn = sqlite3.connect("veritabani.db")#sqlite3.connect(...) metodu, veritabanı dosyasına bağlantı oluşturur. Bu bağlantıyı self.conn değişkenine atarız. 
            #"veritabani.db" parametresi, veritabanı dosyasının adını belirtir. Eğer bu dosya mevcut değilse, yeni bir veritabanı dosyası oluşturulur.
            self.curs = self.conn.cursor() #self.conn.cursor() metodu, veritabanı üzerinde işlem yapmak için bir cursor oluşturur. Bu imleç ile veritabanı üzerinde sorgular çalıştırabiliriz. Bu imleci self.curs değişkenine atarız.
            #Sorgu oluştur
            #IF NOT EXISTS ifadesi, tablonun zaten var olup olmadığını kontrol eder. Eğer tablo mevcut değilse, yeni bir tablo oluşturulur.
            #PRIMARY KEY AUTOINCREMENT ifadesi, Id sütununun primary key olduğunu ve her yeni kayıt eklenirken otomatik olarak artan bir değer alacağını belirtir.
            #NOT NULL yorumuyla birlikte, bu sütunun boş bırakılamayacağını belirtir.
            #UNIQUE, bir tablodaki sütunun benzersiz değerlere sahip olması gerektiğini belirtmek için kullanılan bir kısıtlamadır.örnek:Kart numarası iki kart için aynı olamaz
            self.sorguCreTblKredi = ("CREATE TABLE IF NOT EXISTS kredi(                 \
                                    Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,      \
                                    KartSifresi TEXT NOT NULL,                          \
                                    KartNO TEXT NOT NULL UNIQUE,                        \
                                    Iban TEXT NOT NULL UNIQUE,                          \
                                    Ad TEXT NOT NULL,                                   \
                                    Soyad TEXT NOT NULL,                                \
                                    TCK TEXT NOT NULL UNIQUE,                           \
                                    TelNo TEXT NOT NULL UNIQUE,                         \
                                    Sure TEXT NOT NULL,                                 \
                                    KartTuru TEXT NOT NULL,                             \
                                    Cinsiyet TEXT NOT NULL,                             \
                                    CVC TEXT NOT NULL UNIQUE,                           \
                                    Bakiye TEXT NOT NULL,                               \
                                    BorcMiktari TEXT NOT NULL,                          \
                                    MinOdeme TEXT NOT NULL,                             \
                                    NakitAvans TEXT NOT NULL,                           \
                                    OdemeTarihi TEXT NOT NULL)")
            #Sorguyu çalıştır
            self.curs.execute(self.sorguCreTblKredi) #self.curs.execute(...) ifadesi, önceki adımda tanımlanan tablo oluşturma SQL sorgusunu çalıştırır. 
                                                        #Bu, tablonun oluşturulmasını sağlar.
            #veritabanı değişikliklerini kaydet
            self.conn.commit() #self.conn.commit() ifadesi, yapılan değişikliklerin veritabanına kalıcı olarak yazılmasını sağlar. 
                                #Bu durumda, yeni tablo oluşturulur ve bu değişiklikler kalıcı hale gelir.

        except sqlite3.Error as e:
            print("SQLite veritabanı hatası:", e) #Eğer bir hata oluşursa, bu hata mesajı e değişkenine atanır ve ekrana basılır.
                                                    #Bu sayede olası hataların tespit edilmesi ve giderilmesi sağlanır.
    
            
    # Kayıtları listeleme fonksiyonu
    def listele(self):
        try:
        # Tablo içeriğini temizle
            self.tblwKayitlar.clear()
            self.tblwKayitlar.setRowCount(0)#Satır sayısı ayarlanır.
            self.tblwKayitlar.setColumnCount(17)#Sütun sayısı ayarlanır.
            self.tblwKayitlar.setHorizontalHeaderLabels(('Sıra','Kart Şifresi','Kart numarası','İban','Ad','Soyad','TC Kimlik No','Tel Numarası','süre','Kart Türü','Cinsiyet','CVC','Bakiye','Borç Miktarı','Min Ödeme','Nakit Avans','Ödeme Tarihi'))
            #Üstteki kodda tablonun başlık sütunları belirlenir.
            self.tblwKayitlar.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        # Veritabanından tüm verileri al ve tabloya ekle
            self.curs.execute("SELECT * FROM kredi")
            for satirIndeks, satirVeri in enumerate(self.curs):
                self.tblwKayitlar.insertRow(satirIndeks) #Her satır için insertRow metodu kullanılarak tabloya yeni bir satır eklenir. 
                for sutunIndeks, sutunVeri in enumerate(satirVeri):
                    self.tblwKayitlar.setItem(satirIndeks, sutunIndeks, QtWidgets.QTableWidgetItem(str(sutunVeri))) #Her sütun için setItem metodu kullanılarak veriler tabloya yerleştirilir.

        # Kayıt sayısını güncelle
            self.curs.execute("SELECT COUNT(*) FROM kredi")
            lblKayitSayisi = self.curs.fetchone()
            self.lblKayitSayisi.setText(str(lblKayitSayisi[0]))

        #Form elemanları temizlenir. Bu, kullanıcıya yeni bir kayıt eklemeye hazır bir form sunmak için yapılır. 
        #Kullanıcı yeni bir kayıt eklemek istediğinde, mevcut değerlerin temizlenmiş olması kullanışlı olacaktır.
            self.lneKartSifresi.clear()
            self.lneKartNO.clear()
            self.lneIban.clear()
            self.lneAd.clear()
            self.lneSoyad.clear()
            self.lneTCK.clear()
            self.lneTelNo.clear()
            self.cmbKartTuru.setCurrentIndex(-1)
            self.cmbCinsiyet.setCurrentIndex(-1)
            self.spnCVC.setValue(0)
            self.spnBakiye.setValue(0)
            self.spnBorcMiktari.setValue(0)
            self.spnMinOdeme.setValue(0)
            self.spnNakitAvans.setValue(0)
            self.cwOdemeTarihi.setSelectedDate(QtCore.QDate().currentDate())
            
        except sqlite3.Error as e:
            print("SQLite hatası:", e)

            
    # Kayıt silme fonksiyonu
    def kayit_sil(self):
        cevap = QtWidgets.QMessageBox.question(self, "KAYIT SİL" ,"Kaydı silmek istiyor musunuz?" , QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        #QtWidgets.QMessageBox.question metodu ile kullanıcıya bir soru iletisi gösterilir. Kullanıcının seçenekler arasından birini seçmesi beklenir.
        if cevap == QtWidgets.QMessageBox.Yes:
            secili = self.tblwKayitlar.selectedItems()
            if secili:
                silinecek = secili[6].text() # Eğer herhangi bir satır seçilmişse, bu satırın 6. sütunundaki (TC Kimlik Numarası sütunu) veri alınır ve silinecek adlı değişkene atanır.
                try:
                    self.curs.execute("DELETE FROM kredi WHERE TCK=?",
                    (silinecek,)) #DELETE FROM kredi WHERE TCK=? sorgusu ile silme işlemi gerçekleştirilir.
                    #Bu sorguda, ? işareti yerine silinecek değişkeninin değeri kullanılır.
                    self.conn.commit() #veritabanındaki değişiklikler kaydedilir.
                    
                    self.statusbar.showMessage("Kayıt Başarıyla Silindi..", 10000)
                    self.listele() #listele fonksiyonunu çağırır.
                except sqlite3.Error as hata:
                    self.statusbar.showMessage("Hata oluştu:" + str(hata))
            else:
                self.statusbar.showMessage("Silinecek kaydı Seçin.", 10000)
        else:
            self.statusBar.showMessage("Silme işlemi İptal Edildi...", 10000)
            
            
    # Kayıt güncelleme fonksiyonu
    def kayit_guncelle(self):
        cevap = QtWidgets.QMessageBox.question(self, "GÜNCELLE","Güncellemek istiyor musunuz?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if cevap == QtWidgets.QMessageBox.Yes:
            try:
                secili = self.tblwKayitlar.selectedItems()
                if secili:
                    _Id = int(secili[0].text()) #Id sütunu için
                    _lneKartSifresi=self.lneKartSifresi.text()
                    _lneKartNO=self.lneKartNO.text()
                    _lneIban=self.lneIban.text()
                    _lneAd=self.lneAd.text()
                    _lneSoyad=self.lneSoyad.text()
                    _lneTCK=self.lneTCK.text()
                    _lneTelNo=self.lneTelNo.text()
                    _dateSure=self.dateSure.date().toString('yyyy-MM')
                    _cmbKartTuru = self.cmbKartTuru.currentText()
                    _cmbCinsiyet = self.cmbCinsiyet.currentText()
                    _spnCVC = self.spnCVC.value()
                    _spnBakiye = self.spnBakiye.value()
                    _spnBorcMiktari = self.spnBorcMiktari.value()
                    _spnMinOdeme = self.spnMinOdeme.value()
                    _spnNakitAvans = self.spnNakitAvans.value()
                    _cwOdemeTarihi = self.cwOdemeTarihi.selectedDate().toString(QtCore.Qt.ISODate)
                    
                    self.curs.execute(
    "UPDATE kredi SET KartSifresi=?, KartNO=?, Iban=?, Ad=?, Soyad=?, TCK=?, TelNo=?, Sure=?, KartTuru=?, Cinsiyet=?, CVC=?, Bakiye=?,BorcMiktari=?, MinOdeme=?, NakitAvans=?, OdemeTarihi=? WHERE Id=?" ,
    #UPDATE sorgusu ile veritabanındaki ilgili kayıt güncellenir. WHERE Id=? kısmı, güncellenmek istenen kaydı Id'sine göre belirler.

    (_lneKartSifresi, _lneKartNO, _lneIban,_lneAd, _lneSoyad, _lneTCK, _lneTelNo, _dateSure, _cmbKartTuru, _cmbCinsiyet, _spnCVC, _spnBakiye, _spnBorcMiktari,_spnMinOdeme, _spnNakitAvans, _cwOdemeTarihi, _Id))
                    self.conn.commit()
                    self.listele()  #tabloyu güncelle
                    
                    self.statusbar.showMessage("Kayıt güncellendi...", 10000)
                else:
                    self.statusbar.showMessage("Kaydı seçin.", 10000)
            except sqlite3.Error as hata:
                self.statusbar.showMessage("Hata oluştu:" + str(hata))
        else:
            self.statusbar.showMessage("Güncelleme işlemi iptal edildi", 10000)
    
            
    # Seçilen kaydı form alanlarına doldurma fonksiyonu
    def doldur(self):
        secili = self.tblwKayitlar.selectedItems() #Tabloda seçilen satırlar alınır
        if len(secili) > 0: #Eğer bir satır seçilmişse satırdaki her bir hücrenin verisi ilgili kullanıcı arayüzü alanlarına doldurulur. 
            self.lneKartSifresi.setText(secili[1].text())
            self.lneKartNO.setText(secili[2].text())
            self.lneIban.setText(secili[3].text())
            self.lneAd.setText(secili[4].text())
            self.lneSoyad.setText(secili[5].text())
            self.lneTCK.setText(secili[6].text())
            self.lneTelNo.setText(secili[7].text())

            date_str = secili[8].text()
            date = QtCore.QDate.fromString(date_str, 'yyyy-MM-dd')
            self.dateSure.setDate(date)
            
            self.cmbKartTuru.setCurrentText(secili[9].text())
            self.cmbCinsiyet.setCurrentText(secili[10].text())
            self.spnCVC.setValue(int(secili[11].text()))
            self.spnBakiye.setValue(int(secili[12].text()))
            self.spnBorcMiktari.setValue(int(secili[13].text()))
            self.spnMinOdeme.setValue(int(secili[14].text()))
            self.spnNakitAvans.setValue(int(secili[15].text()))

            date_text = secili[16].text()
            date = QtCore.QDate.fromString(date_text, QtCore.Qt.ISODate)
            self.cwOdemeTarihi.setSelectedDate(date)
        
        else:#Eğer herhangi bir satır seçilmemişse, kullanıcı arayüzündeki tüm giriş alanları temizlenir veya varsayılan değerlere ayarlanır
            self.lneKartSifresi.clear()
            self.lneKartNO.clear()
            self.lneIban.clear()
            self.lneAd.clear()
            self.lneSoyad.clear()
            self.lneTCK.clear()
            self.lneTelNo.clear()
            self.cmbKartTuru.setCurrentIndex(-1)
            self.cmbCinsiyet.setCurrentIndex(-1)
            self.spnCVC.setValue(0)
            self.spnBakiye.setValue(0)
            self.spnBorcMiktari.setValue(0)
            self.spnMinOdeme.setValue(0)
            self.spnNakitAvans.setValue(0)

            
    # Kayıt arama fonksiyonu       
    def kayit_ara(self):
        #Kullanıcı arayüzünden alınan arama kriterleri (aranan1, aranan2 ve aranan3) ilgili değişkenlere atanır. 
        #Bu kriterler sırasıyla "Ad", "Soyad" ve "Kart Türü"nü temsil eder.
        aranan1 = self.lneAd.text()
        aranan2 = self.lneSoyad.text()
        aranan3 = self.cmbKartTuru.currentText()
            
        filtre = [] #Bir filtre listesi oluşturulur ve bu liste, kullanıcı tarafından girilen kriterlere göre doldurulur.
        if aranan1:
            filtre.append("Ad = ?")
        if aranan2:
            filtre.append("Soyad = ?")
        if aranan3:
            filtre.append("KartTuru = ?")
            
        filtre_sorgusu = " OR ".join(filtre) 
        #filtre adlı bir liste içinde bulunan filtrelerin (aranan1, aranan2, aranan3) SQL sorgusu için birleştirilmesini sağlar.
            
        if filtre_sorgusu:
            sorgu = "SELECT * FROM kredi WHERE " + filtre_sorgusu #SQL sorgusunu oluşturur. 
            parametreler = tuple(filter(lambda x: x, [aranan1, aranan2, aranan3])) # Bu satır, kullanıcının belirlediği arama kriterlerini bir tuple içinde toplar.
                
            self.curs.execute(sorgu, parametreler)
            sonuclar = self.curs.fetchall() #fetchall() fonksiyonu kullanılarak tüm sonuçlar sonuclar değişkenine atanır.
                
            self.tblwKayitlar.clearContents() # tablodaki mevcut içeriği temizler.
            self.tblwKayitlar.setRowCount(0) #tablonun satır sayısını sıfırlar.
                
            for satirIndeks, satirVeri in enumerate(sonuclar): #veritabanından alınan sonuçları tabloya ekler.
                self.tblwKayitlar.insertRow(satirIndeks) #Her satırın indeksi alınır.
                for sutunIndeks, sutunVeri in enumerate(satirVeri):#Satır verileri alınır
                    self.tblwKayitlar.setItem(satirIndeks, sutunIndeks,
                    QTableWidgetItem(str(sutunVeri)))
                        
        else:
            QMessageBox.warning(None, "Uyarı", "Arama için en az bir kriter doldur.")
            
            
    # Çıkış fonksiyonu
    def cikis(self):
        cevap = QtWidgets.QMessageBox.question(
            self, "ÇIKIŞ", "Programdan çıkmak istediğinize emin misiniz?", 
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if cevap == QtWidgets.QMessageBox.Yes:
            self.close()
    
    def closeEvent(self, event):
        self.conn.close()
        event.accept()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    lw = Login()
    lw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())