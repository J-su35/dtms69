import pandas as pd
from pathlib import Path
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

# =========================
# LOGIN GOOGLE DRIVE
# =========================
gauth = GoogleAuth()

gauth.LoadClientConfigFile(
    r"C:/Users/GA/OneDrive/เดสก์ท็อป/CleannEY01/client_secrets.json"
)

gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

# =========================
# GOOGLE DRIVE FOLDER ID
# =========================
folder_id = "1hzdKTmYkWZ9vWc4cpbmWnZiA0dagCRvE"

# =========================
# OUTPUT FILE
# =========================
output_file = r"C:/Users/GA/OneDrive/เดสก์ท็อป/CleannEY01/clean_and_filter.csv"

# ลบ output เก่าถ้ามี
if os.path.exists(output_file):
    os.remove(output_file)

# =========================
# HEADER
# =========================
headers = [
    "PEA_No",
    "DATE_Time",
    "KWH",
    "SelfRead_KWH",
    "VA",
    "VB",
    "VC",
    "AA",
    "AB",
    "AC",
    "KVARH_DEL",
    "KVARH_REC",
    "KWHExport",
    "SelfRead_KWHEXP"
]

# =========================
# TARGET PEA
# =========================
target_pea = {
    "6200022544",
    "6200030933",
    "6200031047",
    "6200031051",
    "6200031052",
    "6200031073",
    "6200031074",
    "6200031084",
    "6200031085",
    "6200031086",
    "6200031087",
    "6200031088",
    "6200031902",
    "6200032193",
    "6200032194",
    "6200032196",
    "6200032198",
    "6200050504",
    "6200061392",
    "6200118626"
}

# =========================
# GET FILE LIST
# =========================
file_list = drive.ListFile({
    'q': f"'{folder_id}' in parents and trashed=false"
}).GetList()

print(f"Found {len(file_list)} files")

first_write = True

# =========================
# LOOP FILES
# =========================
for file in file_list:

    # อ่านเฉพาะ csv
    if not file['title'].lower().endswith(".csv"):
        continue

    print(f"\nDownloading: {file['title']}")

    # temp file
    temp_file = f"temp_{file['title']}"

    try:

        # =========================
        # DOWNLOAD FILE
        # =========================
        file.GetContentFile(temp_file)

        print("Reading chunks...")

        # =========================
        # READ CHUNKS
        # =========================
        for chunk in pd.read_csv(
            temp_file,
            header=None,
            names=headers,
            dtype=str,
            chunksize=200000,
            low_memory=False
        ):

            # =========================
            # CLEAN DATA
            # =========================
            for col in chunk.columns:
                chunk[col] = chunk[col].astype(str).str.strip()

            # remove duplicates
            chunk = chunk.drop_duplicates()

            # remove empty rows
            chunk = chunk.dropna(how="all")

            # =========================
            # FILTER PEA
            # =========================
            chunk["PEA_No"] = chunk["PEA_No"].astype(str)

            chunk = chunk[
                chunk["PEA_No"].isin(target_pea)
            ]

            # =========================
            # DATETIME
            # =========================
            chunk["DATE_Time"] = pd.to_datetime(
                chunk["DATE_Time"],
                errors="coerce"
            )

            # remove bad datetime
            chunk = chunk.dropna(
                subset=["DATE_Time"]
            )

            # =========================
            # SAVE OUTPUT
            # =========================
            chunk.to_csv(
                output_file,
                mode="a",
                header=first_write,
                index=False
            )

            first_write = False

            print(f"Written {len(chunk)} rows")

        # =========================
        # DELETE TEMP FILE
        # =========================
        os.remove(temp_file)

        print(f"Finished: {file['title']}")

    except Exception as e:
        print(f"ERROR in {file['title']}: {e}")

print("\n=========================")
print("DONE")
print("=========================")
print(f"Saved to: {output_file}")