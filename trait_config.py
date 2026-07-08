# ==========================================
# 性状计算公式配置 - 在这里调整数值
# ==========================================

# 基础属性范围配置
TRAIT_CONFIG = {
    'attack': {
        'base_min': 10,
        'base_max': 30,
        'description': '攻击力',
    },
    'defense': {
        'base_min': 10,
        'base_max': 30,
        'description': '防御力',
    },
    'health': {
        'base_min': 50,
        'base_max': 100,
        'description': '生命值',
    },
    'speed': {
        'base_min': 5,
        'base_max': 25,
        'description': '速度',
    },
    'stamina': {
        'base_min': 20,
        'base_max': 50,
        'description': '耐力',
    },
    'critical_rate': {
        'base_min': 0,
        'base_max': 30,
        'description': '暴击率(%)',
    },
    'dodge_rate': {
        'base_min': 0,
        'base_max': 30,
        'description': '闪避率(%)',
    },
    'luck': {
        'base_min': 1,
        'base_max': 20,
        'description': '幸运值',
    },
    'charisma': {
        'base_min': 1,
        'base_max': 20,
        'description': '魅力值',
    },
    'adaptability': {
        'base_min': 1,
        'base_max': 15,
        'description': '环境适应',
    },
    'mutation_resistance': {
        'base_min': 10,
        'base_max': 50,
        'description': '抗突变率(%)',
    },
    'size': {
        'base_min': 50,
        'base_max': 150,
        'description': '体型(%)',
    },
    'lifespan': {
        'base_min': 50,
        'base_max': 150,
        'description': '寿命(%)',
    },
    'fertility': {
        'base_min': 30,
        'base_max': 80,
        'description': '生育能力',
    },
    'senses': {
        'base_min': 10,
        'base_max': 40,
        'description': '感官强度',
    },
}

# 继承相关配置
INHERIT_CONFIG = {
    'mutation_rate': 0.05,           # 遗传突变概率
    'methylation_inherit_rate': 0.1, # 甲基化遗传概率
    'dominant_inherit_chance': 0.5,  # 等位基因继承概率
}

# 甲基化效果配置
METHYLATION_EFFECT = {
    'stat_factor': 0.3,              # 甲基化时保留30%
    'skill_disable': True,           # 甲基化禁用技能
    'special_disable': True,         # 甲基化禁用特殊效果
}

# 隐性基因表达条件
RECESSIVE_EXPRESS_CONDITION = {
    'require_heterozygous': False,   # 需要杂合状态
    'express_chance': 0.25,          # 隐性表达概率（纯合时）
    'hybrid_vigor_bonus': 0.2,       # 杂种优势加成
}

# 射线变异配置
RADIATION_CONFIG = {
    'light_mutation_rate': 0.3,      # 轻度变异改变1个碱基
    'heavy_mutation_rate': 0.7,      # 重度变异改变2-4个碱基
    'negative_bias': 0.6,            # 负面影响概率
    'trait_change_range': {
        'min': -5,
        'max': 3,
    },
    'vital_gene_damage_chance': 0.05,# 关键基因损坏概率
}

# 研究系统配置
RESEARCH_CONFIG = {
    'reveal_threshold': 5,           # 揭示性状所需操作次数
    'reveal_trait_info': True,       # 揭示后显示性状信息
}

# 基因切割危险阈值
CUTTING_CONFIG = {
    'vital_gene_min_length': 4,      # 关键基因最小安全长度
    'stat_gene_min_length': 2,        # 属性基因最小安全长度
}

# 杂种优势配置
HYBRID_VIGOR_CONFIG = {
    'enabled': True,
    'bonus_traits': ['attack', 'defense', 'health'],
    'bonus_factor': 0.15,
    'require_different_parents': True,
}