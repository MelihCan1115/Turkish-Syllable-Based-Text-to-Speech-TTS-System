#🎤 Turkish TTS - Syllable-Based Text-to-Speech System / Türkçe TTS - Hecelere Dayalı Metin Okuma Sistemi
# 
---
## ENGLISH / 🇬🇧
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

---


## TÜRKÇE / 🇹🇷
---
### 📖 Proje Açıklaması

**3 Boyutlu Yazıcı Projesi**, geleneksel yöntemlerden ilham alınarak özel bir 3D yazıcı tasarlayıp üretmeyi hedefler. Proje, modern tasarım teknikleri, CNC hassas kontrolü ve PLA filament gibi çevre dostu malzemeleri içerir. Donanım ve yazılım entegrasyonu ile tam işlevsel ve verimli bir 3D baskı sistemi geliştirilmiştir. 🎨🖥️

**Amacı:**  
Çevre dostu bir malzeme olan PLA’yı kullanarak yüksek hassasiyetli baskılar alabilen, kullanıcı dostu ve özelleştirilebilir bir 3 boyutlu yazıcı üretmek.

## 🏆 Başarılar

- **Belge Hakkında**  
  2022-2023 Eğitim-Öğretim yılında düzenlenen **“Teknoloji Fakültesi Proje Sergisi ve Yarışması”** kapsamında, proje dalında Elektrik-Elektronik Mühendisliği alanında İkincilik Ödülü kazanılmıştır.  

  🎉 **Ödülü Sunan**: Prof. Dr. Şakir TAŞDEMİR, Teknoloji Fakültesi Dekanı.

- **Ödül Sertifikası**  
  Resmi ödül sertifikası proje klasöründe `başarı_belgesi.pdf` altında yer almaktadır.

## 🌟 Ana Özellikler

1. 🔗 **Hassas Mühendislik**  
   - 5 step motor ile 3 eksenli CNC kontrol.  
   - STL dosyalarını katmanlara ayırarak doğru ve detaylı baskılar.

2. 🌍 **Çevre Dostu Malzemeler**  
   - Yeniden kullanılabilir termoplastik PLA filament.  
   - Doğada çözünebilir ve sürdürülebilir üretim imkanı.

3. 🛠️ **Özelleştirilebilir Tasarım**  
   - Modüler yazıcı şasisi.  
   - Kullanıcı tarafından üretilebilen PLA destek parçaları.

4. 📱 **Yazılım Entegrasyonu**  
   - Harici yazılım ile kolay kurulum ve kalibrasyon.  
   - Hızlı ve kullanıcı dostu yazıcı yönetimi.

## 💻 Kullanılan Teknolojiler

- **PLA Filament**: Çevre dostu ve yeniden kullanılabilir termoplastik malzeme.  
- **Ramps 1.4 & Arduino Mega 2560**: Gelişmiş kontrol sistemleri.  
- **CNC Hassas Kontrol**: Doğru çok eksenli hareket.  
- **3D Yazıcı Yazılımı**: STL dosya dilimleme ve G-code üretimi.

🤝 Teşekkür

Danışmanımız **Hasan Hüseyin ÇEVİK**'e rehberliği için teşekkür ederiz. Ayrıca ailelerimize destekleri için minnettarız.
