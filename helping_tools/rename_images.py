from pathlib import Path

# === CONFIG ===
folder_path = Path("images")
image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
start_index = 1
zero_padding = 5
prefix = ""  # optional prefix like "dog_"

# === GET ALL IMAGE FILES (renamed or not) ===
images = sorted([f for f in folder_path.iterdir() if f.suffix.lower() in image_extensions])

# === TEMP RENAME to avoid overwriting ===
for idx, file in enumerate(images):
    temp_name = f"temp_{idx}{file.suffix.lower()}"
    file.rename(folder_path / temp_name)

# === FINAL RENAME (sequential) ===
temp_files = sorted([f for f in folder_path.iterdir() if f.name.startswith("temp_")])

for idx, file in enumerate(temp_files, start=start_index):
    new_name = f"{prefix}{str(idx).zfill(zero_padding)}{file.suffix.lower()}"
    file.rename(folder_path / new_name)
    print(f"✅ {file.name} -> {new_name}")

print(f"\nFinished renaming {len(temp_files)} files sequentially in '{folder_path.resolve()}'")
