import os

folders = [
    "dataset/Train/No Tumor/labels",
    "dataset/Val/No Tumor/labels"
]

for folder in folders:
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            open(os.path.join(folder, file), "w").close()
            print(f"Emptied: {file}")
