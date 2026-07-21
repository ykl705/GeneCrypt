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

# ==========================================
# 敌人特质系统（50关后激活）
# ==========================================
ENEMY_TRAITS = {
    'regeneration':    {'name': '再生',   'desc': '每回合恢复5%最大生命',           'type': 'heal',    'value': 0.05, 'weight': 1, 'unlock': 50},
    'berserk':         {'name': '狂暴',   'desc': 'HP<30%时攻击力翻倍',            'type': 'trigger', 'hp_thr': 0.3, 'atk_mul': 2.0, 'weight': 2, 'unlock': 50},
    'toxic':           {'name': '毒域',   'desc': '登场给全体敌方上3层中毒',        'type': 'entry',   'status': 'poison', 'stacks': 3, 'weight': 1, 'unlock': 50},
    'clone':           {'name': '克隆',   'desc': '每3回合在空格复制自身',          'type': 'periodic','interval': 3, 'action': 'clone', 'weight': 2, 'unlock': 60},
    'shielded':        {'name': '护盾',   'desc': '开场获得40%最大生命护盾',        'type': 'entry',   'shield_pct': 0.4, 'weight': 1, 'unlock': 50},
    'thorns':          {'name': '反伤',   'desc': '受到伤害反弹25%',               'type': 'reflect', 'pct': 0.25, 'weight': 1, 'unlock': 50},
    'vampiric':        {'name': '吸血',   'desc': '造成伤害30%转化生命',           'type': 'lifesteal','pct': 0.3, 'weight': 2, 'unlock': 55},
    'pierce':          {'name': '破甲',   'desc': '攻击无视50%防御',              'type': 'pierce',  'pct': 0.5, 'weight': 2, 'unlock': 60},
    'cc_immune':       {'name': '免控',   'desc': '免疫睡眠/麻痹/冻结/混乱',        'type': 'immune',  'weight': 2, 'unlock': 55},
    'death_summon':    {'name': '亡语·召唤','desc': '死亡时召唤2个低级敌人',         'type': 'ondeath', 'action': 'summon', 'count': 2, 'weight': 2, 'unlock': 65},
    'death_poison':    {'name': '亡语·毒爆','desc': '死亡时全体敌方5层中毒',         'type': 'ondeath', 'action': 'poison_all', 'stacks': 5, 'weight': 2, 'unlock': 65},
    'thick_skin':      {'name': '厚皮',   'desc': '最大生命+50%',                'type': 'stat',    'hp_pct': 0.5, 'weight': 1, 'unlock': 50},
    'sharp_claw':      {'name': '利爪',   'desc': '攻击力+30%',                  'type': 'stat',    'atk_pct': 0.3, 'weight': 1, 'unlock': 50},
    'swift':           {'name': '疾风',   'desc': '速度+20%',                   'type': 'stat',    'spd_pct': 0.2, 'weight': 1, 'unlock': 50},
    'headstart':       {'name': '先手',   'desc': '行动条初始80%',               'type': 'entry',   'atb_init': 0.8, 'weight': 2, 'unlock': 70},
}

