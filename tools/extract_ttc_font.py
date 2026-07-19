import struct, sys

def read_big_u32(f):
    return struct.unpack('>I', f.read(4))[0]

def extract_ttf_from_ttc(ttc_path, ttf_path):
    with open(ttc_path, 'rb') as f:
        header = f.read(12)
        if header[:4] != b'ttcf':
            raise ValueError('Not a TTC file')
        count = read_big_u32(f)
        offsets = [read_big_u32(f) for _ in range(count)]
        f.seek(0)
        full_data = f.read()
        start = offsets[0]
        end = offsets[1] if len(offsets) > 1 else len(full_data)
        ttf_data = full_data[start:end]

    with open(ttf_path, 'wb') as out:
        out.write(ttf_data)
    print(f'Extracted {len(ttf_data)} bytes -> {ttf_path}')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python extract_ttc_font.py <input.ttc> <output.ttf>')
        sys.exit(1)
    extract_ttf_from_ttc(sys.argv[1], sys.argv[2])
