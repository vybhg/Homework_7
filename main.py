import sys
import qrcode
from dotenv import load_dotenv
import logging
from pathlib import Path
import os
import argparse
import validators
from datetime import datetime

# Load environment variables
load_dotenv()

# Configuration Variables
DEFAULT_QR_DIRECTORY = 'qr_codes'
DEFAULT_FILL_COLOR = 'yellow'
DEFAULT_BACK_COLOR = 'black'

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def create_directory(directory: Path):
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create directory {directory}: {e}")
        sys.exit(1)

def is_valid_url(url):
    if validators.url(url):
        return True
    else:
        logging.error(f"Invalid URL provided: {url}")
        return False

def generate_qr_code(data, path, fill_color=DEFAULT_FILL_COLOR, back_color=DEFAULT_BACK_COLOR):
    if not is_valid_url(data):
        return

    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color=fill_color, back_color=back_color)

        with path.open('wb') as qr_file:
            qr_image.save(qr_file)
        logging.info(f"QR code saved successfully at {path}")

    except Exception as e:
        logging.error(f"Error occurred during QR code generation or saving: {e}")

def main():
    parser = argparse.ArgumentParser(description='Generate a QR code.')
    parser.add_argument('--url', help='URL to encode in the QR code', default='https://github.com/vybhg/Homework_7.git')
    args = parser.parse_args()

    setup_logging()

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    qr_filename = f"QR_{timestamp}.png"

    qr_directory = Path.cwd() / os.getenv('QR_CODE_DIR', DEFAULT_QR_DIRECTORY)
    create_directory(qr_directory)

    qr_code_path = qr_directory / qr_filename

    generate_qr_code(args.url, qr_code_path)

if _name_ == "_main_":
    main()
