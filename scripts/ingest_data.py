import os
import shutil
import sys


if __name__ == "__main__":
    item = sys.argv[1]

    # Set the database path directly to the mpe_database_randomized folder
    db_path = "data/mpe_database_randomized"

    src = os.path.join(db_path, f"{item}.csv")
    dst = os.path.join("data", "source", f"src_{item}.csv")

    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dst), exist_ok=True)

    # Copy the file
    shutil.copyfile(src, dst)
    print(f"Copied {src} to {dst}")
