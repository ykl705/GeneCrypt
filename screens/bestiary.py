from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.metrics import dp


class BestiaryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        title = Label(text='敌人图鉴', size_hint_y=0.06, bold=True, color=(1, 1, 1, 1))
        main.add_widget(title)
        sv = ScrollView()
        self._content = GridLayout(cols=1, spacing=dp(5), size_hint_y=None)
        self._content.bind(minimum_height=self._content.setter('height'))
        sv.add_widget(self._content)
        main.add_widget(sv)
        self.add_widget(main)

    def on_enter(self):
        self._refresh()

    def _refresh(self):
        self._content.clear_widgets()
        app = App.get_running_app()
        from battle_config import STAGES, ENEMY_TEMPLATES
        from collections import OrderedDict
        maps = OrderedDict()
        for snum in sorted([s for s in STAGES if isinstance(s, int)]):
            stage = STAGES[snum]
            map_name = stage.get('map', 'unknown')
            if map_name not in maps:
                maps[map_name] = []
            for wave in stage.get('waves', []):
                for eid in wave.get('enemies', []):
                    tmpl = ENEMY_TEMPLATES.get(eid)
                    if tmpl and tmpl not in maps[map_name]:
                        maps[map_name].append(tmpl)
        for map_name, enemies in maps.items():
            map_lbl = Label(text=f'📍 {map_name}', size_hint_y=None, height=dp(30), bold=True,
                            color=(0, 0.85, 1, 1))
            self._content.add_widget(map_lbl)
            for tmpl in enemies:
                name = tmpl.get('name', '???')
                hp = tmpl.get('health', 0)
                atk = tmpl.get('attack', 0)
                df = tmpl.get('defense', 0)
                spd = tmpl.get('speed', 0)
                skills = ', '.join([s.get('name', s.get('skill', '')) for s in tmpl.get('skills', [])])
                card = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(5))
                info = f'【{name}】 HP:{hp} ATK:{atk} DEF:{df} SPD:{spd}'
                info_lbl = Label(text=info, size_hint_x=0.6, halign='left', color=(1, 1, 1, 1),
                                 text_size=(dp(300), None))
                skill_lbl = Label(text=f'技能: {skills}' if skills else '无技能', size_hint_x=0.4,
                                  color=(0.6, 1, 0.6, 1), text_size=(dp(200), None))
                card.add_widget(info_lbl)
                card.add_widget(skill_lbl)
                self._content.add_widget(card)
