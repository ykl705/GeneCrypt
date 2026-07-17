from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from gene_game import QUEST_DEFINITIONS


class QuestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._category = 'main'
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        title = Label(text='任务系统', size_hint_y=0.06, bold=True, color=(1, 1, 1, 1))
        main.add_widget(title)

        cat_selector = BoxLayout(orientation='horizontal', size_hint_y=0.06, spacing=dp(5))
        cats = [
            ('main', '主线', '#00d9ff'),
            ('side', '支线', '#4ecdc4'),
            ('challenge', '挑战', '#ff6b6b'),
        ]
        for cid, cname, color in cats:
            btn = Button(text=cname, background_color=self._hex(color), on_press=lambda _, c=cid: self._switch_cat(c))
            cat_selector.add_widget(btn)
        main.add_widget(cat_selector)

        content = BoxLayout(orientation='horizontal', spacing=dp(10))
        self._quest_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self._quest_list.bind(minimum_height=self._quest_list.setter('height'))
        sv_list = ScrollView(size_hint_x=0.5)
        sv_list.add_widget(self._quest_list)
        content.add_widget(sv_list)

        self._detail = BoxLayout(orientation='vertical', size_hint_x=0.5, spacing=dp(5), padding=dp(5))
        self._detail_title = Label(text='选择任务查看详情', color=(0.8, 0.8, 0.8, 1), size_hint_y=0.1)
        self._detail_desc = Label(text='', color=(0.8, 0.8, 0.8, 1), size_hint_y=0.1)
        self._detail_progress = Label(text='', color=(0.8, 0.8, 0.8, 1), size_hint_y=0.1)
        self._detail_reward = Label(text='', color=(1, 1, 0.6, 1), size_hint_y=0.1)
        self._detail_btn = Button(text='领取奖励', size_hint_y=0.1, disabled=True, on_press=self._claim_quest)
        self._detail.add_widget(self._detail_title)
        self._detail.add_widget(self._detail_desc)
        self._detail.add_widget(self._detail_progress)
        self._detail.add_widget(self._detail_reward)
        self._detail.add_widget(self._detail_btn)
        sv_detail = ScrollView(size_hint_x=0.5)
        sv_detail.add_widget(self._detail)
        content.add_widget(sv_detail)
        main.add_widget(content)
        self.add_widget(main)
        self._selected_quest = None

    def _hex(self, h):
        return tuple(int(h[i:i+2], 16)/255 for i in (1, 3, 5)) + (1,)

    def _switch_cat(self, cat):
        self._category = cat
        self._refresh()

    def on_enter(self):
        self._refresh()

    def _refresh(self):
        app = App.get_running_app()
        game = app.game
        self._quest_list.clear_widgets()
        quests = [q for q in QUEST_DEFINITIONS if q['category'] == self._category]
        for q in quests:
            qid = q['id']
            completed = qid in game.quest_completed
            claimed = qid in game.quest_claimed
            unlocked = game._is_quest_unlocked(qid)
            st = '✅' if claimed else ('🔄' if completed else ('🔒' if not unlocked else '📋'))
            btn = Button(text=f"{st} {q['title']}", size_hint_y=None, height=dp(40),
                         halign='left', on_press=lambda _, qq=q: self._show_detail(qq))
            if claimed:
                btn.background_color = (0.3, 0.8, 0.3, 1)
            elif not unlocked:
                btn.background_color = (0.3, 0.3, 0.3, 1)
            self._quest_list.add_widget(btn)

    def _show_detail(self, q):
        self._selected_quest = q
        app = App.get_running_app()
        game = app.game
        qid = q['id']
        self._detail_title.text = q['title']
        self._detail_desc.text = f"描述: {q['description']}"
        progress = game._get_quest_progress(qid)
        target = q.get('target', 1)
        self._detail_progress.text = f"进度: {progress}/{target}"
        rewards_text = '奖励: '
        for r in q.get('rewards', []):
            t = r['type']
            if t == 'gacha_currency':
                rewards_text += f'🧬×{r["amount"]} '
            elif t == 'battle_materials':
                rewards_text += f'🧱×{r["amount"]} '
            elif t == 'card_with_skills':
                skills = ', '.join(r.get('skill_names', []))
                rewards_text += f'[技能卡:{skills}] '
        self._detail_reward.text = rewards_text
        claimed = qid in game.quest_claimed
        completed = qid in game.quest_completed
        if claimed:
            self._detail_btn.text = '已领取'
            self._detail_btn.disabled = True
        elif completed:
            self._detail_btn.text = '领取奖励'
            self._detail_btn.disabled = False
        else:
            self._detail_btn.text = '未完成'
            self._detail_btn.disabled = True

    def _claim_quest(self, btn):
        if not self._selected_quest:
            return
        app = App.get_running_app()
        result = app.game.claim_quest(self._selected_quest['id'])
        msg = result.get('msg', '')
        if result.get('success'):
            app.game.save_game()
            app.refresh_breeding_combos()
        self._show_detail(self._selected_quest)
        self._refresh()
