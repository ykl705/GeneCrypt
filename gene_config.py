# ==========================================
# 基因模板配置 - 在这里添加新基因
# ==========================================
# category: 'stat'(属性) / 'vital'(关键) / 'skill'(技能) / 'special'(特殊) / 'recessive'(隐性)
# vital: True 表示该基因损坏会导致死亡
# dominant: True 表示显性遗传，False 表示隐性遗传
# sequence: 显性等位基因的碱基序列
# recessive_sequence: 隐性等位基因的碱基序列

GENE_TEMPLATES = {
    # ==================== 基础属性基因 ====================
    'attack': {
        'sequence': 'ATGCGATCGG',
        'recessive_sequence': 'aatgcgatcg',
        'dominant': True,
        'vital': False,
        'description': '攻击力基因',
        'category': 'stat',
        'affects_trait': 'attack',
    },
    'defense': {
        'sequence': 'GCTAGCTAGC',
        'recessive_sequence': 'gctagctaac',
        'dominant': True,
        'vital': False,
        'description': '防御力基因',
        'category': 'stat',
        'affects_trait': 'defense',
    },
    'health': {
        'sequence': 'AATTGGCCAT',
        'recessive_sequence': 'aattggcggg',
        'dominant': True,
        'vital': False,
        'description': '生命值基因',
        'category': 'stat',
        'affects_trait': 'health',
    },
    'speed': {
        'sequence': 'ATATATATAC',
        'recessive_sequence': 'atatatatta',
        'dominant': True,
        'vital': False,
        'description': '速度基因',
        'category': 'stat',
        'affects_trait': 'speed',
    },
    'stamina': {
        'sequence': 'GCGCATATAC',
        'recessive_sequence': 'gcgcataact',
        'dominant': True,
        'vital': False,
        'description': '耐力基因',
        'category': 'stat',
        'affects_trait': 'stamina',
    },
    'critical': {
        'sequence': 'TATAGCGCGT',
        'recessive_sequence': 'tatagcgcac',
        'dominant': True,
        'vital': False,
        'description': '暴击率基因',
        'category': 'stat',
        'affects_trait': 'critical_rate',
    },
    'dodge': {
        'sequence': 'CGCGTATAAG',
        'recessive_sequence': 'cgcgtattcc',
        'dominant': True,
        'vital': False,
        'description': '闪避率基因',
        'category': 'stat',
        'affects_trait': 'dodge_rate',
    },

    # ==================== 关键基因 - 维持生命 ====================
    'health_maintain': {
        'sequence': 'ATATGCGCAC',
        'recessive_sequence': 'atatgcgccc',
        'dominant': True,
        'vital': True,
        'description': '生命维持基因',
        'category': 'vital',
        'affects_trait': None,
    },
    'metabolism': {
        'sequence': 'TATATATATT',
        'recessive_sequence': 'tatataagaa',
        'dominant': True,
        'vital': True,
        'description': '代谢基因',
        'category': 'vital',
        'affects_trait': None,
    },
    'reproduction': {
        'sequence': 'CGCGCGCGCA',
        'recessive_sequence': 'cgcgcgcaaa',
        'dominant': True,
        'vital': True,
        'description': '繁殖能力基因',
        'category': 'vital',
        'affects_trait': None,
    },
    'nervous': {
        'sequence': 'GATTACAGAC',
        'recessive_sequence': 'gattacaaaa',
        'dominant': True,
        'vital': True,
        'description': '神经系统基因',
        'category': 'vital',
        'affects_trait': None,
    },
    'immune': {
        'sequence': 'ATCGATCGAT',
        'recessive_sequence': 'atcgatcgaa',
        'dominant': True,
        'vital': True,
        'description': '免疫系统基因',
        'category': 'vital',
        'affects_trait': None,
    },

    # ==================== 技能基因 ====================
    'skill_fire': {
        'sequence': 'GTACGTACGT',
        'recessive_sequence': 'gtacgtaaag',
        'dominant': False,
        'vital': False,
        'description': '火焰吐息基因',
        'category': 'skill',
        'skill_name': '火焰吐息',
    },
    'skill_ice': {
        'sequence': 'CGTACGTACG',
        'recessive_sequence': 'cgtacgtaac',
        'dominant': False,
        'vital': False,
        'description': '冰霜护盾基因',
        'category': 'skill',
        'skill_name': '冰霜护盾',
    },
    'skill_lightning': {
        'sequence': 'TTAATTAATC',
        'recessive_sequence': 'ttaattaaaa',
        'dominant': False,
        'vital': False,
        'description': '雷击基因',
        'category': 'skill',
        'skill_name': '雷击',
    },
    'skill_poison': {
        'sequence': 'GCATGCATGC',
        'recessive_sequence': 'gcatgcatga',
        'dominant': False,
        'vital': False,
        'description': '毒液攻击基因',
        'category': 'skill',
        'skill_name': '毒液攻击',
    },
    'skill_heal': {
        'sequence': 'ATATGCGCGG',
        'recessive_sequence': 'atatgcgcaa',
        'dominant': False,
        'vital': False,
        'description': '自我修复基因',
        'category': 'skill',
        'skill_name': '自我修复',
    },
    'skill_shield': {
        'sequence': 'CGCGTATATT',
        'recessive_sequence': 'cgcgtataag',
        'dominant': False,
        'vital': False,
        'description': '能量护盾基因',
        'category': 'skill',
        'skill_name': '能量护盾',
    },
    'skill_illusion': {
        'sequence': 'TATACGCGCA',
        'recessive_sequence': 'tatacgcgat',
        'dominant': False,
        'vital': False,
        'description': '幻觉制造基因',
        'category': 'skill',
        'skill_name': '幻觉制造',
    },
    'skill_teleport': {
        'sequence': 'ATATATGCGA',
        'recessive_sequence': 'atatatgcaa',
        'dominant': False,
        'vital': False,
        'description': '瞬移基因',
        'category': 'skill',
        'skill_name': '瞬移',
    },
    'skill_sleep': {
        'sequence': 'GCGCATATAG',
        'recessive_sequence': 'gcgcataaaa',
        'dominant': False,
        'vital': False,
        'description': '睡眠诱导基因',
        'category': 'skill',
        'skill_name': '睡眠诱导',
    },
    'skill_paralyze': {
        'sequence': 'TATATGCGCT',
        'recessive_sequence': 'atatgcgcac',
        'dominant': False,
        'vital': False,
        'description': '麻痹神经基因',
        'category': 'skill',
        'skill_name': '麻痹神经',
    },
    'skill_absorption': {
        'sequence': 'CGCGATATAC',
        'recessive_sequence': 'cgcgataaag',
        'dominant': False,
        'vital': False,
        'description': '能量吸收基因',
        'category': 'skill',
        'skill_name': '能量吸收',
    },
    'skill_summon': {
        'sequence': 'ATGCATGCAT',
        'recessive_sequence': 'atgcatgcaa',
        'dominant': False,
        'vital': False,
        'description': '召唤基因',
        'category': 'skill',
        'skill_name': '召唤',
    },
    'skill_invisibility': {
        'sequence': 'TATATATGCG',
        'recessive_sequence': 'tatatatgaa',
        'dominant': False,
        'vital': False,
        'description': '隐身基因',
        'category': 'skill',
        'skill_name': '隐身',
    },
    'skill_explosion': {
        'sequence': 'GCGCGCATAA',
        'recessive_sequence': 'gcgcgcataa',
        'dominant': False,
        'vital': False,
        'description': '自爆基因',
        'category': 'skill',
        'skill_name': '自爆',
    },
    'skill_growth': {
        'sequence': 'ATATATATAA',
        'recessive_sequence': 'atatatataa',
        'dominant': False,
        'vital': False,
        'description': '快速生长基因',
        'category': 'skill',
        'skill_name': '快速生长',
    },
    'skill_observe': {
        'sequence': 'TAGCTAGCTA',
        'recessive_sequence': 'tagctagcga',
        'dominant': False,
        'vital': False,
        'description': '观星基因',
        'category': 'skill',
        'skill_name': '观星',
    },
    'skill_surge': {
        'sequence': 'CGATCGTAGC',
        'recessive_sequence': 'cgatcgtaag',
        'dominant': False,
        'vital': False,
        'description': '澎湃基因',
        'category': 'skill',
        'skill_name': '澎湃',
    },
    'skill_heal_team': {
        'sequence': 'AAGCTAGCGA',
        'recessive_sequence': 'aagctagcga',
        'dominant': False,
        'vital': False,
        'description': '甘霖基因',
        'category': 'skill',
        'skill_name': '甘霖',
    },

    # ==================== 新技能基因 (61-100关) ====================
    'skill_freeze': {
        'sequence': 'AGCTAGCTAG',
        'recessive_sequence': 'agctagctag',
        'dominant': False,
        'vital': False,
        'description': '冻结基因',
        'category': 'skill',
        'skill_name': '冻结',
    },
    'skill_curse': {
        'sequence': 'TAGCTAGCAG',
        'recessive_sequence': 'tagctagcag',
        'dominant': False,
        'vital': False,
        'description': '诅咒基因',
        'category': 'skill',
        'skill_name': '诅咒',
    },
    'skill_burn': {
        'sequence': 'CGATCGATCG',
        'recessive_sequence': 'cgatcgatcg',
        'dominant': False,
        'vital': False,
        'description': '灼烧基因',
        'category': 'skill',
        'skill_name': '灼烧',
    },
    'skill_execute': {
        'sequence': 'ATCGATCGAA',
        'recessive_sequence': 'atcgatcgaa',
        'dominant': False,
        'vital': False,
        'description': '处决基因',
        'category': 'skill',
        'skill_name': '处决',
    },
    'skill_aoe_poison': {
        'sequence': 'GCTAGCTAGC',
        'recessive_sequence': 'gctagctagc',
        'dominant': False,
        'vital': False,
        'description': '毒雾扩散基因',
        'category': 'skill',
        'skill_name': '毒雾扩散',
    },
    'skill_rewind': {
        'sequence': 'TATCGATCGA',
        'recessive_sequence': 'tatcgatcga',
        'dominant': False,
        'vital': False,
        'description': '时光倒流基因',
        'category': 'skill',
        'skill_name': '时光倒流',
    },
    'skill_revive': {
        'sequence': 'CGCGATCGAT',
        'recessive_sequence': 'cgcgatcgat',
        'dominant': False,
        'vital': False,
        'description': '亡灵复苏基因',
        'category': 'skill',
        'skill_name': '亡灵复苏',
    },
    'skill_assassin': {
        'sequence': 'TTCGATCGAT',  # 前6位B序列 TTCGAT
        'recessive_sequence': 'aaaaaaaaaaaa',
        'dominant': True,
        'vital': False,
        'description': '暗杀者被动基因 — 纯合BB获得暗杀者效果',
        'category': 'passive',
        'passive_name': '暗杀者',
    },
    'skill_reflex': {
        'sequence': 'GGCTAGCTAG',  # 前6位B序列 GGCTAG
        'recessive_sequence': 'aaaaaaaaaaaa',
        'dominant': True,
        'vital': False,
        'description': '条件反射被动基因 — 纯合BB获得条件反射效果',
        'category': 'passive',
        'passive_name': '条件反射',
    },

    # ==================== 被动技能基因 ====================
    'thorns': {
        'sequence': 'ATGCGTTTTTT',  # 前6位B序列+后6位全T(最大反射加成)
        'recessive_sequence': 'aaaaaaaaaaaa',
        'dominant': True,
        'vital': False,
        'description': '荆棘被动基因 — 纯合BB获得荆棘反伤',
        'category': 'passive',
        'passive_name': '荆棘',
    },

    # ==================== 特殊基因 ====================
    'luck': {
        'sequence': 'ATGCGCGCGG',
        'recessive_sequence': 'atgcgcgcag',
        'dominant': True,
        'vital': False,
        'description': '幸运值基因',
        'category': 'special',
        'affects_trait': 'luck',
    },
    'charisma': {
        'sequence': 'GCATATATCC',
        'recessive_sequence': 'gcatataacc',
        'dominant': True,
        'vital': False,
        'description': '魅力基因',
        'category': 'special',
        'affects_trait': 'charisma',
    },
    'adaptability': {
        'sequence': 'TATATATGCA',
        'recessive_sequence': 'tatatatgat',
        'dominant': True,
        'vital': False,
        'description': '环境适应基因',
        'category': 'special',
        'affects_trait': 'adaptability',
    },
    'mutation_resistance': {
        'sequence': 'GCGCATATAA',
        'recessive_sequence': 'gcgcataaag',
        'dominant': True,
        'vital': False,
        'description': '抗突变基因',
        'category': 'special',
        'affects_trait': 'mutation_resistance',
    },
    'size_control': {
        'sequence': 'ATATGCGCGT',
        'recessive_sequence': 'atatgcgcaa',
        'dominant': True,
        'vital': False,
        'description': '体型控制基因',
        'category': 'special',
        'affects_trait': 'size',
    },
    'lifespan': {
        'sequence': 'CGCGTATATT',
        'recessive_sequence': 'cgcgtataaa',
        'dominant': True,
        'vital': False,
        'description': '寿命基因',
        'category': 'special',
        'affects_trait': 'lifespan',
    },
    'fertility': {
        'sequence': 'TATATATCGG',
        'recessive_sequence': 'tatatatcaa',
        'dominant': True,
        'vital': False,
        'description': '生育能力基因',
        'category': 'special',
        'affects_trait': 'fertility',
    },
    'senses': {
        'sequence': 'GCGCGCGCGA',
        'recessive_sequence': 'gcgcgcgcag',
        'dominant': True,
        'vital': False,
        'description': '感官增强基因',
        'category': 'special',
        'affects_trait': 'senses',
    },

    # ==================== 隐性基因 - 需要特定条件表达 ====================
    'hybrid_vigor': {
        'sequence': 'ATATCGCTAG',
        'recessive_sequence': 'atatcgctat',
        'dominant': False,
        'vital': False,
        'description': '杂种优势基因',
        'category': 'recessive',
        'affects_trait': 'hybrid_bonus',
    },
    'recessive_power': {
        'sequence': 'GCGCATATAG',
        'recessive_sequence': 'gcgcataaac',
        'dominant': False,
        'vital': False,
        'description': '隐性强化基因',
        'category': 'recessive',
        'affects_trait': 'power_boost',
    },
    'ancient_gene': {
        'sequence': 'TATATATATC',
        'recessive_sequence': 'tatataaaag',
        'dominant': False,
        'vital': False,
        'description': '远古基因片段',
        'category': 'recessive',
        'affects_trait': 'ancient_power',
    },

    # ==================== 抽卡限定技能基因 (仅通过抽卡获得) ====================
    # 剧毒之池 (解锁:第1关)
    'skill_toxic_nova': {
        'sequence': 'GCATCGATGCG',
        'recessive_sequence': 'aaaaaaaaaaaa',
        'dominant': False,
        'vital': False,
        'description': '剧毒新星基因 — 全体中毒爆发【抽卡限定】',
        'category': 'skill',
        'skill_name': '剧毒新星',
        'gacha_only': True,
    },
    'skill_corrosive_touch': {
        'sequence': 'TAGCTAGCATA',
        'recessive_sequence': 'aaaaaaaaaaaa',
        'dominant': False,
        'vital': False,
        'description': '腐蚀之触基因 — 单体减防+中毒+debuff增伤【抽卡限定】',
        'category': 'skill',
        'skill_name': '腐蚀之触',
        'gacha_only': True,
    },
    # 烈焰之池 (解锁:第30关)
    'skill_inferno': {
        'sequence': 'CGATCGTAGCT',
        'recessive_sequence': 'aaaaaaaaaaaa',
        'dominant': False,
        'vital': False,
        'description': '炼狱之火基因 — 全体灼烧+易伤【抽卡限定】',
        'category': 'skill',
        'skill_name': '炼狱之火',
        'gacha_only': True,
    },
    'skill_ember_revival': {
        'sequence': 'ATCGATCGATC',
        'recessive_sequence': 'aaaaaaaaaaaa',
        'dominant': False,
        'vital': False,
        'description': '余烬复燃基因 — 击杀溅射+灼烧爆发【抽卡限定】',
        'category': 'skill',
        'skill_name': '余烬复燃',
        'gacha_only': True,
    },
    # 冰霜之池 (解锁:第50关)
    'skill_permafrost': {
        'sequence': 'GCTAGCTAGCT',
        'recessive_sequence': 'aaaaaaaaaaaa',
        'dominant': False,
        'vital': False,
        'description': '永冻领域基因 — 全体冰冻+伤害加深【抽卡限定】',
        'category': 'skill',
        'skill_name': '永冻领域',
        'gacha_only': True,
    },
    'skill_absolute_zero': {
        'sequence': 'TATATACGCGT',
        'recessive_sequence': 'aaaaaaaaaaaa',
        'dominant': False,
        'vital': False,
        'description': '绝对零度基因 — 冰冻碎击3倍伤害【抽卡限定】',
        'category': 'skill',
        'skill_name': '绝对零度',
        'gacha_only': True,
    },
    # 血池 (解锁:第70关)
    'skill_bloodthirst': {
        'sequence': 'CGCGCGTAATA',
        'recessive_sequence': 'aaaaaaaaaaaa',
        'dominant': False,
        'vital': False,
        'description': '血之渴望基因 — 流血+击杀回血【抽卡限定】',
        'category': 'skill',
        'skill_name': '血之渴望',
        'gacha_only': True,
    },
    'skill_crimson_storm': {
        'sequence': 'ATATATATGCG',
        'recessive_sequence': 'aaaaaaaaaaaa',
        'dominant': False,
        'vital': False,
        'description': '猩红风暴基因 — 全体流血3倍伤【抽卡限定】',
        'category': 'skill',
        'skill_name': '猩红风暴',
        'gacha_only': True,
    },
    # 终焉之池 (解锁:第90关)
    'skill_omnibus_end': {
        'sequence': 'TGCATGCATGC',
        'recessive_sequence': 'aaaaaaaaaaaa',
        'dominant': False,
        'vital': False,
        'description': '万象终结基因 — 每种debuff+30%伤害【抽卡限定】',
        'category': 'skill',
        'skill_name': '万象终结',
        'gacha_only': True,
    },
    'skill_status_resonance': {
        'sequence': 'GATCGATCGAT',
        'recessive_sequence': 'aaaaaaaaaaaa',
        'dominant': False,
        'vital': False,
        'description': '状态共鸣基因 — 利用全屏debuff增伤并转移【抽卡限定】',
        'category': 'skill',
        'skill_name': '状态共鸣',
        'gacha_only': True,
    },
}

