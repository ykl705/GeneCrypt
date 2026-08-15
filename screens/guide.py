from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.metrics import dp


GUIDE_SECTIONS = [
    {
        'title': '🚀 快速入门',
        'lines': [
            '1. 战斗页「选择队伍」→ 编入最多5张卡牌 → 「开始战斗」',
            '2. 通关解锁新关卡；战斗自动进行，可点「自动」观战',
            '3. 用掉落的🧱材料升级科技、训练卡牌',
            '4. 在繁殖实验室让雄♀雌配种，子代继承基因',
            '5. 反复筛选高质量子代继续繁殖——质量决定强度！',
            '6. 任务和成就给大量🧬密钥，抽卡可获得传说卡',
        ],
    },
    {
        'title': '⚔️ 战斗系统',
        'lines': [
            '· 我方3x3格子 vs 敌方格子（后期4x4，挑战可5x5）',
            '· 行动条：速度越高行动越快；技能随机释放（澎湃必放）',
            '· 伤害=攻击-防御，保底15%伤害（防御再高也不会无敌）',
            '· 状态：中毒/灼烧/流血=持续伤害；睡眠/麻痹/冻结=无法行动；诅咒=受伤+50%',
            '· BOSS为2x2等多格单位，普通攻击命中我方全体',
            '· 50关后敌人随机获得特质（再生/狂暴/反伤/先手等）',
            '· 无损通关计入任务与成就；关卡里程碑敌人有额外强化',
        ],
    },
    {
        'title': '🧬 繁殖与基因',
        'lines': [
            '· 每张卡有6条染色体，基因决定属性/技能/被动',
            '· 显性基因才表达；纯合显性(AA)属性最高',
            '· 数值基因内有「增强段」：加算段（特定碱基越多平加越高）+ 乘算段（特定碱基越多倍率指数上涨）',
            '· 增强段强度随主线任务推进增长（卡牌库→基因报告可查看构成）',
            '· 繁殖：30秒基础时长（科技+建筑可加速），子代交叉互换父母基因',
            '· 突变率5%起，35%突变会产生新的显性基因——质量因此攀升',
            '· 基因组质量(0~1)：显性基因越多越高，属性=(基础)x(1+质量)^指数',
            '· 不同父母配种有杂交优势(攻防血+15%)',
            '· 血脉：6种基础血脉，可融合出高级血脉',
            '· 基因工程页：射线变异/基因拼接/甲基化/基因隔离',
            '· 抽卡限定基因位于chrG染色体，可通过繁殖传给后代',
        ],
    },
    {
        'title': '⭐ 卡牌养成',
        'lines': [
            '· 升星：消耗同名卡+精华+材料，每星全属性+10%，5星解锁3芯片槽',
            '· 训练：每项属性最多训练「星级x8」次，直接加属性',
            '· 模组：百分比属性加成，2个低级合成1个高级',
            '· 芯片：装备后直接获得技能（不限基因）',
            '· 装备：6个槽位8种稀有度随机词条；25%几率为套装件，集齐3~4件触发套装效果（龙裔之怒/冰封之心/暗影之舞/混沌之源）',
            '· 奖励卡（任务/成就给的卡）属性与质量绑定，升星模组不会掉属性',
            '· 卡牌库支持：收藏/克隆/射线变异/任务提交/删除',
        ],
    },
    {
        'title': '🔬 科技树',
        'lines': [
            '· 6大分支：核心/育种/变异/基因编辑/强化/后勤',
            '· 消耗🧱材料+🧬密钥，部分科技需前置等级',
            '· 推荐优先：胚胎工程→快速繁殖→自动繁殖（挂机育种）',
            '· 强化分支：基因组强化(属性x1.2~1.6)、破限(全属性x1.1~1.3)',
            '· 变异分支：进化增强(突变率+5%/级)、辐射抗性',
            '· 后勤：卡牌仓库(卡位+)、精灵(战后自动掉卡)',
            '· 升级任意科技计入任务进度',
        ],
    },
    {
        'title': '🎰 基因抽卡',
        'lines': [
            '· 5个卡池，通关解锁：剧毒(1关)/烈焰(30)/冰霜(50)/血池(70)/终焉(90)',
            '· 概率：传说0.2%、稀有1.5%；360抽必定传说（保底）',
            '· 传说卡获得该卡池专属基因，可繁殖遗传',
            '· 每次抽卡有16%几率附带芯片/低级模组',
            '· 🧬密钥来源：战斗/任务/成就/PvP',
        ],
    },
    {
        'title': '🔥 主题挑战',
        'lines': [
            '· 5个主题，通关50/60/80/100/120关解锁，各有专属敌人',
            '· 自行勾选挑战因子（共118个）增加难度与积分',
            '· 因子全部真实生效：敌方强化、巨石填充、圣甲虫群、盲盒、五波攻势、元素轮回……',
            '· 积分越高难度越大，记录每个主题的最高分与最快用时',
            '· 隐藏成就：挑战无损、60秒速通、盲盒战争全因子',
        ],
    },
    {
        'title': '🏰 副本',
        'lines': [
            '· 5个副本（30/50/80/120/160关解锁），楼层随机生成',
            '· 房间类型：战斗/宝箱/商店/事件',
            '· 最终层为BOSS；胜利获得材料与精华',
            '· 副本战斗不影响主线进度，可放心刷资源',
        ],
    },
    {
        'title': '♾️ 无限模式',
        'lines': [
            '· 战斗页点「无限模式」进入',
            '· 每通过1层，敌人强度+15%',
            '· 层数保存，奖励随层数增长',
            '· 成就：第10层/第30层',
        ],
    },
    {
        'title': '🏆 PvP竞技场',
        'lines': [
            '· 5个段位：青铜→白银→黄金→铂金→钻石',
            '· 段位分达标解锁更高段位；击败机器人获得段位分+🧱+🧬',
            '· 机器人为你当前实力的镜像强度，公平对决',
            '· 另有「代码对决」：粘贴双方队伍代码离线模拟战斗',
            '· PvP胜负不影响主线',
        ],
    },
    {
        'title': '🏗️ 基地建筑',
        'lines': [
            '· 基因研究所：全体卡牌攻击+1%/级',
            '· 繁殖中心：繁殖速度+5%/级',
            '· 训练营：训练效果+3%/级',
            '· 仓库：卡牌上限+2/级',
            '· 精华提炼厂：离线每小时产精华（上限12小时）',
            '· 材料+精华升级，最高10级',
        ],
    },
    {
        'title': '📋 任务与成就',
        'lines': [
            '· 75个任务：主线40/支线20/挑战15，链式解锁',
            '· 需要提交卡牌的任务：在卡牌库点「任务提交」',
            '· 完成后在任务页领取奖励（含高质奖励卡）',
            '· 28个成就，隐藏成就需达成特殊条件才显示',
            '· 成就奖励含专属卡：不朽龙裔/完美基因体',
        ],
    },
    {
        'title': '💰 资源说明',
        'lines': [
            '· 🧬基因密钥：战斗/任务/成就/PvP产出 → 抽卡、科技',
            '· 🧱战斗材料：战斗/任务产出 → 训练、科技、建筑、升星',
            '· 精华：战斗/离线(精华厂)产出 → 建筑升级、升星',
            '· 芯片/模组：抽卡附带、战斗掉落',
            '· 装备：战斗胜利概率掉落，关卡越深品质越好',
        ],
    },
]