# ==========================================
# 成就系统
# ==========================================
ACHIEVEMENTS = [
    {'id':'a_battle_1',  'name':'初战告捷', 'desc':'赢得第一场战斗',        'type':'total_wins', 'target':1,    'diff':1, 'reward':{'battle_mats':30}},
    {'id':'a_battle_10', 'name':'百战勇士', 'desc':'赢得100场战斗',         'type':'total_wins', 'target':100,  'diff':2, 'reward':{'battle_mats':200, 'gene_essence':20}},
    {'id':'a_boss_5',    'name':'猎手',    'desc':'击败5个BOSS',            'type':'boss_kills','target':5,    'diff':1, 'reward':{'battle_mats':50}},
    {'id':'a_boss_50',   'name':'BOSS终结者','desc':'击败50个BOSS',         'type':'boss_kills','target':50,   'diff':3, 'reward':{'gacha_currency':300, 'gene_essence':50}},
    {'id':'a_stage_50',  'name':'半百之旅', 'desc':'通关第50关',            'type':'max_stage', 'target':50,   'diff':1, 'reward':{'gacha_currency':150}},
    {'id':'a_stage_100', 'name':'百关突破', 'desc':'通关第100关',           'type':'max_stage', 'target':100,  'diff':2, 'reward':{'gacha_currency':500, 'gene_essence':100}},
    {'id':'a_no_loss_10','name':'完美十战', 'desc':'无阵亡通关10个不同关卡', 'type':'no_loss_count','target':10,'diff':2, 'reward':{'chip':'heal_chip'}},
    {'id':'a_breed_1',   'name':'初代诞生', 'desc':'完成1次繁殖',           'type':'breed_count','target':1,   'diff':1, 'reward':{'battle_mats':20}},
    {'id':'a_breed_50',  'name':'繁殖能手', 'desc':'完成50次繁殖',          'type':'breed_count','target':50,  'diff':2, 'reward':{'gene_essence':30}},
    {'id':'a_breed_200', 'name':'基因传播者','desc':'完成200次繁殖',        'type':'breed_count','target':200, 'diff':3, 'reward':{'chip':'curse_chip', 'gene_essence':100}},
    {'id':'a_card_10',   'name':'收集者',   'desc':'拥有10张卡牌',          'type':'have_cards', 'target':10,  'diff':1, 'reward':{'battle_mats':50}},
    {'id':'a_card_50',   'name':'收藏家',   'desc':'拥有50张卡牌',          'type':'have_cards', 'target':50,  'diff':2, 'reward':{'gacha_currency':200}},
    {'id':'a_star_5',    'name':'星光闪耀', 'desc':'一张卡牌达到5星',       'type':'star_count', 'target':1,   'diff':3, 'reward':{'module':'atk_mod_3'}},
    {'id':'a_bloodline_all','name':'血脉收集者','desc':'拥有全部6种血脉',   'type':'bloodline_collect','target':6,'diff':3,'reward':{'chip':'absolute_chip','gene_essence':200}},
    {'id':'a_chip_equip','name':'芯片初装', 'desc':'给卡牌装备技能芯片',     'type':'chip_equip','target':1,    'diff':1, 'reward':{'chip':'shield_chip'}},
    {'id':'a_module_all','name':'模组收藏家','desc':'拥有每种L3模组至少1个','type':'module_collect','target':4,'diff':3,'reward':{'gacha_currency':500,'gene_essence':150}},
    {'id':'a_training_all','name':'全面训练','desc':'一张卡牌4项属性均完成训练','type':'training_complete','target':1,'diff':2,'reward':{'battle_mats':100}},
    {'id':'a_infinity_30','name':'无尽之始','desc':'挑战模式积分达2000','type':'challenge_score','target':2000,'diff':2,'reward':{'gacha_currency':300}},
    {'id':'a_hidden_immortal','name':'不朽传奇','desc':'一张卡牌在挑战模式中战无不胜','type':'hidden','target':1,'diff':4,'reward':{'card':'不朽龙裔','gene_essence':500,'gacha_currency':1000}},
    {'id':'a_hidden_speed','name':'闪电战',  'desc':'60秒内完成一场挑战',    'type':'hidden','target':1,'diff':3,'reward':{'chip':'freeze_domain_chip','gene_essence':200}},
    {'id':'a_hidden_perfect','name':'完美无缺','desc':'全因子通关盲盒战争',  'type':'hidden','target':1,'diff':5,'reward':{'card':'完美基因体','gene_essence':2000,'gacha_currency':5000}},
]

