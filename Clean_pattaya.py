import pandas as pd
from pathlib import Path

# =========================
# INPUT / OUTPUT
# =========================
input_dir = Path("E:/Documents/dtms69/10_October")
output_file = Path("E:/Documents/dtms69/filtered_data_oct.csv")
chunk_size = 200000

# =========================
# HEADER ที่ต้องการ
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

# csv_files = [
#     input_dir / f"KWH_IMP{i:02d}.csv"
#     for i in range(1, 32)
# ]

csv_files = sorted(input_dir.glob("KWH_IMP*.csv"))

first_write = True
total_rows = 0
files_found = 0

print("Reading CSV files...")

if output_file.exists():
    output_file.unlink()

for csv_file in csv_files:
    if not csv_file.exists():
        print(f"Skip missing file: {csv_file.name}")
        continue

    files_found += 1
    print(f"Reading: {csv_file.name}")

    for chunk in pd.read_csv(
        csv_file,
        header=None,
        names=headers,
        dtype=str,
        low_memory=False,
        chunksize=chunk_size
    ):
        # =========================
        # CLEAN DATA
        # =========================
        for col in chunk.columns:
            chunk[col] = chunk[col].astype(str).str.strip()

        # ลบ duplicate ภายใน chunk
        chunk = chunk.drop_duplicates()

        # ลบ row ว่าง
        chunk = chunk.dropna(how="all")

        # =========================
        # FILTER PEA
        # =========================
        chunk["PEA_No"] = chunk["PEA_No"].astype(str)
        chunk = chunk[chunk["PEA_No"].isin(target_pea)]

        # =========================
        # CLEAN DATETIME
        # =========================
        chunk["DATE_Time"] = pd.to_datetime(
            chunk["DATE_Time"],
            errors="coerce"
        )

        # ลบ datetime เสีย
        chunk = chunk.dropna(subset=["DATE_Time"])

        if chunk.empty:
            continue

        # เรียงภายใน chunk ก่อนเขียนออก
        chunk = chunk.sort_values(
            by=["PEA_No", "DATE_Time"]
        )

        chunk.to_csv(
            output_file,
            mode="a",
            header=first_write,
            index=False
        )

        first_write = False
        total_rows += len(chunk)
        print(f"Written {len(chunk)} rows from {csv_file.name}")

if files_found == 0:
    raise FileNotFoundError(
        f"No matching CSV files found in {input_dir}"
    )

print("Done!")
print(f"Saved to: {output_file}")
print(f"Total rows: {total_rows}")
