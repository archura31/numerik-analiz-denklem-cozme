# 📐 Denklem Çözücü Uygulaması

## 🚀 Proje Açıklaması
Bu proje, çeşitli matematiksel denklemleri farklı sayısal çözüm yöntemleriyle (Newton-Raphson, Bisection, Sekant) çözen bir PyQt6 masaüstü uygulamasıdır.

## 🛠️ Gereksinimler
- Python 3.8 veya üzeri
- pip paket yöneticisi

## 📦 Bağımlılıklar (Dependencies)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-6.8.1-green)

## 💻 Kurulum

### Sanal Ortam Oluşturma (Önerilen)
```bash
# Proje dizininde
python -m venv venv
```

#### Windows
```powershell
# Sanal ortamı etkinleştirme
.\venv\Scripts\activate

# Bağımlılıkları yükleme
pip install PyQt6
pip install numpy
```

#### Linux / macOS
```bash
# Sanal ortamı etkinleştirme
source venv/bin/activate

# Bağımlılıkları yükleme
pip install PyQt6
pip install numpy
```

### Doğrudan Sistem Python'una Kurulum
```bash
pip install PyQt6
pip install numpy
```

## 🚀 Çalıştırma
```bash
python denklem_main.py
```

## 📁 Proje Dosyaları
- `denklem.py`: Sayısal çözüm algoritmaları
- `denklem_ui.py`: PyQt6 kullanılarak oluşturulmuş kullanıcı arayüzü
- `denklem_main.py`: Ana uygulama dosyası

## 🛠️ Sorun Giderme
- Python ve pip güncel sürümde olduğundan emin olun
- Sanal ortam kullanın
- Gerekirse `pip install --upgrade pip` ile pip'i güncelleyin

### Hata Bildirimi
Herhangi bir sorunla karşılaşırsanız lütfen [Issues](../../issues) sayfasından bildiriniz.

## 📝 Lisans
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

**Not**: Bu proje MIT Lisansı altında yayınlanmıştır. Detaylar için `LICENSE` dosyasını inceleyiniz.
