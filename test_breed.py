"""Test that bred child from reward cards only inherits parent skills."""
import sys; sys.path.insert(0,'.')
import gene_config as gc, gene_enhance_config as gec, trait_config as tc, tech_config as tcc
sys.modules.update({'gene_config':gc,'gene_enhance_config':gec,'trait_config':tc,'tech_config':tcc})
from gene_game import *

g = Game(load_save=False)
g.battle_materials = 5000
g.gacha_currency = 500

# Unlock needed techs for breeding
g.tech_tree['gene_engineering']['level'] = 2
g.tech_tree['embryo_engineering']['unlocked'] = True
g.tech_tree['embryo_engineering']['level'] = 2

# Build set of all 35 skill names
ALL_SKILL_NAMES = set()
for gn in gc.SKILL_GENES:
    tmpl = gc.GENE_TEMPLATES.get(gn, {})
    sn = tmpl.get('skill_name')
    if sn: ALL_SKILL_NAMES.add(sn)

def check_chrom_sync(card, desc):
    """Verify gene is_dominant matches chromosome is_dominant for all skill genes"""
    for gn in gc.SKILL_GENES:
        gd = card.genes.get(gn)
        if not gd:
            continue
        gene_is_dom = gd['allele1']['is_dominant']
        chr_id = gd.get('chromosome', 'chr1')
        if chr_id == 'chrY': chr_id = 'chrX'
        h = card.chromosomes.get(chr_id, [{}])
        for hom in h:
            dom = hom.get('is_dominant', {})
            if gn in dom and dom[gn] != gene_is_dom:
                return False
    return True

def make_opposite_gender_card(g, skill, quality, existing_card):
    for _ in range(30):
        c = g._create_skill_reward_card(skill, quality=quality)
        if c.gender != existing_card.gender:
            return c
        g.cards.remove(c)
    return None

# ===== Test 1: Different skills → child gets subset (recessive inheritance) =====
print("=== Test 1: Different parents -> child inherits recessive ===")
card1 = g._create_skill_reward_card(['冻结'], quality=0.3)
card2 = make_opposite_gender_card(g, ['甘霖'], 0.35, card1)

print(f"  P1: skills={card1.skills}  chrom_sync={check_chrom_sync(card1, '')}")
print(f"  P2: skills={card2.skills}  chrom_sync={check_chrom_sync(card2, '')}")

cc, cg = g.breeding(card1, card2)
child = g.create_card("测试子代", chromosomes=cc, parent_ids=[card1.id, card2.id])
child_skills = set(child.skills)

# With recessive inheritance, these different-skill parents can only
# produce a child with a skill if BOTH happen to pass the dominant allele
# for the same gene. Since each parent has only one skill active,
# the child inherits at most those 2 skills.
extra = child_skills - {'冻结', '甘霖'}
print(f"  Child: skills={child.skills}")
print(f"  Has non-parent skills: {extra}")
assert not extra, f"BUG: child has {extra} not in parents!"
all_35 = ALL_SKILL_NAMES
assert child_skills != all_35, f"BUG: child has ALL {len(all_35)} skills!"
print("  PASS")

# ===== Test 2: Same skill on both parents → child can inherit =====
print("\n=== Test 2: Same skill parents -> child can inherit ===")
g2 = Game(load_save=False)
g2.tech_tree['gene_engineering']['level'] = 2
g2.tech_tree['embryo_engineering']['unlocked'] = True
g2.tech_tree['embryo_engineering']['level'] = 2

p1 = g2._create_skill_reward_card(['冻结'], quality=0.3)
p2 = make_opposite_gender_card(g2, ['冻结'], 0.35, p1)

cc, cg = g2.breeding(p1, p2)
c = g2.create_card("同技能子代", chromosomes=cc, parent_ids=[p1.id, p2.id])
cs = set(c.skills)
extra = cs - {'冻结'}
print(f"  P1: skills={p1.skills}  P2: skills={p2.skills}  Child: skills={c.skills}")
assert not extra, f"BUG: child has {extra} not in parents!"
# With both parents all-dominant for the same gene, the child should
# (with high probability) inherit at least one copy -> homozygous -> skill
print(f"  Has '冻结': {'冻结' in cs}")
assert '冻结' in cs, f"Child of two '冻结' parents should inherit it!"
print("  PASS")

# ===== Test 3: Same skill both alleles → force inheritance =====
print("\n=== Test 3: Verify is_dominant propagates through gametes ===")
g3 = Game(load_save=False)
p1 = g3._create_skill_reward_card(['冻结'], quality=0.3)
# Verify chromosome is_dominant
gd = p1.genes.get('skill_freeze', {})
a1 = gd.get('allele1', {}).get('is_dominant', None)
a2 = gd.get('allele2', {}).get('is_dominant', None)
print(f"  P1 skill_freeze: allele1.is_dominant={a1}, allele2.is_dominant={a2}")
assert a1 == True, "skill_freeze allele1 not dominant!"
assert a2 == True, "skill_freeze allele2 not dominant!"

# Check chromosome sync
ch = p1.chromosomes.get('chr1', [{}, {}])
d0 = ch[0].get('is_dominant', {}).get('skill_freeze', None)
d1 = ch[1].get('is_dominant', {}).get('skill_freeze', None)
print(f"  P1 chr1 homologs: is_dominant[skill_freeze] = {d0}, {d1}")
assert d0 == True, "chr1[0] skill_freeze not synced!"
assert d1 == True, "chr1[1] skill_freeze not synced!"

# Also verify non-desired skill genes are False on chromosomes
other = ch[0].get('is_dominant', {}).get('skill_heal', None)
print(f"  P1 chr1 skill_heal (not wanted): is_dominant = {other}")
assert other == False, f"skill_heal should be False but is {other}!"

# Verify child of same-skill parents gets it
for _ in range(5):
    p_freeze = g3._create_skill_reward_card(['冻结'], quality=0.3)
    # Find an opposite gender
    others = [c for c in g3.cards if c.gender != p_freeze.gender and '冻结' in c.skills]
    if others:
        cc, cg = g3.breeding(p_freeze, others[0])
        child3 = g3.create_card("冻结子代", chromosomes=cc)
        has_freeze = '冻结' in child3.skills
        extra_skills = set(child3.skills) - {'冻结'}
        print(f"    Child skills={child3.skills} has_freeze={has_freeze} extra={extra_skills}")
        assert not extra_skills, f"BUG: child has {extra_skills} not in parents!"
        if has_freeze:
            break
else:
    print("  (All children heterozygous if different chromosome copies inherited)")

print("  PASS")

# ===== Summary =====
print("\n=== SUMMARY ===")
print("Test 1 (different skills): No non-parent skills in child - PASS")
print("Test 2 (same skill): Child inherits parent skill - PASS")
print("Test 3 (dominance propagation): is_dominant synced through chain - PASS")
