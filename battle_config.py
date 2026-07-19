import random
random.seed(42)

ENEMY_TEMPLATES = {
    'basic': {
        'name': '野生实验体',
        'color': '#4a90d9',
        'base_health': 60, 'base_attack': 10, 'base_defense': 4, 'base_speed': 8,
        'skills_pool': [],
        'min_skills': 0, 'max_skills': 0,
    },
    'soldier': {
        'name': '守卫实验体',
        'color': '#5dade2',
        'base_health': 80, 'base_attack': 14, 'base_defense': 6, 'base_speed': 10,
        'skills_pool': ['火焰吐息', '冰霜护盾'],
        'min_skills': 0, 'max_skills': 1,
    },
    'mutant': {
        'name': '变异实验体',
        'color': '#a569bd',
        'base_health': 100, 'base_attack': 18, 'base_defense': 8, 'base_speed': 12,
        'skills_pool': ['雷击', '毒液攻击', '自我修复', '能量吸收', '观星'],
        'min_skills': 1, 'max_skills': 2,
    },
    'elite': {
        'name': '精英实验体',
        'color': '#e74c3c',
        'base_health': 130, 'base_attack': 22, 'base_defense': 11, 'base_speed': 15,
        'skills_pool': ['能量护盾', '幻觉制造', '睡眠诱导', '麻痹神经', '隐身', '快速生长', '观星', '澎湃', '甘霖'],
        'min_skills': 1, 'max_skills': 3,
    },
    'boss': {
        'name': '首领实验体',
        'color': '#8e44ad',
        'base_health': 220, 'base_attack': 32, 'base_defense': 18, 'base_speed': 36,
        'skills_pool': ['火焰吐息', '雷击', '自我修复', '召唤', '麻痹神经', '能量吸收', '快速生长', '瞬移', '观星', '澎湃', '甘霖'],
        'min_skills': 2, 'max_skills': 4,
    },
    'overlord': {
        'name': '首领实验体（增强版）',
        'color': '#ff0000',
        'base_health': 2200, 'base_attack': 32, 'base_defense': 18, 'base_speed': 18,
        'skills_pool': ['召唤', '能量吸收', '自我修复', '瞬移', '观星', '澎湃'],
        'min_skills': 4, 'max_skills': 4,
    },

    # ==================== 新敌怪 (31-60关) ====================
    'scout': {
        'name': '侦查眼',
        'color': '#00bcd4',
        'base_health': 50, 'base_attack': 8, 'base_defense': 2, 'base_speed': 18,
        'skills_pool': ['瞬移', '隐身'],
        'min_skills': 0, 'max_skills': 1,
        'description': '高速侦查单位，擅长闪避',
    },
    'flame_guard': {
        'name': '烈焰守卫',
        'color': '#ff5722',
        'base_health': 90, 'base_attack': 22, 'base_defense': 6, 'base_speed': 10,
        'skills_pool': ['火焰吐息', '澎湃'],
        'min_skills': 1, 'max_skills': 2,
        'description': '火焰特化攻击单位',
    },
    'frost_mage': {
        'name': '冰霜术士',
        'color': '#81d4fa',
        'base_health': 80, 'base_attack': 12, 'base_defense': 14, 'base_speed': 8,
        'skills_pool': ['冰霜护盾', '能量护盾', '甘霖'],
        'min_skills': 1, 'max_skills': 2,
        'description': '冰霜防御与治疗单位',
    },
    'venom_stalker': {
        'name': '毒液潜伏者',
        'color': '#8bc34a',
        'base_health': 70, 'base_attack': 14, 'base_defense': 5, 'base_speed': 16,
        'skills_pool': ['毒液攻击', '隐身'],
        'min_skills': 1, 'max_skills': 2,
        'description': '剧毒暗杀单位，擅长叠毒',
    },
    'thunder_bringer': {
        'name': '雷暴使者',
        'color': '#ffeb3b',
        'base_health': 95, 'base_attack': 26, 'base_defense': 7, 'base_speed': 14,
        'skills_pool': ['雷击', '快速生长', '麻痹神经'],
        'min_skills': 1, 'max_skills': 2,
        'description': '雷电爆发单位',
    },
    'void_walker': {
        'name': '虚空行者',
        'color': '#7c4dff',
        'base_health': 75, 'base_attack': 16, 'base_defense': 8, 'base_speed': 20,
        'skills_pool': ['瞬移', '观星', '能量吸收'],
        'min_skills': 1, 'max_skills': 2,
        'description': '高速游击单位，扰乱阵型',
    },
    'phantom_assassin': {
        'name': '幻影刺客',
        'color': '#e040fb',
        'base_health': 60, 'base_attack': 24, 'base_defense': 4, 'base_speed': 22,
        'skills_pool': ['隐身', '幻觉制造', '毒液攻击'],
        'min_skills': 1, 'max_skills': 2,
        'description': '隐身刺杀单位',
    },
    'healer': {
        'name': '治疗先驱',
        'color': '#69f0ae',
        'base_health': 100, 'base_attack': 8, 'base_defense': 10, 'base_speed': 12,
        'skills_pool': ['自我修复', '甘霖', '能量护盾'],
        'min_skills': 2, 'max_skills': 3,
        'description': '专职治疗与辅助，每回合恢复自身生命',
        'passive_abilities': ['regeneration'],
    },
    'iron_fortress': {
        'name': '铁甲堡垒',
        'color': '#78909c',
        'base_health': 200, 'base_attack': 10, 'base_defense': 22, 'base_speed': 4,
        'skills_pool': ['能量护盾', '冰霜护盾', '自我修复'],
        'min_skills': 1, 'max_skills': 2,
        'description': '超重型防御单位，反弹伤害',
        'passive_abilities': ['thorns_aura'],
    },
    'mad_scientist': {
        'name': '疯狂科学家',
        'color': '#ffab40',
        'base_health': 85, 'base_attack': 18, 'base_defense': 6, 'base_speed': 13,
        'skills_pool': ['快速生长', '澎湃', '幻觉制造', '召唤'],
        'min_skills': 1, 'max_skills': 3,
        'description': '强化与辅助单位',
    },
    'suicide_bomber': {
        'name': '自爆工兵',
        'color': '#ff1744',
        'base_health': 50, 'base_attack': 6, 'base_defense': 2, 'base_speed': 15,
        'skills_pool': ['自爆', '快速生长'],
        'min_skills': 1, 'max_skills': 2,
        'description': '低血量高自爆伤害',
    },
    'sleep_emissary': {
        'name': '睡眠使者',
        'color': '#b388ff',
        'base_health': 80, 'base_attack': 10, 'base_defense': 8, 'base_speed': 12,
        'skills_pool': ['睡眠诱导', '幻觉制造', '瞬移'],
        'min_skills': 1, 'max_skills': 2,
        'description': '控制特化单位',
    },
    'paralyze_spider': {
        'name': '麻痹毒蛛',
        'color': '#aed581',
        'base_health': 90, 'base_attack': 16, 'base_defense': 10, 'base_speed': 14,
        'skills_pool': ['麻痹神经', '毒液攻击', '能量吸收'],
        'min_skills': 1, 'max_skills': 2,
        'description': '麻痹与中毒双控单位',
    },
    'energy_vampire': {
        'name': '能量吸血鬼',
        'color': '#ce93d8',
        'base_health': 100, 'base_attack': 20, 'base_defense': 8, 'base_speed': 16,
        'skills_pool': ['能量吸收', '自我修复', '隐身'],
        'min_skills': 1, 'max_skills': 2,
        'description': '吸血续航单位',
    },
    'summon_master': {
        'name': '召唤大师',
        'color': '#4dd0e1',
        'base_health': 110, 'base_attack': 14, 'base_defense': 10, 'base_speed': 10,
        'skills_pool': ['召唤', '能量护盾', '甘霖'],
        'min_skills': 1, 'max_skills': 2,
        'description': '召唤与辅助单位',
    },
    'star_observer': {
        'name': '星辰观测者',
        'color': '#448aff',
        'base_health': 90, 'base_attack': 18, 'base_defense': 8, 'base_speed': 16,
        'skills_pool': ['观星', '雷击', '澎湃'],
        'min_skills': 1, 'max_skills': 2,
        'description': '阵型扰乱与输出',
    },
    'gene_fusion': {
        'name': '基因融合体',
        'color': '#ff6f00',
        'base_health': 150, 'base_attack': 25, 'base_defense': 14, 'base_speed': 18,
        'skills_pool': ['火焰吐息', '毒液攻击', '雷击', '自我修复', '能量吸收', '观星'],
        'min_skills': 2, 'max_skills': 4,
        'description': '多种基因融合的强大单位',
    },
    'crystal_guardian': {
        'name': '水晶守卫',
        'color': '#26c6da',
        'base_health': 160, 'base_attack': 12, 'base_defense': 18, 'base_speed': 8,
        'skills_pool': ['冰霜护盾', '能量护盾', '甘霖', '自我修复'],
        'min_skills': 2, 'max_skills': 3,
        'description': '多重护盾的固守单位',
    },
    'chaos_source': {
        'name': '混沌之源',
        'color': '#d500f9',
        'base_health': 120, 'base_attack': 20, 'base_defense': 10, 'base_speed': 15,
        'skills_pool': ['幻觉制造', '睡眠诱导', '麻痹神经', '观星'],
        'min_skills': 2, 'max_skills': 3,
        'description': '混乱与控制核心',
    },
    'devourer': {
        'name': '吞噬者',
        'color': '#b71c1c',
        'base_health': 350, 'base_attack': 40, 'base_defense': 20, 'base_speed': 22,
        'skills_pool': ['能量吸收', '召唤', '火焰吐息', '雷击', '自我修复', '毒液攻击'],
        'min_skills': 3, 'max_skills': 5,
        'description': '精英首领单位',
    },
    'void_overlord': {
        'name': '虚空霸主',
        'color': '#ff6600',
        'base_health': 3000, 'base_attack': 42, 'base_defense': 24, 'base_speed': 24,
        'skills_pool': ['召唤', '能量吸收', '自我修复', '瞬移', '观星', '澎湃', '甘霖', '幻觉制造'],
        'min_skills': 5, 'max_skills': 5,
        'description': '超越常理的虚空主宰',
        'trigger_all_skills': True,
    },
    'purifier': {
        'name': '净化器',
        'color': '#00e5ff',
        'base_health': 120, 'base_attack': 6, 'base_defense': 10, 'base_speed': 6,
        'skills_pool': ['能量护盾', '自我修复'],
        'min_skills': 1, 'max_skills': 2,
        'description': '每3秒为全体友方施加2秒净化护盾，免疫负面效果',
        'purify_interval': 90,
    },
    'annihilator': {
        'name': '湮灭体',
        'color': '#ff1100',
        'base_health': 80, 'base_attack': 10, 'base_defense': 3, 'base_speed': 10,
        'skills_pool': ['自爆'],
        'min_skills': 0, 'max_skills': 1,
        'description': '受到致命伤害时，将击杀者一起拖入毁灭，死亡时对敌方全体造成伤害',
        'annihilate': True,
        'passive_abilities': ['vengeance'],
    },

    # ==================== 61-100关新敌怪 ====================
    'mutant_spider': {
        'name': '变异狼蛛',
        'color': '#7a3b3b',
        'base_health': 110, 'base_attack': 22, 'base_defense': 10, 'base_speed': 16,
        'skills_pool': ['毒液攻击', '麻痹神经', '快速生长'],
        'min_skills': 1, 'max_skills': 2,
        'description': '剧毒蜘蛛，擅长叠毒麻痹',
    },
    'ghost_assassin': {
        'name': '幽灵刺客',
        'color': '#9c27b0',
        'base_health': 75, 'base_attack': 30, 'base_defense': 5, 'base_speed': 24,
        'skills_pool': ['隐身', '幻觉制造', '能量吸收'],
        'min_skills': 1, 'max_skills': 2,
        'description': '隐身刺杀单位，高暴击',
    },
    'frost_giant': {
        'name': '冰霜巨人',
        'color': '#80deea',
        'base_health': 250, 'base_attack': 24, 'base_defense': 22, 'base_speed': 6,
        'skills_pool': ['冰霜护盾', '冻结', '能量护盾'],
        'min_skills': 1, 'max_skills': 2,
        'description': '冰霜巨人，拥有冻结能力',
    },
    'shadow_mage': {
        'name': '暗影法师',
        'color': '#4a148c',
        'base_health': 100, 'base_attack': 26, 'base_defense': 8, 'base_speed': 14,
        'skills_pool': ['诅咒', '幻觉制造', '能量吸收'],
        'min_skills': 1, 'max_skills': 2,
        'description': '暗影法师，施加强力诅咒',
    },
    'lava_lord': {
        'name': '熔岩领主',
        'color': '#ff6d00',
        'base_health': 180, 'base_attack': 28, 'base_defense': 12, 'base_speed': 10,
        'skills_pool': ['火焰吐息', '灼烧', '澎湃'],
        'min_skills': 1, 'max_skills': 2,
        'description': '熔岩之主，持续灼烧敌人',
    },
    'crystal_guard': {
        'name': '晶壁守卫',
        'color': '#00bcd4',
        'base_health': 200, 'base_attack': 12, 'base_defense': 28, 'base_speed': 6,
        'skills_pool': ['能量护盾', '冰霜护盾', '自我修复'],
        'min_skills': 2, 'max_skills': 3,
        'description': '超强防御单位，多重护盾',
    },
    'plasma_being': {
        'name': '等离子体',
        'color': '#e040fb',
        'base_health': 120, 'base_attack': 32, 'base_defense': 6, 'base_speed': 18,
        'skills_pool': ['雷击', '澎湃', '快速生长'],
        'min_skills': 1, 'max_skills': 2,
        'description': '等离子能量体，高爆发输出',
    },
    'nano_swarm': {
        'name': '纳米虫群',
        'color': '#76ff03',
        'base_health': 140, 'base_attack': 16, 'base_defense': 14, 'base_speed': 20,
        'skills_pool': ['召唤', '毒液攻击', '隐身'],
        'min_skills': 1, 'max_skills': 2,
        'description': '纳米虫群，召唤与毒攻',
    },
    'gene_reaper': {
        'name': '基因收割者',
        'color': '#b71c1c',
        'base_health': 160, 'base_attack': 36, 'base_defense': 14, 'base_speed': 16,
        'skills_pool': ['处决', '火焰吐息', '雷击', '能量吸收'],
        'min_skills': 1, 'max_skills': 2,
        'description': '基因收割者，处决低血量目标',
    },
    'emp_wraith': {
        'name': '电磁脉冲者',
        'color': '#2979ff',
        'base_health': 100, 'base_attack': 18, 'base_defense': 10, 'base_speed': 22,
        'skills_pool': ['麻痹神经', '雷击', '瞬移'],
        'min_skills': 1, 'max_skills': 2,
        'description': '电磁脉冲，群体麻痹',
    },
    'poison_cloud': {
        'name': '毒雾花',
        'color': '#558b2f',
        'base_health': 90, 'base_attack': 14, 'base_defense': 8, 'base_speed': 12,
        'skills_pool': ['毒雾扩散', '毒液攻击', '自我修复'],
        'min_skills': 1, 'max_skills': 2,
        'description': '毒雾之花，群体中毒',
    },
    'iron_colossus': {
        'name': '钢铁巨像',
        'color': '#607d8b',
        'base_health': 350, 'base_attack': 20, 'base_defense': 32, 'base_speed': 4,
        'skills_pool': ['能量护盾', '冰霜护盾', '自我修复', '快速生长'],
        'min_skills': 2, 'max_skills': 3,
        'description': '钢铁巨像，终极防御',
    },
    'time_weaver': {
        'name': '时间操纵者',
        'color': '#7c4dff',
        'base_health': 130, 'base_attack': 20, 'base_defense': 12, 'base_speed': 26,
        'skills_pool': ['时光倒流', '观星', '甘霖'],
        'min_skills': 1, 'max_skills': 2,
        'description': '时间操纵者，回溯恢复',
    },
    'star_spirit': {
        'name': '星灵守护',
        'color': '#448aff',
        'base_health': 150, 'base_attack': 16, 'base_defense': 16, 'base_speed': 14,
        'skills_pool': ['甘霖', '能量护盾', '自我修复', '冻结'],
        'min_skills': 2, 'max_skills': 3,
        'description': '星灵守护，团队治疗与冻结',
    },
    'dark_angel': {
        'name': '暗黑天使',
        'color': '#e91e63',
        'base_health': 140, 'base_attack': 40, 'base_defense': 10, 'base_speed': 20,
        'skills_pool': ['自爆', '火焰吐息', '澎湃', '能量吸收'],
        'min_skills': 1, 'max_skills': 3,
        'description': '暗黑天使，自毁式高伤害',
    },
    'bone_dragon': {
        'name': '骨龙',
        'color': '#bdbdbd',
        'base_health': 280, 'base_attack': 34, 'base_defense': 20, 'base_speed': 12,
        'skills_pool': ['亡灵复苏', '火焰吐息', '冰霜护盾', '麻痹神经'],
        'min_skills': 2, 'max_skills': 3,
        'description': '骨龙，死亡后复苏一次',
        'trigger_all_skills': True,
    },
    'abyss_lord': {
        'name': '深渊领主',
        'color': '#d50000',
        'base_health': 3000, 'base_attack': 44, 'base_defense': 26, 'base_speed': 20,
        'skills_pool': ['召唤', '能量吸收', '自我修复', '处决', '诅咒', '澎湃'],
        'min_skills': 4, 'max_skills': 5,
        'description': '深渊领主，2×2超巨型首领',
        'trigger_all_skills': True,
    },
    'doomsday_bringer': {
        'name': '末日使者',
        'color': '#ffab00',
        'base_health': 100, 'base_attack': 20, 'base_defense': 6, 'base_speed': 18,
        'skills_pool': ['自爆', '澎湃', '快速生长'],
        'min_skills': 1, 'max_skills': 2,
        'description': '末日使者，强化版自爆兵',
    },
    'mech_god': {
        'name': '机械神',
        'color': '#ffd740',
        'base_health': 500, 'base_attack': 50, 'base_defense': 30, 'base_speed': 30,
        'skills_pool': ['火焰吐息', '雷击', '能量护盾', '自我修复', '召唤', '甘霖', '澎湃', '麻痹神经'],
        'min_skills': 3, 'max_skills': 5,
        'description': '机械神明，终极多技能首领',
        'trigger_all_skills': True,
    },
    'void_destroyer': {
        'name': '虚空毁灭者',
        'color': '#ff0040',
        'base_health': 4000, 'base_attack': 55, 'base_defense': 35, 'base_speed': 35,
        'skills_pool': ['召唤', '处决', '诅咒', '灼烧', '冻结', '时光倒流', '亡灵复苏', '能量吸收'],
        'min_skills': 5, 'max_skills': 6,
        'description': '虚空毁灭者，终极BOSS',
        'trigger_all_skills': True,
    },

    # ==================== 圣堂主题 - 血与肉 ====================
    'sanctuary_ascetic': {
        'name': '圣堂苦修者',
        'color': '#8b4513',
        'base_health': 60, 'base_attack': 18, 'base_defense': 4, 'base_speed': 14,
        'skills_pool': ['血肉献祭'],
        'min_skills': 1, 'max_skills': 1,
        'description': '通过自残来治疗友军的狂热信徒',
    },
    'sanctuary_stitcher': {
        'name': '血肉缝合体',
        'color': '#4a0e0e',
        'base_health': 100, 'base_attack': 12, 'base_defense': 8, 'base_speed': 8,
        'skills_pool': ['召唤', '甘霖'],
        'min_skills': 1, 'max_skills': 2,
        'description': '由残肢缝合而成的怪物，会召唤更多的血肉',
    },
    'sanctuary_atonement': {
        'name': '赎罪之眼',
        'color': '#dc143c',
        'base_health': 80, 'base_attack': 20, 'base_defense': 5, 'base_speed': 12,
        'skills_pool': ['圣光惩戒'],
        'min_skills': 1, 'max_skills': 1,
        'description': '悬浮在空中的巨大眼球，注视即惩戒',
    },
    'sanctuary_chalice': {
        'name': '圣餐之杯',
        'color': '#c0a000',
        'base_health': 120, 'base_attack': 8, 'base_defense': 10, 'base_speed': 6,
        'skills_pool': ['甘霖', '能量护盾'],
        'min_skills': 1, 'max_skills': 2,
        'description': '盛满鲜血的圣杯，为友军提供治疗和护盾',
    },
    'sanctuary_idol': {
        'name': '腐化神像',
        'color': '#2f004f',
        'base_health': 150, 'base_attack': 6, 'base_defense': 15, 'base_speed': 4,
        'skills_pool': ['诅咒', '麻痹神经'],
        'min_skills': 1, 'max_skills': 2,
        'description': '被血肉腐蚀的圣像，散发出诅咒的气息',
    },
    'sanctuary_bloodpool': {
        'name': '血池',
        'color': '#8b0000',
        'base_health': 50, 'base_attack': 10, 'base_defense': 3, 'base_speed': 10,
        'skills_pool': ['血之疫病'],
        'min_skills': 1, 'max_skills': 1,
        'description': '地上的一滩血水，会突然爆发瘟疫',
    },
    'sanctuary_boneguard': {
        'name': '白骨卫士',
        'color': '#f5f5dc',
        'base_health': 90, 'base_attack': 8, 'base_defense': 18, 'base_speed': 6,
        'skills_pool': ['能量护盾', '睡眠诱导'],
        'min_skills': 1, 'max_skills': 2,
        'description': '由骸骨组成的守卫，坚不可摧',
    },
    'sanctuary_penitent': {
        'name': '忏悔者',
        'color': '#4a0000',
        'base_health': 70, 'base_attack': 16, 'base_defense': 6, 'base_speed': 12,
        'skills_pool': ['自爆'],
        'min_skills': 1, 'max_skills': 1,
        'annihilate': True,
        'description': '以死亡来赎罪的狂信徒，死亡时拖敌人下水',
    },
    'sanctuary_deacon': {
        'name': '圣堂执事',
        'color': '#8b0000',
        'base_health': 80, 'base_attack': 12, 'base_defense': 8, 'base_speed': 10,
        'skills_pool': ['净化之火', '澎湃'],
        'min_skills': 1, 'max_skills': 2,
        'description': '圣堂的执事，能净化污秽并鼓舞友军',
    },
    'sanctuary_apostle': {
        'name': '血肉使徒',
        'color': '#660066',
        'base_health': 130, 'base_attack': 14, 'base_defense': 10, 'base_speed': 8,
        'skills_pool': ['圣疗', '能量吸收'],
        'min_skills': 1, 'max_skills': 2,
        'description': '被血肉腐蚀的使徒，能够复活阵亡的同伴',
    },
    'sanctuary_relic': {
        'name': '圣骸',
        'color': '#c0c0c0',
        'base_health': 40, 'base_attack': 8, 'base_defense': 4, 'base_speed': 6,
        'skills_pool': ['澎湃'],
        'min_skills': 1, 'max_skills': 1,
        'annihilate': True,
        'description': '蕴含圣力的遗骨，毁灭时赐福残存的敌人',
    },
    'sanctuary_malformed': {
        'name': '畸形圣婴',
        'color': '#ffb6c1',
        'base_health': 50, 'base_attack': 22, 'base_defense': 2, 'base_speed': 18,
        'skills_pool': ['圣光惩戒', '血之疫病'],
        'min_skills': 1, 'max_skills': 2,
        'description': '扭曲的圣婴，行动迅捷且攻击凶狠',
    },
    'sanctuary_thorns': {
        'name': '血荆棘',
        'color': '#006400',
        'base_health': 80, 'base_attack': 14, 'base_defense': 10, 'base_speed': 10,
        'skills_pool': ['毒液攻击', '麻痹神经'],
        'min_skills': 1, 'max_skills': 2,
        'description': '缠绕着圣堂废墟的荆棘，沾满鲜血',
        'passive_abilities': ['thorns_aura'],
    },
    'sanctuary_inquisitor': {
        'name': '审判官',
        'color': '#ff4500',
        'base_health': 85, 'base_attack': 24, 'base_defense': 6, 'base_speed': 14,
        'skills_pool': ['处决', '净化之火'],
        'min_skills': 1, 'max_skills': 2,
        'description': '以圣火净化异端的审判官，对低生命目标毫不留情',
    },
    'sanctuary_archbishop': {
        'name': '大主教',
        'color': '#ff0000',
        'base_health': 250, 'base_attack': 20, 'base_defense': 12, 'base_speed': 10,
        'skills_pool': ['圣疗', '血肉献祭', '圣光惩戒', '能量护盾', '澎湃'],
        'min_skills': 3, 'max_skills': 5,
        'trigger_all_skills': True,
        'description': '被血肉腐蚀的大主教，圣堂的最终统治者',
    },

    # ==================== 多格单位 ====================
    'shadow_sentinel': {
        'name': '幽冥哨兵',
        'color': '#6a0dad',
        'base_health': 100, 'base_attack': 28, 'base_defense': 8, 'base_speed': 18,
        'skills_pool': ['幽冥穿刺'],
        'min_skills': 1, 'max_skills': 1,
        'description': '1×2纵列单位，50%伤害转移至下方单位',
        'width': 1, 'height': 2,
        'passive_abilities': ['guard_protocol'],
    },
    'iron_bulwark': {
        'name': '钢铁壁垒',
        'color': '#607d8b',
        'base_health': 300, 'base_attack': 12, 'base_defense': 30, 'base_speed': 4,
        'skills_pool': ['钢铁震击'],
        'min_skills': 1, 'max_skills': 1,
        'description': '2×1横行单位，相邻友方减伤25%',
        'width': 2, 'height': 1,
        'passive_abilities': ['iron_wall'],
    },
    'ancient_serpent': {
        'name': '远古巨蟒',
        'color': '#2e7d32',
        'base_health': 180, 'base_attack': 20, 'base_defense': 12, 'base_speed': 14,
        'skills_pool': ['剧毒吐息'],
        'min_skills': 1, 'max_skills': 1,
        'description': '1×3纵列单位，毒伤+100%，毒杀扩散',
        'width': 1, 'height': 3,
        'passive_abilities': ['poison_mastery'],
    },
    'war_behemoth': {
        'name': '战争巨兽',
        'color': '#b71c1c',
        'base_health': 400, 'base_attack': 35, 'base_defense': 20, 'base_speed': 8,
        'skills_pool': ['战吼'],
        'min_skills': 1, 'max_skills': 1,
        'description': '3×1横行单位，每回合推进并造成路径伤害',
        'width': 3, 'height': 1,
        'passive_abilities': ['advance'],
        'trigger_all_skills': True,
    },
    'void_dragon_god': {
        'name': '虚空龙神',
        'color': '#4a148c',
        'base_health': 3000, 'base_attack': 45, 'base_defense': 28, 'base_speed': 22,
        'skills_pool': ['虚空传送', '召唤', '能量吸收', '自我修复', '火焰吐息', '雷击'],
        'min_skills': 4, 'max_skills': 6,
        'description': '2×3超巨型首领，统领虚空一族',
        'width': 2, 'height': 3,
        'passive_abilities': ['void_lord'],
        'trigger_all_skills': True,
    },
    'eternal_guardian': {
        'name': '永恒守卫',
        'color': '#00e5ff',
        'base_health': 220, 'base_attack': 18, 'base_defense': 24, 'base_speed': 8,
        'skills_pool': ['能量护盾', '冰霜护盾', '自我修复', '甘霖'],
        'min_skills': 2, 'max_skills': 3,
        'description': '永恒守卫，护盾与治疗',
    },

    # ==================== 辅助/光环敌怪 ====================
    'commander': {
        'name': '指挥官',
        'color': '#ffd700',
        'base_health': 130, 'base_attack': 14, 'base_defense': 12, 'base_speed': 10,
        'skills_pool': ['快速生长', '澎湃', '能量护盾'],
        'min_skills': 1, 'max_skills': 2,
        'description': '攻击灵气+防御灵气，提升全体友方攻防',
        'passive_abilities': ['attack_aura', 'defense_aura'],
    },
    'war_drummer': {
        'name': '战鼓手',
        'color': '#ff8a65',
        'base_health': 100, 'base_attack': 8, 'base_defense': 8, 'base_speed': 14,
        'skills_pool': ['甘霖', '澎湃', '隐身'],
        'min_skills': 1, 'max_skills': 2,
        'description': '速度灵气+治愈灵气，提升友方速度并持续回血',
        'passive_abilities': ['speed_aura', 'heal_aura'],
    },
    'guardian_spirit': {
        'name': '守护之灵',
        'color': '#00e676',
        'base_health': 180, 'base_attack': 6, 'base_defense': 20, 'base_speed': 6,
        'skills_pool': ['能量护盾', '冰霜护盾', '甘霖'],
        'min_skills': 1, 'max_skills': 2,
        'description': '登场时提升全体友方生命上限，每回合提供护盾',
        'passive_abilities': ['fortify', 'shield_aura'],
    },
    'vengeful_wraith': {
        'name': '复仇之魂',
        'color': '#d500f9',
        'base_health': 90, 'base_attack': 18, 'base_defense': 5, 'base_speed': 16,
        'skills_pool': ['能量吸收', '隐身', '诅咒'],
        'min_skills': 1, 'max_skills': 2,
        'description': '死亡时全体友方加攻并对全体敌方造成伤害',
        'passive_abilities': ['rage', 'vengeance'],
    },
    'corruption_source': {
        'name': '腐蚀之源',
        'color': '#76ff03',
        'base_health': 110, 'base_attack': 12, 'base_defense': 8, 'base_speed': 12,
        'skills_pool': ['毒液攻击', '毒雾扩散', '自我修复'],
        'min_skills': 1, 'max_skills': 2,
        'description': '每回合对全体敌方施毒，并净化友方负面效果',
        'passive_abilities': ['toxic_aura', 'bless'],
    },
    'rock': {
        'name': '巨石',
        'color': '#616161',
        'base_health': 99999, 'base_attack': 0, 'base_defense': 50, 'base_speed': 0,
        'skills_pool': [],
        'min_skills': 0, 'max_skills': 0,
        'description': '血量极高的巨石，免疫所有负面效果，其他单位全部死亡后自动毁灭',
        'immune_to_debuffs': True,
    },

    # ==================== 地图1：废弃实验室 ====================
    'lab_slime': {
        'name': '腐蚀黏液怪', 'color': '#7cba3c',
        'base_health': 90, 'base_attack': 16, 'base_defense': 6, 'base_speed': 12,
        'skills_pool': ['腐蚀酸液'], 'min_skills': 1, 'max_skills': 1,
        'description': '腐蚀性黏液聚合体，每回合降低玩家防御',
        'passive_abilities': ['corrosive_aura'],
    },
    'lab_culture': {
        'name': '失控培植体', 'color': '#4caf50',
        'base_health': 120, 'base_attack': 10, 'base_defense': 12, 'base_speed': 8,
        'skills_pool': ['污染净化'], 'min_skills': 1, 'max_skills': 1,
        'description': '将友方debuff转化为治疗',
        'passive_abilities': ['convert_debuff'],
    },
    'lab_barrel': {
        'name': '剧毒废料桶', 'color': '#8bc34a',
        'base_health': 70, 'base_attack': 8, 'base_defense': 4, 'base_speed': 6,
        'skills_pool': ['毒液攻击', '自爆'], 'min_skills': 1, 'max_skills': 2,
        'description': '死亡时留下毒区，每回合对全体玩家造成伤害',
        'passive_abilities': ['death_zone'],
    },
    'lab_security': {
        'name': '实验室保安机甲', 'color': '#607d8b',
        'base_health': 200, 'base_attack': 18, 'base_defense': 22, 'base_speed': 6,
        'skills_pool': ['能量护盾', '护卫铁壁'], 'min_skills': 1, 'max_skills': 2,
        'description': '护卫最低血量友方',
        'passive_abilities': ['protect_ally'],
    },
    'lab_boss': {
        'name': '暴走究极体', 'color': '#ff1744',
        'base_health': 400, 'base_attack': 40, 'base_defense': 20, 'base_speed': 20,
        'skills_pool': ['腐蚀酸液', '污染净化', '护卫铁壁', '狂暴释放'],
        'min_skills': 3, 'max_skills': 4,
        'description': '每损失30%HP切换形态（攻击/防御/平衡），拥有所有形态技能',
        'passive_abilities': ['form_shift_lab'],
    },


    # ===== 废弃实验室 新增敌人 =====
    'lab_mutanthound': {
        'name': '变异猎犬', 'color': '#5a2d2d',
        'base_health': 80, 'base_attack': 26, 'base_defense': 4, 'base_speed': 22,
        'skills_pool': ['腐蚀酸液', '快速生长'], 'min_skills': 1, 'max_skills': 2,
        'description': '高速近战单位，攻击叠加腐蚀效果',
    },
    'lab_centrifuge': {
        'name': '高速离心机', 'color': '#9e9e9e',
        'base_health': 100, 'base_attack': 20, 'base_defense': 10, 'base_speed': 14,
        'skills_pool': ['酸液飞溅', '自爆'], 'min_skills': 1, 'max_skills': 2,
        'description': '旋转喷射酸液攻击全体',
    },
    'lab_gasleak': {
        'name': '毒气泄漏口', 'color': '#76ff03',
        'base_health': 90, 'base_attack': 12, 'base_defense': 8, 'base_speed': 8,
        'skills_pool': ['毒雾扩散'], 'min_skills': 1, 'max_skills': 1,
        'description': '每回合释放毒气',
        'passive_abilities': ['toxic_residue'],
    },
    'lab_mercury': {
        'name': '水银分裂体', 'color': '#b0bec5',
        'base_health': 160, 'base_attack': 14, 'base_defense': 14, 'base_speed': 10,
        'skills_pool': ['腐蚀酸液', '自我修复'], 'min_skills': 1, 'max_skills': 2,
        'description': '生命低于50%时分裂为两个小水银',
        'passive_abilities': ['split_merge'],
    },
    'lab_eyestalk': {
        'name': '眼梗怪', 'color': '#8e24aa',
        'base_health': 70, 'base_attack': 28, 'base_defense': 6, 'base_speed': 16,
        'skills_pool': ['锁定狙击'], 'min_skills': 1, 'max_skills': 1,
        'description': '远程锁定最低血量目标',
        'passive_abilities': ['focus_weak'],
    },
    'lab_tentacle': {
        'name': '培养触手', 'color': '#4a148c',
        'base_health': 110, 'base_attack': 18, 'base_defense': 10, 'base_speed': 12,
        'skills_pool': ['虚空牵引', '麻痹神经'], 'min_skills': 1, 'max_skills': 2,
        'description': '将玩家拉至前排并麻痹',
    },
    'lab_zombie': {
        'name': '废弃研究员', 'color': '#795548',
        'base_health': 100, 'base_attack': 14, 'base_defense': 8, 'base_speed': 10,
        'skills_pool': ['亡灵复苏', '诅咒'], 'min_skills': 1, 'max_skills': 2,
        'description': '死亡后复活继续战斗',
    },
    'lab_injector': {
        'name': '基因注射器', 'color': '#00bcd4',
        'base_health': 90, 'base_attack': 10, 'base_defense': 16, 'base_speed': 12,
        'skills_pool': ['基因突变', '澎湃', '甘霖'], 'min_skills': 1, 'max_skills': 2,
        'description': '为友方注射强化基因',
    },
    'lab_fumes': {
        'name': '腐蚀雾团', 'color': '#558b2f',
        'base_health': 80, 'base_attack': 16, 'base_defense': 10, 'base_speed': 14,
        'skills_pool': ['毒雾扩散', '毒液攻击'], 'min_skills': 1, 'max_skills': 2,
        'description': '全场笼罩腐蚀毒雾',
    },
    'lab_amalgam': {
        'name': '混合聚合体', 'color': '#e65100',
        'base_health': 280, 'base_attack': 22, 'base_defense': 26, 'base_speed': 6,
        'skills_pool': ['自我修复', '能量护盾', '狂暴释放'], 'min_skills': 2, 'max_skills': 3,
        'description': '多基因融合的巨型肉块',
        'passive_abilities': ['berserk'],
    },
    'lab_cleaner': {
        'name': '清洁机器人', 'color': '#26c6da',
        'base_health': 100, 'base_attack': 8, 'base_defense': 18, 'base_speed': 10,
        'skills_pool': ['污染净化', '自我修复', '消毒喷雾'], 'min_skills': 1, 'max_skills': 2,
        'description': '净化友方负面效果',
        'passive_abilities': ['bless'],
    },
    'lab_generator': {
        'name': '应急发电机', 'color': '#ffd54f',
        'base_health': 120, 'base_attack': 6, 'base_defense': 12, 'base_speed': 4,
        'skills_pool': ['能量护盾', '机械充能'], 'min_skills': 1, 'max_skills': 2,
        'description': '能量核心为友方充能',
        'passive_abilities': ['death_explode'],
    },
    'lab_containment': {
        'name': '收容单元', 'color': '#bf360c',
        'base_health': 60, 'base_attack': 10, 'base_defense': 4, 'base_speed': 8,
        'skills_pool': ['自爆'], 'min_skills': 1, 'max_skills': 1,
        'description': '被击破时大范围爆炸',
    },
    'lab_crawler': {
        'name': '爬行异虫', 'color': '#33691e',
        'base_health': 75, 'base_attack': 22, 'base_defense': 4, 'base_speed': 18,
        'skills_pool': ['隐身', '毒液攻击'], 'min_skills': 1, 'max_skills': 2,
        'description': '隐身接近后剧毒攻击',
    },
    'lab_overlord': {
        'name': '监管者机甲', 'color': '#37474f',
        'base_health': 250, 'base_attack': 32, 'base_defense': 24, 'base_speed': 12,
        'skills_pool': ['护卫铁壁', '腐蚀酸液', '能量护盾', '召唤'], 'min_skills': 2, 'max_skills': 3,
        'description': '实验室最终防御系统',
        'passive_abilities': ['attack_aura', 'defense_aura'],
    },

    # ===== 远古遗迹 新增敌人 =====
    'ruins_sentry': {
        'name': '符文哨兵', 'color': '#bcaaa4',
        'base_health': 85, 'base_attack': 22, 'base_defense': 10, 'base_speed': 16,
        'skills_pool': ['锁定狙击', '快速生长'], 'min_skills': 1, 'max_skills': 2,
        'description': '远程侦测并标记弱点',
    },
    'ruins_golem': {
        'name': '符文魔像', 'color': '#6d4c41',
        'base_health': 220, 'base_attack': 16, 'base_defense': 24, 'base_speed': 6,
        'skills_pool': ['石化之躯', '能量护盾'], 'min_skills': 1, 'max_skills': 2,
        'description': '符文护盾吸收魔法伤害',
        'passive_abilities': ['rune_ward'],
    },
    'ruins_phantom': {
        'name': '幻影守卫', 'color': '#ce93d8',
        'base_health': 80, 'base_attack': 18, 'base_defense': 6, 'base_speed': 22,
        'skills_pool': ['隐身', '幻觉制造', '瞬移'], 'min_skills': 1, 'max_skills': 2,
        'description': '高闪避扰乱阵型',
    },
    'ruins_trap': {
        'name': '地刺陷阱', 'color': '#78909c',
        'base_health': 70, 'base_attack': 26, 'base_defense': 4, 'base_speed': 10,
        'skills_pool': ['毒液攻击', '麻痹神经'], 'min_skills': 1, 'max_skills': 2,
        'description': '隐藏在地面，攻击附带麻痹',
    },
    'ruins_obelisk': {
        'name': '符文方尖碑', 'color': '#ffcc80',
        'base_health': 180, 'base_attack': 10, 'base_defense': 20, 'base_speed': 4,
        'skills_pool': ['能量护盾', '古代守护'], 'min_skills': 1, 'max_skills': 2,
        'description': '提升友方生命上限并套盾',
        'passive_abilities': ['fortify', 'shield_aura'],
    },
    'ruins_mummy': {
        'name': '诅咒木乃伊', 'color': '#a1887f',
        'base_health': 120, 'base_attack': 20, 'base_defense': 14, 'base_speed': 10,
        'skills_pool': ['诅咒', '毒雾扩散'], 'min_skills': 1, 'max_skills': 2,
        'description': '死亡时诅咒全体玩家',
        'passive_abilities': ['death_curse'],
    },
    'ruins_scarab': {
        'name': '圣甲虫群', 'color': '#ffb300',
        'base_health': 60, 'base_attack': 14, 'base_defense': 6, 'base_speed': 20,
        'skills_pool': ['毒液攻击', '快速生长'], 'min_skills': 1, 'max_skills': 2,
        'description': '每存在一个友方攻击+10%',
        'passive_abilities': ['swarm_rally'],
    },
    'ruins_priestess': {
        'name': '古代祭司', 'color': '#f8bbd0',
        'base_health': 130, 'base_attack': 10, 'base_defense': 16, 'base_speed': 12,
        'skills_pool': ['甘霖', '自我修复', '污染净化'], 'min_skills': 2, 'max_skills': 3,
        'description': '每回合治疗全体友方',
        'passive_abilities': ['heal_aura'],
    },
    'ruins_warrior': {
        'name': '古代战士', 'color': '#8d6e63',
        'base_health': 150, 'base_attack': 22, 'base_defense': 16, 'base_speed': 14,
        'skills_pool': ['狂暴释放', '快速生长'], 'min_skills': 1, 'max_skills': 2,
        'description': '低血量狂暴翻倍',
        'passive_abilities': ['enrage'],
    },
    'ruins_archer': {
        'name': '古代弓手', 'color': '#d7ccc8',
        'base_health': 90, 'base_attack': 28, 'base_defense': 6, 'base_speed': 18,
        'skills_pool': ['锁定狙击', '隐身'], 'min_skills': 1, 'max_skills': 2,
        'description': '优先攻击最弱目标',
        'passive_abilities': ['focus_weak'],
    },
    'ruins_sphinx': {
        'name': '斯芬克斯', 'color': '#ffd54f',
        'base_health': 160, 'base_attack': 20, 'base_defense': 14, 'base_speed': 14,
        'skills_pool': ['混沌诅咒', '幻觉制造', '沙暴迷眼'], 'min_skills': 1, 'max_skills': 2,
        'description': '谜题之力混乱全场',
    },
    'ruins_serpent': {
        'name': '羽蛇神', 'color': '#81c784',
        'base_health': 130, 'base_attack': 30, 'base_defense': 12, 'base_speed': 20,
        'skills_pool': ['连锁闪电', '快速生长', '能量吸收'], 'min_skills': 1, 'max_skills': 2,
        'description': '操控风雷之力的神兽',
    },
    'ruins_gate': {
        'name': '封印之门', 'color': '#5d4037',
        'base_health': 200, 'base_attack': 6, 'base_defense': 30, 'base_speed': 4,
        'skills_pool': ['召唤', '能量护盾'], 'min_skills': 1, 'max_skills': 2,
        'description': '每回合召唤古代战士',
        'passive_abilities': ['gate_guard'],
    },
    'ruins_hieroglyph': {
        'name': '咒文石碑', 'color': '#ffcc02',
        'base_health': 100, 'base_attack': 24, 'base_defense': 12, 'base_speed': 8,
        'skills_pool': ['诅咒扩散', '符文爆破'], 'min_skills': 1, 'max_skills': 2,
        'description': '铭刻咒文蓄力爆发',
    },
    'ruins_titan': {
        'name': '泰坦守卫', 'color': '#4e342e',
        'base_health': 350, 'base_attack': 34, 'base_defense': 30, 'base_speed': 8,
        'skills_pool': ['石化之躯', '地裂波动', '狂暴释放'], 'min_skills': 2, 'max_skills': 3,
        'description': '远古最终守护者',
        'passive_abilities': ['aoe_barrier', 'iron_wall'],
    },

    # ===== 虚空裂隙 新增敌人 =====
    'rift_worm': {
        'name': '虚空蠕虫', 'color': '#6a1b9a',
        'base_health': 110, 'base_attack': 20, 'base_defense': 12, 'base_speed': 14,
        'skills_pool': ['虚空牵引', '毒液攻击'], 'min_skills': 1, 'max_skills': 2,
        'description': '从地底钻出袭击后排',
    },
    'rift_shade': {
        'name': '虚空之影', 'color': '#311b92',
        'base_health': 70, 'base_attack': 30, 'base_defense': 4, 'base_speed': 26,
        'skills_pool': ['背刺突袭', '隐身'], 'min_skills': 1, 'max_skills': 2,
        'description': '隐匿中攻击力翻倍',
        'passive_abilities': ['shadow_meld'],
    },
    'rift_crystal': {
        'name': '虚空水晶', 'color': '#7b1fa2',
        'base_health': 140, 'base_attack': 8, 'base_defense': 22, 'base_speed': 6,
        'skills_pool': ['虚空风暴', '能量护盾'], 'min_skills': 1, 'max_skills': 2,
        'description': '每回合对玩家造成虚空伤害',
        'passive_abilities': ['void_radiance'],
    },
    'rift_demon': {
        'name': '次元恶魔', 'color': '#b71c1c',
        'base_health': 160, 'base_attack': 32, 'base_defense': 14, 'base_speed': 16,
        'skills_pool': ['狂暴释放', '火焰吐息', '诅咒'], 'min_skills': 1, 'max_skills': 2,
        'description': '低血量狂暴',
        'passive_abilities': ['berserk'],
    },
    'rift_bubble': {
        'name': '泡沫幻影', 'color': '#e1bee7',
        'base_health': 60, 'base_attack': 12, 'base_defense': 4, 'base_speed': 18,
        'skills_pool': ['隐身', '幻觉制造', '瞬移'], 'min_skills': 1, 'max_skills': 2,
        'description': '受到攻击时产生幻影分身',
        'passive_abilities': ['mirage_clone'],
    },
    'rift_flux': {
        'name': '熵增体', 'color': '#00bfa5',
        'base_health': 120, 'base_attack': 18, 'base_defense': 10, 'base_speed': 16,
        'skills_pool': ['虚空风暴', '腐蚀酸液'], 'min_skills': 1, 'max_skills': 2,
        'description': '每回合对随机玩家造成伤害',
        'passive_abilities': ['entropic_aura'],
    },
    'rift_gazer': {
        'name': '凝视者', 'color': '#4a148c',
        'base_health': 100, 'base_attack': 22, 'base_defense': 10, 'base_speed': 18,
        'skills_pool': ['恐惧凝视', '混沌诅咒'], 'min_skills': 1, 'max_skills': 2,
        'description': '虚空凝视恐惧目标',
    },
    'rift_imp': {
        'name': '虚空小鬼', 'color': '#aa00ff',
        'base_health': 50, 'base_attack': 18, 'base_defense': 4, 'base_speed': 22,
        'skills_pool': ['背刺突袭', '麻痹神经'], 'min_skills': 1, 'max_skills': 2,
        'description': '高速低血量的骚扰单位',
    },
    'rift_behemoth': {
        'name': '虚空巨兽', 'color': '#1a237e',
        'base_health': 350, 'base_attack': 28, 'base_defense': 28, 'base_speed': 6,
        'skills_pool': ['虚空风暴', '能量护盾', '自我修复'], 'min_skills': 2, 'max_skills': 3,
        'description': '巨大虚空身躯减伤30%',
        'passive_abilities': ['void_shield'],
    },
    'rift_siren': {
        'name': '虚空塞壬', 'color': '#f48fb1',
        'base_health': 100, 'base_attack': 16, 'base_defense': 10, 'base_speed': 18,
        'skills_pool': ['睡眠诱导', '幻觉制造', '甘霖'], 'min_skills': 1, 'max_skills': 2,
        'description': '歌声迷惑玩家',
    },
    'rift_wraith': {
        'name': '虚空怨灵', 'color': '#4a148c',
        'base_health': 90, 'base_attack': 24, 'base_defense': 8, 'base_speed': 20,
        'skills_pool': ['诅咒', '背刺突袭', '隐身'], 'min_skills': 1, 'max_skills': 2,
        'description': '死亡时对全体造成伤害',
        'passive_abilities': ['vengeance'],
    },
    'rift_spawn': {
        'name': '虚空之子', 'color': '#d500f9',
        'base_health': 80, 'base_attack': 14, 'base_defense': 8, 'base_speed': 14,
        'skills_pool': ['快速生长', '属性镜像'], 'min_skills': 1, 'max_skills': 2,
        'description': '每回合成长，属性逐渐提升',
        'passive_abilities': ['void_growth'],
    },
    'rift_anchor': {
        'name': '锚点核心', 'color': '#263238',
        'base_health': 200, 'base_attack': 12, 'base_defense': 24, 'base_speed': 4,
        'skills_pool': ['虚空牵引', '时间迟滞', '能量护盾'], 'min_skills': 1, 'max_skills': 2,
        'description': '锁定所有玩家位置，禁止位移',
        'passive_abilities': ['anchor_field'],
    },
    'rift_mirage': {
        'name': '海市蜃楼', 'color': '#80cbc4',
        'base_health': 100, 'base_attack': 10, 'base_defense': 20, 'base_speed': 10,
        'skills_pool': ['幻觉制造', '混沌诅咒', '空间扭曲'], 'min_skills': 1, 'max_skills': 2,
        'description': '制造幻象迷惑玩家阵型',
    },
    'rift_dragon': {
        'name': '虚空龙裔', 'color': '#1a237e',
        'base_health': 320, 'base_attack': 38, 'base_defense': 22, 'base_speed': 18,
        'skills_pool': ['虚空风暴', '虚空牵引', '火焰吐息', '连锁闪电'], 'min_skills': 2, 'max_skills': 3,
        'description': '虚空龙族后裔，统领虚空',
        'passive_abilities': ['void_lord'],
    },

    # ===== 元素位面 新增敌人 =====
    'elem_magma': {
        'name': '熔岩元素', 'color': '#bf360c',
        'base_health': 140, 'base_attack': 34, 'base_defense': 10, 'base_speed': 12,
        'skills_pool': ['灼烧', '火焰吐息', '澎湃'], 'min_skills': 1, 'max_skills': 2,
        'description': '每回合灼烧伤害递增',
        'passive_abilities': ['overheat'],
    },
    'elem_crystal': {
        'name': '冰晶元素', 'color': '#80deea',
        'base_health': 180, 'base_attack': 18, 'base_defense': 22, 'base_speed': 8,
        'skills_pool': ['冻结', '冰霜护盾', '石化之躯'], 'min_skills': 1, 'max_skills': 2,
        'description': '攻击者被冻结',
        'passive_abilities': ['frost_armor'],
    },
    'elem_storm': {
        'name': '风暴元素', 'color': '#b2ebf2',
        'base_health': 100, 'base_attack': 26, 'base_defense': 6, 'base_speed': 24,
        'skills_pool': ['连锁闪电', '快速生长', '隐身'], 'min_skills': 1, 'max_skills': 2,
        'description': '高速风雷混合攻击',
    },
    'elem_metal': {
        'name': '金属元素', 'color': '#90a4ae',
        'base_health': 240, 'base_attack': 20, 'base_defense': 30, 'base_speed': 6,
        'skills_pool': ['钢铁壁垒', '能量护盾'], 'min_skills': 1, 'max_skills': 2,
        'description': '高额护甲和反伤',
        'passive_abilities': ['thorns_aura'],
    },
    'elem_nature': {
        'name': '自然元素', 'color': '#66bb6a',
        'base_health': 160, 'base_attack': 12, 'base_defense': 18, 'base_speed': 12,
        'skills_pool': ['甘霖', '自我修复', '毒液攻击'], 'min_skills': 1, 'max_skills': 2,
        'description': '每回合恢复生命',
        'passive_abilities': ['regeneration'],
    },
    'elem_light': {
        'name': '光之元素', 'color': '#fff176',
        'base_health': 130, 'base_attack': 18, 'base_defense': 14, 'base_speed': 16,
        'skills_pool': ['甘霖', '污染净化', '能量护盾'], 'min_skills': 2, 'max_skills': 3,
        'description': '每回合净化负面效果',
        'passive_abilities': ['bless'],
    },
    'elem_dark': {
        'name': '暗之元素', 'color': '#5d4037',
        'base_health': 100, 'base_attack': 30, 'base_defense': 8, 'base_speed': 20,
        'skills_pool': ['诅咒', '背刺突袭', '隐身'], 'min_skills': 1, 'max_skills': 2,
        'description': '黑暗诅咒+背刺',
    },
    'elem_steam': {
        'name': '蒸汽元素', 'color': '#bcaaa4',
        'base_health': 120, 'base_attack': 22, 'base_defense': 12, 'base_speed': 16,
        'skills_pool': ['灼烧', '毒雾扩散', '隐身'], 'min_skills': 1, 'max_skills': 2,
        'description': '灼热蒸汽灼烧全场',
    },
    'elem_mud': {
        'name': '泥浆元素', 'color': '#795548',
        'base_health': 180, 'base_attack': 14, 'base_defense': 20, 'base_speed': 6,
        'skills_pool': ['地裂波动', '时间迟滞', '麻痹神经'], 'min_skills': 1, 'max_skills': 2,
        'description': '泥沼减速+地震',
    },
    'elem_lava_beast': {
        'name': '熔岩巨兽', 'color': '#e65100',
        'base_health': 300, 'base_attack': 30, 'base_defense': 20, 'base_speed': 8,
        'skills_pool': ['火焰吐息', '灼烧', '狂暴释放', '自我修复'], 'min_skills': 2, 'max_skills': 3,
        'description': '熔岩护甲低血量狂暴',
        'passive_abilities': ['berserk'],
    },
    'elem_cyclone': {
        'name': '飓风元素', 'color': '#80cbc4',
        'base_health': 110, 'base_attack': 20, 'base_defense': 8, 'base_speed': 22,
        'skills_pool': ['虚空牵引', '观星', '连锁闪电'], 'min_skills': 1, 'max_skills': 2,
        'description': '飓风卷走并混乱目标',
    },
    'elem_aurora': {
        'name': '极光元素', 'color': '#ce93d8',
        'base_health': 140, 'base_attack': 16, 'base_defense': 16, 'base_speed': 16,
        'skills_pool': ['甘霖', '澎湃', '能量护盾', '快速生长'], 'min_skills': 2, 'max_skills': 3,
        'description': '极光之力全面提升友方',
    },
    'elem_prism': {
        'name': '棱晶元素', 'color': '#f8bbd0',
        'base_health': 120, 'base_attack': 24, 'base_defense': 14, 'base_speed': 14,
        'skills_pool': ['连锁闪电', '冰霜护盾', '属性镜像'], 'min_skills': 1, 'max_skills': 2,
        'description': '棱镜折射反射部分伤害',
        'passive_abilities': ['mirror_copy'],
    },
    'elem_fusion': {
        'name': '融合元素', 'color': '#ff6f00',
        'base_health': 170, 'base_attack': 32, 'base_defense': 16, 'base_speed': 14,
        'skills_pool': ['火焰吐息', '冻结', '连锁闪电', '地裂波动'], 'min_skills': 2, 'max_skills': 3,
        'description': '同时掌握两种元素之力',
        'passive_abilities': ['elemental_siphon'],
    },
    'elem_primordial': {
        'name': '原始元素', 'color': '#ffd600',
        'base_health': 350, 'base_attack': 40, 'base_defense': 24, 'base_speed': 16,
        'skills_pool': ['地裂波动', '连锁闪电', '灼烧', '冻结', '虚空风暴'], 'min_skills': 3, 'max_skills': 4,
        'description': '元素诞生之初的原始之力',
        'passive_abilities': ['element_cycle', 'aoe_barrier'],
    },

    # ===== 深渊之底 新增敌人 =====
    'abyss_hound': {
        'name': '深渊猎犬', 'color': '#212121',
        'base_health': 120, 'base_attack': 28, 'base_defense': 10, 'base_speed': 20,
        'skills_pool': ['恐惧凝视', '快速生长'], 'min_skills': 1, 'max_skills': 2,
        'description': '追击最虚弱目标不死不休',
    },
    'abyss_lurker': {
        'name': '深渊潜伏者', 'color': '#1b1b2f',
        'base_health': 90, 'base_attack': 32, 'base_defense': 6, 'base_speed': 22,
        'skills_pool': ['背刺突袭', '隐身'], 'min_skills': 1, 'max_skills': 2,
        'description': '从暗影中突袭必暴击',
    },
    'abyss_tendril': {
        'name': '深渊触须', 'color': '#2a0a2a',
        'base_health': 130, 'base_attack': 18, 'base_defense': 14, 'base_speed': 14,
        'skills_pool': ['虚空牵引', '麻痹神经'], 'min_skills': 1, 'max_skills': 2,
        'description': '多根触须缠绕全体',
    },
    'abyss_eye': {
        'name': '深渊之眼', 'color': '#1a0033',
        'base_health': 100, 'base_attack': 24, 'base_defense': 10, 'base_speed': 18,
        'skills_pool': ['锁定狙击', '诅咒'], 'min_skills': 1, 'max_skills': 2,
        'description': '破除隐身并标记弱点',
    },
    'abyss_priest': {
        'name': '深渊祭司', 'color': '#3c1053',
        'base_health': 140, 'base_attack': 20, 'base_defense': 16, 'base_speed': 12,
        'skills_pool': ['诅咒', '绝望诅咒', '混沌诅咒'], 'min_skills': 1, 'max_skills': 2,
        'description': '为友方献祭治疗、敌方施加诅咒',
    },
    'abyss_maw': {
        'name': '深渊巨口', 'color': '#1a0000',
        'base_health': 280, 'base_attack': 26, 'base_defense': 24, 'base_speed': 6,
        'skills_pool': ['能量吸收', '处决'], 'min_skills': 1, 'max_skills': 2,
        'description': '吞噬目标回复自身',
    },
    'abyss_shadow': {
        'name': '深渊暗影', 'color': '#0d0d0d',
        'base_health': 80, 'base_attack': 22, 'base_defense': 4, 'base_speed': 24,
        'skills_pool': ['隐身', '背刺突袭', '幻觉制造'], 'min_skills': 1, 'max_skills': 2,
        'description': '每次攻击后留下暗影分身',
        'passive_abilities': ['shadow_clone'],
    },
    'abyss_caller': {
        'name': '深渊呼唤者', 'color': '#4a0e4a',
        'base_health': 130, 'base_attack': 14, 'base_defense': 14, 'base_speed': 10,
        'skills_pool': ['召唤', '快速生长', '澎湃'], 'min_skills': 1, 'max_skills': 2,
        'description': '召唤深渊生物并使友方强化',
    },
    'abyss_beast': {
        'name': '深渊巨兽', 'color': '#1a1a00',
        'base_health': 320, 'base_attack': 34, 'base_defense': 22, 'base_speed': 10,
        'skills_pool': ['狂暴释放', '地裂波动', '恐惧凝视'], 'min_skills': 2, 'max_skills': 3,
        'description': '深渊巨兽越战越狂',
        'passive_abilities': ['berserk'],
    },
    'abyss_wisp': {
        'name': '深渊鬼火', 'color': '#4a004a',
        'base_health': 60, 'base_attack': 16, 'base_defense': 2, 'base_speed': 26,
        'skills_pool': ['诅咒', '灼烧', '瞬移'], 'min_skills': 1, 'max_skills': 2,
        'description': '极速鬼火穿梭攻击',
    },
    'abyss_statue': {
        'name': '深渊雕像', 'color': '#2a2a2a',
        'base_health': 220, 'base_attack': 12, 'base_defense': 30, 'base_speed': 4,
        'skills_pool': ['石化之躯', '绝望诅咒', '恐惧凝视'], 'min_skills': 1, 'max_skills': 2,
        'description': '石化状态中持续施加负面效果',
    },
    'abyss_crawler': {
        'name': '深渊爬行者', 'color': '#1a2a1a',
        'base_health': 200, 'base_attack': 20, 'base_defense': 20, 'base_speed': 12,
        'skills_pool': ['毒液攻击', '毒雾扩散', '自我修复'], 'min_skills': 1, 'max_skills': 2,
        'description': '剧毒之躯持续放毒',
        'passive_abilities': ['toxic_aura'],
    },
    'abyss_herald': {
        'name': '深渊先驱', 'color': '#3a003a',
        'base_health': 200, 'base_attack': 36, 'base_defense': 18, 'base_speed': 18,
        'skills_pool': ['虚空风暴', '远古裁决', '绝望诅咒', '恐惧凝视'], 'min_skills': 2, 'max_skills': 3,
        'description': '混沌降临前的宣告者',
    },
    'abyss_devourer': {
        'name': '深渊吞噬者', 'color': '#1a0000',
        'base_health': 350, 'base_attack': 40, 'base_defense': 26, 'base_speed': 14,
        'skills_pool': ['能量吸收', '处决', '火焰吐息', '自我修复'], 'min_skills': 2, 'max_skills': 3,
        'description': '击杀目标永久提升属性',
        'passive_abilities': ['soul_eater'],
    },
    'abyss_nightmare': {
        'name': '梦魇化身', 'color': '#0a003a',
        'base_health': 280, 'base_attack': 38, 'base_defense': 20, 'base_speed': 20,
        'skills_pool': ['梦魇侵袭', '恐惧凝视', '睡眠诱导', '混沌诅咒'], 'min_skills': 2, 'max_skills': 3,
        'description': '深渊噩梦的具象化',
        'passive_abilities': ['fear_aura', 'heal_reduction'],
    },

    # ==================== 地图2：远古遗迹 ====================
    'ruins_guardian': {
        'name': '巨石守卫', 'color': '#c9a96e',
        'base_health': 250, 'base_attack': 14, 'base_defense': 28, 'base_speed': 4,
        'skills_pool': ['石化之躯'], 'min_skills': 1, 'max_skills': 1,
        'description': '石化自身换取巨额护盾和减伤',
    },
    'ruins_ballista': {
        'name': '机关弩车', 'color': '#a1887f',
        'base_health': 100, 'base_attack': 30, 'base_defense': 8, 'base_speed': 10,
        'skills_pool': ['锁定狙击'], 'min_skills': 1, 'max_skills': 1,
        'description': '每回合锁定同一目标，伤害递增20%',
        'passive_abilities': ['stacking_damage'],
    },
    'ruins_statue': {
        'name': '诅咒雕像', 'color': '#8d6e63',
        'base_health': 130, 'base_attack': 12, 'base_defense': 18, 'base_speed': 8,
        'skills_pool': ['诅咒扩散'], 'min_skills': 1, 'max_skills': 1,
        'description': '每回合给全体玩家随机添加一种debuff',
        'passive_abilities': ['curse_spread'],
    },
    'ruins_hourglass': {
        'name': '时间沙漏', 'color': '#d4a574',
        'base_health': 110, 'base_attack': 8, 'base_defense': 14, 'base_speed': 20,
        'skills_pool': ['时间迟滞'], 'min_skills': 1, 'max_skills': 1,
        'description': '降低全体玩家行动条',
        'passive_abilities': ['time_drain'],
    },
    'ruins_boss': {
        'name': '远古守护神', 'color': '#fdd835',
        'base_health': 500, 'base_attack': 38, 'base_defense': 26, 'base_speed': 16,
        'skills_pool': ['石化之躯', '锁定狙击', '时间迟滞', '远古裁决'],
        'min_skills': 3, 'max_skills': 4,
        'description': '时间领域：玩家每行动一次BOSS获得1层充能，10层释放全屏AOE',
        'passive_abilities': ['tick_charge'],
    },

    # ==================== 地图3：虚空裂隙 ====================
    'rift_tentacle': {
        'name': '虚空触须', 'color': '#7c4dff',
        'base_health': 100, 'base_attack': 20, 'base_defense': 10, 'base_speed': 16,
        'skills_pool': ['虚空牵引'], 'min_skills': 1, 'max_skills': 1,
        'description': '将玩家单位拉至后排空位，打乱阵型',
    },
    'rift_hunter': {
        'name': '次元猎手', 'color': '#9c27b0',
        'base_health': 80, 'base_attack': 34, 'base_defense': 6, 'base_speed': 24,
        'skills_pool': ['背刺突袭'], 'min_skills': 1, 'max_skills': 1,
        'description': '瞬移至最虚弱的玩家身后，造成额外背击伤害',
    },
    'rift_eye': {
        'name': '混沌之眼', 'color': '#e040fb',
        'base_health': 120, 'base_attack': 16, 'base_defense': 12, 'base_speed': 14,
        'skills_pool': ['混沌诅咒'], 'min_skills': 1, 'max_skills': 1,
        'description': '每回合让随机玩家获得随机debuff',
    },
    'rift_mirror': {
        'name': '镜像畸体', 'color': '#ce93d8',
        'base_health': 150, 'base_attack': 10, 'base_defense': 10, 'base_speed': 12,
        'skills_pool': ['属性镜像'], 'min_skills': 1, 'max_skills': 1,
        'description': '复制最高攻击玩家的攻击力',
        'passive_abilities': ['mirror_copy'],
    },
    'rift_boss': {
        'name': '虚空领主·降临', 'color': '#d500f9',
        'base_health': 600, 'base_attack': 45, 'base_defense': 24, 'base_speed': 22,
        'skills_pool': ['虚空牵引', '背刺突袭', '混沌诅咒', '虚空风暴'],
        'min_skills': 3, 'max_skills': 4,
        'description': '每回合召唤虚空触须，触须存在时BOSS减伤50%',
        'passive_abilities': ['void_rift_lord'],
    },

    # ==================== 地图4：元素位面 ====================
    'elem_fire': {
        'name': '烈焰元素', 'color': '#ff5722',
        'base_health': 130, 'base_attack': 32, 'base_defense': 8, 'base_speed': 14,
        'skills_pool': ['火焰吐息', '灼烧'], 'min_skills': 1, 'max_skills': 2,
        'description': '灼烧伤害+50%，死亡时爆炸造成范围火伤',
        'passive_abilities': ['fire_death'],
    },
    'elem_ice': {
        'name': '冰川元素', 'color': '#81d4fa',
        'base_health': 200, 'base_attack': 14, 'base_defense': 24, 'base_speed': 6,
        'skills_pool': ['冻结', '冰霜护盾'], 'min_skills': 1, 'max_skills': 2,
        'description': '冻结攻击者，被击破时治疗全体友方',
        'passive_abilities': ['ice_death'],
    },
    'elem_thunder': {
        'name': '雷霆元素', 'color': '#ffeb3b',
        'base_health': 120, 'base_attack': 28, 'base_defense': 10, 'base_speed': 18,
        'skills_pool': ['连锁闪电'], 'min_skills': 1, 'max_skills': 1,
        'description': '连锁闪电弹射3个目标，麻痹命中的目标',
    },
    'elem_earth': {
        'name': '大地元素', 'color': '#8d6e63',
        'base_health': 280, 'base_attack': 16, 'base_defense': 32, 'base_speed': 4,
        'skills_pool': ['地裂波动'], 'min_skills': 1, 'max_skills': 1,
        'description': '地震波对全体玩家造成当前生命%伤害',
    },
    'elem_boss': {
        'name': '元素之核', 'color': '#ff6b35',
        'base_health': 500, 'base_attack': 36, 'base_defense': 22, 'base_speed': 16,
        'skills_pool': ['火焰吐息', '冻结', '连锁闪电', '地裂波动'],
        'min_skills': 3, 'max_skills': 4,
        'description': '每3回合轮换元素形态（火→冰→雷→地），对当前元素免疫',
        'passive_abilities': ['element_cycle'],
    },

    # ==================== 地图5：深渊之底 ====================
    'abyss_gazer': {
        'name': '深渊凝视者', 'color': '#1a1a2e',
        'base_health': 140, 'base_attack': 22, 'base_defense': 14, 'base_speed': 18,
        'skills_pool': ['恐惧凝视'], 'min_skills': 1, 'max_skills': 1,
        'description': '恐惧目标使其行动条倒退',
        'passive_abilities': ['fear_aura'],
    },
    'abyss_weaver': {
        'name': '梦魇编织者', 'color': '#2d2d44',
        'base_health': 110, 'base_attack': 26, 'base_defense': 8, 'base_speed': 16,
        'skills_pool': ['睡眠诱导', '梦魇侵袭'], 'min_skills': 1, 'max_skills': 2,
        'description': '睡眠中的玩家每回合损失15%最大生命',
    },
    'abyss_apostle': {
        'name': '绝望使徒', 'color': '#3d1a3d',
        'base_health': 130, 'base_attack': 18, 'base_defense': 16, 'base_speed': 12,
        'skills_pool': ['绝望诅咒'], 'min_skills': 1, 'max_skills': 1,
        'description': '降低全体玩家的治疗效果',
        'passive_abilities': ['heal_reduction'],
    },
    'abyss_knight': {
        'name': '终焉骑士', 'color': '#4a0e17',
        'base_health': 300, 'base_attack': 30, 'base_defense': 28, 'base_speed': 8,
        'skills_pool': ['处决', '钢铁壁垒'], 'min_skills': 1, 'max_skills': 2,
        'description': '生命低于50%时获得50%斩杀线',
        'passive_abilities': ['execute_mastery'],
    },
    'abyss_boss': {
        'name': '原初混沌', 'color': '#0d0d0d',
        'base_health': 800, 'base_attack': 55, 'base_defense': 30, 'base_speed': 26,
        'skills_pool': ['恐惧凝视', '梦魇侵袭', '绝望诅咒', '远古裁决', '虚空风暴', '狂暴释放'],
        'min_skills': 4, 'max_skills': 6,
        'description': '最终Boss！拥有所有地图Boss的招牌技能，分3阶段战斗',
        'passive_abilities': ['primordial_chaos'],
        'trigger_all_skills': True,
    },
}

