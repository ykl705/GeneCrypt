import random
import time
import json
import os
from datetime import datetime

# ==========================================    
# 导入配置模块
# ==========================================
from gene_config import (
    GENE_TEMPLATES, SKILL_TRAITS, GENE_CATEGORIES,
    CHROMOSOME_LAYOUT, CHROMOSOME_IDS, GENE_REGIONS,
    CHROMOSOME_LENGTH, VITAL_GENES, SKILL_GENES, TRAIT_GENES,
    PASSIVE_GENES, THORNS_B_SEQUENCE, ASSASSIN_B_SEQUENCE, REFLEX_B_SEQUENCE
)
from gene_enhance_config import STAT_ENHANCE_REGIONS
from trait_config import (
    TRAIT_CONFIG, INHERIT_CONFIG, METHYLATION_EFFECT,
    RECESSIVE_EXPRESS_CONDITION, RADIATION_CONFIG,
    RESEARCH_CONFIG, CUTTING_CONFIG, HYBRID_VIGOR_CONFIG
)
from tech_config import TECH_TREE, TREE_BRANCHES, BREEDING_CONFIG, INITIAL_CARDS_CONFIG
from battle_config import (
    STAGES, INFINITY_MODE, SKILL_EFFECTS, BATTLE_CONFIG, STATUS_EFFECTS, ENEMY_TEMPLATES,
    MAPS, ENEMY_PASSIVES, BOSS_STAT_MULTIPLIERS,
)

BASES = ['A', 'T', 'G', 'C']
COMPLEMENT = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}



# ==========================================
# 任务系统定义
# ==========================================
QUEST_DEFINITIONS = [
    # ==================== 主线 (40) ====================
    {'id':'m_01','requires':[],'category':'main','type':'clear_stage','target_stage':3,'target':1,'title':'基因觉醒','description':'实验室的应急灯闪烁着红光。培养皿中，一段沉睡万年的基因序列正在苏醒。研究员们屏住呼吸——这是人类第一次唤醒远古基因。通关第3关','story':'你站在GeneCrypt实验室的核心控制台前，全息屏幕上显示着一个从未见过的基因序列。博士，这个序列在自行重组！助手的声音充满惊恐。培养液中的细胞开始分裂——一个全新的生命体正在诞生。你伸手触碰屏幕，一道光芒闪过，意识与实验体的神经链接建立了...','rewards':[{'type':'gacha_currency','amount':50}]},
    {'id':'m_02','requires':['m_01'],'category':'main','type':'kill_any','target':5,'title':'初次狩猎','description':'新生的基因体需要通过实战来验证其能力。累计击杀5个敌人','story':'苏醒的实验体在你的意识引导下，第一次踏入模拟战场。它的感官是你的延伸——你能感受到空气中基因碎片的气味。这是狩猎的本能，你低语道，去战斗，去进化。','rewards':[{'type':'battle_materials','amount':30}]},
    {'id':'m_03','requires':['m_02'],'category':'main','type':'clear_stage','target_stage':7,'target':1,'title':'深入丛林','description':'战场模拟切换到了热带雨林环境。新的敌人隐藏在茂密的植被中。通关第7关','story':'模拟器加载了丛林场景。潮湿的空气、腐烂的落叶——一切都如此真实。远处，一个黑影闪过。有东西在跟踪我们。你拉近神经链接，实验体的视觉系统立刻捕捉到了三个敌对目标。它们不是自然进化的产物——而是竞争对手实验室的失败品，被遗弃在这里。','rewards':[{'type':'gacha_currency','amount':50},{'type':'card_with_skills','skill_names':['冻结'],'genome_quality':0.3}]},
    {'id':'m_04','requires':['m_03'],'category':'main','type':'clear_stage','target_stage':11,'target':1,'title':'黑暗边缘','description':'通关第11关','rewards':[{'type':'gacha_currency','amount':60}]},
    {'id':'m_05','requires':['m_04'],'category':'main','type':'breed_count','target':3,'title':'生命传承','description':'累计繁殖3次','rewards':[{'type':'gacha_currency','amount':80},{'type':'card_with_skills','skill_names':['甘霖'],'genome_quality':0.35}]},
    {'id':'m_06','requires':['m_05'],'category':'main','type':'clear_stage','target_stage':15,'target':1,'title':'逆境求生','description':'通关第15关','rewards':[{'type':'battle_materials','amount':100}]},
    {'id':'m_07','requires':['m_06'],'category':'main','type':'have_cards','target':5,'title':'伙伴集结','description':'拥有5张卡牌','rewards':[{'type':'gacha_currency','amount':90},{'type':'card_with_skills','skill_names':['快速生长'],'genome_quality':0.38}]},
    {'id':'m_08','requires':['m_07'],'category':'main','type':'clear_stage','target_stage':19,'target':1,'title':'暴风前夕','description':'通关第19关','rewards':[{'type':'gacha_currency','amount':100},{'type':'card_with_skills','skill_names':['能量护盾','火焰吐息'],'genome_quality':0.4}]},
    {'id':'m_09','requires':['m_08'],'category':'main','type':'no_loss_clear','target_stage':10,'target':1,'title':'完美开局','description':'无阵亡通关第10关','rewards':[{'type':'battle_materials','amount':120}]},
    {'id':'m_10','requires':['m_09'],'category':'main','type':'clear_stage','target_stage':23,'target':1,'title':'战力凝聚','description':'通关第23关','rewards':[{'type':'gacha_currency','amount':130},{'type':'card_with_skills','skill_names':['甘霖','冻结'],'genome_quality':0.42}]},
    {'id':'m_11','requires':['m_10'],'category':'main','type':'kill_any','target':25,'title':'屠戮之路','description':'累计击杀25个敌人','rewards':[{'type':'battle_materials','amount':150}]},
    {'id':'m_12','requires':['m_11'],'category':'main','type':'clear_stage','target_stage':28,'target':1,'title':'铁血意志','description':'通关第28关','rewards':[{'type':'gacha_currency','amount':170},{'type':'card_with_skills','skill_names':['冰霜护盾','快速生长'],'genome_quality':0.45}]},
    {'id':'m_13','requires':['m_12'],'category':'main','type':'clear_stage','target_stage':33,'target':1,'title':'基因强化','description':'通关第33关','rewards':[{'type':'battle_materials','amount':200}]},
    {'id':'m_14','requires':['m_13'],'category':'main','type':'tech_level','target':3,'title':'科技之光','description':'任意科技达到3级','rewards':[{'type':'gacha_currency','amount':200},{'type':'card_with_skills','skill_names':['火焰吐息'],'genome_quality':0.48}]},
    {'id':'m_15','requires':['m_14'],'category':'main','type':'clear_stage','target_stage':38,'target':1,'title':'冰火初融','description':'通关第38关','rewards':[{'type':'battle_materials','amount':220}]},
    {'id':'m_16','requires':['m_15'],'category':'main','type':'clear_stage','target_stage':43,'target':1,'title':'战神觉醒','description':'通关第43关','rewards':[{'type':'gacha_currency','amount':250},{'type':'card_with_skills','skill_names':['诅咒','血之渴望'],'genome_quality':0.5}]},
    {'id':'m_17','requires':['m_16'],'category':'main','type':'kill_boss','target':3,'title':'猎王行动','description':'累计击杀3个BOSS','rewards':[{'type':'battle_materials','amount':280}]},
    {'id':'m_18','requires':['m_17'],'category':'main','type':'clear_stage','target_stage':48,'target':1,'title':'深渊低语','description':'通关第48关','rewards':[{'type':'gacha_currency','amount':300},{'type':'card_with_skills','skill_names':['冰霜护盾'],'genome_quality':0.52}]},
    {'id':'m_19','requires':['m_18'],'category':'main','type':'no_loss_clear','target_stage':25,'target':1,'title':'完美作战','description':'无阵亡通关第25关','rewards':[{'type':'battle_materials','amount':350},{'type':'card_with_skills','skill_names':['自我修复','状态共鸣'],'genome_quality':0.55}]},
    {'id':'m_20','requires':['m_19'],'category':'main','type':'clear_stage','target_stage':53,'target':1,'title':'嗜血之路','description':'通关第53关','rewards':[{'type':'gacha_currency','amount':380}]},
    {'id':'m_21','requires':['m_20'],'category':'main','type':'clear_stage','target_stage':58,'target':1,'title':'极限挑战','description':'通关第58关','rewards':[{'type':'battle_materials','amount':420}]},
    {'id':'m_22','requires':['m_21'],'category':'main','type':'have_cards','target':12,'title':'卡牌大师','description':'拥有12张卡牌','rewards':[{'type':'gacha_currency','amount':450},{'type':'card_with_skills','skill_names':['诅咒'],'genome_quality':0.57}]},
    {'id':'m_23','requires':['m_22'],'category':'main','type':'clear_stage','target_stage':63,'target':1,'title':'冰封王座','description':'通关第63关','rewards':[{'type':'battle_materials','amount':500}]},
    {'id':'m_24','requires':['m_23'],'category':'main','type':'clear_stage','target_stage':68,'target':1,'title':'深渊探索','description':'通关第68关','rewards':[{'type':'gacha_currency','amount':550},{'type':'card_with_skills','skill_names':['猩红风暴','永冻领域'],'genome_quality':0.6}]},
    {'id':'m_25','requires':['m_24'],'category':'main','type':'kill_any','target':150,'title':'百人斩','description':'累计击杀150个敌人','rewards':[{'type':'battle_materials','amount':600}]},
    {'id':'m_26','requires':['m_25'],'category':'main','type':'clear_stage','target_stage':73,'target':1,'title':'元素觉醒','description':'通关第73关','rewards':[{'type':'gacha_currency','amount':650},{'type':'card_with_skills','skill_names':['自我修复'],'genome_quality':0.63}]},
    {'id':'m_27','requires':['m_26'],'category':'main','type':'clear_stage','target_stage':78,'target':1,'title':'战神降临','description':'通关第78关','rewards':[{'type':'battle_materials','amount':700},{'type':'card_with_skills','skill_names':['炼狱之火','能量护盾'],'genome_quality':0.65}]},
    {'id':'m_28','requires':['m_27'],'category':'main','type':'total_tech_levels','target':10,'title':'科技洪流','description':'科技总等级达到10级','rewards':[{'type':'gacha_currency','amount':750}]},
    {'id':'m_29','requires':['m_28'],'category':'main','type':'clear_stage','target_stage':84,'target':1,'title':'冰霜领域','description':'通关第84关','rewards':[{'type':'battle_materials','amount':800}]},
    {'id':'m_30','requires':['m_29'],'category':'main','type':'no_loss_clear','target_stage':45,'target':1,'title':'无伤传说','description':'无阵亡通关第45关','rewards':[{'type':'gacha_currency','amount':850}]},
    {'id':'m_31','requires':['m_30'],'category':'main','type':'clear_stage','target_stage':90,'target':1,'title':'炼狱之路','description':'通关第90关','rewards':[{'type':'battle_materials','amount':900},{'type':'card_with_skills','skill_names':['永冻领域','剧毒新星'],'genome_quality':0.7}]},
    {'id':'m_32','requires':['m_31'],'category':'main','type':'clear_stage','target_stage':97,'target':1,'title':'半百之王','description':'通关第97关','rewards':[{'type':'gacha_currency','amount':1000}]},
    {'id':'m_33','requires':['m_32'],'category':'main','type':'kill_boss','target':15,'title':'首领克星','description':'累计击杀15个BOSS','rewards':[{'type':'battle_materials','amount':1100}]},
    {'id':'m_34','requires':['m_33'],'category':'main','type':'clear_stage','target_stage':108,'target':1,'title':'远古遗迹','description':'通关第108关','rewards':[{'type':'gacha_currency','amount':1300},{'type':'card_with_skills','skill_names':['状态共鸣'],'genome_quality':0.73}]},
    {'id':'m_35','requires':['m_34'],'category':'main','type':'clear_stage','target_stage':120,'target':1,'title':'元素位面','description':'通关第120关','rewards':[{'type':'battle_materials','amount':1500},{'type':'card_with_skills','skill_names':['绝对零度','万象终结'],'genome_quality':0.75}]},
    {'id':'m_36','requires':['m_35'],'category':'main','type':'submit_card','requirements':{'min_atk':200,'min_hp':800},'target':1,'title':'强者试炼','description':'提交一张攻击≥200且生命≥800的卡牌','rewards':[{'type':'gacha_currency','amount':1800}]},
    {'id':'m_37','requires':['m_36'],'category':'main','type':'clear_stage','target_stage':135,'target':1,'title':'深渊之底','description':'通关第135关','rewards':[{'type':'battle_materials','amount':2000},{'type':'card_with_skills','skill_names':['万象终结','永冻领域'],'genome_quality':0.8}]},
    {'id':'m_38','requires':['m_37'],'category':'main','type':'clear_stage','target_stage':155,'target':1,'title':'终焉之路','description':'通关第155关','rewards':[{'type':'gacha_currency','amount':3000},{'type':'battle_materials','amount':1000}]},
    {'id':'m_39','requires':['m_38'],'category':'main','type':'clear_stage','target_stage':180,'target':1,'title':'虚空尽头','description':'通关第180关','rewards':[{'type':'gacha_currency','amount':4000},{'type':'card_with_skills','skill_names':['剧毒新星','万象终结','绝对零度'],'genome_quality':0.85}]},
    {'id':'m_40','requires':['m_39'],'category':'main','type':'clear_stage','target_stage':200,'target':1,'title':'终焉之巅','description':'通关第200关','rewards':[{'type':'gacha_currency','amount':5000},{'type':'battle_materials','amount':3000},{'type':'card_with_skills','skill_names':['万象终结','永冻领域','绝对零度'],'genome_quality':0.9}]},
    # ==================== 支线 (20) ====================
    {'id':'s_01','requires':[],'category':'side','type':'kill_any','target':30,'title':'初露锋芒','description':'累计击杀30个敌人','rewards':[{'type':'battle_materials','amount':50}]},
    {'id':'s_02','requires':['s_01'],'category':'side','type':'breed_count','target':8,'title':'繁殖入门','description':'累计繁殖8次','rewards':[{'type':'gacha_currency','amount':60}]},
    {'id':'s_03','requires':['s_02'],'category':'side','type':'have_cards','target':15,'title':'基因收集者','description':'拥有15张卡牌','rewards':[{'type':'gacha_currency','amount':80}]},
    {'id':'s_04','requires':['s_03'],'category':'side','type':'kill_any','target':100,'title':'百人斩','description':'累计击杀100个敌人','rewards':[{'type':'battle_materials','amount':100}]},
    {'id':'s_05','requires':['s_04'],'category':'side','type':'breed_count','target':20,'title':'繁殖能手','description':'累计繁殖20次','rewards':[{'type':'gacha_currency','amount':120},{'type':'card_with_skills','skill_names':['甘霖'],'genome_quality':0.3}]},
    {'id':'s_06','requires':['s_05'],'category':'side','type':'have_cards','target':25,'title':'卡牌收藏家','description':'拥有25张卡牌','rewards':[{'type':'gacha_currency','amount':150}]},
    {'id':'s_07','requires':['s_06'],'category':'side','type':'kill_boss','target':10,'title':'猎杀精英','description':'累计击杀10个BOSS','rewards':[{'type':'battle_materials','amount':200}]},
    {'id':'s_08','requires':['s_07'],'category':'side','type':'kill_any','target':300,'title':'屠戮机器','description':'累计击杀300个敌人','rewards':[{'type':'gacha_currency','amount':200}]},
    {'id':'s_09','requires':['s_08'],'category':'side','type':'breed_count','target':50,'title':'基因传播者','description':'累计繁殖50次','rewards':[{'type':'gacha_currency','amount':250},{'type':'card_with_skills','skill_names':['冻结','诅咒'],'genome_quality':0.4}]},
    {'id':'s_10','requires':['s_09'],'category':'side','type':'have_cards','target':40,'title':'基因库扩充','description':'拥有40张卡牌','rewards':[{'type':'battle_materials','amount':300}]},
    {'id':'s_11','requires':['s_10'],'category':'side','type':'kill_any','target':500,'title':'战场死神','description':'累计击杀500个敌人','rewards':[{'type':'gacha_currency','amount':350}]},
    {'id':'s_12','requires':['s_11'],'category':'side','type':'breed_count','target':100,'title':'繁殖大师','description':'累计繁殖100次','rewards':[{'type':'gacha_currency','amount':400},{'type':'card_with_skills','skill_names':['自我修复','冰霜护盾'],'genome_quality':0.45}]},
    {'id':'s_13','requires':['s_12'],'category':'side','type':'kill_boss','target':30,'title':'首领克星','description':'累计击杀30个BOSS','rewards':[{'type':'battle_materials','amount':500}]},
    {'id':'s_14','requires':['s_13'],'category':'side','type':'kill_any','target':1000,'title':'千军破','description':'累计击杀1000个敌人','rewards':[{'type':'gacha_currency','amount':600}]},
    {'id':'s_15','requires':['s_14'],'category':'side','type':'have_cards','target':60,'title':'基因宝库','description':'拥有60张卡牌','rewards':[{'type':'battle_materials','amount':700},{'type':'card_with_skills','skill_names':['能量护盾','火焰吐息','血之渴望'],'genome_quality':0.55}]},
    {'id':'s_16','requires':['s_15'],'category':'side','type':'breed_count','target':200,'title':'繁殖狂人','description':'累计繁殖200次','rewards':[{'type':'gacha_currency','amount':800}]},
    {'id':'s_17','requires':['s_16'],'category':'side','type':'kill_any','target':2000,'title':'万夫莫敌','description':'累计击杀2000个敌人','rewards':[{'type':'battle_materials','amount':1000}]},
    {'id':'s_18','requires':['s_17'],'category':'side','type':'kill_boss','target':80,'title':'BOSS终结者','description':'累计击杀80个BOSS','rewards':[{'type':'gacha_currency','amount':1200},{'type':'card_with_skills','skill_names':['永冻领域','剧毒新星'],'genome_quality':0.7}]},
    {'id':'s_19','requires':['s_18'],'category':'side','type':'have_cards','target':100,'title':'基因之主','description':'拥有100张卡牌','rewards':[{'type':'gacha_currency','amount':1500}]},
    {'id':'s_20','requires':['s_19'],'category':'side','type':'kill_any','target':5000,'title':'传说之上','description':'累计击杀5000个敌人','rewards':[{'type':'battle_materials','amount':2000},{'type':'gacha_currency','amount':1000},{'type':'card_with_skills','skill_names':['万象终结','绝对零度','状态共鸣'],'genome_quality':0.85}]},
    # ==================== 挑战 (15) ====================
    {'id':'c_01','requires':[],'category':'challenge','type':'submit_card','requirements':{'min_atk':35},'target':1,'title':'力量试炼','description':'提交一张攻击≥35的卡牌','rewards':[{'type':'gacha_currency','amount':80}]},
    {'id':'c_02','requires':['c_01'],'category':'challenge','type':'no_loss_clear','target_stage':10,'target':1,'title':'无损挑战·一','description':'无阵亡通关第10关','rewards':[{'type':'battle_materials','amount':100}]},
    {'id':'c_03','requires':['c_02'],'category':'challenge','type':'submit_card','requirements':{'min_hp':150},'target':1,'title':'钢铁壁垒','description':'提交一张生命≥150的卡牌','rewards':[{'type':'gacha_currency','amount':120}]},
    {'id':'c_04','requires':['c_03'],'category':'challenge','type':'tech_level','target':5,'title':'科技先锋','description':'任意科技达到5级','rewards':[{'type':'battle_materials','amount':150}]},
    {'id':'c_05','requires':['c_04'],'category':'challenge','type':'submit_card','requirements':{'min_atk':50,'min_def':30},'target':1,'title':'攻守兼备','description':'提交一张攻击≥50且防御≥30的卡牌','rewards':[{'type':'gacha_currency','amount':200},{'type':'card_with_skills','skill_names':['火焰吐息','冻结'],'genome_quality':0.4}]},
    {'id':'c_06','requires':['c_05'],'category':'challenge','type':'no_loss_clear','target_stage':25,'target':1,'title':'无损挑战·二','description':'无阵亡通关第25关','rewards':[{'type':'battle_materials','amount':250}]},
    {'id':'c_07','requires':['c_06'],'category':'challenge','type':'submit_card','requirements':{'min_hp':300,'min_spd':40},'target':1,'title':'如风似岳','description':'提交一张生命≥300且速度≥40的卡牌','rewards':[{'type':'gacha_currency','amount':300}]},
    {'id':'c_08','requires':['c_07'],'category':'challenge','type':'tech_level_all','target':2,'title':'全面科技','description':'所有科技至少2级','rewards':[{'type':'battle_materials','amount':400}]},
    {'id':'c_09','requires':['c_08'],'category':'challenge','type':'submit_card','requirements':{'min_atk':80,'min_hp':400},'target':1,'title':'毁灭之力','description':'提交一张攻击≥80且生命≥400的卡牌','rewards':[{'type':'gacha_currency','amount':500},{'type':'card_with_skills','skill_names':['诅咒','血之渴望','剧毒新星'],'genome_quality':0.55}]},
    {'id':'c_10','requires':['c_09'],'category':'challenge','type':'no_loss_clear','target_stage':50,'target':1,'title':'无损挑战·三','description':'无阵亡通关第50关','rewards':[{'type':'battle_materials','amount':600},{'type':'gacha_currency','amount':300}]},
    {'id':'c_11','requires':['c_10'],'category':'challenge','type':'total_tech_levels','target':30,'title':'科技巨擘','description':'科技总等级达到30级','rewards':[{'type':'gacha_currency','amount':700}]},
    {'id':'c_12','requires':['c_11'],'category':'challenge','type':'submit_card','requirements':{'min_atk':120,'min_hp':600,'min_def':60},'target':1,'title':'全能战神','description':'提交一张攻击≥120、生命≥600且防御≥60的卡牌','rewards':[{'type':'battle_materials','amount':800},{'type':'card_with_skills','skill_names':['永冻领域','猩红风暴'],'genome_quality':0.7}]},
    {'id':'c_13','requires':['c_12'],'category':'challenge','type':'no_loss_clear','target_stage':100,'target':1,'title':'无损挑战·四','description':'无阵亡通关第100关','rewards':[{'type':'gacha_currency','amount':1000},{'type':'battle_materials','amount':500}]},
    {'id':'c_14','requires':['c_13'],'category':'challenge','type':'submit_card','requirements':{'min_atk':200,'min_hp':800,'min_spd':80},'target':1,'title':'传说试炼','description':'提交一张攻击≥200、生命≥800且速度≥80的卡牌','rewards':[{'type':'gacha_currency','amount':1500},{'type':'card_with_skills','skill_names':['万象终结','绝对零度','炼狱之火'],'genome_quality':0.8}]},
    {'id':'c_15','requires':['c_14'],'category':'challenge','type':'no_loss_clear','target_stage':150,'target':1,'title':'无损挑战·五','description':'无阵亡通关第150关','rewards':[{'type':'gacha_currency','amount':2000},{'type':'battle_materials','amount':1000},{'type':'card_with_skills','skill_names':['剧毒新星','永冻领域','万象终结'],'genome_quality':0.9}]},
]

