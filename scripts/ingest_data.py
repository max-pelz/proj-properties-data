import os
import shutil
import sys
from dotenv import load_dotenv


if __name__ == "__main__":
    item = sys.argv[1]

    # Load environment variables from .env file
    load_dotenv(dotenv_path='.env')

    db_path = os.environ.get('DB_PATH')

    if not db_path:
        raise EnvironmentError("Environment variable DB_PATH is not set.")

    src = os.path.join(db_path, f"{item}.csv")
    dst = os.path.join("data", "source", f"src_{item}.csv")

    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dst), exist_ok=True)

    # Copy the file
    shutil.copyfile(src, dst)
    print(f"Copied {src} to {dst}")