# ==========================================
# 技能映射配置 - 基因名称 -> 技能名称
# ==========================================
SKILL_TRAITS = {
    'skill_fire': '火焰吐息',
    'skill_ice': '冰霜护盾',
    'skill_lightning': '雷击',
    'skill_poison': '毒液攻击',
    'skill_heal': '自我修复',
    'skill_shield': '能量护盾',
    'skill_illusion': '幻觉制造',
    'skill_teleport': '瞬移',
    'skill_sleep': '睡眠诱导',
    'skill_paralyze': '麻痹神经',
    'skill_absorption': '能量吸收',
    'skill_summon': '召唤',
    'skill_invisibility': '隐身',
    'skill_explosion': '自爆',
    'skill_growth': '快速生长',
    'skill_observe': '观星',
    'skill_surge': '澎湃',
    'skill_heal_team': '甘霖',
    'skill_freeze': '冻结',
    'skill_curse': '诅咒',
    'skill_burn': '灼烧',
    'skill_execute': '处决',
    'skill_aoe_poison': '毒雾扩散',
    'skill_rewind': '时光倒流',
    'skill_revive': '亡灵复苏',
    'skill_toxic_nova': '剧毒新星',
    'skill_corrosive_touch': '腐蚀之触',
    'skill_inferno': '炼狱之火',
    'skill_ember_revival': '余烬复燃',
    'skill_permafrost': '永冻领域',
    'skill_absolute_zero': '绝对零度',
    'skill_bloodthirst': '血之渴望',
    'skill_crimson_storm': '猩红风暴',
    'skill_omnibus_end': '万象终结',
    'skill_status_resonance': '状态共鸣',
}

