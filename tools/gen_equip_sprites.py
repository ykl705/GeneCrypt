"""Generate pixel art equipment sprites using Pillow."""
import os, struct

COLORS = {
    'common':   [(128,128,128),(160,160,160),(192,192,192)],
    'uncommon': [(30,180,30),(50,200,50),(20,150,20)],
    'rare':     [(40,80,220),(60,120,255),(30,50,180)],
    'epic':     [(160,30,220),(200,80,255),(130,20,180)],
    'legend':   [(255,140,0),(255,180,50),(200,100,0)],
    'ancient':  [(200,150,50),(240,180,80),(160,100,20)],
    'mythic':   [(40,220,220),(80,255,255),(20,180,180)],
    'chaos':    [(255,20,80),(255,120,30),(200,255,50),(80,120,255)],
}

SLOT_PATTERNS = {
    'weapon':    [0,0,0,0,0,0,1,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,2,0,0,0,1,0,0,0,2,0],
    'head':      [0,0,1,1,1,0,0,0,1,2,1,0,0,1,2,2,2,1,0,0,2,2,2,0,0,0,0,0,0,0,0,0],
    'body':      [0,1,1,1,1,1,0,0,1,2,1,0,0,1,2,2,2,1,0,1,2,2,2,2,1,0,1,2,2,2,1,0],
    'accessory': [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,2,0,0,0,0,2,2,2,0,0,0,2,0,2,0,0,0],
    'boots':     [0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,2,1,0,0,0,1,2,2,1,0,0,1,2,1,0,0,0],
    'special':   [0,0,0,1,0,0,0,0,1,2,1,0,0,0,1,2,2,1,0,0,1,2,1,0,0,0,0,1,0,0,0,0],
}

try:
    from PIL import Image
    os.makedirs('assets/equipment', exist_ok=True)
    size = 16
    scale = 2
    for slot, pattern in SLOT_PATTERNS.items():
        for rarity, palette in COLORS.items():
            img = Image.new('RGBA', (size, size), (0,0,0,0))
            px = img.load()
            for i in range(size):
                for j in range(size):
                    idx = (j//(size//4))*4 + (i//(size//4))
                    if idx < 32:
                        v = pattern[idx]
                        if v > 0:
                            c = palette[v-1] if v <= len(palette) else palette[-1]
                            if rarity == 'chaos':
                                c = palette[(i+j)%4]
                            px[i, size-1-j] = (*c, 255)
            big = img.resize((size*scale, size*scale), Image.NEAREST)
            if rarity in ('legend', 'ancient', 'mythic', 'chaos'):
                glow = Image.new('RGBA', (size*scale+4, size*scale+4), (0,0,0,0))
                for x in range(glow.width):
                    for y in range(glow.height):
                        edge = (x<2 or x>=glow.width-2 or y<2 or y>=glow.height-2)
                        if edge:
                            gc = palette[0] if rarity != 'chaos' else palette[(x+y)//4%4]
                            glow.putpixel((x,y), (*gc, 120))
                combined = Image.new('RGBA', (size*scale+4, size*scale+4), (0,0,0,0))
                combined.paste(glow, (0,0))
                combined.paste(big, (2,2), big)
                combined.save(f'assets/equipment/{slot}_{rarity}.png')
            else:
                big.save(f'assets/equipment/{slot}_{rarity}.png')
    print('Generated', 6*8, 'equipment sprites')
except ImportError:
    print('Pillow not available, skipping sprite generation')
except Exception as e:
    print(f'Sprite gen error: {e}')
