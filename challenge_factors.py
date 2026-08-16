# ============================================================
# 挑战因子引擎 - 118个主题挑战因子的战斗效果
# 由 BattleSystem 调用：apply_pre_battle / on_enemy_action /
# process_deaths / process_tick / try_spawn_next_wave
# ============================================================
import random
import time

FORMATIONS = ('field_expand', 'elem_expand', 'bb_expand')
TEAM3 = ('team_3', 'bb_team_3')
TEAM4 = ('team_4', 'bb_team_4')

ELEMENTAL_KEYS = ('elem_fire', 'elem_ice', 'elem_thunder', 'elem_earth', 'elem_magma',
                  'elem_crystal', 'elem_storm', 'elem_metal', 'elem_nature', 'elem_light',
                  'elem_dark', 'elem_steam', 'elem_mud', 'elem_lava_beast', 'elem_cyclone',
                  'elem_aurora', 'elem_prism', 'elem_fusion', 'elem_primordial', 'elem_boss')

ELEM_STATUS = {
    'elem_fire': 'burn', 'elem_magma': 'burn', 'elem_lava_beast': 'burn',
    'elem_ice': 'freeze', 'elem_crystal': 'freeze',
    'elem_thunder': 'paralyze', 'elem_storm': 'paralyze',
    'elem_dark': 'curse',
    'elem_nature': 'poison',
}
ELEMENTAL_STATUSES = ('burn', 'freeze', 'paralyze', 'curse', 'poison', 'sleep', 'confuse')

BLIND_BOX_MONSTER_POOL = ['basic', 'soldier', 'mutant', 'elite', 'scout', 'flame_guard',
                          'venom_stalker', 'phantom_assassin', 'iron_fortress', 'gene_fusion']
RANDOM_PASSIVE_POOL = ['regeneration', 'thick_skin', 'sharp_claw', 'swift', 'vampiric', 'thorns']


def _has(bs, *ids):
    return any(i in bs._factor_ids for i in ids)


def _scale_for_stage(stage_num):
    if stage_num <= 100:
        n = stage_num - 1
        return 1 + n * 0.05 + n * n * 0.0003, 1 + n * 0.04 + n * n * 0.0002
    n = stage_num - 100
    return 1 + n * 0.15 + n * n * 0.002, 1 + n * 0.12 + n * n * 0.0015


def _mk_enemy_data(bs, template_key, scale=1.0, skills=None, position=None, extra=None):
    from battle_config import ENEMY_TEMPLATES
    tmpl = ENEMY_TEMPLATES.get(template_key)
    if not tmpl:
        return None
    hp_s, st_s = _scale_for_stage(bs.stage_num)
    data = {
        'name': tmpl['name'],
        'health': int(tmpl['base_health'] * hp_s * scale),
        'attack': int(tmpl['base_attack'] * st_s * scale),
        'defense': int(tmpl['base_defense'] * st_s * scale),
        'speed': int(tmpl['base_speed'] * st_s * scale),
        'skills': skills if skills is not None else list(tmpl.get('skills_pool', [])[:max(1, tmpl.get('min_skills', 0))]),
        'passive_abilities': list(tmpl.get('passive_abilities', [])),
        'width': tmpl.get('width', 1),
        'height': tmpl.get('height', 1),
        'annihilate': tmpl.get('annihilate', False),
        'immune_to_debuffs': tmpl.get('immune_to_debuffs', False),
        'purify_interval': tmpl.get('purify_interval', 0),
    }
    if position is not None:
        data['position'] = position
    if extra:
        data.update(extra)
    return data


def spawn_enemy(bs, template_key, position=None, scale=1.0, skills=None, extra=None, name=None):
    from gene_game import Enemy
    data = _mk_enemy_data(bs, template_key, scale=scale, skills=skills, position=position, extra=extra)
    if not data:
        return None
    if name:
        data['name'] = name
    gs = bs.enemy_grid_size
    pos = position if position is not None else _find_free_pos(bs)
    if pos is None or pos < 0 or pos >= gs * gs:
        return None
    occupied = set()
    for e in bs.enemies:
        if e.is_alive:
            for op in getattr(e, 'occupied_positions', [e.position]):
                occupied.add(op)
    if pos in occupied:
        return None
    data['position'] = pos
    try:
        enemy = Enemy(data, position=pos, grid_size=gs)
    except Exception:
        return None
    _on_spawn(bs, enemy)
    bs.enemies.append(enemy)
    enemy._enemies_ref = bs.enemies
    bs._rebuild_unit_cache()
    return enemy


def _find_free_pos(bs):
    gs = bs.enemy_grid_size
    occupied = set()
    for e in bs.enemies:
        if e.is_alive:
            for op in getattr(e, 'occupied_positions', [e.position]):
                occupied.add(op)
    for p in range(gs * gs):
        if p not in occupied:
            return p
    return None


