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
        seen = set()
        for snum in sorted([s for s in STAGES if isinstance(s, int)]):
            stage = STAGES[snum]
            enemies = stage.get('enemies', [])
            for e in enemies:
                name = e.get('name', '')
                if name and name not in seen:
                    seen.add(name)
                    hp = e.get('health', 0)
                    atk = e.get('attack', 0)
                    df = e.get('defense', 0)
                    spd = e.get('speed', 0)
                    skills = ', '.join(e.get('skills', [])[:3])
                    info = f'[{stage.get("name","?")}] {name} HP:{hp} ATK:{atk} DEF:{df} SPD:{spd}'
                    lbl = Label(text=info, size_hint_y=None, height=dp(28), halign='left',
                                color=(1, 1, 1, 1))
                    self._content.add_widget(lbl)
                    if skills:
                        self._content.add_widget(Label(text=f'  技能: {skills}',
                                                        size_hint_y=None, height=dp(22),
                                                        color=(0.6, 1, 0.6, 1), font_size=dp(11)))
