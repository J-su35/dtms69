import pandas as pd
from pathlib import Path

# =========================
# INPUT / OUTPUT
# =========================
input_file = "/Users/mixkybabo/Downloads/KWH_IMP01.csv"
output_file = str(Path.home() / "Desktop" / "clean and filter.csv")

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

print("Reading CSV...")

# =========================
# READ CSV (ไม่มี header)
# =========================
df = pd.read_csv(
    input_file,
    header=None,
    names=headers,
    dtype=str,
    low_memory=False
)

# =========================
# CLEAN DATA
# =========================
for col in df.columns:
    df[col] = df[col].astype(str).str.strip()

# ลบ duplicate
df = df.drop_duplicates()

# ลบ row ว่าง
df = df.dropna(how="all")

# =========================
# FILTER PEA
# =========================
df["PEA_No"] = df["PEA_No"].astype(str)

df = df[df["PEA_No"].isin(target_pea)]

# =========================
# CLEAN DATETIME
# =========================
df["DATE_Time"] = pd.to_datetime(
    df["DATE_Time"],
    errors="coerce"
)

# ลบ datetime เสีย
df = df.dropna(subset=["DATE_Time"])

# =========================
# SORT DATA
# =========================
df = df.sort_values(
    by=["PEA_No", "DATE_Time"]
)

# =========================
# SAVE OUTPUT
# =========================
df.to_csv(
    output_file,
    index=False
)

print("Done!")
print(f"Saved to: {output_file}")
print(f"Total rows: {len(df)}")