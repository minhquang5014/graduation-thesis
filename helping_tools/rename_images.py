from pathlib import Path
import cv2
import shutil
import os
from datetime import datetime
# === CONFIG ===
folder_path = Path("images")
image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
start_index = 1
zero_padding = 5
prefix = ""  # optional prefix like "dog_"
max_folder_size = 20 * 1024 * 1024  # 20 MB in bytes

# === CLEANUP OLD TEMP FILES ===
for f in folder_path.iterdir():
    if f.name.startswith("temp_") and f.suffix.lower() in image_extensions:
        f.unlink()

# === GET ALL IMAGE FILES (renamed or not) ===
images = sorted([f for f in folder_path.iterdir() if f.suffix.lower() in image_extensions])

# === TEMP RENAME and resize to avoid overwriting ===
for idx, file in enumerate(images):
    # Read and resize image
    img = cv2.imread(str(file))
    if img is None:
        print(f"⚠️ Skipped unreadable file: {file.name}")
        continue

    img = cv2.resize(img, (640, 480))
    cv2.imwrite(str(file), img)  # Overwrite resized image

    # Create a unique temporary filename
    temp_name = f"temp_{file.stem}_{idx}{file.suffix.lower()}"
    file.rename(folder_path / temp_name)

# === FINAL RENAME (sequential) ===
temp_files = sorted([f for f in folder_path.iterdir() if f.name.startswith("temp_")])
renamed_files = []

for idx, file in enumerate(temp_files, start=start_index):
    from time import time
    new_name = f"{prefix}_{time()}{str(idx).zfill(zero_padding)}{file.suffix.lower()}"
    new_path = folder_path / new_name
    file.rename(new_path)
    renamed_files.append(new_path)
    print(f"✅ {file.name} -> {new_name}")

# === SPLIT INTO FOLDERS OF MAX 20MB ===
folder_counter = 4
current_folder = folder_path / f"set_{folder_counter}"
current_folder.mkdir(exist_ok=True)
current_size = 0

for file in renamed_files:
    file_size = file.stat().st_size

    if current_size + file_size > max_folder_size:
        folder_counter += 1
        current_folder = folder_path / f"set_{folder_counter}"
        current_folder.mkdir(exist_ok=True)
        current_size = 0

    shutil.move(str(file), current_folder / file.name)
    current_size += file_size

print(f"\n🎉 Finished organizing {len(renamed_files)} files into folders under 20MB each at '{folder_path.resolve()}'")
