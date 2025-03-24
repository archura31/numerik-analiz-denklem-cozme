import math

# Matematiksel fonksiyonları içeren sınıf
class Fonksiyonlar:
    # Kullanılan fonksiyon: f(x) = x^2 - 4
    @staticmethod
    def Fonksiyon1(x):
        return x * x - 4

    # f(x) fonksiyonunun türevi: f'(x) = 2x
    @staticmethod
    def Turev1(x):
        return 2 * x


# Aralık Yarılama (Bisection) Yöntemi
class AralikYarilamaYontemi:
    @staticmethod
    def AralikYarilama(Xa, Xb, tol=0.00001, donme=100):
        # Başlangıç aralığında kök olup olmadığını kontrol et
        if Fonksiyonlar.Fonksiyon1(Xa) * Fonksiyonlar.Fonksiyon1(Xb) > 0:
            raise Exception("Başlangıç aralığında kök yok!")

        Xy = Xa
        for i in range(donme):
            Xy = (Xa + Xb) / 2
            # Tolerans değerine ulaşıldığında veya kök bulunduğunda döngüyü bitir
            if Fonksiyonlar.Fonksiyon1(Xy) == 0 or (Xb - Xa) / 2 < tol:
                return Xy

            # Yeni aralığı belirle
            if Fonksiyonlar.Fonksiyon1(Xy) * Fonksiyonlar.Fonksiyon1(Xa) > 0:
                Xa = Xy
            else:
                Xb = Xy

            print(f"Iterasyon {i + 1}: Xy = {Xy}, f(Xy) = {Fonksiyonlar.Fonksiyon1(Xy)}")

        return Xy


# Newton-Raphson Yöntemi
class NewtonRaphsonYontemi:
    @staticmethod
    def NewtonRaphson(x0, tol=1e-6, donme=100):
        x = x0
        for i in range(donme):
            fx = Fonksiyonlar.Fonksiyon1(x)
            dfx = Fonksiyonlar.Turev1(x)

            # Türev sıfıra çok yakınsa hata fırlat
            if abs(dfx) < tol:
                raise Exception("Türev çok küçük, yöntem başarısız olabilir.")

            # Yeni x değerini hesapla
            x1 = x - fx / dfx
            print(f"Iterasyon {i + 1}: x = {x1}, f(x) = {Fonksiyonlar.Fonksiyon1(x1)}")

            # Hata toleransına ulaşıldıysa sonucu döndür
            if abs(x1 - x) < tol:
                return x1

            x = x1
        return x


# Sekant Yöntemi
class SekantYontemi:
    @staticmethod
    def Sekant(x0, x1, tol=1e-6, donme=100):
        x2 = x1
        for i in range(donme):
            fx0 = Fonksiyonlar.Fonksiyon1(x0)
            fx1 = Fonksiyonlar.Fonksiyon1(x1)

            # Bölme hatasını önlemek için kontrol
            if abs(fx1 - fx0) < tol:
                raise Exception("Bölme hatası: f(x1) - f(x0) çok küçük")

            # Yeni x değerini hesapla
            x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
            print(f"Iterasyon {i + 1}: x = {x2}, f(x) = {Fonksiyonlar.Fonksiyon1(x2)}")

            # Hata toleransına ulaşıldıysa sonucu döndür
            if abs(x2 - x1) < tol:
                return x2

            x0 = x1
            x1 = x2
        return x2


# Ana program
if __name__ == "__main__":
    try:
        print("Aralık Yarılama:", AralikYarilamaYontemi.AralikYarilama(0, 3))
        print("Newton Raphson:", NewtonRaphsonYontemi.NewtonRaphson(3))
        print("Sekant Yöntemi:", SekantYontemi.Sekant(0, 3))
        print("Aralık Yarılama:", AralikYarilamaYontemi.AralikYarilama(1, 2))
        print("Newton Raphson:", NewtonRaphsonYontemi.NewtonRaphson(1.5))
        print("Sekant Yöntemi:", SekantYontemi.Sekant(1, 2))
    except Exception as e:
        print("Hata:", str(e))
