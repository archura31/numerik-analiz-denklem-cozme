import sys
from PyQt6.QtWidgets import QMainWindow, QApplication
from denklem_ui import Ui_MainWindow
from denklem import (
    Fonksiyonlar, 
    AralikYarilamaYontemi, 
    NewtonRaphsonYontemi, 
    SekantYontemi
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

    def denklem_coz(self):
        # Seçilen denklemi ve metodu al
        denklem_index = self.denklemBox.currentIndex()
        metod_index = self.metodBox.currentIndex()

        # Liste widget'ını temizle
        self.listWidget.clear()

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

if __name__ == "__main__":
    import math
    app = QApplication(sys.argv)
    pencere = DenklemCozucuUygulama()
    pencere.show()
    sys.exit(app.exec())
