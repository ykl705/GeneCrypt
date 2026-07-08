#!/usr/bin/env python3
import os, sys, math, random, json
from PIL import Image, ImageDraw

random.seed(42)
SPRITE_SIZE = 32
SHIFT = 2
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'enemies')

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def palette(rgb):
    r, g, b = rgb
    return {
        'dark': (max(0, r - 60), max(0, g - 60), max(0, b - 60)),
        'base': rgb,
        'mid': (min(255, r + 40), min(255, g + 40), min(255, b + 40)),
        'light': (min(255, r + 80), min(255, g + 80), min(255, b + 80)),
        'lit': (min(255, r + 120), min(255, g + 120), min(255, b + 120)),
    }

def make_img():
    return Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))

def fill_rect(draw, x1, y1, x2, y2, clr):
    draw.rectangle([x1, y1, x2, y2], fill=clr)

def fill_ellipse(draw, x1, y1, x2, y2, clr):
    draw.ellipse([x1, y1, x2, y2], fill=clr)

def fill_poly(draw, pts, clr):
    draw.polygon(pts, fill=clr)

# ---------- shape classifiers ----------
SHAPE_BLOB = 0
SHAPE_HUMANOID = 1
SHAPE_BEAST = 2
SHAPE_EYE = 3
SHAPE_TENTACLE = 4
SHAPE_MACHINE = 5
SHAPE_ELEMENTAL = 6
SHAPE_WORM = 7
SHAPE_CRYSTAL = 8
SHAPE_VOID = 9
SHAPE_DRAGON = 10
SHAPE_GOLEM = 11
SHAPE_SPIDER = 12
SHAPE_GHOST = 13
SHAPE_SKULL = 14

def classify_shape(name):
    kw = {
        '黏液': SHAPE_BLOB, '培植': SHAPE_BLOB, '聚合': SHAPE_BLOB,
        '雾团': SHAPE_BLOB, '气体': SHAPE_BLOB, '泥浆': SHAPE_BLOB,
        '水银': SHAPE_BLOB, '泡沫': SHAPE_BLOB, '熔岩': SHAPE_ELEMENTAL,
        '元素': SHAPE_ELEMENTAL, '烈焰': SHAPE_ELEMENTAL, '火焰': SHAPE_ELEMENTAL,
        '冰霜': SHAPE_ELEMENTAL, '冰晶': SHAPE_CRYSTAL, '雷霆': SHAPE_ELEMENTAL,
        '风暴': SHAPE_ELEMENTAL, '飓风': SHAPE_ELEMENTAL, '极光': SHAPE_ELEMENTAL,
        '蒸汽': SHAPE_ELEMENTAL, '棱晶': SHAPE_CRYSTAL, '水晶': SHAPE_CRYSTAL,
        '守卫': SHAPE_HUMANOID, '战士': SHAPE_HUMANOID, '弓手': SHAPE_HUMANOID,
        '祭司': SHAPE_HUMANOID, '骑士': SHAPE_HUMANOID, '哨兵': SHAPE_HUMANOID,
        '研究员': SHAPE_HUMANOID, '科学家': SHAPE_HUMANOID, '保安': SHAPE_HUMANOID,
        '实验体': SHAPE_HUMANOID, '先驱': SHAPE_HUMANOID, '使徒': SHAPE_HUMANOID,
        '机甲': SHAPE_MACHINE, '机械': SHAPE_MACHINE,
        '机器人': SHAPE_MACHINE, '离心机': SHAPE_MACHINE, '发电机': SHAPE_MACHINE,
        '注射器': SHAPE_MACHINE, '弩车': SHAPE_MACHINE, '铁甲': SHAPE_MACHINE,
        '堡垒': SHAPE_MACHINE, '钢铁': SHAPE_MACHINE, '金属': SHAPE_MACHINE,
        '要塞': SHAPE_MACHINE, '机关': SHAPE_MACHINE,
        '猎犬': SHAPE_BEAST, '巨兽': SHAPE_BEAST, '猎手': SHAPE_BEAST,
        '巨口': SHAPE_BEAST, '潜伏': SHAPE_BEAST, '爬行': SHAPE_BEAST,
        '异虫': SHAPE_BEAST, '猛兽': SHAPE_BEAST,
        '虫群': SHAPE_SPIDER, '蜘蛛': SHAPE_SPIDER, '圣甲虫': SHAPE_SPIDER,
        '眼': SHAPE_EYE, '凝视': SHAPE_EYE,
        '触手': SHAPE_TENTACLE, '触须': SHAPE_TENTACLE,
        '蛇': SHAPE_WORM, '蠕虫': SHAPE_WORM, '编织': SHAPE_WORM,
        '虚空': SHAPE_VOID, '暗影': SHAPE_VOID, '阴影': SHAPE_VOID,
        '深渊': SHAPE_VOID, '混沌': SHAPE_VOID, '黑暗': SHAPE_VOID,
        '龙': SHAPE_DRAGON, '龙裔': SHAPE_DRAGON,
        '魔像': SHAPE_GOLEM, '石像': SHAPE_GOLEM, '雕像': SHAPE_GOLEM,
        '方尖碑': SHAPE_GOLEM, '巨石': SHAPE_GOLEM, '泰坦': SHAPE_GOLEM,
        '怨灵': SHAPE_GHOST, '幻影': SHAPE_GHOST, '幽灵': SHAPE_GHOST,
        '鬼火': SHAPE_GHOST, '海市': SHAPE_GHOST,
        '骷髅': SHAPE_SKULL, '亡灵': SHAPE_SKULL,
        '腐': SHAPE_BLOB, '毒': SHAPE_BLOB,
        '哨兵': SHAPE_HUMANOID, '小鬼': SHAPE_HUMANOID, '恶魔': SHAPE_HUMANOID,
        '塞壬': SHAPE_HUMANOID, '蛇神': SHAPE_WORM, '半机械': SHAPE_MACHINE,
        '狮': SHAPE_BEAST, '孢子': SHAPE_BLOB,
    }
    for k, v in kw.items():
        if k in name:
            return v
    return SHAPE_HUMANOID