def show_help(title, body):
    from kivy.uix.scrollview import ScrollView
    content = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(12))
    lbl = Label(text=body, halign='left', valign='top', color=(0.9, 0.9, 0.9, 1),
                size_hint_y=None)
    lbl.bind(size=lambda *_: setattr(lbl, 'text_size', lbl.size))
    sv = ScrollView(size_hint_y=1)
    inner = BoxLayout(orientation='vertical', size_hint_y=None)
    inner.bind(minimum_height=inner.setter('height'))
    inner.add_widget(lbl)
    sv.add_widget(inner)
    content.add_widget(sv)
    popup = Popup(title=title, content=content, size_hint=(0.85, 0.6))
    popup.open()
    return popup


class GuideScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(10))
        main.add_widget(Label(text='游戏指引', size_hint_y=0.05, bold=True, color=(0.4, 0.9, 1, 1)))
        sv = ScrollView(size_hint_y=1)
        self._content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
        self._content.bind(minimum_height=self._content.setter('height'))
        sv.add_widget(self._content)
        main.add_widget(sv)
        self.add_widget(main)
        self._refresh()

    def on_enter(self):
        pass

    def _refresh(self):
        self._content.clear_widgets()
        for sec in GUIDE_SECTIONS:
            self._content.add_widget(Label(text=sec['title'], size_hint_y=None, height=dp(28),
                                           bold=True, color=(0, 0.85, 1, 1), halign='left'))
            for line in sec['lines']:
                lbl = Label(text=line, size_hint_y=None, height=dp(26), halign='left', valign='middle',
                            color=(0.8, 0.8, 0.8, 1), font_size=dp(12))
                lbl.bind(size=lambda *_: setattr(lbl, 'text_size', lbl.size))
                self._content.add_widget(lbl)
            self._content.add_widget(Label(text='', size_hint_y=None, height=dp(4)))