STAGE_TITLES = [
    '初入战场', '双重威胁', '变异初现', '精英阻击', '首领之战',
    '深入腹地', '暗影突袭', '基因狂潮', '钢铁防线', '霸主降临',
    '混沌深渊', '异界之门', '亡者归来', '血月之夜', '魔王觉醒',
    '虚空裂缝', '元素暴走', '机械军团', '远古遗迹', '终焉审判',
    '无尽炼狱', '星辰陨落', '末日曙光', '神之试炼', '浩劫重生',
    '秩序崩塌', '混沌再临', '最终抉择', '创世之战', '超越极限',
    '侦查前线', '烈焰风暴', '极寒冰域', '剧毒深渊', '雷霆万钧',
    '虚空漫游', '暗影刺杀', '治愈结界', '钢铁长城', '疯狂实验',
    '爆破禁区', '梦境沉沦', '蛛网密布', '能量汲取', '召唤大军',
    '星辰紊乱', '基因暴走', '水晶迷阵', '混沌降临', '吞噬天地',
    '虚空降临', '元素浩劫', '暗影帷幕', '基因末日', '永恒之战',
    '多元崩塌', '终焉序曲', '虚空王座', '创世之痕', '超越彼岸',
    # 61-100
    '狼蛛巢穴', '暗影刺杀', '冰霜巨人', '诅咒暗影', '熔岩地狱',
    '晶壁迷阵', '等离子场', '纳米虫灾', '死亡收割', '电磁风暴',
    '毒雾深渊', '钢铁巨像', '时空乱流', '星灵守护', '天使陨落',
    '骨龙墓地', '深渊之门', '末日审判', '机械神域', '虚空毁灭',
    '永恒守卫', '混沌深渊', '基因崩坏', '虚空侵蚀', '最终序曲',
    '诸神黄昏', '新世界', '基因觉醒', '超越神域', '终焉之战',
    '虚空万物', '混沌归一', '不朽传说', '基因永恒', '星辰大海',
    '无限可能', '超越极限', '创世神话', '终焉审判', '新纪元',
]

