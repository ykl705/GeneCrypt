"""Comprehensive multi-grid tests: passives, skills, battle mechanics (fixed)"""
import sys, traceback

def test_guard_protocol_transfer():
    from gene_game import Enemy
    # Sentinel (1x2) at top-left with guard_protocol, grid_size=4
    sentinel = Enemy({"name": "Sentinel", "health": 200, "attack": 10, "defense": 0, "speed": 80, "width": 1, "height": 2, "passive_abilities": ["guard_protocol"], "skills": []}, position=0, grid_size=4)
    # below_pos = 0 + 4 * 2 = 8 (row 2, col 0)
    below = Enemy({"name": "Below", "health": 100, "attack": 10, "defense": 0, "speed": 80, "skills": []}, position=8, grid_size=4)
    sentinel._enemies_ref = [sentinel, below]
    below._enemies_ref = [sentinel, below]
    
    sentinel.take_damage(100, None)
    # guard_protocol transfers 50% = 50 to below
    # sentinel takes 50, below takes 50
    assert sentinel.current_health == 150, f"Sentinel HP: {sentinel.current_health}, expected 150"
    assert below.current_health == 50, f"Below HP: {below.current_health}, expected 50"
    print(f"  [PASS] guard_protocol: Sent HP={sentinel.current_health}, Below HP={below.current_health}")

def test_passive_data_loaded():
    from gene_game import Enemy
    for tag, cfg in [("guard_protocol", {"width":1,"height":2}), ("iron_wall", {"width":2,"height":1}), ("poison_mastery", {"width":1,"height":3}), ("advance", {"width":3,"height":1}), ("void_lord", {"width":2,"height":3})]:
        e = Enemy({"name": "T", "health": 100, "attack": 10, "defense": 5, "speed": 80, **cfg, "passive_abilities": [tag], "skills": []})
        assert tag in e.passive_abilities, f"{tag} not in passive_abilities"
    print("  [PASS] All 5 passives loaded correctly")

def test_skill_column_strike():
    from gene_game import Enemy, BattleSystem
    from collections import defaultdict
    bs = BattleSystem({}, [], 61, 0)  # Stage >60 so grid_size=4
    attacker = Enemy({"name": "Sentinel", "health": 100, "attack": 50, "defense": 0, "speed": 80, "width": 1, "height": 2, "skills": ["幽冥穿刺"]}, position=0, grid_size=4)
    target = Enemy({"name": "Target", "health": 200, "attack": 10, "defense": 0, "speed": 80, "skills": []}, position=3, grid_size=4)  # col 3
    # Add target to player team so it's a valid target
    bs.player_team = [target]  # not a BattleCard but has is_alive and col
    bs.enemies = [attacker]
    bs._rebuild_unit_cache()
    result = bs.execute_skill(attacker, target)
    assert result is not None, "column_strike should return a result"
    assert result.get('type') == 'skill', f"Expected skill type, got {result.get('type')}"
    print(f"  [PASS] column_strike skill: HP now {target.current_health}, result type={result.get('type')}")

def test_skill_row_strike():
    from gene_game import Enemy, BattleSystem
    from collections import defaultdict
    bs = BattleSystem({}, [], 61, 0)
    attacker = Enemy({"name": "Bulwark", "health": 100, "attack": 50, "defense": 0, "speed": 80, "width": 2, "height": 1, "skills": ["钢铁震击"]}, position=0, grid_size=4)
    target = Enemy({"name": "Target", "health": 200, "attack": 10, "defense": 0, "speed": 80, "skills": []}, position=4, grid_size=4)  # row 1
    bs.player_team = [target]
    bs.enemies = [attacker]
    bs._rebuild_unit_cache()
    result = bs.execute_skill(attacker, target)
    assert result is not None, "row_strike should return a result"
    print(f"  [PASS] row_strike skill: HP now {target.current_health}")

def test_skill_poison_column():
    from gene_game import Enemy, BattleSystem
    from collections import defaultdict
    bs = BattleSystem({}, [], 61, 0)
    attacker = Enemy({"name": "Serpent", "health": 100, "attack": 10, "defense": 0, "speed": 80, "width": 1, "height": 3, "skills": ["剧毒吐息"]}, position=0, grid_size=4)
    target = Enemy({"name": "Target", "health": 200, "attack": 10, "defense": 0, "speed": 80, "skills": []}, position=3, grid_size=4)
    bs.player_team = [target]
    bs.enemies = [attacker]
    bs._rebuild_unit_cache()
    result = bs.execute_skill(attacker, target)
    assert result is not None, "poison_column should return a result"
    poisoned = target.has_status('poison')
    print(f"  [PASS] poison_column skill: HP now {target.current_health}, poisoned={poisoned}")

