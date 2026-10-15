"""Restore checked static images before building; never rewrite edited assets."""
from pathlib import Path
import hashlib,json,zipfile

def prepare(root=None):
    root=Path(root or Path(__file__).resolve().parents[1]).resolve()
    folder=root/'asset-bundles'
    if not (folder/'manifest.json').exists():return
    manifest=json.loads((folder/'manifest.json').read_text())
    assert manifest['format']==1,'Unsupported image bundle format'
    for bundle in manifest['bundles']:
        archive=folder/bundle['file']
        assert hashlib.sha256(archive.read_bytes()).hexdigest()==bundle['sha256'],archive
        with zipfile.ZipFile(archive) as z:
            expected={x['path'] for x in bundle['files']}
            assert set(z.namelist())==expected and len(z.namelist())==len(expected),archive
            for item in bundle['files']:
                target=(root/item['path']).resolve()
                assert target.is_relative_to(root/'content'),item['path']
                raw=target.read_bytes() if target.exists() else z.read(item['path'])
                assert len(raw)==item['size'] and hashlib.sha256(raw).hexdigest()==item['sha256'],item['path']
                if not target.exists():
                    target.parent.mkdir(parents=True,exist_ok=True)
                    target.write_bytes(raw)

if __name__=='__main__':prepare()