# ==========================================
# 装备系统
# ==========================================
EQUIPMENT_SLOTS = ['weapon', 'head', 'body', 'accessory', 'boots', 'special']
EQUIPMENT_SLOT_NAMES = {'weapon':'武器','head':'头部','body':'躯干','accessory':'饰品','boots':'鞋子','special':'特殊'}
EQUIPMENT_RARITY = [
    {'id':'common',   'name':'普通', 'color':(0.6,0.6,0.6,1), 'affixes':(1,2), 'prefix':'',  'drop':0.55},
    {'id':'uncommon', 'name':'精品', 'color':(0.2,0.8,0.2,1), 'affixes':(2,3), 'prefix':'精', 'drop':0.25},
    {'id':'rare',     'name':'稀有', 'color':(0.2,0.5,1,1),   'affixes':(3,4), 'prefix':'稀', 'drop':0.12},
    {'id':'epic',     'name':'史诗', 'color':(0.7,0.2,1,1),   'affixes':(4,5), 'prefix':'史', 'drop':0.05},
    {'id':'legend',   'name':'传说', 'color':(1,0.6,0,1),     'affixes':(5,6), 'prefix':'传', 'drop':0.02},
    {'id':'ancient',  'name':'远古', 'color':(0.8,0.6,0.2,1), 'affixes':(6,7), 'prefix':'古', 'drop':0.005},
    {'id':'mythic',   'name':'神话', 'color':(0.2,1,1,1),     'affixes':(7,8), 'prefix':'神', 'drop':0.003},
    {'id':'chaos',    'name':'混沌', 'color':(1,0,0.5,1),     'affixes':(8,9), 'prefix':'沌', 'drop':0.001},
]
EQUIPMENT_AFFIX_POOLS = {
    'common': [
        ('ATK', 'attack', 0, 5, 15), ('HP', 'health', 0, 20, 60),
        ('DEF', 'defense', 0, 3, 10), ('SPD', 'speed', 0, 2, 8),
    ],
    'uncommon': [
        ('ATK', 'attack', 0, 10, 30), ('HP', 'health', 0, 50, 120),
        ('DEF', 'defense', 0, 5, 20), ('SPD', 'speed', 0, 4, 12),
        ('CRT', 'critical_rate', 1, 2, 5), ('DDG', 'dodge_rate', 1, 2, 5),
    ],
    'rare': [
        ('ATK', 'attack', 0, 20, 50), ('HP', 'health', 0, 100, 250),
        ('DEF', 'defense', 0, 10, 35), ('SPD', 'speed', 0, 6, 18),
        ('CRT', 'critical_rate', 1, 5, 10), ('DDG', 'dodge_rate', 1, 5, 10),
        ('KLL', 'lifesteal_pct', 1, 5, 10),
    ],
    'epic': [
        ('ATK', 'attack', 0, 40, 100), ('HP', 'health', 0, 200, 500),
        ('DEF', 'defense', 0, 20, 60), ('SPD', 'speed', 0, 10, 30),
        ('CRT', 'critical_rate', 1, 8, 20), ('DDG', 'dodge_rate', 1, 8, 15),
        ('KLL', 'lifesteal_pct', 1, 8, 20), ('RFL', 'reflect_pct', 1, 10, 25),
    ],
    'legend': [
        ('ATK', 'attack', 0, 80, 200), ('HP', 'health', 0, 400, 1000),
        ('DEF', 'defense', 0, 40, 120), ('SPD', 'speed', 0, 20, 50),
        ('CRT', 'critical_rate', 1, 12, 30), ('DDG', 'dodge_rate', 1, 10, 20),
        ('KLL', 'lifesteal_pct', 1, 10, 30), ('RFL', 'reflect_pct', 1, 15, 40),
        ('SDM', 'skill_damage_pct', 1, 15, 40), ('IGN', 'ignore_def_pct', 1, 10, 25),
        ('SKF', 'skill_mod_fire', 1, 15, 30), ('SKI', 'skill_mod_ice', 1, 15, 30),
        ('SKL', 'skill_mod_lightning', 1, 15, 30), ('SKH', 'skill_mod_heal', 1, 15, 30),
        ('SKK', 'skill_mod_freeze', 1, 1, 2), ('SKC', 'skill_mod_curse', 1, 10, 20),
    ],
    'ancient': [
        ('ATK', 'attack', 0, 150, 400), ('HP', 'health', 0, 800, 2000),
        ('DEF', 'defense', 0, 80, 200), ('SPD', 'speed', 0, 30, 80),
        ('CRT', 'critical_rate', 1, 15, 40), ('DDG', 'dodge_rate', 1, 12, 25),
        ('KLL', 'lifesteal_pct', 1, 15, 40), ('RFL', 'reflect_pct', 1, 20, 50),
        ('SDM', 'skill_damage_pct', 1, 20, 60), ('IGN', 'ignore_def_pct', 1, 15, 35),
        ('ATB', 'atb_boost_pct', 1, 15, 30), ('REV', 'revive_chance_pct', 1, 10, 25),
        ('SKF', 'skill_mod_fire', 1, 20, 45), ('SKI', 'skill_mod_ice', 1, 20, 45),
        ('SKL', 'skill_mod_lightning', 1, 20, 45), ('SKH', 'skill_mod_heal', 1, 20, 45),
        ('SKK', 'skill_mod_freeze', 1, 1, 2), ('SKC', 'skill_mod_curse', 1, 15, 30),
        ('SKB', 'skill_mod_burn', 1, 5, 12), ('SKE', 'skill_mod_execute', 1, 5, 12),
    ],
    'mythic': [
        ('ATK', 'attack', 0, 300, 800), ('HP', 'health', 0, 1500, 4000),
        ('DEF', 'defense', 0, 150, 400), ('SPD', 'speed', 0, 50, 120),
        ('CRT', 'critical_rate', 1, 20, 50), ('DDG', 'dodge_rate', 1, 15, 35),
        ('KLL', 'lifesteal_pct', 1, 20, 50), ('RFL', 'reflect_pct', 1, 30, 70),
        ('SDM', 'skill_damage_pct', 1, 30, 80), ('IGN', 'ignore_def_pct', 1, 20, 50),
        ('ATB', 'atb_boost_pct', 1, 20, 50), ('REV', 'revive_chance_pct', 1, 15, 40),
        ('DBL', 'double_dmg_pct', 1, 8, 20), ('CRD', 'crit_dmg_pct', 1, 30, 80),
        ('SKF', 'skill_mod_fire', 1, 30, 65), ('SKI', 'skill_mod_ice', 1, 30, 65),
        ('SKL', 'skill_mod_lightning', 1, 30, 65), ('SKH', 'skill_mod_heal', 1, 30, 65),
        ('SKK', 'skill_mod_freeze', 1, 1, 3), ('SKC', 'skill_mod_curse', 1, 20, 40),
        ('SKB', 'skill_mod_burn', 1, 8, 18), ('SKE', 'skill_mod_execute', 1, 8, 18),
        ('SKA', 'skill_mod_aoe', 1, 10, 25),
    ],
    'chaos': [
        ('ATK', 'attack', 0, 500, 1500), ('HP', 'health', 0, 3000, 8000),
        ('DEF', 'defense', 0, 300, 800), ('SPD', 'speed', 0, 80, 200),
        ('CRT', 'critical_rate', 1, 30, 60), ('DDG', 'dodge_rate', 1, 20, 50),
        ('KLL', 'lifesteal_pct', 1, 30, 80), ('RFL', 'reflect_pct', 1, 50, 100),
        ('SDM', 'skill_damage_pct', 1, 50, 150), ('IGN', 'ignore_def_pct', 1, 30, 70),
        ('ATB', 'atb_boost_pct', 1, 30, 80), ('REV', 'revive_chance_pct', 1, 25, 60),
        ('DBL', 'double_dmg_pct', 1, 15, 35), ('CRD', 'crit_dmg_pct', 1, 50, 150),
        ('OMN', 'all_stats_pct', 1, 10, 30), ('AOE', 'aoe_attack', 0, 1, 1),
        ('RGN', 'random_trait', 0, 1, 1), ('NEG', 'enemy_stat_down_pct', 1, 10, 25),
        ('SKF', 'skill_mod_fire', 1, 40, 100), ('SKI', 'skill_mod_ice', 1, 40, 100),
        ('SKL', 'skill_mod_lightning', 1, 40, 100), ('SKH', 'skill_mod_heal', 1, 40, 100),
        ('SKK', 'skill_mod_freeze', 1, 2, 3), ('SKC', 'skill_mod_curse', 1, 30, 60),
        ('SKB', 'skill_mod_burn', 1, 12, 25), ('SKE', 'skill_mod_execute', 1, 10, 25),
        ('SKA', 'skill_mod_aoe', 1, 15, 40), ('SKP', 'skill_mod_poison', 1, 1, 3),
        ('SKR', 'skill_mod_revive', 1, 15, 30),
    ],
}
SET_BONUSES = {
    'dragon_fury': {'name':'龙裔之怒','pieces':3,'effect':'ATK+30%,火焰吐息→全体'},
    'frost_heart': {'name':'冰封之心','pieces':3,'effect':'DEF+25%,冻结+1回合'},
    'shadow_dance': {'name':'暗影之舞','pieces':3,'effect':'SPD+15%,闪避+8%'},
    'chaos_source': {'name':'混沌之源','pieces':4,'effect':'全属性+25%,每场战斗随机敌人特质一个'},
}

