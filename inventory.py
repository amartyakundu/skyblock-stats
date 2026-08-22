import base64
import gzip
import io
import nbtlib


def decode_inventory_data(encoded_data):
    raw_data = base64.b64decode(encoded_data)

    with gzip.GzipFile(fileobj=io.BytesIO(raw_data)) as nbt_file:
        return nbtlib.File.parse(nbt_file)