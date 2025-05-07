import os

# Set your image folder path
folder_path = "images"

# Get a list of image files (you can add more extensions if needed)
image_extensions = [".jpg", ".jpeg", ".png"]
images = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in image_extensions]

# Sort and rename
for idx, filename in enumerate(sorted(images), start=1):
    ext = os.path.splitext(filename)[1]
    new_name = f"{idx}{ext}"
    old_path = os.path.join(folder_path, filename)
    new_path = os.path.join(folder_path, new_name)
    try:
        os.rename(old_path, new_path)
    except FileExistsError:
        print(f"filename {idx} has been renamed, continue to next one")
        continue

print(f"Renamed {len(images)} files.")