# ==========================================
# 装备名字池（稀有度 × 槽位）
# ==========================================
EQUIPMENT_NAMES = {
    'weapon': {
        'common': ['铁剑','短弓','木杖','石锤','骨刀'],
        'uncommon': ['精钢剑','猎弓','橡木杖','战锤','弯刀'],
        'rare': ['寒冰刃','暗影弓','雷光杖','烈焰剑','毒刺'],
        'epic': ['龙牙·断罪','鳳凰·涅槃','雷霆之怒','深渊之牙','圣光裁决'],
        'legend': ['霜噬·灭','虚空·裂','龙牙·断罪','凤翼·斩','暗星·碎','雷神·锤','天启·终章','混沌撕裂者'],
        'ancient': ['远古·裁决','湮灭·终章','创世·破晓','永恒·凋零','原初·审判','虚空·吞噬者'],
        'mythic': ['混沌·噬星','创世·神谕','终焉·灭世','命运·终结','原初·起源','永恒·不朽','全知·全能','万象·归一'],
        'chaos': ['✦终焉·万象终结✦','✦无限·零✦','✦虚无·存在否定✦','✦混沌·法则崩坏✦','✦起源·万物归零✦','✦虚空·真理破碎✦'],
    },
    'head': {
        'common': ['布帽','皮盔','草冠','骨盔','布巾'],
        'uncommon': ['铁盔','羽冠','锁子头巾','角盔','鳞帽'],
        'rare': ['暗影兜帽','龙鳞盔','冰晶冠','烈焰头环','风暴之眼'],
        'epic': ['圣光之冠','深渊兜帽','雷霆之盔','凤凰冠冕','虚空之眼'],
        'legend': ['不死·王冠','智慧·冠冕','战神·盔','星辰·冠','龙裔·冕','霜语·头环','暗影·面具','秩序·皇冠'],
        'ancient': ['远古·智慧冠','创世·全知之眼','永恒·记忆冠','原初·思维之冕'],
        'mythic': ['神谕·全知之冠','命运·先知面具','终焉·洞悉之眼','混沌·心灵之盔'],
        'chaos': ['✦虚无·无面之冠✦','✦真理·万识之源✦','✦虚空·全知之眼✦'],
    },
    'body': {
        'common': ['布甲','皮甲','棉袍','骨铠','麻衣'],
        'uncommon': ['锁子甲','硬皮甲','鳞甲','铁胸甲','链甲'],
        'rare': ['暗影斗篷','龙鳞甲','冰霜战甲','烈焰铠甲','风暴护甲'],
        'epic': ['圣光铠甲','深渊战甲','雷霆之铠','凤凰羽衣','虚空护甲'],
        'legend': ['不朽·铠','守护·战甲','战神·胸甲','星辰·袍','龙裔·鳞铠','霜语·冰甲','暗影·斗篷','秩序·圣衣'],
        'ancient': ['远古·守护铠','创世·不朽之躯','永恒·时之铠','原初·生命之甲'],
        'mythic': ['创世·神甲','命运·不灭之铠','终焉·虚无之躯','混沌·法则之衣'],
        'chaos': ['✦虚空·无垢之铠✦','✦真理·不灭之躯✦','✦起源·万物之壳✦'],
    },
    'accessory': {
        'common': ['铜戒','骨链','石坠','草环','木符'],
        'uncommon': ['银戒','翠玉链','铁符','珊瑚坠','黄晶戒'],
        'rare': ['暗影徽记','龙牙坠','冰晶戒','烈焰之心','风暴之眼'],
        'epic': ['圣光护符','深渊之眼','雷霆之环','凤凰之泪','虚空之印'],
        'legend': ['命运·戒','时光·坠','战神·徽','星辰·环','龙裔·鳞坠','霜语·冰晶','暗影·印记','秩序·圣符'],
        'ancient': ['远古·时之沙','创世·命运之环','永恒·记忆之坠','原初·生命之印'],
        'mythic': ['神谕·命运之轮','终焉·虚无之环','混沌·法则之印','万象·归一之符'],
        'chaos': ['✦星核·万物之环✦','✦虚空·因果之链✦'],
    },
    'boots': {
        'common': ['草鞋','布靴','木屐','骨靴','麻鞋'],
        'uncommon': ['皮靴','铁靴','钉鞋','硬皮靴','鳞靴'],
        'rare': ['暗影之靴','龙鳞靴','冰霜行者','烈焰之靴','风暴之靴'],
        'epic': ['圣光之靴','深渊漫步','雷霆之靴','凤凰之翼','虚空之履'],
        'legend': ['疾风·靴','踏云·履','战神·战靴','星辰·行者','龙裔·龙行靴','霜语·冰径','暗影·瞬步','秩序·圣靴'],
        'ancient': ['远古·踏空靴','创世·虚空行者','永恒·时之靴','原初·生命之履'],
        'mythic': ['神速·光之翼','命运·时空之靴','终焉·虚无之履','混沌·法则之靴'],
        'chaos': ['✦时停·虚无之履✦','✦空间·折叠之靴✦'],
    },
    'special': {
        'common': ['徽章','小旗','铃铛','羽毛','石子'],
        'uncommon': ['银徽章','铜铃','晶石','护符','小鼓'],
        'rare': ['暗影徽','龙之徽','冰晶石','烈焰之心','风暴之眼'],
        'epic': ['圣光徽','深渊徽','雷霆之印','凤凰之羽','虚空之石'],
        'legend': ['命运之徽','时光之印','战神之章','星辰之石','龙裔之鳞','霜语之晶','暗影之印','秩序之章'],
        'ancient': ['远古·遗物','创世·碎片','永恒·记忆','原初·生命之种'],
        'mythic': ['创世·圣物','命运·残章','终焉·碎片','混沌·核心'],
        'chaos': ['✦起源·万物之源✦','✦虚空·真理碎片✦'],
    },
}

