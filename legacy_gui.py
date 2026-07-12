import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import json
import os
from datetime import datetime
import threading
from PIL import Image, ImageTk

try:
    import winsound
    _HAS_SOUND = True
except ImportError:
    _HAS_SOUND = False

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gene_game import (
    Card, Game, QUEST_DEFINITIONS,
    BattleCard, BattleSystem, Enemy,
    BASES, COMPLEMENT,
)
from gene_config import (
    GENE_TEMPLATES, SKILL_GENES,
    CHROMOSOME_LAYOUT, CHROMOSOME_IDS, GENE_REGIONS,
    VITAL_GENES, PASSIVE_GENES, TRAIT_GENES,
)
from tech_config import BREEDING_CONFIG
from battle_config import (
    STAGES, INFINITY_MODE, SKILL_EFFECTS, BATTLE_CONFIG,
    STATUS_EFFECTS, ENEMY_TEMPLATES, MAPS, ENEMY_PASSIVES,
    BOSS_STAT_MULTIPLIERS,
)
from trait_config import TRAIT_CONFIG, RESEARCH_CONFIG
from tech_config import TECH_TREE
from gene_enhance_config import STAT_ENHANCE_REGIONS


_SOUND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'sounds')

_SOUND_FILES = {
    'hit': os.path.join(_SOUND_DIR, 'hit.wav'),
    'critical': os.path.join(_SOUND_DIR, 'critical.wav'),
    'skill': os.path.join(_SOUND_DIR, 'skill.wav'),
    'death': os.path.join(_SOUND_DIR, 'death.wav'),
    'victory': os.path.join(_SOUND_DIR, 'victory.wav'),
    'defeat': os.path.join(_SOUND_DIR, 'defeat.wav'),
}

def _play_sound(name):
    if not _HAS_SOUND:
        return
    path = _SOUND_FILES.get(name)
    if path and os.path.exists(path):
        try:
            winsound.PlaySound(path, winsound.SND_ASYNC | winsound.SND_NOSTOP)
        except Exception:
            pass


class GeneGameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("基因密码 - GeneCrypt")
        self.root.geometry("1400x950")
        self.root.configure(bg="#1a1a2e")
        
        self._poison_img = None
        try:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'effects', 'poison_mist.png')
            if os.path.exists(path):
                self._poison_img = tk.PhotoImage(file=path)
        except Exception:
            pass
        
        self._enemy_sprites = {}
        self._enemy_sprite_map = {}
        try:
            _sd = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'enemies')
            if os.path.exists(_sd):
                _files = [f for f in os.listdir(_sd) if f.endswith('.png') and f.count('_') >= 1 and f.rsplit('_', 1)[1][0].isdigit()]
                _by_tid = {}
                for _f in _files:
                    _base = _f.rsplit('_', 1)[0]
                    _frame_str = _f.rsplit('_', 1)[1][:-4]
                    if _frame_str.isdigit():
                        _by_tid.setdefault(_base, {})[int(_frame_str)] = _f
                for _tid, _frames in _by_tid.items():
                    try:
                        _imgs = []
                        for _frame_idx in sorted(_frames):
                            _fp = os.path.join(_sd, _frames[_frame_idx])
                            _imgs.append(tk.PhotoImage(file=_fp))
                        self._enemy_sprites[_tid] = _imgs
                        if _tid in ENEMY_TEMPLATES:
                            self._enemy_sprite_map[ENEMY_TEMPLATES[_tid]['name']] = _tid
                    except Exception:
                        pass
        except Exception:
            pass
        
        self._player_card_sprites = []
        try:
            if self._enemy_sprites:
                self._player_card_sprites = list(self._enemy_sprites.values())
        except Exception:
            pass
        
        self._block_library = {}
        self._composed_cache = {}
        try:
            _sd = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'enemies')
            for _tid, _imgs in self._enemy_sprites.items():
                self._block_library[_tid] = {}
                for _frame_idx in range(len(_imgs)):
                    _fp = os.path.join(_sd, f'{_tid}_{_frame_idx}.png')
                    if os.path.exists(_fp):
                        _pil = Image.open(_fp).convert('RGBA')
                        _raw = _pil.tobytes()
                        _blocks = []
                        for _row in range(8):
                            for _col in range(8):
                                _block = bytearray()
                                for _dy in range(4):
                                    _si = ((_row * 4 + _dy) * 32 + _col * 4) * 4
                                    _block.extend(_raw[_si:_si + 16])
                                _blocks.append(bytes(_block))
                        self._block_library[_tid][_frame_idx] = _blocks
        except Exception:
            pass
        
        self.game = Game()
        self.selected_card = None
        
        self.continuous_mode = False
        self.continuous_count = 0
        self.continuous_total_gacha = 0
        self.continuous_total_materials = 0
        self.fast_mode = False
        
        self.setup_styles()
        self.create_ui()
        
        self.root.after(100, self.update_breeding_progress)
        self.root.after(30000, self._auto_save)
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TNotebook', background='#1a1a2e', foreground='#00d9ff')
        style.configure('TNotebook.Tab', background='#16213e', foreground='#00d9ff', padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', '#0f3460')])
        
        style.configure('TFrame', background='#1a1a2e')
        style.configure('Card.TFrame', background='#16213e', relief='raised', borderwidth=2)
        
        style.configure('TLabel', background='#1a1a2e', foreground='#ffffff')
        style.configure('Title.TLabel', font=('微软雅黑', 16, 'bold'), foreground='#00d9ff')
        style.configure('Info.TLabel', font=('微软雅黑', 11), foreground='#aaaaaa')
        
        style.configure('TButton', background='#0f3460', foreground='#00d9ff', borderwidth=1)
        style.map('TButton', background=[('active', '#16213e')])
    
    def _compose_sprite(self, genome, frame=0):
        _key = (tuple(genome), frame)
        if _key in self._composed_cache:
            return self._composed_cache[_key]
        _raw = bytearray(32 * 32 * 4)
        for _pos in range(64):
            _src = genome[_pos]
            _blk = self._block_library.get(_src, {}).get(frame)
            if _blk is None:
                continue
            _row, _col = _pos // 8, _pos % 8
            for _dy in range(4):
                _si = _dy * 16
                _di = ((_row * 4 + _dy) * 32 + _col * 4) * 4
                _raw[_di:_di + 16] = _blk[_pos][_si:_si + 16]
        _pil = Image.frombytes('RGBA', (32, 32), bytes(_raw))
        _tk_img = ImageTk.PhotoImage(_pil)
        self._composed_cache[_key] = _tk_img
        return _tk_img

    def _compose_sprite_frames(self, genome):
        _key = ('anim', tuple(genome))
        if _key in self._composed_cache:
            return self._composed_cache[_key]
        _max_frames = 1
        for _pos in range(64):
            _src = genome[_pos]
            _fd = self._block_library.get(_src, {})
            if _fd:
                _max_frames = max(_max_frames, max(_fd.keys()) + 1)
        _frames = [self._compose_sprite(genome, frame=_f) for _f in range(_max_frames)]
        self._composed_cache[_key] = _frames
        return _frames

    # ── 任务系统 UI ──
    CATEGORY_MAP = {'main':'主线','side':'支线','challenge':'挑战'}
    CATEGORY_KEYS = ['main','side','challenge']

    def create_quest_ui(self):
        self.quest_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.quest_tab, text='任务')
        _container = tk.Frame(self.quest_tab, bg='#1a1a2e')
        _container.pack(fill='both', expand=True, padx=10, pady=10)
        tk.Label(_container, text='📋 任务系统', font=('微软雅黑', 18, 'bold'),
                 fg='#ffd700', bg='#1a1a2e').pack(pady=5)
        _mid = tk.Frame(_container, bg='#1a1a2e')
        _mid.pack(fill='both', expand=True)
        # ── Category selector (vertical left) ──
        _cat_frame = tk.Frame(_mid, bg='#1a1a2e', width=70)
        _cat_frame.pack(side='left', fill='y')
        _cat_frame.pack_propagate(False)
        self._quest_category = tk.StringVar(value='main')
        self._cat_buttons = {}
        for _cat_key in self.CATEGORY_KEYS:
            _cat_name = self.CATEGORY_MAP[_cat_key]
            _colors = {'main': ['#4a9eff','#1a3a7a'], 'side': ['#4ade80','#1a4a2a'], 'challenge': ['#fb923c','#4a2a1a']}
            _fg, _bg = _colors[_cat_key]
            _btn = tk.Button(_cat_frame, text=_cat_name, font=('微软雅黑', 11, 'bold'),
                             fg=_fg, bg=_bg, bd=1, relief='solid', cursor='hand2',
                             activeforeground='#ffffff', activebackground=_fg,
                             command=lambda k=_cat_key: self._switch_category(k))
            _btn.pack(fill='x', padx=4, pady=3)
            self._cat_buttons[_cat_key] = _btn
        self._update_cat_buttons()
        # ── Quest list canvas ──
        _left = tk.Frame(_mid, bg='#1a1a2e', width=340)
        _left.pack(side='left', fill='y')
        _left.pack_propagate(False)
        self._quest_canvas = tk.Canvas(_left, bg='#16213e', highlightthickness=0)
        _vbar = tk.Scrollbar(_left, orient='vertical', command=self._quest_canvas.yview)
        self._quest_canvas.configure(yscrollcommand=_vbar.set)
        _vbar.pack(side='right', fill='y')
        self._quest_canvas.pack(side='left', fill='both', expand=True)
        self._quest_inner = tk.Frame(self._quest_canvas, bg='#16213e')
        self._quest_canvas.create_window((0, 0), window=self._quest_inner, anchor='nw', tags='inner')
        def _on_conf(e):
            self._quest_canvas.configure(scrollregion=self._quest_canvas.bbox('all'))
        self._quest_inner.bind('<Configure>', _on_conf)
        # ── Right: detail panel ──
        self._quest_detail = tk.Frame(_mid, bg='#0f3460', bd=2, relief='solid')
        self._quest_detail.pack(side='right', fill='both', expand=True, padx=(10, 0))
        self._selected_qid = None
        self._show_quest_detail(None)
        self._refresh_quest_list()

    def _switch_category(self, cat_key):
        self._quest_category.set(cat_key)
        self._update_cat_buttons()
        self._selected_qid = None
        self._show_quest_detail(None)
        self._refresh_quest_list()

    def _update_cat_buttons(self):
        _cur = self._quest_category.get()
        for _k, _btn in self._cat_buttons.items():
            if _k == _cur:
                _btn.config(bd=2, relief='sunken', bg='#0f3460', fg='#ffffff')
            else:
                _colors = {'main': ['#4a9eff','#1a3a7a'], 'side': ['#4ade80','#1a4a2a'], 'challenge': ['#fb923c','#4a2a1a']}
                _btn.config(bd=1, relief='solid', fg=_colors[_k][0], bg=_colors[_k][1])

    def _show_quest_detail(self, qid):
        for w in self._quest_detail.winfo_children():
            w.destroy()
        if qid is None:
            tk.Label(self._quest_detail, text='点击左侧任务查看详情', font=('微软雅黑', 14),
                     fg='#666666', bg='#0f3460').pack(expand=True)
            return
        qd = next(q for q in QUEST_DEFINITIONS if q['id'] == qid)
        qid_ = qd['id']
        is_locked = not self.game._is_quest_unlocked(qid_)
        is_claimed = qid_ in self.game.quest_claimed
        is_completed = qid_ in self.game.quest_completed
        progress = self.game.quest_progress.get(qid_, 0)
        target = qd['target']
        pct = min(progress / target, 1.0) if target > 0 else 0
        _color = '#888888' if (is_claimed or is_locked) else '#ffffff'
        _title = qd['title']
        if is_locked:
            _title = '🔒 ' + _title
        elif is_claimed:
            _title = '✅ ' + _title
        elif is_completed:
            _title = '🎯 ' + _title
        else:
            _title = '▶ ' + _title
        # Title
        tk.Label(self._quest_detail, text=_title, font=('微软雅黑', 16, 'bold'),
                 fg=_color, bg='#0f3460').pack(pady=(20, 10))
        # Description
        _desc_frame = tk.Frame(self._quest_detail, bg='#16213e', bd=1, relief='solid')
        _desc_frame.pack(fill='x', padx=20, pady=5)
        tk.Label(_desc_frame, text=qd['description'], font=('微软雅黑', 11),
                 fg='#aaaaaa', bg='#16213e', wraplength=350).pack(padx=10, pady=10)
        if is_locked:
            _req_ids = qd.get('requires', [])
            _req_names = []
            for _rid in _req_ids:
                _rqd = next((q for q in QUEST_DEFINITIONS if q['id'] == _rid), None)
                if _rqd:
                    _req_names.append(_rqd['title'])
            tk.Label(self._quest_detail, text=f"🔒 需要先完成: {', '.join(_req_names)}",
                     font=('微软雅黑', 10), fg='#ff6b6b', bg='#0f3460', wraplength=350).pack(pady=10)
            return
        # Progress bar
        _pct_color = '#39ff14' if pct >= 1 else '#00d9ff'
        tk.Label(self._quest_detail, text=f"进度: {progress}/{target}",
                 font=('微软雅黑', 11, 'bold'), fg=_pct_color, bg='#0f3460').pack(pady=(10, 2))
        _bar_bg = tk.Frame(self._quest_detail, bg='#1a1a2e', height=16, width=300)
        _bar_bg.pack(pady=(0, 10))
        _bar_bg.pack_propagate(False)
        _fill = tk.Frame(_bar_bg, bg=_pct_color, height=16, width=int(300 * pct))
        _fill.pack(side='left')
        # Rewards
        tk.Label(self._quest_detail, text='── 奖励 ──', font=('微软雅黑', 11, 'bold'),
                 fg='#ffd700', bg='#0f3460').pack(pady=(10, 5))
        for r in qd['rewards']:
            _rt = r['type']
            if _rt == 'gacha_currency':
                _rt_text = f"🧬 基因密钥 ×{r['amount']}"
            elif _rt == 'battle_materials':
                _rt_text = f"🧱 战斗材料 ×{r['amount']}"
            elif _rt == 'card_with_skills':
                _rt_text = f"🃏 新卡牌(技能: {'+'.join(r.get('skill_names', []))})"
            else:
                _rt_text = f"其他奖励"
            tk.Label(self._quest_detail, text=_rt_text, font=('微软雅黑', 10),
                     fg='#00d9ff', bg='#0f3460').pack(pady=2)
        # Action button
        if is_claimed:
            tk.Label(self._quest_detail, text='✅ 已领取', font=('微软雅黑', 12, 'bold'),
                     fg='#666666', bg='#0f3460').pack(pady=20)
        elif is_completed:
            tk.Button(self._quest_detail, text='🎁 领取奖励', font=('微软雅黑', 12, 'bold'),
                      bg='#39ff14', fg='#000000', bd=0, padx=30, pady=8,
                      activebackground='#2ecc71',
                      command=lambda q=qid_: self._claim_quest_action(q)).pack(pady=20)
        elif qd['type'] == 'submit_card':
            tk.Button(self._quest_detail, text='📤 提交卡牌', font=('微软雅黑', 12, 'bold'),
                      bg='#4a90d9', fg='#ffffff', bd=0, padx=30, pady=8,
                      activebackground='#357abd',
                      command=lambda q=qid_: self._open_submit_card_dialog(q)).pack(pady=20)
        # Category label
        _cat_name = self.CATEGORY_MAP.get(qd.get('category', ''), '')
        _cc = {'main':'#4a9eff','side':'#4ade80','challenge':'#fb923c'}.get(qd.get('category', ''), '#888888')
        tk.Label(self._quest_detail, text=f"[{_cat_name}]", font=('微软雅黑', 10, 'bold'),
                 fg=_cc, bg='#0f3460').pack(side='bottom', pady=(0, 10))

    def _refresh_quest_list(self):
        _cat = self._quest_category.get()
        for w in self._quest_inner.winfo_children():
            w.destroy()
        _locked = []
        _active = []
        _completed = []
        _claimed = []
        for qd in QUEST_DEFINITIONS:
            if qd.get('category') != _cat:
                continue
            qid = qd['id']
            if qid not in self.game.quest_progress:
                self.game.quest_progress[qid] = self.game._get_quest_progress(qid)
            if qid in self.game.quest_claimed:
                _claimed.append(qd)
            elif qid in self.game.quest_completed:
                _completed.append(qd)
            elif self.game._is_quest_unlocked(qid):
                _active.append(qd)
            else:
                _locked.append(qd)
        for label, items, color in [
            ('── 进行中 ──', _active, '#00d9ff'),
            ('── 可领取 ──', _completed, '#39ff14'),
            ('── 未解锁 ──', _locked, '#666666'),
            ('── 已完成 ──', _claimed, '#555555'),
        ]:
            if items:
                tk.Label(self._quest_inner, text=label, font=('微软雅黑', 10, 'bold'),
                         fg=color, bg='#16213e').pack(pady=(8, 2))
                for qd in items:
                    self._build_quest_row(qd, qd['id'] in self.game.quest_claimed,
                                          qd['id'] not in self.game.quest_completed and not self.game._is_quest_unlocked(qd['id']))

    def _build_quest_row(self, qd, claimed=False, locked=False):
        qid = qd['id']
        progress = self.game.quest_progress.get(qid, 0)
        target = qd['target']
        pct = min(progress / target, 1.0) if target > 0 else 0
        _is_sel = (self._selected_qid == qid)
        _bg = '#1a3a5c' if _is_sel else '#0f3460'
        _bg_hover = '#1a4a6c' if _is_sel else '#16213e'
        if locked:
            _prefix = '🔒 '
            _color = '#666666'
        elif claimed:
            _prefix = '✅ '
            _color = '#888888'
        elif qid in self.game.quest_completed:
            _prefix = '🎯 '
            _color = '#39ff14'
        else:
            _prefix = '▶ ' if self.game._is_quest_unlocked(qid) else '🔒 '
            _color = '#ffffff'
        _pct_text = ''
        if not locked and not claimed:
            _pct_color = '#39ff14' if progress >= target else '#ffd93d'
            _pct_text = f"  {progress}/{target}"
        def _on_click():
            self._selected_qid = qid
            self._show_quest_detail(qid)
            self._refresh_quest_list()
        _row = tk.Button(self._quest_inner, text=_prefix + qd['title'] + _pct_text,
                         font=('微软雅黑', 10, 'bold'), fg=_color, bg=_bg,
                         activeforeground=_color, activebackground=_bg_hover,
                         bd=1, relief='solid', cursor='hand2',
                         anchor='w', padx=10, pady=6,
                         command=_on_click)
        _row.pack(fill='x', padx=8, pady=2)

    def _claim_quest_action(self, qid):
        msgs, err = self.game.claim_quest(qid)
        if err:
            messagebox.showwarning('领取失败', err)
            return
        _text = '\n'.join(f'• {m}' for m in msgs)
        messagebox.showinfo('🎉 领取成功', f'获得奖励:\n{_text}')
        # Next quest in same category chain — select it
        _next_qid = None
        _qd = next((q for q in QUEST_DEFINITIONS if q['id'] == qid), None)
        if _qd:
            _cat = _qd.get('category', '')
            _found = False
            for q in QUEST_DEFINITIONS:
                if q['id'] == qid:
                    _found = True
                    continue
                if _found and q.get('category') == _cat:
                    _next_qid = q['id']
                    break
        self._selected_qid = _next_qid
        self._show_quest_detail(_next_qid)
        self._refresh_quest_list()
        self.refresh_card_list()
        self.update_breeding_combos()
        if hasattr(self, 'gacha_currency_label'):
            self.gacha_currency_label.config(text=str(self.game.gacha_currency))
        if hasattr(self, 'battle_materials_label'):
            self.battle_materials_label.config(text=f"🧱 战斗材料: {self.game.battle_materials}")

    def _open_submit_card_dialog(self, qid):
        qd = next(q for q in QUEST_DEFINITIONS if q['id'] == qid)
        req = qd.get('requirements', {})
        alive = [c for c in self.game.cards if c.is_alive]
        if not alive:
            messagebox.showwarning('无卡牌', '没有存活的卡牌可以提交')
            return
        _win = tk.Toplevel(self.root)
        _win.title(f"提交卡牌 - {qd['title']}")
        _win.configure(bg='#1a1a2e')
        _win.geometry('400x500')
        _win.transient(self.root)
        _win.grab_set()
        tk.Label(_win, text='选择要提交的卡牌:', font=('微软雅黑', 12, 'bold'),
                 fg='#ffffff', bg='#1a1a2e').pack(pady=10)
        _list_frame = tk.Frame(_win, bg='#1a1a2e')
        _list_frame.pack(fill='both', expand=True, padx=10)
        _canv = tk.Canvas(_list_frame, bg='#16213e', highlightthickness=0)
        _bar = tk.Scrollbar(_list_frame, orient='vertical', command=_canv.yview)
        _canv.configure(yscrollcommand=_bar.set)
        _bar.pack(side='right', fill='y')
        _canv.pack(side='left', fill='both', expand=True)
        _inner = tk.Frame(_canv, bg='#16213e')
        _canv.create_window((0, 0), window=_inner, anchor='nw', tags='inner')
        def _on_conf(e):
            _canv.configure(scrollregion=_canv.bbox('all'))
        _inner.bind('<Configure>', _on_conf)
        for c in alive:
            traits = c.traits
            _ok = True
            if 'min_atk' in req and traits.get('attack', 0) < req['min_atk']:
                _ok = False
            if 'min_hp' in req and traits.get('health', 0) < req['min_hp']:
                _ok = False
            if 'min_def' in req and traits.get('defense', 0) < req['min_def']:
                _ok = False
            if 'min_spd' in req and traits.get('speed', 0) < req['min_spd']:
                _ok = False
            _fg = '#39ff14' if _ok else '#888888'
            _text = f"{'♂' if c.gender=='male' else '♀'} {c.name}  HP:{traits.get('health',0)} ATK:{traits.get('attack',0)} DEF:{traits.get('defense',0)} SPD:{traits.get('speed',0)}"
            if _ok:
                _btn = tk.Button(_inner, text=_text, font=('Consolas', 9), fg=_fg,
                                 bg='#0f3460', bd=1, anchor='w', padx=5, pady=3,
                                 command=lambda card=c: self._do_submit_card(qid, card, _win))
                _btn.pack(fill='x', padx=5, pady=2)
            else:
                tk.Label(_inner, text=f"{_text} ❌", font=('Consolas', 9), fg=_fg,
                         bg='#16213e', anchor='w').pack(fill='x', padx=5, pady=2)
        tk.Button(_win, text='取消', font=('微软雅黑', 10), bg='#e74c3c', fg='#ffffff',
                  bd=0, padx=20, pady=5, command=_win.destroy).pack(pady=10)

    def _do_submit_card(self, qid, card, win):
        self.game.quest_progress[qid] = 1
        _new = self.game._check_all_quests()
        win.destroy()
        messagebox.showinfo('提交成功', f'已提交 [{card.name}] 完成任务 [{next(q["title"] for q in QUEST_DEFINITIONS if q["id"]==qid)}]!')
        if _new:
            self._refresh_quest_list()
            _names = '、'.join(q['title'] for q in _new)
            messagebox.showinfo('任务完成', f"🎉 新完成: {_names}\n请领取奖励!")
        self._selected_qid = qid
        self._show_quest_detail(qid)
        self._refresh_quest_list()

    def create_ui(self):
        self.main_notebook = ttk.Notebook(self.root)
        self.main_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.card_library_tab = ttk.Frame(self.main_notebook)
        self.breeding_lab_tab = ttk.Frame(self.main_notebook)
        self.gene_engineering_tab = ttk.Frame(self.main_notebook)
        self.tech_tree_tab = ttk.Frame(self.main_notebook)
        self.gacha_tab = ttk.Frame(self.main_notebook)
        self.battle_tab = ttk.Frame(self.main_notebook)
        self.bestiary_tab = ttk.Frame(self.main_notebook)
        
        self.main_notebook.add(self.card_library_tab, text='卡牌库')
        self.main_notebook.add(self.breeding_lab_tab, text='繁殖实验室')
        self.main_notebook.add(self.gene_engineering_tab, text='基因工程')
        self.main_notebook.add(self.tech_tree_tab, text='科技树')
        self.main_notebook.add(self.gacha_tab, text='基因抽卡')
        self.main_notebook.add(self.battle_tab, text='战斗')
        self.main_notebook.add(self.bestiary_tab, text='敌人图鉴')
        
        self.create_card_library()
        self.create_breeding_lab()
        self.create_gene_engineering()
        self.create_tech_tree()
        self.create_gacha_ui()
        self.create_battle_ui()
        self.create_bestiary_ui()
        self.create_quest_ui()
        
        self.main_notebook.bind('<<NotebookTabChanged>>', self._on_tab_changed)
    
    def _on_tab_changed(self, event):
        tab = event.widget.select()
        if not tab:
            return
        frame = event.widget.nametowidget(tab)
        if frame == self.gacha_tab and hasattr(self, 'gacha_currency_label'):
            self.gacha_currency_label.config(text=str(self.game.gacha_currency))
            if self._selected_pool.get():
                pid = self._selected_pool.get()
                if hasattr(self, '_pity_counter_label'):
                    pc = self.game.pity_counters.get(pid, 0)
                    self._pity_counter_label.config(text=f"{pc}/360")
                    self._pity_remaining_label.config(text=f"剩余 {max(0, 360-pc)} 抽必出传说")
    
    def create_card_library(self):
        left_frame = ttk.Frame(self.card_library_tab)
        left_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        title_label = ttk.Label(left_frame, text="卡牌库", style='Title.TLabel')
        title_label.pack(pady=10)
        
        self.card_count_label = tk.Label(left_frame, text="", font=('微软雅黑', 9),
                                         fg='#aaaaaa', bg='#16213e')
        self.card_count_label.pack(anchor='w', padx=10, pady=(0, 5))
        
        canvas = tk.Canvas(left_frame, bg='#16213e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_frame, orient='vertical', command=canvas.yview)
        self.card_list_frame = ttk.Frame(canvas)
        
        self.card_list_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.card_list_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.refresh_card_list()
        
        right_frame = ttk.Frame(self.card_library_tab)
        right_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        title_label2 = ttk.Label(right_frame, text="卡牌详情", style='Title.TLabel')
        title_label2.pack(pady=10)
        
        detail_canvas = tk.Canvas(right_frame, bg='#16213e', highlightthickness=0)
        detail_scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=detail_canvas.yview)
        self.card_detail_frame = ttk.Frame(detail_canvas, style='Card.TFrame')
        
        self.card_detail_frame.bind(
            "<Configure>",
            lambda e: detail_canvas.configure(scrollregion=detail_canvas.bbox("all"))
        )
        
        detail_canvas.create_window((0, 0), window=self.card_detail_frame, anchor='nw')
        detail_canvas.configure(yscrollcommand=detail_scrollbar.set)
        
        def on_detail_wheel(event):
            detail_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        detail_canvas.bind_all("<MouseWheel>", on_detail_wheel)
        
        detail_canvas.pack(side='left', fill='both', expand=True)
        detail_scrollbar.pack(side='right', fill='y')
        
        self.detail_labels = {}
        self.create_card_detail_ui()
    
    def create_card_detail_ui(self):
        labels_info = [
            ('name', '名称: '),
            ('gender', '性别: '),
            ('id', 'ID: '),
            ('status', '状态: '),
        ]
        
        row = 0
        for key, prefix in labels_info:
            label = ttk.Label(self.card_detail_frame, text=f"{prefix}--", style='Info.TLabel')
            label.grid(row=row, column=0, sticky='w', padx=10, pady=3)
            self.detail_labels[key] = label
            row += 1
        
        ttk.Label(self.card_detail_frame, text="属性:", style='Info.TLabel').grid(row=row, column=0, sticky='w', padx=10, pady=3)
        row += 1
        
        self.traits_frame = ttk.Frame(self.card_detail_frame)
        self.traits_frame.grid(row=row, column=0, columnspan=2, sticky='ew', padx=10)
        row += 1
        
        ttk.Label(self.card_detail_frame, text="技能:", style='Info.TLabel').grid(row=row, column=0, sticky='w', padx=10, pady=3)
        row += 1
        
        self.skills_frame = ttk.Frame(self.card_detail_frame)
        self.skills_frame.grid(row=row, column=0, columnspan=2, sticky='ew', padx=10)
        row += 1
        
        ttk.Label(self.card_detail_frame, text="基因序列:", style='Info.TLabel').grid(row=row, column=0, sticky='w', padx=10, pady=3)
        row += 1
        
        self.gene_seq_frame = ttk.Frame(self.card_detail_frame)
        self.gene_seq_frame.grid(row=row, column=0, columnspan=2, sticky='ew', padx=10)
        row += 1
        
        btn_frame = ttk.Frame(self.card_detail_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=5)
        
        self.mutate_btn = ttk.Button(btn_frame, text="射线变异", command=self.apply_radiation)
        self.mutate_btn.pack(side='left', padx=5)
        self.clone_btn = ttk.Button(btn_frame, text="克隆", command=self.clone_card_action)
        self.clone_btn.pack(side='left', padx=5)
        self.rename_btn = ttk.Button(btn_frame, text="改名", command=self.rename_card)
        self.rename_btn.pack(side='left', padx=5)
        self.report_btn = ttk.Button(btn_frame, text="基因报告", command=self.show_gene_report)
        self.report_btn.pack(side='left', padx=5)
    
    def refresh_card_list(self):
        for widget in self.card_list_frame.winfo_children():
            widget.destroy()
        
        count = len(self.game.cards)
        maxc = self.game.effective_max_cards
        ratio = count / maxc
        if ratio >= 1.0:
            count_color = '#ff4444'
        elif ratio >= 0.8:
            count_color = '#ffaa00'
        else:
            count_color = '#4ecdc4'
        self.card_count_label.config(text=f"📋 卡牌数量: {count} / {maxc}", foreground=count_color)
        
        for card in self.game.cards:
            rarity = getattr(card, '_rarity', None)
            if rarity == 'ultra':
                card_frame = tk.Frame(self.card_list_frame, bg='#16213e',
                                      highlightbackground='#ffd700', highlightthickness=2,
                                      relief='solid', borderwidth=2)
            else:
                card_frame = ttk.Frame(self.card_list_frame, style='Card.TFrame')
            card_frame.pack(fill='x', padx=5, pady=3)
            
            gender_color = "#4a90d9" if card.gender == "male" else "#e74c8c"
            status_color = "#2ecc71" if card.is_alive else "#e74c3c"
            
            _cimg = None
            if hasattr(self, '_block_library') and self._block_library and hasattr(card, 'sprite_genome') and card.sprite_genome:
                try:
                    _cimg = self._compose_sprite(card.sprite_genome)
                except Exception:
                    pass
            if _cimg:
                tk.Label(card_frame, image=_cimg, bg="#16213e",
                         borderwidth=0, highlightthickness=0).pack(side='left', padx=2)
            
            gender_label = tk.Label(card_frame, text="♂" if card.gender == "male" else "♀", 
                                    fg=gender_color, bg="#16213e", font=('Arial', 14))
            gender_label.pack(side='left', padx=5)
            
            name_label = tk.Label(card_frame, text=card.name, fg="#ffffff", bg="#16213e")
            name_label.pack(side='left', padx=5)
            
            if rarity == 'ultra':
                tk.Label(card_frame, text="★ 传说 ★", fg='#ffd700', bg='#16213e',
                         font=('微软雅黑', 9, 'bold')).pack(side='left', padx=5)
            
            status_label = tk.Label(card_frame, text="存活" if card.is_alive else "死亡",
                                    fg=status_color, bg="#16213e", font=('Arial', 10))
            status_label.pack(side='right', padx=5)
            
            del_btn = tk.Button(card_frame, text="✕", fg="#ff6b6b", bg="#16213e",
                                bd=0, font=('Arial', 10, 'bold'), cursor='hand2',
                                command=lambda c=card: self.delete_card(c))
            del_btn.pack(side='right', padx=(0, 5))
            
            card_frame.bind('<Button-1>', lambda e, c=card: self.select_card(c))
            for child in card_frame.winfo_children():
                if child is del_btn:
                    continue
                child.bind('<Button-1>', lambda e, c=card: self.select_card(c))
    
    def select_card(self, card):
        self.selected_card = card
        self.update_card_detail(card)
    
    def delete_card(self, card):
        from tkinter import messagebox
        if not messagebox.askyesno("确认删除", f"确定要删除卡牌 [{card.name}] 吗？\n此操作不可撤销。"):
            return
        if card in self.game.cards:
            self.game.cards.remove(card)
        if self.selected_card is card:
            self.selected_card = None
            for widget in self.card_detail_frame.winfo_children():
                if widget in self.detail_labels.values():
                    continue
                if widget in [self.traits_frame, self.skills_frame, self.gene_seq_frame]:
                    continue
            for widget in self.traits_frame.winfo_children():
                widget.destroy()
            for widget in self.skills_frame.winfo_children():
                widget.destroy()
            for widget in self.gene_seq_frame.winfo_children():
                widget.destroy()
        self.game.save_game()
        self.refresh_card_list()
        self.update_engineer_combos()
        self.update_breeding_combos()
    
    def update_card_detail(self, card):
        self.detail_labels['name'].config(text=f"名称: {card.name}")
        self.detail_labels['gender'].config(text=f"性别: {'雄性' if card.gender == 'male' else '雌性'}")
        self.detail_labels['id'].config(text=f"ID: {card.id}")
        status_text = f"状态: {'存活' if card.is_alive else '死亡'}"
        hv_level = self.game.tech_tree.get('hybrid_enhance', {}).get('level', 0)
        if hv_level >= 1 and len(card.parent_ids) >= 2 and card.parent_ids[0] != card.parent_ids[1]:
            status_text += " [杂种优势]"
        self.detail_labels['status'].config(text=status_text)
        
        for widget in self.traits_frame.winfo_children():
            widget.destroy()
        
        row = 0
        for trait_name, value in card.traits.items():
            config = TRAIT_CONFIG.get(trait_name, {})
            desc = config.get('description', trait_name)
            label = tk.Label(self.traits_frame, text=f"{desc}: {value}", fg="#4ecdc4", bg="#16213e", font=('微软雅黑', 10))
            label.grid(row=row, column=0, sticky='w', padx=5, pady=1)
            row += 1
        
        for widget in self.skills_frame.winfo_children():
            widget.destroy()
        
        r = 0
        if card.skills:
            for skill in card.skills:
                label = tk.Label(self.skills_frame, text=f"  ✦ {skill}", fg="#ffd93d", bg="#16213e", font=('微软雅黑', 10))
                label.grid(row=r, column=0, sticky='w', padx=5, pady=1)
                r += 1
        
        if card.passive_skills:
            sep = tk.Label(self.skills_frame, text="── 被动技能 ──", fg="#888888", bg="#16213e", font=('微软雅黑', 9))
            sep.grid(row=r, column=0, sticky='w', padx=5, pady=(6, 1))
            r += 1
            for pname, pval in card.passive_skills.items():
                if pname == '荆棘':
                    ptext = f"  ⚡ {pname} ({pval}%反伤)"
                elif pname == '条件反射':
                    bound = getattr(card, 'reflex_bound_skill', None)
                    ptext = f"  ⚡ {pname} [{bound}]" if bound else f"  ⚡ {pname}"
                else:
                    ptext = f"  ⚡ {pname}"
                label = tk.Label(self.skills_frame, text=ptext, fg="#ff6b6b", bg="#16213e", font=('微软雅黑', 10, 'bold'))
                label.grid(row=r, column=0, sticky='w', padx=5, pady=1)
                r += 1
        
        if not card.skills and not card.passive_skills:
            label = tk.Label(self.skills_frame, text="无", fg="#666666", bg="#16213e", font=('微软雅黑', 10))
            label.pack(anchor='w', padx=5)
        
        for widget in self.gene_seq_frame.winfo_children():
            widget.destroy()
        
        row = 0
        
        gene_mapped = self.game.tech_tree.get('gene_mapping', {}).get('level', 0) > 0
        
        for chr_id in CHROMOSOME_IDS:
            if chr_id == 'chrY' and card.gender != 'male':
                continue
            chr_conf = CHROMOSOME_LAYOUT.get(chr_id, {})
            chr_name = chr_conf.get('name', chr_id)
            
            if chr_id == 'chrX':
                sex_type = card.chromosomes.get('chrX', [{}, {}])[1].get('type', 'X')
                chr_label = tk.Label(self.gene_seq_frame,
                                     text=f"══ {chr_name} ({'XX' if sex_type=='X' else 'XY'}) ══",
                                     fg="#ff6b6b", bg="#16213e", font=('Consolas', 9, 'bold'))
            else:
                chr_label = tk.Label(self.gene_seq_frame,
                                     text=f"══ {chr_name} ══",
                                     fg="#ff6b6b", bg="#16213e", font=('Consolas', 9, 'bold'))
            chr_label.grid(row=row, column=0, sticky='w', padx=5, pady=3)
            row += 1
            
            if chr_id == 'chrX':
                chr_regions = GENE_REGIONS['chrX'] + (GENE_REGIONS['chrY'] if card.gender == 'male' else [])
            else:
                chr_regions = GENE_REGIONS.get(chr_id, [])
            
            for gene_name, start, end in chr_regions:
                gene_data = card.genes.get(gene_name)
                if not gene_data:
                    continue
                template = GENE_TEMPLATES.get(gene_name, {})
                desc = template.get('description', gene_name)
                genotype = card.get_genotype(gene_name)
                allele1 = gene_data['allele1']['seq']
                allele2 = gene_data['allele2']['seq']
                methylated = gene_data['methylated']
                research = gene_data.get('research_count', 0)
                
                isolated = getattr(card, 'isolated_genes', set())
                iso_indicator = " [隔离]" if gene_name in isolated else ""
                methyl_indicator = " [甲基化]" if methylated else ""
                research_indicator = f" (研究:{research}/{RESEARCH_CONFIG['reveal_threshold']})" if research < RESEARCH_CONFIG['reveal_threshold'] else " [已研究]"
                coord_str = f" ({start}-{end})" if gene_mapped else ""
                
                gene_label = tk.Label(self.gene_seq_frame,
                                       text=f"  {desc}{coord_str} [{genotype}]: {allele1}/{allele2}{methyl_indicator}{iso_indicator}{research_indicator}",
                                       fg="#00d9ff" if not methylated else "#ff6b6b",
                                       bg="#16213e", font=('Consolas', 9))
                gene_label.grid(row=row, column=0, sticky='w', padx=5, pady=2)
                row += 1
        
        has_mut_study = self.game.tech_tree.get('mutation_study', {}).get('unlocked', False)
        has_clone = self.game.tech_tree.get('clone_tech', {}).get('unlocked', False)
        if card.is_alive:
            self.mutate_btn.config(state='normal' if has_mut_study else 'disabled')
            self.clone_btn.config(state='normal' if has_clone else 'disabled')
        else:
            self.mutate_btn.config(state='disabled')
            self.clone_btn.config(state='disabled')
    
    def create_breeding_lab(self):
        title_label = ttk.Label(self.breeding_lab_tab, text="繁殖实验室", style='Title.TLabel')
        title_label.pack(pady=10)
        
        info_frame = ttk.Frame(self.breeding_lab_tab)
        info_frame.pack(fill='x', padx=20, pady=5)
        
        self.breed_speed_label = ttk.Label(info_frame, text=f"繁殖速度: {self.game.breed_speed_multiplier}x")
        self.breed_speed_label.pack(side='left')
        
        select_frame = ttk.Frame(self.breeding_lab_tab)
        select_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(select_frame, text="选择雄性卡牌:").pack(side='left')
        self.male_combo = ttk.Combobox(select_frame, width=20)
        self.male_combo.pack(side='left', padx=5)
        
        ttk.Label(select_frame, text="选择雌性卡牌:").pack(side='left', padx=20)
        self.female_combo = ttk.Combobox(select_frame, width=20)
        self.female_combo.pack(side='left', padx=5)
        
        ttk.Button(select_frame, text="开始繁殖", command=self.start_breeding).pack(side='left', padx=20)
        
        self.auto_breed_btn = ttk.Button(select_frame, text="自动繁殖", command=self.toggle_auto_breeding)
        self.auto_breed_btn.pack(side='left', padx=10)

        # IVF section
        self.ivf_frame = ttk.LabelFrame(self.breeding_lab_tab, text="体外受精")
        self.ivf_frame.pack(fill='x', padx=20, pady=5)

        ivf_btn_frame = ttk.Frame(self.ivf_frame)
        ivf_btn_frame.pack(pady=5)
        ttk.Button(ivf_btn_frame, text="提取精子 (♂)", command=self.extract_sperm_action).pack(side='left', padx=4)
        ttk.Button(ivf_btn_frame, text="提取卵子 (♀)", command=self.extract_egg_action).pack(side='left', padx=4)
        ttk.Button(ivf_btn_frame, text="体外受精", command=self.fuse_gametes_action).pack(side='left', padx=4)

        self.sperm_label = ttk.Label(self.ivf_frame, text="精子: 未提取", style='Info.TLabel')
        self.sperm_label.pack(anchor='w', padx=10)
        self.egg_label = ttk.Label(self.ivf_frame, text="卵子: 未提取", style='Info.TLabel')
        self.egg_label.pack(anchor='w', padx=10)
        self.sperm_gamete = None
        self.egg_gamete = None
        self.sperm_card_id = None
        self.egg_card_id = None

        self.breeding_info_frame = ttk.Frame(self.breeding_lab_tab)
        self.breeding_info_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.breeding_progress_frame = ttk.LabelFrame(self.breeding_lab_tab, text="繁殖进度")
        self.breeding_progress_frame.pack(fill='x', padx=20, pady=10)
        
        self.breeding_progress_label = ttk.Label(self.breeding_progress_frame, text="无进行中的繁殖")
        self.breeding_progress_label.pack(pady=10)
        
        self.update_breeding_combos()
    
    def update_breeding_combos(self):
        male_cards = [c for c in self.game.cards if c.gender == 'male' and c.is_alive]
        female_cards = [c for c in self.game.cards if c.gender == 'female' and c.is_alive]
        
        self.male_combo['values'] = [f"{c.name} ({c.id})" for c in male_cards]
        self.female_combo['values'] = [f"{c.name} ({c.id})" for c in female_cards]
    
    def start_breeding(self):
        male_idx = self.male_combo.current()
        female_idx = self.female_combo.current()
        
        if male_idx < 0 or female_idx < 0:
            messagebox.showwarning("警告", "请选择雄性和雌性卡牌")
            return
        
        male_cards = [c for c in self.game.cards if c.gender == 'male' and c.is_alive]
        female_cards = [c for c in self.game.cards if c.gender == 'female' and c.is_alive]
        
        card1 = male_cards[male_idx]
        card2 = female_cards[female_idx]
        
        def on_breeding_complete():
            child_chromosomes, child_gender = self.game.breeding(card1, card2)
            child_name = f"子代{Card.card_count}"
            child = self.game.create_card(child_name, chromosomes=child_chromosomes, parent_ids=[card1.id, card2.id])
            
            if child and getattr(card1, 'sprite_genome', None) and getattr(card2, 'sprite_genome', None):
                _p = list(range(64))
                random.shuffle(_p)
                _g = [None] * 64
                for _i, _pos in enumerate(_p):
                    _g[_pos] = (card1.sprite_genome[_pos] if _i < 32 else card2.sprite_genome[_pos])
                child.sprite_genome = _g
            
            if child:
                messagebox.showinfo("繁殖成功", f"成功繁殖新卡牌: {child.name}\n性别: {'雄性' if child.gender == 'male' else '雌性'}\n技能: {', '.join(child.skills) if child.skills else '无'}")
                _new_q = self.game._check_all_quests()
                if _new_q:
                    self._refresh_quest_list()
                    _names = '、'.join(q['title'] for q in _new_q)
                    messagebox.showinfo("任务完成", f"🎉 完成任务: {_names}\n请前往[任务]页领取奖励!")
            else:
                messagebox.showerror("繁殖失败", "繁殖过程中出现问题，新生卡牌死亡")
            
            self.refresh_card_list()
            self.update_breeding_combos()
            self.update_engineer_combos()
        
        self.game.add_breeding_task(card1, card2, on_breeding_complete)
        messagebox.showinfo("开始繁殖", f"繁殖已开始，预计时间: {BREEDING_CONFIG['base_duration'] / self.game.breed_speed_multiplier:.1f}秒")
    
    def update_breeding_progress(self):
        self.game.update_breeding()
        
        if self.game.auto_breeding and not self.game.breeding_queue:
            self._auto_breed()
        
        if self.game.breeding_queue:
            task = self.game.breeding_queue[0]
            elapsed = time.time() - task['start_time']
            progress = min(elapsed / task['duration'] * 100, 100)
            label = "自动" if self.game.auto_breeding else ""
            self.breeding_progress_label.config(text=f"{label}繁殖中... {progress:.1f}%")
        else:
            self.breeding_progress_label.config(text="无进行中的繁殖")
        
        has_auto = self.game.tech_tree.get('auto_breeding', {}).get('unlocked', False)
        if hasattr(self, 'auto_breed_btn'):
            if has_auto:
                self.auto_breed_btn.config(state='normal')
            else:
                self.auto_breed_btn.config(state='disabled')
        
        has_ivf = self._check_tech('ivf_tech')
        if hasattr(self, 'ivf_frame'):
            self.ivf_frame.config(text="体外受精" if has_ivf else "体外受精 (未解锁)")
            for child in self.ivf_frame.winfo_children():
                if isinstance(child, ttk.Frame):
                    for btn in child.winfo_children():
                        if isinstance(btn, ttk.Button):
                            btn.config(state='normal' if has_ivf else 'disabled')
        
        speed = self.game.get_breed_speed()
        self.breed_speed_label.config(text=f"繁殖速度: {speed}x")
        
        self.root.after(100, self.update_breeding_progress)
    
    def toggle_auto_breeding(self):
        self.game.auto_breeding = not self.game.auto_breeding
        if self.game.auto_breeding:
            self.auto_breed_btn.config(text="自动繁殖 (开)")
            if not self.game.breeding_queue:
                self._auto_breed()
        else:
            self.auto_breed_btn.config(text="自动繁殖 (关)")
    
    def _auto_breed(self):
        male_cards = [c for c in self.game.cards if c.gender == 'male' and c.is_alive]
        female_cards = [c for c in self.game.cards if c.gender == 'female' and c.is_alive]
        if not male_cards or not female_cards:
            self.game.auto_breeding = False
            self.auto_breed_btn.config(text="自动繁殖 (关)")
            self.breeding_progress_label.config(text="自动繁殖中止: 缺少雌性或雄性卡牌")
            return
        
        card1 = random.choice(male_cards)
        card2 = random.choice(female_cards)
        
        def on_complete():
            child_chromosomes, child_gender = self.game.breeding(card1, card2)
            child_name = f"子代{Card.card_count}"
            child = self.game.create_card(child_name, chromosomes=child_chromosomes, parent_ids=[card1.id, card2.id])
            if child and getattr(card1, 'sprite_genome', None) and getattr(card2, 'sprite_genome', None):
                _p = list(range(64))
                random.shuffle(_p)
                _g = [None] * 64
                for _i, _pos in enumerate(_p):
                    _g[_pos] = (card1.sprite_genome[_pos] if _i < 32 else card2.sprite_genome[_pos])
                child.sprite_genome = _g
            self.game._check_all_quests()
            self.refresh_card_list()
            self.update_breeding_combos()
            self.update_engineer_combos()
        
        self.game.add_breeding_task(card1, card2, on_complete)
    
    def create_gene_engineering(self):
        title_label = ttk.Label(self.gene_engineering_tab, text="基因工程实验室", style='Title.TLabel')
        title_label.pack(pady=10)
        
        control_frame = ttk.Frame(self.gene_engineering_tab)
        control_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(control_frame, text="选择卡牌:").pack(side='left')
        self.engineer_card_combo = ttk.Combobox(control_frame, width=18)
        self.engineer_card_combo.pack(side='left', padx=5)
        
        ttk.Label(control_frame, text="目标卡牌:").pack(side='left', padx=(20, 0))
        self.engineer_target_combo = ttk.Combobox(control_frame, width=18)
        self.engineer_target_combo.pack(side='left', padx=5)
        
        ttk.Label(control_frame, text="基因:").pack(side='left', padx=(20, 0))
        self.gene_combo = ttk.Combobox(control_frame, width=16)
        self.gene_combo['values'] = list(GENE_TEMPLATES.keys())
        self.gene_combo.pack(side='left', padx=5)
        
        self.update_engineer_combos()
        
        tool_frame = ttk.LabelFrame(self.gene_engineering_tab, text="基因操作工具")
        tool_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        btn_frame = ttk.Frame(tool_frame)
        btn_frame.pack(pady=10)
        
        row_idx = 0
        ttk.Button(btn_frame, text="限制性内切酶切割", command=self.restrict_enzyme_cut).grid(row=row_idx, column=0, padx=4, pady=3, sticky='ew')
        ttk.Button(btn_frame, text="甲基化处理", command=self.apply_methylation).grid(row=row_idx, column=1, padx=4, pady=3, sticky='ew')
        ttk.Button(btn_frame, text="去甲基化", command=self.demethylation).grid(row=row_idx, column=2, padx=4, pady=3, sticky='ew')
        ttk.Button(btn_frame, text="研究此基因", command=self.research_gene_action).grid(row=row_idx, column=3, padx=4, pady=3, sticky='ew')
        ttk.Button(btn_frame, text="基因激活", command=self.activate_gene_action).grid(row=row_idx, column=4, padx=4, pady=3, sticky='ew')
        
        row_idx = 1
        ttk.Button(btn_frame, text="基因拼接 (供体→目标)", command=self.splice_gene_action).grid(row=row_idx, column=0, columnspan=2, padx=4, pady=3, sticky='ew')
        ttk.Button(btn_frame, text="CRISPR编辑", command=self.crispr_edit_action).grid(row=row_idx, column=2, padx=4, pady=3, sticky='ew')
        ttk.Button(btn_frame, text="基因敲除", command=self.knockout_gene_action).grid(row=row_idx, column=3, padx=4, pady=3, sticky='ew')
        ttk.Button(btn_frame, text="存入基因库", command=self.store_gene_action).grid(row=row_idx, column=4, padx=4, pady=3, sticky='ew')
        
        row_idx = 2
        ttk.Label(btn_frame, text="切割位置:").grid(row=row_idx, column=0, pady=3, sticky='e')
        self.cut_position_entry = ttk.Entry(btn_frame, width=8)
        self.cut_position_entry.grid(row=row_idx, column=1, pady=3, sticky='w')
        ttk.Label(btn_frame, text="CRISPR位置:").grid(row=row_idx, column=2, pady=3, sticky='e')
        self.crispr_pos_entry = ttk.Entry(btn_frame, width=8)
        self.crispr_pos_entry.grid(row=row_idx, column=3, pady=3, sticky='w')
        ttk.Label(btn_frame, text="碱基(A/T/G/C):").grid(row=row_idx, column=4, pady=3, sticky='e')
        self.crispr_base_entry = ttk.Entry(btn_frame, width=6)
        self.crispr_base_entry.grid(row=row_idx, column=5, pady=3, sticky='w')
        
        row_idx = 3
        ttk.Label(btn_frame, text="库标签:").grid(row=row_idx, column=0, pady=3, sticky='e')
        self.library_label_entry = ttk.Entry(btn_frame, width=12)
        self.library_label_entry.grid(row=row_idx, column=1, pady=3, sticky='w')
        ttk.Button(btn_frame, text="取出基因", command=self.retrieve_gene_action).grid(row=row_idx, column=2, padx=4, pady=3)
        ttk.Button(btn_frame, text="查看基因库", command=self.show_gene_library).grid(row=row_idx, column=3, padx=4, pady=3)
        
        row_idx = 4
        ttk.Button(btn_frame, text="基因隔离 (切换)", command=self.toggle_gene_isolation_action).grid(row=row_idx, column=0, padx=4, pady=3, sticky='ew')
        ttk.Label(btn_frame, text="染色体:").grid(row=row_idx, column=1, pady=3, sticky='e')
        self.chromo_duplicate_combo = ttk.Combobox(btn_frame, width=8, values=CHROMOSOME_IDS)
        self.chromo_duplicate_combo.grid(row=row_idx, column=2, pady=3, sticky='w')
        ttk.Button(btn_frame, text="染色体复制 (源→目标)", command=self.duplicate_chromosome_action).grid(row=row_idx, column=3, columnspan=2, padx=4, pady=3, sticky='ew')

        self.gene_result_label = ttk.Label(tool_frame, text="", style='Info.TLabel', wraplength=700)
        self.gene_result_label.pack(pady=5)
    
    def update_engineer_combos(self):
        alive_cards = [c for c in self.game.cards if c.is_alive]
        vals = [f"{c.name} ({c.id})" for c in alive_cards]
        self.engineer_card_combo['values'] = vals
        self.engineer_target_combo['values'] = vals
        self._update_engineer_buttons()
    
    def _update_engineer_buttons(self):
        pass
    
    def restrict_enzyme_cut(self):
        if self.engineer_card_combo.current() < 0 or self.gene_combo.current() < 0:
            messagebox.showwarning("警告", "请选择卡牌和基因")
            return
        
        try:
            position = int(self.cut_position_entry.get())
        except ValueError:
            messagebox.showwarning("警告", "请输入有效的切割位置")
            return
        
        alive_cards = [c for c in self.game.cards if c.is_alive]
        card = alive_cards[self.engineer_card_combo.current()]
        gene_name = self.gene_combo.get()
        
        result, msg = self.game.restrict_enzyme_cut(gene_name, position, card)
        
        if result == 'vital_damaged':
            messagebox.showerror("操作结果", msg)
        elif result:
            messagebox.showinfo("操作结果", msg)
        else:
            messagebox.showerror("操作结果", msg)
        
        self.refresh_card_list()
        if card.is_alive:
            self.update_card_detail(card)
        elif self.selected_card and not self.selected_card.is_alive:
            self.selected_card = None
            for widget in self.gene_seq_frame.winfo_children():
                widget.destroy()
    
    def apply_methylation(self):
        if not self._check_tech('methylation_tech'):
            messagebox.showwarning("科技锁定", "需要先研发「甲基化技术」科技")
            return
        if self.engineer_card_combo.current() < 0 or self.gene_combo.current() < 0:
            messagebox.showwarning("警告", "请选择卡牌和基因")
            return
        alive_cards = [c for c in self.game.cards if c.is_alive]
        card = alive_cards[self.engineer_card_combo.current()]
        gene_name = self.gene_combo.get()
        result, msg = self.game.methylation(gene_name, card, enable=True)
        if result:
            messagebox.showinfo("操作结果", msg)
            self.refresh_card_list()
            self.update_card_detail(card)
        else:
            messagebox.showerror("操作结果", msg)
    
    def demethylation(self):
        methyl_level = self.game.tech_tree.get('methylation_tech', {}).get('level', 0)
        if methyl_level < 2:
            messagebox.showwarning("科技锁定", "需要「甲基化技术」Lv.2 才能解锁去甲基化")
            return
        if self.engineer_card_combo.current() < 0 or self.gene_combo.current() < 0:
            messagebox.showwarning("警告", "请选择卡牌和基因")
            return
        alive_cards = [c for c in self.game.cards if c.is_alive]
        card = alive_cards[self.engineer_card_combo.current()]
        gene_name = self.gene_combo.get()
        result, msg = self.game.methylation(gene_name, card, enable=False)
        if result:
            messagebox.showinfo("操作结果", msg)
            self.refresh_card_list()
            self.update_card_detail(card)
        else:
            messagebox.showerror("操作结果", msg)
    
    def demethylation(self):
        if self.engineer_card_combo.current() < 0 or self.gene_combo.current() < 0:
            messagebox.showwarning("警告", "请选择卡牌和基因")
            return
        
        alive_cards = [c for c in self.game.cards if c.is_alive]
        card = alive_cards[self.engineer_card_combo.current()]
        gene_name = self.gene_combo.get()
        
        result, msg = self.game.methylation(gene_name, card, enable=False)
        
        if result:
            messagebox.showinfo("操作结果", msg)
            self.refresh_card_list()
            self.update_card_detail(card)
        else:
            messagebox.showerror("操作结果", msg)
    
    def research_gene_action(self):
        if self.engineer_card_combo.current() < 0 or self.gene_combo.current() < 0:
            messagebox.showwarning("警告", "请选择卡牌和基因")
            return
        
        alive_cards = [c for c in self.game.cards if c.is_alive]
        card = alive_cards[self.engineer_card_combo.current()]
        gene_name = self.gene_combo.get()
        
        result = self.game.research_gene(gene_name, card)
        
        if result and isinstance(result, dict):
            info = f"基因: {result['description']}\n"
            info += f"分类: {GENE_CATEGORIES.get(result['category'], result['category'])}\n"
            if result.get('affects_trait'):
                trait_info = TRAIT_CONFIG.get(result['affects_trait'], {})
                info += f"影响属性: {trait_info.get('description', result['affects_trait'])}\n"
            if result.get('skill_name'):
                info += f"技能: {result['skill_name']}\n"
            if result.get('vital'):
                info += "类型: 关键基因（破坏会导致死亡）\n"
            
            self.gene_result_label.config(text=f"研究完成！{result['description']}")
            messagebox.showinfo("研究结果", info)
        else:
            gene_data = card.genes[gene_name]
            count = gene_data.get('research_count', 0)
            self.gene_result_label.config(text=f"研究次数: {count}/{RESEARCH_CONFIG['reveal_threshold']}")
        
        self.update_card_detail(card)
    
    def _get_engineer_card_and_gene(self):
        if self.engineer_card_combo.current() < 0 or self.gene_combo.current() < 0:
            return None, None, "请选择卡牌和基因"
        alive_cards = [c for c in self.game.cards if c.is_alive]
        if self.engineer_card_combo.current() >= len(alive_cards):
            return None, None, "卡牌不存在"
        card = alive_cards[self.engineer_card_combo.current()]
        gene_name = self.gene_combo.get()
        return card, gene_name, None
    
    def _get_engineer_target_card(self):
        if self.engineer_target_combo.current() < 0:
            return None, "请选择目标卡牌"
        alive_cards = [c for c in self.game.cards if c.is_alive]
        if self.engineer_target_combo.current() >= len(alive_cards):
            return None, "目标卡牌不存在"
        return alive_cards[self.engineer_target_combo.current()], None
    
    def _check_tech(self, tech_name):
        tech = self.game.tech_tree.get(tech_name, {})
        return tech.get('unlocked', False) and tech.get('level', 0) > 0

    def activate_gene_action(self):
        if not self._check_tech('gene_activate'):
            messagebox.showwarning("科技锁定", "需要先研发「基因激活」科技")
            return
        card, gene_name, err = self._get_engineer_card_and_gene()
        if err:
            messagebox.showwarning("警告", err)
            return
        result, msg = self.game.activate_gene(gene_name, card)
        if result:
            messagebox.showinfo("基因激活", msg)
            self.update_card_detail(card)
        else:
            messagebox.showerror("基因激活失败", msg)
    
    def splice_gene_action(self):
        if not self._check_tech('gene_splicing'):
            messagebox.showwarning("科技锁定", "需要先研发「基因拼接」科技")
            return
        donor, gene_name, err = self._get_engineer_card_and_gene()
        if err:
            messagebox.showwarning("警告", err)
            return
        target, err2 = self._get_engineer_target_card()
        if err2:
            messagebox.showwarning("警告", err2)
            return
        result, msg = self.game.splice_gene(gene_name, donor, target)
        if result:
            messagebox.showinfo("基因拼接", msg)
            self.refresh_card_list()
            self.update_card_detail(target)
        else:
            messagebox.showerror("拼接失败", msg)
    
    def crispr_edit_action(self):
        if not self._check_tech('crispr_tech'):
            messagebox.showwarning("科技锁定", "需要先研发「CRISPR编辑」科技")
            return
        card, gene_name, err = self._get_engineer_card_and_gene()
        if err:
            messagebox.showwarning("警告", err)
            return
        try:
            position = int(self.crispr_pos_entry.get())
        except ValueError:
            messagebox.showwarning("警告", "请输入有效的CRISPR编辑位置")
            return
        new_base = self.crispr_base_entry.get().strip().upper()
        if new_base not in BASES:
            messagebox.showwarning("警告", "碱基必须是 A, T, G, 或 C")
            return
        result, msg = self.game.crispr_edit(gene_name, card, position, new_base)
        if result == 'vital_damaged':
            messagebox.showerror("CRISPR编辑", msg)
        elif result:
            messagebox.showinfo("CRISPR编辑", msg)
            self.update_card_detail(card)
        else:
            messagebox.showerror("CRISPR编辑失败", msg)
        self.refresh_card_list()
    
    def knockout_gene_action(self):
        crispr_level = self.game.tech_tree.get('crispr_tech', {}).get('level', 0)
        if crispr_level < 3:
            messagebox.showwarning("科技锁定", "需要「CRISPR编辑」Lv.3 才能解锁基因敲除")
            return
        card, gene_name, err = self._get_engineer_card_and_gene()
        if err:
            messagebox.showwarning("警告", err)
            return
        result, msg = self.game.gene_knockout(gene_name, card)
        if result:
            messagebox.showinfo("基因敲除", msg)
            self.update_card_detail(card)
        else:
            messagebox.showerror("敲除失败", msg)
        self.refresh_card_list()
    
    def store_gene_action(self):
        if not self._check_tech('gene_library'):
            messagebox.showwarning("科技锁定", "需要先研发「基因库」科技")
            return
        card, gene_name, err = self._get_engineer_card_and_gene()
        if err:
            messagebox.showwarning("警告", err)
            return
        label = self.library_label_entry.get().strip() or None
        result, msg = self.game.store_gene_fragment(gene_name, card, label)
        if result:
            messagebox.showinfo("基因库", msg)
        else:
            messagebox.showerror("存储失败", msg)
        self.game.save_game()
    
    def retrieve_gene_action(self):
        if not self._check_tech('gene_library'):
            messagebox.showwarning("科技锁定", "需要先研发「基因库」科技")
            return
        if not hasattr(self.game, 'gene_library'):
            self.game.gene_library = {}
        lib = self.game.gene_library
        if not lib:
            messagebox.showinfo("基因库", "基因库为空")
            return
        keys = list(lib.keys())
        from tkinter.simpledialog import askinteger
        idx = askinteger("取出基因", 
            f"基因库中共 {len(keys)} 个片段。\n输入编号 (1-{len(keys)}):\n\n" +
            "\n".join(f"{i+1}. {k}" for i, k in enumerate(keys)),
            minvalue=1, maxvalue=len(keys), parent=self.root)
        if idx is None:
            return
        key = keys[idx - 1]
        target, err2 = self._get_engineer_target_card()
        if err2:
            messagebox.showwarning("警告", err2)
            return
        result, msg = self.game.retrieve_gene_fragment(key, target)
        if result:
            messagebox.showinfo("基因库", msg)
            self.update_card_detail(target)
        else:
            messagebox.showerror("取出失败", msg)
        self.refresh_card_list()
    
    def show_gene_library(self):
        if not hasattr(self.game, 'gene_library'):
            self.game.gene_library = {}
        lib = self.game.gene_library
        if not lib:
            messagebox.showinfo("基因库", "基因库为空")
            return
        lines = [f"基因库 ({len(lib)} 个片段):"]
        for k, v in lib.items():
            lines.append(f"\n  [{k}]")
            lines.append(f"    基因: {v['gene_name']}")
            lines.append(f"    来源: {v['source_name']} ({v['source_card']})")
            lines.append(f"    等位1: {v['allele1_seq'][:30]}...")
            lines.append(f"    等位2: {v['allele2_seq'][:30]}...")
        win = tk.Toplevel(self.root)
        win.title("基因库")
        win.geometry("500x400")
        win.configure(bg="#1a1a2e")
        win.transient(self.root)
        text = tk.Text(win, bg="#0d1b2a", fg="#e0e0e0", font=('Consolas', 10),
                       wrap='word', padx=10, pady=10, relief='flat')
        text.pack(side='left', fill='both', expand=True)
        scroll = ttk.Scrollbar(win, orient='vertical', command=text.yview)
        scroll.pack(side='right', fill='y')
        text.configure(yscrollcommand=scroll.set)
        text.insert('1.0', '\n'.join(lines))
        text.config(state='disabled')

    def extract_sperm_action(self):
        if not self._check_tech('ivf_tech'):
            messagebox.showwarning("科技锁定", "需要先研发「体外受精」科技")
            return
        if self.male_combo.current() < 0:
            messagebox.showwarning("警告", "请先选择雄性卡牌")
            return
        male_cards = [c for c in self.game.cards if c.gender == 'male' and c.is_alive]
        card = male_cards[self.male_combo.current()]
        gamete, msg = self.game.extract_gamete(card, as_male=True)
        if gamete:
            self.sperm_gamete = gamete
            self.sperm_card_id = card.id
            self.sperm_label.config(text=f"精子: 来自 {card.name} ({card.id})")
            messagebox.showinfo("提取成功", msg)
        else:
            messagebox.showerror("提取失败", msg)

    def extract_egg_action(self):
        if not self._check_tech('ivf_tech'):
            messagebox.showwarning("科技锁定", "需要先研发「体外受精」科技")
            return
        if self.female_combo.current() < 0:
            messagebox.showwarning("警告", "请先选择雌性卡牌")
            return
        female_cards = [c for c in self.game.cards if c.gender == 'female' and c.is_alive]
        card = female_cards[self.female_combo.current()]
        gamete, msg = self.game.extract_gamete(card, as_male=False)
        if gamete:
            self.egg_gamete = gamete
            self.egg_card_id = card.id
            self.egg_label.config(text=f"卵子: 来自 {card.name} ({card.id})")
            messagebox.showinfo("提取成功", msg)
        else:
            messagebox.showerror("提取失败", msg)

    def fuse_gametes_action(self):
        if not self._check_tech('ivf_tech'):
            messagebox.showwarning("科技锁定", "需要先研发「体外受精」科技")
            return
        if not self.sperm_gamete or not self.egg_gamete:
            messagebox.showwarning("警告", "请先提取精子和卵子")
            return
        child_chromosomes, child_gender = self.game.fuse_gametes(self.sperm_gamete, self.egg_gamete)
        child_name = f"IVF胚胎{Card.card_count}"
        child = self.game.create_card(child_name, chromosomes=child_chromosomes)
        if child and self.sperm_card_id and self.egg_card_id:
            _p1 = next((c for c in self.game.cards if c.id == self.sperm_card_id), None)
            _p2 = next((c for c in self.game.cards if c.id == self.egg_card_id), None)
            if _p1 and _p2 and getattr(_p1, 'sprite_genome', None) and getattr(_p2, 'sprite_genome', None):
                _p = list(range(64))
                random.shuffle(_p)
                _g = [None] * 64
                for _i, _pos in enumerate(_p):
                    _g[_pos] = (_p1.sprite_genome[_pos] if _i < 32 else _p2.sprite_genome[_pos])
                child.sprite_genome = _g
        self.sperm_gamete = None
        self.egg_gamete = None
        self.sperm_card_id = None
        self.egg_card_id = None
        self.sperm_label.config(text="精子: 未提取")
        self.egg_label.config(text="卵子: 未提取")
        if child:
            self.game.breed_counter += 1
            messagebox.showinfo("体外受精成功",
                f"新卡牌: {child.name}\n性别: {'雄性' if child.gender == 'male' else '雌性'}\n"
                f"技能: {', '.join(child.skills) if child.skills else '无'}")
            _new_q = self.game._check_all_quests()
            if _new_q:
                self._refresh_quest_list()
                _names = '、'.join(q['title'] for q in _new_q)
                messagebox.showinfo("任务完成", f"🎉 完成任务: {_names}\n请前往[任务]页领取奖励!")
            self.refresh_card_list()
            self.update_breeding_combos()
            self.update_engineer_combos()
        else:
            messagebox.showerror("体外受精失败", "胚胎发育失败")

    def duplicate_chromosome_action(self):
        if not self._check_tech('chromo_duplicate'):
            messagebox.showwarning("科技锁定", "需要先研发「染色体复制」科技")
            return
        if self.engineer_card_combo.current() < 0 or self.engineer_target_combo.current() < 0:
            messagebox.showwarning("警告", "请选择源卡牌和目标卡牌")
            return
        chr_id = self.chromo_duplicate_combo.get()
        if chr_id not in CHROMOSOME_IDS:
            messagebox.showwarning("警告", "请选择有效的染色体")
            return
        alive_cards = [c for c in self.game.cards if c.is_alive]
        source = alive_cards[self.engineer_card_combo.current()]
        target = alive_cards[self.engineer_target_combo.current()]
        result, msg = self.game.duplicate_chromosome(chr_id, source, target)
        if result:
            messagebox.showinfo("染色体复制", msg)
            self.refresh_card_list()
            self.update_card_detail(target)
        else:
            messagebox.showerror("复制失败", msg)

    def toggle_gene_isolation_action(self):
        if not self._check_tech('gene_isolation'):
            messagebox.showwarning("科技锁定", "需要先研发「基因隔离」科技")
            return
        card, gene_name, err = self._get_engineer_card_and_gene()
        if err:
            messagebox.showwarning("警告", err)
            return
        result, msg = self.game.toggle_gene_isolation(gene_name, card)
        if result:
            messagebox.showinfo("基因隔离", msg)
            self.update_card_detail(card)
        else:
            messagebox.showerror("隔离失败", msg)

    def apply_radiation(self):
        if not self.selected_card or not self.selected_card.is_alive:
            messagebox.showwarning("警告", "请选择存活的卡牌")
            return
        
        result = self.game.radiation_mutation(self.selected_card)
        
        if result:
            gene_desc = result['gene_desc']
            changes = result['changes']
            alive = result['alive']
            died = result.get('died', False)
            
            if died:
                messagebox.showerror("辐射变异", f"变异基因: {gene_desc}\n数值变化: 无\n状态: 死亡")
            else:
                change_text = ", ".join([f"{k}: {v:+d}" for k, v in changes.items()]) if changes else "无变化"
                status = "存活" if alive else "死亡"
                messagebox.showinfo("辐射变异", f"变异基因: {gene_desc}\n数值变化: {change_text}\n状态: {status}")
            
            self.refresh_card_list()
            if alive:
                self.update_card_detail(self.selected_card)
            else:
                self.selected_card = None
                for widget in self.gene_seq_frame.winfo_children():
                    widget.destroy()
    
    def rename_card(self):
        if not self.selected_card:
            messagebox.showwarning("警告", "请先选择一张卡牌")
            return
        dialog = tk.Toplevel(self.root)
        dialog.title("改名")
        dialog.geometry("300x150")
        dialog.configure(bg='#1a1a2e')
        dialog.transient(self.root)
        dialog.grab_set()
        tk.Label(dialog, text="输入新名称:", fg="#ffffff", bg="#1a1a2e", font=('微软雅黑', 12)).pack(pady=15)
        entry = tk.Entry(dialog, font=('微软雅黑', 12), width=25)
        entry.insert(0, self.selected_card.name)
        entry.pack(pady=5)
        entry.focus_set()
        entry.select_range(0, tk.END)
        def confirm():
            new_name = entry.get().strip()
            if new_name:
                self.selected_card.name = new_name
                self.game.save_game()
                self.refresh_card_list()
                self.update_card_detail(self.selected_card)
            dialog.destroy()
        tk.Button(dialog, text="确认", command=confirm, bg="#4a90d9", fg="#ffffff", font=('微软雅黑', 10)).pack(pady=10)
        entry.bind('<Return>', lambda e: confirm())

    def clone_card_action(self):
        if not self.selected_card:
            messagebox.showwarning("警告", "请先选择卡牌")
            return
        if not messagebox.askyesno("确认克隆", f"确定要克隆 [{self.selected_card.name}] 吗？"):
            return
        result, msg = self.game.clone_card(self.selected_card)
        if result:
            messagebox.showinfo("克隆成功", msg)
            self.refresh_card_list()
            self.update_engineer_combos()
            self.update_breeding_combos()
        else:
            messagebox.showerror("克隆失败", msg)

    def show_gene_report(self):
        if not self.selected_card:
            messagebox.showwarning("警告", "请先选择一张卡牌")
            return
        card = self.selected_card

        win = tk.Toplevel(self.root)
        win.title(f"基因报告 - {card.name}")
        win.geometry("780x620")
        win.configure(bg="#1a1a2e")
        win.transient(self.root)

        text = tk.Text(win, bg="#0d1b2a", fg="#e0e0e0", font=('Consolas', 10),
                       wrap='none', padx=10, pady=10, relief='flat',
                       highlightbackground="#1a1a2e", highlightthickness=0)
        text.pack(side='left', fill='both', expand=True)

        scroll_y = ttk.Scrollbar(win, orient='vertical', command=text.yview)
        scroll_y.pack(side='right', fill='y')
        scroll_x = ttk.Scrollbar(win, orient='horizontal', command=text.xview)
        scroll_x.pack(side='bottom', fill='x')
        text.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        lines = []
        gender_symbol = '♂' if card.gender == 'male' else '♀'
        status_str = '存活' if card.is_alive else '死亡'

        lines.append("=" * 70)
        lines.append(f"  卡牌ID: {card.id}")
        lines.append(f"  名称: {card.name}")
        lines.append(f"  性别: {gender_symbol} {'雄性' if card.gender == 'male' else '雌性'}")
        lines.append(f"  状态: {status_str}")
        birth_str = datetime.fromtimestamp(card.birth_time).strftime('%Y-%m-%d %H:%M:%S') if hasattr(card, 'birth_time') else '?'
        lines.append(f"  诞生: {birth_str}")
        if card.parent_ids:
            lines.append(f"  亲代: {', '.join(card.parent_ids)}")
        lines.append(f"  技能: {', '.join(card.skills) if card.skills else '无'}")
        lines.append("=" * 70)
        lines.append("")

        total_bp = sum(
            len(h.get('genome', ''))
            for chrid in ['chr1', 'chr2', 'chr3', 'chrX']
            for h in card.chromosomes.get(chrid, [])
        )
        lines.append(f"=== 基因组概况（共 {total_bp} bp）===")
        lines.append("")

        for chrid in ['chr1', 'chr2', 'chr3', 'chrX']:
            homs = card.chromosomes.get(chrid, [])
            if not homs:
                continue
            chr_len = len(homs[0].get('genome', ''))
            lines.append(f"── {chrid} ({chr_len} bp) ──")
            for i, h in enumerate(homs):
                genome = h.get('genome', '')
                lines.append(f"  同源体 {i+1}:")
                for j in range(0, len(genome), 60):
                    chunk = genome[j:j+60]
                    lines.append(f"    {chunk}")
            lines.append("")

        lines.append("═" * 70)
        lines.append("=== 基因区域（坐标 + 序列）===")
        lines.append("")
        for chrid in ['chr1', 'chr2', 'chr3', 'chrX']:
            homs = card.chromosomes.get(chrid, [])
            regions = GENE_REGIONS.get(chrid, [])
            if not homs or not regions:
                continue
            lines.append(f"── {chrid} ──")
            for gene_name, start, end in regions:
                tmpl = GENE_TEMPLATES.get(gene_name, {})
                seq_len = end - start
                seqs = []
                for h in homs:
                    g = h.get('genome', '')
                    if start < len(g):
                        seg = g[start:end]
                        if len(seg) > 40:
                            seg = seg[:40] + '...'
                        seqs.append(seg)
                    else:
                        seqs.append('(超)')
                dom_info = ''
                if len(homs) >= 2 and 'is_dominant' in homs[0]:
                    dom0 = homs[0]['is_dominant'].get(gene_name, '?')
                    dom1 = homs[1]['is_dominant'].get(gene_name, '?')
                    dom_info = f' 显性:[{dom0},{dom1}]'
                seq_display = ' / '.join(seqs)
                effect_desc = tmpl.get('description', '') if tmpl else ''
                lines.append(f"  {gene_name} ({start}-{end}, {seq_len}bp){dom_info}")
                if effect_desc:
                    lines.append(f"    {effect_desc}")
                lines.append(f"    序列: {seq_display}")
            lines.append("")

        lines.append("═" * 70)
        lines.append("=== 基因组增强区域 ===")
        lines.append("")
        for trait_name in STAT_ENHANCE_REGIONS:
            regions = STAT_ENHANCE_REGIONS.get(trait_name, [])
            if not regions:
                continue
            trait_val = card.traits.get(trait_name, '?')
            lines.append(f"── {trait_name} (当前值: {trait_val}) ──")
            for i, reg in enumerate(regions):
                chrid = reg['chr']
                start = reg['start']
                end = reg['end']
                if 'add' in reg:
                    rule_str = ', '.join(f'{b}:{v:+d}' for b, v in sorted(reg['add'].items()))
                    rule_type = '加算'
                else:
                    rule_str = ', '.join(f'{b}:{v}' for b, v in reg['mul'].items())
                    rule_type = '乘算'
                seqs = []
                homs = card.chromosomes.get(chrid, [])
                for h in homs:
                    g = h.get('genome', '')
                    if start < len(g):
                        seg = g[start:end]
                        seqs.append(seg[:30] + ('...' if len(seg) > 30 else ''))
                    else:
                        seqs.append('(超)')
                seq_display = ' / '.join(seqs)
                lines.append(f"  区域{i+1}: {chrid}({start}-{end}, {end-start}bp)")
                lines.append(f"    [{rule_type}] {{{rule_str}}}")
                lines.append(f"    序列: {seq_display}")
            lines.append("")

        lines.append("=" * 70)
        lines.append("报告结束")
        lines.append("=" * 70)

        text.insert('1.0', '\n'.join(lines))
        text.configure(state='disabled')

        close_btn = tk.Button(win, text="关闭", command=win.destroy,
                              bg="#4a90d9", fg="#ffffff", font=('微软雅黑', 10))
        close_btn.pack(pady=5)

    def create_tech_tree(self):
        import math
        for w in self.tech_tree_tab.winfo_children():
            w.destroy()

        title_label = ttk.Label(self.tech_tree_tab, text="科技树", style='Title.TLabel')
        title_label.pack(pady=(10, 0))

        main_frame = tk.Frame(self.tech_tree_tab, bg='#1a1a2e')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.tech_canvas_items = {}
        self.tech_tree_tip = None

        canvas_frame = tk.Frame(main_frame, bg='#1a1a2e')
        canvas_frame.pack(fill='both', expand=True)

        h_scroll = ttk.Scrollbar(canvas_frame, orient='horizontal')
        v_scroll = ttk.Scrollbar(canvas_frame, orient='vertical')

        self.tech_canvas = tk.Canvas(canvas_frame, bg='#1a1a2e', highlightthickness=0,
                                      xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        self.tech_canvas.pack(side='left', fill='both', expand=True)
        canvas = self.tech_canvas

        h_scroll.pack(side='bottom', fill='x')
        v_scroll.pack(side='right', fill='y')

        h_scroll.config(command=canvas.xview)
        v_scroll.config(command=canvas.yview)

        info_bar = tk.Frame(self.tech_tree_tab, bg='#16213e', height=36)
        info_bar.pack(fill='x', padx=10, pady=(0, 8))
        self.breed_speed_label = tk.Label(info_bar, text="繁殖速度: 1.0x | 基因组强化: 1.0x",
                                           fg="#aaa", bg="#16213e", font=('微软雅黑', 9))
        self.breed_speed_label.pack(side='left', padx=15, pady=5)
        self.battle_materials_label = tk.Label(info_bar, text="🧱 战斗材料: 0",
                                                fg="#50c878", bg="#16213e", font=('微软雅黑', 9))
        self.battle_materials_label.pack(side='left', padx=5, pady=5)
        tk.Label(info_bar, text="🖱 拖拽移动 · 点击升级", fg="#666", bg="#16213e",
                 font=('微软雅汗', 9)).pack(side='right', padx=15)

        self._drag_click = False

        canvas.bind('<Configure>', lambda e: self._redraw_tech_tree(canvas))
        canvas.bind('<ButtonPress-1>', self._on_canvas_press)
        canvas.bind('<B1-Motion>', self._on_canvas_drag)
        canvas.bind('<ButtonRelease-1>', lambda e: self._on_canvas_release(canvas, e))
        canvas.bind('<MouseWheel>', lambda e: canvas.yview_scroll(-int(e.delta/120), 'units'))
        canvas.bind('<Shift-MouseWheel>', lambda e: canvas.xview_scroll(-int(e.delta/120), 'units'))

    def _on_canvas_press(self, event):
        self._drag_click = True
        self._drag_start_xy = (event.x, event.y)
        self.tech_canvas.scan_mark(event.x, event.y)

    def _on_canvas_drag(self, event):
        if not getattr(self, '_drag_start_xy', None):
            return
        sx, sy = self._drag_start_xy
        if abs(event.x - sx) > 5 or abs(event.y - sy) > 5:
            self._drag_click = False
        self.tech_canvas.scan_dragto(event.x, event.y, gain=1)

    def _on_canvas_release(self, canvas, event):
        was_click = getattr(self, '_drag_click', False)
        self._drag_click = None
        self._drag_start_xy = None
        if was_click:
            self._on_tech_tree_click(canvas, event)

    def _redraw_tech_tree(self, canvas):
        import math
        canvas.delete('all')
        self.tech_canvas_items.clear()
        cw = canvas.winfo_width()
        ch = canvas.winfo_height()
        if cw < 200: cw = 900
        if ch < 200: ch = 680
        cx, cy = cw // 2, ch // 2
        radius_step = max(cw, ch) * 0.28

        tech_tree = self.game.tech_tree
        positions = {}

        max_x = max_y = 0
        for tech_name, tech_data in tech_tree.items():
            angle_deg = tech_data.get('tree_angle')
            radius = tech_data.get('tree_radius', 0)
            if angle_deg is not None:
                rad = math.radians(angle_deg)
                x = cx + radius * radius_step * math.sin(rad)
                y = cy - radius * radius_step * math.cos(rad)
            else:
                x, y = cx, cy
            positions[tech_name] = (x, y)
            max_x = max(max_x, abs(x - cx) + 100)
            max_y = max(max_y, abs(y - cy) + 100)

        canvas.configure(scrollregion=(-max_x, -max_y, cx + max_x, cy + max_y))

        for tech_name, tech_data in tech_tree.items():
            req = tech_data.get('unlock_requirement')
            if req and req[0] in positions and tech_name in positions:
                x1, y1 = positions[req[0]]
                x2, y2 = positions[tech_name]
                can_unlock = (tech_data['unlocked'] or
                              (req[0] in tech_tree and
                               tech_tree[req[0]]['level'] >= req[1]))
                line_color = '#4a9eff' if can_unlock else '#444'
                canvas.create_line(x1, y1, x2, y2, fill=line_color, width=2,
                                   dash=() if tech_data['unlocked'] else (4, 4))

        nw, nh = 120, 55
        for tech_name, tech_data in tech_tree.items():
            x, y = positions[tech_name]
            bx, by = x - nw // 2, y - nh // 2

            branch = tech_data.get('branch', 'root')
            br_color = TREE_BRANCHES.get(branch, {}).get('color', '#888')
            br_bg = TREE_BRANCHES.get(branch, {}).get('bg', '#1a1a2e')

            if not tech_data['unlocked']:
                br_color = '#555'
                br_bg = '#111'

            pad = 3
            canvas.create_rectangle(bx - pad, by - pad, bx + nw + pad, by + nh + pad,
                                    fill=br_color, outline=br_color, width=0, tags=f'node_{tech_name}')

            bg_color = br_bg
            if tech_data['level'] >= tech_data['max_level']:
                bg_color = '#1a2a1a'
            canvas.create_rectangle(bx, by, bx + nw, by + nh,
                                    fill=bg_color, outline=br_color, width=1, tags=f'node_{tech_name}')

            name_color = br_color if tech_data['unlocked'] else '#666'
            canvas.create_text(bx + nw // 2, by + 15, text=tech_data['name'],
                               fill=name_color, font=('微软雅黑', 9, 'bold'), tags=f'node_{tech_name}')

            lvl_text = f"Lv.{tech_data['level']}/{tech_data['max_level']}"
            if tech_data['level'] >= tech_data['max_level']:
                lvl_text += ' MAX'
            canvas.create_text(bx + nw // 2, by + 36, text=lvl_text,
                               fill='#4a9eff' if tech_data['unlocked'] else '#555',
                               font=('Consolas', 8), tags=f'node_{tech_name}')

            self.tech_canvas_items[tech_name] = {
                'x': x, 'y': y, 'w': nw, 'h': nh,
                'bx': bx, 'by': by,
            }

            canvas.tag_bind(f'node_{tech_name}', '<Enter>',
                lambda e, tn=tech_name: self._show_tech_tooltip(e, tn))
            canvas.tag_bind(f'node_{tech_name}', '<Leave>',
                lambda e: self._hide_tech_tooltip())

    def _show_tech_tooltip(self, event, tech_name):
        self._hide_tech_tooltip()
        tech = self.game.tech_tree.get(tech_name, {})
        if not tech:
            return
        lines = []
        lines.append(f"【{tech.get('name', tech_name)}】")
        br = tech.get('branch', '')
        lines.append(f"分支: {TREE_BRANCHES.get(br, {}).get('name', '')}")
        lines.append(f"等级: {tech['level']} / {tech['max_level']}")
        lines.append('')
        lines.append(tech.get('description', ''))
        lines.append('')
        if tech['level'] >= tech['max_level']:
            lines.append("✓ 已达到最大等级")
        else:
            next_lv = tech['level'] + 1
            effect = tech.get('effects', {}).get(next_lv, '')
            if effect:
                lines.append(f"下一级: {effect}")
            cost = tech.get('costs', {}).get(next_lv, {})
            parts = []
            if 'battle_materials' in cost:
                have = self.game.battle_materials
                need = cost['battle_materials']
                color = '充足' if have >= need else '不足'
                parts.append(f"🧱战斗材料 {have}/{need}({color})")
            if 'gacha_currency' in cost:
                have = self.game.gacha_currency
                need = cost['gacha_currency']
                color = '充足' if have >= need else '不足'
                parts.append(f"🧬基因密钥 {have}/{need}({color})")
            if not parts:
                if tech_name == 'card_storage':
                    sc = self.game._get_card_storage_cost()
                    have = self.game.battle_materials
                    color = '充足' if have >= sc else '不足'
                    parts.append(f"🧱战斗材料 {have}/{sc}({color})")
                else:
                    parts.append("升级免费")
            lines.append(f"消耗: {' | '.join(parts)}")
        if not tech['unlocked']:
            req = tech.get('unlock_requirement', (None, None))
            if req[0]:
                rt = self.game.tech_tree.get(req[0], {})
                lines.append(f"🔒 需要: {rt.get('name', req[0])} Lv.{req[1]}")
            else:
                lines.append("🔒 未解锁")
        tip = tk.Toplevel(self.tech_tree_tab, bg='#1a1a2e', relief='solid', borderwidth=1)
        tip.overrideredirect(True)
        tip.attributes('-topmost', True)
        text = '\n'.join(lines)
        label = tk.Label(tip, text=text, justify='left', fg='#e0e0e0',
                          bg='#1a1a2e', font=('微软雅黑', 9), padx=12, pady=8)
        label.pack()
        tip.update_idletasks()
        x = event.x_root + 15
        y = event.y_root + 10
        tip.geometry(f'+{x}+{y}')
        self.tech_tree_tip = tip

    def _hide_tech_tooltip(self):
        if self.tech_tree_tip:
            self.tech_tree_tip.destroy()
            self.tech_tree_tip = None

    def _on_tech_tree_click(self, canvas, event):
        import math
        cx = canvas.canvasx(event.x)
        cy = canvas.canvasy(event.y)
        for tech_name, info in self.tech_canvas_items.items():
            bx, by = info['bx'], info['by']
            nw, nh = info['w'], info['h']
            if bx <= cx <= bx + nw and by <= cy <= by + nh:
                self._handle_tech_click(tech_name)
                return

    def _handle_tech_click(self, tech_name):
        tech_data = self.game.tech_tree.get(tech_name)
        if not tech_data:
            return

        if tech_data['level'] >= tech_data['max_level']:
            messagebox.showinfo("已达最大等级",
                f"{tech_data['name']} 已达到最高等级 Lv.{tech_data['max_level']}")
            return

        success, msg = self.game.upgrade_tech(tech_name)
        if success:
            messagebox.showinfo("升级成功", msg)
            self._refresh_tech_tree_display()
            self.refresh_card_list()
            self.update_engineer_combos()
            self.update_breeding_combos()
            _new_q = self.game._check_all_quests()
            if _new_q:
                self._refresh_quest_list()
                _names = '、'.join(q['title'] for q in _new_q)
                messagebox.showinfo("任务完成", f"🎉 完成任务: {_names}\n请前往[任务]页领取奖励!")
        else:
            messagebox.showwarning("升级失败", msg)

    def _refresh_tech_tree_display(self):
        if hasattr(self, 'tech_canvas') and self.tech_canvas.winfo_exists():
            self._redraw_tech_tree(self.tech_canvas)
        speed = self.game.get_breed_speed()
        gb_level = self.game.tech_tree.get('genome_boost', {}).get('level', 0)
        gb_mult = 1.0 + gb_level * 0.2
        self.breed_speed_label.config(text=f"繁殖速度: {speed:.1f}x | 基因组强化: {gb_mult:.1f}x")
        if hasattr(self, 'battle_materials_label'):
            self.battle_materials_label.config(
                text=f"🧱 战斗材料: {self.game.battle_materials}  |  🧬 基因密钥: {self.game.gacha_currency}")

    def show_breed_speed_info(self):
        speed = self.game.get_breed_speed()
        messagebox.showinfo("繁殖速度", f"当前繁殖速度: {speed:.1f}x")

    def upgrade_tech(self, tech_name):
        self._handle_tech_click(tech_name)

    def update_tech_tree_ui(self):
        self._refresh_tech_tree_display()
    
    def create_gacha_ui(self):
        container = ttk.Frame(self.gacha_tab)
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        top_bar = ttk.Frame(container)
        top_bar.pack(fill='x', pady=(0, 10))
        ttk.Label(top_bar, text="🧬 基因密钥: ", font=('微软雅黑', 14, 'bold'), foreground='#ffd700').pack(side='left')
        self.gacha_currency_label = ttk.Label(top_bar, text=str(self.game.gacha_currency), font=('微软雅黑', 14, 'bold'), foreground='#ffd700')
        self.gacha_currency_label.pack(side='left')
        
        main_area = ttk.Frame(container)
        main_area.pack(fill='both', expand=True)
        
        left_panel = ttk.Frame(main_area, width=250)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        header_bg = tk.Frame(left_panel, bg='#0f3460', height=36)
        header_bg.pack(fill='x', pady=(0, 10))
        tk.Label(header_bg, text="🎯 卡池选择", font=('微软雅黑', 12, 'bold'),
                fg='#00d9ff', bg='#0f3460').pack(expand=True)
        
        self._pool_btns = {}
        self._pool_btn_frames = {}
        self._selected_pool = tk.StringVar(value='')
        
        for pid, pool in Game.GACHA_POOLS.items():
            unlocked = self.game.max_stage >= pool['unlock_stage']
            
            outer = tk.Frame(left_panel, bg=pool['theme_color'] if unlocked else '#333333', height=62)
            outer.pack(fill='x', pady=3, padx=2)
            outer.pack_propagate(False)
            
            inner = tk.Frame(outer, bg=pool['theme_bg'], highlightthickness=0)
            inner.pack(fill='both', expand=True, padx=2, pady=2)
            
            top_row = tk.Frame(inner, bg=pool['theme_bg'])
            top_row.pack(fill='x', padx=6, pady=(4, 0))
            icon_color = pool['theme_color'] if unlocked else '#555555'
            tk.Label(top_row, text=pool['icon'], font=('微软雅黑', 11),
                    fg=icon_color, bg=pool['theme_bg']).pack(side='left')
            btn = tk.Button(top_row, text=f"  {pool['name']}", font=('微软雅黑', 10, 'bold'),
                           fg=icon_color, bg=pool['theme_bg'], relief='flat', anchor='w',
                           activebackground=pool['theme_secondary'], activeforeground=pool['theme_color'],
                           command=lambda p=pid: self._select_gacha_pool(p))
            btn.pack(side='left', fill='x', expand=True)
            
            status_row = tk.Frame(inner, bg=pool['theme_bg'])
            status_row.pack(fill='x', padx=6, pady=(0, 4))
            if unlocked:
                status_color = pool['theme_color']
                status_text = "✔ 已解锁"
            else:
                status_color = '#ff4444'
                status_text = f"🔒 第{pool['unlock_stage']}关"
            tk.Label(status_row, text=status_text, font=('微软雅黑', 7),
                    fg=status_color, bg=pool['theme_bg']).pack(side='left')
            if not unlocked:
                tk.Label(status_row, text=f"解锁", font=('微软雅黑', 7),
                        fg='#ff4444', bg=pool['theme_bg']).pack(side='left')
            if unlocked:
                dot = tk.Frame(inner, bg=pool['theme_color'], width=6, height=6)
                dot.pack(side='bottom', anchor='se', padx=4, pady=2)
            self._pool_btns[pid] = btn
            self._pool_btn_frames[pid] = outer
        
        right_panel = ttk.Frame(main_area)
        right_panel.pack(side='right', fill='both', expand=True)
        
        self._pool_info_frame = ttk.LabelFrame(right_panel, text="📋 卡池详情", padding=10)
        self._pool_info_frame.pack(fill='both', expand=True)
        
        default_info = tk.Frame(self._pool_info_frame, bg='#16213e')
        default_info.pack(expand=True, fill='both')
        tk.Label(default_info, text="👈 请从左侧选择一个卡池",
                font=('微软雅黑', 11), fg='#666666', bg='#16213e').pack(expand=True)
        
        self._gacha_result_frame = ttk.LabelFrame(right_panel, text="📦 抽卡结果", padding=10)
        self._gacha_result_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        result_canvas = tk.Canvas(self._gacha_result_frame, bg='#16213e', highlightthickness=0, height=280)
        h_scroll = ttk.Scrollbar(self._gacha_result_frame, orient='horizontal', command=result_canvas.xview)
        v_scroll = ttk.Scrollbar(self._gacha_result_frame, orient='vertical', command=result_canvas.yview)
        self._gacha_result_inner = ttk.Frame(result_canvas)
        self._gacha_result_inner.bind('<Configure>', lambda e: result_canvas.configure(scrollregion=result_canvas.bbox('all')))
        result_canvas.create_window((0, 0), window=self._gacha_result_inner, anchor='nw')
        result_canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        result_canvas.pack(side='left', fill='both', expand=True)
        v_scroll.pack(side='right', fill='y')
        h_scroll.pack(side='bottom', fill='x')
        def _on_gacha_wheel(event):
            result_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        result_canvas.bind("<MouseWheel>", _on_gacha_wheel)
        self._gacha_result_canvas = result_canvas
    
    def _select_gacha_pool(self, pool_id):
        self._selected_pool.set(pool_id)
        pool = Game.GACHA_POOLS[pool_id]
        for wid in self._pool_info_frame.winfo_children():
            wid.destroy()
        
        for pid, outer in self._pool_btn_frames.items():
            if pid == pool_id:
                outer.config(bg=pool['theme_color'])
            else:
                unlocked = self.game.max_stage >= Game.GACHA_POOLS[pid]['unlock_stage']
                outer.config(bg=pool['theme_color'] if unlocked else '#333333')
        
        main = tk.Frame(self._pool_info_frame, bg='#16213e')
        main.pack(fill='both', expand=True)
        
        accent = tk.Frame(main, bg=pool['theme_color'], height=4)
        accent.pack(fill='x')
        
        header_row = tk.Frame(main, bg='#16213e')
        header_row.pack(fill='x', pady=(10, 2))
        tk.Label(header_row, text=pool['icon'], font=('微软雅黑', 24),
                bg='#16213e').pack(side='left', padx=(0, 8))
        tk.Label(header_row, text=pool['name'], font=('微软雅黑', 18, 'bold'),
                fg=pool['theme_color'], bg='#16213e').pack(side='left')
        
        underline = tk.Frame(main, bg=pool['theme_color'], height=2)
        underline.pack(fill='x', pady=(2, 10))
        
        flavor_frame = tk.Frame(main, bg=pool['theme_bg'], highlightbackground=pool['theme_color'],
                                highlightthickness=1, padx=10, pady=8)
        flavor_frame.pack(fill='x', pady=(0, 10))
        tk.Label(flavor_frame, text=f'"{pool["flavor"]}"', font=('微软雅黑', 9, 'italic'),
                fg=pool['theme_color'], bg=pool['theme_bg'], wraplength=500,
                justify='left').pack(anchor='w')
        
        desc_frame = tk.Frame(main, bg='#16213e')
        desc_frame.pack(fill='x', pady=(0, 8))
        tk.Label(desc_frame, text="📖 卡池说明", font=('微软雅黑', 10, 'bold'),
                fg='#aaaaaa', bg='#16213e').pack(anchor='w')
        tk.Label(desc_frame, text=pool['description'], font=('微软雅黑', 10),
                fg='#cccccc', bg='#16213e', wraplength=500,
                justify='left').pack(anchor='w', pady=(2, 0))
        
        sep = tk.Frame(main, bg='#333333', height=1)
        sep.pack(fill='x', pady=6)
        
        ultra_frame = tk.Frame(main, bg='#16213e')
        ultra_frame.pack(fill='x', pady=(0, 8))
        tk.Label(ultra_frame, text="⭐ 传说技能", font=('微软雅黑', 10, 'bold'),
                fg='#ffd700', bg='#16213e').pack(anchor='w')
        ultra_names = []
        for gn in pool['ultra_skills']:
            tmpl = GENE_TEMPLATES.get(gn, {})
            ultra_names.append(tmpl.get('skill_name', gn))
        badges = tk.Frame(ultra_frame, bg='#16213e')
        badges.pack(anchor='w', pady=(4, 0))
        for uname in ultra_names:
            badge = tk.Label(badges, text=f" {uname} ", font=('微软雅黑', 9, 'bold'),
                           fg='#ffd700', bg=pool['theme_bg'],
                           relief='solid', borderwidth=1,
                           highlightbackground=pool['theme_color'],
                           highlightthickness=1, padx=6, pady=2)
            badge.pack(side='left', padx=(0, 8))
        
        sep2 = tk.Frame(main, bg='#333333', height=1)
        sep2.pack(fill='x', pady=6)
        
        info_grid = tk.Frame(main, bg='#16213e')
        info_grid.pack(fill='x', pady=(0, 8))
        
        cost_frame = tk.Frame(info_grid, bg='#1a1a2e', highlightbackground=pool['theme_color'],
                              highlightthickness=1, padx=10, pady=6)
        cost_frame.pack(side='left', padx=(0, 10))
        tk.Label(cost_frame, text="💎 抽卡消耗", font=('微软雅黑', 9, 'bold'),
                fg=pool['theme_color'], bg='#1a1a2e').pack(anchor='w')
        tk.Label(cost_frame, text=f"单抽: {pool['cost']} 密钥", font=('微软雅黑', 9),
                fg='#cccccc', bg='#1a1a2e').pack(anchor='w')
        tk.Label(cost_frame, text=f"十连: {pool['cost']*9} 密钥 (9折)",
                font=('微软雅黑', 9), fg='#ffd700', bg='#1a1a2e').pack(anchor='w')
        
        rates_box = tk.Frame(info_grid, bg='#1a1a2e', highlightbackground=pool['theme_color'],
                             highlightthickness=1, padx=10, pady=6)
        rates_box.pack(side='left')
        tk.Label(rates_box, text="📊 出货概率", font=('微软雅黑', 9, 'bold'),
                fg=pool['theme_color'], bg='#1a1a2e').pack(anchor='w')
        rates_inner = tk.Frame(rates_box, bg='#1a1a2e')
        rates_inner.pack(anchor='w')
        tk.Label(rates_inner, text="●", font=('微软雅黑', 8), fg='#666666',
                bg='#1a1a2e').pack(side='left')
        tk.Label(rates_inner, text=" 普通 98.3%", font=('微软雅黑', 9),
                fg='#aaaaaa', bg='#1a1a2e').pack(side='left')
        rates_inner2 = tk.Frame(rates_box, bg='#1a1a2e')
        rates_inner2.pack(anchor='w')
        tk.Label(rates_inner2, text="●", font=('微软雅黑', 8), fg='#00bfff',
                bg='#1a1a2e').pack(side='left')
        tk.Label(rates_inner2, text=" 精英 1.5%", font=('微软雅黑', 9),
                fg='#00bfff', bg='#1a1a2e').pack(side='left')
        rates_inner3 = tk.Frame(rates_box, bg='#1a1a2e')
        rates_inner3.pack(anchor='w')
        tk.Label(rates_inner3, text="●", font=('微软雅黑', 8), fg='#ffd700',
                bg='#1a1a2e').pack(side='left')
        tk.Label(rates_inner3, text=" 传说 0.2%", font=('微软雅黑', 9),
                fg='#ffd700', bg='#1a1a2e').pack(side='left')
        
        pity_box = tk.Frame(info_grid, bg='#1a1a2e', highlightbackground=pool['theme_color'],
                            highlightthickness=1, padx=10, pady=6)
        pity_box.pack(side='left', padx=(10, 0))
        tk.Label(pity_box, text="🎯 保底进度", font=('微软雅黑', 9, 'bold'),
                fg=pool['theme_color'], bg='#1a1a2e').pack(anchor='w')
        pity_count = self.game.pity_counters.get(pool_id, 0)
        remaining = max(0, 360 - pity_count)
        self._pity_counter_label = tk.Label(pity_box, text=f"{pity_count}/360",
                font=('微软雅黑', 11, 'bold'), fg='#ffd700', bg='#1a1a2e')
        self._pity_counter_label.pack(anchor='w')
        self._pity_remaining_label = tk.Label(pity_box, text=f"剩余 {remaining} 抽必出传说",
                font=('微软雅黑', 8), fg='#aaaaaa', bg='#1a1a2e')
        self._pity_remaining_label.pack(anchor='w')
        
        btn_frame = tk.Frame(main, bg='#16213e')
        btn_frame.pack(pady=(10, 5))
        self._pull1_btn = tk.Button(btn_frame, text=f"{pool['icon']} 单抽 ×1 ({pool['cost']})",
                bg=pool['theme_bg'], fg=pool['theme_color'], font=('微软雅黑', 11, 'bold'),
                padx=20, pady=6, relief='solid', borderwidth=2,
                activebackground=pool['theme_secondary'], activeforeground=pool['theme_color'],
                highlightbackground=pool['theme_color'], highlightthickness=1,
                command=lambda: self._do_gacha_pull(pool_id, 1))
        self._pull1_btn.pack(side='left', padx=10)
        self._pull10_btn = tk.Button(btn_frame, text=f"🎉 十连 ×10 ({pool['cost']*9})",
                bg='#ffd700', fg='#1a1a2e', font=('微软雅黑', 11, 'bold'),
                padx=20, pady=6, relief='solid', borderwidth=2,
                activebackground='#ffaa00', activeforeground='#000000',
                highlightbackground=pool['theme_color'], highlightthickness=2,
                command=lambda: self._do_gacha_pull(pool_id, 10))
        self._pull10_btn.pack(side='left', padx=10)
    
    def _do_gacha_pull(self, pool_id, count):
        pool = Game.GACHA_POOLS[pool_id]
        total_cost = pool['cost'] * (count if count == 1 else 9)
        if self.game.gacha_currency < total_cost:
            messagebox.showwarning("密钥不足", f"需要 {total_cost} 基因密钥，当前 {self.game.gacha_currency}")
            return
        
        for wid in self._gacha_result_inner.winfo_children():
            wid.destroy()
        
        self._pull1_btn.config(state='disabled')
        self._pull10_btn.config(state='disabled')
        
        self.root.after(100, lambda: self._do_pull_animation(pool_id, count))
    
    def _do_pull_animation(self, pool_id, count):
        pool = Game.GACHA_POOLS[pool_id]
        count_actual = count if count == 1 else 10
        results, msg = self.game.gacha_pull(pool_id, count_actual)
        
        if not results:
            messagebox.showerror("抽卡失败", msg)
            self._pull1_btn.config(state='normal')
            self._pull10_btn.config(state='normal')
            return
        
        self.game.save_game()
        self.gacha_currency_label.config(text=str(self.game.gacha_currency))
        
        pool_color = pool['theme_color']
        pool_bg = pool['theme_bg']
        
        if count_actual > 1:
            row1 = tk.Frame(self._gacha_result_inner, bg='#16213e')
            row1.pack(side='top', fill='x', pady=2)
            row2 = tk.Frame(self._gacha_result_inner, bg='#16213e')
            row2.pack(side='top', fill='x', pady=2)
        else:
            row1 = self._gacha_result_inner
            row2 = None
        
        for i, card in enumerate(results):
            rarity = getattr(card, '_rarity', 'normal')
            border_color = {'normal': '#444444', 'rare': '#00bfff', 'ultra': '#ffd700'}[rarity]
            
            parent = row1 if (i < 5 or row2 is None) else row2
            frame = tk.Frame(parent, bg='#16213e', relief='solid', borderwidth=2,
                            highlightbackground=border_color, highlightthickness=2)
            frame.pack(side='left', padx=5, pady=5, fill='y')
            
            if rarity == 'ultra':
                glow = tk.Frame(frame, bg=border_color, height=3)
                glow.pack(fill='x')
                sparkle = tk.Frame(frame, bg=pool_color, height=1)
                sparkle.pack(fill='x')
            elif rarity == 'rare':
                accent_bar = tk.Frame(frame, bg=pool_color, height=2)
                accent_bar.pack(fill='x')
            
            name_color = {'normal': '#ffffff', 'rare': '#00bfff', 'ultra': '#ffd700'}[rarity]
            name_label = tk.Label(frame, text=card.name, font=('微软雅黑', 10, 'bold'),
                                fg=name_color, bg='#16213e')
            name_label.pack(pady=(5, 0))
            
            gender_symbol = '♂' if card.gender == 'male' else '♀'
            id_color = pool_color if rarity == 'ultra' else '#888888'
            tk.Label(frame, text=f"{gender_symbol} {card.id}", font=('微软雅黑', 8),
                    fg=id_color, bg='#16213e').pack()
            
            if rarity == 'ultra':
                tk.Label(frame, text="★ 传说 ★", font=('微软雅黑', 9, 'bold'),
                        fg='#ffd700', bg='#16213e').pack()
                tk.Label(frame, text=f"✦ {pool['icon']} ✦", font=('微软雅黑', 8),
                        fg=pool_color, bg='#16213e').pack()
            elif rarity == 'rare':
                tk.Label(frame, text="★ 精英 ★", font=('微软雅黑', 9, 'bold'),
                        fg='#00bfff', bg='#16213e').pack()
            
            stats = []
            for k in ('health', 'attack', 'defense', 'speed'):
                v = card.traits.get(k, 0)
                stats.append(f"{k[:3]}:{v}")
            tk.Label(frame, text='  '.join(stats), font=('Consolas', 8),
                    fg='#aaaaaa', bg='#16213e').pack(pady=2)
            
            if card.skills:
                skills_text = '\n'.join(card.skills[:4])
                tk.Label(frame, text=skills_text, font=('微软雅黑', 8),
                        fg='#88ccff', bg='#16213e', justify='left').pack(pady=2)
            
            add_bg = pool['theme_bg'] if rarity == 'ultra' else '#0f3460'
            add_fg = pool_color if rarity == 'ultra' else '#00d9ff'
            add_btn = tk.Button(frame, text="加入卡库", bg=add_bg, fg=add_fg,
                              relief='solid', borderwidth=1,
                              activebackground=pool['theme_secondary'],
                              activeforeground=pool_color,
                              command=lambda c=card: self._add_gacha_card(c))
            add_btn.pack(pady=3)
        
        ultra_names = [c.name for c in results if getattr(c, '_rarity', None) == 'ultra']
        if ultra_names:
            names_str = '、'.join(ultra_names)
            messagebox.showinfo("🎉 传说卡牌!", f"恭喜获得传说卡牌:\n{names_str}")
        
        self.refresh_card_list()
        self._pull1_btn.config(state='normal')
        self._pull10_btn.config(state='normal')
        self._gacha_result_canvas.xview_moveto(0)
        
        if hasattr(self, '_pity_counter_label') and self._selected_pool.get():
            pid = self._selected_pool.get()
            pc = self.game.pity_counters.get(pid, 0)
            self._pity_counter_label.config(text=f"{pc}/360")
            remaining = max(0, 360 - pc)
            self._pity_remaining_label.config(text=f"剩余 {remaining} 抽必出传说")
    
    def _add_gacha_card(self, card):
        if len(self.game.cards) >= self.game.effective_max_cards:
            messagebox.showwarning("卡库已满", f"卡牌库已达上限 ({self.game.effective_max_cards}张)，请先删除部分卡牌")
            return
        self.game.cards.append(card)
        self.game.save_game()
        self.refresh_card_list()
        messagebox.showinfo("添加成功", f"{card.name} 已加入卡牌库!")
    
    def create_battle_ui(self):
        self.battle_system = None
        self.battle_is_running = False
        self.battle_update_job = None
        self.team_grid = {}
        self.auto_battle = False
        
        title_label = ttk.Label(self.battle_tab, text="战斗系统", style='Title.TLabel')
        title_label.pack(pady=10)
        
        select_frame = ttk.Frame(self.battle_tab)
        select_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(select_frame, text="选择关卡:").pack(side='left')
        self.stage_combo = ttk.Combobox(select_frame, width=30)
        self.stage_combo.pack(side='left', padx=5)
        self.stage_combo['values'] = self.get_available_stages()
        self.stage_combo.current(0)
        self.stage_combo.bind('<<ComboboxSelected>>', self._on_stage_changed)
        
        ttk.Label(select_frame, text="队伍:").pack(side='left', padx=20)
        self.team_size_label = ttk.Label(select_frame, text="0/5 (3×3)")
        self.team_size_label.pack(side='left', padx=5)
        
        ttk.Button(select_frame, text="选择队伍", command=self.open_team_selection).pack(side='left', padx=10)
        
        btn_frame = ttk.Frame(self.battle_tab)
        btn_frame.pack(pady=10)
        
        self.start_battle_btn = ttk.Button(btn_frame, text="开始战斗", command=self.start_battle)
        self.start_battle_btn.pack(side='left', padx=5)
        
        self.exit_battle_btn = ttk.Button(btn_frame, text="退出战斗", command=self.exit_battle, state='disabled')
        self.exit_battle_btn.pack(side='left', padx=5)
        
        continuous_frame = ttk.Frame(self.battle_tab)
        continuous_frame.pack(fill='x', padx=20, pady=5)
        self.continuous_btn = ttk.Button(continuous_frame, text="连续作战", command=self._start_continuous_battle, state='disabled')
        self.continuous_btn.pack(side='left', padx=5)
        self.continuous_stop_btn = ttk.Button(continuous_frame, text="停止", command=self._stop_continuous_battle, state='disabled')
        self.continuous_stop_btn.pack(side='left', padx=5)
        self.continuous_status = ttk.Label(continuous_frame, text="", font=('微软雅黑', 10))
        self.continuous_status.pack(side='left', padx=20)
        
        self.battle_area = ttk.Frame(self.battle_tab)
        self.battle_area.pack(fill='both', expand=True, padx=20, pady=10)
        
        log_frame = ttk.LabelFrame(self.battle_tab, text="战斗日志")
        log_frame.pack(fill='x', padx=20, pady=10)
        
        self.log_text = tk.Text(log_frame, height=5, width=80, bg='#16213e', fg='#ffffff', font=('Consolas', 10))
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.log_text.config(yscrollcommand=scrollbar.set)
    
    def create_bestiary_ui(self):
        _maps_order = ['abandoned_lab', 'ancient_ruins', 'void_rift', 'elemental_plane', 'abyss_bottom', 'holy_sanctuary']
        _sv = ttk.Scrollbar(self.bestiary_tab, orient='vertical')
        _cv = tk.Canvas(self.bestiary_tab, bg='#1a1a2e', highlightthickness=0, yscrollcommand=_sv.set)
        self._bestiary_cv = _cv
        _sv.config(command=_cv.yview)
        _inner = ttk.Frame(_cv)
        _inner.bind('<Configure>', lambda e: _cv.configure(scrollregion=_cv.bbox('all')))
        _cv.create_window((0, 0), window=_inner, anchor='nw')
        _sv.pack(side='right', fill='y')
        _cv.pack(side='left', fill='both', expand=True)
        _cv.bind('<MouseWheel>', lambda e: _cv.yview_scroll(-int(e.delta / 60), 'units'))

        def _on_card_click(widget, callback):
            widget.bind('<Button-1>', callback)
            for c in widget.winfo_children():
                _on_card_click(c, callback)

        _inner.grid_rowconfigure(0, weight=1)
        _inner.grid_columnconfigure(0, weight=1)
        self._bestiary_list_frame = tk.Frame(_inner, bg='#1a1a2e')
        self._bestiary_list_frame.grid(row=0, column=0, sticky='nsew')
        self._bestiary_detail_frame = tk.Frame(_inner, bg='#1a1a2e')
        self._bestiary_detail_frame.grid(row=0, column=0, sticky='nsew')
        self._bestiary_detail_frame.lower()

        title = ttk.Label(self._bestiary_list_frame, text='敌人图鉴', font=('微软雅黑', 16, 'bold'), foreground='#00d9ff', background='#1a1a2e')
        title.pack(pady=(10, 5))
        subtitle = ttk.Label(self._bestiary_list_frame, text='包含所有主线关卡与地图关卡的全部敌人', font=('微软雅黑', 9), foreground='#888888', background='#1a1a2e')
        subtitle.pack(pady=(0, 15))

        for _mid in _maps_order:
            _map = MAPS.get(_mid)
            if not _map:
                continue
            _pool = _map.get('enemy_pool', [])
            _mc = _map.get('color', '#ffffff')

            _mf = tk.Frame(self._bestiary_list_frame, bg='#1a1a2e', highlightbackground=_mc, highlightthickness=1)
            _mf.pack(fill='x', padx=20, pady=(5, 10))

            _hdr = tk.Frame(_mf, bg=_mc)
            _hdr.pack(fill='x')
            _dot = tk.Label(_hdr, text='◉', fg='#ffffff', bg=_mc, font=('微软雅黑', 12))
            _dot.pack(side='left', padx=(8, 4), pady=4)
            _range = f'{_map["start_stage"]}–{_map["start_stage"] + _map["stages"] - 1}关'
            _label = tk.Label(_hdr, text=f'{_map["name"]}（{_range}）', fg='#ffffff', bg=_mc,
                              font=('微软雅黑', 12, 'bold'))
            _label.pack(side='left', padx=(0, 8), pady=4)
            _desc = tk.Label(_hdr, text=_map.get('description', ''), fg='#ffffff', bg=_mc,
                             font=('微软雅黑', 8))
            _desc.pack(side='left', padx=8, pady=4)

            _body = tk.Frame(_mf, bg='#16213e')
            _body.pack(fill='x', padx=4, pady=4)

            _row_frame = None
            for _i, _tid in enumerate(_pool):
                if _i % 4 == 0:
                    _row_frame = tk.Frame(_body, bg='#16213e')
                    _row_frame.pack(fill='x', pady=2)
                _tpl = ENEMY_TEMPLATES.get(_tid)
                if not _tpl:
                    continue
                _card = tk.Frame(_row_frame, bg='#0f3460', highlightbackground=_mc, highlightthickness=1,
                                 width=150, height=72)
                _card.pack(side='left', padx=4, pady=2)
                _card.pack_propagate(False)

                _top = tk.Frame(_card, bg='#0f3460')
                _top.pack(fill='x', pady=(2, 0))
                # Sprite
                _spr = None
                if hasattr(self, '_enemy_sprites') and _tid in self._enemy_sprites:
                    _spr = self._enemy_sprites[_tid][0]
                    _sl = tk.Label(_top, image=_spr, bg='#0f3460')
                    _sl.pack(side='left', padx=(4, 2))
                # Name + desc
                _nframe = tk.Frame(_top, bg='#0f3460')
                _nframe.pack(side='left', fill='x', expand=True)
                _boss = _tid in BOSS_STAT_MULTIPLIERS
                _nf = _mc if _boss else '#00d9ff'
                _nm = tk.Label(_nframe, text=_tpl['name'], fg=_nf, bg='#0f3460',
                               font=('微软雅黑', 8, 'bold'), anchor='w')
                _nm.pack(fill='x')
                _desc_text = _tpl.get('description', '')
                _dl = tk.Label(_nframe, text=_desc_text, fg='#aaaaaa', bg='#0f3460',
                               font=('微软雅黑', 6), anchor='w', wraplength=100)
                _dl.pack(fill='x')
                # Stats
                _stat_f = tk.Frame(_card, bg='#0f3460')
                _stat_f.pack(fill='x', padx=4, pady=(0, 2))
                _st = _tpl
                _stat_txt = f'HP {_st["base_health"]}  ATK {_st["base_attack"]}  DEF {_st["base_defense"]}  SPD {_st["base_speed"]}'
                _sl2 = tk.Label(_stat_f, text=_stat_txt, fg='#66bb6a', bg='#0f3460',
                                font=('Consolas', 6))
                _sl2.pack()
                _on_card_click(_card, lambda e, _tid=_tid, _tpl=_tpl: self._show_bestiary_detail(_tid, _tpl))

            # support enemies section after all map sections
        _sup_header = tk.Frame(self._bestiary_list_frame, bg='#1a1a2e')
        _sup_header.pack(fill='x', padx=20, pady=(15, 5))
        tk.Label(_sup_header, text='辅助/光环敌人', fg='#ffd700', bg='#1a1a2e',
                 font=('微软雅黑', 12, 'bold')).pack(side='left')
        _sup_list = [
            ('commander', '指挥官', '#ffd700', '攻击灵气+防御灵气'),
            ('war_drummer', '战鼓手', '#ffd700', '速度灵气+治愈灵气'),
            ('guardian_spirit', '守护之灵', '#ffd700', '钢铁意志+护盾灵气'),
            ('vengeful_wraith', '复仇之魂', '#ffd700', '怒火+复仇'),
            ('corruption_source', '腐蚀之源', '#ffd700', '毒瘴灵气+净化祝福'),
        ]
        _sf = tk.Frame(self._bestiary_list_frame, bg='#16213e', highlightbackground='#ffd700', highlightthickness=1)
        _sf.pack(fill='x', padx=20, pady=(0, 10))
        for _name, _cn, _cc, _desc in _sup_list:
            if _name not in ENEMY_TEMPLATES:
                continue
            _tpl = ENEMY_TEMPLATES[_name]
            _card = tk.Frame(_sf, bg='#0f3460', highlightbackground='#ffd700', highlightthickness=1)
            _card.pack(side='left', padx=4, pady=4)
            _inner_card = tk.Frame(_card, bg='#0f3460')
            _inner_card.pack(padx=4, pady=2)
            _spr_list = self._enemy_sprites.get(_name)
            if _spr_list:
                tk.Label(_inner_card, image=_spr_list[0], bg='#0f3460').pack(side='left', padx=(0, 4))
            tk.Label(_inner_card, text=_tpl['name'], fg='#ffd700', bg='#0f3460',
                     font=('微软雅黑', 8, 'bold')).pack(side='left')
            tk.Label(_card, text=_tpl.get('description', ''), fg='#aaaaaa', bg='#0f3460',
                     font=('微软雅黑', 6), wraplength=140).pack(padx=4, pady=(0, 2))
            _on_card_click(_card, lambda e, _n=_name, _t=_tpl: self._show_bestiary_detail(_n, _t))

        # Boss section
        _boss_header = tk.Frame(self._bestiary_list_frame, bg='#1a1a2e')
        _boss_header.pack(fill='x', padx=20, pady=(15, 5))
        tk.Label(_boss_header, text='首领/精英敌人', fg='#ff4444', bg='#1a1a2e',
                 font=('微软雅黑', 12, 'bold')).pack(side='left')
        _boss_list = ['devourer', 'void_overlord', 'abyss_lord', 'bone_dragon', 'mech_god', 'void_destroyer']
        _bf = tk.Frame(self._bestiary_list_frame, bg='#16213e', highlightbackground='#ff4444', highlightthickness=1)
        _bf.pack(fill='x', padx=20, pady=(0, 20))
        for _name in _boss_list:
            if _name not in ENEMY_TEMPLATES:
                continue
            _tpl = ENEMY_TEMPLATES[_name]
            _card = tk.Frame(_bf, bg='#0f3460', highlightbackground='#ff4444', highlightthickness=1)
            _card.pack(side='left', padx=4, pady=4)
            _inner_card = tk.Frame(_card, bg='#0f3460')
            _inner_card.pack(padx=4, pady=2)
            _spr_list2 = self._enemy_sprites.get(_name)
            if _spr_list2:
                tk.Label(_inner_card, image=_spr_list2[0], bg='#0f3460').pack(side='left', padx=(0, 4))
            tk.Label(_inner_card, text=_tpl['name'], fg='#ff4444', bg='#0f3460',
                     font=('微软雅黑', 8, 'bold')).pack(side='left')
            _st = _tpl
            tk.Label(_card, text=f'HP {_st["base_health"]} ATK {_st["base_attack"]} DEF {_st["base_defense"]} SPD {_st["base_speed"]}',
                     fg='#66bb6a', bg='#0f3460', font=('Consolas', 6)).pack(padx=4)
            tk.Label(_card, text=_tpl.get('description', ''), fg='#aaaaaa', bg='#0f3460',
                     font=('微软雅黑', 6), wraplength=140).pack(padx=4, pady=(0, 2))
            _on_card_click(_card, lambda e, _n=_name, _t=_tpl: self._show_bestiary_detail(_n, _t))

    def _show_bestiary_detail(self, tid, tpl):
        if hasattr(self, '_detail_anim_id'):
            self.root.after_cancel(self._detail_anim_id)
            self._detail_anim_id = None
        for w in self._bestiary_detail_frame.winfo_children():
            w.destroy()

        _boss = tid in BOSS_STAT_MULTIPLIERS
        _bm = BOSS_STAT_MULTIPLIERS.get(tid, 1.0)
        _df = self._bestiary_detail_frame
        _df.tkraise()

        _top = tk.Frame(_df, bg='#1a1a2e')
        _top.pack(fill='x', padx=24, pady=(20, 0))
        if hasattr(self, '_enemy_sprites') and tid in self._enemy_sprites:
            _frames = self._enemy_sprites[tid]
            _sl = tk.Label(_top, image=_frames[0], bg='#1a1a2e')
            _sl.pack(side='left', padx=(0, 16))
            _sl._anim_frames = _frames
            _sl._anim_idx = 0
            def _anim():
                if not _sl.winfo_exists():
                    return
                _sl._anim_idx = (_sl._anim_idx + 1) % len(_sl._anim_frames)
                _sl.config(image=_sl._anim_frames[_sl._anim_idx])
                self._detail_anim_id = self.root.after(800, _anim)
            self._detail_anim_id = self.root.after(800, _anim)
        _nf = '#ff4444' if _boss else '#00d9ff'
        _info = tk.Frame(_top, bg='#1a1a2e')
        _info.pack(side='left', fill='x', expand=True)
        tk.Label(_info, text=tpl['name'], fg=_nf, bg='#1a1a2e',
                 font=('微软雅黑', 22, 'bold'), anchor='w').pack(fill='x')
        tk.Label(_info, text=tpl.get('description', ''), fg='#aaaaaa', bg='#1a1a2e',
                 font=('微软雅黑', 11), anchor='w').pack(fill='x', pady=(4, 0))

        _st = tpl
        ttk.Separator(_df, orient='horizontal').pack(fill='x', padx=24, pady=14)

        _sw = tk.Frame(_df, bg='#16213e')
        _sw.pack(fill='x', padx=24, pady=(0, 10))
        tk.Label(_sw, text=f'基础生命: {_st["base_health"]}    基础攻击: {_st["base_attack"]}', fg='#66bb6a', bg='#16213e',
                 font=('Consolas', 12), anchor='w').pack(fill='x', padx=14, pady=(8, 0))
        tk.Label(_sw, text=f'基础防御: {_st["base_defense"]}    基础速度: {_st["base_speed"]}', fg='#66bb6a', bg='#16213e',
                 font=('Consolas', 12), anchor='w').pack(fill='x', padx=14, pady=(2, 4))
        if _bm > 1.0:
            tk.Label(_sw, text=f'首领倍率: ×{_bm}', fg='#ff4444', bg='#16213e',
                     font=('微软雅黑', 12, 'bold'), anchor='w').pack(fill='x', padx=14, pady=(2, 8))
        _min_s = tpl.get('min_skills', 1)
        _max_s = tpl.get('max_skills', 1)
        _trigger_all = tpl.get('trigger_all_skills', False)
        _sk_str = f'技能数量: {_min_s}~{_max_s}'
        if _trigger_all:
            _sk_str += '  (每回合发动全部技能)'
        tk.Label(_sw, text=_sk_str, fg='#ffd700', bg='#16213e',
                 font=('微软雅黑', 11), anchor='w').pack(fill='x', padx=14, pady=(0, 8))

        ttk.Separator(_df, orient='horizontal').pack(fill='x', padx=24, pady=6)

        _skills = tpl.get('skills_pool', [])
        if _skills:
            tk.Label(_df, text='▎技能池', fg='#00d9ff', bg='#1a1a2e',
                     font=('微软雅黑', 14, 'bold'), anchor='w').pack(fill='x', padx=24)
            _sf = tk.Frame(_df, bg='#0f3460')
            _sf.pack(fill='x', padx=24, pady=(4, 12))
            for _sk in _skills:
                _sk_info = SKILL_EFFECTS.get(_sk, {})
                _sk_type = _sk_info.get('type', '?')
                _sk_desc = _sk_info.get('description', '无描述')
                _row = tk.Frame(_sf, bg='#0f3460')
                _row.pack(fill='x', padx=10, pady=3)
                tk.Label(_row, text=f'▪ {_sk}', fg='#ffd700', bg='#0f3460',
                         font=('微软雅黑', 11, 'bold'), anchor='w', width=14).pack(side='left')
                tk.Label(_row, text=f'[{_sk_type}]', fg='#88ccff', bg='#0f3460',
                         font=('Consolas', 10), anchor='w').pack(side='left', padx=(0, 8))
                tk.Label(_row, text=_sk_desc, fg='#cccccc', bg='#0f3460',
                         font=('微软雅黑', 10), anchor='w').pack(side='left')

        _passives = tpl.get('passive_abilities', [])
        if _passives:
            tk.Label(_df, text='▎被动能力', fg='#ffb74d', bg='#1a1a2e',
                     font=('微软雅黑', 14, 'bold'), anchor='w').pack(fill='x', padx=24, pady=(8, 0))
            _pf = tk.Frame(_df, bg='#0f3460')
            _pf.pack(fill='x', padx=24, pady=(4, 12))
            for _pa in _passives:
                _pa_info = ENEMY_PASSIVES.get(_pa, {})
                _pa_name = _pa_info.get('name', _pa)
                _pa_desc = _pa_info.get('description', '')
                _row = tk.Frame(_pf, bg='#0f3460')
                _row.pack(fill='x', padx=10, pady=3)
                tk.Label(_row, text=f'◇ {_pa_name}', fg='#ffb74d', bg='#0f3460',
                         font=('微软雅黑', 11, 'bold'), anchor='w', width=14).pack(side='left')
                tk.Label(_row, text=_pa_desc, fg='#cccccc', bg='#0f3460',
                         font=('微软雅黑', 10), anchor='w').pack(side='left')

        if tpl.get('annihilate'):
            _af = tk.Frame(_df, bg='#4a0000')
            _af.pack(fill='x', padx=24, pady=(8, 10))
            tk.Label(_af, text='⚠ 死亡时触发特殊效果（自爆/毁灭）', fg='#ff6666', bg='#4a0000',
                     font=('微软雅黑', 11, 'bold')).pack(padx=10, pady=5)

        _back = tk.Button(_df, text='← 返回图鉴', command=self._back_to_bestiary_list,
                          bg='#0f3460', fg='#ffffff', font=('微软雅黑', 12),
                          activebackground='#1a5276', activeforeground='#ffffff',
                          bd=0, padx=40, pady=8)
        _back.pack(pady=(16, 20))

    def _back_to_bestiary_list(self):
        if hasattr(self, '_detail_anim_id'):
            self.root.after_cancel(self._detail_anim_id)
            self._detail_anim_id = None
        self._bestiary_list_frame.tkraise()
        self.root.update_idletasks()
        if hasattr(self, '_bestiary_cv'):
            self._bestiary_cv.configure(scrollregion=self._bestiary_cv.bbox('all'))
            self._bestiary_cv.yview_moveto(0)

    def get_available_stages(self):
        stages = []
        for i in self.game.unlocked_stages:
            if i in STAGES:
                stage = STAGES[i]
                stages.append(f"{i}. {stage['name']}")
        return stages
    
    def _get_selected_stage_num(self):
        sel = self.stage_combo.get()
        try:
            return int(sel.split('.')[0])
        except (ValueError, IndexError, AttributeError):
            return 1

    def _on_stage_changed(self, event=None):
        stage_num = self._get_selected_stage_num()
        gs = 3
        max_team = BATTLE_CONFIG['max_team_size']
        old = self.team_size_label.cget('text')
        new_label = f"{len(self.team_grid)}/{max_team} ({gs}×{gs})"
        if f'({gs}×{gs})' not in old:
            self.team_grid.clear()
            new_label = f"0/{max_team} ({gs}×{gs})"
        self.team_size_label.config(text=new_label)
        if stage_num in self.game.no_loss_stages and not self.continuous_mode:
            self.continuous_btn.config(state='normal')
        else:
            self.continuous_btn.config(state='disabled')

    def open_team_selection(self):
        alive_cards = [c for c in self.game.cards if c.is_alive]
        
        if not alive_cards:
            messagebox.showwarning("警告", "没有存活的卡牌")
            return
        
        stage_num = self._get_selected_stage_num()
        gs = 3
        _max_pos = gs * gs
        max_team = BATTLE_CONFIG['max_team_size']
        cell_size = 120
        title_text = f"选择战斗队伍 - {gs}x{gs} 网格布阵 (最多{max_team}张)"
        
        top = tk.Toplevel(self.root)
        top.title(title_text)
        top.geometry("900x650" if gs == 4 else "800x600")
        top.configure(bg="#1a1a2e")
        
        main_frame = tk.Frame(top, bg="#1a1a2e")
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 左侧：gs x gs 网格
        left_frame = tk.Frame(main_frame, bg="#1a1a2e")
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        tk.Label(left_frame, text=f"布阵网格 ({gs}x{gs})", bg="#1a1a2e", fg="#00d9ff",
                 font=('微软雅黑', 12, 'bold')).pack(pady=5)
        
        grid_frame = tk.Frame(left_frame, bg="#16213e", highlightbackground="#00d9ff",
                               highlightthickness=1)
        grid_frame.pack(pady=10)
        
        grid_cells = {}
        selected_cell = [None]
        
        def bind_cell_recursive(widget, pos):
            widget.bind('<Button-1>', lambda e, p=pos: on_cell_click(p), add='+')
            for child in widget.winfo_children():
                bind_cell_recursive(child, pos)
        
        def render_grid():
            for w in grid_frame.winfo_children():
                w.destroy()
            grid_cells.clear()
            for pos in range(_max_pos):
                row, col = pos // gs, pos % gs
                cell = tk.Frame(grid_frame, width=cell_size, height=cell_size-20, bg="#0f3460",
                                highlightbackground="#1a1a2e", highlightthickness=2)
                cell.grid(row=row, column=col, padx=4, pady=4)
                cell.grid_propagate(False)
                
                if pos in self.team_grid:
                    card = self.team_grid[pos]
                    gender_color = "#4a90d9" if card.gender == "male" else "#e74c8c"
                    gender_symbol = "♂" if card.gender == "male" else "♀"
                    
                    _pframes = None
                    if hasattr(self, '_player_card_sprites') and self._player_card_sprites:
                        _pidx = abs(hash(str(getattr(card, 'id', id(card))))) % len(self._player_card_sprites)
                        _pframes = self._player_card_sprites[_pidx]
                    if _pframes:
                        tk.Label(cell, image=_pframes[0], bg="#0f3460",
                                 borderwidth=0, highlightthickness=0).pack(pady=(4, 0))
                    
                    tk.Label(cell, text=f"{gender_symbol} {card.name}", fg=gender_color,
                             bg="#0f3460", font=('微软雅黑', 9, 'bold')).pack(pady=(8 if not _pframes else 2, 2))
                    tk.Label(cell, text=f"HP:{card.traits.get('health',50)}", fg="#4ecdc4",
                             bg="#0f3460", font=('Consolas', 8)).pack()
                    tk.Label(cell, text=f"ATK:{card.traits.get('attack',10)}", fg="#ff6b6b",
                             bg="#0f3460", font=('Consolas', 8)).pack()
                    tk.Label(cell, text=f"SPD:{card.traits.get('speed',10)}", fg="#ffd93d",
                             bg="#0f3460", font=('Consolas', 8)).pack()
                else:
                    tk.Label(cell, text=f"位置 {pos+1}", fg="#555555",
                             bg="#0f3460", font=('微软雅黑', 9)).pack(expand=True)
                
                bind_cell_recursive(cell, pos)
                grid_cells[pos] = cell
            
            update_info()
        
        def on_cell_click(pos):
            if selected_cell[0] is not None:
                if selected_cell[0] in grid_cells:
                    grid_cells[selected_cell[0]].configure(highlightbackground="#1a1a2e")
            
            if pos in self.team_grid:
                del self.team_grid[pos]
                render_grid()
                refresh_card_list()
                selected_cell[0] = None
                return
            
            if selected_cell[0] == pos:
                selected_cell[0] = None
            else:
                selected_cell[0] = pos
                if pos in grid_cells:
                    grid_cells[pos].configure(highlightbackground="#ffd93d")
        
        # 右侧：可用卡牌列表
        right_frame = tk.Frame(main_frame, bg="#1a1a2e")
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        tk.Label(right_frame, text="可用卡牌", bg="#1a1a2e", fg="#00d9ff",
                 font=('微软雅黑', 12, 'bold')).pack(pady=5)
        
        list_frame = tk.Frame(right_frame, bg="#1a1a2e")
        list_frame.pack(fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        card_listbox = tk.Listbox(list_frame, height=15,
                                   bg='#16213e', fg='#ffffff', font=('微软雅黑', 10),
                                   selectbackground='#0f3460', selectforeground='#ffffff')
        card_listbox.pack(side='left', fill='both', expand=True)
        card_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=card_listbox.yview)
        
        def refresh_card_list():
            card_listbox.delete(0, 'end')
            placed_ids = set(c.id for c in self.team_grid.values())
            for card in alive_cards:
                if card.id in placed_ids:
                    continue
                skills = ", ".join(card.skills[:3]) if card.skills else "无"
                card_listbox.insert('end', f"{card.name} ({'♂' if card.gender=='male' else '♀'}) HP:{card.traits.get('health',50)} ATK:{card.traits.get('attack',10)} SPD:{card.traits.get('speed',10)}")
        
        def on_card_select(evt):
            sel = card_listbox.curselection()
            if not sel:
                return
            if selected_cell[0] is None:
                messagebox.showwarning("提示", "请先在网格中点击一个位置")
                return
            pos = selected_cell[0]
            if pos in self.team_grid:
                messagebox.showwarning("提示", "该位置已有卡牌，点击可移除")
                return
            used = len(self.team_grid)
            if used >= max_team:
                messagebox.showwarning("提示", f"最多放置{max_team}张卡牌")
                return
            
            # 找到列表中实际未被放置的卡牌索引
            unplaced = [c for c in alive_cards if c.id not in set(x.id for x in self.team_grid.values())]
            if sel[0] < len(unplaced):
                card = unplaced[sel[0]]
                self.team_grid[pos] = card
                render_grid()
                refresh_card_list()
                selected_cell[0] = None
        
        card_listbox.bind('<Double-Button-1>', on_card_select)
        card_listbox.bind('<Return>', on_card_select)
        
        # 信息显示
        info_frame = tk.Frame(right_frame, bg="#1a1a2e")
        info_frame.pack(fill='x', pady=5)
        
        info_label = tk.Label(info_frame, text="", bg="#1a1a2e", fg="#aaaaaa",
                               font=('微软雅黑', 9), justify='left')
        info_label.pack()
        
        def update_info():
            used = len(self.team_grid)
            info_label.config(text=f"已放置: {used}/{max_team} 张卡牌\n"
                                   f"点击格子选中，双击卡牌放入\n"
                                   f"点击已放置的格子可移除卡牌")
        
        # 按钮
        btn_frame = tk.Frame(top, bg="#1a1a2e")
        btn_frame.pack(pady=10)
        
        def confirm_team():
            if not self.team_grid:
                messagebox.showwarning("警告", "请至少放置一张卡牌")
                return
            self.team_size_label.config(text=f"{len(self.team_grid)}/{max_team} ({gs}×{gs})")
            top.destroy()
        
        def clear_team():
            self.team_grid.clear()
            render_grid()
            refresh_card_list()
        
        tk.Button(btn_frame, text="确认编队", command=confirm_team,
                  bg="#0f3460", fg="#00d9ff", font=('微软雅黑', 10)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="清空", command=clear_team,
                  bg="#0f3460", fg="#ff6b6b", font=('微软雅黑', 10)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="取消", command=top.destroy,
                  bg="#0f3460", fg="#aaaaaa", font=('微软雅黑', 10)).pack(side='left', padx=5)
        
        render_grid()
        refresh_card_list()
    
    def start_battle(self, continuous=False):
        if not continuous:
            if not self.team_grid:
                messagebox.showwarning("警告", "请先选择队伍")
                return
            
            sel = self.stage_combo.get()
            try:
                stage_idx = int(sel.split('.')[0])
            except (ValueError, IndexError, AttributeError):
                messagebox.showwarning("警告", "关卡选择无效")
                return
            if stage_idx not in STAGES:
                messagebox.showwarning("警告", "关卡不存在")
                return
        
        stage_idx = self._get_selected_stage_num()
        stage_data = STAGES[stage_idx]
        enemy_list = stage_data['enemies'].copy()
        
        tech_level = self.game.tech_tree.get('skill_enhance', {}).get('level', 0)
        enemy_grid_size = stage_data.get('enemy_grid_size', None)
        self.battle_system = BattleSystem(self.team_grid, enemy_list, stage_idx, tech_level, enemy_grid_size)
        self.battle_is_running = True
        self.auto_battle = True
        self.fast_mode = continuous
        
        self.start_battle_btn.config(state='disabled')
        self.exit_battle_btn.config(state='normal')
        
        if not continuous or getattr(self, '_first_continuous', False):
            self._first_continuous = False
            self.show_battle_ui()
        
        self.add_battle_log("=" * 50)
        self.add_battle_log(f"【战斗开始】关卡: {stage_data['name']}")
        self.add_battle_log("-" * 40)
        enemy_gs = self.battle_system.enemy_grid_size
        self.add_battle_log("【敌方单位】")
        for i, e in enumerate(stage_data['enemies']):
            pos = e.get('position', i)
            r, c = pos // enemy_gs + 1, pos % enemy_gs + 1
            self.add_battle_log(f"  [{r},{c}] {e['name']}: HP={e['health']} ATK={e['attack']} DEF={e['defense']} SPD={e['speed']}")
        self.add_battle_log("-" * 40)
        self.add_battle_log("【我方队伍】")
        for pos, card in sorted(self.team_grid.items()):
            r, c = pos // self.battle_system.grid_size + 1, pos % self.battle_system.grid_size + 1
            skills = ", ".join(card.skills) if card.skills else "无"
            self.add_battle_log(f"  [{r},{c}] {card.name}: HP={card.traits.get('health',50)} ATK={card.traits.get('attack',10)} DEF={card.traits.get('defense',5)} SPD={card.traits.get('speed',10)} 技能:{skills}")
        self.add_battle_log("=" * 50)
        
        self.run_battle_turn()
    
    def _create_grid_cell(self, parent, unit, is_enemy):
        gs = self.battle_system.enemy_grid_size if is_enemy else self.battle_system.grid_size
        uw = getattr(unit, 'width', 1) if unit else 1
        uh = getattr(unit, 'height', 1) if unit else 1
        is_boss = uw > 1 or uh > 1
        base_w, base_h = (110, 80) if gs == 4 else (140, 90)
        w = base_w * uw + (uw - 1) * 6
        h = base_h * uh + (uh - 1) * 6

        if unit is None:
            cell = tk.Frame(parent, width=base_w, height=base_h, bg="#0f3460",
                            highlightbackground="#1a1a2e", highlightthickness=2)
            tk.Label(cell, text="— 空 —", fg="#333333", bg="#0f3460",
                     font=('微软雅黑', 9)).pack(expand=True)
            cell.pack_propagate(False)
            return cell, None
        
        cell = tk.Frame(parent, width=w, height=h,
                        bg="#16213e" if not is_enemy else "#1e1530",
                        highlightbackground="#ff0000" if is_boss else ("#00d9ff" if unit.is_alive else "#e74c3c"),
                        highlightthickness=3 if is_boss else 2)
        
        name_color = "#ff0000" if is_boss else ("#ff6b6b" if is_enemy else ("#4a90d9" if unit.gender == "male" else "#e74c8c"))
        if is_boss:
            name_prefix = f"【{uw}×{uh}】"
        elif is_enemy:
            name_prefix = "【敌】"
        else:
            name_prefix = "♂ " if unit.gender == "male" else "♀ "
        _small = gs == 4

        _sprite_frames = None
        if hasattr(self, '_enemy_sprites') and hasattr(self, '_enemy_sprite_map'):
            if is_enemy:
                _sprite_tid = self._enemy_sprite_map.get(unit.name)
                if _sprite_tid and _sprite_tid in self._enemy_sprites:
                    _sprite_frames = self._enemy_sprites[_sprite_tid]
            elif hasattr(self, '_block_library') and self._block_library and hasattr(unit, 'card') and getattr(unit.card, 'sprite_genome', None):
                _sprite_frames = self._compose_sprite_frames(unit.card.sprite_genome)
            elif hasattr(self, '_player_card_sprites') and self._player_card_sprites:
                _cid = getattr(unit, 'id', id(unit))
                _idx = abs(hash(str(_cid))) % len(self._player_card_sprites)
                _sprite_frames = self._player_card_sprites[_idx]
        if _sprite_frames:
            _sl = tk.Label(cell, image=_sprite_frames[0], bg=cell['bg'], borderwidth=0, highlightthickness=0)
            _sl.pack(pady=(1, 0))
            _sl._anim_frames = _sprite_frames
            _sl._anim_idx = 0
            _sl._anim_tid = id(cell)
            _sl._anim_cell_widget = cell
            _schedule = lambda: None
            def _anim_loop(sl=_sl):
                if not sl.winfo_exists():
                    return
                sl._anim_idx = (sl._anim_idx + 1) % len(sl._anim_frames)
                try:
                    sl.config(image=sl._anim_frames[sl._anim_idx])
                except tk.TclError:
                    return
                sl.after(400, _anim_loop)
            _sl.after(random.randint(0, 400), _anim_loop)

        tk.Label(cell, text=f"{name_prefix}{unit.name}", fg=name_color,
                 bg=cell['bg'], font=('微软雅黑', 7 if _small else 8, 'bold')).pack(pady=(2 if _small else 4, 0))
        
        health_percent = (unit.current_health / unit.max_health * 100) if unit.max_health > 0 else 0
        hp_color = "#2ecc71" if health_percent > 50 else ("#ffd93d" if health_percent > 25 else "#e74c3c")
        hp_label = tk.Label(cell, text=f"HP {unit.current_health}/{unit.max_health}  ATK {unit.attack}",
                            fg=hp_color, bg=cell['bg'], font=('Consolas', 6 if _small else 7))
        hp_label.pack()
        
        _bar_w = 95 if _small else 125
        hp_canvas = tk.Canvas(cell, width=_bar_w, height=14, bg='#222',
                              highlightthickness=0)
        hp_canvas.pack(padx=6, pady=(1, 0))
        hp_canvas._shield = 0
        hp_canvas._hp = 0
        self._redraw_hp_shield(hp_canvas, health_percent, 0, unit)
        
        action_bar = ttk.Progressbar(cell, length=_bar_w, maximum=100, mode='determinate')
        action_bar.pack(fill='x', padx=6, pady=(1, 0))
        action_bar['value'] = min(unit.action_bar, 100)
        
        unit._cell_frame = cell
        cell.pack_propagate(False)
        return cell, {'hp_canvas': hp_canvas, 'hp_label': hp_label, 'action': action_bar}

    def _rebuild_enemy_grid(self):
        if not hasattr(self, '_enemy_grid') or not self._enemy_grid.winfo_exists():
            return
        gs = self.battle_system.enemy_grid_size
        _max_pos = gs * gs
        for w in self._enemy_grid.winfo_children():
            w.destroy()
        self._enemy_cell_map.clear()
        enemy_pos_map = {e.position: e for e in self.battle_system.enemies}
        _rendered = set()
        for pos in range(_max_pos):
            if pos in _rendered:
                continue
            row, col = pos // gs, pos % gs
            unit = enemy_pos_map.get(pos, None)
            is_multi = unit and (getattr(unit, 'width', 1) > 1 or getattr(unit, 'height', 1) > 1) and unit.is_alive
            if is_multi:
                cell, widgets = self._create_grid_cell(self._enemy_grid, unit, is_enemy=True)
                cell.grid(row=row, column=col, rowspan=unit.height, columnspan=unit.width, padx=3, pady=3)
                for p in unit.occupied_positions:
                    _rendered.add(p)
                    self._enemy_cell_map[p] = cell
            else:
                cell, widgets = self._create_grid_cell(self._enemy_grid, unit, is_enemy=True)
                cell.grid(row=row, column=col, padx=3, pady=3)
                _rendered.add(pos)
                self._enemy_cell_map[pos] = cell
            if unit and unit.is_alive:
                cell.bind('<Button-1>', lambda e, u=unit: self._on_enemy_click(u))
            if unit and widgets:
                unit.status_widgets = widgets
        self._refresh_enemy_marks()

    def show_battle_ui(self):
        for widget in self.battle_area.winfo_children():
            widget.destroy()
        
        player_gs = self.battle_system.grid_size
        enemy_gs = self.battle_system.enemy_grid_size
        
        battle_canvas = tk.Frame(self.battle_area, bg="#1a1a2e")
        battle_canvas.pack(fill='both', expand=True, pady=5)
        
        enemy_pos_map = {e.position: e for e in self.battle_system.enemies}
        player_pos_map = {p.position: p for p in self.battle_system.player_team}
        
        center_frame = tk.Frame(battle_canvas, bg="#1a1a2e")
        self._battle_center_frame = center_frame
        center_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # 左：我方阵营
        left_frame = tk.Frame(center_frame, bg="#1a1a2e")
        left_frame.pack(side='left', padx=(0, 20))
        
        tk.Label(left_frame, text=f"— 我 方 阵 营 ({player_gs}x{player_gs}) —", fg="#4ecdc4", bg="#1a1a2e",
                 font=('微软雅黑', 14, 'bold')).pack(pady=(0, 8))
        
        self._player_grid = tk.Frame(left_frame, bg="#1a1a2e")
        self._player_grid.pack()
        self._player_cell_map = {}
        for pos in range(player_gs * player_gs):
            row, col = pos // player_gs, pos % player_gs
            unit = player_pos_map.get(pos, None)
            cell, widgets = self._create_grid_cell(self._player_grid, unit, is_enemy=False)
            cell.grid(row=row, column=col, padx=3, pady=3)
            self._player_cell_map[pos] = cell
            if unit and widgets:
                unit.status_widgets = widgets
        
        # 中：VS
        vs_frame = tk.Frame(center_frame, bg="#1a1a2e")
        vs_frame.pack(side='left', padx=10)
        
        vs_height = max(player_gs, enemy_gs) * 90
        tk.Frame(vs_frame, width=2, height=vs_height, bg="#00d9ff").pack()
        tk.Label(vs_frame, text=" VS ", fg="#ffd93d", bg="#1a1a2e",
                 font=('微软雅黑', 16, 'bold')).pack(pady=8)
        tk.Frame(vs_frame, width=2, height=vs_height, bg="#00d9ff").pack()
        
        # 右：敌方阵营
        right_frame = tk.Frame(center_frame, bg="#1a1a2e")
        right_frame.pack(side='left', padx=(20, 0))
        
        tk.Label(right_frame, text=f"— 敌 方 阵 营 ({enemy_gs}x{enemy_gs}) —", fg="#ff6b6b", bg="#1a1a2e",
                 font=('微软雅黑', 14, 'bold')).pack(pady=(0, 8))
        
        enemy_grid = tk.Frame(right_frame, bg="#1a1a2e")
        enemy_grid.pack()
        self._enemy_grid = enemy_grid
        self._enemy_cell_map = {}
        _rendered = set()
        for pos in range(enemy_gs * enemy_gs):
            if pos in _rendered:
                continue
            row, col = pos // enemy_gs, pos % enemy_gs
            unit = enemy_pos_map.get(pos, None)
            is_multi = unit and (getattr(unit, 'width', 1) > 1 or getattr(unit, 'height', 1) > 1) and unit.is_alive
            if is_multi:
                cell, widgets = self._create_grid_cell(enemy_grid, unit, is_enemy=True)
                cell.grid(row=row, column=col, rowspan=unit.height, columnspan=unit.width, padx=3, pady=3)
                for p in unit.occupied_positions:
                    _rendered.add(p)
                    self._enemy_cell_map[p] = cell
            else:
                cell, widgets = self._create_grid_cell(enemy_grid, unit, is_enemy=True)
                cell.grid(row=row, column=col, padx=3, pady=3)
                _rendered.add(pos)
                self._enemy_cell_map[pos] = cell
            if unit and widgets:
                unit.status_widgets = widgets
        
        self.exit_battle_btn.config(state='normal')
        
        for pos, cell in self._enemy_cell_map.items():
            unit = enemy_pos_map.get(pos)
            if unit and unit.is_alive:
                cell.bind('<Button-1>', lambda e, u=unit: self._on_enemy_click(u))
    
    def _on_enemy_click(self, unit):
        if not unit or not unit.is_alive:
            return
        if self.battle_system.marked_target is unit:
            self.battle_system.marked_target = None
        else:
            self.battle_system.marked_target = unit
        self._refresh_enemy_marks()
    
    def _set_enemy_mark(self, unit):
        cell = getattr(unit, '_cell_frame', None)
        if not cell:
            return
        if self.battle_system.marked_target is unit:
            cell.config(highlightbackground="#ffd93d", highlightthickness=3)
        else:
            gs = self.battle_system.enemy_grid_size
            is_boss = getattr(unit, 'width', 1) > 1 or getattr(unit, 'height', 1) > 1
            cell.config(highlightbackground="#ff0000" if is_boss else "#00d9ff", highlightthickness=3 if is_boss else 2)
    
    def _refresh_enemy_marks(self):
        if not self.battle_system:
            return
        for e in self.battle_system.enemies:
            self._set_enemy_mark(e)
    
    def run_battle_turn(self):
        if not self.battle_is_running or not self.battle_system:
            return
        if self.battle_system.check_winner():
            self.end_battle()
            return
        self.battle_system.update_action_bars_frame()
        self.update_battle_display()
        self._process_next_unit()

    def _prepare_battle_tick(self):
        if not hasattr(self, '_battle_frame_counter'):
            self._battle_frame_counter = 0

    def _process_next_unit(self):
        unit = self.battle_system.get_next_unit()
        if not unit:
            self._prepare_battle_tick()
            self._battle_frame_counter += 1
            if self._battle_frame_counter >= 12:
                self._battle_frame_counter = 0
                _all = self.battle_system._all_units_cache
                for u in _all:
                    if u.is_alive:
                        u.update_status()
                self.battle_system.update_status_damage()
                self.battle_system.process_purify()
                self.battle_system.process_enemy_passives()
                for removed in self.battle_system.cleanup_summons():
                    self._remove_summon_from_grid(removed)
                    self.add_battle_log(f"  {removed.name} 消失了")
            if self.battle_is_running and hasattr(self, 'auto_battle') and self.auto_battle:
                delay = 10 if self.fast_mode else 33
                self.root.after(delay, self.run_battle_turn)
            return

        unit.action_bar = 0
        if not (unit.is_alive and unit.can_act()):
            self._process_next_unit()
            return

        _all = self.battle_system._all_units_cache
        alive_before = {id(u) for u in _all if u.is_alive}

        if unit.is_player:
            targets = [e for e in self.battle_system.enemies if e.is_alive]
            result = self.battle_system.execute_turn(unit, targets)
        else:
            result = self.battle_system.execute_turn(unit, None)

        logs = list(self.battle_system.battle_log)
        self.battle_system.battle_log.clear()

        alive_after = {id(u) for u in _all if u.is_alive}
        had_death = bool(alive_before - alive_after)

        reflex_result = result.get('reflex_result') if result else None

        def on_anim_done():
            if result and result.get('summon'):
                self._add_summon_to_grid(result['summon'])
            for msg in logs:
                self.add_battle_log(msg)
            if result and result.get('healed_units'):
                heal_amount = result.get('heal_amount', 0)
                unit_map = {}
                for u in _all:
                    uid = u.id if hasattr(u, 'id') else id(u)
                    unit_map[uid] = u
                for uid in result['healed_units']:
                    healed = unit_map.get(uid)
                    if healed:
                        tcell = getattr(healed, '_cell_frame', None)
                        if tcell:
                            self._show_floating_number(tcell, heal_amount, False, is_heal=True)
            self.update_battle_display()
            if result and result.get('skill') == '观星':
                self._rebuild_enemy_grid()
            if had_death:
                _play_sound('death')

            if reflex_result and reflex_result.get('target_obj'):
                def reflex_anim_done():
                    if reflex_result.get('summon'):
                        self._add_summon_to_grid(reflex_result['summon'])
                    if reflex_result.get('healed_units'):
                        heal_amount = reflex_result.get('heal_amount', 0)
                        unit_map = {}
                        for u in self.battle_system.get_all_units():
                            uid = u.id if hasattr(u, 'id') else id(u)
                            unit_map[uid] = u
                        for uid in reflex_result['healed_units']:
                            healed = unit_map.get(uid)
                            if healed:
                                tcell = getattr(healed, '_cell_frame', None)
                                if tcell:
                                    self._show_floating_number(tcell, heal_amount, False, is_heal=True)
                    self.update_battle_display()
                    if self.battle_system.check_winner():
                        self.end_battle()
                        return
                    if had_death:
                        if self.battle_is_running and hasattr(self, 'auto_battle') and self.auto_battle:
                            death_delay = 80 if self.fast_mode else 500
                            self.root.after(death_delay, self._process_next_unit)
                        return
                    self._process_next_unit()

                if reflex_result.get('annihilated'):
                    annihilator = reflex_result.get('annihilator_obj')
                    atk_reflex = reflex_result.get('attacker_obj')
                    if annihilator and atk_reflex:
                        self._play_annihilate_anim(annihilator, atk_reflex, reflex_anim_done)
                    else:
                        reflex_anim_done()
                else:
                    ratk_obj = reflex_result['attacker_obj']
                    rtgt_obj = reflex_result['target_obj']
                    rdamage = reflex_result.get('damage', 0)
                    rcrit = reflex_result.get('critical', False)
                    rskill_name = reflex_result.get('skill')
                    self._play_attack_anim(ratk_obj, rtgt_obj, rdamage, rcrit, True, reflex_anim_done, rskill_name)
                return

            if self.battle_system.check_winner():
                self.end_battle()
                return
            if had_death:
                if self.battle_is_running and hasattr(self, 'auto_battle') and self.auto_battle:
                    death_delay = 80 if self.fast_mode else 500
                    self.root.after(death_delay, self._process_next_unit)
                return
            self._process_next_unit()

        if result and result.get('annihilated'):
            annihilator = result.get('annihilator_obj')
            atk_obj = result['attacker_obj']
            if annihilator and atk_obj:
                self._play_annihilate_anim(annihilator, atk_obj, on_anim_done)
            else:
                on_anim_done()
        elif result and result.get('type') == 'aoe_attack':
            atk_obj = result['attacker_obj']
            alive = [p for p in self.battle_system.player_team if p.is_alive]
            first = alive[0] if alive else None
            if first:
                is_critical = result.get('critical', False)
                self._play_attack_anim(atk_obj, first, result.get('damage', 0), is_critical, False, on_anim_done)
            else:
                on_anim_done()
        elif result and result.get('skill') == '观星':
            on_anim_done()
        elif result and result.get('target_obj'):
            atk_obj = result['attacker_obj']
            tgt_obj = result['target_obj']
            damage = result.get('damage', 0)
            is_critical = result.get('critical', False)
            is_skill = result.get('type') == 'skill'
            skill_name = result.get('skill') if is_skill else None
            self._play_attack_anim(atk_obj, tgt_obj, damage, is_critical, is_skill, on_anim_done, skill_name)
        else:
            on_anim_done()
    
    def _redraw_hp_shield(self, canvas, hp_pct, shield_pct, unit):
        if not canvas or not canvas.winfo_exists():
            return
        w = 125
        h = 14
        try:
            canvas.delete('all')
        except tk.TclError:
            return
        try:
            canvas.create_rectangle(0, 0, w, h, fill='#222', outline='#444', width=1)

            if getattr(unit, 'purify_shield_expires', 0.0) > time.time():
                hp_color = "#00e5ff"
            elif hasattr(unit, 'has_status') and unit.has_status('poison'):
                hp_color = "#9b59b6"
            else:
                hp_color = "#2ecc71" if hp_pct > 50 else ("#ffd93d" if hp_pct > 25 else "#e74c3c")
            hp_w = max(0, int(w * hp_pct / 100))
            if hp_w > 0:
                canvas.create_rectangle(0, 0, hp_w, h, fill=hp_color, outline='')

            shield_bar_pct = shield_pct
            shield_w = max(0, int(w * shield_bar_pct / 100))
            if shield_w > 0:
                canvas.create_rectangle(0, 4, shield_w, h - 4, fill='#3498db', outline='')

            canvas._hp = hp_pct
            canvas._shield = shield_pct
        except tk.TclError:
            pass

    def update_battle_display(self):
        if not self.battle_system:
            return
        
        if self.battle_system.marked_target and not self.battle_system.marked_target.is_alive:
            self.battle_system.marked_target = None
        
        for enemy in self.battle_system.enemies:
            sw = getattr(enemy, 'status_widgets', None)
            if not sw:
                continue
            try:
                mh = enemy.max_health
                if mh <= 0:
                    continue
                hp_pct = (enemy.current_health / mh * 100)
                sh_pct = (enemy.shield / mh * 100)
                canvas = sw.get('hp_canvas')
                if canvas:
                    self._redraw_hp_shield(canvas, hp_pct, sh_pct, enemy)
                hp_label = sw.get('hp_label')
                if hp_label:
                    hp_text = f"HP {enemy.current_health}/{mh}  ATK {enemy.attack}"
                    if hp_label.cget('text') != hp_text:
                        clr = "#2ecc71" if hp_pct > 50 else ("#ffd93d" if hp_pct > 25 else "#e74c3c")
                        hp_label.config(text=hp_text, fg=clr)
                bar = sw.get('action')
                if bar and bar.winfo_exists():
                    bar['value'] = min(enemy.action_bar, 100)
            except (tk.TclError, KeyError):
                pass
        
        for player in self.battle_system.player_team:
            sw = getattr(player, 'status_widgets', None)
            if not sw:
                continue
            try:
                mh = player.max_health
                if mh <= 0:
                    continue
                hp_pct = (player.current_health / mh * 100)
                sh_pct = (player.shield / mh * 100)
                canvas = sw.get('hp_canvas')
                if canvas:
                    self._redraw_hp_shield(canvas, hp_pct, sh_pct, player)
                hp_label = sw.get('hp_label')
                if hp_label:
                    hp_text = f"HP {player.current_health}/{mh}  ATK {player.attack}"
                    if hp_label.cget('text') != hp_text:
                        clr = "#2ecc71" if hp_pct > 50 else ("#ffd93d" if hp_pct > 25 else "#e74c3c")
                        hp_label.config(text=hp_text, fg=clr)
                bar = sw.get('action')
                if bar and bar.winfo_exists():
                    bar['value'] = min(player.action_bar, 100)
            except (tk.TclError, KeyError):
                pass
        self._refresh_enemy_marks()
    
    def _get_unit_cell_center(self, unit):
        cell = getattr(unit, '_cell_frame', None)
        if not cell or not self._battle_center_frame:
            return None, None
        cfx = self._battle_center_frame.winfo_rootx()
        cfy = self._battle_center_frame.winfo_rooty()
        cx = cell.winfo_rootx() - cfx + cell.winfo_width() // 2
        cy = cell.winfo_rooty() - cfy + cell.winfo_height() // 2
        return cx, cy

    def _screen_shake(self, intensity):
        if intensity <= 0 or not self._battle_center_frame:
            return
        cf = self._battle_center_frame
        for _ in range(3):
            rx = random.randint(-intensity, intensity)
            ry = random.randint(-intensity, intensity)
            cf.place_configure(x=rx, y=ry)
            self.root.update_idletasks()
            self.root.after(15)
        cf.place_configure(x=0, y=0)

    def _play_attack_anim(self, attacker, target, damage, is_critical, is_skill, callback=None, skill_name=None):
        if self.fast_mode:
            if callback:
                callback()
            return
        cell = getattr(attacker, '_cell_frame', None)
        tcell = getattr(target, '_cell_frame', None)
        if not cell or not tcell or not self._battle_center_frame:
            if callback: callback()
            return
        if not cell.winfo_exists() or not tcell.winfo_exists():
            if callback: callback()
            return

        cfx = self._battle_center_frame.winfo_rootx()
        cfy = self._battle_center_frame.winfo_rooty()
        try:
            sx = cell.winfo_rootx() - cfx
            sy = cell.winfo_rooty() - cfy
            ex = tcell.winfo_rootx() - cfx
            ey = tcell.winfo_rooty() - cfy
            cw = cell.winfo_width()
            ch = cell.winfo_height()
        except tk.TclError:
            if callback: callback()
            return

        border_color = "#ffd93d" if is_critical else ("#4ecdc4" if is_skill else "#ff4444")
        try:
            cell.grid_remove()
        except tk.TclError:
            if callback: callback()
            return
        self.root.update_idletasks()

        try:
            proxy = tk.Frame(self._battle_center_frame, width=cw, height=ch,
                             bg="#16213e", highlightbackground=border_color, highlightthickness=3)
        except tk.TclError:
            cell.grid()
            if callback: callback()
            return
        aname = attacker.name if hasattr(attacker, 'name') else '?'
        hp_cur = getattr(attacker, 'current_health', '?')
        hp_max = getattr(attacker, 'max_health', '?')
        tk.Label(proxy, text=aname, fg="#ffffff", bg="#16213e",
                 font=('微软雅黑', 8, 'bold')).pack(pady=(10, 0))
        tk.Label(proxy, text=f"HP {hp_cur}/{hp_max}", fg="#2ecc71", bg="#16213e",
                 font=('Consolas', 7)).pack()
        proxy.place(x=sx, y=sy)
        proxy.lift()

        frames = 4
        dx = (ex - sx) / frames
        dy = (ey - sy) / frames

        def step(n=0):
            if n >= frames:
                proxy.destroy()
                try:
                    cell.grid()
                except tk.TclError:
                    pass
                _play_sound('critical' if is_critical else ('skill' if is_skill else 'hit'))
                shake_intensity = int(min(damage // 5, 30))
                if is_critical:
                    shake_intensity = int(shake_intensity * 1.5)
                self._screen_shake(shake_intensity)
                self._show_floating_number(tcell, damage, is_critical)
                if skill_name == '毒液攻击':
                    self._show_poison_mist(tcell)
                if callback:
                    callback()
                return
            try:
                proxy.place(x=sx + dx * n, y=sy + dy * n)
            except tk.TclError:
                return
            self.root.after(10, lambda: step(n + 1))

        step()

    def _play_annihilate_anim(self, annihilator, attacker, callback=None):
        if self.fast_mode:
            if callback:
                callback()
            return
        cell = getattr(annihilator, '_cell_frame', None)
        tcell = getattr(attacker, '_cell_frame', None)
        if not cell or not tcell or not self._battle_center_frame:
            if callback: callback()
            return
        if not cell.winfo_exists() or not tcell.winfo_exists():
            if callback: callback()
            return

        cfx = self._battle_center_frame.winfo_rootx()
        cfy = self._battle_center_frame.winfo_rooty()
        try:
            sx = cell.winfo_rootx() - cfx
            sy = cell.winfo_rooty() - cfy
            ex = tcell.winfo_rootx() - cfx
            ey = tcell.winfo_rooty() - cfy
            cw = cell.winfo_width()
            ch = cell.winfo_height()
        except tk.TclError:
            if callback: callback()
            return

        try:
            cell.grid_remove()
        except tk.TclError:
            if callback: callback()
            return
        self.root.update_idletasks()

        try:
            proxy = tk.Frame(self._battle_center_frame, width=cw, height=ch,
                             bg="#2d0000", highlightbackground="#ff1100", highlightthickness=2)
        except tk.TclError:
            cell.grid()
            if callback: callback()
            return
        proxy.place(x=sx, y=sy)
        proxy.lift()

        fly_frames = 8
        fdx = (ex - sx) / fly_frames
        fdy = (ey - sy) / fly_frames

        def phase2():
            proxy.destroy()
            self.update_battle_display()
            try:
                canvas = tk.Canvas(self._battle_center_frame, width=cw, height=ch,
                                   bg='', highlightthickness=0, bd=0)
            except tk.TclError:
                cell.grid()
                if callback: callback()
                return
            canvas.place(x=ex, y=ey)
            canvas.lift()

            max_r = max(cw, ch) // 2
            ball = canvas.create_oval(cw // 2, ch // 2, cw // 2, ch // 2,
                                      fill='black', outline='')

            grow_frames = 8

            def grow(n=0):
                if n > grow_frames:
                    canvas.destroy()
                    self._screen_shake(15)
                    if callback:
                        callback()
                    return
                t = n / grow_frames
                r = int(max_r * t)
                try:
                    canvas.coords(ball,
                                  cw // 2 - r, ch // 2 - r,
                                  cw // 2 + r, ch // 2 + r)
                except tk.TclError:
                    if callback: callback()
                    return
                self.root.after(15, lambda: grow(n + 1))

            grow()

        def fly(n=0):
            if n > fly_frames:
                phase2()
                return
            px = int(sx + fdx * n)
            py = int(sy + fdy * n)
            try:
                proxy.place(x=px, y=py)
            except tk.TclError:
                proxy.destroy()
                self.update_battle_display()
                if callback: callback()
                return
            self.root.after(15, lambda: fly(n + 1))

        fly()

    def _show_floating_number(self, cell, damage, is_critical, is_heal=False):
        if not cell or not self._battle_center_frame:
            return
        if not cell.winfo_exists() or not self._battle_center_frame.winfo_exists():
            return
        cfx = self._battle_center_frame.winfo_rootx()
        cfy = self._battle_center_frame.winfo_rooty()
        cx = cell.winfo_rootx() - cfx + cell.winfo_width() // 2
        cy = cell.winfo_rooty() - cfy + cell.winfo_height() // 4

        if is_heal:
            color = '#2ecc71'
            font_spec = ('Consolas', 14, 'bold')
        elif is_critical:
            color = '#ffd93d'
            font_spec = ('Consolas', 18, 'bold')
        else:
            color = '#ff6b6b'
            font_spec = ('Consolas', 14, 'bold')

        prefix = '+' if is_heal else ''
        label = tk.Label(self._battle_center_frame, text=f'{prefix}{damage}',
                         fg=color, bg='#1a1a2e', font=font_spec)
        label.place(x=cx, y=cy, anchor='center')
        label.lift()

        frames = 15

        def float_up(n=0):
            if n >= frames:
                label.destroy()
                return
            alpha = 1.0 - n / frames
            label.place(x=cx, y=cy - n * 3)
            if is_heal:
                r, g, b = 46, 204, 113
            elif is_critical:
                r, g, b = 255, 217, 61
            else:
                r, g, b = 255, 107, 107
            r, g, b = int(r * alpha), int(g * alpha), int(b * alpha)
            label.config(fg=f'#{r:02x}{g:02x}{b:02x}')
            self.root.after(20, lambda: float_up(n + 1))

        float_up()

    def _show_poison_mist(self, cell):
        if not cell or not self._poison_img or not self._battle_center_frame:
            return
        cfx = self._battle_center_frame.winfo_rootx()
        cfy = self._battle_center_frame.winfo_rooty()
        cx = cell.winfo_rootx() - cfx + cell.winfo_width() // 2
        cy = cell.winfo_rooty() - cfy + cell.winfo_height() // 2
        label = tk.Label(self._battle_center_frame, image=self._poison_img, bg='#1a1a2e')
        label.place(x=cx, y=cy, anchor='center')
        label.lift()
        self.root.after(600, label.destroy)

    def _add_summon_to_grid(self, minion):
        pos = minion.position
        gs = minion.grid_size
        is_enemy_side = not minion.is_player
        grid = self._enemy_grid if is_enemy_side else self._player_grid
        cell_map = self._enemy_cell_map if is_enemy_side else self._player_cell_map
        cell, widgets = self._create_grid_cell(grid, minion, is_enemy=is_enemy_side)
        row, col = pos // gs, pos % gs
        cell.grid(row=row, column=col, padx=3, pady=3)
        cell_map[pos] = cell
        minion.status_widgets = widgets
        if is_enemy_side and minion.is_alive:
            cell.bind('<Button-1>', lambda e, u=minion: self._on_enemy_click(u))

    def _remove_summon_from_grid(self, minion):
        pos = minion.position
        gs = minion.grid_size
        is_enemy_side = not minion.is_player
        grid = self._enemy_grid if is_enemy_side else self._player_grid
        cell_map = self._enemy_cell_map if is_enemy_side else self._player_cell_map
        cell = cell_map.get(pos)
        if cell:
            cell.destroy()
            empty, _ = self._create_grid_cell(grid, None, is_enemy=is_enemy_side)
            row, col = pos // gs, pos % gs
            empty.grid(row=row, column=col, padx=3, pady=3)
            cell_map[pos] = empty

    def _show_damage_stats(self):
        bs = self.battle_system
        lines = ["", "─" * 50, "  伤害统计", "─" * 50]
        player_total = sum(u.total_damage_dealt for u in bs.player_team)
        enemy_total = sum(u.total_damage_dealt for u in bs.enemies)
        lines.append(f"  我方总伤害: {player_total}")
        for u in sorted(bs.player_team, key=lambda x: x.total_damage_dealt, reverse=True):
            lines.append(f"    {u.name}: {u.total_damage_dealt}")
        lines.append(f"  敌方总伤害: {enemy_total}")
        for u in sorted(bs.enemies, key=lambda x: x.total_damage_dealt, reverse=True):
            lines.append(f"    {u.name}: {u.total_damage_dealt}")
        return '\n'.join(lines)

    def _give_spirit_rewards(self):
        spirit_level = (
            (3 if self.game.tech_tree.get('spirit_large', {}).get('level', 0) > 0 else
             2 if self.game.tech_tree.get('spirit_medium', {}).get('level', 0) > 0 else
             1 if self.game.tech_tree.get('spirit_small', {}).get('level', 0) > 0 else 0)
        )
        if spirit_level == 1:
            card = self.game.generate_low_quality_card()
            if card:
                self.add_battle_log(f"🪽 小精灵送来: {card.name}")
        elif spirit_level == 2:
            for _ in range(2):
                card = self.game.generate_low_quality_card()
                if card:
                    self.add_battle_log(f"🪽 中精灵送来: {card.name}")
        elif spirit_level == 3:
            card_m = self.game.generate_low_quality_card(gender='male')
            card_f = self.game.generate_low_quality_card(gender='female')
            if card_m:
                self.add_battle_log(f"🪽 大精灵送来 ♂: {card_m.name}")
            if card_f:
                self.add_battle_log(f"🪽 大精灵送来 ♀: {card_f.name}")

    def _start_continuous_battle(self):
        if not self.team_grid:
            messagebox.showwarning("警告", "请先选择队伍")
            return
        stage_num = self._get_selected_stage_num()
        if stage_num not in self.game.no_loss_stages:
            messagebox.showwarning("警告", "该关卡尚未无损失通关")
            return
        self.continuous_mode = True
        self.continuous_count = 0
        self.continuous_total_gacha = 0
        self.continuous_total_materials = 0
        self.continuous_btn.config(state='disabled')
        self.continuous_stop_btn.config(state='normal')
        self.stage_combo.config(state='disabled')
        self.continuous_status.config(text="连续作战准备中...")
        self.fast_mode = True
        self._first_continuous = True
        self.start_battle(continuous=True)

    def _stop_continuous_battle(self, reason=None):
        self.continuous_mode = False
        self.fast_mode = False
        self.continuous_stop_btn.config(state='disabled')
        self.continuous_btn.config(state='normal')
        self.stage_combo.config(state='normal')
        self.continuous_status.config(text="")
        if self.continuous_count > 0:
            summary = f"连续作战结束！\n共完成 {self.continuous_count} 场战斗\n获得 {self.continuous_total_gacha} 基因密钥\n获得 {self.continuous_total_materials} 战斗材料"
            if reason:
                summary = f"{reason}\n\n{summary}"
            messagebox.showinfo("连续作战结果", summary)
        self.continuous_count = 0
        self.continuous_total_gacha = 0
        self.continuous_total_materials = 0

    def _continue_battle(self):
        for pos, card in list(self.team_grid.items()):
            if card not in self.game.cards or not card.is_alive:
                self._stop_continuous_battle("队伍卡牌已无效，连续作战终止")
                return
        self.start_battle(continuous=True)

    def end_battle(self):
        self.battle_is_running = False
        self.auto_battle = False
        self.start_battle_btn.config(state='normal')
        self.exit_battle_btn.config(state='disabled')
        
        winner = self.battle_system.winner
        stage_num = self.battle_system.stage_num
        
        if winner == 'player':
            _play_sound('victory')
            self.add_battle_log("=" * 50)
            self.add_battle_log("🎉 战斗胜利!")
            self.add_battle_log("=" * 50)
            self.add_battle_log(self._show_damage_stats())
            all_survived = all(p.is_alive for p in self.battle_system.player_team)
            if all_survived:
                self.game.no_loss_stages.add(stage_num)
            
            gacha_reward = 5 + stage_num // 2
            mat_reward = 2 * (5 + stage_num // 2)
            
            if self.continuous_mode:
                if all_survived:
                    self.continuous_count += 1
                    self.continuous_total_gacha += gacha_reward
                    self.continuous_total_materials += mat_reward
                    self.game.gacha_currency += gacha_reward
                    self.game.battle_materials += mat_reward
                    self.gacha_currency_label.config(text=str(self.game.gacha_currency))
                    
                    stage_data = STAGES[stage_num]
                    if 'reward' in stage_data:
                        next_stage = stage_num + 1
                        if next_stage <= 100:
                            if next_stage in STAGES and next_stage not in self.game.unlocked_stages:
                                self.game.unlocked_stages.append(next_stage)
                                self.game.max_stage = max(self.game.max_stage, next_stage)
                                self.stage_combo['values'] = self.get_available_stages()
                        if next_stage > 100 and 'infinity' not in self.game.unlocked_stages:
                            self.game.unlocked_stages.append('infinity')
                            self.stage_combo['values'] = self.get_available_stages()
                    
                    self._give_spirit_rewards()
                    
                    self.continuous_status.config(
                        text=f"连续作战: {self.continuous_count} 场 | +{self.continuous_total_gacha} 密钥 | +{self.continuous_total_materials} 材料"
                    )
                    self.game.save_game()
                    self.root.after(100, self._continue_battle)
                    return
                else:
                    self._stop_continuous_battle("卡牌阵亡，连续作战终止")
            
            if not self.continuous_mode:
                messagebox.showinfo("战斗结果", "恭喜！战斗胜利！")
            
            stage_data = STAGES[stage_num]
            if 'reward' in stage_data:
                reward = stage_data['reward']
                self.add_battle_log(f"获得奖励: {reward}")
                
                next_stage = stage_num + 1
                if next_stage <= 100:
                    if next_stage in STAGES and next_stage not in self.game.unlocked_stages:
                        self.game.unlocked_stages.append(next_stage)
                        self.game.max_stage = max(self.game.max_stage, next_stage)
                        self.stage_combo['values'] = self.get_available_stages()
                        self.add_battle_log(f"解锁新关卡: 第{next_stage}关")
                if next_stage > 100 and 'infinity' not in self.game.unlocked_stages:
                    self.game.unlocked_stages.append('infinity')
                    self.add_battle_log("解锁无限模式！")
                    self.stage_combo['values'] = self.get_available_stages()
            
            self.add_battle_log(f"获得 {gacha_reward} 基因密钥")
            self.gacha_currency_label.config(text=str(self.game.gacha_currency))
            
            self.add_battle_log(f"获得 {mat_reward} 战斗材料")
            
            self._give_spirit_rewards()
            
            self.game.save_game()
        else:
            _play_sound('defeat')
            self.add_battle_log("=" * 50)
            self.add_battle_log("💀 战斗失败...")
            self.add_battle_log("=" * 50)
            
            if self.continuous_mode:
                self._stop_continuous_battle("战斗失败，连续作战终止")
            
            for player in self.battle_system.player_team:
                if not player.is_alive:
                    original_card = next((c for c in self.game.cards if c.id == player.id), None)
                    if original_card:
                        self.game.cards.remove(original_card)
                        self.add_battle_log(f"{player.name} 战亡，已移除")
            
            all_dead = all(not p.is_alive for p in self.battle_system.player_team)
            if all_dead:
                card_m = self.game.generate_low_quality_card(gender='male')
                card_f = self.game.generate_low_quality_card(gender='female')
                self.add_battle_log(f"🔄 全体阵亡，获得一雄一雌基础卡牌")
                if card_m:
                    self.add_battle_log(f"  ♂ {card_m.name}")
                if card_f:
                    self.add_battle_log(f"  ♀ {card_f.name}")
            
            self.add_battle_log(self._show_damage_stats())
            if not self.continuous_mode:
                messagebox.showinfo("战斗结果", "战斗失败，部分卡牌战亡")
        
        # ── 任务进度: 记录击杀 ──
        if hasattr(self, 'battle_system') and self.battle_system:
            for _e in self.battle_system.enemies:
                if not _e.is_alive:
                    _ename = _e.name
                    self.game.enemy_kills[_ename] = self.game.enemy_kills.get(_ename, 0) + 1
                    if getattr(_e, 'width', 1) > 1 or getattr(_e, 'height', 1) > 1:
                        self.game.enemy_kills['__boss__'] = self.game.enemy_kills.get('__boss__', 0) + 1
        
        # ── 任务进度: 检查所有任务 ──
        _new_quests = self.game._check_all_quests()
        if _new_quests:
            _names = '\n'.join(f"✅ {q['title']}" for q in _new_quests)
            self.add_battle_log(f"\n📋 新任务完成!\n{_names}")
        
        for widget in self.battle_area.winfo_children():
            widget.destroy()
        
        self.refresh_card_list()
        self._refresh_quest_list()
    
    def add_battle_log(self, message):
        self.log_text.insert('end', message + '\n')
        self.log_text.see('end')
    
    def exit_battle(self):
        self.battle_is_running = False
        self.auto_battle = False
        
        if self.continuous_mode:
            self._stop_continuous_battle("手动退出，连续作战终止")
        
        if self.battle_system:
            for player in self.battle_system.player_team:
                if player.is_alive:
                    original_card = next((c for c in self.game.cards if c.id == player.id), None)
                    if original_card:
                        original_card.traits['health'] = player.current_health
        
        for widget in self.battle_area.winfo_children():
            widget.destroy()
        
        ttk.Label(self.battle_area, text="战斗已退出").pack()
        self.log_text.insert('end', '战斗已退出\n')
        self.start_battle_btn.config(state='normal')
        self.exit_battle_btn.config(state='disabled')
    
    def _auto_save(self):
        if not self.game.save_game():
            print("自动保存失败")
        self.root.after(30000, self._auto_save)

    def on_closing(self):
        if not self.game.save_game():
            messagebox.showerror("保存失败", "游戏数据保存失败，请检查磁盘空间或文件权限")
        self.root.destroy()
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()



if __name__ == "__main__":
    app = GeneGameGUI()
    app.run()
