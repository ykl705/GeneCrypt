from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.graphics import Color, Rectangle
import random


class CardWidget(ButtonBehavior, BoxLayout):
    card = ObjectProperty(None, allownone=True)

    def __init__(self, card=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = dp(4)
        self.spacing = dp(2)
        self.card = card
        if card:
            self._build_ui()
        self.bind(size=self._on_size_changed)

    def _on_size_changed(self, instance, value):
        if not self.card:
            return
        for child in self.children:
            if isinstance(child, Label):
                child.text_size = (self.width - dp(10), None)

    def _build_ui(self):
        self.clear_widgets()
        c = self.card
        gender_color = '#4a90d9' if c.gender == 'male' else '#d94a8a'
        alive_str = '' if c.is_alive else ' [已死亡]'

        name_lbl = Label(text=f'{c.name} [{c.id}]{alive_str}',
                         size_hint_y=0.35, color=(1, 1, 1, 1), halign='left', valign='middle',
                         text_size=(self.width - dp(10), None), shorten=True)
        traits = c.traits
        star_str = '★' * getattr(c, 'star', 1)
        bl = getattr(c, 'bloodline', '')
        bl_str = f'[{bl}]' if bl else ''
        info = f'{star_str}{bl_str} HP:{traits.get("health","?")} ATK:{traits.get("attack","?")}'
        info_lbl = Label(text=info, size_hint_y=0.25, color=(0.8, 0.8, 0.8, 1),
                         halign='left', text_size=(self.width - dp(10), None))
        extra = []
        if getattr(c, 'modules', []):
            extra.append(f'M:{len(c.modules)}')
        if getattr(c, 'chips', []):
            extra.append(f'C:{len(c.chips)}')
        extra_str = ' '.join(extra)
        skills_lbl = Label(text=f'{extra_str} 技能: {", ".join(c.skills[:3])}' if c.skills else f'{extra_str} 无技能',
                           size_hint_y=0.25, color=(0.6, 1, 0.6, 1), halign='left',
                           text_size=(self.width - dp(10), None))
        self.add_widget(name_lbl)
        self.add_widget(info_lbl)
        self.add_widget(skills_lbl)


class CardDetailPopup(BoxLayout):
    orientation = 'vertical'
    card = ObjectProperty(None, allownone=True)

    def __init__(self, card=None, **kwargs):
        super().__init__(**kwargs)
        self.card = card
        if card:
            self._build_ui()

    def _build_ui(self):
        self.clear_widgets()
        c = self.card
        if not c:
            return
        gender_color = '#4a90d9' if c.gender == 'male' else '#d94a8a'
        alive_str = '' if c.is_alive else ' [已死亡]'
        title = f'{c.name} [{c.id}]{alive_str}'
        title_lbl = Label(text=title, size_hint_y=0.06, bold=True, color=(1, 1, 1, 1))
        self.add_widget(title_lbl)
        header_lbl = Label(text=f'性别: {"♂ 雄性" if c.gender == "male" else "♀ 雌性"} | '
                                f'代系: {len(c.parent_ids)} | 寿命: {c.traits.get("lifespan", "?")}',
                           size_hint_y=0.05, color=(0.8, 0.8, 0.8, 1))
        self.add_widget(header_lbl)
        sv = ScrollView(size_hint_y=0.7)
        inner = GridLayout(cols=2, spacing=dp(2), size_hint_y=None, padding=dp(5))
        inner.bind(minimum_height=inner.setter('height'))
        t = c.traits
        stats = [
            ('攻击', t.get('attack', 0)), ('生命', t.get('health', 0)),
            ('防御', t.get('defense', 0)), ('速度', t.get('speed', 0)),
            ('体力', t.get('stamina', 0)), ('暴击', t.get('critical_rate', 0)),
            ('闪避', t.get('dodge_rate', 0)), ('寿命', t.get('lifespan', 0)),
        ]
        for name, val in stats:
            inner.add_widget(Label(text=name, color=(0.8, 0.8, 0.8, 1)))
            inner.add_widget(Label(text=str(val), color=(1, 1, 1, 1)))
        inner.add_widget(Label(text='技能', color=(0.6, 1, 0.6, 1)))
        inner.add_widget(Label(text=', '.join(c.skills) if c.skills else '无', color=(1, 1, 1, 1)))
        inner.add_widget(Label(text='被动', color=(0.6, 0.8, 1, 1)))
        inner.add_widget(Label(text=', '.join(c.passive_skills) if c.passive_skills else '无', color=(1, 1, 1, 1)))
        sv.add_widget(inner)
        self.add_widget(sv)