# ---------- drawing functions (all accept frame) ----------
def draw_blob(draw, pal, seed, frame=0):
    rnd = random.Random(seed)
    c = pal['base']
    dc = pal['dark']
    lc = pal['light']
    squeeze = {0: 0, 1: -1, 2: 1}[frame]
    body_h = 18 + rnd.randint(-2, 2) + squeeze
    body_y = 28 - body_h
    bw = 20 + rnd.randint(-2, 2)
    bx = 16 - bw // 2
    fill_ellipse(draw, bx, body_y, bx + bw, 28, c)
    fill_ellipse(draw, bx + 1, body_y + 1, bx + bw - 1, 28, c)
    hl_h = body_h // 3
    fill_ellipse(draw, bx + 4, body_y + 2, bx + bw - 6, body_y + hl_h, lc)
    eye_state = {0: 0, 1: -1, 2: 0}[frame]
    ey = body_y + body_h // 2 - 2 + eye_state
    eye_clr = (255, 50, 50) if rnd.random() < 0.5 else (255, 255, 100)
    if frame == 1:
        eye_clr = (255, 200, 200)
    fill_ellipse(draw, bx + 5, ey, bx + 8, ey + 4, eye_clr)
    fill_ellipse(draw, bx + bw - 9, ey, bx + bw - 6, ey + 4, eye_clr)
    for i in range(3):
        dx = bx + 4 + i * 5 + rnd.randint(-1, 1)
        dh = 2 + rnd.randint(0, 2)
        fill_ellipse(draw, dx, 28 - dh, dx + 3, 28, dc)

def draw_humanoid(draw, pal, seed, frame=0):
    rnd = random.Random(seed)
    c = pal['base']
    dc = pal['dark']
    lc = pal['light']
    dy = {0: 0, 1: -1, 2: 1}[frame]
    bx = 11
    bw = 10
    by = 10 + dy
    bh = 14
    fill_rect(draw, bx, by, bx + bw, by + bh, c)
    fill_rect(draw, bx + 1, by, bx + bw - 1, by + bh, lc)
    hx = 12
    hy = 3 + dy
    hw = 8
    hh = 8
    fill_ellipse(draw, hx, hy, hx + hw, hy + hh, c)
    fill_ellipse(draw, hx + 1, hy + 1, hx + hw - 1, hy + hh, lc)
    eye_clr = (255, 60, 60) if rnd.random() < 0.6 else (255, 200, 50)
    if frame == 1:
        eye_clr = (255, 255, 100)
    fill_ellipse(draw, hx + 1, hy + 3, hx + 3, hy + 5, eye_clr)
    fill_ellipse(draw, hx + 5, hy + 3, hx + 7, hy + 5, eye_clr)
    fill_rect(draw, bx + 1, by + bh, bx + 4, by + bh + 6, dc)
    fill_rect(draw, bx + bw - 4, by + bh, bx + bw - 1, by + bh + 6, dc)
    fill_rect(draw, bx - 2, by + 3, bx, by + 3 + 8, dc)
    fill_rect(draw, bx + bw, by + 3, bx + bw + 2, by + 3 + 8, dc)

