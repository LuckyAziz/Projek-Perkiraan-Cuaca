# Prediksi Cuaca Jangka Pendek Kelurahan Jebres, Surakarta

Proyek mata kuliah Kecerdasan Buatan oleh Lucky Aziz Putra Pratama, Julian Fikri Rahmat Fajri dan Dustin Budi Sunjoyo.
Tujuan: membandingkan akurasi model machine learning terhadap prakiraan cuaca resmi BMKG untuk wilayah Jebres, Kota Surakarta.

## Sumber Data

- Prakiraan cuaca: API Data Terbuka BMKG (`https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={kode}`), https://data.bmkg.go.id/prakiraan-cuaca/
- Data historis pembanding: [Open-Meteo / NASA POWER, belum diambil]

**Atribusi: data prakiraan cuaca bersumber dari BMKG (Badan Meteorologi, Klimatologi, dan Geofisika).**

## Lokasi

| Kelurahan | Kode adm4 |
|---|---|
| Jebres | 33.72.04.1010 |
| Mojosongo | 33.72.04.1011 |
| Pucangsawit | 33.72.04.1006 |

## Cara Kerja Pengumpulan Data

GitHub Actions menjalankan `ambil_data.py` otomatis tiap 6 jam (00:15, 06:15, 12:15, 18:15 UTC).
Skrip mengambil prakiraan 3 hari tiap lokasi, menambahkannya ke `data/jebres_forecast.csv`, dan membuang baris dengan kunci (`adm4`, `utc_datetime`, `analysis_date`) yang sama.
Workflow juga bisa dijalankan manual lewat tab Actions.

## Struktur Folder

| Folder/File | Isi | Pemilik |
|---|---|---|
| `data/` | CSV hasil pengambilan (jangan diedit manual) | Lucky |
| `ambil_data.py` | Skrip pengambilan data | Lucky |
| `.github/workflows/` | Jadwal otomatis | Lucky |
| `notebooks/` | EDA dan modeling | Dustin |
| `app/`, `docs/` | Demo, laporan, slide | Julian |

## Kamus Data (`data/jebres_forecast.csv`)

| Kolom | Arti | Satuan |
|---|---|---|
| adm4 | Kode kelurahan | - |
| desa | Nama kelurahan | - |
| analysis_date | Waktu BMKG membuat prakiraan | UTC |
| utc_datetime | Waktu yang diprakirakan | UTC |
| local_datetime | Waktu yang diprakirakan | WIB (UTC+7) |
| t | Suhu | °C |
| hu | Kelembapan | % |
| tcc | Tutupan awan | % |
| tp | Curah hujan | mm |
| ws | Kecepatan angin | km/jam |
| wd_deg | Arah angin | derajat |
| weather | Kode cuaca BMKG (1 = Cerah, 2 = Cerah Berawan, 3 = Berawan, 61 = Hujan Ringan; kode lain akan dicatat saat muncul) | - |
| weather_desc | Deskripsi cuaca | - |
| fetched_at | Waktu data diambil robot | UTC |

## Catatan Temuan Data

- Titik jam prakiraan bergeser mengikuti kapan data diambil (kadang 02:00, 03:00, 04:00 UTC dst.), jadi baris dengan `analysis_date` sama bisa punya `utc_datetime` berbeda. Duplikat dirapikan saat preprocessing.
- Prakiraan Jebres dan Mojosongo tampak identik (dugaan: resolusi grid BMKG lebih kasar dari kelurahan). [Perlu dikonfirmasi]
- `tp` bisa bernilai > 0 walau `weather_desc` = "Cerah". Definisi "hujan" harus ditetapkan tim modeling.
- Ini data prakiraan, bukan observasi. Ground truth berasal dari sumber historis terpisah.

## Cara Membaca Data

```python
import pandas as pd
url = "https://raw.githubusercontent.com/USERNAME/Projek-Perkiraan-Cuaca/main/data/jebres_forecast.csv"
df = pd.read_csv(url)
```

## Status

- [x] Pipeline pengambilan data otomatis
- [ ] Data historis pembanding
- [ ] Preprocessing dan EDA
- [ ] Modeling dan evaluasi
- [ ] Demo dan laporan