# ==========================================
# 基建系统
# ==========================================
BASE_BUILDINGS = [
    {'id':'gene_lab',    'name':'基因研究所', 'icon':'T', 'desc':'全局ATK+{bonus}%',     'per_lv':1, 'max_lv':10},
    {'id':'breed_center','name':'繁殖中心',   'icon':'B', 'desc':'繁殖速度+{bonus}%',     'per_lv':5, 'max_lv':10},
    {'id':'training_camp','name':'训练营',    'icon':'G', 'desc':'训练效果+{bonus}%',     'per_lv':3, 'max_lv':10},
    {'id':'warehouse',   'name':'仓库',       'icon':'W', 'desc':'卡牌上限+{bonus}',      'per_lv':2, 'max_lv':10},
    {'id':'essence_plant','name':'精华提炼厂', 'icon':'E', 'desc':'离线每小时+{bonus}精华','per_lv':1,'max_lv':10},
]

# ==========================================
# 装备词条代码→中文映射
# ==========================================
AFFIX_CODE_NAMES = {
    'ATK':'攻击', 'HP':'生命', 'DEF':'防御', 'SPD':'速度',
    'CRT':'暴击率', 'DDG':'闪避率', 'KLL':'吸血率', 'RFL':'反伤率',
    'SDM':'技能伤害', 'IGN':'无视防御', 'ATB':'行动条加成',
    'REV':'复活概率', 'DBL':'双倍伤害率', 'CRD':'暴击伤害',
    'OMN':'全属性', 'AOE':'攻击全体化', 'RGN':'随机特质',
    'NEG':'敌方属性降低',
    'SKF':'火焰吐息伤害','SKI':'冰霜护盾护盾量','SKL':'雷击伤害',
    'SKH':'自我修复治疗量','SKK':'冻结回合','SKC':'诅咒增伤',
    'SKB':'灼烧百分比','SKE':'处决阈值','SKA':'甘霖治疗量',
    'SKP':'中毒层数','SKR':'亡灵复苏回复',
}