def draw_beast(draw, pal, seed, frame=0):
    rnd = random.Random(seed)
    c = pal['base']
    dc = pal['dark']
    lc = pal['light']
    dy = {0: 0, 1: -1, 2: 1}[frame]
    fill_ellipse(draw, 7, 12 + dy, 25, 24 + dy, c)
    fill_ellipse(draw, 8, 13 + dy, 24, 24 + dy, lc)
    fill_ellipse(draw, 3, 8 + dy, 13, 18 + dy, c)
    fill_ellipse(draw, 4, 9 + dy, 12, 17 + dy, lc)
    eye_clr = (255, 60, 60)
    if frame == 1:
        eye_clr = (255, 100, 100)
    fill_ellipse(draw, 5, 11 + dy, 7, 13 + dy, eye_clr)
    fill_ellipse(draw, 9, 11 + dy, 11, 13 + dy, eye_clr)
    fill_rect(draw, 9, 24 + dy, 12, 30 + dy, dc)
    fill_rect(draw, 13, 24 + dy, 16, 30 + dy, dc)
    fill_rect(draw, 18, 24 + dy, 21, 30 + dy, dc)
    fill_rect(draw, 22, 24 + dy, 25, 30 + dy, dc)
    fill_ellipse(draw, 24, 14 + dy, 30, 18 + dy, dc)

def draw_eye(draw, pal, seed, frame=0):
    rnd = random.Random(seed)
    c = pal['base']
    dc = pal['dark']
    lc = pal['light']
    fill_ellipse(draw, 4, 4, 28, 28, dc)
    fill_ellipse(draw, 5, 5, 27, 27, c)
    fill_ellipse(draw, 6, 6, 26, 26, lc)
    fill_ellipse(draw, 9, 9, 23, 23, dc)
    fill_ellipse(draw, 10, 10, 22, 22, pal['mid'])
    pupil_r = {0: 3, 1: 2, 2: 4}[frame]
    pupil = (255, 0, 0) if rnd.random() < 0.5 else (0, 0, 0)
    cx, cy = 16, 16
    fill_ellipse(draw, cx - pupil_r, cy - pupil_r, cx + pupil_r, cy + pupil_r, pupil)
    if frame == 2:
        fill_ellipse(draw, cx - pupil_r - 1, cy - pupil_r - 1, cx + pupil_r + 1, cy + pupil_r + 1, (255, 0, 0, 100))
    fill_ellipse(draw, 11, 11, 14, 14, (255, 255, 255, 180))
    for i in range(3):
        vx = 4 + rnd.randint(0, 3)
        vy = 4 + rnd.randint(0, 10)
        fill_rect(draw, vx, vy, vx + 1, vy + 2, (255, 80, 80, 160))
    for i in range(4):
        ang = i * 1.57 + rnd.random() * 0.5 + {0: 0, 1: 0.2, 2: -0.2}[frame]
        tx = 16 + int(18 * math.cos(ang))
        ty = 16 + int(18 * math.sin(ang))
        fill_ellipse(draw, tx - 2, ty - 2, tx + 2, ty + 2, dc)

