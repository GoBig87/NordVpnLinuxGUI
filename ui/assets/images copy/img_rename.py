import os

if __name__ == "__main__":
    files = os.listdir()
    for file in files:
        rename = file.split("-64x64")[0] + ".png"
        os.rename(file, rename)
        os.remove(file)