import random

random.seed(42)

STAT_TRAITS = [
    'health', 'stamina', 'defense', 'dodge_rate',
    'attack', 'speed', 'critical_rate',
]

CHROMOSOMES = ['chr1', 'chr2', 'chr3', 'chrX']
CHR_LENGTHS = {'chr1': 1000, 'chr2': 1000, 'chr3': 1000, 'chrX': 700}

BASE_CHOICES = ['A', 'T', 'G', 'C']

# Additive patterns: per-base additive value (for all traits; health gets scaled up)
ADD_PATTERNS = [
    {'A': 1, 'T': -1},
    {'A': -1, 'T': 1},
    {'G': 1, 'C': -1},
    {'G': -1, 'C': 1},
    {'A': 1, 'G': -1},
    {'A': -1, 'G': 1},
    {'T': 1, 'C': -1},
    {'T': -1, 'C': 1},
    {'A': 1, 'C': -1},
    {'T': 1, 'G': -1},
]

# Multiplicative patterns: per-base factor (applied after all addition)
# Attack gets ~1.2x, other traits get smaller factors
MUL_PATTERNS = {
    'attack': [
        {'A': 1.20, 'T': 0.90},
        {'G': 1.15, 'C': 0.88},
    ],
    'health': [
        {'C': 1.08, 'A': 0.95},
    ],
    'stamina': [
        {'G': 1.06, 'C': 0.94},
    ],
    'defense': [
        {'A': 1.05, 'T': 0.95},
    ],
    'dodge_rate': [
        {'C': 1.04, 'G': 0.96},
    ],
    'speed': [
        {'T': 1.07, 'A': 0.93},
    ],
    'critical_rate': [
        {'G': 1.05, 'C': 0.95},
    ],
}


def _generate_enhancements():
    regions = {trait: [] for trait in STAT_TRAITS}
    counts = {t: 3 if t == 'attack' else 2 for t in STAT_TRAITS}
    add_idx = 0

    for trait in STAT_TRAITS:
        # Generate additive regions (no mul key)
        for _ in range(counts[trait]):
            chr_id = random.choice(CHROMOSOMES)
            max_len = CHR_LENGTHS[chr_id]
            padding_start = 120 if chr_id != 'chrX' else 90
            region_len = random.randint(40, 70)
            start = random.randint(padding_start, max_len - region_len - 10)
            end = start + region_len

            add = ADD_PATTERNS[add_idx % len(ADD_PATTERNS)]
            add_idx += 1

            if trait == 'health':
                add = {k: v * 50 for k, v in add.items()}

            regions[trait].append({
                'chr': chr_id,
                'start': start,
                'end': end,
                'add': add,
            })

        # Generate multiplicative regions (no add key) — short regions to avoid runaway
        mul_list = MUL_PATTERNS.get(trait, [])
        for mul in mul_list:
            chr_id = random.choice(CHROMOSOMES)
            max_len = CHR_LENGTHS[chr_id]
            padding_start = 120 if chr_id != 'chrX' else 90
            region_len = random.randint(20, 35)
            start = random.randint(padding_start, max_len - region_len - 10)
            end = start + region_len

            regions[trait].append({
                'chr': chr_id,
                'start': start,
                'end': end,
                'mul': mul,
            })

    return regions


STAT_ENHANCE_REGIONS = _generate_enhancements()