def draw_tentacle(draw, pal, seed, frame=0):
    rnd = random.Random(seed)
    c = pal['base']
    dc = pal['dark']
    lc = pal['light']
    wave = {0: 0, 1: 0.8, 2: -0.8}[frame]
    for i in range(3):
        ox = 7 + i * 9 + rnd.randint(-1, 1)
        pts = []
        for j in range(8):
            t = j / 7
            x = ox + int(math.sin(t * 4 + i * 1.5 + seed + wave) * 5)
            y = int(t * 28)
            pts.append((x, y))
        for j in range(len(pts) - 1):
            w = 4 - j // 2
            fill_ellipse(draw, pts[j][0] - w // 2, pts[j][1], pts[j][0] + w // 2, pts[j][1] + 4, c if j % 2 == 0 else dc)
    fill_ellipse(draw, 4, 22, 28, 30, dc)

def draw_machine(draw, pal, seed, frame=0):
    rnd = random.Random(seed)
    c = pal['base']
    dc = pal['dark']
    lc = pal['light']
    dy = {0: 0, 1: -1, 2: 1}[frame]
    fill_rect(draw, 6, 8 + dy, 26, 24 + dy, dc)
    fill_rect(draw, 7, 9 + dy, 25, 23 + dy, c)
    fill_rect(draw, 8, 10 + dy, 24, 22 + dy, pal['mid'])
    fill_rect(draw, 14, 3 + dy, 18, 9 + dy, dc)
    fill_rect(draw, 15, 4 + dy, 17, 8 + dy, lc)
    led = (255, 60, 60) if frame == 1 else ((0, 255, 255) if frame == 2 else (255, 60, 60))
    fill_rect(draw, 12, 12 + dy, 20, 16 + dy, (0, 0, 0))
    fill_rect(draw, 13, 13 + dy, 19, 15 + dy, led)
    fill_rect(draw, 5, 24 + dy, 27, 27 + dy, dc)
    for i in range(4):
        wx = 7 + i * 6
        fill_ellipse(draw, wx, 24 + dy, wx + 3, 27 + dy, (80, 80, 80))
    fill_rect(draw, 9, 18 + dy, 11, 22 + dy, dc)
    fill_rect(draw, 21, 18 + dy, 23, 22 + dy, dc)

def draw_elemental(draw, pal, seed, frame=0):
    rnd = random.Random(seed)
    c = pal['base']
    dc = pal['dark']
    lc = pal['light']
    pulse = {0: 0, 1: 3, 2: -2}[frame]
    pts = []
    for i in range(12):
        ang = i * 0.524 - math.pi
        rv = 10 + rnd.randint(-2, 4) + int(math.sin(i * 1.5 + seed) * 3) + pulse
        if i < 4:
            rv += 4
        x = 16 + int(rv * math.cos(ang))
        y = 16 + int(rv * math.sin(ang))
        pts.append((x, y))
    fill_poly(draw, pts, c)
    pts2 = []
    for i in range(10):
        ang = i * 0.628 - math.pi
        rv = 5 + rnd.randint(-1, 2) + pulse // 2
        x = 16 + int(rv * math.cos(ang))
        y = 16 + int(rv * math.sin(ang))
        pts2.append((x, y))
    fill_poly(draw, pts2, lc)
    core_clr = (255, 255, 255, 200) if frame != 1 else (255, 200, 50, 200)
    fill_ellipse(draw, 13, 13, 19, 19, core_clr)
    for i in range(3):
        px = 16 + rnd.randint(-14, 14)
        py = 16 + rnd.randint(-14, 14)
        if 0 <= px < 32 and 0 <= py < 32:
            fill_ellipse(draw, px, py, px + 2, py + 2, lc)

def draw_worm(draw, pal, seed, frame=0):
    rnd = random.Random(seed)
    c = pal['base']
    dc = pal['dark']
    lc = pal['light']
    wave = {0: 0, 1: 0.6, 2: -0.6}[frame]
    segs = 6
    for i in range(segs):
        sx = 4 + i * 4 + rnd.randint(-1, 1)
        sy = 16 + int(math.sin(i * 1.2 + seed + wave) * 6)
        sr = 4 + rnd.randint(-1, 1)
        fill_ellipse(draw, sx - sr, sy - sr, sx + sr, sy + sr, dc)
        fill_ellipse(draw, sx - sr + 1, sy - sr + 1, sx + sr - 1, sy + sr - 1, c if i % 2 == 0 else pal['mid'])
    hx = 4 + rnd.randint(-1, 1)
    hy = 16 + int(math.sin(seed + wave) * 6)
    fill_ellipse(draw, hx - 5, hy - 5, hx + 5, hy + 5, c)
    fill_ellipse(draw, hx - 4, hy - 4, hx + 4, hy + 4, lc)
    fill_ellipse(draw, hx - 3, hy - 3, hx - 1, hy - 1, (255, 0, 0))
    fill_ellipse(draw, hx + 1, hy - 3, hx + 3, hy - 1, (255, 0, 0))

def draw_crystal(draw, pal, seed, frame=0):
    rnd = random.Random(seed)
    c = pal['base']
    dc = pal['dark']
    lc = pal['light']
    dy = {0: 0, 1: -1, 2: 1}[frame]
    glow = {0: 150, 1: 220, 2: 100}[frame]
    pts = [(16, 2 + dy), (8, 14 + dy), (12, 28 + dy), (20, 28 + dy), (24, 14 + dy)]
    fill_poly(draw, pts, dc)
    fill_poly(draw, [(16, 3 + dy), (9, 14 + dy), (13, 27 + dy), (19, 27 + dy), (23, 14 + dy)], c)
    fill_poly(draw, [(16, 4 + dy), (11, 14 + dy), (14, 26 + dy), (18, 26 + dy), (22, 14 + dy)], lc)
    fill_poly(draw, [(6, 16 + dy), (3, 24 + dy), (9, 26 + dy)], dc)
    fill_poly(draw, [(7, 17 + dy), (4, 23 + dy), (8, 25 + dy)], c)
    fill_poly(draw, [(26, 12 + dy), (29, 22 + dy), (23, 24 + dy)], dc)
    fill_poly(draw, [(27, 13 + dy), (28, 21 + dy), (24, 23 + dy)], c)
    fill_ellipse(draw, 14, 8 + dy, 18, 12 + dy, (255, 255, 255, glow))

def draw_void(draw, pal, seed, frame=0):
    rnd = random.Random(seed)
    c = pal['base']
    dc = pal['dark']
    lc = pal['light']
    wave = {0: 0, 1: 1.5, 2: -1.5}[frame]
    pts = []
    for i in range(14):
        ang = i * 0.448 - math.pi
        rv = 8 + rnd.randint(-2, 6) + abs(int(math.sin(i * 2 + seed + wave) * 5))
        x = 16 + int(rv * math.cos(ang))
        y = 16 + int(rv * math.sin(ang))
        pts.append((x, y))
    fill_poly(draw, pts, dc)
    fill_poly(draw, [(x, y) for i, (x, y) in enumerate(pts) if i % 2 == 0], c)
    fill_ellipse(draw, 11, 11, 21, 21, (0, 0, 0, 200))
    eye_clr = (255, 0, 100) if frame != 1 else (200, 0, 200)
    fill_ellipse(draw, 12, 14, 15, 17, eye_clr)
    fill_ellipse(draw, 17, 14, 20, 17, eye_clr)
    for i in range(3):
        wx = 16 + rnd.randint(-12, 12)
        wy = 16 + rnd.randint(-12, 12)
        fill_ellipse(draw, wx, wy, wx + 2, wy + 2, lc)

def draw_dragon(draw, pal, seed, frame=0):
    rnd = random.Random(seed)
    c = pal['base']
    dc = pal['dark']
    lc = pal['light']
    dy = {0: 0, 1: -1, 2: 1}[frame]
    wing_wave = {0: 0, 1: -3, 2: 2}[frame]
    fill_ellipse(draw, 8, 12 + dy, 24, 24 + dy, dc)
    fill_ellipse(draw, 9, 13 + dy, 23, 23 + dy, c)
    fill_ellipse(draw, 4, 6 + dy, 14, 16 + dy, dc)
    fill_ellipse(draw, 5, 7 + dy, 13, 15 + dy, c)
    fill_rect(draw, 8, 10 + dy, 14, 16 + dy, dc)
    fill_rect(draw, 9, 11 + dy, 13, 15 + dy, c)
    fill_poly(draw, [(14, 14 + dy), (30, 4 + dy + wing_wave), (28, 14 + dy)], pal['mid'])
    fill_poly(draw, [(14, 16 + dy), (30, 8 + dy + wing_wave), (28, 16 + dy)], dc)
    fill_poly(draw, [(14, 18 + dy), (30, 18 + dy + wing_wave), (28, 22 + dy)], pal['mid'])
    fill_poly(draw, [(14, 20 + dy), (30, 22 + dy + wing_wave), (28, 24 + dy)], dc)
    fill_ellipse(draw, 6, 9 + dy, 8, 11 + dy, (255, 200, 50))
    fill_ellipse(draw, 7, 10 + dy, 8, 11 + dy, (255, 0, 0))
    fill_poly(draw, [(4, 13 + dy), (2, 18 + dy), (10, 16 + dy)], dc)
    fill_rect(draw, 3, 15 + dy, 8, 17 + dy, (255, 80, 80))
    fill_ellipse(draw, 22, 18 + dy, 30, 24 + dy, dc)

def draw_golem(draw, pal, seed, frame=0):
    rnd = random.Random(seed)
    c = pal['base']
    dc = pal['dark']
    lc = pal['light']
    dy = {0: 0, 1: -1, 2: 1}[frame]
    fill_rect(draw, 6, 10 + dy, 26, 26 + dy, dc)
    fill_rect(draw, 7, 11 + dy, 25, 25 + dy, c)
    fill_rect(draw, 8, 12 + dy, 24, 24 + dy, pal['mid'])
    fill_rect(draw, 10, 3 + dy, 22, 11 + dy, dc)
    fill_rect(draw, 11, 4 + dy, 21, 10 + dy, c)
    eye_clr = (255, 100, 0) if frame != 1 else (255, 200, 100)
    fill_rect(draw, 12, 5 + dy, 14, 7 + dy, eye_clr)
    fill_rect(draw, 18, 5 + dy, 20, 7 + dy, eye_clr)
    fill_rect(draw, 13, 8 + dy, 19, 9 + dy, dc)
    fill_rect(draw, 3, 12 + dy, 6, 24 + dy, dc)
    fill_rect(draw, 4, 13 + dy, 5, 23 + dy, c)
    fill_rect(draw, 26, 12 + dy, 29, 24 + dy, dc)
    fill_rect(draw, 27, 13 + dy, 28, 23 + dy, c)
    fill_rect(draw, 9, 26 + dy, 14, 31 + dy, dc)
    fill_rect(draw, 18, 26 + dy, 23, 31 + dy, dc)

def draw_spider(draw, pal, seed, frame=0):
    rnd = random.Random(seed)
    c = pal['base']
    dc = pal['dark']
    lc = pal['light']
    dy = {0: 0, 1: -1, 2: 1}[frame]
    fill_ellipse(draw, 8, 10 + dy, 24, 24 + dy, dc)
    fill_ellipse(draw, 9, 11 + dy, 23, 23 + dy, c)
    fill_ellipse(draw, 10, 12 + dy, 22, 22 + dy, lc)
    fill_ellipse(draw, 10, 6 + dy, 22, 14 + dy, dc)
    fill_ellipse(draw, 11, 7 + dy, 21, 13 + dy, c)
    eye_clr = (255, 0, 0)
    for ex, ey in [(12, 8), (14, 8), (18, 8), (20, 8)]:
        fill_ellipse(draw, ex, ey + dy, ex + 1, ey + 1 + dy, eye_clr)
    leg_wave = {0: 0, 1: -2, 2: 2}[frame]
    for i in range(4):
        for side in [-1, 1]:
            lx = 16 + side * (8 + i * 2) + leg_wave // 2
            ly = 18 + i * 3 + dy + leg_wave
            lx2 = lx + side * 4
            fill_rect(draw, min(lx, lx2), ly, max(lx, lx2), ly + 1, dc)

def draw_ghost(draw, pal, seed, frame=0):
    rnd = random.Random(seed)
    c = pal['base']
    dc = pal['dark']
    lc = pal['light']
    wave = {0: 0, 1: -2, 2: 2}[frame]
    pts = [(6, 8 + wave), (6, 24), (8, 28), (10, 24 + wave // 2), (12, 28),
           (14, 24 + wave), (16, 28), (18, 24 + wave // 2), (20, 28),
           (22, 24 + wave), (24, 28), (26, 24 + wave), (26, 8 + wave)]
    fill_poly(draw, pts, dc)
    pts2 = [(7, 9 + wave), (7, 23), (9, 27), (11, 23 + wave // 2), (13, 27),
            (15, 23 + wave), (17, 27), (19, 23 + wave // 2), (21, 27),
            (23, 23), (25, 27 + wave), (25, 9 + wave)]
    fill_poly(draw, pts2, c)
    eye_state = {0: 0, 1: 2, 2: 0}[frame]
    fill_ellipse(draw, 10, 12 + wave, 13, 15 + wave + eye_state, (0, 0, 0))
    fill_ellipse(draw, 19, 12 + wave, 22, 15 + wave + eye_state, (0, 0, 0))
    fill_ellipse(draw, 11, 13 + wave, 12, 14 + wave, (255, 255, 255))
    fill_ellipse(draw, 20, 13 + wave, 21, 14 + wave, (255, 255, 255))
    fill_ellipse(draw, 13, 18 + wave, 19, 21 + wave, (0, 0, 0))

def draw_skull(draw, pal, seed, frame=0):
    rnd = random.Random(seed)
    c = pal['base']
    dc = pal['dark']
    lc = pal['light']
    dy = {0: 0, 1: -1, 2: 1}[frame]
    fill_ellipse(draw, 6, 4 + dy, 26, 20 + dy, dc)
    fill_ellipse(draw, 7, 5 + dy, 25, 19 + dy, c)
    fill_ellipse(draw, 8, 6 + dy, 24, 18 + dy, lc)
    fill_poly(draw, [(8, 16 + dy), (6, 28 + dy), (14, 26 + dy), (16, 28 + dy), (18, 26 + dy), (26, 28 + dy), (24, 16 + dy)], dc)
    fill_poly(draw, [(9, 17 + dy), (7, 27 + dy), (14, 25 + dy), (16, 27 + dy), (18, 25 + dy), (25, 27 + dy), (23, 17 + dy)], c)
    fill_ellipse(draw, 9, 10 + dy, 14, 15 + dy, (0, 0, 0))
    fill_ellipse(draw, 18, 10 + dy, 23, 15 + dy, (0, 0, 0))
    glow = (255, 0, 0, 200) if frame != 1 else (255, 100, 100, 200)
    fill_ellipse(draw, 10, 11 + dy, 13, 14 + dy, glow)
    fill_ellipse(draw, 19, 11 + dy, 22, 14 + dy, glow)
    fill_poly(draw, [(14, 15 + dy), (16, 15 + dy), (15, 18 + dy)], (0, 0, 0))
    fill_rect(draw, 10, 20 + dy, 13, 22 + dy, lc)
    fill_rect(draw, 15, 20 + dy, 17, 22 + dy, dc)
    fill_rect(draw, 18, 20 + dy, 21, 22 + dy, lc)

SHAPE_DRAWERS = {
    SHAPE_BLOB: draw_blob, SHAPE_HUMANOID: draw_humanoid,
    SHAPE_BEAST: draw_beast, SHAPE_EYE: draw_eye,
    SHAPE_TENTACLE: draw_tentacle, SHAPE_MACHINE: draw_machine,
    SHAPE_ELEMENTAL: draw_elemental, SHAPE_WORM: draw_worm,
    SHAPE_CRYSTAL: draw_crystal, SHAPE_VOID: draw_void,
    SHAPE_DRAGON: draw_dragon, SHAPE_GOLEM: draw_golem,
    SHAPE_SPIDER: draw_spider, SHAPE_GHOST: draw_ghost,
    SHAPE_SKULL: draw_skull,
}

def generate(enemy_data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total = 0
    for tid, data in enemy_data.items():
        name = data['name']
        color = data.get('color', '#888888')
        rgb = hex_to_rgb(color)
        pal = palette(rgb)
        seed = hash(tid) & 0x7FFFFFFF
        shape_type = classify_shape(name)
        drawer = SHAPE_DRAWERS.get(shape_type, draw_humanoid)
        for frame in range(3):
            img = make_img()
            draw = ImageDraw.Draw(img)
            drawer(draw, pal, seed, frame=frame)
            path = os.path.join(OUTPUT_DIR, f'{tid}_{frame}.png')
            img.save(path, 'PNG')
            total += 1
    print(f'Generated {total} frames for {len(enemy_data)} enemies in {OUTPUT_DIR}')

if __name__ == '__main__':
    with open('enemy_data.json', 'r', encoding='utf-8') as f:
        enemy_data = json.load(f)
    generate(enemy_data)
