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