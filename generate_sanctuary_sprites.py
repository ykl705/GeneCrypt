#!/usr/bin/env python3
import os, sys, math, random
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_enemy_sprites import (
    make_img, hex_to_rgb, palette, SPRITE_SIZE, OUTPUT_DIR,
    draw_humanoid, draw_blob, draw_eye, draw_golem, draw_skull,
    draw_tentacle, draw_machine, draw_void,
)

SHAPE_HUMANOID = 1
SHAPE_BLOB = 0
SHAPE_EYE = 3
SHAPE_TENTACLE = 4
SHAPE_MACHINE = 5
SHAPE_VOID = 9
SHAPE_GOLEM = 11
SHAPE_SKULL = 14

SANCTUARY_ENEMIES = {
    'sanctuary_ascetic':    {'name': '圣堂苦修者', 'color': '#8b4513', 'shape': SHAPE_HUMANOID},
    'sanctuary_stitcher':   {'name': '血肉缝合体', 'color': '#4a0e0e', 'shape': SHAPE_BLOB},
    'sanctuary_atonement':  {'name': '赎罪之眼',   'color': '#dc143c', 'shape': SHAPE_EYE},
    'sanctuary_chalice':    {'name': '圣餐之杯',   'color': '#c0a000', 'shape': SHAPE_MACHINE},
    'sanctuary_idol':       {'name': '腐化神像',   'color': '#2f004f', 'shape': SHAPE_GOLEM},
    'sanctuary_bloodpool':  {'name': '血池',       'color': '#8b0000', 'shape': SHAPE_BLOB},
    'sanctuary_boneguard':  {'name': '白骨卫士',   'color': '#f5f5dc', 'shape': SHAPE_SKULL},
    'sanctuary_penitent':   {'name': '忏悔者',     'color': '#4a0000', 'shape': SHAPE_HUMANOID},
    'sanctuary_deacon':     {'name': '圣堂执事',   'color': '#8b0000', 'shape': SHAPE_HUMANOID},
    'sanctuary_apostle':    {'name': '血肉使徒',   'color': '#660066', 'shape': SHAPE_HUMANOID},
    'sanctuary_relic':      {'name': '圣骸',       'color': '#c0c0c0', 'shape': SHAPE_SKULL},
    'sanctuary_malformed':  {'name': '畸形圣婴',   'color': '#ffb6c1', 'shape': SHAPE_BLOB},
    'sanctuary_thorns':     {'name': '血荆棘',     'color': '#006400', 'shape': SHAPE_TENTACLE},
    'sanctuary_inquisitor': {'name': '审判官',     'color': '#ff4500', 'shape': SHAPE_HUMANOID},
    'sanctuary_archbishop': {'name': '大主教',     'color': '#ff0000', 'shape': SHAPE_VOID},
}

SHAPE_DRAWERS = {
    SHAPE_BLOB: draw_blob,
    SHAPE_HUMANOID: draw_humanoid,
    SHAPE_EYE: draw_eye,
    SHAPE_TENTACLE: draw_tentacle,
    SHAPE_MACHINE: draw_machine,
    SHAPE_VOID: draw_void,
    SHAPE_GOLEM: draw_golem,
    SHAPE_SKULL: draw_skull,
}

def generate():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total = 0
    for tid, data in SANCTUARY_ENEMIES.items():
        rgb = hex_to_rgb(data['color'])
        pal = palette(rgb)
        seed = hash(tid) & 0x7FFFFFFF
        drawer = SHAPE_DRAWERS[data['shape']]
        for frame in range(3):
            img = make_img()
            draw = ImageDraw.Draw(img)
            drawer(draw, pal, seed, frame=frame)
            path = os.path.join(OUTPUT_DIR, f'{tid}_{frame}.png')
            img.save(path, 'PNG')
            total += 1
        print(f'  {tid} ({data["name"]}) -> {data["shape"]}')
    print(f'Generated {total} frames for {len(SANCTUARY_ENEMIES)} enemies')

if __name__ == '__main__':
    generate()