# ============================================================
# 地图系统定义
# ============================================================
MAPS = {
    'abandoned_lab': {
        'id': 'abandoned_lab', 'name': '废弃实验室',
        'unlock_stage': 100, 'start_stage': 101, 'stages': 20,
        'color': '#7cba3c',
        'description': '废弃基因实验室的残骸，到处弥漫着腐蚀性气体和失控的突变体。',
        'enemy_pool': ['lab_slime', 'lab_culture', 'lab_barrel', 'lab_security', 'lab_mutanthound', 'lab_centrifuge', 'lab_gasleak', 'lab_mercury', 'lab_eyestalk', 'lab_tentacle', 'lab_zombie', 'lab_injector', 'lab_fumes', 'lab_amalgam', 'lab_cleaner', 'lab_generator', 'lab_containment', 'lab_crawler', 'lab_overlord', 'lab_boss'],
        'boss_interval': 5,
    },
    'ancient_ruins': {
        'id': 'ancient_ruins', 'name': '远古遗迹',
        'unlock_stage': 120, 'start_stage': 121, 'stages': 20,
        'color': '#c9a96e',
        'description': '埋藏千年的古代文明遗迹，守护者仍然在执行最后的命令。',
        'enemy_pool': ['ruins_guardian', 'ruins_ballista', 'ruins_statue', 'ruins_hourglass', 'ruins_sentry', 'ruins_golem', 'ruins_phantom', 'ruins_trap', 'ruins_obelisk', 'ruins_mummy', 'ruins_scarab', 'ruins_priestess', 'ruins_warrior', 'ruins_archer', 'ruins_sphinx', 'ruins_serpent', 'ruins_gate', 'ruins_hieroglyph', 'ruins_titan', 'ruins_boss'],
        'boss_interval': 5,
    },
    'void_rift': {
        'id': 'void_rift', 'name': '虚空裂隙',
        'unlock_stage': 140, 'start_stage': 141, 'stages': 20,
        'color': '#8b5cf6',
        'description': '现实与虚空的边界正在消融，异界生物从中涌出。',
        'enemy_pool': ['rift_tentacle', 'rift_hunter', 'rift_eye', 'rift_mirror', 'rift_worm', 'rift_shade', 'rift_crystal', 'rift_demon', 'rift_bubble', 'rift_flux', 'rift_gazer', 'rift_imp', 'rift_behemoth', 'rift_siren', 'rift_wraith', 'rift_spawn', 'rift_anchor', 'rift_mirage', 'rift_dragon', 'rift_boss'],
        'boss_interval': 5,
    },
    'elemental_plane': {
        'id': 'elemental_plane', 'name': '元素位面',
        'unlock_stage': 160, 'start_stage': 161, 'stages': 20,
        'color': '#ff6b35',
        'description': '纯粹元素之力构成的位面，元素领主在此统治。',
        'enemy_pool': ['elem_fire', 'elem_ice', 'elem_thunder', 'elem_earth', 'elem_magma', 'elem_crystal', 'elem_storm', 'elem_metal', 'elem_nature', 'elem_light', 'elem_dark', 'elem_steam', 'elem_mud', 'elem_lava_beast', 'elem_cyclone', 'elem_aurora', 'elem_prism', 'elem_fusion', 'elem_primordial', 'elem_boss'],
        'boss_interval': 5,
    },
    'abyss_bottom': {
        'id': 'abyss_bottom', 'name': '深渊之底',
        'unlock_stage': 180, 'start_stage': 181, 'stages': 20,
        'color': '#1a1a2e',
        'description': '一切噩梦的源头，终极混沌沉眠之地。',
        'enemy_pool': ['abyss_gazer', 'abyss_weaver', 'abyss_apostle', 'abyss_knight', 'abyss_hound', 'abyss_lurker', 'abyss_tendril', 'abyss_eye', 'abyss_priest', 'abyss_maw', 'abyss_shadow', 'abyss_caller', 'abyss_beast', 'abyss_wisp', 'abyss_statue', 'abyss_crawler', 'abyss_herald', 'abyss_devourer', 'abyss_nightmare', 'abyss_boss'],
        'boss_interval': 5,
    },
    'holy_sanctuary': {
        'id': 'holy_sanctuary', 'name': '圣堂',
        'unlock_stage': 200, 'start_stage': 201, 'stages': 20,
        'color': '#c0392b',
        'description': '被血肉腐蚀的圣殿，神圣与污秽在此交织。',
        'enemy_pool': ['sanctuary_ascetic', 'sanctuary_stitcher', 'sanctuary_atonement', 'sanctuary_chalice', 'sanctuary_idol', 'sanctuary_bloodpool', 'sanctuary_boneguard', 'sanctuary_penitent', 'sanctuary_deacon', 'sanctuary_apostle', 'sanctuary_relic', 'sanctuary_malformed', 'sanctuary_thorns', 'sanctuary_inquisitor', 'sanctuary_archbishop', 'sanctuary_ascetic', 'sanctuary_boneguard', 'sanctuary_bloodpool', 'sanctuary_thorns', 'sanctuary_archbishop'],
        'boss_interval': 5,
    },
}

