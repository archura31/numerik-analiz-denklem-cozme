import sys
import numpy as np
from PyQt6.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox
from denklem_ui import Ui_MainWindow
from denklem import (
    Fonksiyonlar, 
    AralikYarilamaYontemi, 
    NewtonRaphsonYontemi, 
    SekantYontemi,
    GaussYokEtmeYontemi
)

class Fonksiyonlar_Genisletilmis:
    @staticmethod
    def Fonksiyon2(x):
        return math.sin(x) - x/2

    @staticmethod
    def Turev2(x):
        return math.cos(x) - 0.5

    @staticmethod
    def Fonksiyon3(x):
        return math.exp(-x) - x

    @staticmethod
    def Turev3(x):
        return -math.exp(-x) - 1

class DenklemCozucuUygulama(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Buton event'ini bağla
        self.sonucButton.clicked.connect(self.denklem_coz)
        
        # Varsayılan denklem sistemleri
        self.varsayilan_denklem_sistemi_4x4 = [
            [2, 1, -1, 2],
            [-3, -1, 2, -11],
            [-2, 1, 2, -3],
            [1, 2, 3, 4]
        ]
        self.varsayilan_sonuclar_4x4 = [8, -15, -3, 10]
        
        # Kullanıcının metod seçimine göre UI güncellemeleri
        self.denklemBox.currentIndexChanged.connect(self.ui_guncelle)
        
    def ui_guncelle(self):
        # Eğer lineer denklem sistemi seçildiyse, sadece Gauss yöntemini göster
        if self.denklemBox.currentIndex() == 3:  # Lineer Denklem Sistemi
            self.metodBox.setCurrentIndex(3)  # Gauss Eliminasyon
            
    def denklem_coz(self):
        # Seçilen denklemi ve metodu al
        denklem_index = self.denklemBox.currentIndex()
        metod_index = self.metodBox.currentIndex()

        # Liste widget'ını temizle
        self.listWidget.clear()
        
        # Lineer denklem sistemi ve Gauss seçildi
        if denklem_index == 3 and metod_index == 3:  # Lineer Denklem Sistemi ve Gauss Eliminasyon
            self.gauss_cozum()
            return
            
        # Eğer Gauss seçilmişse ama denklem sistemi seçilmemişse uyarı ver
        if metod_index == 3 and denklem_index != 3:
            QMessageBox.warning(self, "Uyarı", "Gauss Eliminasyon yöntemi sadece lineer denklem sistemleri için kullanılabilir!")
            return

        try:
            sonuc = None
            
            # Denklem ve metoda göre çözüm
            if denklem_index == 0:  # x^2 - 4
                if metod_index == 0:  # Newton-Raphson
                    self.newton_raphson_cozum(
                        Fonksiyonlar.Fonksiyon1, 
                        Fonksiyonlar.Turev1, 
                        3
                    )
                elif metod_index == 1:  # Bisection
                    self.bisection_cozum(
                        Fonksiyonlar.Fonksiyon1, 
                        0, 3
                    )
                else:  # Sekant
                    self.sekant_cozum(
                        Fonksiyonlar.Fonksiyon1, 
                        0, 3
                    )

            elif denklem_index == 1:  # sin(x) - x/2
                if metod_index == 0:  # Newton-Raphson
                    self.newton_raphson_cozum(
                        Fonksiyonlar_Genisletilmis.Fonksiyon2, 
                        Fonksiyonlar_Genisletilmis.Turev2, 
                        1
                    )
                elif metod_index == 1:  # Bisection
                    self.bisection_cozum(
                        Fonksiyonlar_Genisletilmis.Fonksiyon2, 
                        0, 2
                    )
                else:  # Sekant
                    self.sekant_cozum(
                        Fonksiyonlar_Genisletilmis.Fonksiyon2, 
                        0, 2
                    )

            elif denklem_index == 2:  # e^(-x) - x
                if metod_index == 0:  # Newton-Raphson
                    self.newton_raphson_cozum(
                        Fonksiyonlar_Genisletilmis.Fonksiyon3, 
                        Fonksiyonlar_Genisletilmis.Turev3, 
                        0
                    )
                elif metod_index == 1:  # Bisection
                    self.bisection_cozum(
                        Fonksiyonlar_Genisletilmis.Fonksiyon3, 
                        0, 1
                    )
                else:  # Sekant
                    self.sekant_cozum(
                        Fonksiyonlar_Genisletilmis.Fonksiyon3, 
                        0, 1
                    )

        except Exception as e:
            self.listWidget.addItem(f"Hata: {str(e)}")

    def newton_raphson_cozum(self, fonksiyon, turev, x0):
        sonuc = None
        try:
            # Global değişkenleri geçici olarak değiştirmek için bir fonksiyon
            def custom_newton_raphson(x0, tol=1e-6, donme=100):
                x = x0
                for i in range(donme):
                    fx = fonksiyon(x)
                    dfx = turev(x)

                    if abs(dfx) < tol:
                        raise Exception("Türev çok küçük, yöntem başarısız olabilir.")

                    x1 = x - fx / dfx
                    iterasyon_mesaji = f"Iterasyon {i + 1}: x = {x1}, f(x) = {fonksiyon(x1)}"
                    self.listWidget.addItem(iterasyon_mesaji)

                    if abs(x1 - x) < tol:
                        return x1

                    x = x1
                return x

            sonuc = custom_newton_raphson(x0)
            self.sonucLabel.setText(f"Sonuc: {sonuc}")

        except Exception as e:
            self.listWidget.addItem(f"Hata: {str(e)}")

    def bisection_cozum(self, fonksiyon, xa, xb):
        sonuc = None
        try:
            # Global değişkenleri geçici olarak değiştirmek için bir fonksiyon
            def custom_bisection(Xa, Xb, tol=0.00001, donme=100):
                if fonksiyon(Xa) * fonksiyon(Xb) > 0:
                    raise Exception("Başlangıç aralığında kök yok!")

                Xy = Xa
                for i in range(donme):
                    Xy = (Xa + Xb) / 2
                    iterasyon_mesaji = f"Iterasyon {i + 1}: Xy = {Xy}, f(Xy) = {fonksiyon(Xy)}"
                    self.listWidget.addItem(iterasyon_mesaji)

                    if fonksiyon(Xy) == 0 or (Xb - Xa) / 2 < tol:
                        return Xy

                    if fonksiyon(Xy) * fonksiyon(Xa) > 0:
                        Xa = Xy
                    else:
                        Xb = Xy

                return Xy

            sonuc = custom_bisection(xa, xb)
            self.sonucLabel.setText(f"Sonuc: {sonuc}")

        except Exception as e:
            self.listWidget.addItem(f"Hata: {str(e)}")

    def sekant_cozum(self, fonksiyon, x0, x1):
        sonuc = None
        try:
            # Global değişkenleri geçici olarak değiştirmek için bir fonksiyon
            def custom_sekant(x0, x1, tol=1e-6, donme=100):
                x2 = x1
                for i in range(donme):
                    fx0 = fonksiyon(x0)
                    fx1 = fonksiyon(x1)

                    if abs(fx1 - fx0) < tol:
                        raise Exception("Bölme hatası: f(x1) - f(x0) çok küçük")

                    x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
                    iterasyon_mesaji = f"Iterasyon {i + 1}: x = {x2}, f(x) = {fonksiyon(x2)}"
                    self.listWidget.addItem(iterasyon_mesaji)

                    if abs(x2 - x1) < tol:
                        return x2

                    x0 = x1
                    x1 = x2
                return x2

            sonuc = custom_sekant(x0, x1)
            self.sonucLabel.setText(f"Sonuc: {sonuc}")

        except Exception as e:
            self.listWidget.addItem(f"Hata: {str(e)}")
            
    def gauss_cozum(self):
        """Gauss Eliminasyon yöntemi ile lineer denklem sistemini çöz"""
        try:
            # Varsayılan değerler
            katsayilar = self.varsayilan_denklem_sistemi_4x4
            sonuclar = self.varsayilan_sonuclar_4x4
            
            # Kullanıcıya seçenek sun
            boyut, ok = QInputDialog.getItem(
                self, 
                "Denklem Sistemi Boyutu",
                "Hangi boyutta denklem sistemi çözmek istersiniz?",
                ["4x4 (varsayılan)", "3x3 (kullanıcı girişi)", "10x10 (rastgele)"],
                0, False
            )
            
            if ok:
                if boyut == "4x4 (varsayılan)":
                    # Varsayılan 4x4 kullan
                    pass
                    
                elif boyut == "3x3 (kullanıcı girişi)":
                    # Kullanıcıdan 3x3 matris ve sonuç vektörü al
                    katsayilar = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                    sonuclar = [0, 0, 0]
                    
                    for i in range(3):
                        for j in range(3):
                            deger, ok = QInputDialog.getDouble(
                                self, 
                                f"Matris Değeri [A{i+1},{j+1}]", 
                                f"A[{i+1},{j+1}] değerini girin:", 
                                1.0, -1000.0, 1000.0, 2
                            )
                            if ok:
                                katsayilar[i][j] = deger
                            else:
                                return
                                
                    for i in range(3):
                        deger, ok = QInputDialog.getDouble(
                            self, 
                            f"Sonuç Vektörü [b{i+1}]", 
                            f"b[{i+1}] değerini girin:", 
                            1.0, -1000.0, 1000.0, 2
                        )
                        if ok:
                            sonuclar[i] = deger
                        else:
                            return
                
                elif boyut == "10x10 (rastgele)":
                    # 10x10 rastgele matris oluştur
                    import random
                    katsayilar = []
                    sonuclar = []
                    for i in range(10):
                        satir = []
                        for j in range(10):
                            satir.append(random.randint(1, 10))
                        katsayilar.append(satir)
                        sonuclar.append(random.randint(1, 20))
            
            # Matris ve sonuç vektörünü göster
            self.listWidget.addItem("Katsayı Matrisi ve Sonuç Vektörü:")
            n = len(sonuclar)
            for i in range(n):
                satir_str = "| "
                for j in range(n):
                    satir_str += f"{katsayilar[i][j]:6.2f} "
                satir_str += f"| = {sonuclar[i]:6.2f}"
                self.listWidget.addItem(satir_str)
            
            # Gauss Eliminasyon çözümü
            cozum, iterasyonlar = GaussYokEtmeYontemi.coz(katsayilar, sonuclar)
            
            # İterasyonları göster
            self.listWidget.addItem("\nİterasyon Adımları:")
            for i, matris in enumerate(iterasyonlar):
                self.listWidget.addItem(f"Adım {i+1}:")
                n = matris.shape[0]
                for j in range(n):
                    satir_str = "| "
                    for k in range(n+1):
                        if k == n:
                            satir_str += f"| {matris[j, k]:6.2f}"
                        else:
                            satir_str += f"{matris[j, k]:6.2f} "
                    self.listWidget.addItem(satir_str)

            # Sonuçları göster
            self.listWidget.addItem("\nÇözüm:")
            sonuc_str = "["
            for i in range(len(cozum)):
                sonuc_str += f"x{i+1} = {cozum[i]:.4f}"
                if i < len(cozum) - 1:
                    sonuc_str += ", "
            sonuc_str += "]"
            self.sonucLabel.setText(f"Sonuc: {sonuc_str}")
            
        except Exception as e:
            self.listWidget.addItem(f"Hata: {str(e)}")

if __name__ == "__main__":
    import math
    app = QApplication(sys.argv)
    pencere = DenklemCozucuUygulama()
    pencere.show()
    sys.exit(app.exec())
