from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.metrics import dp


class GeneEngineeringScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        title = Label(text='基因工程实验室', size_hint_y=0.06, bold=True, color=(1, 1, 1, 1))
        main.add_widget(title)

        select = BoxLayout(orientation='horizontal', size_hint_y=0.06, spacing=dp(5))
        select.add_widget(Label(text='卡片:', color=(0.8, 0.8, 0.8, 1)))
        self._card_btn = Button(text='选择卡片', on_press=lambda _: self._show_card_dropdown())
        select.add_widget(self._card_btn)
        main.add_widget(select)

        tools = GridLayout(cols=4, size_hint_y=0.5, spacing=dp(3), padding=dp(5))
        tools.add_widget(Button(text='限制性内切酶', on_press=lambda _: self._do_op('cut')))
        tools.add_widget(Button(text='甲基化', on_press=lambda _: self._do_op('methyl')))
        tools.add_widget(Button(text='射线照射', on_press=lambda _: self._do_op('radiate')))
        tools.add_widget(Button(text='基因敲除', on_press=lambda _: self._do_op('knockout')))
        tools.add_widget(Button(text='基因拼接', on_press=lambda _: self._do_op('splice')))
        tools.add_widget(Button(text='CRISPR编辑', on_press=lambda _: self._do_op('crispr')))
        tools.add_widget(Button(text='激活基因', on_press=lambda _: self._do_op('activate')))
        tools.add_widget(Button(text='基因隔离', on_press=lambda _: self._do_op('isolate')))
        tools.add_widget(Button(text='重复染色体', on_press=lambda _: self._do_op('duplicate')))
        tools.add_widget(Button(text='基因库', on_press=lambda _: self._show_gene_library()))
        self._input1 = TextInput(hint_text='位置', multiline=False, size_hint_y=None, height=dp(30))
        self._input2 = TextInput(hint_text='碱基/基因名', multiline=False, size_hint_y=None, height=dp(30))
        tools.add_widget(self._input1)
        tools.add_widget(self._input2)
        main.add_widget(tools)

        self._result_lbl = Label(text='选择卡片并操作', size_hint_y=0.05, color=(0.8, 0.8, 0.8, 1))
        main.add_widget(self._result_lbl)

        sv = ScrollView()
        self._gene_info = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self._gene_info.bind(minimum_height=self._gene_info.setter('height'))
        sv.add_widget(self._gene_info)
        main.add_widget(sv)

        self.add_widget(main)
        self._selected_card = None

    def on_enter(self):
        pass

    def _show_card_dropdown(self):
        app = App.get_running_app()
        dd = DropDown()
        for card in app.game.cards:
            if not card.is_alive:
                continue
            btn = Button(text=f'{card.name} [{card.id}]', size_hint_y=None, height=dp(40))
            btn.bind(on_release=lambda b, c=card: self._select_card(c, dd))
            dd.add_widget(btn)
        dd.open(self._card_btn)

    def _select_card(self, card, dd):
        self._selected_card = card
        self._card_btn.text = f'{card.name} [{card.id}]'
        dd.dismiss()
        self._show_genes(card)

    def _show_genes(self, card):
        self._gene_info.clear_widgets()
        for gname, gdata in card.genes.items():
            a1 = gdata.get('allele1', {})
            a2 = gdata.get('allele2', {})
            chr_name = gdata.get('chromosome', '?')
            d1 = '显' if a1.get('is_dominant') else '隐'
            d2 = '显' if a2.get('is_dominant') else '隐'
            self._gene_info.add_widget(Label(
                text=f'{gname}: {d1}/{d2} (chr:{chr_name})',
                size_hint_y=None, height=dp(20), color=(0.8, 0.8, 1, 1),
                font_size=dp(11)))

    def _do_op(self, op):
        if not self._selected_card:
            from kivy.uix.popup import Popup
            popup = Popup(title='错误', content=Label(text='请先选择卡片'), size_hint=(0.5, 0.3))
            popup.open()
            return
        app = App.get_running_app()
        card = self._selected_card
        arg1 = self._input1.text
        arg2 = self._input2.text
        result = None
        try:
            if op == 'cut':
                pos = int(arg1) if arg1 else 0
                result = app.game.restrict_enzyme_cut(arg2 if arg2 else card.genes.get('gene1', {}).get('name', ''), pos, card)
            elif op == 'methyl':
                result = app.game.methylation(arg2 if arg2 else None, card)
            elif op == 'radiate':
                result = app.game.radiation_mutation(card)
            elif op == 'knockout':
                result = app.game.gene_knockout(arg2 if arg2 else None, card)
            elif op == 'splice':
                result = app.game.splice_gene(arg2 if arg2 else None, card, card)
            elif op == 'crispr':
                pos = int(arg1) if arg1 else 0
                base = arg2.upper() if arg2 and arg2.upper() in 'ATGC' else None
                result = app.game.crispr_edit(base or '', card, pos, base)
            elif op == 'activate':
                result = app.game.activate_gene(arg2 if arg2 else None, card)
            elif op == 'isolate':
                result = app.game.toggle_gene_isolation(arg2 if arg2 else None, card)
            elif op == 'duplicate':
                result = app.game.duplicate_chromosome(arg2 if arg2 else None, card, card)
        except Exception as e:
            from kivy.uix.popup import Popup
            popup = Popup(title='操作失败', content=Label(text=str(e)), size_hint=(0.5, 0.3))
            popup.open()
            return
        if result:
            msg = result.get('msg') if isinstance(result, dict) else str(result)
            self._result_lbl.text = msg[:80] if msg else '完成'
            app.game.save_game()
        self._show_genes(card)

    def _show_gene_library(self):
        app = App.get_running_app()
        lib = app.game.get_gene_library()
        from kivy.uix.popup import Popup
        content = BoxLayout(orientation='vertical', spacing=dp(5))
        sv = ScrollView()
        inner = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        inner.bind(minimum_height=inner.setter('height'))
        for gname, fragments in lib.items():
            inner.add_widget(Label(text=f'{gname}: {len(fragments)} fragments', size_hint_y=None, height=dp(25),
                                   color=(0.8, 0.8, 1, 1)))
        sv.add_widget(inner)
        content.add_widget(sv)
        close_btn = Button(text='关闭', size_hint_y=0.15)
        content.add_widget(close_btn)
        popup = Popup(title='基因库', content=content, size_hint=(0.6, 0.6))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