MAP_STAGE_TITLES = {
    'abandoned_lab': [
        '腐蚀蔓延', '失控增殖', '毒液泄漏', '密室逃脱', '安保系统',
        '基因污染', '培养皿暴走', '废料处理区', '消毒通道', '狂暴实验体',
        '腐蚀深渊', '培育温室', '毒废料库', '机甲整备室', '变异体巢穴',
        '基因熔炉', '紧急封锁', '实验室核心', '最终样本', '暴走终端',
    ],
    'ancient_ruins': [
        '苏醒之石', '弩机阵列', '诅咒回廊', '时计塔', '守护者殿堂',
        '陷阱迷宫', '石像鬼群', '符文密室', '时间裂隙', '机关王座',
        '沉眠祭坛', '记忆碎片', '诅咒之源', '永恒之沙', '远古审判',
        '封印遗迹', '灵魂墓室', '时光尽头', '守护神魂', '远古觉醒',
    ],
    'void_rift': [
        '虚空渗透', '次元猎杀', '混沌凝视', '镜像迷宫', '裂隙领主',
        '空间扭曲', '暗影突袭', '熵增领域', '现实破碎', '虚空潮汐',
        '无光之海', '维度陷阱', '奇点逼近', '虚空共鸣', '领主降临',
        '位面崩塌', '虚空吞噬', '无限回廊', '裂隙核心', '终焉虚空',
    ],
    'elemental_plane': [
        '炎狱之门', '冰川走廊', '雷霆之径', '大地裂谷', '元素融合',
        '烈焰风暴', '永冻领域', '闪电网络', '地脉震荡', '混沌元素',
        '火雨降临', '极寒深渊', '雷暴中心', '地震核心', '元素暴走',
        '熔核爆发', '绝对零度', '万雷齐鸣', '地核崩塌', '元素湮灭',
    ],
    'abyss_bottom': [
        '深渊凝视', '梦魇降临', '绝望回廊', '骑士试炼', '混沌前兆',
        '恐惧深渊', '噩梦编织', '使徒集会', '终焉之路', '深渊低语',
        '黑暗之心', '灵魂吞噬', '绝望深渊', '骑士陨落', '混沌觉醒',
        '虚无之境', '噩梦终章', '深渊之门', '最终审判', '原初混沌',
    ],
    'holy_sanctuary': [
        '血染圣堂', '苦修之路', '红袍集会', '赎罪之门', '圣餐之殇',
        '缝合怪谈', '神像腐化', '忏悔回廊', '执事密室', '荆棘迷宫',
        '血肉使徒', '圣骸遗骨', '畸形摇篮', '审判大厅', '大主教的恩赐',
        '血池之内', '白骨之墙', '净化的代价', '圣堂深渊', '终焉祈祷',
    ],
}

