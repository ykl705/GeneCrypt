# ============================================================
# 基因增强区域配置 - 跨多条染色体的长增强段
#
# 每条染色体（chr1/chr2/chr3/chrX）的基因后方是随机填充区（碱基随机、
# 随繁殖交叉遗传）。在每个数值属性分配多个「增强区域」：
#   加算区域（40~70碱基）: 某碱基越多 -> 平加越高（如 A越多攻击+越多）
#   乘算区域（20~35碱基）: 某碱基越多 -> 倍率指数上涨（如 C越多 x(1.04)^C）
# 两条同源染色体（一对）都参与计算。
#
# 所有数值再乘以「任务推进强度」 Card._enhance_power：
#   前期主线任务少 -> 增强弱；任务推进 -> 增强越来越强
# ============================================================
import random

random.seed(42)

STAT_TRAITS = [
    'health', 'stamina', 'defense', 'dodge_rate',
    'attack', 'speed', 'critical_rate',
]

CHROMOSOMES = ['chr1', 'chr2', 'chr3', 'chrX']
CHR_LENGTHS = {'chr1': 1000, 'chr2': 1000, 'chr3': 1000, 'chrX': 700}

# 各染色体基因区之后（填充区起始）
PADDING_STARTS = {'chr1': 130, 'chr2': 130, 'chr3': 210, 'chrX': 100}

BASE_CHOICES = ['A', 'T', 'G', 'C']

# 加算规则：每属性多个区域（跨多条染色体），正碱基平加 / 负碱基平减
TRAIT_ADD_RULES = {
    'attack': [
        {'A': 0.8, 'T': -0.4},
        {'G': 0.8, 'C': -0.4},
        {'A': 0.8, 'G': -0.4},
    ],
    'health': [
        {'C': 8, 'G': -4},
        {'A': 8, 'T': -4},
    ],
    'defense': [
        {'G': 1.2, 'C': -0.6},
        {'A': 1.2, 'T': -0.6},
    ],
    'speed': [
        {'T': 0.9, 'A': -0.45},
        {'C': 0.9, 'G': -0.45},
    ],
    'stamina': [
        {'G': 4, 'C': -2},
        {'A': 4, 'T': -2},
    ],
    'critical_rate': [
        {'C': 1.2, 'G': -0.6},
        {'T': 1.2, 'A': -0.6},
    ],
    'dodge_rate': [
        {'T': 1.2, 'A': -0.6},
        {'G': 1.2, 'C': -0.6},
    ],
}

# 乘算规则：正碱基倍率>1 / 负碱基倍率<1，在（基础+加算）之上指数上涨
TRAIT_MUL_RULES = {
    'attack': [
        {'C': 1.04, 'G': 0.97},
        {'A': 1.03, 'T': 0.98},
    ],
    'health': [
        {'C': 1.02, 'G': 0.985},
    ],
    'defense': [
        {'C': 1.02, 'G': 0.985},
    ],
    'speed': [
        {'T': 1.02, 'A': 0.985},
    ],
    'stamina': [
        {'G': 1.015, 'C': 0.985},
    ],
    'critical_rate': [
        {'G': 1.02, 'C': 0.985},
    ],
    'dodge_rate': [
        {'C': 1.02, 'G': 0.985},
    ],
}

ADD_REGION_LEN = (40, 70)
MUL_REGION_LEN = (20, 35)


def _place_region(chr_id, region_len):
    max_len = CHR_LENGTHS[chr_id]
    pad_start = PADDING_STARTS.get(chr_id, 120)
    lo = pad_start
    hi = max_len - region_len - 5
    if hi <= lo:
        hi = lo
    start = random.randint(lo, hi)
    return start, start + region_len


def _generate_enhancements():
    regions = {trait: [] for trait in STAT_TRAITS}
    for trait in STAT_TRAITS:
        add_rules = TRAIT_ADD_RULES.get(trait, [])
        for i, rules in enumerate(add_rules):
            chr_id = CHROMOSOMES[i % len(CHROMOSOMES)]
            rlen = random.randint(*ADD_REGION_LEN)
            start, end = _place_region(chr_id, rlen)
            regions[trait].append({
                'chr': chr_id,
                'start': start,
                'end': end,
                'add': dict(rules),
            })
        mul_rules = TRAIT_MUL_RULES.get(trait, [])
        for i, rules in enumerate(mul_rules):
            chr_id = CHROMOSOMES[(len(add_rules) + i) % len(CHROMOSOMES)]
            rlen = random.randint(*MUL_REGION_LEN)
            start, end = _place_region(chr_id, rlen)
            regions[trait].append({
                'chr': chr_id,
                'start': start,
                'end': end,
                'mul': dict(rules),
            })
    return regions


STAT_ENHANCE_REGIONS = _generate_enhancements()

# 兼容旧代码（基因内5碱基段已弃用，保留空表）
STAT_GENE_SEGMENTS = {}