def _on_spawn(bs, enemy):
    ids = bs._factor_ids
    enemy._spawn_attrs = {'base_atk': enemy.attack, 'base_hp': enemy.max_health,
                          'base_spd': enemy.speed, 'base_def': enemy.defense, 't': 0}
    if 'bb_rnd_stat' in ids:
        kind = random.choice(['hp', 'atk', 'spd', 'def'])
        if kind == 'hp':
            enemy.max_health = int(enemy.max_health * 1.3)
            enemy.current_health = enemy.max_health
        elif kind == 'atk':
            enemy.attack = int(enemy.attack * 1.3)
        elif kind == 'spd':
            enemy.speed = int(enemy.speed * 1.3)
        else:
            enemy.defense = int(enemy.defense * 1.3)
        enemy._rnd_stat = kind
    if 'bb_rnd_skill' in ids or 'bb_double_rnd' in ids:
        from battle_config import SKILL_EFFECTS
        pool = [s for s in SKILL_EFFECTS if s not in ('召唤', '观星', '澎湃', '亡灵复苏', '时光倒流')]
        n = 2 if 'bb_double_rnd' in ids else 1
        for _ in range(n):
            s = random.choice(pool)
            if s not in enemy.skills:
                enemy.skills.append(s)
    if 'bb_rnd_passive' in ids or 'bb_double_rnd' in ids:
        n = 2 if 'bb_double_rnd' in ids else 1
        for _ in range(n):
            pa = random.choice(RANDOM_PASSIVE_POOL)
            if pa not in enemy.passive_abilities:
                enemy.passive_abilities.append(pa)
    if 'swarm_stack' in ids and '圣甲虫' in enemy.name:
        enemy._swarm_stack = 3
        enemy._swarm_base_hp = max(1, enemy.max_health // 3)
        enemy.max_health = enemy._swarm_base_hp * 3
        enemy.current_health = enemy.max_health
        enemy._swarm_base_name = enemy.name
        enemy._swarm_base_atk = enemy.attack
        enemy._swarm_base_spd = enemy.speed
        enemy._update_swarm_display()
    if 'elem_resistance' in ids or 'elem_domain' in ids:
        key = getattr(enemy, 'template_key', '')
        if key in ELEMENTAL_KEYS:
            if 'elem_domain' in ids:
                enemy._elem_immune = set(ELEMENTAL_STATUSES)
            else:
                st = ELEM_STATUS.get(key)
                enemy._elem_immune = {st} if st else set()
    if 'elem_cycle_fire' in ids and '烈焰元素' in enemy.name:
        enemy._revive_as = ('elem_ice', '冰川元素')
    if 'elem_cycle_ice' in ids and '冰川元素' in enemy.name:
        enemy._revive_as = ('elem_earth', '大地元素')
    if 'elem_cycle_earth' in ids and '大地元素' in enemy.name:
        enemy._revive_as = ('elem_thunder', '雷霆元素')
    if 'elem_cycle_thunder' in ids and '雷霆元素' in enemy.name:
        enemy._revive_as = ('elem_nature', '自然元素')


def _replace_enemy(bs, old_name, new_key):
    from gene_game import Enemy
    for i, e in enumerate(bs.enemies):
        if e.name == old_name and e.is_alive:
            data = _mk_enemy_data(bs, new_key, position=e.position)
            if not data:
                continue
            try:
                ne = Enemy(data, position=e.position, grid_size=bs.enemy_grid_size)
            except Exception:
                continue
            ne.action_bar = e.action_bar
            _on_spawn(bs, ne)
            bs.enemies[i] = ne
            ne._enemies_ref = bs.enemies
            bs.add_log(f'[因子] {old_name} 突变为 {ne.name}!')


def apply_pre_battle(bs):
    ids = bs._factor_ids
    fs = bs._factor_state
    if any(fid in ids for fid in ('iron_formation', 'elem_formation', 'bb_formation')):
        bs._formation_locked = True
        bs.add_log('[因子] 敌方阵型不可打乱!')
    hp_mul = 1.0
    atk_mul = 1.0
    spd_mul = 1.0
    if 'subject_gene_boost' in ids:
        hp_mul *= 1.2
        atk_mul *= 1.2
    if 'subject_super_gene' in ids:
        hp_mul *= 1.4
        atk_mul *= 1.4
    if 'flesh_armor' in ids:
        hp_mul *= 1.5
    if 'steel_armor' in ids:
        hp_mul *= 1.8
    if 'elem_obliteration' in ids:
        atk_mul *= 1.5
    if 'elem_speed_light' in ids:
        spd_mul *= 1.1
    if 'elem_speed_storm' in ids:
        spd_mul *= 1.2
    if hp_mul != 1.0 or atk_mul != 1.0 or spd_mul != 1.0:
        for e in bs.enemies:
            e.max_health = int(e.max_health * hp_mul)
            e.current_health = e.max_health
            e.attack = int(e.attack * atk_mul)
            e.speed = int(e.speed * spd_mul)
        bs.add_log('[因子] 敌人属性已强化!')
    if 'elem_fragile' in ids:
        for p in bs.player_team:
            p.max_health = int(p.max_health * 0.7)
            p.current_health = min(p.current_health, p.max_health)
        bs.add_log('[因子] 我方最大生命值-30%!')

    if 'gene_mutate' in ids:
        _replace_enemy(bs, '野生实验体', 'mutant')
    if 'elite_force' in ids:
        _replace_enemy(bs, '野生实验体', 'elite')
    if 'subject_boss_descent' in ids:
        _replace_enemy(bs, '首领实验体', 'overlord')
        if 'subject_all_mastery' in ids:
            from battle_config import ENEMY_TEMPLATES
            boss_skills = list(ENEMY_TEMPLATES['boss']['skills_pool'])
            for e in bs.enemies:
                if '增强版' in e.name:
                    for s in boss_skills:
                        if s not in e.skills:
                            e.skills.append(s)
    if 'subject_immortal' in ids:
        for e in bs.enemies:
            if '增强版' in e.name:
                e._immortal = True

    if 'elem_summon_primal' in ids:
        spawn_enemy(bs, 'elem_primordial')
    if 'elem_summon_shadow' in ids:
        spawn_enemy(bs, 'elem_dark')
        spawn_enemy(bs, 'elem_light')
    if 'elem_summon_crystal' in ids:
        spawn_enemy(bs, 'elem_crystal')
        spawn_enemy(bs, 'elem_prism')

    if 'boulder_fill' in ids:
        gs = bs.enemy_grid_size
        occupied = set()
        for e in bs.enemies:
            if e.is_alive:
                for op in getattr(e, 'occupied_positions', [e.position]):
                    occupied.add(op)
        filled = 0
        for p in range(gs * gs):
            if p not in occupied:
                rock = spawn_enemy(bs, 'rock', position=p)
                if rock:
                    rock.attack = max(1, rock.attack)
                    rock.speed = max(1, int(bs.enemies[0].speed * 0.5) if bs.enemies else 2)
                    filled += 1
        if filled:
            bs.add_log(f'[因子] 巨石填充了 {filled} 个空格!')
    if 'purify_stone' in ids:
        for e in bs.enemies:
            if '巨石' in e.name and not e.skills:
                e.purify_interval = 90

    if 'bb_balance' in ids and bs.enemies:
        alive = [e for e in bs.enemies if e.is_alive]
        if alive:
            avg_hp = sum(e.max_health for e in alive) // len(alive)
            avg_atk = sum(e.attack for e in alive) // len(alive)
            avg_spd = sum(e.speed for e in alive) // len(alive)
            for e in alive:
                e.max_health = avg_hp
                e.current_health = avg_hp
                e.attack = avg_atk
                e.speed = avg_spd
            bs.add_log('[因子] 所有怪物属性已平均!')

    for e in bs.enemies:
        if e.is_alive:
            _on_spawn(bs, e)

    if 'bb_5_waves' in ids:
        fs['waves'] = [_build_wave(bs, i) for i in range(5)]
        fs['wave'] = 0
        bs.add_log('[因子] 五波攻势：第1波来袭!')

    if 'elem_pact_short' in ids:
        fs['pact_left'] = 4
    elif 'elem_pact_long' in ids:
        fs['pact_left'] = 8
    elif 'elem_pact_eternal' in ids:
        fs['pact_left'] = -1
    fs['dead_processed'] = set()
    fs['elite_evolve'] = 0
    fs['swarm_tick'] = 0
    fs['box_tick'] = 0
    fs['last_hp_snapshot'] = {}
    if 'bb_precharge' in ids and 'waves' in fs:
        fs['precharge_waves'] = {3, 4}
    fs['activated_factors'] = set()


def _build_wave(bs, wave_idx):
    from battle_config import ENEMY_TEMPLATES
    gs = bs.enemy_grid_size
    base_keys = [k for k in ENEMY_TEMPLATES if not ENEMY_TEMPLATES[k].get('immune_to_debuffs', False)]
    wave = []
    scale = 0.7 * (1 + wave_idx * 0.2)
    for i in range(gs * gs):
        key = random.choice(base_keys)
        data = _mk_enemy_data(bs, key, scale=scale, position=i)
        if data:
            wave.append(data)
    return wave


def try_spawn_next_wave(bs):
    fs = bs._factor_state
    waves = fs.get('waves')
    if not waves:
        return False
    if fs.get('wave', 0) < len(waves) - 1:
        fs['wave'] += 1
        bs.enemies = []
        from gene_game import Enemy
        gs = bs.enemy_grid_size
        for i, data in enumerate(waves[fs['wave']]):
            data = dict(data)
            data['position'] = i
            try:
                e = Enemy(data, position=i, grid_size=gs)
            except Exception:
                continue
            _on_spawn(bs, e)
            bs.enemies.append(e)
        for e in bs.enemies:
            e._enemies_ref = bs.enemies
        bs._rebuild_unit_cache()
        bs.winner = None
        bs.add_log(f'[因子] 第{fs["wave"] + 1}波敌人来袭! 状态保留!')
        return True
    return False


def on_enemy_action(bs, enemy, result):
    ids = bs._factor_ids
    fs = bs._factor_state
    if not enemy.is_alive:
        return
    target = result.get('target_obj') if result else None

    if 'void_corrosion' in ids:
        for p in bs.player_team:
            if p.is_alive:
                p.add_status('poison', 3, 10)
        if not fs.get('void_corrosion'):
            fs['void_corrosion'] = True
            bs.add_log('[因子] 虚空蚀化：我方每回合获得中毒!')

    if 'subject_rapid_evolve' in ids and '精英实验体' in enemy.name:
        kind = random.choice(['attack_buff', 'speed_buff', 'defense_buff'])
        if enemy.has_status(kind):
            enemy.status_effects[kind]['value'] = enemy.status_effects[kind].get('value', 10) + 10
            enemy.status_effects[kind]['turns'] = 3
        else:
            d = enemy.add_status(kind, 3)
            if d:
                d['value'] = 10
        bs.add_log(f'[因子] {enemy.name} 快速进化: {kind}+10%!')

    if 'subject_vampiric' in ids and '变异实验体' in enemy.name and result:
        dmg = result.get('damage', 0)
        if dmg > 0:
            enemy.heal(dmg)
    if 'subject_poison_spread' in ids and '变异实验体' in enemy.name and target and target.is_player:
        for p in [u for u in bs.player_team if u.is_alive and u is not target][:2]:
            p.add_status('poison', 3, enemy.attack)
            bs.add_log(f'[因子] 剧毒扩散到 {p.name}!')

    if _has(bs, 'subject_shield_focus', 'subject_shield_boost', 'subject_shield_team') and '守卫实验体' in enemy.name:
        if result and result.get('skill') == '冰霜护盾':
            if 'subject_shield_boost' in ids:
                enemy.shield += enemy.max_health // 4
            if 'subject_shield_team' in ids:
                allies = [e for e in bs.enemies if e.is_alive and e is not enemy]
                if allies:
                    a = random.choice(allies)
                    a.shield += a.max_health // 5
                    bs.add_log(f'[因子] 寒霜庇护了 {a.name}!')

    if 'corrosive_slime' in ids and '腐蚀黏液' in enemy.name and target and target.is_player:
        if target.has_status('speed_buff'):
            target.status_effects['speed_buff']['value'] = target.status_effects['speed_buff'].get('value', 0) - 10
        else:
            target.add_status('speed_buff', 2)
            target.status_effects['speed_buff']['value'] = -10
        bs.add_log(f'[因子] 腐蚀黏液减慢了 {target.name}!')
    if 'eye_poison_tip' in ids and '眼梗怪' in enemy.name and target and target.is_player:
        target.add_status('poison', 2, enemy.attack)
    if 'eye_sniper_ramp' in ids and '眼梗怪' in enemy.name:
        if not getattr(enemy, '_sniped', None):
            enemy._sniped = target
            enemy._snipe_stack = 1
        elif enemy._sniped is target or 'eye_kill_memory' in ids:
            enemy._snipe_stack = getattr(enemy, '_snipe_stack', 0) + 1
            enemy.attack = int(getattr(enemy, '_spawn_attrs', {}).get('base_atk', enemy.attack) * (1 + 0.2 * enemy._snipe_stack))
        else:
            enemy._sniped = target
            enemy._snipe_stack = 1
    if 'eye_dual_lock' in ids and '眼梗怪' in enemy.name:
        alive = [p for p in bs.player_team if p.is_alive and p is not target]
        if alive:
            weak = min(alive, key=lambda p: p.current_health)
            dmg = max(1, enemy.attack // 2)
            weak.take_damage(dmg, enemy)
            bs.add_log(f'[因子] 眼梗怪双瞳锁定 {weak.name}，造成 {dmg} 伤害!')
    if 'eye_death_mark' in ids and '眼梗怪' in enemy.name and target and target.is_player:
        bs.marked_target = target
        bs.add_log(f'[因子] {target.name} 被死亡标记，所有敌人将集火!')

    if 'toxic_miasma' in ids and '毒气泄漏口' in enemy.name:
        for p in bs.player_team:
            if p.is_alive:
                p.add_status('poison', 3, enemy.attack)
        bs.add_log('[因子] 毒瘴笼罩全场!')
    if 'cleaner_absorb' in ids and '清洁机器人' in enemy.name:
        for e in bs.enemies:
            if e.is_alive and e.has_status('poison'):
                stacks = e.status_effects['poison'].get('stacks', 1)
                e.remove_status('poison')
                enemy.heal(stacks * 20)
        bs.add_log('[因子] 清洁机器人回收了毒素!')
    if 'energy_chain' in ids and '应急发电机' in enemy.name:
        gs = bs.enemy_grid_size
        left = enemy.position - 1
        if left >= 0 and enemy.row == left // gs:
            for e in bs.enemies:
                if e.is_alive and e.position == left:
                    e.action_bar = max(e.action_bar, 100)
                    bs.add_log(f'[因子] 发电机充能，{e.name} 立即行动!')
                    break

    if 'subject_summon_ritual' in ids and (getattr(enemy, 'is_overlord', False) or '首领' in enemy.name):
        enemy._ritual_count = getattr(enemy, '_ritual_count', 0) + 1
        if enemy._ritual_count >= 3:
            enemy._ritual_count = 0
            _engine_summon(bs, enemy)
    if 'subject_double_summon' in ids and (getattr(enemy, 'is_overlord', False) or '首领' in enemy.name):
        _engine_summon(bs, enemy)
        _engine_summon(bs, enemy)

    if 'elem_core_extra' in ids and '元素之核' in enemy.name:
        alive_elem = len([e for e in bs.enemies if e.is_alive and '元素' in e.name and e is not enemy])
        depth = getattr(bs, '_extra_action_depth', 0)
        for _ in range(min(alive_elem, 3)):
            if depth < 4 and enemy.is_alive:
                bs._extra_action_depth = depth + 1
                try:
                    bs.execute_enemy_turn(enemy)
                finally:
                    bs._extra_action_depth = depth
    if 'elem_core_scatter' in ids and '元素之核' in enemy.name:
        alive_elem = len([e for e in bs.enemies if e.is_alive and '元素' in e.name and e is not enemy])
        others = [p for p in bs.player_team if p.is_alive and p is not target]
        for p in others[:min(alive_elem, len(others))]:
            dmg = max(1, enemy.attack // 2)
            p.take_damage(dmg, enemy)
            bs.add_log(f'[因子] 核能散射命中 {p.name} ({dmg})!')

    if 'subject_chain_reaction' in ids and (getattr(enemy, 'is_overlord', False) or '首领' in enemy.name):
        depth = getattr(bs, '_extra_action_depth', 0)
        if depth < 3 and enemy.is_alive:
            bs._extra_action_depth = depth + 1
            try:
                bs.execute_enemy_turn(enemy)
            finally:
                bs._extra_action_depth = depth
    if 'subject_full_power' in ids and (getattr(enemy, 'is_overlord', False) or '首领' in enemy.name):
        for s in list(enemy.skills):
            if not enemy.is_alive:
                break
            alive_p = [p for p in bs.player_team if p.is_alive]
            if alive_p:
                bs.execute_skill(enemy, alive_p[0], force_skill=s)
        if enemy.is_alive:
            enemy.attack = int(getattr(enemy, '_spawn_attrs', {}).get('base_atk', enemy.attack))
            bs.execute_enemy_turn(enemy)
    if 'subject_crushing_blow' in ids and '增强版' in enemy.name:
        for p in [u for u in bs.player_team if u.is_alive and u is not target]:
            dmg = max(1, enemy.attack)
            p.take_damage(dmg, enemy)
        bs.add_log(f'[因子] {enemy.name} 碾压全体!')
    if 'subject_full_screen' in ids and '增强版' in enemy.name and result and result.get('type') == 'skill':
        for p in [u for u in bs.player_team if u.is_alive and u is not target]:
            dmg = max(1, enemy.attack // 2)
            p.take_damage(dmg, enemy)
        bs.add_log(f'[因子] {enemy.name} 技能覆盖全场!')

    if 'elem_frenzy' in ids and enemy.skills:
        depth = getattr(bs, '_extra_skill_depth', 0)
        if depth < 2 and enemy.is_alive:
            bs._extra_skill_depth = depth + 1
            try:
                alive_p = [p for p in bs.player_team if p.is_alive]
                if alive_p:
                    s = random.choice(enemy.skills)
                    bs.execute_skill(enemy, alive_p[0], force_skill=s)
            finally:
                bs._extra_skill_depth = depth

    if 'bb_resonance' in ids:
        alive_e = len([e for e in bs.enemies if e.is_alive])
        base = 3 + bs.stage_num // 20
        if 'bb_resonance_amp' in ids:
            boxes = len([e for e in bs.enemies if e.is_alive and getattr(e, '_box', False)])
            base = int(base * (1 + boxes * 0.05))
        if 'bb_resonance_scale' in ids:
            base = int(base * (1 + bs.stage_num * 0.01))
        for p in bs.player_team:
            if p.is_alive:
                dmg = max(1, base + alive_e // 3)
                p.take_damage(dmg)
        bs.add_log(f'[因子] 波次回响冲击全场 ({alive_e}个敌人存活)!')

    if 'elem_assimilation' in ids and target and target.is_player:
        for e in bs.enemies:
            if e.is_alive and '元素' in e.name:
                st = ELEM_STATUS.get(getattr(e, 'template_key', ''))
                if st:
                    if st == 'burn':
                        target.add_status('burn', 2)
                    elif st == 'freeze':
                        target.add_status('freeze', 1)
                    elif st == 'paralyze':
                        target.add_status('paralyze', 1)
                    elif st == 'curse':
                        target.add_status('curse', 2)
                    elif st == 'poison':
                        target.add_status('poison', 2, enemy.attack)
        bs.add_log('[因子] 元素同化：攻击附带元素之力!')


def _engine_summon(bs, enemy):
    from battle_config import ENEMY_TEMPLATES
    basic = _mk_enemy_data(bs, 'basic', scale=0.6)
    if basic:
        pos = _find_free_pos(bs)
        if pos is not None:
            from gene_game import Enemy
            basic['position'] = pos
            try:
                m = Enemy(basic, position=pos, grid_size=bs.enemy_grid_size)
            except Exception:
                return
            _on_spawn(bs, m)
            bs.enemies.append(m)
            m._enemies_ref = bs.enemies
            bs._rebuild_unit_cache()
            bs.add_log(f'[因子] {enemy.name} 召唤了 {m.name}!')


def on_player_action(bs, attacker):
    ids = bs._factor_ids
    fs = bs._factor_state
    if not attacker.is_alive:
        return
    pact = fs.get('pact_left')
    if pact is not None and pact != 0:
        dmg = max(1, int(attacker.max_health * 0.15))
        attacker.take_damage(dmg)
        if pact > 0:
            fs['pact_left'] = pact - 1
        if fs['pact_left'] == 0 and pact > 0:
            bs.add_log('[因子] 血祭契约结束!')


def process_tick(bs):
    ids = bs._factor_ids
    fs = bs._factor_state
    now = time.time()
    last = fs.get('last_sec_tick', now)
    sec_elapsed = now - last
    if sec_elapsed < 1.0:
        return
    fs['last_sec_tick'] = now

    if 'toxic_permanent' in ids and fs.get('perm_zone'):
        for p in bs.player_team:
            if p.is_alive:
                p.add_status('poison', 3, 10)

    # 虫附于身：附着在单位上的圣甲虫群每回合对玩家造成中毒
    attached = sum(getattr(e, '_attached_swarms', 0) for e in bs.enemies if e.is_alive)
    if attached > 0:
        for p in bs.player_team:
            if p.is_alive:
                p.add_status('poison', 3, 10)

    if 'swarm_reproduce' in ids or 'rapid_reproduce' in ids:
        fs['swarm_tick'] = fs.get('swarm_tick', 0) + 1
        interval = 1 if 'rapid_reproduce' in ids else 3
        if fs['swarm_tick'] >= interval:
            fs['swarm_tick'] = 0
            for e in [u for u in bs.enemies if u.is_alive and '圣甲虫' in u.name]:
                _reproduce_swarm(bs, e)

    if 'bb_growth' in ids:
        for e in bs.enemies:
            if e.is_alive and getattr(e, '_box_spawned', False):
                born = getattr(e, '_born_at', now)
                if now - born >= 5.0 and getattr(e, '_grown_ticks', 0) < 10:
                    e._grown_ticks = getattr(e, '_grown_ticks', 0) + 1
                    e.attack = int(e.attack * 1.1)
    if 'bb_charge' in ids or 'bb_decay' in ids or 'bb_precharge' in ids:
        for e in bs.enemies:
            if e.is_alive and getattr(e, '_box', False):
                born = getattr(e, '_born_at', now)
                if now - born >= 3.0:
                    e._box_charge = getattr(e, '_box_charge', 0) + 0.10
                    e._born_at = now

    if _has(bs, 'elem_reso_offense', 'elem_reso_defense', 'elem_reso_speed'):
        alive_elem = [e for e in bs.enemies if e.is_alive and getattr(e, 'template_key', '') in ELEMENTAL_KEYS]
        n = len(alive_elem)
        mult = 2 if 'elem_reso_mastery' in ids else 1
        for e in alive_elem:
            base = getattr(e, '_spawn_attrs', {})
            if 'elem_reso_offense' in ids:
                e.attack = int(base.get('base_atk', e.attack) * (1 + n * 0.05 * mult))
            if 'elem_reso_defense' in ids:
                new_hp = int(base.get('base_hp', e.max_health) * (1 + n * 0.10 * mult))
                if new_hp > e.max_health:
                    diff = new_hp - e.max_health
                    e.max_health = new_hp
                    e.current_health += diff
                else:
                    e.max_health = new_hp
                    e.current_health = min(e.current_health, e.max_health)
            if 'elem_reso_speed' in ids:
                e.speed = int(base.get('base_spd', e.speed) * (1 + n * 0.05 * mult))

    if 'titan_reduce' in ids:
        titans = [e for e in bs.enemies if e.is_alive and '泰坦' in e.name]
        if titans:
            t = titans[0]
            gs = bs.enemy_grid_size
            tr, tc = t.position // gs, t.position % gs
            for e in bs.enemies:
                if e.is_alive and e is not t:
                    er, ec = e.position // gs, e.position % gs
                    if abs(er - tr) <= 1 and abs(ec - tc) <= 1:
                        e.add_status('defense_buff', 2)
                        e.status_effects['defense_buff']['value'] = 50
    if 'titan_transfer' in ids:
        titans = [e for e in bs.enemies if e.is_alive and '泰坦' in e.name]
        if titans:
            t = titans[0]
            gs = bs.enemy_grid_size
            tr, tc = t.position // gs, t.position % gs
            snap = fs.get('last_hp_snapshot', {})
            for e in bs.enemies:
                if not e.is_alive or e is t:
                    continue
                er, ec = e.position // gs, e.position % gs
                if abs(er - tr) <= 1 and abs(ec - tc) <= 1:
                    prev = snap.get(id(e), e.max_health)
                    lost = prev - e.current_health
                    if lost > 0:
                        e.heal(lost)
                        t.take_damage(lost)
                        if not t.is_alive:
                            break
    fs['last_hp_snapshot'] = {id(e): e.current_health for e in bs.enemies if e.is_alive}

    if 'elem_buff_permanent' in ids:
        for u in bs._all_units_cache:
            for s in ('attack_buff', 'speed_buff', 'defense_buff', 'guarantee_skill'):
                if u.has_status(s):
                    u.status_effects[s]['turns'] = 3

    if 'elem_entropy' in ids:
        for p in bs.player_team:
            if p.is_alive and getattr(p, '_entropy', 0) > 0:
                dmg = max(1, int(p.max_health * 0.05 * p._entropy))
                p.take_damage(dmg)

    if 'bb_swarm' in ids:
        boxed = [e for e in bs.enemies if e.is_alive and getattr(e, '_box_spawned', False)]
        n = len(boxed)
        for e in boxed:
            e.attack = int(getattr(e, '_spawn_attrs', {}).get('base_atk', e.attack) * (1 + n * 0.05))


def _reproduce_swarm(bs, scarab):
    if 'swarm_stack' in bs._factor_ids:
        stack = getattr(scarab, '_swarm_stack', 1)
        if stack < 5:
            scarab._swarm_stack = stack + 1
            scarab.max_health = scarab._swarm_base_hp * scarab._swarm_stack
            scarab.current_health = min(scarab.current_health + scarab._swarm_base_hp, scarab.max_health)
            scarab._update_swarm_display()
            bs.add_log(f'[因子] 圣甲虫群繁衍 ({scarab.name})!')
            return
    # 格子堆满或未开启堆叠：尝试新格子，虫附于身时允许附在任意单位上
    if 'swarm_attach' in bs._factor_ids:
        hosts = [e for e in bs.enemies if e.is_alive and '圣甲虫' not in e.name]
        if hosts:
            host = random.choice(hosts)
            host._attached_swarms = getattr(host, '_attached_swarms', 0) + 1
            bs.add_log(f'[因子] 圣甲虫群附着在 {host.name} 上!')
            return
    spawn_enemy(bs, 'ruins_scarab', position=scarab.position, scale=0.6)


def process_deaths(bs):
    ids = bs._factor_ids
    fs = bs._factor_state
    processed = fs.get('dead_processed', set())
    for u in list(bs._all_units_cache):
        if u.is_alive or id(u) in processed:
            continue
        processed.add(id(u))
        if not u.is_player:
            _on_enemy_death(bs, u)
        else:
            if 'poison_chain' in ids and u.has_status('poison'):
                gs = bs.grid_size
                pr, pc = u.position // gs, u.position % gs
                for p in bs.player_team:
                    if p.is_alive:
                        r, c = p.position // gs, p.position % gs
                        if abs(r - pr) <= 1 and abs(c - pc) <= 1:
                            p.add_status('poison', 2, 10)
                for e in bs.enemies:
                    if e.is_alive:
                        r, c = e.position // gs, e.position % gs
                        if abs(r - pr) <= 1 and abs(c - pc) <= 1:
                            e.add_status('poison', 2, 10)
    fs['dead_processed'] = processed


def _on_enemy_death(bs, u):
    ids = bs._factor_ids
    fs = bs._factor_state

    if getattr(u, '_box', False):
        _break_box(bs, u)
        return
    if getattr(u, '_revive_as', None):
        key, name = u._revive_as
        u._revive_as = None
        data = _mk_enemy_data(bs, key, position=u.position)
        if data:
            from gene_game import Enemy
            try:
                ne = Enemy(data, position=u.position, grid_size=bs.enemy_grid_size)
            except Exception:
                ne = None
            if ne:
                _on_spawn(bs, ne)
                idx = None
                for i, e in enumerate(bs.enemies):
                    if e is u:
                        idx = i
                        break
                if idx is not None:
                    bs.enemies[idx] = ne
                else:
                    bs.enemies.append(ne)
                ne._enemies_ref = bs.enemies
                bs.add_log(f'[因子] 元素轮回：{u.name} 复活为 {ne.name}!')
                return
    if getattr(u, '_immortal', False):
        u._immortal = False
        u.current_health = u.max_health // 2
        u.is_alive = True
        u.attack = int(u.attack * 1.3)
        u.max_health = int(u.max_health * 1.3)
        u.current_health = u.max_health // 2
        u.shield = 0
        bs.add_log(f'[因子] 不朽实验体复活! 属性+30%!')
        return
    if 'swarm_remains' in ids and '巨石守卫' in u.name:
        gs = bs.enemy_grid_size
        r, c = u.position // gs, u.position % gs
        count = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                pos = (r + dr) * gs + (c + dc)
                if 0 <= pos < gs * gs and count < 4:
                    s = spawn_enemy(bs, 'ruins_scarab', position=pos, scale=0.7)
                    if s:
                        count += 1
        if count:
            bs.add_log(f'[因子] 巨石守卫爆出 {count} 群圣甲虫!')
    if 'containment_breach' in ids and '收容单元' in u.name:
        b = spawn_enemy(bs, 'lab_boss', position=u.position, scale=0.9)
        if b:
            bs.add_log('[因子] 收容泄露！暴走究极体出现了!')
    if 'toxic_permanent' in ids and '剧毒废料桶' in u.name:
        fs['perm_zone'] = True
        bs.add_log('[因子] 永久污染：毒气将持续整场!')
    if 'toxic_spawn' in ids and '剧毒废料桶' in u.name:
        g = spawn_enemy(bs, 'lab_gasleak', position=u.position, scale=0.8)
        if g:
            bs.add_log('[因子] 废料桶爆出毒气泄漏口!')
    if 'cleaner_transfer' in ids and '清洁机器人' in u.name:
        poison = u.status_effects.get('poison')
        if poison:
            alive_p = [p for p in bs.player_team if p.is_alive]
            if alive_p:
                t = random.choice(alive_p)
                t.add_status('poison', 3, u.attack)
                bs.add_log(f'[因子] 清洁机器人将毒素转移到 {t.name}!')
    if 'elem_mourning' in ids and getattr(u, 'template_key', '') in ELEMENTAL_KEYS:
        for e in bs.enemies:
            if e.is_alive:
                e.action_bar = 100
        bs.add_log('[因子] 元素哀恸：剩余元素立刻行动!')
    if 'eye_overflow' in ids and '眼梗怪' in u.name:
        overflow = getattr(u, '_overflow_pending', 0)
        if overflow > 0:
            alive_p = [p for p in bs.player_team if p.is_alive]
            if alive_p:
                t = alive_p[0]
                t.take_damage(overflow, u)
                bs.add_log(f'[因子] 溢伤追击 {t.name} ({overflow})!')

    if _has(bs, 'bb_drop', 'bb_remains'):
        is_box_spawn = getattr(u, '_box_spawned', False)
        if 'bb_drop' in ids and not is_box_spawn and random.random() < 0.4:
            _spawn_box(bs, u.position)
        elif 'bb_remains' in ids and is_box_spawn:
            _spawn_box(bs, u.position)
    if 'bb_rare' in ids and random.random() < 0.25:
        m = spawn_enemy(bs, random.choice(['elite', 'gene_fusion']), position=u.position, scale=0.8)
        if m:
            bs.add_log('[因子] 盲盒爆出精英怪!')
    if 'bb_legendary' in ids and random.random() < 0.25:
        m = spawn_enemy(bs, random.choice(['devourer', 'overlord']), position=u.position, scale=0.7)
        if m:
            bs.add_log('[因子] 盲盒爆出首领怪!')


def _spawn_box(bs, position):
    gs = bs.enemy_grid_size
    if position is None or position < 0 or position >= gs * gs:
        return None
    occupied = {op for e in bs.enemies if e.is_alive for op in getattr(e, 'occupied_positions', [e.position])}
    if position in occupied:
        return None
    from gene_game import Enemy
    hp_s, _ = _scale_for_stage(bs.stage_num)
    box_hp = max(10, int(20 * hp_s * 0.4))
    data = {
        'name': '盲盒', 'health': box_hp, 'attack': 0, 'defense': 0, 'speed': 0,
        'skills': [], 'passive_abilities': [], 'width': 1, 'height': 1,
        'position': position, 'immune_to_debuffs': True,
    }
    try:
        box = Enemy(data, position=position, grid_size=gs)
    except Exception:
        return None
    box._box = True
    box._box_charge = getattr(bs, '_initial_box_charge', 0)
    box._born_at = time.time()
    if 'bb_hard_shell' in bs._factor_ids:
        box.shield = box.max_health * 2
    elif 'bb_spell_shield' in bs._factor_ids:
        box._spell_shield = True
    if 'bb_thorns' in bs._factor_ids:
        box.passive_skills['荆棘'] = 50
    bs.enemies.append(box)
    box._enemies_ref = bs.enemies
    bs._rebuild_unit_cache()
    bs.add_log('[因子] 一个盲盒出现了!')
    return box


def _break_box(bs, box):
    ids = bs._factor_ids
    if 'bb_drain' in ids:
        for p in bs.player_team:
            if p.is_alive:
                p.action_bar = max(0, p.action_bar - 5)
    if 'bb_trap' in ids:
        alive_p = [p for p in bs.player_team if p.is_alive]
        if alive_p:
            t = random.choice(alive_p)
            debuff = random.choice(['poison', 'burn', 'paralyze', 'curse', 'confuse'])
            t.add_status(debuff, 2, box.attack)
            bs.add_log(f'[因子] 盲盒陷阱：{t.name} 中了 {debuff}!')
    if 'bb_activate' in ids:
        from gene_config import CHALLENGE_FACTORS
        theme = None
        for f in CHALLENGE_FACTORS:
            if f['id'] in ids:
                theme = f.get('theme')
                break
        candidates = [f['id'] for f in CHALLENGE_FACTORS
                      if f.get('theme') == theme and f['id'] not in ids and not f.get('prereq', '').startswith('__')]
        if candidates:
            fid = random.choice(candidates)
            bs._factor_ids.add(fid)
            fs = bs._factor_state
            fs['activated_factors'].add(fid)
            bs.add_log(f'[因子] 盲盒激活了新因子: {fid}!')
            _activate_factor(bs, fid)
    if 'bb_chain' in ids and random.random() < 0.2:
        gs = bs.enemy_grid_size
        r, c = box.position // gs, box.position % gs
        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            pos = (r + dr) * gs + (c + dc)
            if 0 <= pos < gs * gs:
                if _spawn_box(bs, pos):
                    break
    hp_s, _ = _scale_for_stage(bs.stage_num)
    key = random.choice(BLIND_BOX_MONSTER_POOL)
    m = spawn_enemy(bs, key, position=box.position, scale=0.8)
    if m:
        m._box_spawned = True
        m._born_at = time.time()
        bonus = 1.0
        if 'bb_decay' in ids:
            elapsed_ticks = getattr(bs._factor_state, 'box_tick', 0)
            bonus = max(0.5, 1.5 - elapsed_ticks * 0.25)
        elif 'bb_charge' in ids or 'bb_precharge' in ids:
            bonus = 1.0 + getattr(box, '_box_charge', 0)
        if bonus != 1.0:
            m.max_health = int(m.max_health * bonus)
            m.current_health = m.max_health
            m.attack = int(m.attack * bonus)
        bs.add_log(f'[因子] 盲盒打开！{m.name} 出现了!')


def _activate_factor(bs, fid):
    stat_effects = {
        'subject_gene_boost': (1.2, 1.2, 1.0),
        'subject_super_gene': (1.4, 1.4, 1.0),
        'flesh_armor': (1.5, 1.0, 1.0),
        'steel_armor': (1.8, 1.0, 1.0),
        'elem_obliteration': (1.0, 1.5, 1.0),
        'elem_speed_light': (1.0, 1.0, 1.1),
        'elem_speed_storm': (1.0, 1.0, 1.2),
    }
    if fid in stat_effects:
        hm, am, sm = stat_effects[fid]
        for e in bs.enemies:
            if e.is_alive:
                e.max_health = int(e.max_health * hm)
                e.current_health = e.max_health
                e.attack = int(e.attack * am)
                e.speed = int(e.speed * sm)
    if fid == 'elem_fragile':
        for p in bs.player_team:
            p.max_health = int(p.max_health * 0.7)
            p.current_health = min(p.current_health, p.max_health)
    if fid == 'elem_summon_primal':
        spawn_enemy(bs, 'elem_primordial')
    if fid == 'elem_summon_shadow':
        spawn_enemy(bs, 'elem_dark')
        spawn_enemy(bs, 'elem_light')
    if fid == 'elem_summon_crystal':
        spawn_enemy(bs, 'elem_crystal')
        spawn_enemy(bs, 'elem_prism')
    if fid == 'elem_pact_short':
        bs._factor_state['pact_left'] = 4
    if fid == 'elem_pact_long':
        bs._factor_state['pact_left'] = 8
    if fid == 'elem_pact_eternal':
        bs._factor_state['pact_left'] = -1
    if fid == 'subject_boss_descent':
        _replace_enemy(bs, '首领实验体', 'overlord')
    if fid == 'gene_mutate':
        _replace_enemy(bs, '野生实验体', 'mutant')
    if fid == 'elite_force':
        _replace_enemy(bs, '野生实验体', 'elite')