def _pick_skills(template, stage):
    pool = template['skills_pool']
    if not pool:
        return []
    max_skills = template['max_skills']
    skill_count = min(template['min_skills'] + (stage - 1) // 5, max_skills)
    skill_count = min(skill_count, max_skills)
    if skill_count <= 0:
        return []
    return random.sample(pool, min(skill_count, len(pool)))

# ============================================================
# Boss/elite stat multipliers
# ============================================================
BOSS_STAT_MULTIPLIERS = {
    'boss': 1.3, 'overlord': 1.5, 'devourer': 1.4, 'void_overlord': 1.5,
    'abyss_lord': 1.5, 'mech_god': 1.6, 'void_destroyer': 1.6,
    'bone_dragon': 1.4, 'lab_boss': 1.3, 'ruins_boss': 1.4,
    'rift_boss': 1.4, 'elem_boss': 1.4, 'abyss_boss': 1.5,
    'void_dragon_god': 1.5, 'abyss_devourer': 1.5,
    'sanctuary_archbishop': 1.5,
}

# ============================================================
# Enemy synergy rules — giver type buffs target type(s)
# ============================================================
ENEMY_SYNERGIES = [
    # (giver_type, target_type, stat, multiplier)
    # target_type=None means all allies
    ('commander', 'soldier', 'attack', 1.2),
    ('commander', 'mutant', 'attack', 1.15),
    ('commander', 'elite', 'attack', 1.1),
    ('war_drummer', None, 'speed', 1.15),
    ('guardian_spirit', None, 'health', 1.15),
    ('healer', None, 'defense', 1.1),
    ('corruption_source', None, 'attack', 1.1),
    ('mad_scientist', 'gene_fusion', 'attack', 1.25),
    ('mad_scientist', 'gene_fusion', 'defense', 1.15),
    ('vengeful_wraith', None, 'attack', 1.1),
    ('purifier', None, 'defense', 1.1),
    ('annihilator', 'suicide_bomber', 'attack', 1.2),
]

SPECIAL_SKIP_EXTRA = {'rock'}


def _apply_synergies(enemies, enemy_types_in_stage):
    type_map = {e['_etype']: e for e in enemies}
    for giver, target, stat, mult in ENEMY_SYNERGIES:
        if giver not in enemy_types_in_stage:
            continue
        if target is None:
            for e in enemies:
                if stat == 'health':
                    e['health'] = int(e['health'] * mult)
                elif stat == 'attack':
                    e['attack'] = int(e['attack'] * mult)
                elif stat == 'defense':
                    e['defense'] = int(e['defense'] * mult)
                elif stat == 'speed':
                    e['speed'] = int(e['speed'] * mult)
        else:
            if target in enemy_types_in_stage:
                e = type_map.get(target)
                if e:
                    if stat == 'health':
                        e['health'] = int(e['health'] * mult)
                    elif stat == 'attack':
                        e['attack'] = int(e['attack'] * mult)
                    elif stat == 'defense':
                        e['defense'] = int(e['defense'] * mult)
                    elif stat == 'speed':
                        e['speed'] = int(e['speed'] * mult)


def _generate_stages():
    stages = {}

    for stage_num in range(1, 101):
        n = stage_num - 1
        health_scale = 1 + n * 0.05 + n * n * 0.0003
        stat_scale = 1 + n * 0.04 + n * n * 0.0002

        extra_count = 0
        if stage_num > 30:
            extra_count = 1
        if stage_num > 60:
            extra_count = 2
        if stage_num > 80:
            extra_count = 3

        enemy_config = []

        if stage_num <= 30:
            if stage_num == 1:
                enemy_config = [('basic', 1)]
            elif stage_num == 2:
                enemy_config = [('basic', 2)]
            elif stage_num == 3:
                enemy_config = [('basic', 1), ('soldier', 1)]
            elif stage_num <= 5:
                enemy_config = [('soldier', 2)]
            elif stage_num <= 7:
                enemy_config = [('soldier', 1), ('mutant', 2)]
            elif stage_num <= 10:
                enemy_config = [('mutant', 2), ('elite', 1)]
            elif stage_num <= 12:
                enemy_config = [('mutant', 2), ('elite', 2)]
            elif stage_num <= 15:
                enemy_config = [('elite', 2), ('mutant', 1)]
            elif stage_num <= 18:
                enemy_config = [('elite', 2), ('mutant', 2)]
            elif stage_num <= 20:
                enemy_config = [('elite', 3)]
            elif stage_num <= 23:
                enemy_config = [('elite', 2), ('mutant', 2)]
            elif stage_num <= 25:
                enemy_config = [('elite', 3), ('mutant', 1)]
            elif stage_num <= 28:
                enemy_config = [('elite', 3), ('mutant', 2)]
            else:
                enemy_config = [('elite', 4)]

            if stage_num % 5 == 0:
                if stage_num >= 25:
                    enemy_config.append(('overlord', 1))
                else:
                    enemy_config.append(('boss', 1))

        elif stage_num <= 32:
            enemy_config = [('scout', 2), ('flame_guard', 1)]
        elif stage_num <= 34:
            enemy_config = [('flame_guard', 1), ('frost_mage', 1), ('scout', 1)]
        elif stage_num <= 36:
            enemy_config = [('venom_stalker', 2), ('thunder_bringer', 1)]
        elif stage_num <= 38:
            enemy_config = [('void_walker', 1), ('phantom_assassin', 1), ('venom_stalker', 1)]
        elif stage_num <= 40:
            enemy_config = [('healer', 1), ('purifier', 1), ('venom_stalker', 1)]
        elif stage_num <= 42:
            enemy_config = [('mad_scientist', 1), ('suicide_bomber', 2), ('flame_guard', 1)]
        elif stage_num <= 44:
            enemy_config = [('annihilator', 1), ('paralyze_spider', 2), ('sleep_emissary', 1)]
        elif stage_num <= 46:
            enemy_config = [('energy_vampire', 2), ('purifier', 1), ('commander', 1)]
        elif stage_num <= 48:
            enemy_config = [('annihilator', 1), ('vengeful_wraith', 1), ('star_observer', 1)]
        elif stage_num <= 50:
            enemy_config = [('gene_fusion', 2), ('crystal_guardian', 1), ('healer', 1)]
        elif stage_num <= 52:
            enemy_config = [('chaos_source', 1), ('phantom_assassin', 1), ('sleep_emissary', 1)]
        elif stage_num <= 54:
            enemy_config = [('crystal_guardian', 2), ('iron_fortress', 1), ('guardian_spirit', 1)]
        elif stage_num <= 56:
            enemy_config = [('gene_fusion', 2), ('chaos_source', 1), ('corruption_source', 1)]
        elif stage_num <= 58:
            enemy_config = [('gene_fusion', 2), ('war_drummer', 1), ('mad_scientist', 1), ('healer', 1)]
        elif stage_num == 59:
            enemy_config = [('devourer', 2), ('gene_fusion', 2), ('commander', 1)]
        elif stage_num == 60:
            enemy_config = [('devourer', 2), ('gene_fusion', 2), ('guardian_spirit', 1), ('chaos_source', 1)]

        # ============ Stages 61-100 with new enemies ============
        elif stage_num <= 62:
            enemy_config = [('mutant_spider', 2), ('ghost_assassin', 1)]
        elif stage_num <= 64:
            enemy_config = [('frost_giant', 1), ('shadow_mage', 1), ('commander', 1)]
        elif stage_num <= 66:
            enemy_config = [('lava_lord', 1), ('crystal_guard', 1), ('war_drummer', 1)]
        elif stage_num <= 68:
            enemy_config = [('nano_swarm', 2), ('gene_reaper', 1), ('vengeful_wraith', 1)]
        elif stage_num <= 70:
            enemy_config = [('emp_wraith', 1), ('poison_cloud', 1), ('corruption_source', 1)]
        elif stage_num <= 72:
            enemy_config = [('iron_colossus', 1), ('guardian_spirit', 1), ('star_spirit', 1)]
        elif stage_num <= 74:
            enemy_config = [('bone_dragon', 1), ('dark_angel', 1), ('vengeful_wraith', 1)]
        elif stage_num <= 76:
            enemy_config = [('eternal_guardian', 1), ('commander', 1), ('gene_reaper', 1)]
        elif stage_num <= 78:
            enemy_config = [('shadow_mage', 2), ('war_drummer', 1), ('time_weaver', 1)]
        elif stage_num <= 80:
            enemy_config = [('lava_lord', 2), ('crystal_guard', 2), ('guardian_spirit', 1)]
        elif stage_num <= 82:
            enemy_config = [('gene_reaper', 2), ('emp_wraith', 1), ('corruption_source', 1)]
        elif stage_num <= 84:
            enemy_config = [('iron_colossus', 1), ('bone_dragon', 1), ('commander', 1)]
        elif stage_num <= 86:
            enemy_config = [('dark_angel', 2), ('doomsday_bringer', 2), ('vengeful_wraith', 1)]
        elif stage_num <= 88:
            enemy_config = [('mutant_spider', 2), ('ghost_assassin', 2), ('war_drummer', 1)]
        elif stage_num <= 90:
            enemy_config = [('mech_god', 1), ('guardian_spirit', 1), ('commander', 1)]
        elif stage_num <= 92:
            enemy_config = [('void_destroyer', 1), ('bone_dragon', 1), ('corruption_source', 1)]
        elif stage_num <= 94:
            enemy_config = [('mech_god', 1), ('abyss_lord', 1), ('rock', 1)]
        elif stage_num <= 96:
            enemy_config = [('void_destroyer', 1), ('war_drummer', 1), ('rock', 1)]
        elif stage_num <= 98:
            enemy_config = [('mech_god', 2), ('bone_dragon', 2), ('guardian_spirit', 1)]
        elif stage_num == 99:
            enemy_config = [('void_destroyer', 2), ('mech_god', 1), ('rock', 1)]
        else:
            enemy_config = [('void_destroyer', 3), ('mech_god', 2), ('rock', 1)]

        # Boss stages every 5 for stages 31-100
        if stage_num >= 31 and stage_num % 5 == 0:
            if stage_num >= 95:
                enemy_config.append(('void_destroyer', 1))
            elif stage_num >= 85:
                enemy_config.append(('mech_god', 1))
            elif stage_num >= 75:
                enemy_config.append(('abyss_lord', 1))
            elif stage_num >= 65:
                enemy_config.append(('bone_dragon', 1))
            elif stage_num >= 55:
                enemy_config.append(('void_overlord', 1))
            else:
                enemy_config.append(('devourer', 1))
            if stage_num == 40:
                enemy_config.append(('commander', 1))
            elif stage_num == 50:
                enemy_config.append(('guardian_spirit', 1))
            elif stage_num == 60:
                enemy_config.append(('war_drummer', 1))
            elif stage_num == 70:
                enemy_config.append(('corruption_source', 1))
            elif stage_num == 80:
                enemy_config.append(('vengeful_wraith', 1))
            elif stage_num == 90:
                enemy_config.append(('commander', 1))
                enemy_config.append(('guardian_spirit', 1))

        enemies = []
        enemy_types_in_stage = set()
        reward_exp = 10 + stage_num * 8

        # First pass: build enemy list, track types
        for etype, count in enemy_config:
            template = ENEMY_TEMPLATES[etype]
            effective_count = count + (extra_count if etype not in SPECIAL_SKIP_EXTRA else 0)
            for _ in range(effective_count):
                skills = _pick_skills(template, stage_num)
                boss_mult = BOSS_STAT_MULTIPLIERS.get(etype, 1.0)
                enemy = {
                    '_etype': etype,
                    'name': template['name'],
                    'health': int(template['base_health'] * health_scale * boss_mult),
                    'attack': int(template['base_attack'] * stat_scale * boss_mult),
                    'defense': int(template['base_defense'] * stat_scale * boss_mult),
                    'speed': int(template['base_speed'] * stat_scale * boss_mult),
                    'skills': skills,
                    'reward_exp': reward_exp,
                    'purify_interval': template.get('purify_interval', 0),
                    'annihilate': template.get('annihilate', False),
                    'immune_to_debuffs': template.get('immune_to_debuffs', False),
                    'passive_abilities': template.get('passive_abilities', []),
                    'trigger_all_skills': template.get('trigger_all_skills', False),
                }
                if etype in ('overlord', 'void_overlord', 'abyss_lord'):
                    enemy['is_overlord'] = True
                    enemy['width'] = 2
                    enemy['height'] = 2
                    enemy['position'] = 0
                elif etype == 'devourer':
                    enemy['is_overlord'] = True
                    enemy['width'] = 2
                    enemy['height'] = 2
                    enemy['position'] = 0
                elif etype in ('shadow_sentinel', 'iron_bulwark', 'ancient_serpent', 'war_behemoth', 'void_dragon_god'):
                    enemy['width'] = template.get('width', 1)
                    enemy['height'] = template.get('height', 1)
                    enemy['position'] = 0
                elif etype == 'rock':
                    enemy['position'] = 0
                enemies.append(enemy)
                enemy_types_in_stage.add(etype)

        # Second pass: apply synergies
        _apply_synergies(enemies, enemy_types_in_stage)

        # Remove internal _etype key from final output
        for e in enemies:
            e.pop('_etype', None)

        reward = {'unlock_stage': stage_num + 1}
        if stage_num % 5 == 0:
            reward['extra_exp'] = 100 + stage_num * 10
            reward['gene_fragment'] = True
        if stage_num > 30:
            existing_exp = reward.get('extra_exp', 0) or 0
            reward['extra_exp'] = existing_exp + 200
        if stage_num > 60:
            existing_exp = reward.get('extra_exp', 0) or 0
            reward['extra_exp'] = existing_exp + 500

        stage = {
            'name': f'第{stage_num}关 - {STAGE_TITLES[stage_num-1]}',
            'description': f'击败关卡中的所有敌人',
            'unlock_requirement': (stage_num - 1, 'complete') if stage_num > 1 else None,
            'enemies': enemies,
            'reward': reward,
        }
        if stage_num >= 40 and stage_num % 10 == 0:
            stage['enemy_grid_size'] = 4
        stages[stage_num] = stage

    return stages

STAGES = _generate_stages()

def _generate_map_stages():
    all_map_stages = {}
    for map_id, map_info in MAPS.items():
        start = map_info['start_stage']
        pool = map_info['enemy_pool']
        boss_interval = map_info.get('boss_interval', 5)
        titles = MAP_STAGE_TITLES.get(map_id, [])
        map_index = list(MAPS.keys()).index(map_id)
        map_bonus = 1.0 + map_index * 0.15

        extra_count = 1 + map_index

        for i in range(map_info['stages']):
            stage_num = start + i
            n = stage_num - 100
            hp_scale = 1 + n * 0.15 + n * n * 0.002
            stat_scale = 1 + n * 0.12 + n * n * 0.0015

            enemy_config = []
            if (i + 1) % boss_interval == 0:
                boss_key = pool[-1]
                enemy_config.append((boss_key, 1))
                non_boss = [e for e in pool if e != boss_key]
                if i == 19:
                    enemy_config = [(boss_key, 1), (pool[0], 1), (pool[2], 1)]
                elif i == 14:
                    enemy_config.append((pool[0], 1))
                    enemy_config.append((pool[1], 1))
                elif non_boss:
                    extra = extra_count if boss_key not in SPECIAL_SKIP_EXTRA else 0
                    for _ in range(extra):
                        enemy_config.append((non_boss[i % len(non_boss)], 1))
            else:
                idx = i % (len(pool) - 1)
                base_count = 1 + (i // (len(pool) - 1)) % 2
                etype = pool[idx]
                ecount = base_count + (extra_count if etype not in SPECIAL_SKIP_EXTRA else 0)
                enemy_config.append((etype, ecount))

            enemies = []
            enemy_types_in_stage = set()
            reward_exp = 100 + stage_num * 10

            for etype, count in enemy_config:
                template = ENEMY_TEMPLATES[etype]
                for _ in range(count):
                    skills = _pick_skills(template, stage_num)
                    boss_mult = BOSS_STAT_MULTIPLIERS.get(etype, 1.0)
                    enemy = {
                        '_etype': etype,
                        'name': template['name'],
                        'health': int(template['base_health'] * hp_scale * map_bonus * boss_mult),
                        'attack': int(template['base_attack'] * stat_scale * map_bonus * boss_mult),
                        'defense': int(template['base_defense'] * stat_scale * map_bonus * boss_mult),
                        'speed': int(template['base_speed'] * stat_scale * map_bonus * boss_mult),
                        'skills': skills,
                        'reward_exp': reward_exp,
                        'purify_interval': template.get('purify_interval', 0),
                        'annihilate': template.get('annihilate', False),
                        'immune_to_debuffs': template.get('immune_to_debuffs', False),
                        'passive_abilities': template.get('passive_abilities', []),
                        'trigger_all_skills': template.get('trigger_all_skills', False),
                        'width': template.get('width', 1),
                        'height': template.get('height', 1),
                    }
                    enemies.append(enemy)
                    enemy_types_in_stage.add(etype)

            _apply_synergies(enemies, enemy_types_in_stage)
            for e in enemies:
                e.pop('_etype', None)

            title = titles[i] if i < len(titles) else f'第{stage_num}层'
            stage = {
                'name': f'第{stage_num}层 - {title}',
                'description': f'{map_info["name"]} - {map_info["description"]}',
                'unlock_requirement': (stage_num - 1, 'complete') if i > 0 else None,
                'enemies': enemies,
                'map_id': map_id,
                'reward': {
                    'unlock_stage': stage_num + 1,
                    'extra_exp': 200 + stage_num * 15,
                    'gene_fragment': (i + 1) % boss_interval == 0,
                },
            }
            all_map_stages[stage_num] = stage

    return all_map_stages

MAP_STAGES = _generate_map_stages()

INFINITY_MODE = {
    'base_enemy_scale': 1.0,
    'scale_per_stage': 0.15,
    'max_stages': 200,
    'enemy_pool': [
        {'name': '侦查眼', 'base_health': 50, 'base_attack': 8, 'base_defense': 2, 'base_speed': 18},
        {'name': '烈焰守卫', 'base_health': 90, 'base_attack': 22, 'base_defense': 6, 'base_speed': 10},
        {'name': '冰霜术士', 'base_health': 80, 'base_attack': 12, 'base_defense': 14, 'base_speed': 8},
        {'name': '毒液潜伏者', 'base_health': 70, 'base_attack': 14, 'base_defense': 5, 'base_speed': 16},
        {'name': '雷暴使者', 'base_health': 95, 'base_attack': 26, 'base_defense': 7, 'base_speed': 14},
        {'name': '虚空行者', 'base_health': 75, 'base_attack': 16, 'base_defense': 8, 'base_speed': 20},
        {'name': '幻影刺客', 'base_health': 60, 'base_attack': 24, 'base_defense': 4, 'base_speed': 22},
        {'name': '治疗先驱', 'base_health': 100, 'base_attack': 8, 'base_defense': 10, 'base_speed': 12},
        {'name': '铁甲堡垒', 'base_health': 200, 'base_attack': 10, 'base_defense': 22, 'base_speed': 4},
        {'name': '疯狂科学家', 'base_health': 85, 'base_attack': 18, 'base_defense': 6, 'base_speed': 13},
        {'name': '自爆工兵', 'base_health': 50, 'base_attack': 6, 'base_defense': 2, 'base_speed': 15},
        {'name': '睡眠使者', 'base_health': 80, 'base_attack': 10, 'base_defense': 8, 'base_speed': 12},
        {'name': '麻痹毒蛛', 'base_health': 90, 'base_attack': 16, 'base_defense': 10, 'base_speed': 14},
        {'name': '能量吸血鬼', 'base_health': 100, 'base_attack': 20, 'base_defense': 8, 'base_speed': 16},
        {'name': '召唤大师', 'base_health': 110, 'base_attack': 14, 'base_defense': 10, 'base_speed': 10},
        {'name': '星辰观测者', 'base_health': 90, 'base_attack': 18, 'base_defense': 8, 'base_speed': 16},
        {'name': '基因融合体', 'base_health': 150, 'base_attack': 25, 'base_defense': 14, 'base_speed': 18},
        {'name': '水晶守卫', 'base_health': 160, 'base_attack': 12, 'base_defense': 18, 'base_speed': 8},
        {'name': '混沌之源', 'base_health': 120, 'base_attack': 20, 'base_defense': 10, 'base_speed': 15},
        {'name': '吞噬者', 'base_health': 350, 'base_attack': 40, 'base_defense': 20, 'base_speed': 22},
        {'name': '净化器', 'base_health': 120, 'base_attack': 6, 'base_defense': 10, 'base_speed': 6},
        {'name': '湮灭体', 'base_health': 80, 'base_attack': 10, 'base_defense': 3, 'base_speed': 10},
        {'name': '变异狼蛛', 'base_health': 110, 'base_attack': 22, 'base_defense': 10, 'base_speed': 16},
        {'name': '幽灵刺客', 'base_health': 75, 'base_attack': 30, 'base_defense': 5, 'base_speed': 24},
        {'name': '冰霜巨人', 'base_health': 250, 'base_attack': 24, 'base_defense': 22, 'base_speed': 6},
        {'name': '暗影法师', 'base_health': 100, 'base_attack': 26, 'base_defense': 8, 'base_speed': 14},
        {'name': '熔岩领主', 'base_health': 180, 'base_attack': 28, 'base_defense': 12, 'base_speed': 10},
        {'name': '晶壁守卫', 'base_health': 200, 'base_attack': 12, 'base_defense': 28, 'base_speed': 6},
        {'name': '等离子体', 'base_health': 120, 'base_attack': 32, 'base_defense': 6, 'base_speed': 18},
        {'name': '纳米虫群', 'base_health': 140, 'base_attack': 16, 'base_defense': 14, 'base_speed': 20},
        {'name': '基因收割者', 'base_health': 160, 'base_attack': 36, 'base_defense': 14, 'base_speed': 16},
        {'name': '电磁脉冲者', 'base_health': 100, 'base_attack': 18, 'base_defense': 10, 'base_speed': 22},
        {'name': '毒雾花', 'base_health': 90, 'base_attack': 14, 'base_defense': 8, 'base_speed': 12},
        {'name': '钢铁巨像', 'base_health': 350, 'base_attack': 20, 'base_defense': 32, 'base_speed': 4},
        {'name': '时间操纵者', 'base_health': 130, 'base_attack': 20, 'base_defense': 12, 'base_speed': 26},
        {'name': '星灵守护', 'base_health': 150, 'base_attack': 16, 'base_defense': 16, 'base_speed': 14},
        {'name': '暗黑天使', 'base_health': 140, 'base_attack': 40, 'base_defense': 10, 'base_speed': 20},
        {'name': '骨龙', 'base_health': 280, 'base_attack': 34, 'base_defense': 20, 'base_speed': 12},
        {'name': '末日使者', 'base_health': 100, 'base_attack': 20, 'base_defense': 6, 'base_speed': 18},
        {'name': '永恒守卫', 'base_health': 220, 'base_attack': 18, 'base_defense': 24, 'base_speed': 8},
        {'name': '指挥官', 'base_health': 130, 'base_attack': 14, 'base_defense': 12, 'base_speed': 10},
        {'name': '战鼓手', 'base_health': 100, 'base_attack': 8, 'base_defense': 8, 'base_speed': 14},
        {'name': '守护之灵', 'base_health': 180, 'base_attack': 6, 'base_defense': 20, 'base_speed': 6},
        {'name': '复仇之魂', 'base_health': 90, 'base_attack': 18, 'base_defense': 5, 'base_speed': 16},
        {'name': '腐蚀之源', 'base_health': 110, 'base_attack': 12, 'base_defense': 8, 'base_speed': 12},
        {'name': '巨石', 'base_health': 99999, 'base_attack': 0, 'base_defense': 50, 'base_speed': 0},
    ],
}

SKILL_EFFECTS = {
    '火焰吐息': {
        'type': 'damage',
        'base_damage': 25,
        'element': 'fire',
        'description': '喷出火焰造成伤害',
    },
    '雷击': {
        'type': 'damage',
        'base_damage': 30,
        'element': 'lightning',
        'description': '释放雷电造成高伤害',
    },
    '毒液攻击': {
        'type': 'damage_poison',
        'base_damage': 10,
        'turns': 5,
        'description': '喷射毒液造成持续伤害',
    },
    '自爆': {
        'type': 'self_damage',
        'base_damage': 50,
        'description': '自爆造成大量伤害，使用后自身也会受伤',
    },

    '冰霜护盾': {
        'type': 'shield',
        'shield_value': 40,
        'description': '获得冰霜护盾',
    },
    '能量护盾': {
        'type': 'shield',
        'shield_value': 25,
        'description': '获得能量护盾',
    },
    '隐身': {
        'type': 'invisible',
        'turns': 2,
        'description': '进入隐身状态，闪避率大幅提升',
    },

    '自我修复': {
        'type': 'heal',
        'heal_value': 30,
        'description': '恢复自身生命值',
    },

    '睡眠诱导': {
        'type': 'sleep',
        'turns': 2,
        'description': '使目标陷入睡眠',
    },
    '麻痹神经': {
        'type': 'paralyze',
        'turns': 2,
        'description': '使目标麻痹，无法行动',
    },
    '幻觉制造': {
        'type': 'confuse',
        'turns': 2,
        'description': '使目标产生幻觉',
    },

    '瞬移': {
        'type': 'evade',
        'turns': 1,
        'description': '瞬间闪避下次攻击',
    },
    '能量吸收': {
        'type': 'absorb',
        'damage': 15,
        'heal': 15,
        'description': '吸收敌人能量恢复自身',
    },
    '召唤': {
        'type': 'summon',
        'extra_damage': 20,
        'description': '召唤额外伤害',
    },
    '快速生长': {
        'type': 'buff',
        'buff_type': 'attack',
        'buff_value': 20,
        'turns': 3,
        'description': '提升攻击力',
    },
    '观星': {
        'type': 'rearrange',
        'description': '随机打乱对方阵型',
    },
    '澎湃': {
        'type': 'surge',
        'turns': 5,
        'description': '接下来5次行动必定为技能',
    },
    '甘霖': {
        'type': 'heal_team',
        'base_heal': 25,
        'targets': 3,
        'description': '恢复己方3名单位生命值',
    },

    # ==================== 新技能 (61-100关) ====================
    '冻结': {
        'type': 'freeze',
        'turns': 1,
        'description': '冻结目标，跳过下一次行动',
    },
    '诅咒': {
        'type': 'curse',
        'turns': 3,
        'damage_mult': 1.5,
        'description': '诅咒目标，受到的伤害提升50%',
    },
    '灼烧': {
        'type': 'burn',
        'turns': 3,
        'max_hp_pct': 0.15,
        'description': '灼烧目标，每回合损失15%最大生命值',
    },
    '处决': {
        'type': 'execute',
        'hp_threshold': 0.25,
        'base_damage': 60,
        'description': '处决低血量目标，若目标HP低于25%则直接秒杀',
    },
    '毒雾扩散': {
        'type': 'aoe_poison',
        'base_damage': 8,
        'turns': 4,
        'targets': 3,
        'description': '毒雾扩散，对最多3个目标施加中毒',
    },
    '时光倒流': {
        'type': 'rewind',
        'heal_pct': 0.5,
        'description': '时光倒流，恢复50%最大生命值',
    },
    '亡灵复苏': {
        'type': 'revive',
        'heal_pct': 0.3,
        'description': '亡灵复苏，死亡后以30%生命值复活一次',
    },

    # ==================== 抽卡限定技能 ====================
    '剧毒新星': {
        'type': 'toxic_nova',
        'base_damage': 15,
        'poison_stacks': 3,
        'turns': 5,
        'description': '对全体敌人造成伤害并叠加3层中毒，目标已有中毒时每层额外造成20%伤害',
    },
    '腐蚀之触': {
        'type': 'corrosive_touch',
        'base_damage': 35,
        'def_reduce': 0.50,
        'def_turns': 3,
        'poison_turns': 3,
        'description': '单体高伤，降低50%防御3回合并附加中毒，目标每个debuff额外+15%伤害',
    },
    '炼狱之火': {
        'type': 'inferno',
        'base_damage': 25,
        'burn_turns': 5,
        'description': '对全体敌人造成伤害并附加灼烧5回合，灼烧中目标受到伤害+30%',
    },
    '余烬复燃': {
        'type': 'ember_revival',
        'base_damage': 40,
        'bonus_pct': 0.20,
        'splash_pct': 0.50,
        'description': '单体伤害，击杀则溅射+传播灼烧；若目标带灼烧则额外造成20%最大生命伤害',
    },
    '永冻领域': {
        'type': 'permafrost',
        'base_damage': 20,
        'freeze_turns': 1,
        'frozen_dmg_mult': 1.5,
        'description': '全体伤害+冰冻1回合，被冰冻目标受此技能伤害+50%',
    },
    '绝对零度': {
        'type': 'absolute_zero',
        'base_damage': 55,
        'frozen_mult': 3.0,
        'freeze_turns': 2,
        'description': '单体巨量伤害，若目标被冰冻则3倍伤害并击碎冰冻',
    },
    '血之渴望': {
        'type': 'bloodthirst',
        'base_damage': 30,
        'bleed_pct': 0.10,
        'bleed_turns': 3,
        'description': '单体伤害附加流血3回合，流血期间击杀则回复50%伤害量的生命',
    },
    '猩红风暴': {
        'type': 'crimson_storm',
        'base_damage': 20,
        'bleed_turns': 2,
        'bleed_mult': 3.0,
        'description': '全体伤害，流血目标受3倍伤害并附加流血2回合',
    },
    '万象终结': {
        'type': 'omnibus_end',
        'base_damage': 18,
        'per_debuff_pct': 0.30,
        'description': '全体伤害，目标每有一种负面效果额外+30%伤害，消耗所有负面效果造成爆发',
    },
    '状态共鸣': {
        'type': 'status_resonance',
        'base_damage': 35,
        'per_type_atk': 0.10,
        'description': '单体伤害，统计全场debuff种类数每种+10%攻击力，转移自身一个随机debuff给目标',
    },

    # ==================== 多格单位技能 ====================
    '幽冥穿刺': {
        'type': 'column_strike',
        'base_damage': 30,
        'armor_pierce': 0.50,
        'description': '纵列攻击，50%护甲穿透',
    },
    '钢铁震击': {
        'type': 'row_strike',
        'base_damage': 25,
        'stun_turns': 1,
        'description': '横行攻击，附加眩晕1回合',
    },
    '剧毒吐息': {
        'type': 'poison_column',
        'base_damage': 15,
        'poison_turns': 3,
        'poison_stacks': 2,
        'description': '纵列攻击+中毒3回合',
    },
    '战吼': {
        'type': 'war_cry',
        'atk_bonus': 0.30,
        'turns': 3,
        'description': '全体友方攻击力提升30%持续3回合',
    },
    '虚空传送': {
        'type': 'void_teleport',
        'hp_pct': 0.15,
        'description': '传送扰乱所有玩家位置，造成15%最大生命伤害',
    },

    # ==================== 地图技能 ====================
    '腐蚀酸液': {
        'type': 'defense_reduce',
        'base_damage': 18,
        'def_reduce_pct': 0.15,
        'turns': 3,
        'description': '腐蚀攻击降低目标15%防御，持续3回合',
    },
    '污染净化': {
        'type': 'convert_debuff_damage',
        'base_damage': 12,
        'heal_per_debuff': 20,
        'description': '将目标的debuff转化为等量治疗，每个debuff额外造成12伤害',
    },
    '护卫铁壁': {
        'type': 'taunt_shield',
        'shield_value': 35,
        'turns': 2,
        'description': '嘲讽所有玩家强制攻击自己，并获得护盾',
    },
    '狂暴释放': {
        'type': 'berserk_burst',
        'atk_mult': 1.5,
        'base_damage': 30,
        'description': '牺牲20%当前生命，提升攻击力50%并造成额外伤害',
    },
    '石化之躯': {
        'type': 'petrify',
        'shield_pct': 0.30,
        'turns': 2,
        'description': '石化自身2回合，获得30%最大生命护盾，期间减伤50%',
    },
    '锁定狙击': {
        'type': 'lock_snipe',
        'base_damage': 35,
        'stack_pct': 0.20,
        'description': '锁定最低血量敌人造成伤害，连续使用同一目标伤害+20%',
    },
    '诅咒扩散': {
        'type': 'curse_aoe',
        'turns': 2,
        'description': '对全体玩家随机附加一种负面效果（中毒/麻痹/睡眠/诅咒）2回合',
    },
    '时间迟滞': {
        'type': 'slow_all',
        'bar_reduce': 20,
        'description': '降低全体玩家行动条20点',
    },
    '远古裁决': {
        'type': 'judgment',
        'base_damage': 20,
        'per_charge_dmg': 8,
        'description': '根据充能层数造成额外伤害，消耗所有充能',
    },
    '虚空牵引': {
        'type': 'void_pull',
        'base_damage': 15,
        'description': '将随机玩家单位拉至后排空位，造成伤害',
    },
    '背刺突袭': {
        'type': 'backstab',
        'base_damage': 28,
        'bonus_per_lost_hp': 0.5,
        'description': '瞬移至最虚弱玩家身后，每损失1%生命额外+0.5%伤害',
    },
    '混沌诅咒': {
        'type': 'chaos_curse',
        'turns': 3,
        'description': '让随机玩家获得随机debuff持续3回合',
    },
    '属性镜像': {
        'type': 'copy_stats',
        'turns': 2,
        'description': '复制最高攻击玩家的攻击力为己用，持续2回合',
    },
    '虚空风暴': {
        'type': 'void_storm',
        'base_damage': 20,
        'hp_pct': 0.08,
        'description': '对全体玩家造成伤害+8%最大生命伤害',
    },
    '连锁闪电': {
        'type': 'chain_lightning',
        'base_damage': 22,
        'bounces': 3,
        'paralyze_turns': 1,
        'falloff': 0.7,
        'description': '闪电弹射3个目标，伤害递减30%，麻痹命中的目标1回合',
    },
    '地裂波动': {
        'type': 'earthquake',
        'hp_pct': 0.12,
        'description': '地震波对全体玩家造成12%当前生命值的伤害',
    },
    '恐惧凝视': {
        'type': 'fear',
        'bar_rewind': 30,
        'turns': 1,
        'description': '恐惧目标，使其行动条倒退30点',
    },
    '梦魇侵袭': {
        'type': 'nightmare',
        'base_damage': 15,
        'sleep_hp_pct': 0.15,
        'description': '对睡眠中的目标造成15%最大生命伤害，否则造成基础伤害',
    },
    '绝望诅咒': {
        'type': 'heal_block_curse',
        'turns': 3,
        'description': '诅咒目标3回合，期间无法被治疗',
    },
    '钢铁壁垒': {
        'type': 'shield_self',
        'shield_value': 60,
        'description': '获得大量护盾',
    },

    # ==================== 废弃实验室 新增技能 ====================
    '酸液飞溅': {
        'type': 'aoe_damage',
        'base_damage': 18, 'targets': 3,
        'description': '喷射酸液溅射3个目标',
    },
    '基因突变': {
        'type': 'buff_team',
        'atk_bonus': 0.25, 'def_bonus': 0.25, 'turns': 3,
        'description': '全体友方攻防提升25%持续3回合',
    },
    '废料投掷': {
        'type': 'damage',
        'base_damage': 40,
        'description': '投掷剧毒废料造成高额伤害',
    },
    '消毒喷雾': {
        'type': 'heal_team',
        'base_heal': 35, 'targets': 3,
        'description': '喷洒消毒液恢复友方生命',
    },
    '机械充能': {
        'type': 'surge',
        'turns': 3,
        'description': '接下来3次行动必定为技能',
    },

    # ==================== 远古遗迹 新增技能 ====================
    '符文爆破': {
        'type': 'aoe_damage',
        'base_damage': 25,
        'description': '引爆符文力量对全体造成伤害',
    },
    '沙暴迷眼': {
        'type': 'confuse',
        'turns': 2, 'targets': 3,
        'description': '沙暴使最多3个目标混乱2回合',
    },
    '古代守护': {
        'type': 'shield_team',
        'shield_value': 30, 'targets': 3,
        'description': '为3名友方提供护盾',
    },
    '落石碾压': {
        'type': 'damage',
        'base_damage': 45,
        'description': '召唤巨石碾压单体目标',
    },
    '时间裂隙': {
        'type': 'slow_all',
        'bar_reduce': 35,
        'description': '大幅降低全体玩家行动条35点',
    },

    # ==================== 虚空裂隙 新增技能 ====================
    '虚空裂隙斩': {
        'type': 'damage',
        'base_damage': 42, 'armor_pierce': 0.30,
        'description': '撕裂空间造成高伤，无视30%防御',
    },
    '次元放逐': {
        'type': 'banish',
        'turns': 2,
        'description': '将目标放逐到异次元2回合，无法行动',
    },
    '空间扭曲': {
        'type': 'rearrange',
        'description': '随机打乱所有玩家位置',
    },
    '黑洞吞噬': {
        'type': 'void_storm',
        'base_damage': 30, 'hp_pct': 0.12,
        'description': '黑洞吸引全体造成伤害+12%最大生命',
    },
    '相位转移': {
        'type': 'evade',
        'turns': 1,
        'description': '进入相位空间闪避下次攻击',
    },

    # ==================== 元素位面 新增技能 ====================
    '元素爆炸': {
        'type': 'aoe_damage',
        'base_damage': 28,
        'description': '引爆周身元素之力对全体造成伤害',
    },
    '熔岩喷发': {
        'type': 'damage_burn',
        'base_damage': 35, 'burn_turns': 3, 'burn_pct': 0.10,
        'description': '熔岩喷射单体高伤并灼烧',
    },
    '暴风雪': {
        'type': 'aoe_freeze',
        'base_damage': 15, 'freeze_turns': 1,
        'description': '暴风雪全体伤害并冻结1回合',
    },
    '闪电风暴': {
        'type': 'aoe_paralyze',
        'base_damage': 20, 'paralyze_turns': 1,
        'description': '闪电风暴全体伤害并麻痹1回合',
    },
    '地核震动': {
        'type': 'earthquake',
        'hp_pct': 0.18,
        'description': '强烈地震造成18%当前生命伤害',
    },

    # ==================== 深渊之底 新增技能 ====================
    '深渊裂隙': {
        'type': 'void_storm',
        'base_damage': 25, 'hp_pct': 0.15,
        'description': '撕裂深渊造成全体伤害+15%最大生命',
    },
    '灵魂剥离': {
        'type': 'absorb',
        'damage': 30, 'heal': 30,
        'description': '剥离目标灵魂造成伤害并回复等量生命',
    },
    '暗影爆发': {
        'type': 'aoe_fear',
        'base_damage': 22, 'bar_rewind': 25,
        'description': '暗影冲击全体伤害并倒退行动条25点',
    },
    '绝望低语': {
        'type': 'curse_aoe',
        'turns': 3,
        'description': '低语诅咒全体3回合，随机附加debuff',
    },
    '混沌喷射': {
        'type': 'chaos_spray',
        'base_damage': 35,
        'description': '喷射混沌能量造成伤害并随机附加一种负面效果',
    },

    # ==================== 圣堂主题技能 ====================
    '圣疗': {
        'type': 'resurrect',
        'heal_pct': 0.5,
        'description': '以圣光之力复活一名阵亡的友军，恢复50%生命',
    },
    '血肉献祭': {
        'type': 'sacrifice_heal',
        'hp_pct': 0.3,
        'heal_pct': 0.5,
        'description': '献祭30%自身生命，恢复所有友军50%攻击力的生命',
    },
    '圣光惩戒': {
        'type': 'missing_hp_damage',
        'base_damage': 15,
        'missing_hp_ratio': 0.3,
        'description': '基于目标已损生命值造成额外伤害',
    },
    '净化之火': {
        'type': 'cleanse_damage',
        'base_damage': 18,
        'bonus_per_debuff': 8,
        'description': '净化自身所有负面效果，每个被净化的效果附加额外伤害',
    },
    '血之疫病': {
        'type': 'blood_plague',
        'base_damage': 12,
        'bleed_turns': 3,
        'poison_turns': 3,
        'description': '对所有敌人造成伤害并附加流血和中毒效果',
    },
}

BATTLE_CONFIG = {
    'team_size': 5,
    'max_team_size': 5,
    'grid_size': 3,
    'grid_size_advanced': 4,
    'max_team_size_advanced': 7,
    'action_bar_max': 100,
    'base_action_speed': 10,
    'critical_rate_base': 0.15,
    'critical_damage': 1.5,
    'dodge_rate_base': 0.10,
    'damage_formula': 'attack - defense',
    'min_damage': 1,
    'turn_timeout': 30,
    'auto_battle_speed': 0.5,
}

STATUS_EFFECTS = {
    'poison': {'name': '中毒', 'type': 'debuff', 'icon': '☠'},
    'sleep': {'name': '睡眠', 'type': 'debuff', 'icon': '💤'},
    'paralyze': {'name': '麻痹', 'type': 'debuff', 'icon': '⚡'},
    'confuse': {'name': '混乱', 'type': 'debuff', 'icon': '🌪'},
    'freeze': {'name': '冻结', 'type': 'debuff', 'icon': '❄'},
    'curse': {'name': '诅咒', 'type': 'debuff', 'icon': '🔮'},
    'burn': {'name': '灼烧', 'type': 'debuff', 'icon': '🔥'},
    'shield': {'name': '护盾', 'type': 'buff', 'icon': '🛡'},
    'invisible': {'name': '隐身', 'type': 'buff', 'icon': '👻'},
    'attack_buff': {'name': '攻击强化', 'type': 'buff', 'icon': '⚔'},
    'evade': {'name': '闪避', 'type': 'buff', 'icon': '💨'},
    'bleed': {'name': '流血', 'type': 'debuff', 'icon': '🩸'},
}

# ============================================================
# 敌方被动技能定义
# ============================================================
ENEMY_PASSIVES = {
    'attack_aura': {
        'name': '攻击灵气',
        'description': '提升全体友方攻击力',
        'params': {'bonus_pct': 0.20},
    },
    'defense_aura': {
        'name': '防御灵气',
        'description': '提升全体友方防御力',
        'params': {'bonus_pct': 0.30},
    },
    'speed_aura': {
        'name': '速度灵气',
        'description': '提升全体友方速度',
        'params': {'bonus_pct': 0.20},
    },
    'heal_aura': {
        'name': '治愈灵气',
        'description': '每回合恢复全体友方生命值',
        'params': {'heal_pct': 0.03},
    },
    'fortify': {
        'name': '钢铁意志',
        'description': '登场时提升全体友方最大生命值',
        'params': {'hp_bonus_pct': 0.25},
    },
    'rage': {
        'name': '怒火',
        'description': '死亡时提升全体友方攻击力',
        'params': {'atk_bonus_pct': 0.30, 'turns': 5},
    },
    'vengeance': {
        'name': '复仇',
        'description': '死亡时对全体敌方造成伤害',
        'params': {'dmg_pct': 0.50},
    },
    'bless': {
        'name': '净化祝福',
        'description': '每回合移除全体友方一个负面效果',
        'params': {'interval': 1},
    },
    'shield_aura': {
        'name': '护盾灵气',
        'description': '每回合为全体友方提供护盾',
        'params': {'shield_pct': 0.05},
    },
    'berserk': {
        'name': '狂怒',
        'description': '生命低于50%时攻击力翻倍',
        'params': {'hp_threshold': 0.50, 'atk_mult': 2.0},
    },
    'regeneration': {
        'name': '再生',
        'description': '每回合恢复自身生命值',
        'params': {'heal_pct': 0.08},
    },
    'toxic_aura': {
        'name': '毒瘴灵气',
        'description': '每回合对全体敌方造成中毒效果',
        'params': {'poison_dmg': 30, 'turns': 2},
    },
    'thorns_aura': {
        'name': '荆棘灵气',
        'description': '反弹受到的伤害',
        'params': {'reflect_pct': 0.25},
    },
    # === 新增：里程碑关卡 Boss 专属被动 ===
    'aoe_barrier': {
        'name': '群体屏障',
        'description': '受到AOE伤害减半',
        'params': {'aoe_reduction': 0.50},
    },
    'focus_weak': {
        'name': '弱点狙击',
        'description': '优先攻击血量最低的敌人',
        'params': {},
    },
    'enrage': {
        'name': '狂暴',
        'description': '生命低于30%时攻击力翻倍，速度提升50%',
        'params': {'hp_threshold': 0.30, 'atk_mult': 2.0, 'spd_mult': 1.5},
    },
    'debuff_cleanse': {
        'name': '净化之躯',
        'description': '每回合移除自身所有负面效果',
        'params': {},
    },

    # === 多格单位被动 ===
    'guard_protocol': {
        'name': '护卫协议',
        'description': '50%伤害转移至下方单位',
        'params': {'transfer_pct': 0.50},
    },
    'iron_wall': {
        'name': '钢铁之壁',
        'description': '相邻友方单位减伤25%',
        'params': {'dmg_reduction': 0.25},
    },
    'poison_mastery': {
        'name': '剧毒掌控',
        'description': '毒伤+100%，毒杀后扩散至相邻敌人',
        'params': {'poison_dmg_mult': 2.0},
    },
    'advance': {
        'name': '战争推进',
        'description': '每回合前进1列，对路径敌人造成20%攻击伤害',
        'params': {'advance_dmg_pct': 0.20},
    },
    'void_lord': {
        'name': '虚空领主',
        'description': '虚空族友方+30%攻击/-30%受伤，每回合对全体玩家造成5%最大生命伤害',
        'params': {'void_atk_bonus': 0.30, 'void_dmg_reduction': 0.30, 'player_hp_pct': 0.05},
    },

    # ==================== 地图被动 ====================
    'corrosive_aura': {
        'name': '腐蚀灵气',
        'description': '每回合降低全体玩家防御',
        'params': {'def_reduce_pct': 0.10},
    },
    'convert_debuff': {
        'name': '污染净化',
        'description': '每回合将一个debuff转化为等量治疗',
        'params': {'heal_pct': 0.05},
    },
    'death_zone': {
        'name': '死亡毒区',
        'description': '死亡后每回合对全体玩家造成伤害',
        'params': {'dmg_pct': 0.06, 'turns': 5},
    },
    'protect_ally': {
        'name': '护卫协议',
        'description': '自动为最低血量友方承受伤害',
        'params': {},
    },
    'stacking_damage': {
        'name': '狙击锁定',
        'description': '连续攻击同一目标伤害递增',
        'params': {'stack_pct': 0.20, 'max_stacks': 5},
    },
    'curse_spread': {
        'name': '诅咒扩散',
        'description': '每回合给全体玩家随机添加一种debuff',
        'params': {},
    },
    'time_drain': {
        'name': '时间偷取',
        'description': '每回合降低全体玩家行动条',
        'params': {'bar_drain': 8},
    },
    'tick_charge': {
        'name': '充能爆发',
        'description': '玩家每行动一次获得1层充能，10层释放全屏AOE',
        'params': {'max_charge': 10, 'aoe_damage_pct': 1.5},
    },
    'mirror_copy': {
        'name': '属性镜像',
        'description': '每回合复制最高攻击敌人的属性',
        'params': {},
    },
    'void_rift_lord': {
        'name': '虚空裂隙领主',
        'description': '每回合召唤虚空触须，触须存在时减伤50%',
        'params': {},
    },
    'fire_death': {
        'name': '火焰余烬',
        'description': '死亡时爆炸对全体玩家造成火伤',
        'params': {'dmg_pct': 0.20},
    },
    'ice_death': {
        'name': '冰川破碎',
        'description': '被击破时治疗全体友方',
        'params': {'heal_pct': 0.20},
    },
    'element_cycle': {
        'name': '元素轮换',
        'description': '每3回合轮换元素形态，对当前元素免疫',
        'params': {'cycle_turns': 3},
    },
    'fear_aura': {
        'name': '恐惧光环',
        'description': '每回合降低全体玩家行动条',
        'params': {'bar_drain': 5},
    },
    'heal_reduction': {
        'name': '绝望光环',
        'description': '降低所有玩家治疗效果',
        'params': {'heal_reduction_pct': 0.50},
    },
    'execute_mastery': {
        'name': '处决精通',
        'description': '生命低于50%时获得50%斩杀线',
        'params': {'execute_threshold': 0.50},
    },
    'form_shift_lab': {
        'name': '形态切换·实验室',
        'description': '每损失30%HP切换攻击/防御/平衡形态',
        'params': {},
    },
    'primordial_chaos': {
        'name': '原初混沌',
        'description': '拥有所有地图Boss的招牌被动，分3阶段',
        'params': {},
    },

    # ==================== 废弃实验室 新增被动 ====================
    'toxic_residue': {
        'name': '毒区残留',
        'description': '死亡后留下毒区，每回合格全体玩家造成伤害',
        'params': {'poison_dmg': 25, 'turns': 3},
    },
    'split_merge': {
        'name': '分裂再生',
        'description': '生命低于50%时分裂成2个小型单位',
        'params': {'split_hp_pct': 0.50, 'split_count': 2},
    },
    'death_explode': {
        'name': '殉爆',
        'description': '死亡时爆炸，对全体玩家造成30%最大生命伤害',
        'params': {'dmg_pct': 0.30},
    },
    'lab_overdrive': {
        'name': '过载模式',
        'description': '生命低于30%时攻击+50%，防御-30%',
        'params': {'atk_mult': 1.5, 'def_reduce': 0.3},
    },
    'acid_armor': {
        'name': '酸蚀装甲',
        'description': '攻击者受到15%反伤并被降低防御',
        'params': {'reflect_pct': 0.15},
    },

    # ==================== 远古遗迹 新增被动 ====================
    'rune_ward': {
        'name': '符文庇护',
        'description': '受到伤害减少20%',
        'params': {'dmg_reduction': 0.20},
    },
    'death_curse': {
        'name': '死亡诅咒',
        'description': '死亡时诅咒全体玩家3回合，受伤+30%',
        'params': {'curse_turns': 3},
    },
    'swarm_rally': {
        'name': '虫群集结',
        'description': '每存在一个友方单位攻击力+10%',
        'params': {'atk_per_ally': 0.10},
    },
    'gate_guard': {
        'name': '门扉守卫',
        'description': '每3回合召唤1个古代战士',
        'params': {'summon_interval': 3},
    },
    'sand_veil': {
        'name': '流沙帷幕',
        'description': '获得20%闪避率',
        'params': {'dodge_pct': 0.20},
    },

    # ==================== 虚空裂隙 新增被动 ====================
    'shadow_meld': {
        'name': '暗影融合',
        'description': '生命低于30%时自动进入隐身',
        'params': {'invisible_hp': 0.30},
    },
    'void_radiance': {
        'name': '虚空辐射',
        'description': '每回合对全体玩家造成5%最大生命伤害',
        'params': {'dmg_pct': 0.05},
    },
    'entropic_aura': {
        'name': '熵增光环',
        'description': '每回合30%概率给随机玩家添加debuff',
        'params': {'debuff_chance': 0.30},
    },
    'mirage_clone': {
        'name': '幻影分身',
        'description': '受击时产生一个30%血量的幻影分身',
        'params': {'clone_count': 1, 'clone_hp': 0.30},
    },
    'void_growth': {
        'name': '虚空成长',
        'description': '每回合提升5%全属性',
        'params': {'growth_per_turn': 0.05},
    },

    # ==================== 元素位面 新增被动 ====================
    'overheat': {
        'name': '过热爆发',
        'description': '每回合灼烧伤害+5%，上限叠加10层',
        'params': {'burn_stack_pct': 0.05, 'max_stacks': 10},
    },
    'frost_armor': {
        'name': '冰霜铠甲',
        'description': '被近战攻击时50%冻结攻击者',
        'params': {'freeze_chance': 0.50},
    },
    'elemental_siphon': {
        'name': '元素虹吸',
        'description': '使用元素技能时恢复10%伤害量生命',
        'params': {'heal_on_hit': 0.10},
    },
    'reactive_armor': {
        'name': '反伤甲壳',
        'description': '反弹30%受到的伤害',
        'params': {'reflect_pct': 0.30},
    },
    'static_field': {
        'name': '静电场',
        'description': '每回合25%概率对随机玩家造成雷击',
        'params': {'lightning_pct': 0.25},
    },

    # ==================== 深渊之底 新增被动 ====================
    'shadow_clone': {
        'name': '暗影分身',
        'description': '每次攻击后留下40%属性的暗影分身',
        'params': {'clone_pct': 0.40},
    },
    'soul_eater': {
        'name': '噬魂者',
        'description': '击杀目标永久+3%攻击和+2%生命',
        'params': {'perm_atk_gain': 0.03, 'perm_hp_gain': 0.02},
    },
    'abyss_resistance': {
        'name': '深渊抗性',
        'description': '深渊生物减少15%所有伤害',
        'params': {'dmg_reduction': 0.15},
    },
    'nightmare_fuel': {
        'name': '噩梦燃料',
        'description': '目标每有一种debuff攻击+8%',
        'params': {'atk_per_debuff': 0.08},
    },
    'chaos_instability': {
        'name': '混沌不稳',
        'description': '死亡时触发随机效果（爆炸/治疗/召唤/诅咒）',
        'params': {},
    },
}

# Merge map stages into STAGES
for _map_stage_num, _map_stage_data in MAP_STAGES.items():
    STAGES[_map_stage_num] = _map_stage_data

# ============================================================
# 里程碑关卡难度尖刺 — 在生成 + JSON 覆盖之后统一应用
# ============================================================
MILESTONE_BONUS = {
    20: 1.15, 30: 1.30, 40: 1.20, 50: 1.40,
    60: 1.25, 70: 1.50, 80: 1.30, 90: 1.60, 100: 2.0,
}

MILESTONE_BOSS_PASSIVES = {
    20: 'aoe_barrier',
    30: 'debuff_cleanse',
    40: 'enrage',
    50: 'focus_weak',
    60: 'aoe_barrier',
    70: 'debuff_cleanse',
    80: 'enrage',
    90: 'focus_weak',
    100: 'aoe_barrier',
}

for _sn, _bonus in MILESTONE_BONUS.items():
    if _sn in STAGES:
        for _e in STAGES[_sn].get('enemies', []):
            _e['health'] = int(_e['health'] * _bonus)
            _e['attack'] = int(_e['attack'] * _bonus)
        # Assign boss passives: give to the strongest enemy on the stage
        _boss_passive = MILESTONE_BOSS_PASSIVES.get(_sn)
        if _boss_passive:
            _sorted = sorted(STAGES[_sn]['enemies'], key=lambda x: x.get('health', 0) * x.get('attack', 0), reverse=True)
            if _sorted:
                _boss = _sorted[0]
                _existing = _boss.get('passive_abilities', [])
                if _boss_passive not in _existing:
                    _boss['passive_abilities'] = _existing + [_boss_passive]
