from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.popup import Popup
from widgets.card_widget import CardWidget, CardDetailPopup


class CardLibraryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='horizontal', spacing=dp(10), padding=dp(10))
        left = BoxLayout(orientation='vertical', size_hint_x=0.4, spacing=dp(5))
        left.add_widget(Label(text='卡牌库', size_hint_y=0.06, bold=True, color=(1, 1, 1, 1)))
        self._count_lbl = Label(text='卡牌: 0/20', size_hint_y=0.04, color=(0.8, 0.8, 0.8, 1))
        left.add_widget(self._count_lbl)
        sv = ScrollView()
        self._card_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self._card_list.bind(minimum_height=self._card_list.setter('height'))
        sv.add_widget(self._card_list)
        left.add_widget(sv)
        main.add_widget(left)

        right = BoxLayout(orientation='vertical', size_hint_x=0.6, spacing=dp(5))
        right.add_widget(Label(text='卡牌详情', size_hint_y=0.06, bold=True, color=(1, 1, 1, 1)))
        sv2 = ScrollView()
        self._detail = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        self._detail.bind(minimum_height=self._detail.setter('height'))
        sv2.add_widget(self._detail)
        right.add_widget(sv2)
        self._action_bar = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=dp(5))
        right.add_widget(self._action_bar)
        main.add_widget(right)
        self.add_widget(main)
        self._selected_card = None

    def on_enter(self):
        self._refresh()

    def _refresh(self):
        app = App.get_running_app()
        game = app.game
        self._count_lbl.text = f'卡牌: {len(game.cards)}/{game.effective_max_cards}'
        self._card_list.clear_widgets()
        for card in game.cards:
            cw = CardWidget(card=card)
            cw.bind(on_release=lambda _, c=card: self._on_card_select(c))
            self._card_list.add_widget(cw)
        if self._selected_card and self._selected_card in game.cards:
            self._show_detail(self._selected_card)
        else:
            self._detail.clear_widgets()
            self._action_bar.clear_widgets()

    def _on_card_select(self, card):
        self._selected_card = card
        self._show_detail(card)

    def _show_detail(self, card):
        self._detail.clear_widgets()
        self._action_bar.clear_widgets()
        c = card
        gender_color = '#4a90d9' if c.gender == 'male' else '#d94a8a'
        alive_str = '' if c.is_alive else ' [已死亡]'
        title = f'{c.name} [{c.id}]{alive_str}'
        self._detail.add_widget(Label(text=title, bold=True, color=(1, 1, 1, 1), size_hint_y=None, height=dp(30)))
        self._detail.add_widget(Label(text=f'性别: {"♂ 雄性" if c.gender == "male" else "♀ 雌性"} | '
                                           f'代系: {len(c.parent_ids)} | 寿命: {c.traits.get("lifespan", "?")}',
                                     size_hint_y=None, height=dp(25), color=(0.8, 0.8, 0.8, 1)))
        t = c.traits
        stats_grid = GridLayout(cols=4, size_hint_y=None, height=dp(100), spacing=dp(2))
        stats = [
            ('攻击', t.get('attack', 0)), ('生命', t.get('health', 0)),
            ('防御', t.get('defense', 0)), ('速度', t.get('speed', 0)),
            ('体力', t.get('stamina', 0)), ('暴击', t.get('critical_rate', 0)),
            ('闪避', t.get('dodge_rate', 0)), ('寿命', t.get('lifespan', 0)),
        ]
        for name, val in stats:
            stats_grid.add_widget(Label(text=f'{name}:', color=(0.8, 0.8, 0.8, 1), font_size=dp(11)))
            stats_grid.add_widget(Label(text=str(val), color=(1, 1, 1, 1), font_size=dp(11)))
        self._detail.add_widget(stats_grid)
        skills_text = ', '.join(c.skills) if c.skills else '无'
        self._detail.add_widget(Label(text=f'技能: {skills_text}', color=(0.6, 1, 0.6, 1), size_hint_y=None, height=dp(25)))
        passive_text = ', '.join(c.passive_skills) if c.passive_skills else '无'
        self._detail.add_widget(Label(text=f'被动: {passive_text}', color=(0.6, 0.8, 1, 1), size_hint_y=None, height=dp(25)))
        if c.is_alive:
            mutate_btn = Button(text='射线变异', on_press=lambda _: self._mutate_card(c))
            self._action_bar.add_widget(mutate_btn)
        clone_btn = Button(text='克隆', on_press=lambda _: self._clone_card(c))
        self._action_bar.add_widget(clone_btn)
        report_btn = Button(text='基因报告', on_press=lambda _: self._show_report(c))
        self._action_bar.add_widget(report_btn)
        delete_btn = Button(text='删除', on_press=lambda _: self._delete_card(c))
        delete_btn.background_color = (0.8, 0.2, 0.2, 1)
        self._action_bar.add_widget(delete_btn)

    def _delete_card(self, card):
        app = App.get_running_app()
        app.game.cards.remove(card)
        app.game.save_game()
        self._selected_card = None
        app.refresh_breeding_combos()
        self._refresh()

    def _mutate_card(self, card):
        from kivy.uix.textinput import TextInput
        app = App.get_running_app()
        popup = Popup(title='射线变异', size_hint=(0.6, 0.4))
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        content.add_widget(Label(text=f'对 {card.name} 进行射线照射？\n这将随机改变基因序列，可能有益也可能有害。'))
        btn_box = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=0.3)
        confirm = Button(text='确认照射')
        cancel = Button(text='取消')
        btn_box.add_widget(confirm)
        btn_box.add_widget(cancel)
        content.add_widget(btn_box)
        popup.content = content
        confirm.bind(on_press=lambda _: self._do_mutate(card, popup))
        cancel.bind(on_press=popup.dismiss)
        popup.open()

    def _do_mutate(self, card, popup):
        app = App.get_running_app()
        app.game.radiation_mutation(card)
        app.game.save_game()
        popup.dismiss()
        self._show_detail(card)

    def _clone_card(self, card):
        app = App.get_running_app()
        result = app.game.clone_card(card)
        if isinstance(result, str):
            from kivy.uix.popup import Popup
            popup = Popup(title='克隆失败', content=Label(text=result), size_hint=(0.5, 0.3))
            popup.open()
        else:
            app.refresh_breeding_combos()
            self._refresh()

    def _show_report(self, card):
        popup = Popup(title=f'{card.name} - 基因报告', size_hint=(0.8, 0.8))
        sv = ScrollView()
        inner = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2), padding=dp(10))
        inner.bind(minimum_height=inner.setter('height'))
        inner.add_widget(Label(text=f'名称: {card.name}', color=(1, 1, 1, 1), size_hint_y=None, height=dp(25)))
        inner.add_widget(Label(text=f'ID: {card.id}', color=(1, 1, 1, 1), size_hint_y=None, height=dp(25)))
        inner.add_widget(Label(text=f'性别: {"♂ 雄性" if card.gender == "male" else "♀ 雌性"}',
                               size_hint_y=None, height=dp(25), color=(1, 1, 1, 1)))
        inner.add_widget(Label(text=f'亲代: {", ".join(card.parent_ids) if card.parent_ids else "无"}',
                               size_hint_y=None, height=dp(25), color=(0.8, 0.8, 0.8, 1)))
        inner.add_widget(Label(text=f'存活: {"是" if card.is_alive else "否"}',
                               size_hint_y=None, height=dp(25), color=(0.3, 1, 0.3, 1) if card.is_alive else (1, 0.3, 0.3, 1)))
        for chr_id, homologs in card.chromosomes.items():
            inner.add_widget(Label(text=f'--- {chr_id} ---', bold=True, size_hint_y=None, height=dp(25), color=(0, 0.85, 1, 1)))
            for i, h in enumerate(homologs):
                genome = h.get('genome', '')[:60]
                dom = h.get('is_dominant', {})
                inner.add_widget(Label(text=f'  同源{i+1}: {genome}...', size_hint_y=None, height=dp(25),
                                        color=(0.6, 0.6, 0.6, 1)))
        for gname, gdata in card.genes.items():
            a1d = gdata.get('allele1', {}).get('is_dominant', False)
            a2d = gdata.get('allele2', {}).get('is_dominant', False)
            inner.add_widget(Label(text=f'  {gname}: {"显" if a1d else "隐"}/{"显" if a2d else "隐"}',
                                   size_hint_y=None, height=dp(20), color=(0.8, 0.8, 1, 1)))
        close_btn = Button(text='关闭', size_hint_y=None, height=dp(40))
        inner.add_widget(close_btn)
        sv.add_widget(inner)
        popup.content = sv
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
