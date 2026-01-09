🎤#Turkish TTS - Syllable-Based Text-to-Speech System / Türkçe TTS - Hecelere Dayalı Metin Okuma Sistemi
---
**Authors / Geliştiriciler**

👤 Fatih Can GÖÇÜLÜ
👤 Melih Can KÖK

### ENGLISH / 🇬🇧
---
### 📖 Project Description

The **Turkish Text-to-Speech (TTS) System** is a rule-based, syllable-level speech synthesis application developed in Python.
The system converts Turkish text into speech by analyzing linguistic structures, segmenting words into syllables, and concatenating pre-recorded WAV audio files using signal processing techniques.

The project is designed as an **educational and research-oriented TTS engine**, avoiding external APIs and deep learning models, and instead focusing on transparency, modularity, and linguistic rule compliance.🖥️

**Purpose:**  
To demonstrate the fundamental principles of text-to-speech synthesis for the Turkish language using a lightweight, fully offline, and explainable architecture.

## 🌟 Key Features

1. 🔤**Turkish-Specific Syllabification**  
   - Rule-based syllable segmentation compliant with Turkish phonetics.
   - Special handling of Turkish character casing (İ / I).

2. 🎧**Concatenative Speech Synthesis**  
   - Pre-recorded WAV syllable database.
   - Missing syllables handled gracefully with silence insertion.

3. 🎚️**Audio Signal Processing**  
   - Pitch shifting using resampling techniques.
   - Crossfade-based smoothing between syllables.
   - Output normalization to prevent clipping.
4. 🖥️ **Graphical User Interface (GUI)**
   - Built with Tkinter.
   - Real-time logging and example sentence support.
   - Adjustable pitch and output file control.

## 💻 Technologies Used

- **Python 3.x**: Core development language
- **NumPy**: Audio signal processing  
- **wave**: WAV file read/write operations 
- **Tkinter**: Graphical User Interface
- **Threading**: Non-blocking audio synthesis

### TÜRKÇE / 🇹🇷
---
### 📖 Proje Açıklaması

**Türkçe Metin Seslendirme (TTS) Sistemi**, Python ile geliştirilmiş, hece tabanlı ve kural temelli bir konuşma sentezleme uygulamasıdır.
Sistem, Türkçe metni analiz ederek kelimeleri hecelerine ayırır ve önceden kaydedilmiş WAV ses dosyalarını sinyal işleme yöntemleriyle birleştirerek konuşma üretir.Proje, harici API veya derin öğrenme modelleri kullanmadan, **eğitsel ve araştırma odaklı bir TTS motoru** geliştirmeyi hedefler.🖥️

**Amacı:**  
Türkçe için metinden konuşma üretiminin temel prensiplerini, düşük sistem gereksinimleri ve şeffaf bir mimari ile ortaya koymak.

## 🌟 Ana Özellikler

1. 🔤 **Türkçeye Özgü Heceleme**  
   - Türkçe fonetik kurallarına uygun heceleme algoritması.
   - Türkçe büyük/küçük harf dönüşümlerine özel işlem.

2. 🎧 **Eklemeli Konuşma Sentezi**  
   - WAV formatında hece veritabanı.  
   - Eksik heceler için otomatik sessizlik atama.

3. 🎚️ **Ses Sinyali İşleme**  
   - Yeniden örnekleme tabanlı perde (pitch) ayarı.
   - Hece geçişlerinde crossfade ile yumuşatma.
   - Genlik normalizasyonu.

4. 🖥️ **Grafiksel Kullanıcı Arayüzü**  
   - Tkinter tabanlı masaüstü arayüz.
   - Anlık log takibi ve örnek cümle desteği.
   - Pitch ve çıktı dosyası kontrolü.

## 💻 Kullanılan Teknolojiler

- **NumPy**: Sayısal ses işleme
- **wave**: WAV dosya okuma/yazma
- **Python 3.x**: Ana programlama dili
- **Threading**: Asenkron işlem yönetimi
- **Tkinter**: Grafiksel kullanıcı arayüzü