class Card:
    card_count = 0
    _genome_boost_mult = 1.0
    _life_extension_mult = 1.0
    _hybrid_vigor_level = 0
    _hybrid_vigor_all = False
    _stat_break_mult = 1.0
    
    def __init__(self, name, gender=None, chromosomes=None, genes=None, parent_ids=None):
        Card.card_count += 1
        self.id = f"CARD{Card.card_count:04d}"
        self.name = name
        self.parent_ids = parent_ids or []
        self.birth_time = time.time()
        
        if chromosomes:
            self.chromosomes = chromosomes
            self.gender = Card._gender_from_chromosomes(chromosomes)
        elif genes:
            self.gender = gender or 'female'
            self.chromosomes = self._build_chromosomes_from_genes(genes, self.gender)
        else:
            self.gender = gender or random.choice(['male', 'female'])
            self.chromosomes = self._build_chromosomes(self.gender)
        
        self.genes = {}
        self._rebuild_genes()
        self.traits = self.calculate_traits()
        self.is_alive = self.check_vital_genes()
        self.skills = self.get_skills()
        self.passive_skills = self.get_passive_skills()
        self.reflex_bound_skill = None
        if '条件反射' in self.passive_skills and self.skills:
            self.reflex_bound_skill = random.choice(self.skills)
        self.sprite_genome = self._random_genome()
        self.bloodline = None
        self.star = 1
        self.training = {}
        self.modules = []
        self.chips = []
        self.chip_slots = 1
        self.equipment = {}
        self.favorite = False
        self.base_traits = {}
    
    @staticmethod
    def _random_genome():
        from battle_config import ENEMY_TEMPLATES as _ET
        _tids = list(_ET.keys())
        _a, _b = random.sample(_tids, 2)
        _g = [_a] * 32 + [_b] * 32
        random.shuffle(_g)
        return _g
    
    @staticmethod
    def _gender_from_chromosomes(chromosomes):
        sex_homologs = chromosomes.get('chrX', [])
        if len(sex_homologs) >= 2 and sex_homologs[1].get('type') == 'Y':
            return 'male'
        return 'female'
    
    @staticmethod
    def _build_genome_for_regions(regions):
        parts = []
        is_dominant = {}
        for gene_name, _, _ in regions:
            tmpl = GENE_TEMPLATES.get(gene_name, {})
            seq = tmpl.get('sequence', 'ATGCATGC')
            parts.append(seq)
            is_dominant[gene_name] = True
        return ''.join(parts), is_dominant

    @staticmethod
    def _pad_genome(genome, chr_id):
        target = CHROMOSOME_LENGTH.get(chr_id, len(genome))
        if len(genome) < target:
            genome += ''.join(random.choices(BASES, k=target - len(genome)))
        return genome

    @staticmethod
    def _get_padding_starts():
        cache = {}
        for chr_id, regions in GENE_REGIONS.items():
            if regions:
                cache[chr_id] = max(end for _, _, end in regions)
            else:
                cache[chr_id] = 0
        return cache

    def _optimize_genome(self, quality):
        if quality <= 0:
            return
        padding_start = self._get_padding_starts()
        import math
        from collections import defaultdict

        all_rules = defaultdict(list)

        for _trait_name, regions in STAT_ENHANCE_REGIONS.items():
            for region in regions:
                chr_id = region['chr']
                start = region['start']
                end = region['end']
                safe_start = max(start, padding_start.get(chr_id, 0))
                if safe_start >= end:
                    continue
                add_rules = region.get('add', {})
                mul_rules = region.get('mul', {})
                if add_rules:
                    max_abs = max(abs(v) for v in add_rules.values())
                    norm_add = {k: v / max_abs for k, v in add_rules.items()}
                    for pos in range(safe_start, end):
                        key = (chr_id, pos)
                        all_rules[key].append(('add', norm_add))
                if mul_rules:
                    for pos in range(safe_start, end):
                        key = (chr_id, pos)
                        all_rules[key].append(('mul', mul_rules))

        targets = {}
        for pos_key, rules_list in all_rules.items():
            scores = {'A': 0.0, 'T': 0.0, 'G': 0.0, 'C': 0.0}
            for rule_type, rules in rules_list:
                for base in scores:
                    if rule_type == 'add':
                        scores[base] += rules.get(base, 0.0)
                    else:
                        f = rules.get(base, 1.0)
                        if f > 0:
                            scores[base] += math.log(f)
            sorted_bases = sorted(scores, key=lambda b: scores[b], reverse=True)
            if len(sorted_bases) >= 2 and abs(scores[sorted_bases[0]] - scores[sorted_bases[1]]) < 1e-9:
                continue
            targets[pos_key] = sorted_bases[0]

        chr_targets = defaultdict(list)
        for (cid, pos), base in targets.items():
            chr_targets[cid].append((pos, base))
        for cid in chr_targets:
            chr_targets[cid].sort(key=lambda x: x[0])

        for chr_id, homologs in self.chromosomes.items():
            if chr_id not in chr_targets:
                continue
            pos_base_list = chr_targets[chr_id]
            n_to_set = int(len(pos_base_list) * quality + 0.5)
            n_to_set = max(0, min(n_to_set, len(pos_base_list)))
            for homolog in homologs:
                genome = list(homolog.get('genome', ''))
                if not genome:
                    continue
                for idx in range(n_to_set):
                    pos, base = pos_base_list[idx]
                    if pos < len(genome):
                        genome[pos] = base
                homolog['genome'] = ''.join(genome)

    @staticmethod
    def _build_chromosomes(gender):
        import copy
        chromosomes = {}
        for chr_id, chr_conf in CHROMOSOME_LAYOUT.items():
            if chr_id in ('chrY', 'chrG'):
                continue
            if chr_id == 'chrX':
                x_genome, x_dom = Card._build_genome_for_regions(GENE_REGIONS['chrX'])
                x_genome = Card._pad_genome(x_genome, 'chrX')
                y_genome, y_dom = Card._build_genome_for_regions(GENE_REGIONS['chrY'])
                y_genome = Card._pad_genome(y_genome, 'chrY')
                if gender == 'male':
                    chromosomes['chrX'] = [
                        {'type': 'X', 'genome': x_genome, 'is_dominant': copy.deepcopy(x_dom)},
                        {'type': 'Y', 'genome': y_genome, 'is_dominant': copy.deepcopy(y_dom)}
                    ]
                else:
                    chromosomes['chrX'] = [
                        {'type': 'X', 'genome': x_genome, 'is_dominant': copy.deepcopy(x_dom)},
                        {'type': 'X', 'genome': x_genome, 'is_dominant': copy.deepcopy(x_dom)}
                    ]
            else:
                genome, dom = Card._build_genome_for_regions(GENE_REGIONS[chr_id])
                genome = Card._pad_genome(genome, chr_id)
                chromosomes[chr_id] = [
                    {'genome': genome, 'is_dominant': copy.deepcopy(dom)},
                    {'genome': genome, 'is_dominant': copy.deepcopy(dom)}
                ]
        return chromosomes
    
    @staticmethod
    def _build_chromosomes_from_genes(genes, gender):
        import copy
        chromosomes = {}
        for chr_id, chr_conf in CHROMOSOME_LAYOUT.items():
            if chr_id in ('chrY', 'chrG'):
                continue
            regions = GENE_REGIONS[chr_id]
            if chr_id == 'chrX':
                x_parts, x_dom = [], {}
                for gene_name, _, _ in GENE_REGIONS['chrX']:
                    gd = genes.get(gene_name, {})
                    a1 = gd.get('allele1', {})
                    seq = a1.get('seq', '')
                    x_parts.append(seq)
                    x_dom[gene_name] = a1.get('is_dominant', True)
                x_genome = Card._pad_genome(''.join(x_parts), 'chrX')
                
                y_parts, y_dom = [], {}
                for gene_name, _, _ in GENE_REGIONS['chrY']:
                    gd = genes.get(gene_name, {})
                    a1 = gd.get('allele1', {})
                    seq = a1.get('seq', '')
                    y_parts.append(seq)
                    y_dom[gene_name] = a1.get('is_dominant', True)
                y_genome = Card._pad_genome(''.join(y_parts), 'chrY')
                
                if gender == 'male':
                    chromosomes['chrX'] = [
                        {'type': 'X', 'genome': x_genome, 'is_dominant': x_dom},
                        {'type': 'Y', 'genome': y_genome, 'is_dominant': y_dom}
                    ]
                else:
                    chromosomes['chrX'] = [
                        {'type': 'X', 'genome': x_genome, 'is_dominant': x_dom},
                        {'type': 'X', 'genome': x_genome, 'is_dominant': x_dom}
                    ]
            else:
                parts_a, parts_b = [], []
                dom_a, dom_b = {}, {}
                for gene_name, _, _ in regions:
                    gd = genes.get(gene_name, {})
                    a1 = gd.get('allele1', {})
                    a2 = gd.get('allele2', {})
                    parts_a.append(a1.get('seq', ''))
                    parts_b.append(a2.get('seq', ''))
                    dom_a[gene_name] = a1.get('is_dominant', True)
                    dom_b[gene_name] = a2.get('is_dominant', True)
                genome_a, genome_b = ''.join(parts_a), ''.join(parts_b)
                chromosomes[chr_id] = [
                    {'genome': Card._pad_genome(genome_a, chr_id), 'is_dominant': dom_a},
                    {'genome': Card._pad_genome(genome_b, chr_id), 'is_dominant': dom_b}
                ]
        return chromosomes
    
    def _sync_gene_to_chromosome(self, gene_name):
        gene_data = self.genes.get(gene_name)
        if not gene_data:
            return
        chr_id = gene_data.get('chromosome', 'chr1')
        if chr_id == 'chrY':
            chr_id = 'chrX'
        homologs = self.chromosomes.get(chr_id, [{}, {}])
        if chr_id == 'chrX' and gene_name in [g[0] for g in GENE_REGIONS['chrY']]:
            h_idx = 1
            regions = GENE_REGIONS['chrY']
        elif chr_id == 'chrX':
            regions = GENE_REGIONS['chrX']
            for h_idx in [0, 1]:
                _, start, end = next((r for r in regions if r[0] == gene_name), (None, None, None))
                if start is None:
                    continue
                genome = homologs[h_idx].get('genome', '')
                if start < len(genome):
                    seq = gene_data['allele1']['seq'] if h_idx == 0 else gene_data['allele2']['seq']
                    new_genome = genome[:start] + seq + genome[end:]
                    homologs[h_idx]['genome'] = new_genome
            return
        else:
            regions = GENE_REGIONS.get(chr_id, [])
        
        _, start, end = next((r for r in regions if r[0] == gene_name), (None, None, None))
        if start is None:
            return
        for h_idx in [0, 1]:
            genome = homologs[h_idx].get('genome', '')
            if start < len(genome):
                seq = gene_data['allele1']['seq'] if h_idx == 0 else gene_data['allele2']['seq']
                new_genome = genome[:start] + seq + genome[end:]
                homologs[h_idx]['genome'] = new_genome
    
    def _rebuild_genes(self):
        self.genes.clear()
        for chr_id, homologs in self.chromosomes.items():
            if chr_id == 'chrX':
                region_list = GENE_REGIONS['chrX']
            else:
                region_list = GENE_REGIONS.get(chr_id, [])
            
            for gene_name, start, end in region_list:
                tmpl = GENE_TEMPLATES.get(gene_name, {})
                if not tmpl:
                    continue
                g0 = homologs[0].get('genome', '')
                g1 = homologs[1].get('genome', '')
                seq1 = g0[start:end] if len(g0) >= end else ''
                seq2 = g1[start:end] if len(g1) >= end else ''
                if not seq1 and not seq2:
                    continue
                old = self.genes.get(gene_name, {})
                self.genes[gene_name] = {
                    'allele1': {'seq': seq1, 'is_dominant': homologs[0].get('is_dominant', {}).get(gene_name, True)},
                    'allele2': {'seq': seq2, 'is_dominant': homologs[1].get('is_dominant', {}).get(gene_name, True)},
                    'template_dominant': tmpl.get('dominant', True),
                    'methylated': old.get('methylated', False),
                    'vital': tmpl.get('vital', False),
                    'research_count': old.get('research_count', 0),
                    'chromosome': chr_id,
                }
            
            if chr_id == 'chrX' and homologs[1].get('type') == 'Y':
                for gene_name, start, end in GENE_REGIONS['chrY']:
                    tmpl = GENE_TEMPLATES.get(gene_name, {})
                    if not tmpl:
                        continue
                    g1 = homologs[1].get('genome', '')
                    seq2 = g1[start:end] if len(g1) >= end else ''
                    if not seq2:
                        continue
                    old = self.genes.get(gene_name, {})
                    self.genes[gene_name] = {
                        'allele1': {'seq': '', 'is_dominant': True},
                        'allele2': {'seq': seq2, 'is_dominant': homologs[1].get('is_dominant', {}).get(gene_name, True)},
                        'template_dominant': tmpl.get('dominant', True),
                        'methylated': old.get('methylated', False),
                        'vital': tmpl.get('vital', False),
                        'research_count': old.get('research_count', 0),
                        'chromosome': 'chrX',
                    }
    
    def calculate_traits(self):
        traits = {}
        
        for gene_name, gene_data in self.genes.items():
            template = GENE_TEMPLATES.get(gene_name, {})
            trait_name = template.get('affects_trait')
            
            if not trait_name:
                continue
            
            allele1 = gene_data['allele1']
            allele2 = gene_data['allele2']
            is_template_dominant = gene_data.get('template_dominant', True)
            methylated = gene_data['methylated']
            
            a1_is_dominant = allele1.get('is_dominant', True) == is_template_dominant
            a2_is_dominant = allele2.get('is_dominant', True) == is_template_dominant
            
            if a1_is_dominant and a2_is_dominant:
                genotype = 'AA'
            elif not a1_is_dominant and not a2_is_dominant:
                genotype = 'aa'
            else:
                genotype = 'Aa'
            
            config = TRAIT_CONFIG.get(trait_name, {})
            base_min = config.get('base_min', 10)
            base_max = config.get('base_max', 30)
            
            if genotype == 'AA':
                value_min = int(base_max * 0.8)
                value_max = base_max + 10
            elif genotype == 'Aa':
                value_min = int(base_min * 1.1)
                value_max = int(base_max * 0.75)
            else:
                value_min = base_min
                value_max = base_min + 1
            
            base_value = sum(ord(b) for b in allele1['seq']) % (value_max - value_min) + value_min
            
            if methylated:
                base_value = int(base_value * METHYLATION_EFFECT['stat_factor'])
            
            traits[trait_name] = base_value
        
        # Apply genome sequence enhancements to stat traits
        for trait_name in list(traits.keys()):
            if trait_name in STAT_ENHANCE_REGIONS:
                traits[trait_name] = self._apply_genome_enhancements(trait_name, traits[trait_name])
        
        self.base_traits = dict(traits)
        
        # Apply life_extension bonus to lifespan trait
        life_mult = getattr(Card, '_life_extension_mult', 1.0)
        if life_mult != 1.0 and 'lifespan' in traits:
            traits['lifespan'] = int(traits['lifespan'] * life_mult)

        # Apply stat_break caps increase
        stat_mult = getattr(Card, '_stat_break_mult', 1.0)
        if stat_mult != 1.0:
            for t in list(traits.keys()):
                traits[t] = int(traits[t] * stat_mult)

        # Apply hybrid vigor bonus when parents differ
        if HYBRID_VIGOR_CONFIG['enabled'] and len(self.parent_ids) >= 2:
            if self.parent_ids[0] != self.parent_ids[1]:
                vigor_factor = HYBRID_VIGOR_CONFIG['bonus_factor']
                hv_level = getattr(Card, '_hybrid_vigor_level', 0)
                if hv_level >= 2:
                    vigor_factor *= 1.5
                all_traits = getattr(Card, '_hybrid_vigor_all', False)
                if all_traits:
                    for t in list(traits.keys()):
                        traits[t] = int(traits.get(t, 0) * (1 + vigor_factor))
                else:
                    for t in HYBRID_VIGOR_CONFIG['bonus_traits']:
                        if t in traits:
                            traits[t] = int(traits[t] * (1 + vigor_factor))
        
        if getattr(self, 'bloodline', None):
            from gene_config import BLOODLINES
            bd = BLOODLINES.get(self.bloodline, {})
            for stat_key in ('attack', 'health', 'defense', 'speed'):
                pct = bd.get(stat_key[:3], 0) / 100.0
                if pct > 0 and stat_key in traits:
                    traits[stat_key] = int(traits[stat_key] * (1 + pct))
        
        star = getattr(self, 'star', 1)
        if star > 1:
            star_mult = 1 + 0.10 * (star - 1)
            for t in list(traits.keys()):
                traits[t] = int(traits[t] * star_mult)
        
        if getattr(self, 'modules', None):
            from gene_config import MODULE_POOLS
            for mid in self.modules:
                md = MODULE_POOLS.get(mid, {})
                stat = md.get('stat', '')
                pct = md.get('pct', 0) / 100.0
                if stat and pct > 0 and stat in traits:
                    traits[stat] = int(traits[stat] * (1 + pct))
        
        eq = getattr(self, 'equipment', None)
        if eq:
            import random as _rnd
            for slot, item in eq.items():
                affixes = item.get('affixes', [])
                for aff in affixes:
                    stat = aff.get('stat', '')
                    val = aff.get('value', 0)
                    is_pct = aff.get('is_pct', False)
                    if stat in traits:
                        if is_pct:
                            traits[stat] = int(traits[stat] * (1 + val / 100.0))
                        else:
                            traits[stat] = traits.get(stat, 0) + val
        
        return traits
    
    def _apply_genome_enhancements(self, trait_name, base_value):
        regions = STAT_ENHANCE_REGIONS.get(trait_name, [])
        if not regions:
            return base_value
        
        total_add = 0
        total_mul = 1.0
        
        for region in regions:
            chr_id = region['chr']
            start = region['start']
            end = region['end']
            add_rules = region.get('add', {})
            mul_rules = region.get('mul', {})
            
            homologs = self.chromosomes.get(chr_id, [{}, {}])
            for homolog in homologs:
                genome = homolog.get('genome', '')
                if start >= len(genome):
                    continue
                actual_end = min(end, len(genome))
                seq = genome[start:actual_end]
                
                if add_rules:
                    for base, val in add_rules.items():
                        total_add += seq.count(base) * val
                
                if mul_rules:
                    for base, factor in mul_rules.items():
                        count = seq.count(base)
                        if count > 0:
                            total_mul *= factor ** count
        
        result = int(round((base_value + total_add) * total_mul * Card._genome_boost_mult))
        return max(1, result)
    
    def _get_active_sequence(self, allele1, allele2, is_template_dominant):
        a1_is_dominant = allele1.get('is_dominant', True)
        a2_is_dominant = allele2.get('is_dominant', True)
        
        if is_template_dominant:
            # 显性基因：只要有显性等位基因就用显性序列，数值由显性基因决定
            if a1_is_dominant:
                return allele1['seq']
            return allele2['seq']
        else:
            # 隐性基因：只有纯合隐性才表达
            if not a1_is_dominant and not a2_is_dominant:
                if not a1_is_dominant:
                    return allele1['seq']
                return allele2['seq']
            return allele1['seq']
    
    def get_genotype(self, gene_name):
        gene_data = self.genes.get(gene_name)
        if not gene_data:
            return "?"
        
        allele1 = gene_data['allele1']
        allele2 = gene_data['allele2']
        is_template_dominant = gene_data.get('template_dominant', True)
        
        a1 = 'A' if (allele1['is_dominant'] == is_template_dominant) else 'a'
        a2 = 'A' if (allele2['is_dominant'] == is_template_dominant) else 'a'
        
        return f"{a1}{a2}"
    
    def get_skills(self):
        skills = []
        for gene_name in SKILL_GENES:
            gene_data = self.genes.get(gene_name)
            if not gene_data or gene_data['methylated']:
                continue
            
            template = GENE_TEMPLATES.get(gene_name, {})
            is_template_dominant = template.get('dominant', True)
            
            allele1 = gene_data['allele1']
            allele2 = gene_data['allele2']
            a1_is_dominant = allele1.get('is_dominant', True)
            a2_is_dominant = allele2.get('is_dominant', True)
            
            has_skill = False
            if is_template_dominant:
                has_skill = a1_is_dominant or a2_is_dominant
            else:
                has_skill = a1_is_dominant and a2_is_dominant
            
            if has_skill:
                skill_name = template.get('skill_name')
                if skill_name:
                    skills.append(skill_name)
        return skills
    
    def get_passive_skills(self):
        passive = {}
        for gene_name in PASSIVE_GENES:
            gene_data = self.genes.get(gene_name)
            if not gene_data or gene_data['methylated']:
                continue
            template = GENE_TEMPLATES.get(gene_name, {})
            pname = template.get('passive_name', '')
            if not pname:
                continue
            
            is_template_dominant = gene_data.get('template_dominant', True)
            a1_is_dominant = gene_data['allele1'].get('is_dominant', True) == is_template_dominant
            a2_is_dominant = gene_data['allele2'].get('is_dominant', True) == is_template_dominant
            
            if not a1_is_dominant and not a2_is_dominant:
                if pname == '荆棘':
                    seq = gene_data['allele1'].get('seq', '')
                    tail = seq[6:12] if len(seq) >= 12 else ''
                    t_count = tail.count('T')
                    reflect_pct = 50 + t_count * 20
                    passive[pname] = reflect_pct
                elif pname in ('暗杀者', '条件反射'):
                    passive[pname] = True
        return passive
    
    def check_vital_genes(self):
        for vital_gene in VITAL_GENES:
            gene_data = self.genes.get(vital_gene)
            if gene_data:
                allele1 = gene_data['allele1']
                allele2 = gene_data['allele2']
                seq1 = allele1.get('seq', '')
                seq2 = allele2.get('seq', '')
                
                min_length = CUTTING_CONFIG['vital_gene_min_length']
                if len(seq1) < min_length or len(seq2) < min_length:
                    return False
        return True
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'chromosomes': self.chromosomes,
            'genes': self.genes,
            'traits': self.traits,
            'skills': self.skills,
            'passive_skills': self.passive_skills,
            'is_alive': self.is_alive,
            'birth_time': self.birth_time,
            'parent_ids': self.parent_ids,
            'isolated_genes': list(getattr(self, 'isolated_genes', set())),
            'reflex_bound_skill': getattr(self, 'reflex_bound_skill', None),
            '_rarity': getattr(self, '_rarity', None),
            'sprite_genome': getattr(self, 'sprite_genome', None),
            'bloodline': getattr(self, 'bloodline', None),
            'star': getattr(self, 'star', 1),
            'training': getattr(self, 'training', {}),
            'modules': getattr(self, 'modules', []),
            'chips': getattr(self, 'chips', []),
            'equipment': getattr(self, 'equipment', {}),
            'chip_slots': getattr(self, 'chip_slots', 1),
            'favorite': getattr(self, 'favorite', False),
            'base_traits': getattr(self, 'base_traits', {}),
        }
    
    @staticmethod
    def from_dict(data):
        ver = data.get('_genome_version', 1)
        if 'chromosomes' in data:
            if ver >= 2:
                card = Card(data['name'], chromosomes=data['chromosomes'], parent_ids=data.get('parent_ids', []))
            else:
                card = Card._from_old_genome_dict(data)
        else:
            card = Card(data['name'], data.get('gender', 'female'), genes=data.get('genes'),
                        parent_ids=data.get('parent_ids', []))
        card.id = data['id']
        card.name = data['name']
        card.gender = data['gender']
        card.traits = data['traits']
        card.is_alive = data['is_alive']
        card.birth_time = data.get('birth_time', time.time())
        card.parent_ids = data.get('parent_ids', [])
        card.skills = data.get('skills', [])
        for gene_name in SKILL_GENES:
            tmpl = GENE_TEMPLATES.get(gene_name, {})
            desired = tmpl.get('skill_name') in card.skills
            gene_data = card.genes.get(gene_name)
            if gene_data:
                gene_data['allele1']['is_dominant'] = desired
                gene_data['allele2']['is_dominant'] = desired
                chr_id = gene_data.get('chromosome', 'chr1')
                if chr_id == 'chrY':
                    chr_id = 'chrX'
                homologs = card.chromosomes.get(chr_id, [])
                for h in homologs:
                    dom = h.get('is_dominant')
                    if dom and gene_name in dom:
                        dom[gene_name] = desired
        card.passive_skills = data.get('passive_skills', {})
        card.reflex_bound_skill = data.get('reflex_bound_skill', None)
        card._rarity = data.get('_rarity', None)
        card.bloodline = data.get('bloodline', None)
        card.star = data.get('star', 1)
        card.training = data.get('training', {})
        card.modules = data.get('modules', [])
        card.chips = data.get('chips', [])
        card.chip_slots = data.get('chip_slots', 1)
        card.equipment = data.get('equipment', {})
        card.favorite = data.get('favorite', False)
        card.base_traits = data.get('base_traits', {})
        for chip_info in card.chips:
            skill = chip_info.get('skill_name', '')
            if skill and skill not in card.skills:
                card.skills.append(skill)
        isolated = data.get('isolated_genes', [])
        card.isolated_genes = set(isolated) if isolated else set()
        sg = data.get('sprite_genome', None)
        if sg and len(sg) == 64:
            card.sprite_genome = sg
        return card
    
    @staticmethod
    def _from_old_genome_dict(data):
        chromosomes = data['chromosomes']
        genes_data = data.get('genes', {})
        for chr_id, homologs in list(chromosomes.items()):
            for h in homologs:
                if 'genes' in h and 'genome' not in h:
                    h['genome'] = ''
                    h['is_dominant'] = {}
                    for gname, gval in h.pop('genes', {}).items():
                        h['genome'] += gval.get('seq', '')
                        h['is_dominant'][gname] = gval.get('is_dominant', True)
        card = Card(data['name'], chromosomes=chromosomes, parent_ids=data.get('parent_ids', []))
        for gene_name, gd in genes_data.items():
            if gene_name in card.genes:
                card.genes[gene_name]['methylated'] = gd.get('methylated', False)
                card.genes[gene_name]['research_count'] = gd.get('research_count', 0)
        return card


