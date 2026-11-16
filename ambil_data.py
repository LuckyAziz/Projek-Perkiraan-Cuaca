import os
import requests
import pandas as pd
from datetime import datetime, timezone

ADM4 = "33.72.04.1010"
URL = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={ADM4}"
FILE = "data/jebres_forecast.csv"
os.makedirs("data", exist_ok=True)
KUNCI = ["adm4", "utc_datetime", "analysis_date"]


def ambil_data():
    resp = requests.get(URL, timeout=30)
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
    if os.path.exists(FILE):
        lama = pd.read_csv(FILE)
        gabung = pd.concat([lama, df_baru], ignore_index=True)
    else:
        gabung = df_baru

    sebelum = len(gabung)
    gabung = gabung.drop_duplicates(subset=KUNCI, keep="first")
    gabung.to_csv(FILE, index=False)
    print(f"Baru diambil: {len(df_baru)} | duplikat dibuang: {sebelum - len(gabung)} | total di file: {len(gabung)}")


if __name__ == "__main__":
    df = ambil_data()
    if df.empty:
        raise SystemExit("Data kosong, tidak disimpan.")
    simpan(df)
