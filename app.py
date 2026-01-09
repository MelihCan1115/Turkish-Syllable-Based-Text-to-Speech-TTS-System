import numpy as np
import wave
import os
import sys
import locale
import threading
import traceback
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from typing import List, Dict

def turkish_lower(text: str) -> str:
    """türkçe karakterleri küçük harfe çevirir"""
    turkish_map = {
        'I': 'ı',
        'İ': 'i',
    }
    result = text.lower()
    for upper, lower in turkish_map.items():
        result = result.replace(upper, lower)
    return result


class TurkishSyllabifier:
    
    VOWELS = set('aeıioöuüAEIİOÖUÜ')
    
    @staticmethod
    def syllabify(word: str) -> List[str]:
        word = turkish_lower(word)
        syllables: List[str] = []

        # find vowel indices
        vowel_idxs = [i for i, ch in enumerate(word) if ch in TurkishSyllabifier.VOWELS]
        if not vowel_idxs:
            return [word] if word else []

        start = 0
        for vi, vpos in enumerate(vowel_idxs):
            # if this is the last vowel, take the rest of the word
            if vi == len(vowel_idxs) - 1:
                syllables.append(word[start:])
                break

            next_vpos = vowel_idxs[vi + 1]
            consonant_cluster = word[vpos + 1: next_vpos]
            c_len = len(consonant_cluster)

            if c_len == 0:
                # vowel directly followed by next vowel
                end = vpos + 1
            elif c_len == 1:
                # single consonant between vowels -> consonant goes to next syllable
                end = vpos + 1
            else:
                # two or more consonants -> split after the first consonant
                end = vpos + 2

            syllables.append(word[start:end])
            start = end

        # catch any trailing characters
        if start < len(word):
            # If not already added by the loop
            if not syllables or syllables[-1] != word[start:]:
                syllables.append(word[start:])

        return syllables


