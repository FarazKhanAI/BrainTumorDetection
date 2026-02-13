import os

folders = [
    "dataset/Train/Pituitary/labels",
    "dataset/Val/Pituitary/labels"
]

for folder in folders:
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            path = os.path.join(folder, file)
            with open(path, "r") as f:
                lines = f.readlines()
            new_lines = [line.replace("3 ", "2 ", 1) for line in lines]
            with open(path, "w") as f:
                f.writelines(new_lines)
            print(f"Updated: {file}")
