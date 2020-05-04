from pathlib import Path
import zipfile


def _walk(path: Path):
    all_files = []
    for x in path.iterdir():
        if x.is_dir():
            all_files.extend(_walk(x))
        else:
            all_files.append(x)
    return all_files


def zip_files(path: Path, archive_name: str):
    all_files = _walk(path)
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in all_files:
            if f.name == '.freezeme':
                continue
            
            zipf.write(f)
        zipf.close()
