from datetime import datetime as dt
import hashlib

FILE_CHUNK_SIZE = 1024 * 1024

def generate_id(text: str):
    def hash_from(text: str):
        return hashlib.md5(text.encode()).hexdigest()
    ts = dt.now().timestamp()
    result = hash_from(text) + str(ts).replace('.', '')
    print(f'generate id: {result}')
    return result