class AudioProcessor:    
    @staticmethod
    def change_pitch(audio: np.ndarray, semitones: float) -> np.ndarray:
        if semitones == 0:
            return audio
        
        factor = 2 ** (semitones / 12.0)
        new_length = int(len(audio) / factor)
        indices = np.linspace(0, len(audio) - 1, new_length)
        return np.interp(indices, np.arange(len(audio)), audio)
    
    @staticmethod
    def crossfade(audio1: np.ndarray, audio2: np.ndarray, 
                  overlap_samples: int) -> np.ndarray:
        """İki sesi yumuşak birleştir"""
        if len(audio1) < overlap_samples or len(audio2) < overlap_samples:
            overlap_samples = min(len(audio1) // 4, len(audio2) // 4, overlap_samples)
        
        if overlap_samples < 10:
            return np.concatenate([audio1, audio2])
        
        fade_out = np.linspace(1, 0, overlap_samples)
        fade_in = np.linspace(0, 1, overlap_samples)
        
        audio1_copy = audio1.copy()
        audio2_copy = audio2.copy()
        
        audio1_copy[-overlap_samples:] *= fade_out
        audio2_copy[:overlap_samples] *= fade_in
        
        result = np.concatenate([
            audio1_copy[:-overlap_samples],
            audio1_copy[-overlap_samples:] + audio2_copy[:overlap_samples],
            audio2_copy[overlap_samples:]
        ])
        
        return result
    
    @staticmethod
    def normalize(audio: np.ndarray, target: float = 0.85) -> np.ndarray:
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            return audio / max_val * target
        return audio


class SyllableDatabase:
    
    def __init__(self, db_path: str = "ses dosyaları"):
        self.db_path = db_path
        self.sample_rate = 22050
        self.cache = {}
        
        #klasör kontrolü
        if not os.path.exists(db_path):
            raise RuntimeError(f"'{db_path}' klasörü bulunamadı!")
        
        #veritabanını yükle
        self._load_database()
    
    def _load_database(self):
        wav_files = [f for f in os.listdir(self.db_path) if f.endswith('.wav')]
        
        if len(wav_files) == 0:
            raise RuntimeError(f"'{self.db_path}' klasöründe WAV dosyası yok!")
        
        for wav_file in sorted(wav_files):
            syllable = wav_file.replace('.wav', '')
            filepath = os.path.join(self.db_path, wav_file)
            
            try:
                with wave.open(filepath, 'r') as wav:
                    frames = wav.readframes(wav.getnframes())
                    audio = np.frombuffer(frames, dtype=np.int16)
                    audio = audio.astype(np.float32) / 32767.0
                    self.cache[syllable] = audio
            
            except Exception as e:
                pass
    
    def get_syllable(self, syllable: str) -> np.ndarray:
        return self.cache.get(syllable, None)
    
    def has_syllable(self, syllable: str) -> bool:
        return syllable in self.cache
    
    def get_all_syllables(self) -> List[str]:
        return sorted(self.cache.keys())


class TurkishTTS:    
    def __init__(self, db_path: str = "ses dosyaları", pitch_shift: float = 0):
        self.syllabifier = TurkishSyllabifier()
        self.database = SyllableDatabase(db_path)
        self.processor = AudioProcessor()
        self.sample_rate = 22050
        
        # Ayarlar
        self.pitch_shift = pitch_shift
        self.crossfade_ms = 25
        self.word_pause = 0.08
        self.comma_pause = 0.15
        self.period_pause = 0.35
    
    def check_text_coverage(self, text: str) -> Dict:
        """metindeki hecelerin kaçı veritabanında var?"""
        words = text.replace(',', '').replace('.', '').replace('!', '').replace('?', '').split()
        
        all_syllables = []
        missing = []
        
        for word in words:
            clean = ''.join(c for c in word if c.isalpha())
            if clean:
                syls = self.syllabifier.syllabify(clean)
                all_syllables.extend(syls)
                
                for syl in syls:
                    if not self.database.has_syllable(syl):
                        if syl not in missing:
                            missing.append(syl)
        
        return {
            'total': len(all_syllables),
            'missing': missing,
            'coverage': (len(all_syllables) - len(missing)) / len(all_syllables) * 100 if all_syllables else 0
        }
    
    def synthesize_text(self, text: str, verbose: bool = True) -> np.ndarray:
        """metin -> ses"""
        if verbose:
            print(f"\n{'='*60}")
            print(f"🎵 METİN SESLENDİRME")
            print(f"{'='*60}")
            print(f"Metin: {text}\n")
        
        coverage = self.check_text_coverage(text)
        
        if coverage['missing']:
            print(f"⚠️  UYARI: {len(coverage['missing'])} hece bulunamadı!")
            print(f"   Eksik heceler: {', '.join(coverage['missing'])}")
            print(f"   Bu heceler için sessizlik eklenecek\n")
        else:
            print(f"✅ Tüm heceler veritabanında mevcut!\n")
        
        print(f"Kapsam: %{coverage['coverage']:.1f}\n")
        
        audio_segments = []
        
        words = text.replace(',', ' ,').replace('.', ' .').replace('!', ' !').replace('?', ' ?').split()
        
        if verbose:
            print("Heceleme:")
        
        for word in words:
            #noktalama
            if word in [',', '.', '!', '?', ';', ':']:
                pause_map = {'.': self.period_pause, '!': self.period_pause, 
                            '?': self.period_pause, ',': self.comma_pause,
                            ';': self.comma_pause, ':': self.comma_pause}
                pause_dur = pause_map.get(word, 0.1)
                audio_segments.append(np.zeros(int(self.sample_rate * pause_dur)))
                continue
            
            clean_word = ''.join(c for c in word if c.isalpha())
            if not clean_word:
                continue
            
            syllables = self.syllabifier.syllabify(clean_word)
            
            if verbose:
                #eksik heceleri işaretle
                syl_display = []
                for syl in syllables:
                    if self.database.has_syllable(syl):
                        syl_display.append(syl)
                    else:
                        syl_display.append(f"[{syl}]")
                
                print(f"  {clean_word:15} → {'-'.join(syl_display)}")
            
            for syllable in syllables:
                syl_audio = self.database.get_syllable(syllable)
                
                if syl_audio is None:
                    #eksik hecede sessizlik ekleme
                    syl_audio = np.zeros(int(self.sample_rate * 0.15))
                else:
                    #pitch ayarla
                    if self.pitch_shift != 0:
                        syl_audio = self.processor.change_pitch(syl_audio, self.pitch_shift)
                    
                    syl_audio = self.processor.normalize(syl_audio, 0.8)
                
                audio_segments.append(syl_audio)
            
            #kelime arası duraklama
            audio_segments.append(np.zeros(int(self.sample_rate * self.word_pause)))
        
        #merge
        if verbose:
            print(f"\n🔗 Segmentler birleştiriliyor...")
        
        overlap_samples = int(self.sample_rate * self.crossfade_ms / 1000)
        
        final_audio = audio_segments[0]
        for segment in audio_segments[1:]:
            final_audio = self.processor.crossfade(final_audio, segment, overlap_samples)
        
        final_audio = self.processor.normalize(final_audio, 0.85)
        
        if verbose:
            print(f"✅ Sentez tamamlandı!")
            print(f"   Süre: {len(final_audio)/self.sample_rate:.2f} saniye")
        
        return final_audio
    
    def save_wav(self, audio: np.ndarray, filename: str):
        """WAV dosyası kaydet"""
        audio_int = np.int16(audio * 32767)
        
        with wave.open(filename, 'w') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            wav.writeframes(audio_int.tobytes())
        
        print(f"\n{'='*60}")
        print(f"💾 Ses dosyası kaydedildi: {filename}")
        print(f"{'='*60}")
        print(f"Süre: {len(audio)/self.sample_rate:.2f} saniye")
        print(f"Format: 16-bit Mono WAV, {self.sample_rate} Hz")


### ARAYÜZ

class TTSApp:
    def __init__(self, root):
        self.root = root
        root.title("Metin Seslendirme Uygulaması")

        main = ttk.Frame(root, padding=10)
        main.grid(row=0, column=0, sticky="nsew")

        #metin girişi
        ttk.Label(main, text="Seslendirilecek Metin:").grid(row=0, column=0, sticky="w")
        self.text_input = tk.Text(main, width=60, height=6)
        self.text_input.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        
        self.text_input.insert('1.0', 'Baba evde kırmızı ve mavi kitapları okuyor.')
        
        #örnek cümleler
        ttk.Label(main, text="Örnek Cümleler:").grid(row=2, column=0, sticky="w")
        self.examples_var = tk.StringVar()
        self.examples_combo = ttk.Combobox(main, textvariable=self.examples_var, state='readonly', width=58)
        self.examples_combo['values'] = (
            'Baba evde kırmızı ve mavi kitapları okuyor.',
            'Küçük köpek bahçede koşuyor ve top oynuyor.',
            'Ayşe ve Mehmet pazar günü sinemaya gittiler.',
            'Öğretmen sınıfta yeni konuları anlatıyor.',
            'Güneş sabah erken doğar ve ışığıyla ısıtır.',
            'Zeytin ağaçları bahçede yavaşça büyüyor.',
            'Yağmur pencerelere hafifçe vuruyor ve sesi güzel.',
            'Jale ve Yusuf tatilde yeni yerler keşfettiler.'
        )
        self.examples_combo.grid(row=2, column=1, columnspan=2, sticky="w", pady=(0, 5))
        self.examples_combo.bind('<<ComboboxSelected>>', self.on_example_selected)

        #pitch
        ttk.Label(main, text="Pitch (semitone, çok kalın gelirse artırın):").grid(row=4, column=0, sticky="w")
        self.pitch_var = tk.DoubleVar(value=11.0)
        self.pitch_spin = ttk.Spinbox(main, from_=-12, to=12, increment=0.5, textvariable=self.pitch_var, width=6)
        self.pitch_spin.grid(row=4, column=1, sticky="w")

        #output dosyası cikti.wav
        ttk.Label(main, text="Çıktı dosyası:").grid(row=5, column=0, sticky="w")
        self.output_var = tk.StringVar(value="cikti.wav")
        self.output_entry = ttk.Entry(main, textvariable=self.output_var, width=30)
        self.output_entry.grid(row=5, column=1, sticky="w")

        #butonlar
        self.synthesize_btn = ttk.Button(main, text="Sentezle ve Kaydet", command=self.on_synthesize)
        self.synthesize_btn.grid(row=6, column=0, pady=(10, 0), sticky="w")

        self.list_btn = ttk.Button(main, text="Heceleri Listele", command=self.on_list)
        self.list_btn.grid(row=6, column=1, pady=(10, 0), sticky="w")

        self.clear_log_btn = ttk.Button(main, text="Log Temizle", command=self.clear_log)
        self.clear_log_btn.grid(row=6, column=2, pady=(10, 0), sticky="e")

        #log
        ttk.Label(main, text="Log:").grid(row=7, column=0, sticky="w", pady=(10, 0))
        self.log = ScrolledText(main, width=80, height=12, state='disabled')
        self.log.grid(row=8, column=0, columnspan=3, pady=(0, 10))

        #durum çubuğu
        self.status_var = tk.StringVar(value="Hazır")
        self.status = ttk.Label(main, textvariable=self.status_var, relief='sunken', anchor='w')
        self.status.grid(row=9, column=0, columnspan=3, sticky="ew")

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

    def append_log(self, text):
        self.log.configure(state='normal')
        self.log.insert('end', text + '\n')
        self.log.see('end')
        self.log.configure(state='disabled')

    def on_example_selected(self, event):
        """Örnek cümle seçildiğinde metin alanını doldur"""
        selected = self.examples_var.get()
        if selected:
            self.text_input.delete('1.0', 'end')
            self.text_input.insert('1.0', selected)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)
            self.append_log(f'✓ Cümle panoya kopyalandı: {selected}')

    def clear_log(self):
        self.log.configure(state='normal')
        self.log.delete('1.0', 'end')
        self.log.configure(state='disabled')

    def set_busy(self, busy: bool):
        state = 'disabled' if busy else 'normal'
        self.synthesize_btn.configure(state=state)
        self.list_btn.configure(state=state)
        self.clear_log_btn.configure(state=state)
        self.status_var.set('Çalışıyor...' if busy else 'Hazır')

    def on_list(self):
        self.append_log('Heceler listeleniyor...')
        def task():
            try:
                tts = TurkishTTS(pitch_shift=0)
                syllables = tts.database.get_all_syllables()
                self.append_log(f"Toplam hece: {len(syllables)}")
                
                popup = tk.Toplevel(self.root)
                popup.title('Veritabanındaki Heceler')
                txt = ScrolledText(popup, width=60, height=20)
                txt.pack(fill='both', expand=True)
                txt.insert('end', '\n'.join(syllables))
                txt.configure(state='disabled')

            except Exception as e:
                self.append_log('Hata: ' + str(e))
        threading.Thread(target=task, daemon=True).start()

    def on_synthesize(self):
        text = self.text_input.get('1.0', 'end').strip()
        if not text:
            messagebox.showwarning('Uyarı', 'Lütfen seslendirilecek bir metin girin.')
            return

        output = self.output_var.get().strip() or 'cikti.wav'
        pitch = float(self.pitch_var.get())

        self.set_busy(True)
        self.append_log(f'Sentezleme başlatıldı. Output: {output} Pitch: {pitch}')

        def task():
            try:
                tts = TurkishTTS(pitch_shift=pitch)
                self.append_log('Veritabanı yüklendi, sentezleme yapılıyor...')
                audio = tts.synthesize_text(text, verbose=False)
                tts.save_wav(audio, output)
                self.append_log(f'Başarılı: {output} kaydedildi.')
                messagebox.showinfo('Tamamlandı', f'Çıktı kaydedildi: {output}')

            except Exception as e:
                tb = traceback.format_exc()
                self.append_log('Hata oluştu:\n' + tb)
                messagebox.showerror('Hata', str(e))
            finally:
                self.set_busy(False)

        threading.Thread(target=task, daemon=True).start()


def main():
    root = tk.Tk()
    app = TTSApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
