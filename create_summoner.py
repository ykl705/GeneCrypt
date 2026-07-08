import sys, json, os, random, copy
sys.path.insert(0, '.')
from gene_game import Card, Game, GENE_TEMPLATES, GENE_REGIONS, CHROMOSOME_LENGTH, BASES
from gene_enhance_config import STAT_ENHANCE_REGIONS


def gene_strategy(gene_name, homolog_idx):
    """
    Return (seq_to_use, is_dominant_bool).
    homology_idx: 0=homolog1, 1=homolog2
    """
    tmpl = GENE_TEMPLATES.get(gene_name, {})
    dom_seq = tmpl.get('sequence', '')
    rec_seq = tmpl.get('recessive_sequence', '')
    cat = tmpl.get('category', '')
    
    if cat == 'vital':
        return (dom_seq, True)
    if cat == 'passive':
        return (rec_seq, False)
    if cat == 'special' or cat == 'recessive':
        return (dom_seq, True)
    if cat == 'skill':
        if gene_name == 'skill_summon':
            return (dom_seq, True)
        else:
            return (dom_seq, True) if homolog_idx == 0 else (rec_seq, False)
    
    # Stats
    if gene_name in ('health', 'defense'):
        return (rec_seq, False)
    elif gene_name == 'speed':
        return (dom_seq, True)
    elif gene_name == 'attack':
        return (dom_seq, True) if homolog_idx == 0 else (rec_seq, False)
    elif gene_name == 'stamina':
        return (dom_seq, True)
    elif gene_name == 'dodge':
        return (dom_seq, True)
    elif gene_name == 'critical':
        return (dom_seq, True)
    
    return (dom_seq, True)


def neutral_base(region):
    add = region.get('add', {})
    mul = region.get('mul', {})
    forbidden = set(add.keys()) | set(mul.keys())
    for b in 'ATGC':
        if b not in forbidden:
            return b
    return 'A'


def build_chromosomes():
    chromosomes = {}
    
    for chr_id in ['chr1', 'chr2', 'chr3', 'chrX']:
        regions = GENE_REGIONS.get(chr_id if chr_id != 'chrX' else 'chrX', [])
        target = CHROMOSOME_LENGTH.get(chr_id, 1000)
        
        for h_idx in (0, 1):
            gene_parts = []
            dom_map = {}
            for gene_name, start, end in regions:
                tmpl = GENE_TEMPLATES.get(gene_name, {})
                seqlen = end - start
                s, dom = gene_strategy(gene_name, h_idx)
                s = (s or 'A'*seqlen)[:seqlen].ljust(seqlen, 'A')
                gene_parts.append(s)
                dom_map[gene_name] = dom
            
            gene_region = ''.join(gene_parts)
            pad_start = len(gene_region)
            pad_len = target - pad_start
            
            # Fill padding with neutral bases per enhancer region
            padding = ['N'] * pad_len
            
            for trait_name, enh_regions in STAT_ENHANCE_REGIONS.items():
                for ri, reg in enumerate(enh_regions):
                    if reg['chr'] != chr_id:
                        continue
                    estart = reg['start']
                    eend = reg['end']
                    if estart < pad_start:
                        continue
                    lo = estart - pad_start
                    hi = min(eend - pad_start, pad_len)
                    if lo >= pad_len:
                        continue
                    length = hi - lo
                    if length <= 0:
                        continue
                    
                    bases = _fill_strategy(trait_name, ri, reg, length)
                    for i in range(length):
                        if lo + i < pad_len:
                            padding[lo + i] = bases[i % len(bases)]
            
            # Fill remaining N's with neutral per each region's default
            for trait_name, enh_regions in STAT_ENHANCE_REGIONS.items():
                for ri, reg in enumerate(enh_regions):
                    if reg['chr'] != chr_id:
                        continue
                    estart = reg['start']
                    eend = reg['end']
                    if estart < pad_start:
                        continue
                    lo = estart - pad_start
                    hi = min(eend - pad_start, pad_len)
                    if lo >= pad_len:
                        continue
                    nb = neutral_base(reg)
                    for i in range(lo, hi):
                        if padding[i] == 'N':
                            padding[i] = nb
            
            # Remaining N's → pick any neutral base that works for ALL trait regions covering this position
            # For simplicity, fill with 'A' (it's neutral for most regions)
            for i in range(pad_len):
                if padding[i] == 'N':
                    padding[i] = 'A'
            
            genome = gene_region + ''.join(padding)
            
            if chr_id == 'chrX':
                if 'chrX' not in chromosomes:
                    chromosomes['chrX'] = []
                chromosomes['chrX'].append({'type': 'X', 'genome': genome, 'is_dominant': dom_map})
            else:
                if chr_id not in chromosomes:
                    chromosomes[chr_id] = []
                chromosomes[chr_id].append({'genome': genome, 'is_dominant': dom_map})
    
    return chromosomes


