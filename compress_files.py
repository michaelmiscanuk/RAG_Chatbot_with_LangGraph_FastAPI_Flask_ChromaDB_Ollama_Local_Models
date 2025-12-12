"""Compression utility script for CZSU multi-agent project using XZ (LZMA) format."""

import os
import lzma
import tarfile
from pathlib import Path
from dotenv import load_dotenv

# Get the base directory
try:
    BASE_DIR = Path(__file__).resolve().parents[0]
except NameError:
    BASE_DIR = Path(os.getcwd())

# Load environment variables
load_dotenv(BASE_DIR / "backend" / ".env")


# Get embedding model name for ChromaDB path
def get_chromadb_path():
    """Get ChromaDB path with embedding model suffix."""
    provider = os.getenv("EMBEDDING_PROVIDER", "ollama").lower()
    if provider == "azure":
        model_name = os.getenv(
            "AZURE_EMBEDDING_DEPLOYMENT", "text-embedding-3-small_mimi"
        )
    else:
        model_name = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    # Sanitize model name for use in paths
    model_name = model_name.replace("/", "-").replace("\\", "-").replace(":", "-")
    return BASE_DIR / "backend" / "data" / f"chroma_db_{model_name}"


# Configuration of paths to zip
PATHS_TO_ZIP = [
    get_chromadb_path(),  # ChromaDB for chatbot (with embedding model suffix)
]


def compress_path(path_to_compress: Path):
    """Compress a file or folder at the specified path using tar.xz (LZMA).

    XZ (LZMA) provides excellent compression ratios, typically 30-50% better than ZIP.
    """
    abs_path = path_to_compress
    if not abs_path.exists():
        print(f"Warning: Path does not exist: {abs_path}")
        return

    # Create compressed file path with .tar.xz extension
    compressed_path = abs_path.parent / f"{abs_path.name}.tar.xz"
    print(f"Compressing: {abs_path}")
    print(f"Output: {compressed_path}")
    print("Using XZ (LZMA) compression for maximum compression ratio...")
    print("This may take a while but will produce the smallest file size.")

    try:
        # Create tar.xz archive with maximum compression
        # preset=9 gives maximum compression, slower but smallest size
        with lzma.open(compressed_path, "wb", preset=9) as xz_file:
            with tarfile.open(fileobj=xz_file, mode="w") as tar:
                if abs_path.is_file():
                    # If it's a file, just add it
                    tar.add(abs_path, arcname=abs_path.name)
                else:
                    # If it's a directory, add it recursively
                    tar.add(abs_path, arcname=abs_path.name)

        print(f"Successfully compressed: {abs_path}")
        # Show file size info
        original_size = get_size(abs_path)
        compressed_size = compressed_path.stat().st_size
        if original_size > 0:
            compression_ratio = (
                (original_size - compressed_size) / original_size
            ) * 100
            print(f"Original size: {format_size(original_size)}")
            print(f"Compressed size: {format_size(compressed_size)}")
            print(f"Compression ratio: {compression_ratio:.1f}%")
    except Exception as exc:
        print(f"Compression failed: {exc}")
        raise


def get_size(path: Path):
    """Get total size of a file or directory."""
    if path.is_file():
        return path.stat().st_size
    else:
        total_size = 0
        for root, _, files in os.walk(path):
            for file in files:
                file_path = Path(root) / file
                try:
                    total_size += file_path.stat().st_size
                except (OSError, FileNotFoundError):
                    pass
        return total_size


