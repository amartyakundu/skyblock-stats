import base64
import gzip
import io
import nbtlib


def decode_inventory_data(encoded_data):
    raw_data = base64.b64decode(encoded_data)

    with gzip.GzipFile(fileobj=io.BytesIO(raw_data)) as nbt_file:
        return nbtlib.File.parse(nbt_file)


def get_inventory_items(encoded_data):
    if not encoded_data:
        return []

    try:
        nbt_data = decode_inventory_data(encoded_data)
    except (ValueError, OSError, EOFError):
        # bad base64, bad gzip or cut-off data
        return []

    # Some nbtlib versions keep the outer "" key, others don't
    root = nbt_data.get("", nbt_data)
    return root.get("i") or []