class Game:
    SAVE_FILE = 'gene_game_save.json'
    SAVE_VERSION = 3
    _save_dir = None
    
    def __init__(self, load_save=True, save_dir=None):
        if save_dir:
            Game._save_dir = save_dir
            self.SAVE_FILE = os.path.join(save_dir, 'gene_game_save.json')
        self.cards = []
        self.max_cards = 20
        self.effective_max_cards = 20
        self.breeding_queue = []
        self.tech_tree = self._copy_tech_tree()
        self.breed_speed_multiplier = 1.0
        self.auto_breeding = False
        self.unlocked_stages = list(range(1, 31))
        self.max_stage = 30
        # New stages 61-100 are unlocked progressively via end_battle
        self.card_count = 0
        self.gacha_currency = 0
        self.pity_counters = {pid: 0 for pid in self.GACHA_POOLS}
        self.battle_materials = 0
        self.no_loss_stages = set()
        self.quest_progress = {}
        self.quest_completed = set()
        self.quest_claimed = set()
        self.enemy_kills = {}
        self.breed_counter = 0
        self.gene_essence = 0
        self.chip_inventory = {}
        self.module_inventory = {}
        self.challenge_scores = {}
        self.achievements = {}
        self.equipment_inventory = {}
        self.base_buildings = {}
        
        if load_save and self.load_game():
            pass
        else:
            self.create_initial_cards()
        
        if len(self.cards) == 0:
            self.create_initial_cards()
        self._init_quests()
    
    def _copy_tech_tree(self):
        return {k: v.copy() for k, v in TECH_TREE.items()}
    
    def _create_low_stat_card(self, name, gender, atk=10, hp=60, def_val=8, spd=8):
        card = Card(name, gender)
        card.traits['attack'] = atk
        card.traits['health'] = hp
        card.traits['defense'] = def_val
        card.traits['speed'] = spd
        card.traits['stamina'] = 20
        card.traits['critical_rate'] = 3
        card.traits['dodge_rate'] = 2
        card.traits['lifespan'] = 50
        return card

    def create_initial_cards(self):
        config = INITIAL_CARDS_CONFIG
        if 'cards' in config:
            for entry in config['cards']:
                card = Card(entry['name'], entry.get('gender'))
                card.skills = card.skills[:2]
                self._init_starter_passive(card)
                self._deactivate_extra_skill_genes(card)
                self.cards.append(card)
        else:
            for i in range(config['count']):
                gender = config['genders'][i] if i < len(config['genders']) else 'male'
                name = config['names'].get(gender, f"初始体{i+1}")
                card = Card(name, gender)
                card.skills = card.skills[:2]
                self._init_starter_passive(card)
                self._deactivate_extra_skill_genes(card)
                self.cards.append(card)
        starter_gifts = [
            {'name': '新手战士', 'gender': 'male', 'atk': 12, 'hp': 70, 'def_val': 10, 'spd': 9},
            {'name': '新手法师', 'gender': 'female', 'atk': 15, 'hp': 55, 'def_val': 6, 'spd': 10},
            {'name': '新手护卫', 'gender': 'male', 'atk': 8, 'hp': 90, 'def_val': 14, 'spd': 6},
            {'name': '新手斥候', 'gender': 'female', 'atk': 11, 'hp': 60, 'def_val': 7, 'spd': 14},
        ]
        for g in starter_gifts:
            card = self._create_low_stat_card(g['name'], g['gender'],
                atk=g['atk'], hp=g['hp'], def_val=g['def_val'], spd=g['spd'])
            card.skills = card.skills[:2]
            self._init_starter_passive(card)
            self._deactivate_extra_skill_genes(card)
            self.cards.append(card)
    
    def _deactivate_extra_skill_genes(self, card):
        from gene_config import SKILL_GENES, GENE_TEMPLATES
        kept_skill_genes = set()
        for sname in card.skills:
            for gn, tmpl in GENE_TEMPLATES.items():
                if tmpl.get('skill_name') == sname:
                    kept_skill_genes.add(gn)
                    break
        for gene_name in SKILL_GENES:
            if gene_name in kept_skill_genes:
                continue
            gene_data = card.genes.get(gene_name)
            if not gene_data:
                continue
            gene_data['allele1']['is_dominant'] = False
            gene_data['allele2']['is_dominant'] = False
            chr_id = gene_data.get('chromosome', 'chr1')
            homologs = card.chromosomes.get(chr_id)
            if homologs:
                for h in homologs:
                    dom = h.get('is_dominant')
                    if dom and gene_name in dom:
                        dom[gene_name] = False
    
    def _init_starter_passive(self, card):
        import random
        from gene_config import PASSIVE_GENES, GENE_TEMPLATES
        active_gene = random.choice(PASSIVE_GENES)
        for gene_name in PASSIVE_GENES:
            gene_data = card.genes.get(gene_name)
            if not gene_data:
                continue
            new_dom = gene_name != active_gene
            gene_data['allele1']['is_dominant'] = new_dom
            gene_data['allele2']['is_dominant'] = new_dom
            chr_id = gene_data.get('chromosome', 'chr1')
            homologs = card.chromosomes.get(chr_id)
            if homologs:
                for h in homologs:
                    dom = h.get('is_dominant')
                    if dom and gene_name in dom:
                        dom[gene_name] = new_dom
        card.passive_skills = card.get_passive_skills()
    
    @staticmethod
    def _fibonacci(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    def _get_card_storage_level(self):
        return self.tech_tree.get('card_storage', {}).get('level', 0)

    def _get_card_storage_bonus(self):
        total = 0
        for i in range(1, self._get_card_storage_level() + 1):
            total += self._fibonacci(i)
        return total

    def _get_card_storage_cost(self):
        level = self._get_card_storage_level()
        return 20 * (self._fibonacci(level + 1) ** 2)

    def generate_low_quality_card(self, gender=None):
        import random
        names = ['巡林者', '精灵守卫', '月光行者', '风语者', '花之精灵',
                 '叶之守护者', '露水精灵', '林间使者', '溪流歌者', '苔藓行者']
        name = f"{random.choice(names)}-{random.randint(100, 999)}"
        if gender is None:
            gender = random.choice(['male', 'female'])
        card = Card(name, gender=gender)
        if card.is_alive:
            self.cards.append(card)
            return card
        return None

    def create_card(self, name, gender=None, chromosomes=None, genes=None, parent_ids=None, add_to_library=True):
        if add_to_library and len(self.cards) >= self.effective_max_cards:
            return None
        card = Card(name, gender=gender, chromosomes=chromosomes, genes=genes, parent_ids=parent_ids)
        if card.is_alive:
            opt_level = self.tech_tree.get('gene_optimize', {}).get('level', 0)
            if opt_level > 0:
                for t in list(card.traits.keys()):
                    card.traits[t] = card.traits.get(t, 0) + opt_level * 3
            if add_to_library:
                self.cards.append(card)
            return card
        return None
    
    def _mutate_genome_region(self, genome, start, end, severity='light'):
        if start >= len(genome):
            return genome
        actual_end = min(end, len(genome))
        region = genome[start:actual_end]
        if not region:
            return genome
        mutated = self.mutate_sequence(region, severity)
        return genome[:start] + mutated + genome[actual_end:]

    def _create_gamete(self, chromosomes, gender):
        import copy
        gamete = {}
        for chr_id in CHROMOSOME_IDS:
            if chr_id == 'chrY':
                continue
            h = chromosomes.get(chr_id, [{}, {}])
            if len(h) < 2:
                continue

            if chr_id == 'chrX' and h[1].get('type') == 'Y':
                gamete[chr_id] = copy.deepcopy(random.choice(h))
            else:
                h0 = copy.deepcopy(h[0])
                h1 = copy.deepcopy(h[1])
                if random.random() < 0.5:
                    h0, h1 = h1, h0
                g0 = h0.get('genome', '')
                g1 = h1.get('genome', '')
                if g0 and g1 and len(g0) == len(g1) and len(g0) > 1:
                    n = random.randint(1, min(3, len(g0) - 1))
                    pts = sorted(random.sample(range(1, len(g0)), n))
                    parts, prev = [], 0
                    use_h0 = True
                    for pt in pts:
                        src = g0 if use_h0 else g1
                        parts.append(src[prev:pt])
                        prev = pt
                        use_h0 = not use_h0
                    parts.append((g0 if use_h0 else g1)[prev:])
                    h0['genome'] = ''.join(parts)

                    new_dom = {}
                    for gname, gs, ge in GENE_REGIONS.get(chr_id, []):
                        mid = (gs + ge) // 2
                        from_h0 = True
                        for pt in pts:
                            if mid < pt:
                                break
                            from_h0 = not from_h0
                        new_dom[gname] = h0['is_dominant'].get(gname, True) if from_h0 else h1['is_dominant'].get(gname, True)
                    h0['is_dominant'] = new_dom
                gamete[chr_id] = h0
        return gamete

    def breeding(self, card1, card2):
        if card1.gender == card2.gender:
            return None

        if card1.gender == 'male':
            male, female = card1, card2
        else:
            male, female = card2, card1

        sperm = self._create_gamete(male.chromosomes, 'male')
        egg = self._create_gamete(female.chromosomes, 'female')

        child_chromosomes = {}
        for chr_id in CHROMOSOME_IDS:
            if chr_id == 'chrY':
                continue
            child_chromosomes[chr_id] = [egg.get(chr_id, {}), sperm.get(chr_id, {})]

        child_gender = Card._gender_from_chromosomes(child_chromosomes)

        mutation_rate = INHERIT_CONFIG['mutation_rate']
        evo_level = self.tech_tree.get('evolution_boost', {}).get('level', 0)
        mutation_rate += evo_level * 0.05
        for chr_id, homologs in child_chromosomes.items():
            for h_idx, homolog in enumerate(homologs):
                genome = homolog.get('genome', '')
                if not genome:
                    continue
                for gene_name, start, end in GENE_REGIONS.get(chr_id if chr_id != 'chrX' or h_idx == 0 else 'chrY', []):
                    if random.random() < mutation_rate:
                        genome = self._mutate_genome_region(genome, start, end)
                homolog['genome'] = genome
                if chr_id == 'chrX' and h_idx == 1 and homolog.get('type') == 'Y':
                    for gene_name, start, end in GENE_REGIONS['chrY']:
                        if random.random() < mutation_rate:
                            genome = self._mutate_genome_region(genome, start, end)
                    homolog['genome'] = genome

        self.breed_counter += 1
        return child_chromosomes, child_gender

    def inherit_bloodline(self, parent1, parent2):
        from gene_config import BLOODLINES, FUSION_TABLE
        r = random.random()
        b1 = getattr(parent1, 'bloodline', None)
        b2 = getattr(parent2, 'bloodline', None)
        if r < 0.25 and b1:
            return b1
        if r < 0.50 and b2:
            return b2
        if r < 0.60 and b1 and b2 and b1 != b2:
            fused = FUSION_TABLE.get((b1, b2))
            if fused:
                return fused
        if r < 0.70:
            return random.choice(list(BLOODLINES.keys()))
        return None
    
    def mutate_sequence(self, seq, severity='light'):
        seq_list = list(seq)
        mutation_count = 1 if severity == 'light' else random.randint(2, 4)
        
        for _ in range(mutation_count):
            if seq_list:
                idx = random.randint(0, len(seq_list) - 1)
                seq_list[idx] = random.choice(BASES)
        
        return ''.join(seq_list)
    
    def restrict_enzyme_cut(self, gene_name, cut_position, card):
        gene_data = card.genes.get(gene_name)
        if not gene_data:
            return False, "基因不存在"
        
        template = GENE_TEMPLATES.get(gene_name, {})
        min_length = CUTTING_CONFIG['vital_gene_min_length'] if template.get('vital') else CUTTING_CONFIG['stat_gene_min_length']
        
        chr_id = gene_data.get('chromosome', 'chr1')
        if chr_id == 'chrY':
            chr_id = 'chrX'
        homologs = card.chromosomes.get(chr_id, [{}, {}])
        
        regions = GENE_REGIONS.get(chr_id if chr_id != 'chrX' else 'chrX', [])
        _, start, end = next((r for r in regions if r[0] == gene_name), (None, None, None))
        if start is None and chr_id == 'chrX':
            regions = GENE_REGIONS['chrY']
            _, start, end = next((r for r in regions if r[0] == gene_name), (None, None, None))
        if start is None:
            return False, "基因位置未找到"
        
        seq1 = gene_data['allele1']['seq']
        seq2 = gene_data['allele2']['seq']
        if cut_position < 0 or cut_position >= len(seq1) or cut_position >= len(seq2):
            return False, "切割位置无效"
        
        new_seq1 = seq1[:cut_position] + seq1[cut_position+1:]
        new_seq2 = seq2[:cut_position] + seq2[cut_position+1:]
        
        vital_hit = len(new_seq1) < min_length or len(new_seq2) < min_length
        
        pos = start + cut_position
        for h_idx in [0, 1]:
            genome = homologs[h_idx].get('genome', '')
            if pos < len(genome):
                homologs[h_idx]['genome'] = genome[:pos] + genome[pos+1:]
        
        card._rebuild_genes()
        if vital_hit:
            card.is_alive = False
            card.traits = card.calculate_traits()
            return 'vital_damaged', f"破坏了关键基因 {template.get('description', gene_name)}，卡牌死亡！"
        
        card.traits = card.calculate_traits()
        card.is_alive = card.check_vital_genes()
        card.skills = card.get_skills()
        return True, "基因切割成功"
    
    def methylation(self, gene_name, card, enable=None):
        gene_data = card.genes.get(gene_name)
        if not gene_data:
            return False, "基因不存在"
        
        if enable is None:
            enable = not gene_data['methylated']
        
        gene_data['methylated'] = enable
        card.traits = card.calculate_traits()
        card.skills = card.get_skills()
        
        status = "已甲基化" if enable else "已去甲基化"
        return True, f"甲基化操作成功: {status}"
    
    def radiation_mutation(self, card):
        if not card.is_alive:
            return None
        
        isolated = getattr(card, 'isolated_genes', set()) if hasattr(card, 'isolated_genes') else set()
        candidates = [g for g in GENE_TEMPLATES if g not in isolated]
        if not candidates:
            return None
        gene_to_mutate = random.choice(candidates)
        gene_data = card.genes.get(gene_to_mutate)
        
        if not gene_data:
            return None
        
        study_level = self.tech_tree.get('mutation_study', {}).get('level', 0)
        light_rate = RADIATION_CONFIG['light_mutation_rate']
        if study_level >= 3:
            light_rate = min(0.7, light_rate + 0.2)
        severity = 'light' if random.random() < light_rate else 'heavy'
        
        old_traits = card.traits.copy()
        old_alive = card.is_alive
        
        allele1 = gene_data['allele1']
        allele2 = gene_data['allele2']
        
        if random.random() < 0.5:
            allele1['seq'] = self.mutate_sequence(allele1.get('seq', ''), severity)
        if random.random() < 0.5:
            allele2['seq'] = self.mutate_sequence(allele2.get('seq', ''), severity)
        
        card._sync_gene_to_chromosome(gene_to_mutate)
        card.traits = card.calculate_traits()
        card.is_alive = card.check_vital_genes()
        card.skills = card.get_skills()
        
        dir_level = self.tech_tree.get('directed_mutation', {}).get('level', 0)
        resist_level = self.tech_tree.get('radiation_resist', {}).get('level', 0)
        study_level = self.tech_tree.get('mutation_study', {}).get('level', 0)
        neg_bias = RADIATION_CONFIG['negative_bias']
        neg_bias -= dir_level * 0.15
        neg_bias -= resist_level * 0.15
        if study_level >= 2:
            neg_bias -= 0.15
        neg_bias = max(0.1, neg_bias)

        trait_changes = {}
        for trait_name in old_traits:
            if trait_name in card.traits:
                change = card.traits[trait_name] - old_traits[trait_name]
                if abs(change) > 0:
                    if random.random() < neg_bias:
                        if change > 0:
                            change = -random.randint(1, abs(change))
                    trait_changes[trait_name] = change
        
        template = GENE_TEMPLATES.get(gene_to_mutate, {})
        gene_desc = template.get('description', gene_to_mutate)
        
        return {
            'gene': gene_to_mutate,
            'gene_desc': gene_desc,
            'changes': trait_changes,
            'alive': card.is_alive,
            'was_alive': old_alive,
            'died': old_alive and not card.is_alive
        }
    
    def research_gene(self, gene_name, card):
        gene_data = card.genes.get(gene_name)
        if not gene_data:
            return None
        
        gene_data['research_count'] = gene_data.get('research_count', 0) + 1
        
        threshold = RESEARCH_CONFIG['reveal_threshold']
        if gene_data['research_count'] >= threshold:
            template = GENE_TEMPLATES.get(gene_name, {})
            return {
                'description': template.get('description', '未知基因'),
                'category': template.get('category', 'unknown'),
                'affects_trait': template.get('affects_trait'),
                'skill_name': template.get('skill_name'),
                'vital': template.get('vital', False),
            }
        return None
    
    def clone_card(self, card):
        import copy
        if not card.is_alive:
            return None, "源卡牌已死亡"
        if len(self.cards) >= self.effective_max_cards:
            return None, f"卡牌库已满 (上限{self.effective_max_cards}张)"
        new_chromosomes = copy.deepcopy(card.chromosomes)
        new_name = f"{card.name}的克隆体"
        clone = Card(new_name, chromosomes=new_chromosomes, parent_ids=[card.id, card.id])
        if clone.is_alive:
            self.cards.append(clone)
            return clone, f"克隆成功: {new_name}"
        return None, "克隆失败"
    
    def splice_gene(self, gene_name, donor_card, target_card):
        if not donor_card.is_alive or not target_card.is_alive:
            return False, "卡牌已死亡"
        donor_gene = donor_card.genes.get(gene_name)
        target_gene = target_card.genes.get(gene_name)
        if not donor_gene or not target_gene:
            return False, "基因不存在"
        target_gene['allele1']['seq'] = donor_gene['allele1']['seq']
        target_gene['allele2']['seq'] = donor_gene['allele2']['seq']
        target_card._rebuild_genes()
        target_card.traits = target_card.calculate_traits()
        target_card.is_alive = target_card.check_vital_genes()
        target_card.skills = target_card.get_skills()
        return True, f"拼接成功: 将 {gene_name} 从 {donor_card.name} 移植到 {target_card.name}"
    
    def activate_gene(self, gene_name, card):
        gene_data = card.genes.get(gene_name)
        if not gene_data:
            return False, "基因不存在"
        if not gene_data['methylated']:
            return False, "该基因未被甲基化"
        gene_data['methylated'] = False
        card.skills = card.get_skills()
        card.traits = card.calculate_traits()
        return True, f"基因激活成功: {gene_name} 已去甲基化"
    
    def crispr_edit(self, gene_name, card, position, new_base):
        if not card.is_alive:
            return False, "卡牌已死亡"
        gene_data = card.genes.get(gene_name)
        if not gene_data:
            return False, "基因不存在"
        if new_base not in BASES:
            return False, f"无效碱基: {new_base}，仅接受 A/T/G/C"
        for key in ['allele1', 'allele2']:
            seq = gene_data[key]['seq']
            if position < 0 or position >= len(seq):
                return False, f"位置 {position} 超出范围 (0-{len(seq)-1})"
            new_seq = list(seq)
            new_seq[position] = new_base
            gene_data[key]['seq'] = ''.join(new_seq)
        card._sync_gene_to_chromosome(gene_name)
        card.traits = card.calculate_traits()
        card.is_alive = card.check_vital_genes()
        if not card.is_alive:
            return 'vital_damaged', f"CRISPR编辑破坏了关键基因，卡牌死亡！"
        return True, f"CRISPR编辑成功: {gene_name} 位置 {position} 改为 {new_base}"
    
    def gene_knockout(self, gene_name, card):
        if not card.is_alive:
            return False, "卡牌已死亡"
        gene_data = card.genes.get(gene_name)
        if not gene_data:
            return False, "基因不存在"
        template = GENE_TEMPLATES.get(gene_name, {})
        if template.get('vital'):
            return False, "无法敲除关键基因"
        for key in ['allele1', 'allele2']:
            seq = gene_data[key]['seq']
            gene_data[key]['seq'] = 'N' * len(seq)
        card._sync_gene_to_chromosome(gene_name)
        card.traits = card.calculate_traits()
        card.is_alive = card.check_vital_genes()
        card.skills = card.get_skills()
        return True, f"基因敲除成功: {gene_name} 已失活"
    
    def store_gene_fragment(self, gene_name, card, label=None):
        gene_data = card.genes.get(gene_name)
        if not gene_data:
            return False, "基因不存在"
        if not hasattr(self, 'gene_library'):
            self.gene_library = {}
        entry = {
            'gene_name': gene_name,
            'allele1_seq': gene_data['allele1']['seq'],
            'allele2_seq': gene_data['allele2']['seq'],
            'source_card': card.id,
            'source_name': card.name,
        }
        key = label or f"{gene_name}_#{len(self.gene_library)+1}"
        self.gene_library[key] = entry
        return True, f"基因片段已存入基因库: {key}"
    
    def retrieve_gene_fragment(self, key, target_card):
        if not hasattr(self, 'gene_library') or key not in self.gene_library:
            return False, "基因库中未找到该片段"
        entry = self.gene_library[key]
        gene_name = entry['gene_name']
        target_gene = target_card.genes.get(gene_name)
        if not target_gene:
            return False, f"目标卡牌没有 {gene_name} 基因"
        target_gene['allele1']['seq'] = entry['allele1_seq']
        target_gene['allele2']['seq'] = entry['allele2_seq']
        target_card._rebuild_genes()
        target_card.traits = target_card.calculate_traits()
        target_card.is_alive = target_card.check_vital_genes()
        target_card.skills = target_card.get_skills()
        return True, f"基因片段 {key} 已应用到 {target_card.name}"
    
    def get_gene_library(self):
        if not hasattr(self, 'gene_library'):
            self.gene_library = {}
        return self.gene_library
    
    def extract_gamete(self, card, as_male):
        if not card.is_alive:
            return None, "卡牌已死亡"
        if as_male and card.gender != 'male':
            return None, "需要雄性卡牌提取精子"
        if not as_male and card.gender != 'female':
            return None, "需要雌性卡牌提取卵子"
        import copy
        gamete = copy.deepcopy(self._create_gamete(card.chromosomes, 'male' if as_male else 'female'))
        return gamete, f"{'精子' if as_male else '卵子'}提取成功"
    
    def fuse_gametes(self, sperm, egg, label1='父本', label2='母本'):
        child_chromosomes = {}
        for chr_id in CHROMOSOME_IDS:
            if chr_id == 'chrY':
                continue
            child_chromosomes[chr_id] = [egg.get(chr_id, {}), sperm.get(chr_id, {})]
        child_gender = Card._gender_from_chromosomes(child_chromosomes)
        mutation_rate = INHERIT_CONFIG['mutation_rate']
        evo_level = self.tech_tree.get('evolution_boost', {}).get('level', 0)
        mutation_rate += evo_level * 0.05
        for chr_id, homologs in child_chromosomes.items():
            for h_idx, homolog in enumerate(homologs):
                genome = homolog.get('genome', '')
                if not genome:
                    continue
                for gene_name, start, end in GENE_REGIONS.get(chr_id if chr_id != 'chrX' or h_idx == 0 else 'chrY', []):
                    if random.random() < mutation_rate:
                        genome = self._mutate_genome_region(genome, start, end)
                homolog['genome'] = genome
                if chr_id == 'chrX' and h_idx == 1 and homolog.get('type') == 'Y':
                    for gene_name, start, end in GENE_REGIONS['chrY']:
                        if random.random() < mutation_rate:
                            genome = self._mutate_genome_region(genome, start, end)
                    homolog['genome'] = genome
        return child_chromosomes, child_gender
    
    def duplicate_chromosome(self, chr_id, source_card, target_card):
        if not source_card.is_alive or not target_card.is_alive:
            return False, "卡牌已死亡"
        if chr_id not in source_card.chromosomes or chr_id not in target_card.chromosomes:
            return False, "染色体不存在"
        import copy
        target_card.chromosomes[chr_id] = copy.deepcopy(source_card.chromosomes[chr_id])
        target_card._rebuild_genes()
        target_card.traits = target_card.calculate_traits()
        target_card.is_alive = target_card.check_vital_genes()
        target_card.skills = target_card.get_skills()
        return True, f"染色体 {chr_id} 复制成功"
    
    def toggle_gene_isolation(self, gene_name, card):
        if not hasattr(card, 'isolated_genes'):
            card.isolated_genes = set()
        if gene_name in card.isolated_genes:
            card.isolated_genes.discard(gene_name)
            return True, f"{gene_name} 已移出隔离保护"
        else:
            iso_level = self.tech_tree.get('gene_isolation', {}).get('level', 0)
            if iso_level >= 2:
                pass
            elif len(card.isolated_genes) >= 1:
                return False, "基因隔离 Lv.1 只能保护1个基因，升级至Lv.2可保护多个"
            card.isolated_genes.add(gene_name)
            return True, f"{gene_name} 已加入隔离保护"
    
    def star_up_card(self, card):
        if not card.is_alive:
            return False, "卡牌已死亡"
        if card.star >= 5:
            return False, "已达到最大星级"
        cost_essence = card.star * 10
        cost_mats = card.star * 20
        if self.gene_essence < cost_essence:
            return False, f"基因精华不足 (需要{cost_essence}，当前{self.gene_essence})"
        if self.battle_materials < cost_mats:
            return False, f"战斗材料不足 (需要{cost_mats}，当前{self.battle_materials})"
        dup = next((c for c in self.cards if c.id != card.id and c.name == card.name and c.is_alive), None)
        if dup is None:
            return False, "需要一张同名卡牌作为材料"
        self.cards.remove(dup)
        self.gene_essence -= cost_essence
        self.battle_materials -= cost_mats
        card.star += 1
        if card.star >= 3:
            card.chip_slots = 2
        if card.star >= 5:
            card.chip_slots = 3
        card.traits = card.calculate_traits()
        return True, f"升星成功! 当前{card.star}星"

    def train_card(self, card, stat_key):
        if not card.is_alive:
            return False, "卡牌已死亡"
        max_sessions = card.star * 8
        done = card.training.get(stat_key, 0)
        if done >= max_sessions:
            return False, f"{stat_key}训练已达上限({max_sessions}次)"
        cost = 20 + done * 5
        if self.battle_materials < cost:
            return False, f"战斗材料不足(需要{cost}，当前{self.battle_materials})"
        self.battle_materials -= cost
        card.training[stat_key] = done + 1
        import random
        if stat_key == 'health':
            boost = random.randint(3, 8)
        elif stat_key == 'attack':
            boost = random.randint(1, 3)
        elif stat_key == 'defense':
            boost = random.randint(1, 2)
        else:
            boost = random.randint(1, 2)
        card.traits[stat_key] = card.traits.get(stat_key, 10) + boost
        return True, f"训练成功! {stat_key}+{boost} ({card.training[stat_key]}/{max_sessions})"

    def equip_chip(self, card, chip_id):
        if not card.is_alive:
            return False, "卡牌已死亡"
        if len(card.chips) >= card.chip_slots:
            return False, f"芯片槽已满({card.chip_slots}个)"
        if self.chip_inventory.get(chip_id, 0) <= 0:
            return False, "芯片库存不足"
        from gene_config import CHIP_POOLS
        cp = CHIP_POOLS.get(chip_id, {})
        if not cp:
            return False, "芯片数据不存在"
        self.chip_inventory[chip_id] -= 1
        skill = cp['skill']
        card.chips.append({'chip_id': chip_id, 'skill_name': skill})
        if skill not in card.skills:
            card.skills.append(skill)
        return True, f"装备芯片: {cp['name']}"

    def remove_chip(self, card, chip_index):
        if not card.is_alive or chip_index >= len(card.chips):
            return False, "无效操作"
        removed = card.chips.pop(chip_index)
        card.skills = [s for s in card.skills if s != removed['skill_name']]
        return True, "芯片已移除"

    def equip_module(self, card, module_id):
        if not card.is_alive:
            return False, "卡牌已死亡"
        max_slots = 1 if card.star < 3 else (2 if card.star < 5 else 3)
        if len(card.modules) >= max_slots:
            return False, f"模组槽已满({max_slots}个)"
        if self.module_inventory.get(module_id, 0) <= 0:
            return False, "模组库存不足"
        self.module_inventory[module_id] -= 1
        card.modules.append(module_id)
        card.traits = card.calculate_traits()
        return True, "模组装备成功"

    def remove_module(self, card, module_id):
        if module_id in card.modules:
            card.modules.remove(module_id)
            card.traits = card.calculate_traits()
            return True, "模组已卸下"
        return False, "该模组未装备"

    def merge_modules(self, module_id):
        from gene_config import MODULE_POOLS, MODULE_MERGE
        md = MODULE_POOLS.get(module_id, {})
        lv = md.get('level', 0)
        next_lv = MODULE_MERGE.get(lv, 0)
        if next_lv == 0:
            return False, "该模组已达最高等级"
        next_id = module_id.replace(f'_{lv}', f'_{next_lv}')
        if self.module_inventory.get(module_id, 0) >= 2:
            self.module_inventory[module_id] -= 2
            self.module_inventory[next_id] = self.module_inventory.get(next_id, 0) + 1
            return True, f"合成成功! {MODULE_POOLS[next_id]['name']}"
        return False, "需要2个同等级模组合成"

    def generate_equipment(self, stage_num):
        from gene_config import EQUIPMENT_SLOTS, EQUIPMENT_RARITY, EQUIPMENT_AFFIX_POOLS, EQUIPMENT_SLOT_NAMES, EQUIPMENT_NAMES
        import random
        roll = random.random()
        cumulative = 0
        chosen_rarity = EQUIPMENT_RARITY[0]
        for r in EQUIPMENT_RARITY:
            cumulative += r['drop']
            if roll < cumulative:
                chosen_rarity = r
                break
        slot = random.choice(EQUIPMENT_SLOTS)
        pool = EQUIPMENT_AFFIX_POOLS.get(chosen_rarity['id']) or EQUIPMENT_AFFIX_POOLS.get('epic', EQUIPMENT_AFFIX_POOLS.get('common', []))
        min_a, max_a = chosen_rarity['affixes']
        n_affixes = random.randint(min_a, min(max_a, len(pool)))
        picked = random.sample(pool, n_affixes)
        affixes = []
        for code, stat_key, is_pct, lo, hi in picked:
            val = random.randint(lo, hi)
            affixes.append({'code': code, 'stat': stat_key, 'value': val, 'is_pct': bool(is_pct)})
        item_id = f'{slot}_{chosen_rarity["id"]}_{random.randint(1000,9999)}'
        name_pool = EQUIPMENT_NAMES.get(slot, {}).get(chosen_rarity['id'], [f'{chosen_rarity["prefix"]}{EQUIPMENT_SLOT_NAMES.get(slot,slot)}'])
        real_name = random.choice(name_pool)
        item = {
            'id': item_id, 'slot': slot, 'rarity': chosen_rarity['id'],
            'name': real_name, 'affixes': affixes,
        }
        if item_id not in self.equipment_inventory:
            self.equipment_inventory[item_id] = {'data': item, 'count': 0}
        self.equipment_inventory[item_id]['count'] += 1
        return item

    def equip_item(self, card, item_id):
        inv_entry = self.equipment_inventory.get(item_id)
        if not inv_entry or inv_entry.get('count', 0) <= 0:
            return False, "装备不存在"
        item = dict(inv_entry['data'])
        inv_entry['count'] -= 1
        if inv_entry['count'] <= 0:
            del self.equipment_inventory[item_id]
        slot = item['slot']
        old = card.equipment.get(slot)
        if old:
            oid = old['id']
            if oid not in self.equipment_inventory:
                self.equipment_inventory[oid] = {'data': old, 'count': 0}
            self.equipment_inventory[oid]['count'] += 1
        card.equipment[slot] = item
        card.traits = card.calculate_traits()
        return True, "装备成功"

    def unequip_item(self, card, slot):
        if slot not in card.equipment:
            return False, "该槽位无装备"
        item = card.equipment.pop(slot)
        iid = item['id']
        if iid not in self.equipment_inventory:
            self.equipment_inventory[iid] = {'data': item, 'count': 0}
        self.equipment_inventory[iid]['count'] += 1
        card.traits = card.calculate_traits()
        return True, "已卸下"

    def _parse_equip_slot(self, item_id):
        parts = item_id.split('_')
        return parts[0] if parts else ''

    def _parse_equip_rarity(self, item_id):
        parts = item_id.split('_')
        return parts[1] if len(parts) > 1 else 'common'

    def upgrade_building(self, bid):
        from gene_config import BASE_BUILDINGS
        bld = next((b for b in BASE_BUILDINGS if b['id'] == bid), None)
        if not bld:
            return False, "建筑不存在"
        lv = self.base_buildings.get(bid, 0)
        if lv >= bld['max_lv']:
            return False, "已满级"
        cost_mats = 50 + lv * 30
        cost_essence = 5 + lv * 3
        if self.battle_materials < cost_mats:
            return False, f"材料不足(需要{cost_mats})"
        if self.gene_essence < cost_essence:
            return False, f"精华不足(需要{cost_essence})"
        self.battle_materials -= cost_mats
        self.gene_essence -= cost_essence
        self.base_buildings[bid] = lv + 1
        return True, f"升级成功! Lv.{lv+1}"

    def _get_chip_slots(self, card):
        star = getattr(card, 'star', 1)
        if star >= 5:
            return 3
        elif star >= 3:
            return 2
        return 1
    
    def add_breeding_task(self, card1, card2, callback):
        base_duration = BREEDING_CONFIG['base_duration']
        duration = base_duration / self.breed_speed_multiplier
        
        task = {
            'card1': card1,
            'card2': card2,
            'start_time': time.time(),
            'duration': duration,
            'callback': callback,
            'completed': False
        }
        self.breeding_queue.append(task)
    
    def update_breeding(self):
        current_time = time.time()
        completed = []
        
        for task in self.breeding_queue:
            if task['completed']:
                continue
            
            elapsed = current_time - task['start_time']
            if elapsed >= task['duration']:
                task['completed'] = True
                completed.append(task)
        
        for task in completed:
            task['callback']()
        
        self.breeding_queue = [t for t in self.breeding_queue if not t['completed']]
    
    def get_breed_speed(self):
        embryo_level = self.tech_tree.get('embryo_engineering', {}).get('level', 0)
        fast_level = self.tech_tree.get('fast_breeding', {}).get('level', 0)
        base = 1.0 + embryo_level * BREEDING_CONFIG['speed_per_level']
        if fast_level > 0:
            base += fast_level * 0.3
        return base

    def _sync_tech_effects(self):
        gb_level = self.tech_tree.get('genome_boost', {}).get('level', 0)
        Card._genome_boost_mult = 1.0 + gb_level * 0.2
        
        life_level = self.tech_tree.get('life_extension', {}).get('level', 0)
        Card._life_extension_mult = 1.0 + life_level * 0.2
        
        hv_level = self.tech_tree.get('hybrid_enhance', {}).get('level', 0)
        Card._hybrid_vigor_level = hv_level
        super_hv = self.tech_tree.get('super_hybrid', {}).get('unlocked', False)
        Card._hybrid_vigor_all = super_hv and self.tech_tree.get('super_hybrid', {}).get('level', 0) > 0

        sb_level = self.tech_tree.get('stat_break', {}).get('level', 0)
        Card._stat_break_mult = 1.0 + sb_level * 0.1

        self.effective_max_cards = self.max_cards + self._get_card_storage_bonus()

        self.breed_speed_multiplier = self.get_breed_speed()
    
    def unlock_tech(self, tech_name):
        tech = self.tech_tree.get(tech_name)
        if not tech or tech['unlocked']:
            return False
        
        req = tech.get('unlock_requirement')
        if not req:
            return False
        
        req_tech, req_level = req
        req_tech_data = self.tech_tree.get(req_tech, {})
        
        if req_tech_data.get('level', 0) >= req_level:
            tech['unlocked'] = True
            return True
        return False
    
    def upgrade_tech(self, tech_name):
        tech = self.tech_tree.get(tech_name)
        if not tech:
            return False, "科技不存在"
        
        if not tech['unlocked']:
            if not self.unlock_tech(tech_name):
                return False, "未满足解锁条件"
        
        if tech['level'] >= tech['max_level']:
            return False, "已达到最大等级"
        
        next_level = tech['level'] + 1
        
        cost = tech.get('costs', {}).get(next_level, {})
        bm_needed = cost.get('battle_materials', 0)
        gc_needed = cost.get('gacha_currency', 0)
        
        if tech_name == 'card_storage':
            bm_needed = self._get_card_storage_cost()
            gc_needed = 0
        
        if self.battle_materials < bm_needed:
            return False, f"战斗材料不足 (需要 {bm_needed}，当前 {self.battle_materials})"
        if self.gacha_currency < gc_needed:
            return False, f"基因密钥不足 (需要 {gc_needed}，当前 {self.gacha_currency})"
        
        self.battle_materials -= bm_needed
        self.gacha_currency -= gc_needed
        tech['level'] += 1
        
        effect = tech['effects'].get(tech['level'], '')
        
        self._sync_tech_effects()
        
        if tech_name in ('genome_boost', 'life_extension', 'hybrid_enhance', 'super_hybrid', 'stat_break'):
            for card in self.cards:
                if card.is_alive:
                    card.traits = card.calculate_traits()
        
        return True, f"{tech['name']} 已升级到 {tech['level']} 级\n效果: {effect}"

    # ============================================================
    # 抽卡系统
    # ============================================================
    GACHA_POOLS = {
        'poison': {
            'name': '剧毒之池',
            'unlock_stage': 1,
            'cost': 80,
            'description': '蕴含剧毒之力的卡池，可获得与中毒相关的强力技能',
            'ultra_skills': ['skill_toxic_nova', 'skill_corrosive_touch'],
            'theme_color': '#39ff14',
            'theme_bg': '#0a1a0a',
            'theme_secondary': '#0a3d0a',
            'icon': '☠️',
            'flavor': '紫黑色的毒雾在池中翻涌，空气中弥漫着腐蚀性的气息……只有最坚韧的基因才能在此幸存。',
        },
        'flame': {
            'name': '烈焰之池',
            'unlock_stage': 30,
            'cost': 120,
            'description': '燃烧一切的烈焰之力，可获得与灼烧相关的强力技能',
            'ultra_skills': ['skill_inferno', 'skill_ember_revival'],
            'theme_color': '#ff4500',
            'theme_bg': '#1a0a0a',
            'theme_secondary': '#3d0a0a',
            'icon': '🔥',
            'flavor': '岩浆在池底翻滚咆哮，灼热的气浪扭曲了视线……这份力量足以焚尽一切阻碍。',
        },
        'frost': {
            'name': '冰霜之池',
            'unlock_stage': 50,
            'cost': 160,
            'description': '冰封万物的极寒之力，可获得与冰冻相关的强力技能',
            'ultra_skills': ['skill_permafrost', 'skill_absolute_zero'],
            'theme_color': '#00bfff',
            'theme_bg': '#0a0a1a',
            'theme_secondary': '#0a0a3d',
            'icon': '❄️',
            'flavor': '极寒的冻气从池面升起，连时间仿佛都被冻结……沉睡于冰层之下的，是永寂的力量。',
        },
        'blood': {
            'name': '血池',
            'unlock_stage': 70,
            'cost': 200,
            'description': '嗜血者的乐园，可获得与流血相关的强力技能',
            'ultra_skills': ['skill_bloodthirst', 'skill_crimson_storm'],
            'theme_color': '#dc143c',
            'theme_bg': '#1a0a0a',
            'theme_secondary': '#3d0a0a',
            'icon': '🩸',
            'flavor': '猩红的血池翻涌不止，刺鼻的铁锈味充斥鼻腔……以血换血，以命搏命。',
        },
        'final': {
            'name': '终焉之池',
            'unlock_stage': 90,
            'cost': 300,
            'description': '掌控一切负面效果的终极卡池',
            'ultra_skills': ['skill_omnibus_end', 'skill_status_resonance'],
            'theme_color': '#9932cc',
            'theme_bg': '#0a0a1a',
            'theme_secondary': '#1a0a2e',
            'icon': '💀',
            'flavor': '混沌的暗紫色能量在池中旋涡般涌动……这里汇聚了世间一切负面状态的终极源头。',
        },
    }
    
    def get_unlocked_pools(self):
        unlocked = {}
        for pid, pool in self.GACHA_POOLS.items():
            if self.max_stage >= pool['unlock_stage']:
                unlocked[pid] = pool
        return unlocked
    
    def _inject_gacha_genes(self, card, gene_name):
        tmpl = GENE_TEMPLATES.get(gene_name)
        if not tmpl:
            return
        active_seq = tmpl.get('sequence', 'AAAAAAAAAAAA')
        from gene_config import CHROMOSOME_LENGTH as _GL
        target_len = _GL.get('chrG', 200)
        regs = GENE_REGIONS.get('chrG', [])
        parts = []
        dom_map = {}
        for gname, gs, ge in regs:
            gtmpl = GENE_TEMPLATES.get(gname, {})
            if gname == gene_name:
                seq = active_seq
                dom_map[gname] = True
            else:
                filler = gtmpl.get('recessive_sequence', 'a' * (ge - gs))
                seq = filler[:ge-gs].ljust(ge-gs, 'a')
                dom_map[gname] = False
            parts.append(seq)
        genome = ''.join(parts)
        if len(genome) < target_len:
            genome += 'a' * (target_len - len(genome))
        else:
            genome = genome[:target_len]
        card.chromosomes['chrG'] = [
            {'genome': genome, 'is_dominant': dict(dom_map)},
            {'genome': genome, 'is_dominant': dict(dom_map)},
        ]
        card._rebuild_genes()
        card.traits = card.calculate_traits()
        card.skills = card.get_skills()
        card.passive_skills = card.get_passive_skills()
    
    def gacha_pull(self, pool_id, count=1):
        pool = self.GACHA_POOLS.get(pool_id)
        if not pool:
            return None, "卡池不存在"
        if self.max_stage < pool['unlock_stage']:
            return None, "卡池未解锁"
        total_cost = pool['cost'] * count
        if self.gacha_currency < total_cost:
            return None, f"基因密钥不足（需要{total_cost}，当前{self.gacha_currency}）"
        
        self.gacha_currency -= total_cost
        results = []
        for _ in range(count):
            self.pity_counters[pool_id] += 1
            
            if self.pity_counters[pool_id] >= 360:
                rarity = 'ultra'
            else:
                roll = random.random()
                if roll < 0.002:
                    rarity = 'ultra'
                elif roll < 0.017:
                    rarity = 'rare'
                else:
                    rarity = 'normal'
            
            gender = random.choice(['male', 'female'])
            names_pool = ['迅捷体', '坚韧体', '狂暴体', '灵巧体', '钢铁体',
                          '暗影体', '光辉体', '混沌体', '星辰体', '虚空体',
                          '熔岩体', '冰霜体', '风暴体', '深渊体', '圣光体']
            name = random.choice(names_pool)
            card = self.create_card(name, gender, add_to_library=False)
            if not card:
                continue
            card.skills = []
            card.passive_skills = {}
            
            if rarity == 'rare':
                for t in list(card.traits.keys()):
                    card.traits[t] = int(card.traits.get(t, 10) * 1.2)
                from battle_config import SKILL_EFFECTS as _SE
                extra = [s for s in _SE if s not in card.skills]
                random.shuffle(extra)
                card.skills.extend(extra[:2])
                card._rarity = 'rare'
            elif rarity == 'ultra':
                self.pity_counters[pool_id] = 0
                gene_name = random.choice(pool['ultra_skills'])
                self._inject_gacha_genes(card, gene_name)
                card._rarity = 'ultra'
            else:
                card._rarity = 'normal'
            
            results.append(card)
            
            roll_bonus = random.random()
            if roll_bonus < 0.08:
                from gene_config import CHIP_POOLS
                chip_id = random.choice(list(CHIP_POOLS.keys()))
                self.chip_inventory[chip_id] = self.chip_inventory.get(chip_id, 0) + 1
            elif roll_bonus < 0.16:
                from gene_config import MODULE_POOLS
                mod_id = random.choice([k for k, v in MODULE_POOLS.items() if v['level'] == 1])
                self.module_inventory[mod_id] = self.module_inventory.get(mod_id, 0) + 1
        
        return results, f"抽卡成功，获得{len(results)}张卡牌"
    
    # ── 任务系统 ──
    def _init_quests(self):
        for qd in QUEST_DEFINITIONS:
            qid = qd['id']
            if qid not in self.quest_progress:
                self.quest_progress[qid] = 0

    def _grant_achievement_reward(self, ach_id):
        from gene_config import ACHIEVEMENTS, BLOODLINES
        ach = next((a for a in ACHIEVEMENTS if a['id'] == ach_id), None)
        if not ach: return
        r = ach.get('reward', {})
        for k, v in r.items():
            if k == 'battle_mats':
                self.battle_materials += v
            elif k == 'gacha_currency':
                self.gacha_currency += v
            elif k == 'gene_essence':
                self.gene_essence += v
            elif k == 'chip':
                self.chip_inventory[v] = self.chip_inventory.get(v, 0) + 1
            elif k == 'module':
                self.module_inventory[v] = self.module_inventory.get(v, 0) + 1
            elif k == 'card':
                card = self._create_skill_reward_card(['万象终结'], quality=0.7)
                if card:
                    card.name = v
                    card.bloodline = random.choice(list(BLOODLINES.keys())) if BLOODLINES else None

    def claim_achievement(self, ach_id):
        if ach_id not in self.achievements:
            return None, "成就未完成"
        from gene_config import ACHIEVEMENTS
        ach = next((a for a in ACHIEVEMENTS if a['id'] == ach_id), None)
        if not ach:
            return None, "成就不存在"
        r = ach.get('reward', {})
        msgs = []
        for k, v in r.items():
            if k == 'battle_mats': self.battle_materials += v; msgs.append(f'材料+{v}')
            elif k == 'gacha_currency': self.gacha_currency += v; msgs.append(f'密钥+{v}')
            elif k == 'gene_essence': self.gene_essence += v; msgs.append(f'精华+{v}')
            elif k == 'chip': self.chip_inventory[v] = self.chip_inventory.get(v,0)+1; msgs.append(f'芯片+1')
            elif k == 'module': self.module_inventory[v] = self.module_inventory.get(v,0)+1; msgs.append(f'模组+1')
            elif k == 'card':
                card = self._create_skill_reward_card(['万象终结'], quality=0.7)
                if card:
                    card.name = v
                    card.bloodline = random.choice(list(BLOODLINES.keys()))
                    msgs.append(f'卡牌:{v}')
        del self.achievements[ach_id]
        return msgs, None

    def _get_quest_progress(self, qid):
        qd = next(q for q in QUEST_DEFINITIONS if q['id'] == qid)
        t = qd['type']
        if t == 'clear_stage':
            return 1 if self.max_stage >= qd['target_stage'] else 0
        elif t == 'no_loss_clear':
            return 1 if qd['target_stage'] in self.no_loss_stages else 0
        elif t == 'kill_any':
            return sum(self.enemy_kills.values())
        elif t == 'kill_boss':
            return self.enemy_kills.get('__boss__', 0)
        elif t == 'submit_card':
            return self.quest_progress.get(qid, 0)
        elif t == 'breed_count':
            return self.breed_counter
        elif t == 'tech_level':
            return max(tch['level'] for tch in self.tech_tree.values())
        elif t == 'tech_level_all':
            return min(tch['level'] for tch in self.tech_tree.values())
        elif t == 'have_cards':
            return len(self.cards)
        elif t == 'total_tech_levels':
            return sum(tch['level'] for tch in self.tech_tree.values())
        return 0

    def _is_quest_unlocked(self, qid):
        qd = next((q for q in QUEST_DEFINITIONS if q['id'] == qid), None)
        if not qd or not qd.get('requires'):
            return True
        return all(r in self.quest_claimed for r in qd['requires'])

    def _check_quest(self, qid):
        if not self._is_quest_unlocked(qid):
            return False
        if qid in self.quest_completed or qid in self.quest_claimed:
            return False
        p = self._get_quest_progress(qid)
        self.quest_progress[qid] = p
        qd = next(q for q in QUEST_DEFINITIONS if q['id'] == qid)
        if p >= qd['target']:
            self.quest_completed.add(qid)
            return True
        return False

    def _check_all_quests(self):
        newly = []
        for qd in QUEST_DEFINITIONS:
            if self._check_quest(qd['id']):
                newly.append(qd)
        from gene_config import ACHIEVEMENTS
        for ach in ACHIEVEMENTS:
            aid = ach['id']
            if aid in self.achievements:
                continue
            atype = ach['type']
            if atype == 'total_wins':
                p = self.max_stage
            elif atype == 'boss_kills':
                p = self.enemy_kills.get('__boss__', 0)
            elif atype == 'max_stage':
                p = self.max_stage
            elif atype == 'no_loss_count':
                p = len(self.no_loss_stages)
            elif atype == 'breed_count':
                p = self.breed_counter
            elif atype == 'have_cards':
                p = len(self.cards)
            elif atype == 'bloodline_collect':
                bls = set(getattr(c, 'bloodline', None) for c in self.cards if c.is_alive)
                bls.discard(None)
                p = len(bls)
            elif atype == 'star_count':
                p = sum(1 for c in self.cards if getattr(c, 'star', 1) >= 5)
            elif atype == 'chip_equip':
                p = 1 if any(c.chips for c in self.cards) else 0
            elif atype == 'training_complete':
                p = sum(1 for c in self.cards if len(getattr(c, 'training', {})) >= 4 and c.is_alive)
            elif atype == 'module_collect':
                from gene_config import MODULE_POOLS
                p = sum(1 for mid, v in MODULE_POOLS.items() if v['level'] == 3 and self.module_inventory.get(mid, 0) > 0)
            elif atype == 'challenge_score':
                p = max(self.challenge_scores.values(), key=lambda x: x.get('points', 0)).get('points', 0)
            elif atype == 'hidden':
                continue
            else:
                p = 0
            if p >= ach['target']:
                self.achievements[aid] = True
                newly_ach = next((a for a in ACHIEVEMENTS if a['id'] == aid), None)
                if newly_ach:
                    newly.append({'id': aid, 'title': f'[成就] {newly_ach["name"]}', 'rewards': [{'type': 'achievement', 'ach_id': aid}]})
        return newly

    def claim_quest(self, qid):
        if qid not in self.quest_completed or qid in self.quest_claimed:
            return None, "任务未完成或已领取"
        qd = next(q for q in QUEST_DEFINITIONS if q['id'] == qid)
        reward_msgs = []
        for r in qd['rewards']:
            try:
                if r['type'] == 'gacha_currency':
                    self.gacha_currency += r['amount']
                    reward_msgs.append(f"基因密钥 +{r['amount']}")
                elif r['type'] == 'battle_materials':
                    self.battle_materials += r['amount']
                    reward_msgs.append(f"战斗材料 +{r['amount']}")
                elif r['type'] == 'achievement':
                    ach_id = r.get('ach_id')
                    if ach_id:
                        self._grant_achievement_reward(ach_id)
                        reward_msgs.append("成就奖励已发放!")
                elif r['type'] == 'card_with_skills':
                    gq = r.get('genome_quality', 0.0)
                    card = self._create_skill_reward_card(r.get('skill_names', []), quality=gq)
                    if card:
                        reward_msgs.append(f"新卡牌 [{card.name}] 技能: {', '.join(card.skills)}")
            except Exception as e:
                reward_msgs.append(f"奖励发放异常: {e}")
        self.quest_claimed.add(qid)
        self.quest_completed.discard(qid)
        return reward_msgs, None

    def _create_skill_reward_card(self, skill_names, quality=0.0):
        name = f"奖励体{Card.card_count}"
        card = Card(name, gender=random.choice(['male','female']))
        if not card.is_alive:
            return None
        card.traits = self._compute_reward_traits(quality)
        for gene_name in SKILL_GENES:
            tmpl = GENE_TEMPLATES.get(gene_name, {})
            desired = tmpl.get('skill_name') in skill_names
            if gene_name in card.genes:
                card.genes[gene_name]['allele1']['is_dominant'] = desired
                card.genes[gene_name]['allele2']['is_dominant'] = desired
        for gene_name in SKILL_GENES:
            gene_data = card.genes.get(gene_name)
            if not gene_data:
                continue
            is_dom = gene_data['allele1']['is_dominant']
            chr_id = gene_data.get('chromosome', 'chr1')
            if chr_id == 'chrY':
                chr_id = 'chrX'
            homologs = card.chromosomes.get(chr_id, [])
            for h in homologs:
                dom = h.get('is_dominant')
                if dom and gene_name in dom:
                    dom[gene_name] = is_dom
        chrG_gene_names = CHROMOSOME_LAYOUT.get('chrG', {}).get('genes', [])
        if chrG_gene_names:
            from gene_config import CHROMOSOME_LENGTH as _GL
            regs = GENE_REGIONS.get('chrG', [])
            parts = []
            dom_map = {}
            for gname, gs, ge in regs:
                tmpl = GENE_TEMPLATES.get(gname, {})
                desired = tmpl.get('skill_name') in skill_names
                seq = tmpl.get('sequence', 'AAAAAAAAAAAA')
                if not desired:
                    seq = tmpl.get('recessive_sequence', 'a' * (ge - gs))
                seq = (seq or '')[:ge-gs].ljust(ge-gs, 'a')
                parts.append(seq)
                dom_map[gname] = desired
            if any(dom_map.values()):
                genome = ''.join(parts)
                target_len = _GL.get('chrG', 200)
                if len(genome) < target_len:
                    genome += 'a' * (target_len - len(genome))
                else:
                    genome = genome[:target_len]
                card.chromosomes['chrG'] = [
                    {'genome': genome, 'is_dominant': dict(dom_map)},
                    {'genome': genome, 'is_dominant': dict(dom_map)},
                ]
                card._rebuild_genes()
        card.skills = card.get_skills()
        self.cards.append(card)
        return card

    def _compute_reward_traits(self, quality):
        q = max(0.0, min(0.95, quality))
        traits = {
            'attack': int(12 * (1 + q) ** 9),
            'health': int(60 * (1 + q) ** 6),
            'defense': int(5 * (1 + q) ** 6),
            'speed': int(8 * (1 + q) ** 5),
            'stamina': int(20 * (1 + q) ** 5),
            'lifespan': int(50 * (1 + q) ** 4),
            'critical_rate': int(3 + q * 15),
            'dodge_rate': int(2 + q * 10),
        }
        return traits

    def save_game(self):
        try:
            save_data = {
                'cards': [card.to_dict() for card in self.cards],
                'tech_tree': self.tech_tree,
                'breed_speed_multiplier': self.breed_speed_multiplier,
                'auto_breeding': self.auto_breeding,
                'unlocked_stages': self.unlocked_stages,
                'max_stage': self.max_stage,
                'card_count': Card.card_count,
                'gene_library': getattr(self, 'gene_library', {}),
                'gacha_currency': self.gacha_currency,
                'pity_counters': self.pity_counters,
                'battle_materials': self.battle_materials,
                'no_loss_stages': list(self.no_loss_stages),
                'quest_progress': self.quest_progress,
                'quest_completed': list(self.quest_completed),
                'quest_claimed': list(self.quest_claimed),
                'enemy_kills': self.enemy_kills,
                'breed_counter': self.breed_counter,
                'save_version': self.SAVE_VERSION,
                'gene_essence': self.gene_essence,
                'chip_inventory': self.chip_inventory,
                'module_inventory': self.module_inventory,
                'challenge_scores': self.challenge_scores,
                'achievements': self.achievements,
                'equipment_inventory': self.equipment_inventory,
                'base_buildings': self.base_buildings,
            }
            tmp = self.SAVE_FILE + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            os.replace(tmp, self.SAVE_FILE)
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def load_game(self):
        try:
            if not os.path.exists(self.SAVE_FILE):
                return False
            with open(self.SAVE_FILE, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            self.cards = [Card.from_dict(card_data) for card_data in save_data.get('cards', [])]
            old_tree = save_data.get('tech_tree', {})
            self.tech_tree = self._copy_tech_tree()
            for tech_name, tech_data in self.tech_tree.items():
                old_data = old_tree.get(tech_name)
                if old_data:
                    tech_data['level'] = old_data.get('level', 0)
                    tech_data['unlocked'] = old_data.get('unlocked', False)
            self.breed_speed_multiplier = save_data.get('breed_speed_multiplier', 1.0)
            self.auto_breeding = save_data.get('auto_breeding', False)
            self.gene_library = save_data.get('gene_library', {})
            self.unlocked_stages = save_data.get('unlocked_stages', [1])
            self.max_stage = save_data.get('max_stage', 1)
            from battle_config import STAGES as _all_s
            _numeric = [s for s in self.unlocked_stages if isinstance(s, (int, float)) and not isinstance(s, bool)]
            max_in_save = max(_numeric) if _numeric else 1
            for _k in _all_s:
                if _k > max_in_save and _k <= max_in_save + 1 and _k not in self.unlocked_stages:
                    self.unlocked_stages.append(_k)
                    self.max_stage = max(self.max_stage, _k)
            self.gacha_currency = save_data.get('gacha_currency', 0)
            loaded_pity = save_data.get('pity_counters', {})
            self.pity_counters = {pid: loaded_pity.get(pid, 0) for pid in self.GACHA_POOLS}
            self.battle_materials = save_data.get('battle_materials', 0)
            self.no_loss_stages = set(save_data.get('no_loss_stages', []))
            self.quest_progress = save_data.get('quest_progress', {})
            self.quest_completed = set(save_data.get('quest_completed', []))
            self.quest_claimed = set(save_data.get('quest_claimed', []))
            self.enemy_kills = save_data.get('enemy_kills', {})
            self.breed_counter = save_data.get('breed_counter', 0)
            self.gene_essence = save_data.get('gene_essence', 0)
            self.chip_inventory = save_data.get('chip_inventory', {})
            self.module_inventory = save_data.get('module_inventory', {})
            self.challenge_scores = save_data.get('challenge_scores', {})
            self.achievements = save_data.get('achievements', {})
            self.equipment_inventory = save_data.get('equipment_inventory', {})
            self.base_buildings = save_data.get('base_buildings', {})
            Card.card_count = save_data.get('card_count', len(self.cards))
            
            old_ver = save_data.get('save_version', 0)
            if old_ver < self.SAVE_VERSION:
                existing_names = {c.name for c in self.cards}
                from tech_config import INITIAL_CARDS_CONFIG
                for entry in INITIAL_CARDS_CONFIG.get('cards', []):
                    if entry['name'] not in existing_names:
                        card = Card(entry['name'], entry.get('gender'))
                        self.cards.append(card)
            
            self._sync_tech_effects()
            for card in self.cards:
                if card.is_alive:
                    card.traits = card.calculate_traits()
            return True
        except Exception as e:
            print(f"加载失败: {e}")
            return False


class BattleCard:
    def __init__(self, card, position=0, grid_size=3):
        self.card = card
        self.id = card.id
        self.name = card.name
        self.gender = card.gender
        self.max_health = card.traits.get('health', 50)
        self.current_health = self.max_health
        self.attack = card.traits.get('attack', 10)
        self.defense = card.traits.get('defense', 5)
        self.speed = card.traits.get('speed', 10)
        self.critical_rate = card.traits.get('critical_rate', 10)
        self.dodge_rate = card.traits.get('dodge_rate', 10)
        self.skills = card.skills.copy()
        
        self.action_bar = 0
        self.status_effects = {}
        self.shield = 0
        self.is_alive = True
        self.is_player = True
        self.total_damage_dealt = 0
        self.position = position
        self.grid_size = grid_size
        self.row = position // grid_size
        self.col = position % grid_size
        self.passive_skills = card.passive_skills.copy() if hasattr(card, 'passive_skills') else {}
        self.passive_abilities = []
        self.reflex_bound_skill = getattr(card, 'reflex_bound_skill', None)
    
    def take_damage(self, damage, attacker=None):
        if self.has_status('evade'):
            self.remove_status('evade')
            return 0
        
        if self.has_status('invisible'):
            self.remove_status('invisible')
            return 0
        
        if self.has_status('curse'):
            dmg_mult = self.status_effects['curse'].get('damage_mult', 1.5)
            damage = int(damage * dmg_mult)
        
        effective_defense = self.defense
        if self.has_status('defense_buff'):
            buff_value = self.status_effects['defense_buff'].get('value', 0)
            effective_defense = int(self.defense * (1 + buff_value / 100))
        actual_damage = max(damage - effective_defense, BATTLE_CONFIG['min_damage'])
        if self.shield > 0:
            shield_damage = min(self.shield, actual_damage)
            self.shield -= shield_damage
            actual_damage -= shield_damage
        
        if actual_damage > 0:
            self.current_health -= actual_damage
            if self.current_health <= 0:
                self.current_health = 0
                self.is_alive = False
        
        if actual_damage > 0 and attacker and not getattr(attacker, '_reflecting', False):
            attacker.total_damage_dealt += actual_damage
            reflect_pct = self.passive_skills.get('荆棘', 0)
            if reflect_pct > 0 and attacker.is_alive:
                reflect_dmg = max(1, int(actual_damage * reflect_pct / 100))
                attacker._reflecting = True
                attacker.take_damage(reflect_dmg)
                attacker._reflecting = False
        
        return actual_damage
    
    def heal(self, amount):
        self.current_health = min(self.current_health + amount, self.max_health)
    
    def add_status(self, status_name, turns, attacker_attack=0):
        if getattr(self, 'immune_to_debuffs', False):
            return
        if status_name == 'poison':
            if status_name not in self.status_effects:
                self.status_effects[status_name] = {'turns': turns, 'stacks': 1, 'attacker_attack': attacker_attack}
            else:
                self.status_effects[status_name]['stacks'] += 1
                self.status_effects[status_name]['turns'] = turns
                self.status_effects[status_name]['attacker_attack'] = max(
                    self.status_effects[status_name]['attacker_attack'], attacker_attack
                )
        elif status_name not in self.status_effects:
            self.status_effects[status_name] = {'turns': turns}
        else:
            self.status_effects[status_name]['turns'] = max(
                self.status_effects[status_name]['turns'], turns
            )
    
    def remove_status(self, status_name):
        if status_name in self.status_effects:
            del self.status_effects[status_name]
    
    def has_status(self, status_name):
        return status_name in self.status_effects
    
    def update_status(self):
        se = self.status_effects
        dead = []
        for s, d in se.items():
            if s in ('poison', 'burn', 'bleed'):
                continue
            d['turns'] = d.get('turns', 0) - 1
            if d['turns'] <= 0:
                dead.append(s)
        for s in dead:
            del se[s]
    
    def can_act(self):
        if not self.is_alive:
            return False
        se = self.status_effects
        return 'paralyze' not in se and 'sleep' not in se and 'freeze' not in se


class Enemy:
    _counter = 0

    def __init__(self, enemy_data, scale=1.0, position=0, grid_size=3):
        Enemy._counter += 1
        self.id = f'enemy_{Enemy._counter}'
        self.name = enemy_data['name']
        self.max_health = int(enemy_data['health'] * scale)
        self.current_health = self.max_health
        self.attack = int(enemy_data['attack'] * scale)
        self.defense = int(enemy_data['defense'] * scale)
        self.speed = int(enemy_data['speed'] * scale)
        self.skills = enemy_data.get('skills', [])
        
        self.action_bar = 0
        self.status_effects = {}
        self.shield = 0
        self.is_alive = True
        self.is_player = False
        
        self.template_key = ''
        for tid, tmpl in ENEMY_TEMPLATES.items():
            if tmpl['name'] == self.name:
                self.template_key = tid
                break
        self._traits = []
        self.total_damage_dealt = 0
        self.is_overlord = enemy_data.get('is_overlord', False)
        self.grid_size = grid_size
        self.width = enemy_data.get('width', 2 if self.is_overlord else 1)
        self.height = enemy_data.get('height', 2 if self.is_overlord else 1)
        self.occupied_positions = []
        _max_pos = grid_size * grid_size
        if self.width > 1 or self.height > 1:
            _valid_starts = []
            for p in range(_max_pos):
                r = p // grid_size
                c = p % grid_size
                if c + self.width <= grid_size and r + self.height <= grid_size:
                    _valid_starts.append(p)
            start = position if position in _valid_starts else (_valid_starts[0] if _valid_starts else 0)
            self.position = start
        else:
            self.position = position
        for h in range(self.height):
            for w in range(self.width):
                self.occupied_positions.append(self.position + w + h * grid_size)
        self.row = self.position // grid_size
        self.col = self.position % grid_size
        self.passive_skills = {}
        self.reflex_bound_skill = None
        _tmpl = None
        for _t in ENEMY_TEMPLATES.values():
            if _t['name'] == self.name:
                _tmpl = _t
                break
        if _tmpl is None and enemy_data.get('template'):
            for _t in ENEMY_TEMPLATES.values():
                if _t['name'] == enemy_data['template']:
                    _tmpl = _t
                    break
        self.purify_interval = enemy_data.get('purify_interval', _tmpl.get('purify_interval', 0) if _tmpl else 0)
        self.last_purify_time = 0.0
        self.purify_shield_expires = 0.0
        self.annihilate = enemy_data.get('annihilate', _tmpl.get('annihilate', False) if _tmpl else False)
        self.immune_to_debuffs = enemy_data.get('immune_to_debuffs', _tmpl.get('immune_to_debuffs', False) if _tmpl else False)
        self.passive_abilities = enemy_data.get('passive_abilities', [])
        if not self.passive_abilities and _tmpl:
            self.passive_abilities = _tmpl.get('passive_abilities', [])
        self._fortify_applied = False
        self._berserk_active = False
        self._original_attack = self.attack
        self._on_death_triggered = False
        from battle_config import ENEMY_PASSIVES as _EP
        for _pa_key in self.passive_abilities:
            _pdata = _EP.get(_pa_key)
            if _pdata and _pa_key == 'thorns_aura':
                _reflect_pct = int(_pdata['params'].get('reflect_pct', 0) * 100)
                self.passive_skills['荆棘'] = _reflect_pct
    
    def take_damage(self, damage, attacker=None):
        if self.has_status('evade'):
            self.remove_status('evade')
            return 0
        
        if self.has_status('invisible'):
            self.remove_status('invisible')
            return 0
        
        if self.has_status('curse'):
            dmg_mult = self.status_effects['curse'].get('damage_mult', 1.5)
            damage = int(damage * dmg_mult)
        
        if getattr(self, 'passive_abilities', None) and 'aoe_barrier' in self.passive_abilities:
            damage = int(damage * 0.5)
        
        effective_defense = self.defense
        if self.has_status('defense_buff'):
            buff_value = self.status_effects['defense_buff'].get('value', 0)
            effective_defense = int(self.defense * (1 + buff_value / 100))
        actual_damage = max(damage - effective_defense, BATTLE_CONFIG['min_damage'])
        if self.shield > 0:
            shield_damage = min(self.shield, actual_damage)
            self.shield -= shield_damage
            actual_damage -= shield_damage
        
        # guard_protocol: transfer 50% damage to the unit below
        if getattr(self, 'passive_abilities', None) and 'guard_protocol' in self.passive_abilities and actual_damage > 0:
            below_pos = self.position + self.grid_size * self.height
            if hasattr(self, '_enemies_ref'):
                for ally in self._enemies_ref:
                    if ally.is_alive and ally is not self and below_pos in ally.occupied_positions:
                        transfer = max(1, int(actual_damage * 0.5))
                        actual_damage -= transfer
                        ally.take_damage(transfer)
                        break
        
        if actual_damage > 0:
            self.current_health -= actual_damage
            if self.current_health <= 0:
                self.current_health = 0
                self.is_alive = False
        
        if actual_damage > 0 and attacker and not getattr(attacker, '_reflecting', False):
            attacker.total_damage_dealt += actual_damage
            reflect_pct = self.passive_skills.get('荆棘', 0)
            if reflect_pct > 0 and attacker.is_alive:
                reflect_dmg = max(1, int(actual_damage * reflect_pct / 100))
                attacker._reflecting = True
                attacker.take_damage(reflect_dmg)
                attacker._reflecting = False
        
        if self.annihilate and not self.is_alive and attacker and attacker.is_alive:
            attacker.is_alive = False
            attacker.current_health = 0
        
        return actual_damage
    
    def heal(self, amount):
        self.current_health = min(self.current_health + amount, self.max_health)
    
    def add_status(self, status_name, turns, attacker_attack=0):
        if getattr(self, 'immune_to_debuffs', False):
            return
        DEBUFFS = {'poison', 'sleep', 'paralyze', 'confuse'}
        if status_name in DEBUFFS and getattr(self, 'purify_shield_expires', 0.0) > time.time():
            return
        if status_name == 'poison':
            if status_name not in self.status_effects:
                self.status_effects[status_name] = {'turns': turns, 'stacks': 1, 'attacker_attack': attacker_attack}
            else:
                self.status_effects[status_name]['stacks'] += 1
                self.status_effects[status_name]['turns'] = turns
                self.status_effects[status_name]['attacker_attack'] = max(
                    self.status_effects[status_name]['attacker_attack'], attacker_attack
                )
        elif status_name not in self.status_effects:
            self.status_effects[status_name] = {'turns': turns}
        else:
            self.status_effects[status_name]['turns'] = max(
                self.status_effects[status_name]['turns'], turns
            )
    
    def remove_status(self, status_name):
        if status_name in self.status_effects:
            del self.status_effects[status_name]
    
    def has_status(self, status_name):
        return status_name in self.status_effects
    
    def update_status(self):
        se = self.status_effects
        dead = []
        for s, d in se.items():
            if s in ('poison', 'burn', 'bleed'):
                continue
            d['turns'] = d.get('turns', 0) - 1
            if d['turns'] <= 0:
                dead.append(s)
        for s in dead:
            del se[s]
    
    def can_act(self):
        if not self.is_alive:
            return False
        se = self.status_effects
        return 'paralyze' not in se and 'sleep' not in se and 'freeze' not in se


class BattleSystem:
    def __init__(self, player_grid, enemy_data_list, stage_num=1, skill_enhance_level=0, enemy_grid_size=None):
        self.marked_target = None
        self.grid_size = 3
        self.enemy_grid_size = enemy_grid_size if enemy_grid_size else (4 if stage_num > 60 else 3)
        self.player_team = [BattleCard(card, pos, self.grid_size) for pos, card in player_grid.items() if card.is_alive]
        self.skill_enhance_level = skill_enhance_level
        
        self.battle_log = []
        self.enemies = []
        _occupied = set()
        _max_pos = self.enemy_grid_size * self.enemy_grid_size
        for i, data in enumerate(enemy_data_list):
            pos = data.get('position', list(range(_max_pos))[i] if i < _max_pos else i)
            enemy = Enemy(data, position=pos, grid_size=self.enemy_grid_size)
            is_multi = enemy.width > 1 or enemy.height > 1
            if is_multi:
                for op in enemy.occupied_positions:
                    _occupied.add(op)
                self.enemies.append(enemy)
            else:
                while pos in _occupied and pos < _max_pos:
                    pos += 1
                if pos >= _max_pos:
                    self.add_log(f"【警告】{enemy.name} 无法放置到战场上（位置已满），已跳过")
                    continue
                enemy.position = pos
                enemy.row = pos // self.enemy_grid_size
                enemy.col = pos % self.enemy_grid_size
                self.enemies.append(enemy)
        
        for enemy in self.enemies:
            enemy._enemies_ref = self.enemies

        self.stage_num = stage_num
        if stage_num >= 50:
            self._assign_traits()
        self.is_running = False
        self.is_auto = False
        self.winner = None
        self.current_turn = 0
        self._all_units_cache = self.player_team + self.enemies
    
    def _rebuild_unit_cache(self):
        self._all_units_cache = self.player_team + self.enemies
        for enemy in self.enemies:
            enemy._enemies_ref = self.enemies

    def _assign_traits(self):
        import random
        from gene_config import ENEMY_TRAITS
        available = [tid for tid, t in ENEMY_TRAITS.items() if t.get('unlock', 0) <= self.stage_num]
        if not available:
            return
        trait_count = min(2, self.stage_num // 30)
        for enemy in self.enemies:
            if getattr(enemy, 'annihilate', False) or getattr(enemy, 'immune_to_debuffs', False):
                continue
            enemy._traits = []
            weights = [ENEMY_TRAITS[tid]['weight'] for tid in available]
            try:
                picked = random.choices(available, weights=weights, k=min(trait_count, len(available)))
            except ValueError:
                continue
            for tid in picked:
                td = ENEMY_TRAITS[tid]
                enemy._traits.append(tid)
                if td['type'] == 'stat':
                    if 'hp_pct' in td:
                        enemy.max_health = int(enemy.max_health * (1 + td['hp_pct']))
                        enemy.current_health = enemy.max_health
                    if 'atk_pct' in td:
                        enemy.attack = int(enemy.attack * (1 + td['atk_pct']))
                    if 'spd_pct' in td:
                        enemy.speed = int(enemy.speed * (1 + td['spd_pct']))
                elif td['type'] == 'entry' and 'shield_pct' in td:
                    enemy.shield = int(enemy.max_health * td['shield_pct'])
                elif td['type'] == 'entry' and 'atb_init' in td:
                    enemy.action_bar = BATTLE_CONFIG['action_bar_max'] * td['atb_init']
                elif td['type'] == 'immune':
                    enemy.immune_to_debuffs = True
                elif td['type'] == 'pierce':
                    enemy._pierce_pct = td['pct']
                elif td['type'] == 'reflect':
                    enemy.passive_skills['荆棘'] = int(td['pct'] * 100)
                elif td['type'] == 'lifesteal':
                    enemy._lifesteal_pct = td['pct']
    
    def add_log(self, message):
        self.battle_log.append(message)
    
    def get_all_units(self):
        return self._all_units_cache
    
    def get_active_units(self):
        return [unit for unit in self._all_units_cache if unit.is_alive and unit.can_act()]
    
    def update_action_bars_frame(self):
        for unit in self._all_units_cache:
            if not unit.is_alive:
                continue
            se = unit.status_effects
            if 'paralyze' in se or 'freeze' in se or 'sleep' in se:
                continue
            effective_speed = unit.speed
            sb = se.get('speed_buff')
            if sb:
                effective_speed = int(unit.speed * (1 + sb.get('value', 0) / 100))
            unit.action_bar += effective_speed / 12
    
    def get_next_unit(self):
        max_bar = BATTLE_CONFIG['action_bar_max']
        candidates = [u for u in self.get_all_units() if u.action_bar >= max_bar and u.can_act()]
        if not candidates:
            return None
        return max(candidates, key=lambda u: u.action_bar)
    
    def execute_turn(self, attacker, targets):
        if not attacker.can_act():
            return None
        
        if attacker.has_status('confuse'):
            all_units = [u for u in self.get_all_units() if u.is_alive and u is not attacker]
            if not all_units:
                return None
            confused_target = random.choice(all_units)
            base_damage = attacker.attack
            actual_damage = confused_target.take_damage(base_damage, attacker)
            self.add_log(f"【{attacker.name}】陷入混乱! 胡乱攻击了 {confused_target.name}，造成 {actual_damage} 伤害!")
            if not confused_target.is_alive:
                self.add_log(f"  → {confused_target.name} 死亡!")
            _annihilated = getattr(confused_target, 'annihilate', False) and not confused_target.is_alive and not attacker.is_alive
            if _annihilated:
                self.add_log(f"  ☠ {attacker.name} 被湮灭体拖入毁灭!")
            return {'type': 'confuse_attack', 'annihilated': _annihilated, 'annihilator_obj': confused_target if _annihilated else None, 'attacker': attacker.name, 'target': confused_target.name, 'damage': actual_damage, 'attacker_obj': attacker, 'target_obj': confused_target}
        
        if attacker.is_player:
            result = self.execute_player_turn(attacker, targets)
        else:
            result = self.execute_enemy_turn(attacker)
        
        if result:
            target_obj = result.get('target_obj')
            if target_obj and getattr(target_obj, 'annihilate', False) and not target_obj.is_alive and attacker and not attacker.is_alive:
                self.add_log(f"  ☠ {attacker.name} 被湮灭体拖入毁灭!")
                result['annihilated'] = True
                result['annihilator_obj'] = target_obj
        
        if (result and '条件反射' in attacker.passive_skills
                and attacker.reflex_bound_skill
                and not getattr(attacker, '_is_reflex_cast', False)
                and attacker.is_alive):
            attacker._is_reflex_cast = True
            if attacker.is_player:
                reflex_target = self._select_front_target(targets, attacker)
            else:
                reflex_target = self._select_front_target(self.player_team, attacker)
            if reflex_target:
                reflex_result = self.execute_skill(attacker, reflex_target, force_skill=attacker.reflex_bound_skill)
                if reflex_result:
                    result['reflex_result'] = reflex_result
                    result['reflex_skill'] = attacker.reflex_bound_skill
                    reflex_tgt = reflex_result.get('target_obj')
                    if reflex_tgt and getattr(reflex_tgt, 'annihilate', False) and not reflex_tgt.is_alive and not attacker.is_alive:
                        self.add_log(f"  ☠ {attacker.name} 被湮灭体拖入毁灭!")
                        reflex_result['annihilated'] = True
                        reflex_result['annihilator_obj'] = reflex_tgt
            attacker._is_reflex_cast = False
        
        return result
    
    def _select_front_target(self, units, attacker=None):
        alive = [u for u in units if u.is_alive]
        if not alive:
            return None
        if self.marked_target and self.marked_target in alive:
            return self.marked_target
        gs = alive[0].grid_size if alive else self.grid_size
        if attacker and attacker.passive_skills.get('暗杀者'):
            for row in range(gs - 1, -1, -1):
                back = [u for u in alive if u.row == row]
                if back:
                    return random.choice(back)
        if alive[0].is_player:
            cols = list(range(gs - 1, -1, -1))
        else:
            cols = list(range(gs))
        for col in cols:
            front = [u for u in alive if u.col == col]
            if front:
                return random.choice(front)
        return random.choice(alive)

    def execute_player_turn(self, attacker, targets):
        target = self._select_front_target(targets, attacker)
        if not target:
            return None
        
        if self._should_use_skill(attacker):
            return self.execute_skill(attacker, target)
        
        base_damage = attacker.attack
        if attacker.has_status('attack_buff'):
            buff_value = attacker.status_effects['attack_buff'].get('value', 20)
            base_damage = int(base_damage * (1 + buff_value / 100))
        
        if attacker.passive_skills.get('暗杀者'):
            base_damage = int(base_damage * (1 + target.row * 0.2))
        
        is_critical = random.random() < ((attacker.critical_rate + target.row * 10) / 100 if attacker.passive_skills.get('暗杀者') else (attacker.critical_rate / 100))
        
        if is_critical:
            base_damage = int(base_damage * BATTLE_CONFIG['critical_damage'])
            self.add_log(f"【{attacker.name}】暴击! 攻击 {target.name}，造成 {base_damage} 点伤害!")
        else:
            self.add_log(f"【{attacker.name}】发起攻击，攻击 {target.name}，造成 {base_damage} 点伤害!")
        
        actual_damage = target.take_damage(base_damage, attacker)
        
        if not target.is_alive:
            self.add_log(f"  → {target.name} 死亡!")
        
        return {'type': 'attack', 'attacker': attacker.name, 'target': target.name, 'damage': actual_damage, 'critical': is_critical, 'attacker_obj': attacker, 'target_obj': target}
    
    def execute_enemy_turn(self, attacker):
        is_boss = getattr(attacker, 'width', 1) > 1 or getattr(attacker, 'height', 1) > 1
        if is_boss:
            alive_targets = [p for p in self.player_team if p.is_alive]
            if not alive_targets:
                return None
            if self._should_use_skill(attacker):
                return self.execute_skill(attacker, alive_targets[0])
            base_damage = attacker.attack
            if attacker.has_status('attack_buff'):
                buff_value = attacker.status_effects['attack_buff'].get('value', 20)
                base_damage = int(base_damage * (1 + buff_value / 100))
            is_critical = random.random() < BATTLE_CONFIG['critical_rate_base']
            if is_critical:
                base_damage = int(base_damage * BATTLE_CONFIG['critical_damage'])
            self.add_log(f"【敌方 {attacker.name}】发起全体攻击!{' 暴击!' if is_critical else ''}")
            for target in alive_targets:
                dmg = target.take_damage(base_damage, attacker)
                self.add_log(f"  → {target.name} 受到 {dmg} 点伤害{' 死亡!' if not target.is_alive else ''}")
            return {'type': 'aoe_attack', 'attacker': attacker.name, 'targets': [t.name for t in alive_targets], 'damage': base_damage, 'critical': is_critical, 'attacker_obj': attacker}

        if getattr(attacker, 'passive_abilities', None) and 'focus_weak' in attacker.passive_abilities:
            alive_targets = [p for p in self.player_team if p.is_alive]
            target = min(alive_targets, key=lambda p: p.current_health) if alive_targets else None
        else:
            target = self._select_front_target(self.player_team, attacker)
        if not target:
            return None
        
        if self._should_use_skill(attacker):
            return self.execute_skill(attacker, target)
        
        base_damage = attacker.attack
        if attacker.has_status('attack_buff'):
            buff_value = attacker.status_effects['attack_buff'].get('value', 20)
            base_damage = int(base_damage * (1 + buff_value / 100))
        
        if attacker.passive_skills.get('暗杀者'):
            base_damage = int(base_damage * (1 + target.row * 0.2))
        
        is_critical = random.random() < ((BATTLE_CONFIG['critical_rate_base'] + target.row * 0.1) if attacker.passive_skills.get('暗杀者') else BATTLE_CONFIG['critical_rate_base'])
        
        if is_critical:
            base_damage = int(base_damage * BATTLE_CONFIG['critical_damage'])
            self.add_log(f"【敌方 {attacker.name}】暴击! 攻击 {target.name}，造成 {base_damage} 点伤害!")
        else:
            self.add_log(f"【敌方 {attacker.name}】发起攻击，攻击 {target.name}，造成 {base_damage} 点伤害!")
        
        actual_damage = target.take_damage(base_damage, attacker)
        
        if not target.is_alive:
            self.add_log(f"  → {target.name} 死亡!")
        
        return {'type': 'attack', 'attacker': attacker.name, 'target': target.name, 'damage': actual_damage, 'critical': is_critical, 'attacker_obj': attacker, 'target_obj': target}
    
    def _skill_scale(self, base, attacker, scale_ratio=0.5):
        tech_mult = 1 + self.skill_enhance_level * 0.1
        return int((base + attacker.attack * scale_ratio) * tech_mult)

    def _apply_assassin_bonus(self, damage, attacker, target):
        if attacker.passive_skills.get('暗杀者'):
            return int(damage * (1 + target.row * 0.2))
        return damage

    def _should_use_skill(self, attacker):
        if attacker.has_status('guarantee_skill'):
            return bool(attacker.skills)
        return attacker.skills and random.random() < 0.5

    def _decrement_guarantee_skill(self, unit):
        if not unit.has_status('guarantee_skill'):
            return
        d = unit.status_effects['guarantee_skill']
        remaining = d.get('remaining', d.get('turns', 1)) - 1
        if remaining <= 0:
            unit.remove_status('guarantee_skill')
        else:
            d['remaining'] = remaining
            d['turns'] = remaining

    def execute_skill(self, attacker, target, force_skill=None):
        if force_skill:
            skill_name = force_skill
        elif not attacker.skills:
            return None
        else:
            skill_name = random.choice(attacker.skills)
        skill_effect = SKILL_EFFECTS.get(skill_name, {})
        
        if not skill_effect:
            return self.execute_player_turn(attacker, [target])
        
        skill_type = skill_effect.get('type', 'damage')
        is_enemy = not attacker.is_player
        name_prefix = "敌方 " if is_enemy else ""
        
        if skill_type == 'damage':
            damage = self._skill_scale(skill_effect.get('base_damage', 20), attacker, 0.6)
            damage = self._apply_assassin_bonus(damage, attacker, target)
            actual_damage = target.take_damage(damage, attacker)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，对 {target.name} 造成 {actual_damage} 点伤害!")
        
        elif skill_type == 'damage_poison':
            damage = self._skill_scale(skill_effect.get('base_damage', 10), attacker, 0.4)
            damage = self._apply_assassin_bonus(damage, attacker, target)
            actual_damage = target.take_damage(damage, attacker)
            turns = skill_effect.get('turns', 5)
            target.add_status('poison', turns, attacker.attack)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，造成 {actual_damage} 伤害，附加中毒效果!")
        
        elif skill_type == 'shield':
            shield_value = self._skill_scale(skill_effect.get('shield_value', 20), attacker, 0.4)
            attacker.shield += shield_value
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，获得 {shield_value} 点护盾!")
        
        elif skill_type == 'heal':
            heal_value = self._skill_scale(skill_effect.get('heal_value', 20), attacker, 0.3)
            attacker.heal(heal_value)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，恢复 {heal_value} 点生命!")
        
        elif skill_type == 'self_damage':
            damage = attacker.current_health // 2
            damage = self._apply_assassin_bonus(damage, attacker, target)
            actual_damage = target.take_damage(damage, attacker)
            self_dmg = attacker.current_health // 2
            attacker.take_damage(self_dmg)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，对 {target.name} 造成 {actual_damage} 伤害，自损 {self_dmg} 点!")
            if getattr(attacker, 'annihilate', False) and not attacker.is_alive and target.is_alive:
                target.is_alive = False
                target.current_health = 0
                self.add_log(f"  ☠ {target.name} 被湮灭体拖入毁灭!")
        
        elif skill_type == 'summon':
            team = self.player_team if attacker.is_player else self.enemies
            team_grid = self.grid_size if attacker.is_player else self.enemy_grid_size
            occupied = {u.position for u in team if u.is_alive}
            empty_pos = None
            _max_pos = team_grid * team_grid
            for pos in range(_max_pos):
                if pos not in occupied:
                    empty_pos = pos
                    break
            if empty_pos is not None:
                dummy = type('', (), {})()
                dummy.id = f"summon_{len(self.get_all_units())}_{random.randint(1000,9999)}"
                dummy.name = f"{attacker.name}的使者"
                dummy.gender = 'male'
                dummy.traits = {
                    'health': attacker.max_health // 2,
                    'attack': attacker.attack * 3 // 5,
                    'defense': attacker.defense // 2,
                    'speed': max(attacker.speed, 5),
                    'critical_rate': 5,
                    'dodge_rate': 5,
                }
                dummy.skills = []
                dummy.passive_skills = {}
                minion = BattleCard(dummy, empty_pos, grid_size=team_grid)
                minion._summon_turns = 3
                minion.is_player = attacker.is_player
                team.append(minion)
                self._rebuild_unit_cache()
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，召唤了使者!")
                return {'type': 'skill', 'skill': skill_name, 'attacker': attacker.name, 'target': attacker.name,
                        'attacker_obj': attacker, 'target_obj': attacker, 'summon': minion}
            else:
                damage = self._skill_scale(20, attacker, 0.3)
                actual_damage = target.take_damage(damage, attacker)
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，但没有空位，造成 {actual_damage} 点伤害!")
        
        elif skill_type == 'sleep':
            turns = skill_effect.get('turns', 2)
            target.add_status('sleep', turns)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，{target.name} 陷入睡眠!")
        
        elif skill_type == 'paralyze':
            turns = skill_effect.get('turns', 2)
            target.add_status('paralyze', turns)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，{target.name} 被麻痹!")
        
        elif skill_type == 'confuse':
            turns = skill_effect.get('turns', 2)
            target.add_status('confuse', turns)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，{target.name} 陷入混乱!")
        
        elif skill_type == 'invisible':
            turns = skill_effect.get('turns', 2)
            attacker.add_status('invisible', turns)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，进入隐身状态!")
        
        elif skill_type == 'evade':
            turns = skill_effect.get('turns', 1)
            attacker.add_status('evade', turns)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，获得闪避状态!")
        
        elif skill_type == 'absorb':
            base_damage = skill_effect.get('damage', 15)
            base_heal = skill_effect.get('heal', 15)
            damage = self._skill_scale(base_damage, attacker, 0.4)
            damage = self._apply_assassin_bonus(damage, attacker, target)
            heal_val = self._skill_scale(base_heal, attacker, 0.3)
            actual_damage = target.take_damage(damage, attacker)
            attacker.heal(heal_val)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，造成 {actual_damage} 伤害，吸收 {heal_val} 点生命!")
        
        elif skill_type == 'buff':
            buff_value = skill_effect.get('buff_value', 20)
            turns = skill_effect.get('turns', 3)
            attacker.add_status('attack_buff', turns)
            attacker.status_effects['attack_buff']['value'] = buff_value
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，攻击力提升 {buff_value}%!")

        elif skill_type == 'rearrange':
            units = self.enemies if not is_enemy else self.player_team
            target_grid = self.enemy_grid_size if not is_enemy else self.grid_size
            alive = [u for u in units if u.is_alive]
            overlords = [u for u in alive if getattr(u, 'width', 1) > 1 or getattr(u, 'height', 1) > 1]
            small = [u for u in alive if getattr(u, 'width', 1) == 1 and getattr(u, 'height', 1) == 1]
            if len(small) >= 2:
                occupied = set()
                for o in overlords:
                    for p in getattr(o, 'occupied_positions', [o.position]):
                        occupied.add(p)
                _max_pos = target_grid * target_grid
                free = [p for p in range(_max_pos) if p not in occupied]
                if len(free) >= len(small):
                    random.shuffle(free)
                    for u, new_pos in zip(small, free[:len(small)]):
                        u.position = new_pos
                        u.row = new_pos // target_grid
                        u.col = new_pos % target_grid
                    self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，打乱了对方阵型!")
                else:
                    self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，但空间不足，未能扰乱阵型!")
            else:
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，但可移动目标不足，未能扰乱阵型!")

        elif skill_type == 'surge':
            turns = skill_effect.get('turns', 5)
            attacker.add_status('guarantee_skill', turns)
            attacker.status_effects['guarantee_skill']['remaining'] = turns
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，接下来 {turns} 次行动必定释放技能!")

        elif skill_type == 'heal_team':
            team = self.player_team if attacker.is_player else self.enemies
            alive = [u for u in team if u.is_alive]
            targets_count = skill_effect.get('targets', 3)
            targets_heal = random.sample(alive, min(targets_count, len(alive)))
            heal_val = self._skill_scale(skill_effect.get('base_heal', 25), attacker, 0.4)
            healed_ids = []
            for t in targets_heal:
                t.heal(heal_val)
                self.add_log(f"  → {t.name} 恢复 {heal_val} 点生命!")
                healed_ids.append(t.id if hasattr(t, 'id') else id(t))
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，恢复 {len(targets_heal)} 名队友 {heal_val} 点生命!")
            return {'type': 'skill', 'skill': skill_name, 'attacker': attacker.name, 'target': attacker.name,
                    'attacker_obj': attacker, 'target_obj': attacker, 'healed_units': healed_ids, 'heal_amount': heal_val}

        elif skill_type == 'freeze':
            turns = skill_effect.get('turns', 1)
            target.add_status('freeze', turns)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，{target.name} 被冻结!")

        elif skill_type == 'curse':
            turns = skill_effect.get('turns', 3)
            target.add_status('curse', turns)
            dmg_mult = skill_effect.get('damage_mult', 1.5)
            target.status_effects['curse']['damage_mult'] = dmg_mult
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，{target.name} 受到诅咒，伤害加深!")

        elif skill_type == 'burn':
            turns = skill_effect.get('turns', 3)
            target.add_status('burn', turns)
            max_hp_pct = skill_effect.get('max_hp_pct', 0.15)
            target.status_effects['burn']['max_hp_pct'] = max_hp_pct
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，{target.name} 被灼烧!")

        elif skill_type == 'execute':
            hp_threshold = skill_effect.get('hp_threshold', 0.25)
            if target.current_health / target.max_health <= hp_threshold:
                execute_damage = target.current_health
                target.take_damage(execute_damage, attacker)
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，处决了 {target.name}!")
            else:
                base_damage = self._skill_scale(skill_effect.get('base_damage', 60), attacker, 0.5)
                base_damage = self._apply_assassin_bonus(base_damage, attacker, target)
                actual_damage = target.take_damage(base_damage, attacker)
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，对 {target.name} 造成 {actual_damage} 点伤害!")

        elif skill_type == 'aoe_poison':
            targets_count = skill_effect.get('targets', 3)
            team = self.player_team if is_enemy else self.enemies
            alive = [u for u in team if u.is_alive]
            poison_targets = random.sample(alive, min(targets_count, len(alive)))
            base_damage = skill_effect.get('base_damage', 8)
            turns = skill_effect.get('turns', 4)
            for t in poison_targets:
                damage = self._skill_scale(base_damage, attacker, 0.3)
                damage = self._apply_assassin_bonus(damage, attacker, t)
                actual_damage = t.take_damage(damage, attacker)
                t.add_status('poison', turns, attacker.attack)
                self.add_log(f"  → {t.name} 受到 {actual_damage} 伤害并中毒!")
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，毒雾扩散!")

        elif skill_type == 'rewind':
            heal_pct = skill_effect.get('heal_pct', 0.5)
            heal_value = int(attacker.max_health * heal_pct)
            attacker.heal(heal_value)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，恢复 {heal_value} 点生命!")

        elif skill_type == 'revive':
            if not attacker.is_alive:
                heal_pct = skill_effect.get('heal_pct', 0.3)
                attacker.current_health = int(attacker.max_health * heal_pct)
                attacker.is_alive = True
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，亡灵复苏!")

        elif skill_type == 'resurrect':
            team = self.enemies if is_enemy else self.player_team
            dead = [u for u in team if not u.is_alive]
            if dead:
                heal_pct = skill_effect.get('heal_pct', 0.5)
                target = random.choice(dead)
                target.current_health = int(target.max_health * heal_pct)
                target.is_alive = True
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，{target.name}复活!")
            else:
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，但没有阵亡的友军!")

        elif skill_type == 'sacrifice_heal':
            hp_pct = skill_effect.get('hp_pct', 0.3)
            heal_pct = skill_effect.get('heal_pct', 0.5)
            self_dmg = max(1, int(attacker.max_health * hp_pct))
            attacker.take_damage(self_dmg)
            team = self.enemies if is_enemy else self.player_team
            alive = [u for u in team if u.is_alive]
            for ally in alive:
                heal_value = self._skill_scale(skill_effect.get('base_heal', 20), attacker, heal_pct)
                ally.heal(heal_value)
                self.add_log(f"  → {ally.name} 恢复 {heal_value} 点生命!")
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，自损 {self_dmg} 治疗友军!")

        elif skill_type == 'missing_hp_damage':
            base_damage = self._skill_scale(skill_effect.get('base_damage', 15), attacker, 0.6)
            base_damage = self._apply_assassin_bonus(base_damage, attacker, target)
            missing = target.max_health - target.current_health
            ratio = skill_effect.get('missing_hp_ratio', 0.3)
            bonus = int(missing * ratio)
            total = base_damage + bonus
            actual_damage = target.take_damage(total, attacker)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，对 {target.name} 造成 {actual_damage} 伤害!(基础{base_damage}+已损{bonus})")
            if not target.is_alive:
                self.add_log(f"  → {target.name} 死亡!")

        elif skill_type == 'cleanse_damage':
            debuffs = ['poison', 'burn', 'bleed', 'curse', 'paralyze', 'sleep', 'freeze', 'confuse']
            removed = 0
            for db in debuffs:
                if attacker.has_status(db):
                    attacker.remove_status(db)
                    removed += 1
            base_damage = self._skill_scale(skill_effect.get('base_damage', 18), attacker, 0.5)
            bonus_per = skill_effect.get('bonus_per_debuff', 8)
            total = base_damage + removed * bonus_per
            actual_damage = target.take_damage(total, attacker)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，净化{removed}个效果，对 {target.name} 造成 {actual_damage} 伤害!")
            if not target.is_alive:
                self.add_log(f"  → {target.name} 死亡!")

        elif skill_type == 'blood_plague':
            team = self.enemies if is_enemy else self.player_team
            alive = [u for u in team if u.is_alive]
            if not alive:
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，但没有目标!")
            else:
                base_damage = self._skill_scale(skill_effect.get('base_damage', 12), attacker, 0.4)
                bleed_turns = skill_effect.get('bleed_turns', 3)
                poison_turns = skill_effect.get('poison_turns', 3)
                for t in alive:
                    dmg = self._apply_assassin_bonus(base_damage, attacker, t)
                    actual = t.take_damage(dmg, attacker)
                    t.add_status('bleed', bleed_turns, attacker.attack)
                    t.add_status('poison', poison_turns, attacker.attack)
                    self.add_log(f"  → {t.name} 受到 {actual} 伤害，附加流血和中毒!")
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，血之疫病蔓延!")

        # ==================== 抽卡限定技能 ====================
        elif skill_type == 'toxic_nova':
            team = self.enemies if is_enemy else self.player_team
            alive = [u for u in team if u.is_alive]
            if not alive:
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，但没有目标!")
            else:
                base_damage = self._skill_scale(skill_effect.get('base_damage', 15), attacker, 0.5)
                poison_stacks = skill_effect.get('poison_stacks', 3)
                turns = skill_effect.get('turns', 5)
                for t in alive:
                    damage = self._apply_assassin_bonus(base_damage, attacker, t)
                    se = t.status_effects
                    existing = se.get('poison')
                    if existing:
                        bonus = int(damage * 0.2 * existing.get('stacks', 1))
                        damage += bonus
                    actual_damage = t.take_damage(damage, attacker)
                    t.add_status('poison', turns, attacker.attack)
                    if existing:
                        se['poison']['stacks'] += poison_stacks
                    else:
                        se['poison']['stacks'] = poison_stacks
                    self.add_log(f"  → {t.name} 受到 {actual_damage} 伤害，叠加{poison_stacks}层中毒!")
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，剧毒新星爆发!")

        elif skill_type == 'corrosive_touch':
            base_damage = self._skill_scale(skill_effect.get('base_damage', 35), attacker, 0.6)
            base_damage = self._apply_assassin_bonus(base_damage, attacker, target)
            def_reduce = skill_effect.get('def_reduce', 0.50)
            def_turns = skill_effect.get('def_turns', 3)
            poison_turns = skill_effect.get('poison_turns', 3)
            debuff_count = len([k for k in target.status_effects if k in ('poison','burn','bleed','freeze','curse','sleep','paralyze','confuse')])
            bonus = int(base_damage * 0.15 * debuff_count)
            total_damage = base_damage + bonus
            actual_damage = target.take_damage(total_damage, attacker)
            target.add_status('poison', poison_turns, attacker.attack)
            target.status_effects['curse'] = {'turns': def_turns, 'damage_mult': 1.0}
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，对 {target.name} 造成 {actual_damage} 伤害(debuff加成{bonus})，降低防御并附加中毒!")

        elif skill_type == 'inferno':
            team = self.enemies if is_enemy else self.player_team
            alive = [u for u in team if u.is_alive]
            if not alive:
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，但没有目标!")
            else:
                base_damage = self._skill_scale(skill_effect.get('base_damage', 25), attacker, 0.5)
                burn_turns = skill_effect.get('burn_turns', 5)
                for t in alive:
                    damage = self._apply_assassin_bonus(base_damage, attacker, t)
                    if t.has_status('burn'):
                        damage = int(damage * 1.3)
                    actual_damage = t.take_damage(damage, attacker)
                    t.add_status('burn', burn_turns)
                    t.status_effects['burn']['max_hp_pct'] = 0.15
                    self.add_log(f"  → {t.name} 受到 {actual_damage} 伤害，附加灼烧{burn_turns}回合!")
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，炼狱之火席卷战场!")

        elif skill_type == 'ember_revival':
            base_damage = self._skill_scale(skill_effect.get('base_damage', 40), attacker, 0.6)
            base_damage = self._apply_assassin_bonus(base_damage, attacker, target)
            has_burn = target.has_status('burn')
            if has_burn:
                bonus_pct = skill_effect.get('bonus_pct', 0.20)
                bonus_dmg = max(1, int(target.max_health * bonus_pct))
                base_damage += bonus_dmg
            actual_damage = target.take_damage(base_damage, attacker)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，对 {target.name} 造成 {actual_damage} 伤害{'（灼烧加成）' if has_burn else ''}!")
            if not target.is_alive:
                splash_pct = skill_effect.get('splash_pct', 0.50)
                team = self.enemies if is_enemy else self.player_team
                for other in team:
                    if other.is_alive and other is not target:
                        splash = max(1, int(actual_damage * splash_pct))
                        other.take_damage(splash, attacker)
                        other.add_status('burn', 3)
                        other.status_effects['burn']['max_hp_pct'] = 0.15
                        self.add_log(f"  → 溅射! {other.name} 受到 {splash} 伤害并灼烧!")
            elif has_burn:
                self.add_log(f"  → {target.name}的灼烧被引爆!")

        elif skill_type == 'permafrost':
            team = self.enemies if is_enemy else self.player_team
            alive = [u for u in team if u.is_alive]
            if not alive:
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，但没有目标!")
            else:
                base_damage = self._skill_scale(skill_effect.get('base_damage', 20), attacker, 0.4)
                freeze_turns = skill_effect.get('freeze_turns', 1)
                dmg_mult = skill_effect.get('frozen_dmg_mult', 1.5)
                for t in alive:
                    damage = self._apply_assassin_bonus(base_damage, attacker, t)
                    if t.has_status('freeze'):
                        damage = int(damage * dmg_mult)
                    actual_damage = t.take_damage(damage, attacker)
                    t.add_status('freeze', freeze_turns)
                    self.add_log(f"  → {t.name} 受到 {actual_damage} 伤害，被冻结!")
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，永冻领域展开!")

        elif skill_type == 'absolute_zero':
            base_damage = self._skill_scale(skill_effect.get('base_damage', 55), attacker, 0.7)
            base_damage = self._apply_assassin_bonus(base_damage, attacker, target)
            is_frozen = target.has_status('freeze')
            if is_frozen:
                mult = skill_effect.get('frozen_mult', 3.0)
                base_damage = int(base_damage * mult)
                target.remove_status('freeze')
                self.add_log(f"  → 冻结碎裂! 伤害提升至{mult}倍!")
            freeze_turns = skill_effect.get('freeze_turns', 2)
            target.add_status('freeze', freeze_turns)
            actual_damage = target.take_damage(base_damage, attacker)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，对 {target.name} 造成 {actual_damage} 伤害!")

        elif skill_type == 'bloodthirst':
            base_damage = self._skill_scale(skill_effect.get('base_damage', 30), attacker, 0.6)
            base_damage = self._apply_assassin_bonus(base_damage, attacker, target)
            actual_damage = target.take_damage(base_damage, attacker)
            bleed_pct = skill_effect.get('bleed_pct', 0.10)
            bleed_turns = skill_effect.get('bleed_turns', 3)
            target.add_status('bleed', bleed_turns)
            target.status_effects['bleed']['max_hp_pct'] = bleed_pct
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，对 {target.name} 造成 {actual_damage} 伤害，附加流血!")
            if not target.is_alive:
                heal_amt = int(actual_damage * 0.5)
                attacker.heal(heal_amt)
                self.add_log(f"  → {attacker.name} 汲取了 {heal_amt} 点生命!")

        elif skill_type == 'crimson_storm':
            team = self.enemies if is_enemy else self.player_team
            alive = [u for u in team if u.is_alive]
            if not alive:
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，但没有目标!")
            else:
                base_damage = self._skill_scale(skill_effect.get('base_damage', 20), attacker, 0.5)
                bleed_mult = skill_effect.get('bleed_mult', 3.0)
                bleed_turns = skill_effect.get('bleed_turns', 2)
                bleed_pct = 0.10
                for t in alive:
                    damage = self._apply_assassin_bonus(base_damage, attacker, t)
                    if t.has_status('bleed'):
                        damage = int(damage * bleed_mult)
                    actual_damage = t.take_damage(damage, attacker)
                    t.add_status('bleed', bleed_turns)
                    t.status_effects['bleed']['max_hp_pct'] = bleed_pct
                    self.add_log(f"  → {t.name} 受到 {actual_damage} 伤害，血流不止!")
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，猩红风暴肆虐!")

        elif skill_type == 'omnibus_end':
            team = self.enemies if is_enemy else self.player_team
            alive = [u for u in team if u.is_alive]
            if not alive:
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，但没有目标!")
            else:
                base_damage = self._skill_scale(skill_effect.get('base_damage', 18), attacker, 0.5)
                per_debuff_pct = skill_effect.get('per_debuff_pct', 0.30)
                all_debuffs = {'poison','burn','bleed','freeze','curse','sleep','paralyze','confuse'}
                for t in alive:
                    damage = self._apply_assassin_bonus(base_damage, attacker, t)
                    debuffs_on_target = [k for k in t.status_effects if k in all_debuffs]
                    bonus_pct = len(debuffs_on_target) * per_debuff_pct
                    damage = int(damage * (1 + bonus_pct))
                    for k in debuffs_on_target:
                        del t.status_effects[k]
                    actual_damage = t.take_damage(damage, attacker)
                    self.add_log(f"  → {t.name} 受到 {actual_damage} 伤害({len(debuffs_on_target)}种debuff加成{bonus_pct*100:.0f}%)，所有负面效果被引爆!")
                self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，万象终结!")

        elif skill_type == 'status_resonance':
            base_damage = self._skill_scale(skill_effect.get('base_damage', 35), attacker, 0.6)
            base_damage = self._apply_assassin_bonus(base_damage, attacker, target)
            all_debuffs = {'poison','burn','bleed','freeze','curse','sleep','paralyze','confuse'}
            all_units = self._all_units_cache
            battlefield_types = set()
            for u in all_units:
                if u.is_alive:
                    for k in u.status_effects:
                        if k in all_debuffs:
                            battlefield_types.add(k)
            per_type_atk = skill_effect.get('per_type_atk', 0.10)
            atk_bonus = len(battlefield_types) * per_type_atk
            total_damage = int(base_damage * (1 + atk_bonus))
            actual_damage = target.take_damage(total_damage, attacker)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，利用{len(battlefield_types)}种负面效果共鸣，造成 {actual_damage} 伤害!")
            my_debuffs = [k for k in attacker.status_effects if k in all_debuffs]
            if my_debuffs:
                transfer = random.choice(my_debuffs)
                target.status_effects[transfer] = dict(attacker.status_effects[transfer])
                del attacker.status_effects[transfer]
                self.add_log(f"  → 将『{transfer}』转移给了 {target.name}!")

        # ==================== 多格单位技能 ====================
        elif skill_type == 'column_strike':
            team = self.enemies if is_enemy else self.player_team
            alive = [u for u in team if u.is_alive]
            target_col = target.col
            armor_pierce = skill_effect.get('armor_pierce', 0)
            for t in alive:
                if t.col == target_col:
                    base_damage = self._skill_scale(skill_effect.get('base_damage', 30), attacker, 0.6)
                    base_damage = self._apply_assassin_bonus(base_damage, attacker, t)
                    if armor_pierce > 0:
                        t.defense = int(t.defense * (1 - armor_pierce))
                    actual_damage = t.take_damage(base_damage, attacker)
                    if armor_pierce > 0:
                        t.defense = int(t.defense / (1 - armor_pierce))
                    self.add_log(f"  → {t.name} 受到 {actual_damage} 点纵列穿刺伤害!")
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，纵列穿刺!")

        elif skill_type == 'row_strike':
            team = self.enemies if is_enemy else self.player_team
            alive = [u for u in team if u.is_alive]
            target_row = target.row
            stun_turns = skill_effect.get('stun_turns', 1)
            for t in alive:
                if t.row == target_row:
                    base_damage = self._skill_scale(skill_effect.get('base_damage', 25), attacker, 0.5)
                    base_damage = self._apply_assassin_bonus(base_damage, attacker, t)
                    actual_damage = t.take_damage(base_damage, attacker)
                    t.add_status('paralyze', stun_turns)
                    self.add_log(f"  → {t.name} 受到 {actual_damage} 点横行震击伤害，被眩晕!")
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，横行震击!")

        elif skill_type == 'poison_column':
            team = self.enemies if is_enemy else self.player_team
            alive = [u for u in team if u.is_alive]
            target_col = target.col
            poison_turns = skill_effect.get('poison_turns', 3)
            poison_stacks = skill_effect.get('poison_stacks', 2)
            for t in alive:
                if t.col == target_col:
                    base_damage = self._skill_scale(skill_effect.get('base_damage', 15), attacker, 0.4)
                    base_damage = self._apply_assassin_bonus(base_damage, attacker, t)
                    actual_damage = t.take_damage(base_damage, attacker)
                    t.add_status('poison', poison_turns, attacker.attack)
                    se = t.status_effects.get('poison')
                    if se:
                        se['stacks'] = se.get('stacks', 1) + poison_stacks - 1
                    self.add_log(f"  → {t.name} 受到 {actual_damage} 点伤害，附加{poison_stacks}层中毒!")
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，剧毒吐息!")

        elif skill_type == 'war_cry':
            atk_bonus = skill_effect.get('atk_bonus', 0.30)
            turns = skill_effect.get('turns', 3)
            team = self.enemies if is_enemy else self.player_team
            for ally in team:
                if ally.is_alive:
                    ally.add_status('attack_buff', turns)
                    ally.status_effects['attack_buff']['value'] = int(atk_bonus * 100)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，全体友方攻击力提升{int(atk_bonus*100)}%!")

        elif skill_type == 'void_teleport':
            team = self.player_team
            alive = [u for u in team if u.is_alive]
            hp_pct = skill_effect.get('hp_pct', 0.15)
            target_grid = self.grid_size
            for p in alive:
                dmg = max(1, int(p.max_health * hp_pct))
                p.take_damage(dmg)
                self.add_log(f"  → {p.name} 受到 {dmg} 点虚空伤害!")
            positions = list(range(target_grid * target_grid))
            random.shuffle(positions)
            for p, new_pos in zip(alive, positions):
                p.position = new_pos
                p.row = new_pos // target_grid
                p.col = new_pos % target_grid
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，传送扰乱敌方阵型!")

        else:
            damage = attacker.attack
            damage = self._apply_assassin_bonus(damage, attacker, target)
            actual_damage = target.take_damage(damage, attacker)
            self.add_log(f"【{name_prefix}{attacker.name}】释放技能 [{skill_name}]，对 {target.name} 造成 {actual_damage} 点伤害!")
        
        if hasattr(target, 'is_alive') and not target.is_alive:
            self.add_log(f"  → {target.name} 死亡!")

        self._decrement_guarantee_skill(attacker)

        return {'type': 'skill', 'skill': skill_name, 'attacker': attacker.name, 'target': target.name, 'attacker_obj': attacker, 'target_obj': target}

    def check_winner(self):
        player_alive = any(p.is_alive for p in self.player_team)
        enemy_alive = any(e.is_alive for e in self.enemies)

        if not enemy_alive:
            self.winner = 'player'
            return True
        if not player_alive:
            self.winner = 'enemy'
            return True

        # Check if only immune-to-debuffs enemies remain (e.g. 巨石)
        alive_non_rock = [e for e in self.enemies if e.is_alive and not getattr(e, 'immune_to_debuffs', False)]
        alive_rocks = [e for e in self.enemies if e.is_alive and getattr(e, 'immune_to_debuffs', False)]
        if not alive_non_rock and alive_rocks:
            for rock in alive_rocks:
                rock.is_alive = False
            self.add_log(f"  所有其他单位已被消灭，巨石崩塌!")
            self.winner = 'player'
            return True

        return False
    
    def update_status_damage(self):
        poison_mult = 1.0
        for e in self.enemies:
            if e.is_alive and 'poison_mastery' in getattr(e, 'passive_abilities', []):
                poison_mult = 2.0
                break
        for unit in self._all_units_cache:
            if not unit.is_alive:
                continue
            se = unit.status_effects
            pdata = se.get('poison')
            if pdata:
                stacks = pdata.get('stacks', 1)
                atk = pdata.get('attacker_attack', 0)
                damage = int(stacks * (100 + 0.1 * atk) * poison_mult)
                unit.take_damage(damage)
                self.add_log(f"  ☠ {unit.name} 中毒发作 ({stacks}层), 受到 {damage} 伤害")
                pdata['turns'] -= 1
                if pdata['turns'] <= 0:
                    se.pop('poison', None)
            bdata = se.get('burn')
            if bdata:
                max_hp_pct = bdata.get('max_hp_pct', 0.15)
                damage = max(1, int(unit.max_health * max_hp_pct))
                unit.take_damage(damage)
                self.add_log(f"  🔥 {unit.name} 灼烧发作, 受到 {damage} 伤害")
                bdata['turns'] -= 1
                if bdata['turns'] <= 0:
                    unit.remove_status('burn')
            bldata = se.get('bleed')
            if bldata:
                pct = bldata.get('max_hp_pct', 0.10)
                damage = max(1, int(unit.max_health * pct))
                unit.take_damage(damage)
                self.add_log(f"  🩸 {unit.name} 流血不止, 受到 {damage} 伤害")
                bldata['turns'] -= 1
                if bldata['turns'] <= 0:
                    unit.remove_status('bleed')

    def process_purify(self):
        now = time.time()
        for unit in self.enemies:
            pi = getattr(unit, 'purify_interval', 0)
            if unit.is_alive and pi > 0:
                interval_sec = pi / 30.0
                lpt = getattr(unit, 'last_purify_time', 0.0)
                if now - lpt >= interval_sec:
                    unit.last_purify_time = now
                    for ally in self.enemies:
                        if ally.is_alive:
                            ally.purify_shield_expires = now + 2.0
                    self.add_log(f"【{unit.name}】释放净化护盾，全体友方2秒内免疫负面效果!")

    def cleanup_summons(self):
        removed = []
        for team_attr in ('player_team', 'enemies'):
            team = getattr(self, team_attr)
            for unit in team[:]:
                turns = getattr(unit, '_summon_turns', 0)
                if turns > 0:
                    unit._summon_turns = turns - 1
                    if unit._summon_turns <= 0:
                        team.remove(unit)
                        removed.append(unit)
        if removed:
            self._rebuild_unit_cache()
        return removed

    def process_enemy_passives(self):
        from battle_config import ENEMY_PASSIVES as _EP
        for enemy in self.enemies[:]:
            if not enemy.passive_abilities:
                continue

            # === On-entry: fortify ===
            if 'fortify' in enemy.passive_abilities and enemy.is_alive and not enemy._fortify_applied:
                enemy._fortify_applied = True
                pct = _EP['fortify']['params']['hp_bonus_pct']
                for ally in self.enemies:
                    if ally.is_alive and ally is not enemy:
                        bonus = int(ally.max_health * pct)
                        ally.max_health += bonus
                        ally.current_health += bonus
                self.add_log(f"【{enemy.name}】钢铁意志! 全体友方生命上限提升{int(pct*100)}%!")

            # === On-death: rage & vengeance ===
            if not enemy.is_alive and not enemy._on_death_triggered:
                enemy._on_death_triggered = True
                if 'rage' in enemy.passive_abilities:
                    pdata = _EP['rage']['params']
                    for ally in self.enemies:
                        if ally.is_alive:
                            ally.status_effects['attack_buff'] = {
                                'turns': pdata['turns'],
                                'value': int(pdata['atk_bonus_pct'] * 100),
                            }
                    self.add_log(f"【{enemy.name}】怒火! 全体友方攻击力提升{int(pdata['atk_bonus_pct']*100)}%!")
                if 'vengeance' in enemy.passive_abilities:
                    pdata = _EP['vengeance']['params']
                    dmg_pct = pdata['dmg_pct']
                    for player in self.player_team:
                        if player.is_alive:
                            dmg = max(1, int(player.max_health * dmg_pct))
                            player.take_damage(dmg)
                            if not player.is_alive:
                                self.add_log(f"  {player.name} 被复仇之力击杀!")
                    self.add_log(f"【{enemy.name}】复仇! 对全体敌方造成{int(dmg_pct*100)}%最大生命值的伤害!")

            if not enemy.is_alive:
                continue

            # === Periodic auras and effects ===
            for pa in enemy.passive_abilities:
                pdata = _EP.get(pa)
                if not pdata:
                    continue

                if pa == 'attack_aura':
                    for ally in self.enemies:
                        if ally.is_alive:
                            ally.status_effects['attack_buff'] = {
                                'turns': 2,
                                'value': int(pdata['params']['bonus_pct'] * 100),
                            }

                elif pa == 'defense_aura':
                    for ally in self.enemies:
                        if ally.is_alive:
                            ally.status_effects.setdefault('defense_buff', {})
                            ally.status_effects['defense_buff'] = {
                                'turns': 2,
                                'value': int(pdata['params']['bonus_pct'] * 100),
                            }

                elif pa == 'speed_aura':
                    for ally in self.enemies:
                        if ally.is_alive:
                            ally.status_effects.setdefault('speed_buff', {})
                            ally.status_effects['speed_buff'] = {
                                'turns': 2,
                                'value': int(pdata['params']['bonus_pct'] * 100),
                            }

                elif pa == 'heal_aura':
                    pct = pdata['params']['heal_pct']
                    for ally in self.enemies:
                        if ally.is_alive:
                            heal_amt = max(1, int(ally.max_health * pct))
                            ally.heal(heal_amt)

                elif pa == 'shield_aura':
                    pct = pdata['params']['shield_pct']
                    for ally in self.enemies:
                        if ally.is_alive:
                            ally.shield += max(1, int(ally.max_health * pct))

                elif pa == 'toxic_aura':
                    dmg = pdata['params']['poison_dmg']
                    turns = pdata['params']['turns']
                    for player in self.player_team:
                        if player.is_alive:
                            player.add_status('poison', turns, dmg)

                elif pa == 'bless':
                    for ally in self.enemies:
                        if ally.is_alive:
                            for key in list(ally.status_effects.keys()):
                                if key in ('poison', 'sleep', 'paralyze', 'confuse', 'freeze', 'curse', 'burn'):
                                    del ally.status_effects[key]
                                    break

                elif pa == 'regeneration':
                    pct = pdata['params']['heal_pct']
                    heal_amt = max(1, int(enemy.max_health * pct))
                    enemy.heal(heal_amt)

                elif pa == 'berserk':
                    threshold = pdata['params']['hp_threshold']
                    mult = pdata['params']['atk_mult']
                    hp_pct = enemy.current_health / enemy.max_health if enemy.max_health > 0 else 1
                    if hp_pct < threshold and not enemy._berserk_active:
                        enemy._berserk_active = True
                        enemy.attack = int(enemy._original_attack * mult)
                        self.add_log(f"【{enemy.name}】狂怒! 攻击力翻倍!")
                    elif hp_pct >= threshold and enemy._berserk_active:
                        enemy._berserk_active = False
                        enemy.attack = enemy._original_attack

                elif pa == 'aoe_barrier':
                    pass
                elif pa == 'focus_weak':
                    pass
                elif pa == 'enrage':
                    threshold = pdata['params']['hp_threshold']
                    atk_mult = pdata['params']['atk_mult']
                    spd_mult = pdata['params']['spd_mult']
                    hp_pct = enemy.current_health / enemy.max_health if enemy.max_health > 0 else 1
                    if hp_pct < threshold and not getattr(enemy, '_enraged', False):
                        enemy._enraged = True
                        enemy._enrage_original_attack = getattr(enemy, '_enrage_original_attack', enemy.attack)
                        enemy._enrage_original_speed = getattr(enemy, '_enrage_original_speed', enemy.speed)
                        enemy.attack = int(enemy.attack * atk_mult)
                        enemy.speed = int(enemy.speed * spd_mult)
                        self.add_log(f"【{enemy.name}】狂暴! 攻击力×{atk_mult}，速度×{spd_mult}!")
                elif pa == 'debuff_cleanse':
                    for key in list(enemy.status_effects.keys()):
                        if key in ('poison', 'sleep', 'paralyze', 'confuse', 'freeze', 'curse', 'burn', 'bleed'):
                            del enemy.status_effects[key]

                # ==================== 多格单位被动 ====================
                elif pa == 'guard_protocol':
                    pass

                elif pa == 'iron_wall':
                    gs = enemy.grid_size
                    for ally in self.enemies:
                        if ally.is_alive and ally is not enemy:
                            dr = abs(ally.row - enemy.row)
                            dc = abs(ally.col - enemy.col)
                            if dr + dc <= 1:
                                ally.status_effects.setdefault('defense_buff', {})
                                ally.status_effects['defense_buff'] = {
                                    'turns': 2,
                                    'value': int(pdata['params']['dmg_reduction'] * 100),
                                }

                elif pa == 'poison_mastery':
                    pass

                elif pa == 'advance':
                    if not hasattr(enemy, '_advance_cooldown'):
                        enemy._advance_cooldown = 0
                    enemy._advance_cooldown += 1
                    if enemy._advance_cooldown >= 3:
                        enemy._advance_cooldown = 0
                        old_col = enemy.col
                        if old_col > 0:
                            new_col = old_col - 1
                            gs = enemy.grid_size
                            new_pos = enemy.row * gs + new_col
                            enemy.col = new_col
                            enemy.position = new_pos
                            enemy.occupied_positions = []
                            for h in range(enemy.height):
                                for w in range(enemy.width):
                                    enemy.occupied_positions.append(new_pos + w + h * gs)
                            dmg_pct = pdata['params']['advance_dmg_pct']
                            for player in self.player_team:
                                if player.is_alive and player.col == new_col:
                                    dmg = max(1, int(enemy.attack * dmg_pct))
                                    player.take_damage(dmg)
                                    if not player.is_alive:
                                        self.add_log(f"  {player.name} 被战争巨兽碾碎!")
                            self.add_log(f"【{enemy.name}】战争推进! 前进到第{new_col+1}列!")

                elif pa == 'void_lord':
                    hp_pct = pdata['params']['player_hp_pct']
                    for player in self.player_team:
                        if player.is_alive:
                            dmg = max(1, int(player.max_health * hp_pct))
                            player.take_damage(dmg)
                    atk_bonus = pdata['params']['void_atk_bonus']
                    dmg_reduction = pdata['params']['void_dmg_reduction']
                    for ally in self.enemies:
                        if ally.is_alive and ally is not enemy:
                            ally.status_effects['attack_buff'] = {
                                'turns': 2,
                                'value': int(atk_bonus * 100),
                            }
                            ally.status_effects.setdefault('defense_buff', {})
                            ally.status_effects['defense_buff'] = {
                                'turns': 2,
                                'value': int(dmg_reduction * 100),
                            }
                    self.add_log(f"【{enemy.name}】虚空领主! 对全体玩家造成{int(hp_pct*100)}%最大生命伤害，友方攻+{int(atk_bonus*100)}%防+{int(dmg_reduction*100)}%!")