# ==========================================
# 染色体布局 - 基因在染色体上的分布
# ==========================================
CHROMOSOME_LAYOUT = {
    'chr1': {
        'name': '第1染色体',
        'type': 'autosome',
        'genes': ['health', 'stamina', 'defense', 'dodge', 'health_maintain', 'metabolism',
                  'skill_ice', 'skill_shield', 'skill_heal', 'skill_absorption',
                  'skill_freeze', 'skill_rewind'],
    },
    'chr2': {
        'name': '第2染色体',
        'type': 'autosome',
        'genes': ['attack', 'speed', 'critical', 'reproduction', 'nervous', 'immune',
                  'skill_fire', 'skill_lightning', 'skill_poison', 'skill_sleep',
                  'skill_burn', 'skill_execute'],
    },
    'chr3': {
        'name': '第3染色体',
        'type': 'autosome',
        'genes': ['skill_paralyze', 'skill_summon', 'skill_growth', 'skill_illusion',
                  'skill_teleport', 'skill_invisibility', 'skill_explosion',
                  'skill_observe', 'skill_surge', 'skill_heal_team',
                  'skill_assassin', 'skill_reflex',
                  'luck', 'charisma', 'adaptability', 'thorns',
                  'skill_curse', 'skill_aoe_poison', 'skill_revive'],
    },
    'chrX': {
        'name': 'X染色体',
        'type': 'sex',
        'genes': ['mutation_resistance', 'size_control', 'lifespan', 'fertility',
                  'senses', 'hybrid_vigor', 'recessive_power'],
    },
    'chrY': {
        'name': 'Y染色体',
        'type': 'sex',
        'genes': ['ancient_gene'],
    },
    'chrG': {
        'name': '隐藏基因片段',
        'type': 'gacha',
        'genes': ['skill_toxic_nova', 'skill_corrosive_touch',
                  'skill_inferno', 'skill_ember_revival',
                  'skill_permafrost', 'skill_absolute_zero',
                  'skill_bloodthirst', 'skill_crimson_storm',
                  'skill_omnibus_end', 'skill_status_resonance'],
    },
}

# 染色体ID列表
CHROMOSOME_IDS = ['chr1', 'chr2', 'chr3', 'chrX', 'chrY', 'chrG']

