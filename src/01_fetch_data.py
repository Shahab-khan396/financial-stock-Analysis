import os
import urllib.request as request
import zipfile
import sys

data_url = "https://github.com/entbappy/Branching-tutorial/raw/master/articles.zip"

def download_file(url, filename):
    try:
        print(f"Downloading {url} to {filename}...")
        filename, headers = request.urlretrieve(url, filename)
        print(f"Downloaded successfully to {filename}")
        return filename
    except Exception as e:
        print(f"Error downloading file: {e}")
        sys.exit(1)

def extract_zip(filename):
    try:
        print(f"Extracting {filename}...")
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall()
        print("Extraction completed")
    except zipfile.BadZipFile:
        print(f"Error: {filename} is not a valid zip file")
        sys.exit(1)
    except Exception as e:
        print(f"Error extracting file: {e}")
        sys.exit(1)

def remove_file(filename):
    try:
        print(f"Removing {filename}...")
        os.remove(filename)
        print("File removed successfully")
    except Exception as e:
        print(f"Error removing file: {e}")
        sys.exit(1)

def main():
    zip_filename = "articles.zip"
    download_file(data_url, zip_filename)
    extract_zip(zip_filename)
    remove_file(zip_filename)

if __name__ == "__main__":
    main()