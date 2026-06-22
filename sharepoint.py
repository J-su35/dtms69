import pandas as pd
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from office365.runtime.auth.user_credential import UserCredential
import os

# =========================
# SHAREPOINT INFO
# =========================

# site_url = "https://sites.ey.com"
site_url = "https://pea365.sharepoint.com/sites/DriveHQ"

# client_id = "paraboric500@gmail.com"
client_id = "jiranat.tan@pea.co.th"

# client_secret = "EIT255i111a"
client_secret = "cto5Xer21%"

folder_url = "/sites/DriveHQ/Shared Documents/สายงาน-วว/ฝวร/กรอ/กองระบบไฟฟ้าอัจฉริยะ"

# =========================
# CONNECT SHAREPOINT
# =========================

ctx = ClientContext(site_url).with_credentials(
    UserCredential(client_id, client_secret)
)


# =========================
# OUTPUT FILE
# =========================

output_file = r"D:\dtms69\MixKlaKU69\clean_and_filter2.csv"

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
# GET FILES
# =========================

folder = ctx.web.get_folder_by_server_relative_url(
    folder_url
)

files = folder.files

ctx.load(files)

ctx.execute_query()

print(f"Found {len(files)} files")


for file in files:
    print(file.properties["Name"])


# first_write = True

# # =========================
# # LOOP FILES
# # =========================

# for file in files:

#     file_name = file.properties["Name"]

#     if not file_name.lower().endswith(".csv"):
#         continue

#     print(f"\nDownloading: {file_name}")

#     temp_file = f"temp_{file_name}"

#     try:

#         # =========================
#         # DOWNLOAD FILE
#         # =========================

#         with open(temp_file, "wb") as local_file:

#             file.download(local_file)

#             ctx.execute_query()

#         print("Reading chunks...")

#         # =========================
#         # READ CSV CHUNKS
#         # =========================

#         for chunk in pd.read_csv(
#             temp_file,
#             header=None,
#             names=headers,
#             dtype=str,
#             chunksize=200000,
#             low_memory=False
#         ):

#             # clean
#             for col in chunk.columns:
#                 chunk[col] = chunk[col].astype(str).str.strip()

#             # remove duplicates
#             chunk = chunk.drop_duplicates()

#             # remove empty rows
#             chunk = chunk.dropna(how="all")

#             # filter PEA
#             chunk["PEA_No"] = chunk["PEA_No"].astype(str)

#             chunk = chunk[
#                 chunk["PEA_No"].isin(target_pea)
#             ]

#             # datetime
#             chunk["DATE_Time"] = pd.to_datetime(
#                 chunk["DATE_Time"],
#                 errors="coerce"
#             )

#             # remove bad datetime
#             chunk = chunk.dropna(
#                 subset=["DATE_Time"]
#             )

#             # append output
#             chunk.to_csv(
#                 output_file,
#                 mode="a",
#                 header=first_write,
#                 index=False
#             )

#             first_write = False

#             print(f"Written {len(chunk)} rows")

#         # delete temp
#         os.remove(temp_file)

#         print(f"Finished: {file_name}")

#     except Exception as e:

#         print(f"ERROR in {file_name}: {e}")

# print("\n=========================")
# print("DONE")
# print("=========================")
# print(f"Saved to: {output_file}")