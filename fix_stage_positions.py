"""Final fix: restore milestone stage positions + set enemy_grid_size=4.
Stages 40 and 50 lost enemies in previous fixes - reconstruct them properly."""
import json
import copy

with open('stages_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

from battle_config import STAGES, MILESTONE_BONUS, ENEMY_TEMPLATES

# Stage configs: (grid_size, [enemy_template_keys], [multi_grid_additions])
STAGE_CONFIGS = {
    40: (4, ['commander', 'war_drummer', 'guardian_spirit', 'corruption_source', 'devourer'],
         [{'template': 'shadow_sentinel', 'extra_hp': 1.2, 'extra_atk': 1.2}]),
    50: (4, ['devourer', 'devourer', 'gene_fusion', 'gene_fusion', 'void_overlord'],
         [{'template': 'iron_bulwark', 'extra_hp': 1.4, 'extra_atk': 1.4}]),
}

def build_enemy_from_template(tkey, sn, extra_hp=1.0, extra_atk=1.0):
    if sn <= 60:
        health_scale = 1 + (sn - 1) * 0.18
        stat_scale = 1 + (sn - 1) * 0.12
    else:
        health_scale = 1 + 59 * 0.18 + (sn - 60) * 0.10
        stat_scale = 1 + 59 * 0.12 + (sn - 60) * 0.08
    t = ENEMY_TEMPLATES[tkey]
    e = {
        'name': t['name'],
        'health': int(t['base_health'] * health_scale * extra_hp),
        'attack': int(t['base_attack'] * stat_scale * extra_atk),
        'defense': int(t['base_defense'] * stat_scale),
        'speed': int(t['base_speed'] * stat_scale),
        'skills': [],
        'reward_exp': 10 + sn * 8,
        'passive_abilities': list(t.get('passive_abilities', [])),
    }
    # Overlord/multi-grid flags
    w = t.get('width', 2 if tkey in ('devourer', 'overlord', 'void_overlord', 'abyss_lord') else 1)
    h = t.get('height', 2 if tkey in ('devourer', 'overlord', 'void_overlord', 'abyss_lord') else 1)
    if w > 1 or h > 1:
        e['width'] = w
        e['height'] = h
    return e

def apply_milestone_bonus(e, sn):
    bonus = MILESTONE_BONUS.get(sn, 1.0)
    e['health'] = int(e['health'] * bonus)
    e['attack'] = int(e['attack'] * bonus)
    return e

def place_enemies(enemies, grid_size):
    multi = [e for e in enemies if e.get('width', 1) > 1 or e.get('height', 1) > 1]
    single = [e for e in enemies if e.get('width', 1) == 1 and e.get('height', 1) == 1]
    multi.sort(key=lambda e: -(e.get('width', 1) * e.get('height', 1)))
    occupied = set()
    placed = []
    for e in multi:
        w, h = e['width'], e['height']
        found = False
        for pos in range(grid_size * grid_size):
            r = pos // grid_size
            c = pos % grid_size
            if c + w > grid_size or r + h > grid_size:
                continue
            cells = [pos + wi + hi * grid_size for hi in range(h) for wi in range(w)]
            if not any(p in occupied for p in cells):
                e['position'] = pos
                for p in cells:
                    occupied.add(p)
                placed.append(e)
                found = True
                break
        if not found:
            print(f"  DROP: {e['name']} ({w}x{h})")
    for e in single:
        e.pop('position', None)
        placed.append(e)
    return placed

# Rebuild stages 40 and 50 from scratch
for sn, (gs, template_keys, additions) in STAGE_CONFIGS.items():
    enemies = []
    for tkey in template_keys:
        e = build_enemy_from_template(tkey, sn)
        e = apply_milestone_bonus(e, sn)
        enemies.append(e)
    for add in additions:
        tkey = add['template']
        e = build_enemy_from_template(tkey, sn, add.get('extra_hp', 1.0), add.get('extra_atk', 1.0))
        e = apply_milestone_bonus(e, sn)
        enemies.append(e)
    
    sk = str(sn)
    stage = data.get(sk, {})
    stage['name'] = stage.get('name', STAGES[sn]['name'])
    stage['enemy_grid_size'] = gs
    placed = place_enemies(enemies, gs)
    stage['enemies'] = placed
    data[sk] = stage
    
    # Verify
    occupied = set()
    for e in placed:
        pos = e.get('position')
        if pos is None:
            continue
        w = e.get('width', 1)
        h = e.get('height', 1)
        cells = [pos + wi + hi * gs for hi in range(h) for wi in range(w)]
        overlaps = [p for p in cells if p in occupied]
        if overlaps:
            print(f"  CONFLICT Stage {sn}: {e['name']}@{pos} overlaps {overlaps}")
        for p in cells:
            occupied.add(p)
    print(f"Stage {sn}: {len(placed)} enemies, {len(occupied)}/{gs*gs} cells (grid={gs}x{gs})")

# Fix positions for stages 60-100 (keep existing enemies, fix positions, add grid_size)
for sn in [60, 70, 80, 90, 100]:
    sk = str(sn)
    if sk not in data:
        continue
    stage = data[sk]
    enemies = stage.get('enemies', [])
    stage['enemy_grid_size'] = 4
    placed = place_enemies(enemies, 4)
    stage['enemies'] = placed
    occupied = set()
    for e in placed:
        pos = e.get('position')
        if pos is None:
            continue
        w = e.get('width', 1)
        h = e.get('height', 1)
        cells = [pos + wi + hi * 4 for hi in range(h) for wi in range(w)]
        overlaps = [p for p in cells if p in occupied]
        if overlaps:
            print(f"  CONFLICT Stage {sn}: {e['name']}@{pos} overlaps {overlaps}")
        for p in cells:
            occupied.add(p)
    print(f"Stage {sn}: {len(placed)} enemies, {len(occupied)}/16 cells")

with open('stages_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("\nSaved stages_data.json")
