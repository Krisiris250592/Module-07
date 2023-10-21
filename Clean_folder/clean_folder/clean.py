import sys
import re
import shutil
from pathlib import Path
JPEG_IMAGES = []
PNG_IMAGES = []
JPG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_DOC = []
DOCX_DOC = []
TXT_DOC = []
PDF_DOC = []
XLSX_DOC = []
PPTX_DOC = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
ZIP_ARCHIVES = []
GZ_ARCHIVES = []
TAR_ARCHIVES = []
OTHER_FILES = []
REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'PNG': PNG_IMAGES,
    'JPG': JPG_IMAGES,
    'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'DOC': DOC_DOC,
    'DOCX': DOCX_DOC,
    'TXT': TXT_DOC,
    'PDF': PDF_DOC,
    'XLSX': XLSX_DOC,
    'PPTX': PPTX_DOC,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'ZIP': ZIP_ARCHIVES,
    'GZ': GZ_ARCHIVES,
    'TAR': TAR_ARCHIVES,
}
FOLSERS = []
EXTENSIONS = set()
UNKNOWN = set()
def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()
def scan(folder: Path):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'OTHER_FILES'):
                FOLSERS.append(item)
                scan(item)
            continue
        extension = get_extension(item.name)
        full_name = folder / item.name
        if not extension:
            OTHER_FILES.append(full_name)
        else:
            try:
                ext_reg = REGISTER_EXTENSION[extension]
                ext_reg.append(full_name)
            except KeyError:
                UNKNOWN.add(extension)
                OTHER_FILES.append(full_name)
CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = dict()
for cyrllic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrllic)] = latin
    TRANS[ord(cyrllic.upper())] = latin.upper()
def normalize(name: str) -> str:
    translate_name = re.sub(r'[^a-zA-Z0-9_\.]', '_', name.translate(TRANS))
    return translate_name
def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))
def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute(), str(folder_for_file.absolute())))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()
def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')
    for file in AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')
    for file in MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    for file in MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV')
    for file in MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')
    for file in DOC_DOC:
        handle_media(file, folder / 'documents' / 'DOC')
    for file in DOCX_DOC:
        handle_media(file, folder / 'documents' / 'DOCX')
    for file in TXT_DOC:
        handle_media(file, folder / 'documents' / 'TXT')
    for file in PDF_DOC:
        handle_media(file, folder / 'documents' / 'PDF')
    for file in XLSX_DOC:
        handle_media(file, folder / 'documents' / 'XLSX')
    for file in PPTX_DOC:
        handle_media(file, folder / 'documents' / 'PPTX')
    for file in MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in WAV_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV')
    for file in AMR_AUDIO:
        handle_media(file, folder / 'audio' / 'AMR')
    for file in ZIP_ARCHIVES:
        handle_archive(file, folder / 'archives' / 'ZIP')
    for file in GZ_ARCHIVES:
        handle_archive(file, folder / 'archives' / 'GZ')
    for file in TAR_ARCHIVES:
        handle_archive(file, folder / 'archives' / 'TAR')
    for file in OTHER_FILES:
        handle_media(file, folder / 'OTHER_FILES')
    for folder in FOLSERS[::1]:
        try:
            folder.mkdir()
        except OSError:
            print(f'Error during remove folder {folder}')
def start():
    if sys.argv[1]:
        folder_process = Path(sys.argv[1])
        main(folder_process)