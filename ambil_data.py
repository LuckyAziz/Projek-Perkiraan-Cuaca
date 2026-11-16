import os
import time
import requests
import pandas as pd
from datetime import datetime, timezone

LOKASI = [
    "33.72.04.1010",  # Jebres
    "33.72.04.1011",  # Mojosongo 
    "33.72.04.1006",  # Pucangsawit 
]
FILE = "data/jebres_forecast.csv"
KUNCI = ["adm4", "utc_datetime", "analysis_date"]


def ambil_satu(adm4):
    url = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={adm4}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    lokasi = data["data"][0]["lokasi"]
    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    rows = []
    for hari in data["data"][0]["cuaca"]:
        for item in hari:
            rows.append({
                "adm4": lokasi["adm4"],
                "desa": lokasi["desa"],
                "analysis_date": item["analysis_date"],
                "utc_datetime": item["utc_datetime"],
                "local_datetime": item["local_datetime"],
                "t": item["t"],
                "hu": item["hu"],
                "tcc": item["tcc"],
                "tp": item["tp"],
                "ws": item["ws"],
                "wd_deg": item["wd_deg"],
                "weather": item["weather"],
                "weather_desc": item["weather_desc"],
                "fetched_at": fetched_at,
            })
    return pd.DataFrame(rows)


def simpan(df_baru):
    os.makedirs(os.path.dirname(FILE), exist_ok=True)
    if os.path.exists(FILE):
        gabung = pd.concat([pd.read_csv(FILE), df_baru], ignore_index=True)
    else:
        gabung = df_baru
    sebelum = len(gabung)
    gabung = gabung.drop_duplicates(subset=KUNCI, keep="first")
    gabung.to_csv(FILE, index=False)
    print(f"Baru: {len(df_baru)} | duplikat dibuang: {sebelum - len(gabung)} | total: {len(gabung)}")


if __name__ == "__main__":
    hasil, gagal = [], []
    for kode in LOKASI:
        try:
            df = ambil_satu(kode)
            print(f"OK {kode}: {len(df)} baris")
            hasil.append(df)
        except Exception as e:
            print(f"GAGAL {kode}: {e}")
            gagal.append(kode)
        time.sleep(2)  # jeda sopan agar tidak melewati batas request

    if hasil:
        simpan(pd.concat(hasil, ignore_index=True))
    if gagal:
        raise SystemExit(f"Lokasi gagal: {gagal}")