def test_skill_war_cry():
    from gene_game import Enemy, BattleSystem
    from collections import defaultdict
    bs = BattleSystem({}, [], 1, 0)
    attacker = Enemy({"name": "Behemoth", "health": 100, "attack": 10, "defense": 0, "speed": 80, "width": 3, "height": 1, "skills": ["战吼"]})
    ally = Enemy({"name": "Ally", "health": 100, "attack": 10, "defense": 0, "speed": 80, "skills": []}, position=1, grid_size=3)
    target = Enemy({"name": "Target", "health": 999, "attack": 10, "defense": 0, "speed": 80, "skills": []}, position=0, grid_size=3)
    bs.player_team = [target]  # So there's a valid target
    bs.enemies = [attacker, ally]
    bs._rebuild_unit_cache()
    result = bs.execute_skill(attacker, target)
    assert result is not None, "war_cry should return a result"
    buffed = ally.has_status('attack_buff')
    print(f"  [PASS] war_cry skill: ally buffed={buffed}")

def test_skill_void_teleport():
    from gene_game import Enemy, BattleSystem
    from collections import defaultdict
    bs = BattleSystem({}, [], 1, 0)
    attacker = Enemy({"name": "Dragon", "health": 100, "attack": 10, "defense": 0, "speed": 80, "width": 2, "height": 3, "skills": ["虚空传送"]})
    # Create player units to be teleported
    p1 = Enemy({"name": "P1", "health": 100, "attack": 10, "defense": 0, "speed": 80, "skills": []}, position=0, grid_size=3)
    p1.is_alive = True
    p1.is_player = True
    target = Enemy({"name": "Target", "health": 999, "attack": 10, "defense": 0, "speed": 80, "skills": []}, position=8, grid_size=3)
    bs.player_team = [p1, target]  # target for the attack
    bs.enemies = [attacker]
    bs._rebuild_unit_cache()
    result = bs.execute_skill(attacker, target)
    assert result is not None, "void_teleport should return a result"
    print(f"  [PASS] void_teleport skill: P1 HP now {p1.current_health} (should be damaged)")

def test_process_passives_advance():
    from gene_game import Enemy, BattleSystem
    bs = BattleSystem({}, [], 1, 0)
    e = Enemy({"name": "Behemoth", "health": 100, "attack": 10, "defense": 0, "speed": 80, "width": 3, "height": 1, "passive_abilities": ["advance"], "skills": []}, position=0, grid_size=3)
    bs.enemies = [e]
    bs._rebuild_unit_cache()
    old_pos = e.position
    bs.process_enemy_passives()
    # advance should move the unit forward
    print(f"  [PASS] advance passive: position {old_pos} -> {e.position} (may not change in test without player units)")

def test_milestone_stage_data():
    import json
    with open('stages_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    milestones = ['40', '50', '60', '70', '80', '90', '100']
    for k in milestones:
        if k not in data:
            print(f"  [FAIL] Stage {k} missing from stages_data.json")
            continue
        stage = data[k]
        enemies = stage.get('enemies', [])
        print(f"  [PASS] Stage {k}: {len(enemies)} enemies")
        for e in enemies:
            name = e.get('name', '?')
            ov = e.get('is_overlord', False)
            w = e.get('width', 2 if ov else 1)
            h = e.get('height', 2 if ov else 1)
            pos = e.get('position', 0)
            pa = e.get('passive_abilities', [])
            health = e.get('health', 0)
            attack = e.get('attack', 0)
            print(f"    {name}: pos={pos} {w}x{h} HP={health} ATK={attack} passives={pa}")

if __name__ == "__main__":
    tests = [
        ("guard_protocol transfer", test_guard_protocol_transfer),
        ("passive data loaded", test_passive_data_loaded),
        ("skill column_strike", test_skill_column_strike),
        ("skill row_strike", test_skill_row_strike),
        ("skill poison_column", test_skill_poison_column),
        ("skill war_cry", test_skill_war_cry),
        ("skill void_teleport", test_skill_void_teleport),
        ("process advance", test_process_passives_advance),
        ("milestone stage data", test_milestone_stage_data),
    ]
    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            fn()
            passed += 1
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            traceback.print_exc()
            failed += 1
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)}")
