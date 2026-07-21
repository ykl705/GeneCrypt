from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.metrics import dp
from gene_config import ACHIEVEMENTS


class AchievementScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        main.add_widget(Label(text='成就系统', size_hint_y=0.05, bold=True, color=(1,0.85,0,1)))
        sv = ScrollView(size_hint_y=1)
        self._content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        self._content.bind(minimum_height=self._content.setter('height'))
        sv.add_widget(self._content)
        main.add_widget(sv)
        self.add_widget(main)

    def on_enter(self):
        self._refresh()

    def _refresh(self):
        self._content.clear_widgets()
        app = App.get_running_app()
        game = app.game

        cats = {'战斗':[],'繁殖':[],'收集':[],'养成':[],'挑战':[],'隐藏':[]}
        for a in ACHIEVEMENTS:
            tp = a.get('type','')
            if tp == 'hidden': cats['隐藏'].append(a)
            elif tp in ('total_wins','boss_kills','max_stage','no_loss_count'): cats['战斗'].append(a)
            elif tp in ('breed_count','bloodline_collect'): cats['繁殖'].append(a)
            elif tp in ('have_cards','module_collect'): cats['收集'].append(a)
            elif tp in ('star_count','chip_equip','training_complete'): cats['养成'].append(a)
            else: cats['挑战'].append(a)

        done_count = sum(1 for a in ACHIEVEMENTS if a['id'] in game.achievements)
        self._content.add_widget(Label(text=f'已完成: {done_count}/{len(ACHIEVEMENTS)}',
                                        size_hint_y=None, height=dp(24), color=(0.6,1,0.6,1)))

        for cat, items in cats.items():
            if not items:
                continue
            self._content.add_widget(Label(text=f'-- {cat} --', size_hint_y=None, height=dp(22),
                                            bold=True, color=(0,0.85,1,1)))
            for a in items:
                aid = a['id']
                is_done = aid in game.achievements
                is_claimed = aid in game.achievements  # already removed after claim
                name = a['name'] if a['type'] != 'hidden' or is_done else '???'
                stars = '★' * a.get('diff',1)
                row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36), spacing=dp(5))
                icon = '✓' if is_done else '○'
                c = (0.4,1,0.4,1) if is_done else (0.5,0.5,0.5,1)
                row.add_widget(Label(text=f'{icon} {name} [{stars}]', color=c, size_hint_x=0.55))
                if is_done and aid in game.achievements:
                    btn = Button(text='领取', size_hint_x=0.2, background_color=(0.2,0.6,0.2,1))
                    btn.bind(on_press=lambda _, a=aid: self._claim(a))
                    row.add_widget(btn)
                else:
                    row.add_widget(Label(text='已领' if is_done else a['desc'][:15], size_hint_x=0.45,
                                          color=(0.5,0.5,0.5,1), font_size=dp(10)))
                self._content.add_widget(row)

    def _claim(self, aid):
        app = App.get_running_app()
        msgs, err = app.game.claim_achievement(aid)
        if msgs:
            app.game.save_game()
            popup = Popup(title='成就奖励', content=Label(text='\n'.join(msgs)), size_hint=(0.5,0.4))
            popup.open()
        self._refresh()