def format_size(size_bytes):
    """Format size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"


def upload_to_gdrive(file_path: Path, gdrive_folder_link: str) -> bool:
    """
    Prepare file for Google Drive upload and provide easy access.
    Since Google Drive API requires authentication, this function will:
    1. Copy the file to an easily accessible location
    2. Open the Google Drive folder in browser
    3. Provide clear instructions for manual upload

    Args:
        file_path: Path to the file to upload
        gdrive_folder_link: Google Drive shared folder link

    Returns:
        bool: True if file preparation successful, False otherwise
    """
    if not file_path.exists():
        print(f"Error: File does not exist: {file_path}")
        return False

    try:
        # Create a convenient upload folder on desktop
        desktop_path = Path.home() / "Desktop"
        upload_folder = desktop_path / "GDRIVE_UPLOAD"
        upload_folder.mkdir(exist_ok=True)

        # Copy file to desktop upload folder
        destination_file = upload_folder / file_path.name

        print(f"Preparing file for Google Drive upload...")
        print(f"File: {file_path.name}")
        print(f"Size: {format_size(file_path.stat().st_size)}")

        # Show progress bar while copying
        print("Copying file to desktop folder...")
        print_progress_bar(0, 100, prefix="Progress:", suffix="Complete", length=50)

        import shutil

        shutil.copy2(file_path, destination_file)

        print_progress_bar(100, 100, prefix="Progress:", suffix="Complete", length=50)

        print(f"\n✓ File copied to: {destination_file}")
        print(f"\n{'='*60}")
        print("MANUAL UPLOAD INSTRUCTIONS")
        print(f"{'='*60}")
        print(f"1. File location: {destination_file}")
        print(f"2. Google Drive folder: {gdrive_folder_link}")
        print(f"3. Open the Google Drive folder in your browser")
        print(f"4. Drag and drop the file from your desktop folder")
        print(f"{'='*60}")

        # Try to open the Google Drive folder in browser
        try:
            import webbrowser

            print(f"Opening Google Drive folder in browser...")
            webbrowser.open(gdrive_folder_link)
        except Exception as exc:
            print(f"Could not open browser automatically: {exc}")
            print(f"Please manually open: {gdrive_folder_link}")

        # Try to open the desktop folder
        try:
            import subprocess

            print(f"Opening desktop upload folder...")
            subprocess.run(["explorer", str(upload_folder)], check=False)
        except Exception as exc:
            print(f"Could not open folder automatically: {exc}")
            print(f"Please manually navigate to: {upload_folder}")

        return True

    except Exception as exc:
        print(f"\n✗ Error preparing file: {exc}")
        print(f"Manual upload required:")
        print(f"File: {file_path}")
        print(f"Google Drive folder: {gdrive_folder_link}")
        return False


def print_progress_bar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=1,
    length=100,
    fill="█",
    print_end="\r",
):
    """
    Call in a loop to create terminal progress bar
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + "-" * (length - filled_length)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


def upload_pdf_chromadb_to_gdrive():
    """Prepare the pdf_chromadb_llamaparse.tar.xz file for Google Drive upload."""
    pdf_chromadb_compressed = BASE_DIR / "data" / "pdf_chromadb_llamaparse.tar.xz"
    # Google Drive shared folder link
    gdrive_folder_link = (
        "https://drive.google.com/drive/folders/"
        "1TZWxURgYoYHgKMji4OV333ftEDCyJRgD?usp=sharing"
    )

    print(f"\n{'='*50}")
    print("PREPARING FOR GOOGLE DRIVE UPLOAD")
    print(f"{'='*50}")

    if pdf_chromadb_compressed.exists():
        success = upload_to_gdrive(pdf_chromadb_compressed, gdrive_folder_link)
        if success:
            print("✓ File preparation completed successfully!")
            print("Please follow the instructions above to complete the upload.")
        else:
            print("✗ File preparation failed.")
    else:
        print(f"Warning: File not found: {pdf_chromadb_compressed}")
        print(
            "Make sure the pdf_chromadb_llamaparse folder was compressed successfully."
        )


def main():
    """Main function to compress files and upload to Google Drive."""
    print(f"Base directory: {BASE_DIR}")
    print("Starting compression process with XZ (LZMA) - best compression ratio...")

    for path in PATHS_TO_ZIP:
        compress_path(path)

    print("\nCompression process completed!")

    # Prepare the pdf_chromadb_llamaparse.tar.xz for Google Drive upload
    upload_pdf_chromadb_to_gdrive()


if __name__ == "__main__":
    main()
