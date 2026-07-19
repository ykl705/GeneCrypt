from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image as KivyImage
from kivy.app import App
from kivy.metrics import dp
import os


class BestiaryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        title = Label(text='敌人图鉴', size_hint_y=0.06, bold=True, color=(1, 1, 1, 1))
        main.add_widget(title)
        sv = ScrollView()
        self._content = GridLayout(cols=1, spacing=dp(3), size_hint_y=None)
        self._content.bind(minimum_height=self._content.setter('height'))
        sv.add_widget(self._content)
        main.add_widget(sv)
        self.add_widget(main)

    def on_enter(self):
        self._refresh()

    def _refresh(self):
        self._content.clear_widgets()
        from battle_config import STAGES, ENEMY_TEMPLATES
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
                    row = BoxLayout(orientation='horizontal', size_hint_y=None,
                                    height=dp(56), spacing=dp(6))
                    tkey = ''
                    for tid, tmpl in ENEMY_TEMPLATES.items():
                        if tmpl['name'] == name:
                            tkey = tid
                            break
                    img_path = os.path.join('assets', 'enemies', f'{tkey}_0.png') if tkey else ''
                    if os.path.exists(img_path):
                        img = KivyImage(source=img_path, size_hint_x=None, width=dp(48),
                                        allow_stretch=True, keep_ratio=True, fit_mode='contain')
                        row.add_widget(img)
                    info = BoxLayout(orientation='vertical', size_hint_x=1, spacing=dp(1))
                    info.add_widget(Label(text=f'[{stage.get("name","?")}] {name}',
                                          size_hint_y=None, height=dp(20), halign='left',
                                          color=(1, 1, 1, 1), bold=True, font_size=dp(11)))
                    info.add_widget(Label(text=f'HP:{hp} ATK:{atk} DEF:{df} SPD:{spd}',
                                          size_hint_y=None, height=dp(16), halign='left',
                                          color=(0.8, 0.8, 0.8, 1), font_size=dp(10)))
                    sk = f'技能: {skills}' if skills else ''
                    info.add_widget(Label(text=sk, size_hint_y=None, height=dp(16), halign='left',
                                          color=(0.6, 1, 0.6, 1), font_size=dp(10)))
                    row.add_widget(info)
                    self._content.add_widget(row)
