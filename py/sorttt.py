import pandas as pd

# อ่านไฟล์ CSV
df = pd.read_csv(r"C:/Users/GA/OneDrive/เดสก์ท็อป/CleannEY01/clean_and_filter.csv")

# แปลง DATE_Time เป็น datetime
df['DATE_Time'] = pd.to_datetime(df['DATE_Time'])

# เรียงตามเลขมิเตอร์ และวันเวลา
df = df.sort_values(
    by=['PEA_No', 'DATE_Time']
)

# แยกเป็นกลุ่มตามเลขมิเตอร์
grouped = {
    meter: group
    for meter, group in df.groupby('PEA_No')
}

# ตัวอย่างแสดงข้อมูลแต่ละกลุ่ม
for meter, data in grouped.items():
    print(f"\nMeter: {meter}")
    print(data[['PEA_No', 'DATE_Time']].head())

# บันทึกไฟล์ใหม่
df.to_csv(r"C:/Users/GA/OneDrive/เดสก์ท็อป/CleannEY01/sorted_meter.csv", index=False)

print("เสร็จแล้ว")