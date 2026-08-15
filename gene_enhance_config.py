# ============================================================
# 基因增强段配置 - 数值基因内的加算/乘算片段
#
# 每个数值基因（10碱基）内部划分为两段：
#   add段: 某一碱基越多 -> 加算值越高（平加）
#   mul段: 某一碱基越多 -> 乘算倍率越高（(1+per_base)^count，在基础+加算之上指数上涨）
#
# 所有数值会乘以「任务推进强度」 Card._enhance_power：
#   前期任务进度低 -> 增强段较弱；主线任务推进 -> 增强越来越强
# ============================================================

STAT_TRAITS = [
    'health', 'stamina', 'defense', 'dodge_rate',
    'attack', 'speed', 'critical_rate',
]

CHROMOSOMES = ['chr1', 'chr2', 'chr3', 'chrX']
CHR_LENGTHS = {'chr1': 1000, 'chr2': 1000, 'chr3': 1000, 'chrX': 700}

BASE_CHOICES = ['A', 'T', 'G', 'C']

# 增强段定义：每个数值基因内部两段各5个碱基
# add: {'base': 碱基, 'start': 基因内偏移, 'end': 基因内偏移, 'per_base': 每个该碱基的加算值}
# mul: {'base': 碱基, 'start': ..., 'end': ..., 'per_base': 每个该碱基的乘算倍率}
STAT_GENE_SEGMENTS = {
    'attack': {
        'add': {'base': 'A', 'start': 0, 'end': 5, 'per_base': 4},
        'mul': {'base': 'C', 'start': 5, 'end': 10, 'per_base': 0.05},
    },
    'health': {
        'add': {'base': 'A', 'start': 0, 'end': 5, 'per_base': 12},
        'mul': {'base': 'C', 'start': 5, 'end': 10, 'per_base': 0.04},
    },
    'defense': {
        'add': {'base': 'G', 'start': 0, 'end': 5, 'per_base': 2},
        'mul': {'base': 'C', 'start': 5, 'end': 10, 'per_base': 0.04},
    },
    'speed': {
        'add': {'base': 'T', 'start': 0, 'end': 5, 'per_base': 1},
        'mul': {'base': 'C', 'start': 5, 'end': 10, 'per_base': 0.04},
    },
    'stamina': {
        'add': {'base': 'G', 'start': 0, 'end': 5, 'per_base': 4},
        'mul': {'base': 'C', 'start': 5, 'end': 10, 'per_base': 0.03},
    },
    'critical_rate': {
        'add': {'base': 'C', 'start': 0, 'end': 5, 'per_base': 1},
        'mul': {'base': 'G', 'start': 5, 'end': 10, 'per_base': 0.04},
    },
    'dodge_rate': {
        'add': {'base': 'T', 'start': 0, 'end': 5, 'per_base': 1},
        'mul': {'base': 'G', 'start': 5, 'end': 10, 'per_base': 0.04},
    },
}

# 兼容旧代码：保留 STAT_ENHANCE_REGIONS 为空（旧padding随机段已弃用）
STAT_ENHANCE_REGIONS = {t: [] for t in STAT_TRAITS}