def _fill_strategy(trait_name, ri, reg, length):
    """Return the base string for an enhancer region based on trait strategy."""
    add = reg.get('add', {})
    mul = reg.get('mul', {})
    
    if trait_name == 'speed':
        # Want fast: ~5-7% beneficial bases
        if add:
            beneficial = next(iter(add.keys()))  # find the +1 base
            for b, v in add.items():
                if v > 0: beneficial = b
            n_beneficial = max(1, int(length * 0.06))
            nb = neutral_base(reg)
            return beneficial * n_beneficial + nb * (length - n_beneficial)
        if mul:
            beneficial = next(iter(mul.keys()))
            for b, v in mul.items():
                if v > 1.0: beneficial = b
            n_beneficial = max(1, int(length * 0.07))
            nb = neutral_base(reg)
            return beneficial * n_beneficial + nb * (length - n_beneficial)
    
    if trait_name == 'attack':
        # Want moderate: no add contributions, balanced mul
        if add and not mul:
            return neutral_base(reg) * length
        if mul:
            # attack mul region 0: chrX(477-500) {A:1.2, T:0.9}
            if ri == 3:  # first mul region
                a_cnt = min(8, length)
                t_cnt = min(15, length - a_cnt)
                remaining = length - a_cnt - t_cnt
                nb = neutral_base(reg)
                return 'A' * a_cnt + 'T' * t_cnt + nb * remaining
            # attack mul region 1: chr1(763-792) {G:1.15, C:0.88}
            if ri == 4:
                g_cnt = min(15, length)
                c_cnt = min(14, length - g_cnt)
                remaining = length - g_cnt - c_cnt
                nb = neutral_base(reg)
                return 'G' * g_cnt + 'C' * c_cnt + nb * remaining
    
    if trait_name in ('health', 'defense'):
        # Want very low: use detrimental bases
        if add:
            detrimental = next(iter(add.keys()))
            for b, v in add.items():
                if v < 0: detrimental = b
            return detrimental * length
        if mul:
            detrimental = next(iter(mul.keys()))
            for b, v in mul.items():
                if v < 1.0: detrimental = b
            return detrimental * length
    
    # Default: fill with neutral base
    return neutral_base(reg) * length


def main():
    game = Game(load_save=True)
    chromosomes = build_chromosomes()
    card = Card("召唤师", chromosomes=chromosomes)
    
    if card.is_alive:
        card.id = f"CARD{Card.card_count:04d}"
        game.cards.append(card)
        
        print("召唤师创建成功!")
        print(f"  ID: {card.id}")
        print(f"  性别: {'雄性' if card.gender == 'male' else '雌性'}")
        print(f"  技能: {card.skills}")
        print(f"  被动: {card.passive_skills}")
        print(f"\n--- 属性 ---")
        for k, v in sorted(card.traits.items()):
            print(f"  {k}: {v}")
        
        has_summon = '召唤' in card.skills
        extra_skills = [s for s in card.skills if s != '召唤']
        spd = card.traits.get('speed', 0)
        atk = card.traits.get('attack', 0)
        hp = card.traits.get('health', 0)
        df = card.traits.get('defense', 0)
        
        checks = []
        checks.append(('仅有召唤技能', has_summon and len(extra_skills) == 0, str(extra_skills)))
        checks.append(('速度适中偏快', 20 <= spd <= 80, str(spd)))
        checks.append(('攻击适中', 10 <= atk <= 40, str(atk)))
        checks.append(('血量偏低', hp <= 15, str(hp)))
        checks.append(('防御偏低', df <= 15, str(df)))
        
        print(f"\n--- 验证 ---")
        all_ok = True
        for label, ok, val in checks:
            status = '通过' if ok else '失败'
            if not ok: all_ok = False
            print(f"  {label}: {status} ({val})")
        
        if all_ok:
            # Remove old summoners
            to_remove = [c for c in game.cards if c.name == '召唤师' and c.id != card.id]
            for c in to_remove:
                game.cards.remove(c)
                print(f"  已移除旧版本: {c.id}")
            
            game.save_game()
            print(f"\n已保存到 {game.SAVE_FILE}")
        else:
            print(f"\n需要调整后重新运行")
    else:
        print("创建失败: 卡牌死亡")
        for v in ['health_maintain', 'metabolism', 'reproduction', 'nervous', 'immune']:
            if v in card.genes:
                gd = card.genes[v]
                a1, a2 = gd['allele1']['seq'], gd['allele2']['seq']
                print(f"  {v}: len={len(a1)},{len(a2)}")


if __name__ == '__main__':
    main()