# ==========================================
# 基因分类列表 - 用于UI显示和组织
# ==========================================
GENE_CATEGORIES = {
    'stat': '基础属性',
    'vital': '关键基因',
    'skill': '技能基因',
    'special': '特殊基因',
    'recessive': '隐性基因',
}

# ==========================================
# 基因区域坐标 - 每条染色体上基因的起始/结束位置
# ==========================================
def _compute_gene_regions():
    regions = {}
    for chr_id, chr_conf in CHROMOSOME_LAYOUT.items():
        cur = []
        start = 0
        for gene_name in chr_conf['genes']:
            tmpl = GENE_TEMPLATES.get(gene_name, {})
            seq_len = len(tmpl.get('sequence', 'ATGCATGC'))
            cur.append((gene_name, start, start + seq_len))
            start += seq_len
        regions[chr_id] = cur
    return regions

GENE_REGIONS = _compute_gene_regions()

# ==========================================
# 关键基因列表 - 死亡判定使用
# ==========================================
# 染色体目标总长（基因只占开头一部分，其余为空填充区域）
CHROMOSOME_LENGTH = {'chr1': 1000, 'chr2': 1000, 'chr3': 1000, 'chrX': 700, 'chrY': 100, 'chrG': 200}
VITAL_GENES = [name for name, data in GENE_TEMPLATES.items() if data.get('vital', False)]

# ==========================================
# 被动技能基因 - B等位基因特征序列
# ==========================================
THORNS_B_SEQUENCE = 'ATGCGT'
ASSASSIN_B_SEQUENCE = 'TTCGAT'
REFLEX_B_SEQUENCE = 'GGCTAG'

# ==========================================
# 被动技能基因列表
# ==========================================
PASSIVE_GENES = [name for name, data in GENE_TEMPLATES.items() if data.get('category') == 'passive']

# ==========================================
# 技能基因列表 - 技能判定使用
# ==========================================
SKILL_GENES = [name for name, data in GENE_TEMPLATES.items() if data.get('category') == 'skill']

# ==========================================
# 可计算性状的基因列表
# ==========================================
TRAIT_GENES = [name for name, data in GENE_TEMPLATES.items() if data.get('affects_trait')]

# ==========================================
# 血脉系统配置
# ==========================================
BLOODLINES = {
    'dragon':  {'name': '龙裔', 'atk': 5, 'hp': 3, 'def': 0, 'spd': 0, 'icon': 'D'},
    'phoenix': {'name': '鳳凰', 'atk': 0, 'hp': 5, 'def': 5, 'spd': 0, 'icon': 'P'},
    'shadow':  {'name': '影暗', 'atk': 2, 'hp': 0, 'def': 0, 'spd': 8, 'icon': 'S'},
    'frost':   {'name': '冰霜', 'atk': 0, 'hp': 2, 'def': 3, 'spd': 5, 'icon': 'F'},
    'storm':   {'name': '雷鸣', 'atk': 4, 'hp': 0, 'def': 0, 'spd': 4, 'icon': 'T'},
    'vital':   {'name': '生命', 'atk': 0, 'hp': 8, 'def': 2, 'spd': 0, 'icon': 'V'},
}

FUSION_TABLE = {
    ('dragon', 'phoenix'): 'storm',
    ('phoenix', 'dragon'): 'storm',
    ('shadow', 'frost'): 'vital',
    ('frost', 'shadow'): 'vital',
    ('storm', 'vital'): 'dragon',
    ('vital', 'storm'): 'dragon',
}

# ==========================================
# 技能芯片配置
# ==========================================
CHIP_POOLS = {
    'freeze_chip':     {'name': '冻结芯片',   'skill': '冻结',    'rarity': 1},
    'shield_chip':     {'name': '护盾芯片',   'skill': '冰霜护盾', 'rarity': 1},
    'heal_chip':       {'name': '治疗芯片',   'skill': '自我修复', 'rarity': 1},
    'growth_chip':     {'name': '成长芯片',   'skill': '快速生长', 'rarity': 2},
    'curse_chip':      {'name': '诅咒芯片',   'skill': '诅咒',    'rarity': 2},
    'poison_nova_chip':{'name': '剧毒芯片',   'skill': '剧毒新星', 'rarity': 3},
    'freeze_domain_chip':{'name':'永冻芯片',  'skill': '永冻领域', 'rarity': 3},
    'absolute_chip':   {'name': '绝对零度芯片','skill':'绝对零度', 'rarity': 4},
}

# ==========================================
# 模组配置
# ==========================================
MODULE_POOLS = {
    'atk_mod_1':  {'name':'攻击芯片L1',  'stat':'attack',  'pct':8,  'level':1},
    'hp_mod_1':   {'name':'生命核心L1',  'stat':'health',  'pct':10, 'level':1},
    'def_mod_1':  {'name':'防御护甲L1',  'stat':'defense', 'pct':8,  'level':1},
    'spd_mod_1':  {'name':'速度引擎L1',  'stat':'speed',   'pct':6,  'level':1},
    'atk_mod_2':  {'name':'攻击芯片L2',  'stat':'attack',  'pct':16, 'level':2},
    'hp_mod_2':   {'name':'生命核心L2',  'stat':'health',  'pct':20, 'level':2},
    'def_mod_2':  {'name':'防御护甲L2',  'stat':'defense', 'pct':16, 'level':2},
    'spd_mod_2':  {'name':'速度引擎L2',  'stat':'speed',   'pct':12, 'level':2},
    'atk_mod_3':  {'name':'攻击芯片L3',  'stat':'attack',  'pct':25, 'level':3},
    'hp_mod_3':   {'name':'生命核心L3',  'stat':'health',  'pct':30, 'level':3},
}

MODULE_MERGE = {
    1: 2,  # 2个L1→1个L2
    2: 3,  # 2个L2→1个L3
}

