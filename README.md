<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f1117,50:1a1b2e,100:89b4fa&height=220&section=header&text=AI-EVENT-LOG-ANALYZER&fontSize=40&fontColor=89b4fa&fontAlignY=40&desc=Windows%20loglarını%20okur%2C%20tehditleri%20bulur%2C%20sana%20rapor%20verir&descAlignY=60&descSize=17&descColor=cdd6f4&animation=fadeIn" />

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-89b4fa?style=for-the-badge&logo=python&logoColor=white&labelColor=0f1117)](https://python.org)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-f38ba8?style=for-the-badge&logo=meta&logoColor=white&labelColor=0f1117)](https://groq.com)
[![Windows](https://img.shields.io/badge/Windows-Event_Log-a6e3a1?style=for-the-badge&logo=windows&logoColor=white&labelColor=0f1117)](https://microsoft.com)
[![License](https://img.shields.io/badge/License-MIT-fab387?style=for-the-badge&labelColor=0f1117)](LICENSE)

<br/>

```
  ██████╗ ███████╗ ██████╗██╗   ██╗██████╗ ██╗████████╗██╗   ██╗
  ██╔══██╗██╔════╝██╔════╝██║   ██║██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝
  ██████╔╝███████╗██║     ██║   ██║██████╔╝██║   ██║    ╚████╔╝ 
  ██╔═══╝ ╚════██║██║     ██║   ██║██╔══██╗██║   ██║     ╚██╔╝  
  ██║     ███████║╚██████╗╚██████╔╝██║  ██║██║   ██║      ██║   
  ╚═╝     ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝  
```

</div>

---

## Ne işe yarıyor?

Bilgisayarına kim bağlanmaya çalışıyor? Hangi IP sürekli yanlış şifre giriyor? Birisi aynı anda 5 farklı kullanıcıyla mı deneme yapıyor?

Bu araç tam olarak bunları buluyor. Windows'un kendi güvenlik loglarını okuyup şüpheli IP adreslerini tespit ediyor, sonra bir yapay zekaya danışarak sana insan dilinde bir tehdit raporu çıkarıyor. Her şey otomatik — sadece çalıştır, raporu oku.

---

## ✨ Özellikler

<table>
<tr>
<td width="50%">

### 🔍 Olay Toplama
Windows Security Log'dan başarısız giriş denemelerini (`Event ID 4625`) otomatik çekip parse eder. Kaynak IP, hedef kullanıcı, logon tipi — hepsini hazırlar.

</td>
<td width="50%">

### 🧠 Anomali Tespiti
Brute Force ve Multi-Account Targeting kurallarıyla şüpheli IP'leri yakalar. Eşik değerleri istenildiğinde ayarlanabilir.

</td>
</tr>
<tr>
<td width="50%">

### 🤖 Yapay Zeka Değerlendirmesi
Groq üzerinde **LLaMA 3.3 70B** ile bulgular analiz edilir. Tehdit seviyesi belirlenir, her IP'nin ne yapmaya çalıştığı açıklanır, ne yapman gerektiği söylenir.

</td>
<td width="50%">

### 📊 HTML Rapor Üretimi
Her analizin sonunda otomatik olarak şık, zaman damgalı bir HTML raporu oluşturulur. Renk kodlu tehdit seviyesi, tablolar ve AI yorumu tek belgede.

</td>
</tr>
</table>

---

## 🚀 Nasıl çalışıyor?

```
1. Windows Security Log'u okur  →  4625 (başarısız giriş denemeleri)
            ↓
2. Kural motorunu çalıştırır
   ├─ Aynı IP'den 5+ başarısız deneme   →  🚨 BRUTE_FORCE
   └─ Aynı IP'den 3+ farklı kullanıcı  →  🚨 MULTI_ACCOUNT_TARGETING
            ↓
3. Bulgularını LLaMA 3.3'e gönderir  →  Groq API
            ↓
4. Tehdit raporu çıkarır  →  reports/threat_report_TARIH.html
```

---

## 🛠️ Kurulum

Önce [Groq'tan](https://console.groq.com) ücretsiz bir API anahtarı al. Sonra:

```bash
git clone https://github.com/Bor-Code/Monitoring-Windows-Logs-with-AI.git
cd Monitoring-Windows-Logs-with-AI

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

`.env` dosyasını düzenle:

```dotenv
GROQ_API_KEY=buraya_kendi_anahtarını_yaz
LLM_PROVIDER=groq
```

> ⚠️ `.env` dosyasını asla Git'e ekleme — `.gitignore` tarafından zaten korunuyor.

---

## 🖥️ Çalıştırma

> Terminali **yönetici olarak** aç — Security loglarına erişmek için gerekli.

```bash
python main.py
```

Konsolda hangi IP'lerin şüpheli olduğunu göreceksin. İş bitince `reports/` klasöründe HTML rapor hazır olacak.

### Örnek çıktı

```
[*] Querying 'Security' log for Event ID 4625 (Failed Logons)...
[+] Found 34 failed logon event(s).

=======================================================
          ANOMALY DETECTION REPORT
=======================================================
  Total Events Analyzed : 34
  Unique Source IPs     : 8
  Flagged IPs           : 3
=======================================================

[!] SUSPICIOUS ACTIVITY DETECTED:

  IP Address       : 192.168.1.105
  Failed Attempts  : 17
  Targeted Users   : admin, Administrator, sa
  Triggered Rules  : BRUTE_FORCE, MULTI_ACCOUNT_TARGETING
-------------------------------------------------------
[*] Sending analysis to Groq (llama-3.3-70b-versatile)...
[+] Report saved: reports/threat_report_2025-01-15_14-32-07.html
```

---

## 📊 Raporda ne var?

| Bölüm | İçerik |
|-------|--------|
| 🟢🟡🔴 Tehdit Seviyesi | CLEAN / MEDIUM / HIGH — renkli banner ile |
| 🚨 Şüpheli IP'ler | Deneme sayısı, hedef kullanıcılar, tetiklenen kurallar |
| 📋 Ham Loglar | Tüm başarısız girişlerin tam listesi |
| 🤖 AI Yorumu | Tehdidin ne anlama geldiği ve ne yapman gerektiği |

---

## 📁 Proje yapısı

```
├── src/
│   ├── collector/          → Windows loglarını okur
│   ├── analyzer/           → Kural motorunu çalıştırır
│   ├── ai/                 → Groq'a bağlanır, analiz alır
│   └── reporter/           → HTML rapor üretir
│
├── reports/                → Oluşturulan raporlar (git'e dahil değil)
├── main.py                 → Buradan başlar her şey
├── .env                    → API anahtarın (git'e dahil değil)
└── requirements.txt
```

---

## 🔍 Tespit Kuralları

| Kural | Ne anlama geliyor | Varsayılan Eşik |
|-------|-------------------|-----------------|
| `BRUTE_FORCE` | Tek IP'den çok sayıda yanlış şifre | ≥ 5 deneme |
| `MULTI_ACCOUNT_TARGETING` | Tek IP'den birden fazla kullanıcıya saldırı | ≥ 3 farklı kullanıcı |

> Eşikleri `src/analyzer/anomaly_detector.py` içinden değiştirebilirsin.

---

## 📝 Notlar

- Sadece **Windows**'ta çalışır — Security Log'a erişmek için `pywin32` kullanıyor
- API anahtarını `.env` dışına sakın yazma
- Groq **ücretsiz planı** gayet yeterli, ücretli API gerekmez
- Yeni bir LLM sağlayıcısı eklemek istersen `BaseLLMProvider` sınıfını genişletmen yeterli

---

## 🗺️ Yol haritası

- [ ] OpenAI ve Ollama desteği
- [ ] E-posta / Slack bildirimleri
- [ ] Daha fazla Event ID (4648, 4768, 4776...)
- [ ] Web arayüzü
- [ ] Docker desteği

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:89b4fa,50:1a1b2e,100:0f1117&height=120&section=footer&animation=fadeIn" />

**Projeyi beğendiysen ⭐ atmayı unutma**

*Siber güvenlik topluluğu için ❤️ ile yapılmıştır*

</div>