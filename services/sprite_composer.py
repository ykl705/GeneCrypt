import os
import random
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
from io import BytesIO

def compose_sprite(genome_list, enemy_templates=None):
    try:
        from PIL import Image as PILImage
    except ImportError:
        return None
    if not enemy_templates:
        return None
    tid_map = {}
    for tid, tmpl in enemy_templates.items():
        tid_map[tmpl.get('name', '')] = tid
    used = []
    for g in genome_list:
        if isinstance(g, int) and g in enemy_templates:
            used.append(g)
        elif isinstance(g, str):
            tid = tid_map.get(g)
            if tid is not None:
                used.append(tid)
    if not used:
        return None
    n_tids = len(enemy_templates)
    mosaic = [[0]*8 for _ in range(8)]
    for i, g in enumerate(genome_list):
        row = (i // 8) % 8
        col = i % 8
        tid_val = g if isinstance(g, int) else (hash(g) % n_tids)
        mosaic[row][col] = tid_val
    try:
        size = 4
        block_w = 4
        block_h = 4
        sprite_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'enemies')
        tid_textures = {}
        for tid in enemy_templates:
            fp = os.path.join(sprite_dir, f'{tid}_0.png')
            if os.path.exists(fp):
                tid_textures[tid] = PILImage.open(fp).convert('RGBA')
        if not tid_textures:
            return None
        canvas_w = 8 * block_w
        canvas_h = 8 * block_h
        canvas = PILImage.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
        for row in range(8):
            for col in range(8):
                tid = mosaic[row][col]
                tex = tid_textures.get(tid % len(tid_textures) if tid_textures else 0)
                if tex:
                    block = tex.crop((col*block_w, row*block_h, col*block_w+block_w, row*block_h+block_h))
                    canvas.paste(block, (col*block_w, row*block_h))
        buf = BytesIO()
        canvas.save(buf, format='png')
        buf.seek(0)
        core_img = CoreImage(buf, ext='png')
        return core_img.texture
    except Exception:
        return None