# ==========================================
# 主题挑战因子（从PC版移植）
# ==========================================
CHALLENGE_FACTORS = [
    # ── 远古遗迹 ──
    {'id': 'field_expand',         'name': '战场扩张',   'desc': '敌方格子扩大至5x5',                             'group': '战场', 'icon': '🗺️', 'prereq': None,     'exclusive': None, 'theme': 'ancient_ruins', 'points': 10},
    {'id': 'iron_formation',       'name': '钢铁之阵',   'desc': '敌方的阵型无法被打乱',                           'group': '阵地', 'icon': '🛡️', 'prereq': None,     'exclusive': None, 'theme': 'ancient_ruins', 'points': 15},
    {'id': 'boulder_fill',         'name': '巨石填充',   'desc': '敌方初始空格子以巨石填充，巨石获得速度与攻击力',   'group': '巨石', 'icon': '🪨', 'prereq': None,     'exclusive': None, 'theme': 'ancient_ruins', 'points': 20},
    {'id': 'purify_stone',         'name': '净化之石',   'desc': '巨石替换为巨石材质净化器，获得净化器被动',         'group': '巨石', 'icon': '💎', 'prereq': 'boulder_fill', 'exclusive': None, 'theme': 'ancient_ruins', 'points': 30},
    {'id': 'swarm_stack',          'name': '虫群叠嶂',   'desc': '圣甲虫群可以堆叠，显示数量x，单体打1层AOE打全部',  'group': '虫群', 'icon': '🦟', 'prereq': None,     'exclusive': None, 'theme': 'ancient_ruins', 'points': 15},
    {'id': 'swarm_reproduce',      'name': '虫群繁衍',   'desc': '圣甲虫群每3回合在当前格生成一个圣甲虫群',          'group': '虫群', 'icon': '🪺', 'prereq': 'swarm_stack', 'exclusive': None, 'theme': 'ancient_ruins', 'points': 25},
    {'id': 'rapid_reproduce',      'name': '急速繁殖',   'desc': '圣甲虫群的繁殖冷却缩减至1回合',                   'group': '虫群', 'icon': '⚡', 'prereq': 'swarm_reproduce', 'exclusive': None, 'theme': 'ancient_ruins', 'points': 40},
    {'id': 'swarm_attach',         'name': '虫附于身',   'desc': '圣甲虫群可以在任意单位上堆叠',                     'group': '虫群', 'icon': '🦗', 'prereq': 'swarm_stack', 'exclusive': None, 'theme': 'ancient_ruins', 'points': 20},
    {'id': 'swarm_remains',        'name': '虫爆遗骸',   'desc': '巨石守卫死亡时以自身3x3范围生成圣甲虫群',          'group': '虫群', 'icon': '💥', 'prereq': 'swarm_stack', 'exclusive': None, 'theme': 'ancient_ruins', 'points': 25},
    {'id': 'titan_summon',         'name': '泰坦召唤',   'desc': '泰坦守卫替换封印之门召唤的古代战士',               'group': '遗迹', 'icon': '🗿', 'prereq': None,     'exclusive': None, 'theme': 'ancient_ruins', 'points': 25},
    {'id': 'swarm_alt',            'name': '虫群替代',   'desc': '封印之门无空格子时召唤圣甲虫群',                   'group': '遗迹', 'icon': '🔄', 'prereq': 'swarm_stack', 'exclusive': None, 'theme': 'ancient_ruins', 'points': 30},
    {'id': 'priest_shield',        'name': '祭司溢能·护盾', 'desc': '古代祭司治疗的溢出量将转化为护盾',             'group': '祭司', 'icon': '🔵', 'prereq': None,     'exclusive': 'priest', 'theme': 'ancient_ruins', 'points': 15},
    {'id': 'priest_poison',        'name': '祭司溢能·毒奶', 'desc': '古代祭司治疗溢出量对己方血量最多/最少单位造成伤害', 'group': '祭司', 'icon': '🟢', 'prereq': None, 'exclusive': 'priest', 'theme': 'ancient_ruins', 'points': 35},
    {'id': 'titan_reduce',         'name': '泰坦庇护·减伤', 'desc': '泰坦守卫周围3x3内敌人获得50%伤害减免',          'group': '泰坦', 'icon': '🛡️', 'prereq': 'titan_summon', 'exclusive': 'titan', 'theme': 'ancient_ruins', 'points': 30},
    {'id': 'titan_transfer',       'name': '泰坦庇护·承伤', 'desc': '泰坦守卫周围3x3内敌人伤害由泰坦承担',           'group': '泰坦', 'icon': '🔗', 'prereq': 'titan_summon', 'exclusive': 'titan', 'theme': 'ancient_ruins', 'points': 40},

    # ── 实验体暴乱 ──
    {'id': 'field_expand',         'name': '战场扩张',     'desc': '敌方格子扩大至5x5',                              'group': '战场', 'icon': '🗺️', 'prereq': None,     'exclusive': None, 'theme': 'subject_rampage', 'points': 10},
    {'id': 'team_4',               'name': '四人小队',     'desc': '我方队伍只能编入4张卡牌',                         'group': '队伍', 'icon': '👥', 'prereq': None,     'exclusive': 'team_3', 'theme': 'subject_rampage', 'points': 10},
    {'id': 'team_3',               'name': '三人小队',     'desc': '我方队伍只能编入3张卡牌',                         'group': '队伍', 'icon': '👤', 'prereq': 'team_4',  'exclusive': 'team_4', 'theme': 'subject_rampage', 'points': 20},
    {'id': 'gene_mutate',          'name': '基因突变',     'desc': '"野生实验体"替换为"变异实验体"',                  'group': '变异', 'icon': '🧬', 'prereq': None,     'exclusive': 'elite_force', 'theme': 'subject_rampage', 'points': 10},
    {'id': 'elite_force',          'name': '精英集结',     'desc': '"野生实验体"替换为"精英实验体"',                  'group': '精英', 'icon': '⭐', 'prereq': None,     'exclusive': 'gene_mutate', 'theme': 'subject_rampage', 'points': 20},
    {'id': 'subject_shield_focus', 'name': '极寒护盾',     'desc': '"守卫实验体"只会释放"冰霜护盾"技能',              'group': '护盾', 'icon': '❄️', 'prereq': None,    'exclusive': None, 'theme': 'subject_rampage', 'points': 5},
    {'id': 'subject_shield_boost', 'name': '冰霜壁垒',     'desc': '"守卫实验体"的"冰霜护盾"提供的护盾量增加',        'group': '护盾', 'icon': '🧊', 'prereq': 'subject_shield_focus', 'exclusive': None, 'theme': 'subject_rampage', 'points': 10},
    {'id': 'subject_shield_team',  'name': '寒霜庇护',     'desc': '"守卫实验体"的"冰霜护盾"额外作用于随机敌人',      'group': '护盾', 'icon': '🛡️', 'prereq': 'subject_shield_focus', 'exclusive': None, 'theme': 'subject_rampage', 'points': 15},
    {'id': 'subject_poison_spread','name': '剧毒扩散',     'desc': '"变异实验体"的"毒液攻击"目标数扩大至3个',         'group': '变异', 'icon': '☠️', 'prereq': 'gene_mutate', 'exclusive': None, 'theme': 'subject_rampage', 'points': 15},
    {'id': 'subject_vampiric',     'name': '吸血体质',     'desc': '"变异实验体"造成伤害时回复等量生命值',            'group': '变异', 'icon': '🩸', 'prereq': 'gene_mutate', 'exclusive': None, 'theme': 'subject_rampage', 'points': 25},
    {'id': 'subject_rapid_evolve', 'name': '快速进化',     'desc': '"精英实验体"每回合随机获得一种增益效果，全场可叠加', 'group': '精英', 'icon': '⚡', 'prereq': 'elite_force', 'exclusive': None, 'theme': 'subject_rampage', 'points': 25},
    {'id': 'subject_summon_ritual','name': '召唤仪式',     'desc': '首领敌人每3次行动额外释放一次召唤',               'group': '召唤', 'icon': '🔮', 'prereq': None,    'exclusive': None, 'theme': 'subject_rampage', 'points': 15},
    {'id': 'subject_double_summon','name': '双重召唤',     'desc': '首领敌人每次行动额外释放两次召唤',                'group': '召唤', 'icon': '🔁', 'prereq': 'subject_summon_ritual', 'exclusive': None, 'theme': 'subject_rampage', 'points': 35},
    {'id': 'subject_boss_descent', 'name': '首领降临',     'desc': '"首领实验体(增强版)"替换"首领实验体"',            'group': '首领', 'icon': '👑', 'prereq': None,    'exclusive': None, 'theme': 'subject_rampage', 'points': 30},
    {'id': 'subject_all_mastery',  'name': '全能掌握',     'desc': '"首领实验体(增强版)"额外获得首领实验体的全部技能','group': '首领', 'icon': '📚', 'prereq': 'subject_boss_descent', 'exclusive': None, 'theme': 'subject_rampage', 'points': 10},
    {'id': 'subject_full_power',   'name': '全力释放',     'desc': '首领敌人每次行动会同时释放全部技能(包含普通攻击)','group': '首领', 'icon': '💥', 'prereq': None,    'exclusive': None, 'theme': 'subject_rampage', 'points': 35},
    {'id': 'subject_crushing_blow','name': '碾压之击',     'desc': '"首领实验体(增强版)"的普通攻击会命中对方全体卡牌', 'group': '首领', 'icon': '🔨', 'prereq': 'subject_boss_descent', 'exclusive': None, 'theme': 'subject_rampage', 'points': 20},
    {'id': 'subject_full_screen',  'name': '全屏审判',     'desc': '"首领实验体(增强版)"的技能会以对方全体卡牌为目标', 'group': '首领', 'icon': '⚔️', 'prereq': 'subject_boss_descent', 'exclusive': None, 'theme': 'subject_rampage', 'points': 35},
    {'id': 'subject_chain_reaction','name': '连动狂潮',    'desc': '首领敌人每次行动后额外行动一次',                  'group': '首领', 'icon': '🌀', 'prereq': None,    'exclusive': None, 'theme': 'subject_rampage', 'points': 35},
    {'id': 'subject_back_row',     'name': '后排统帅',     'desc': '首领敌人的初始位置改变(变为在后排)',              'group': '首领', 'icon': '📐', 'prereq': None,    'exclusive': None, 'theme': 'subject_rampage', 'points': 10},
    {'id': 'subject_immortal',     'name': '不朽实验体',   'desc': '"首领实验体(增强版)"死亡时以50%HP复活一次，复活后属性+30%', 'group': '首领', 'icon': '♾️', 'prereq': 'subject_boss_descent', 'exclusive': None, 'theme': 'subject_rampage', 'points': 30},
    {'id': 'subject_gene_boost',   'name': '基因强化',     'desc': '所有敌人基础HP和ATK提升20%',                     'group': '强化', 'icon': '💪', 'prereq': None,    'exclusive': None, 'theme': 'subject_rampage', 'points': 15},
    {'id': 'subject_super_gene',   'name': '超级基因',     'desc': '所有敌人基础HP和ATK提升40%',                     'group': '强化', 'icon': '🔥', 'prereq': None,    'exclusive': None, 'theme': 'subject_rampage', 'points': 25},

    # ── 废弃实验室 ──
    {'id': 'corrosive_slime',         'name': '腐蚀减速',   'desc': '"腐蚀黏液怪"同时降低玩家卡牌的速度10%',                              'group': '黏液', 'icon': '🟢', 'prereq': None,   'exclusive': None, 'theme': 'abandoned_lab', 'points': 15},
    {'id': 'eye_dual_lock',           'name': '双瞳锁定',   'desc': '"眼梗怪"额外锁定生命次低的卡牌',                                       'group': '眼梗', 'icon': '👁️', 'prereq': None,   'exclusive': None, 'theme': 'abandoned_lab', 'points': 20},
    {'id': 'eye_true_sight',          'name': '真实视野',   'desc': '"眼梗怪"的攻击无视前后排限制，无视嘲讽，无视"潜行""隐身"等效果',       'group': '眼梗', 'icon': '🔍', 'prereq': None,   'exclusive': None, 'theme': 'abandoned_lab', 'points': 25},
    {'id': 'eye_poison_tip',          'name': '毒液弹头',   'desc': '"眼梗怪"的攻击造成中毒效果',                                            'group': '眼梗', 'icon': '☠️', 'prereq': None,   'exclusive': None, 'theme': 'abandoned_lab', 'points': 15},
    {'id': 'eye_sniper_ramp',         'name': '狙击递增',   'desc': '"眼梗怪"攻击同一单位伤害逐渐增加（20%），切换单位时重置',              'group': '眼梗', 'icon': '📈', 'prereq': None,   'exclusive': None, 'theme': 'abandoned_lab', 'points': 20},
    {'id': 'eye_kill_memory',         'name': '杀戮记忆',   'desc': '"眼梗怪"切换单位时造成的伤害不重置',                                    'group': '眼梗', 'icon': '🧠', 'prereq': 'eye_sniper_ramp', 'exclusive': None, 'theme': 'abandoned_lab', 'points': 35},
    {'id': 'eye_overflow',            'name': '溢伤追击',   'desc': '"眼梗怪"杀死目标时溢出的伤害会立刻作用于下一个目标',                    'group': '眼梗', 'icon': '💫', 'prereq': None,   'exclusive': None, 'theme': 'abandoned_lab', 'points': 35},
    {'id': 'eye_death_mark',          'name': '死亡标记',   'desc': '"眼梗怪"锁定的目标会被所有敌人锁定',                                    'group': '眼梗', 'icon': '🎯', 'prereq': None,   'exclusive': None, 'theme': 'abandoned_lab', 'points': 25},
    {'id': 'containment_breach',      'name': '收容泄露',   'desc': '"收容单元"死亡后在当前位置生成"暴走究极体"',                            'group': '收容', 'icon': '💥', 'prereq': None,   'exclusive': None, 'theme': 'abandoned_lab', 'points': 30},
    {'id': 'toxic_miasma',            'name': '毒瘴笼罩',   'desc': '"毒气泄漏口"的毒范围扩大至全体我方卡牌',                                'group': '毒气', 'icon': '🌫️', 'prereq': None,  'exclusive': None, 'theme': 'abandoned_lab', 'points': 25},
    {'id': 'toxic_permanent',         'name': '永久污染',   'desc': '"剧毒废料桶"死亡产生的毒气持续整场战斗',                                'group': '毒气', 'icon': '♾️', 'prereq': None,  'exclusive': None, 'theme': 'abandoned_lab', 'points': 25},
    {'id': 'toxic_spawn',             'name': '二次污染',   'desc': '"剧毒废料桶"死亡时，在自身位置生成一个"毒气泄漏口"',                    'group': '毒气', 'icon': '🔄', 'prereq': None,  'exclusive': None, 'theme': 'abandoned_lab', 'points': 25},
    {'id': 'energy_chain',            'name': '能量链结',   'desc': '"应急发电机"每一次行动可以使前方（左邻居）单位立即行动一次',            'group': '能源', 'icon': '⚡', 'prereq': None,   'exclusive': None, 'theme': 'abandoned_lab', 'points': 30},
    {'id': 'energy_deploy',           'name': '战术部署',   'desc': '"应急发电机"的初始位置改变（位于更具威胁性的单位后方）',                'group': '能源', 'icon': '📐', 'prereq': None,   'exclusive': None, 'theme': 'abandoned_lab', 'points': 15},
    {'id': 'cleaner_immune',          'name': '毒免机体',   'desc': '"清洁机器人"受到的中毒伤害为0',                                        'group': '清洁', 'icon': '🛡️', 'prereq': None,  'exclusive': None, 'theme': 'abandoned_lab', 'points': 10},
    {'id': 'cleaner_absorb',          'name': '毒素回收',   'desc': '"清洁机器人"每次行动会吸收所有敌方的中毒',                              'group': '清洁', 'icon': '🧹', 'prereq': None,   'exclusive': None, 'theme': 'abandoned_lab', 'points': 25},
    {'id': 'cleaner_transfer',        'name': '毒爆转移',   'desc': '"清洁机器人"死亡时会将自身的中毒转移到玩家的一张随机卡牌上',            'group': '清洁', 'icon': '💀', 'prereq': 'cleaner_absorb', 'exclusive': None, 'theme': 'abandoned_lab', 'points': 30},
    {'id': 'poison_chain',            'name': '毒爆连锁',   'desc': '带有"中毒"效果的单位死亡时，对相邻3x3范围内的所有单位施加1层"中毒"',  'group': '连锁', 'icon': '🔗', 'prereq': None,   'exclusive': None, 'theme': 'abandoned_lab', 'points': 25},
    {'id': 'void_corrosion',          'name': '虚空蚀化',   'desc': '我方卡牌每回合获得一层中毒',                                            'group': '蚀化', 'icon': '🌑', 'prereq': None,   'exclusive': None, 'theme': 'abandoned_lab', 'points': 30},
    {'id': 'flesh_armor',             'name': '血肉强化',   'desc': '全体敌人的血量增加50%',                                                  'group': '强化', 'icon': '🩸', 'prereq': None,   'exclusive': 'reinforce', 'theme': 'abandoned_lab', 'points': 20},
    {'id': 'steel_armor',             'name': '钢铁之躯',   'desc': '全体敌人的血量增加80%',                                                  'group': '强化', 'icon': '🛡️', 'prereq': None,  'exclusive': 'reinforce', 'theme': 'abandoned_lab', 'points': 30},

    # ── 元素轮回 ──
    {'id': 'elem_expand',           'name': '战场扩张',       'desc': '敌方格子扩大至5x5',                                       'group': '战场', 'icon': '⬜', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 10},
    {'id': 'elem_formation',        'name': '钢铁之阵',       'desc': '敌方阵容不可被打乱',                                     'group': '战场', 'icon': '🛡️', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 15},
    {'id': 'elem_fragile',          'name': '脆弱之躯',       'desc': '我方最大生命值减少30%',                                  'group': '战场', 'icon': '💔', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 25},
    {'id': 'elem_speed_light',      'name': '极速追猎',       'desc': '全体敌方速度增加10%',                                    'group': '速度', 'icon': '💨', 'prereq': None,             'exclusive': 'elem_spd',    'theme': 'elemental_cycle', 'points': 10},
    {'id': 'elem_speed_storm',      'name': '疾风迅雷',       'desc': '全体敌方速度增加20%（与极速追猎互斥）',                  'group': '速度', 'icon': '⚡', 'prereq': None,             'exclusive': 'elem_spd',    'theme': 'elemental_cycle', 'points': 20},
    {'id': 'elem_pact_short',       'name': '血祭契约·短暂',  'desc': '我方单位每次行动受到15%最大生命真实伤害，4次行动后消失',   'group': '契约', 'icon': '🩸', 'prereq': None,             'exclusive': 'elem_pact',   'theme': 'elemental_cycle', 'points': 20},
    {'id': 'elem_pact_long',        'name': '血祭契约·持久',  'desc': '我方单位每次行动受到15%最大生命真实伤害，8次行动后消失',   'group': '契约', 'icon': '🩸', 'prereq': None,             'exclusive': 'elem_pact',   'theme': 'elemental_cycle', 'points': 30},
    {'id': 'elem_pact_eternal',     'name': '血祭契约·永恒',  'desc': '我方单位每次行动受到15%最大生命真实伤害',                  'group': '契约', 'icon': '🩸', 'prereq': None,             'exclusive': 'elem_pact',   'theme': 'elemental_cycle', 'points': 40},
    {'id': 'elem_reso_offense',     'name': '元素共鸣·强攻',  'desc': '每存活一个元素，所有元素攻击+5%',                         'group': '共鸣', 'icon': '🔥', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 25},
    {'id': 'elem_reso_defense',     'name': '元素共鸣·壁垒',  'desc': '每存活一个元素，所有元素生命值+10%',                      'group': '共鸣', 'icon': '🛡️', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 25},
    {'id': 'elem_reso_speed',       'name': '元素共鸣·疾走',  'desc': '每存活一个元素，所有元素速度+5%',                        'group': '共鸣', 'icon': '💨', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 25},
    {'id': 'elem_reso_mastery',     'name': '元素共鸣·强化',  'desc': '共鸣数值翻倍（需已选至少2个共鸣因子）',                    'group': '共鸣', 'icon': '💎', 'prereq': '__reso_count2__', 'exclusive': None,          'theme': 'elemental_cycle', 'points': 40},
    {'id': 'elem_core_extra',       'name': '核能连动',       'desc': '每存活一个元素，元素之核行动后立刻额外行动一次',            'group': '核心', 'icon': '🔄', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 35},
    {'id': 'elem_core_scatter',     'name': '核能散射',       'desc': '每存活一个元素，元素之核的攻击目标会额外+1',              'group': '核心', 'icon': '💥', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 30},
    {'id': 'elem_assimilation',     'name': '元素同化',       'desc': '每存活一个元素，其他所有元素攻击均附带该元素的效果',        'group': '同化', 'icon': '🔀', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 40},
    {'id': 'elem_resistance',       'name': '元素抗性',       'desc': '元素免疫自身属性的伤害及buff',                             'group': '领域', 'icon': '🔰', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 15},
    {'id': 'elem_domain',           'name': '元素领域',       'desc': '场上所有元素免疫现存元素相关属性的伤害及buff',              'group': '领域', 'icon': '🌐', 'prereq': 'elem_resistance', 'exclusive': None,          'theme': 'elemental_cycle', 'points': 35},
    {'id': 'elem_cycle_fire',       'name': '烈焰轮回',       'desc': '烈焰元素死亡时会复活成为冰川元素',                         'group': '轮回', 'icon': '🔥', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 20},
    {'id': 'elem_cycle_ice',        'name': '冰川轮回',       'desc': '冰川元素死亡时会复活成为大地元素',                         'group': '轮回', 'icon': '❄️', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 20},
    {'id': 'elem_cycle_earth',      'name': '大地轮回',       'desc': '大地元素死亡时会复活成为雷霆元素',                         'group': '轮回', 'icon': '🪨', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 20},
    {'id': 'elem_cycle_thunder',    'name': '雷霆轮回',       'desc': '雷霆元素死亡时会复活成为自然元素',                         'group': '轮回', 'icon': '⚡', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 20},
    {'id': 'elem_summon_primal',    'name': '原始登场',       'desc': '原始元素出现在场中',                                      'group': '登场', 'icon': '🌌', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 20},
    {'id': 'elem_summon_shadow',    'name': '暗光登场',       'desc': '暗之元素和光之元素出现在场中',                              'group': '登场', 'icon': '🌓', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 10},
    {'id': 'elem_summon_crystal',   'name': '冰棱登场',       'desc': '冰晶元素和棱晶元素出现在场中',                              'group': '登场', 'icon': '💎', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 10},
    {'id': 'elem_entropy',          'name': '熵能侵蚀',       'desc': '被原始元素攻击的目标每次损失5%最大生命值（可叠8层）',      'group': '熵能', 'icon': '☢️', 'prereq': 'elem_summon_primal', 'exclusive': None,        'theme': 'elemental_cycle', 'points': 30},
    {'id': 'elem_buff_permanent',   'name': '永恒增益',       'desc': '所有buff的层数不会减少（敌我双方）',                       'group': '狂潮', 'icon': '♾️', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 30},
    {'id': 'elem_frenzy',           'name': '元素狂潮',       'desc': '敌方单位行动时额外释放一次随机技能',                       'group': '狂潮', 'icon': '🌪️', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 30},
    {'id': 'elem_mourning',         'name': '元素哀恸',       'desc': '每有一个元素死亡时，其他元素立刻行动一次',                  'group': '狂潮', 'icon': '💀', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 35},
    {'id': 'elem_obliteration',     'name': '毁灭之力',       'desc': '敌方攻击增加50%',                                         'group': '狂潮', 'icon': '☠️', 'prereq': None,             'exclusive': None,          'theme': 'elemental_cycle', 'points': 30},

    # ── 盲盒战争 ──
    {'id': 'bb_expand',          'name': '战场扩张',    'desc': '敌方格子扩大至5x5',                                'group': '战场', 'icon': '🗺️', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 10},
    {'id': 'bb_formation',       'name': '钢铁之阵',    'desc': '敌方阵型无法被打乱',                                'group': '阵型', 'icon': '🛡️', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 15},
    {'id': 'bb_team_4',          'name': '四人小队',    'desc': '我方队伍只能编入4张卡牌',                            'group': '队伍', 'icon': '👥', 'prereq': None,             'exclusive': 'bb_team_3',   'theme': 'blind_box_war', 'points': 10},
    {'id': 'bb_team_3',          'name': '三人小队',    'desc': '我方队伍只能编入3张卡牌',                            'group': '队伍', 'icon': '👤', 'prereq': 'bb_team_4',       'exclusive': 'bb_team_4',   'theme': 'blind_box_war', 'points': 20},
    {'id': 'bb_5_waves',         'name': '五波攻势',    'desc': '战斗变为5波，每波5x5填满，状态保留',                'group': '波次', 'icon': '🌊', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 20},
    {'id': 'bb_wave_boost',      'name': '波次递增',    'desc': '每波敌人获得递增强化(攻/血/速/技能)',               'group': '波次', 'icon': '📈', 'prereq': 'bb_5_waves',       'exclusive': None,          'theme': 'blind_box_war', 'points': 25},
    {'id': 'bb_resonance',       'name': '波次回响',    'desc': '每波盲盒行动时，每存活敌方对全体我方造成伤害',       'group': '回响', 'icon': '🔊', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 15},
    {'id': 'bb_resonance_amp',   'name': '盲盒回响',    'desc': '每存活一个盲盒，波次回响伤害+5%',                   'group': '回响', 'icon': '📯', 'prereq': 'bb_resonance',    'exclusive': None,          'theme': 'blind_box_war', 'points': 15},
    {'id': 'bb_resonance_scale', 'name': '回响增幅',    'desc': '敌方伤害提高可以作用于波次回响上',                   'group': '回响', 'icon': '📊', 'prereq': 'bb_resonance',    'exclusive': None,          'theme': 'blind_box_war', 'points': 20},
    {'id': 'bb_drop',            'name': '盲盒掉落',    'desc': '怪物死亡时40%概率在自身位置生成盲盒',               'group': '盲盒', 'icon': '📦', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 20},
    {'id': 'bb_rare',            'name': '稀有盲盒',    'desc': '盲盒被击破时25%概率召唤精英级怪物',                 'group': '盲盒', 'icon': '🌟', 'prereq': 'bb_drop',        'exclusive': None,          'theme': 'blind_box_war', 'points': 25},
    {'id': 'bb_legendary',       'name': '传说盲盒',    'desc': '盲盒被击破时25%概率召唤首领级怪物',                 'group': '盲盒', 'icon': '👑', 'prereq': 'bb_drop',        'exclusive': None,          'theme': 'blind_box_war', 'points': 35},
    {'id': 'bb_chain',           'name': '盲盒连锁',    'desc': '盲盒被击破时20%概率在相邻空格生成新盲盒',           'group': '盲盒', 'icon': '🔗', 'prereq': 'bb_drop',        'exclusive': None,          'theme': 'blind_box_war', 'points': 25},
    {'id': 'bb_growth',          'name': '盲盒成长',    'desc': '盲盒召唤的怪物每存活5秒攻击力+10%',                 'group': '盲盒', 'icon': '📈', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 30},
    {'id': 'bb_swarm',           'name': '盲盒集群',    'desc': '每存在一个盲盒召唤的怪物，所有该类怪物攻击+5%',     'group': '盲盒', 'icon': '🐝', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 25},
    {'id': 'bb_remains',         'name': '盲盒遗骸',    'desc': '盲盒召唤的怪物死亡时在自身位置生成盲盒',            'group': '盲盒', 'icon': '💀', 'prereq': 'bb_drop',        'exclusive': None,          'theme': 'blind_box_war', 'points': 30},
    {'id': 'bb_charge',          'name': '盲盒蓄力',    'desc': '未击破的盲盒每3秒使召唤怪物属性+10%',              'group': '盲盒', 'icon': '⏳', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 25},
    {'id': 'bb_decay',           'name': '盲盒衰减',    'desc': '盲盒初始召唤加成150%，每5秒衰减25%至最低50%',      'group': '盲盒', 'icon': '💫', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 25},
    {'id': 'bb_precharge',       'name': '盲盒预长',    'desc': '第3波时第4/5波盲盒提前进入蓄力状态',               'group': '盲盒', 'icon': '🔮', 'prereq': 'bb_5_waves',     'exclusive': None,          'theme': 'blind_box_war', 'points': 25},
    {'id': 'bb_hard_shell',      'name': '盲盒坚壳',    'desc': '盲盒需要被攻击两次才能被击破',                      'group': '盲盒', 'icon': '🛡️', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 20},
    {'id': 'bb_spell_shield',    'name': '盲盒法障',    'desc': '盲盒需要至少受到一次技能伤害才能被击破',            'group': '盲盒', 'icon': '🔮', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 20},
    {'id': 'bb_thorns',          'name': '盲盒荆棘',    'desc': '盲盒获得50%反伤的荆棘',                            'group': '盲盒', 'icon': '🌵', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 25},
    {'id': 'bb_drain',           'name': '资源枯竭',    'desc': '每击破一个盲盒，我方行动条减少5%',                 'group': '资源', 'icon': '💧', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 20},
    {'id': 'bb_trap',            'name': '盲盒陷阱',    'desc': '盲盒被击破触发随机负面效果',                       'group': '陷阱', 'icon': '⚠️', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 30},
    {'id': 'bb_activate',        'name': '盲盒激活',    'desc': '盲盒被击破激活随机未选择的挑战因子',               'group': '激活', 'icon': '💥', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 40},
    {'id': 'bb_rnd_stat',        'name': '随机属性',    'desc': '怪物出生时获得随机一项属性加成',                   'group': '随机', 'icon': '🎲', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 20},
    {'id': 'bb_rnd_skill',       'name': '随机技能',    'desc': '怪物出生时额外获得一个随机技能',                   'group': '随机', 'icon': '📖', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 25},
    {'id': 'bb_rnd_passive',     'name': '随机被动',    'desc': '怪物出生时额外获得一个随机被动',                   'group': '随机', 'icon': '✨', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 25},
    {'id': 'bb_balance',         'name': '属性平均',    'desc': '所有怪物攻击/血量/速度属性平均',                   'group': '随机', 'icon': '⚖️', 'prereq': None,             'exclusive': None,          'theme': 'blind_box_war', 'points': 15},
    {'id': 'bb_double_rnd',      'name': '双重抽卡',    'desc': '怪物获得2个随机技能和2个随机被动',                 'group': '随机', 'icon': '🎴', 'prereq': '__bb_double__',  'exclusive': None,          'theme': 'blind_box_war', 'points': 40},
]

CHALLENGE_GROUPS_BY_THEME = {
    'ancient_ruins': ['战场', '阵地', '巨石', '虫群', '遗迹', '祭司', '泰坦'],
    'subject_rampage': ['战场', '队伍', '变异', '精英', '护盾', '首领', '召唤', '强化'],
    'abandoned_lab': ['战场', '队伍', '黏液', '眼梗', '收容', '毒气', '能源', '清洁', '连锁', '蚀化', '强化'],
    'elemental_cycle': ['战场', '速度', '契约', '共鸣', '核心', '同化', '领域', '轮回', '登场', '熵能', '狂潮'],
    'blind_box_war': ['战场', '阵型', '队伍', '波次', '回响', '盲盒', '资源', '陷阱', '激活', '随机'],
}
CHALLENGE_GROUP_ORDER = CHALLENGE_GROUPS_BY_THEME['ancient_ruins']  # 默认
