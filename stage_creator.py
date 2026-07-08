import tkinter as tk
from tkinter import ttk, messagebox
import json, os, sys, copy
sys.path.insert(0, '.')
from battle_config import STAGES, STAGE_TITLES, SKILL_EFFECTS, ENEMY_TEMPLATES

BG = "#1a1a2e"
FG = "#ffffff"
ACCENT = "#00d9ff"
FRAME_BG = "#16213e"
DISABLED_BG = "#0d1b2a"

ALL_SKILLS = sorted(SKILL_EFFECTS.keys())
TEMPLATE_NAMES = {v['name']: k for k, v in ENEMY_TEMPLATES.items()}
ENEMY_TYPE_NAMES = list(TEMPLATE_NAMES.keys())

OVERLORD_TEMPLATE_KEY = 'overlord'

def _overlord_occupied_positions(pos, grid_size=3):
    if grid_size == 4:
        valid_starts = [0, 1, 4, 5]
        start = pos if pos in valid_starts else 0
        return [start, start + 1, start + grid_size, start + grid_size + 1]
    else:
        valid_starts = [0, 1, 3, 4]
        start = pos if pos in valid_starts else 0
        return [start, start + 1, start + grid_size, start + grid_size + 1]

DATA_FILE = "stages_data.json"

def load_custom_stages():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_custom_stages(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class StageCreator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("关卡编辑器")
        self.root.geometry("1200x720")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.custom_stages = load_custom_stages()
        self.selected_pos = None
        self.grid_data = {}  # pos -> enemy dict

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background=BG, foreground=FG, font=('微软雅黑', 10))
        style.configure('TFrame', background=BG)
        style.configure('TLabelframe', background=BG, foreground=ACCENT, font=('微软雅黑', 10, 'bold'))
        style.configure('TLabelframe.Label', background=BG, foreground=ACCENT, font=('微软雅黑', 10, 'bold'))
        style.configure('TButton', font=('微软雅黑', 10), background='#0f3460', foreground=FG)
        style.configure('TCheckbutton', background=BG, foreground=FG, font=('微软雅黑', 9))

        self._build_ui()
        self._load_stage_list()

    def _build_ui(self):
        main = ttk.Frame(self.root)
        main.pack(fill='both', expand=True, padx=15, pady=10)

        # ── Top Bar ──
        top = ttk.Frame(main)
        top.pack(fill='x', pady=(0, 10))

        ttk.Label(top, text="关卡编辑器", font=('微软雅黑', 16, 'bold'), foreground=ACCENT).pack(side='left', padx=(0, 20))

        ttk.Label(top, text="选择关卡:").pack(side='left')
        self.stage_combo = ttk.Combobox(top, width=12, font=('微软雅黑', 10), state='readonly')
        self.stage_combo.pack(side='left', padx=5)
        self.stage_combo.bind('<<ComboboxSelected>>', self._on_stage_select)

        ttk.Label(top, text="关卡名称:").pack(side='left', padx=(15, 0))
        self.name_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.name_var, font=('微软雅黑', 10), width=30).pack(side='left', padx=5)

        ttk.Label(top, text="网格:").pack(side='left', padx=(10, 0))
        self.grid_size_var = tk.IntVar(value=3)
        self.grid_size_combo = ttk.Combobox(top, values=['3×3', '4×4'], width=6, state='readonly')
        self.grid_size_combo.current(0)
        self.grid_size_combo.pack(side='left', padx=2)
        self.grid_size_combo.bind('<<ComboboxSelected>>', self._on_grid_size_change)

        ttk.Button(top, text="新建关卡", command=self._new_stage).pack(side='left', padx=10)
        ttk.Button(top, text="删除关卡", command=self._delete_stage).pack(side='left', padx=2)

        # ── Body: Grid (left) + Editor (right) ──
        body = ttk.Frame(main)
        body.pack(fill='both', expand=True)

        # ── Left: Grid ──
        left_panel = ttk.LabelFrame(body, text="敌方格位布局 (点击格子选择)", padding=10)
        left_panel.pack(side='left', fill='y', padx=(0, 10))

        self.grid_buttons = {}
        self._grid_frame = tk.Frame(left_panel, bg=FRAME_BG)
        self._grid_frame.pack()

        ctl_frame = ttk.Frame(left_panel)
        ctl_frame.pack(fill='x', pady=8)
        ttk.Button(ctl_frame, text="清空当前格子", command=self._clear_selected_pos).pack(side='left', padx=5)
        ttk.Button(ctl_frame, text="清空所有敌人", command=self._clear_all).pack(side='left', padx=5)

        self._rebuild_grid_buttons()

        # ── Right: Enemy Editor ──
        right_panel = ttk.LabelFrame(body, text="敌人编辑器", padding=15)
        right_panel.pack(side='left', fill='both', expand=True)

        # Basic info
        info_f = ttk.Frame(right_panel)
        info_f.pack(fill='x', pady=3)
        ttk.Label(info_f, text="当前位置:").pack(side='left')
        self.pos_label = ttk.Label(info_f, text="未选择", foreground='#aaa')
        self.pos_label.pack(side='left', padx=5)

        ttk.Label(info_f, text="敌人名称:").pack(side='left', padx=(10, 0))
        self.enemy_name_var = tk.StringVar()
        ttk.Entry(info_f, textvariable=self.enemy_name_var, width=18, font=('微软雅黑', 10)).pack(side='left', padx=5)

        ttk.Label(info_f, text="类型模板:").pack(side='left', padx=(10, 0))
        self.type_combo = ttk.Combobox(info_f, values=ENEMY_TYPE_NAMES, width=10, state='readonly')
        self.type_combo.pack(side='left', padx=5)
        self.type_combo.bind('<<ComboboxSelected>>', self._apply_template)

        # Stats
        stat_f = ttk.LabelFrame(right_panel, text="属性", padding=10)
        stat_f.pack(fill='x', pady=6)

        self.stat_vars = {}
        for i, (label, key, default) in enumerate([
            ("生 命:", 'health', 100), ("攻 击:", 'attack', 20),
            ("防 御:", 'defense', 10), ("速 度:", 'speed', 15),
        ]):
            sf = ttk.Frame(stat_f)
            sf.grid(row=i // 2, column=i % 2, sticky='ew', padx=8, pady=3)
            ttk.Label(sf, text=label, width=6).pack(side='left')
            var = tk.IntVar(value=default)
            self.stat_vars[key] = var
            tk.Scale(sf, from_=0, to=2000, orient='horizontal', variable=var, length=200,
                     bg=FRAME_BG, fg=FG, troughcolor='#0f3460', highlightbackground=BG,
                     command=lambda v, k=key: self._update_stat_label(k)).pack(side='left', padx=5)
            lbl = ttk.Label(sf, text=str(default), width=5)
            lbl.pack(side='left')
            self.stat_vars[f'{key}_lbl'] = lbl

        # Skills
        skill_f = ttk.LabelFrame(right_panel, text="技能", padding=8)
        skill_f.pack(fill='x', pady=6)

        self.skill_vars = {}
        skill_canvas = tk.Canvas(skill_f, bg=FRAME_BG, highlightthickness=0, height=110)
        skill_sb = ttk.Scrollbar(skill_f, orient='vertical', command=skill_canvas.yview)
        skill_inner = ttk.Frame(skill_canvas)
        skill_inner.bind('<Configure>', lambda e: skill_canvas.configure(scrollregion=skill_canvas.bbox('all')))
        skill_canvas.create_window((0, 0), window=skill_inner, anchor='nw')
        skill_canvas.configure(yscrollcommand=skill_sb.set)

        for idx, sk in enumerate(ALL_SKILLS):
            var = tk.BooleanVar(value=False)
            self.skill_vars[sk] = var
            r, c = idx // 4, idx % 4
            ttk.Checkbutton(skill_inner, text=sk, variable=var).grid(row=r, column=c, sticky='w', padx=4, pady=1)

        skill_canvas.pack(side='left', fill='both', expand=True)
        skill_sb.pack(side='right', fill='y')

        # Action buttons
        action_f = ttk.Frame(right_panel)
        action_f.pack(fill='x', pady=10)
        tk.Button(action_f, text="应用到格子", command=self._apply_to_grid,
                  bg='#00d9ff', fg='#1a1a2e', font=('微软雅黑', 11, 'bold'), padx=20, pady=4).pack(side='left', padx=5)
        ttk.Button(action_f, text="重置编辑器", command=self._reset_editor).pack(side='left', padx=5)

        # ── Bottom: Stage Settings ──
        btm = ttk.LabelFrame(main, text="关卡奖励设置", padding=8)
        btm.pack(fill='x', pady=(8, 0))

        bw = ttk.Frame(btm)
        bw.pack(fill='x')

        ttk.Label(bw, text="解锁下一关:").pack(side='left')
        self.unlock_var = tk.IntVar(value=1)
        ttk.Entry(bw, textvariable=self.unlock_var, width=5, font=('微软雅黑', 10)).pack(side='left', padx=5)

        ttk.Label(bw, text="额外经验:").pack(side='left', padx=(15, 0))
        self.exp_var = tk.StringVar(value="")
        ttk.Entry(bw, textvariable=self.exp_var, width=8, font=('微软雅黑', 10)).pack(side='left', padx=5)

        self.gene_frag_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(bw, text="基因碎片奖励", variable=self.gene_frag_var).pack(side='left', padx=15)

        # ── Save ──
        save_f = ttk.Frame(main)
        save_f.pack(fill='x', pady=8)

        tk.Button(save_f, text="保存关卡", command=self._save_stage,
                  bg='#00d9ff', fg='#1a1a2e', font=('微软雅黑', 12, 'bold'), padx=40, pady=6).pack(side='left', padx=5)
        ttk.Button(save_f, text="导入现有关卡", command=self._import_stage).pack(side='left', padx=5)
        ttk.Button(save_f, text="预览关卡", command=self._preview_stage).pack(side='left', padx=5)
        ttk.Label(save_f, text=f"  数据文件: {DATA_FILE}", foreground='#666', font=('微软雅黑', 8)).pack(side='left', padx=10)

    def _update_stat_label(self, key):
        var = self.stat_vars[key]
        self.stat_vars[f'{key}_lbl'].configure(text=str(var.get()))

    def _load_stage_list(self):
        all_stages = []
        for num in sorted(self.custom_stages.keys(), key=int):
            s = self.custom_stages[num]
            all_stages.append(f"第{num}关 - {s.get('name', s.get('name',''))}")
        self.stage_combo['values'] = all_stages
        if all_stages:
            self.stage_combo.current(0)
            self._on_stage_select()

    def _new_stage(self):
        nums = [int(k) for k in self.custom_stages.keys()]
        next_num = max(nums) + 1 if nums else 31
        key = str(next_num)
        self.custom_stages[key] = {
            'name': f'第{key}关 - 新关卡',
            'enemies': [],
            'reward': {'unlock_stage': next_num + 1, 'extra_exp': None, 'gene_fragment': False},
        }
        self._load_stage_list()
        idx = len(self.stage_combo['values']) - 1
        self.stage_combo.current(idx)
        self._on_stage_select()
        self._clear_all()

    def _delete_stage(self):
        sel = self.stage_combo.current()
        if sel < 0:
            return
        vals = self.stage_combo['values']
        key = self._current_stage_key()
        if not key:
            return
        ok = messagebox.askyesno("确认删除", f"确定删除第{key}关？")
        if not ok:
            return
        del self.custom_stages[key]
        save_custom_stages(self.custom_stages)
        self._load_stage_list()

    def _current_stage_key(self):
        sel = self.stage_combo.current()
        if sel < 0:
            return None
        txt = self.stage_combo.get()
        if not txt:
            return None
        num = txt.split('关')[0].replace('第', '').strip()
        return num

    def _get_grid_size(self):
        sel = self.grid_size_combo.get()
        return 4 if '4' in sel else 3

    def _rebuild_grid_buttons(self):
        for w in self._grid_frame.winfo_children():
            w.destroy()
        self.grid_buttons.clear()
        gs = self._get_grid_size()
        n = gs * gs
        btn_w = 10 if gs == 4 else 14
        btn_h = 3 if gs == 4 else 4
        for pos in range(n):
            row, col = pos // gs, pos % gs
            btn = tk.Button(self._grid_frame, text="— 空 —", width=btn_w, height=btn_h,
                           bg='#0f3460', fg='#555', font=('微软雅黑', 9),
                           relief='raised', bd=3,
                           command=lambda p=pos: self._select_grid_pos(p))
            btn.grid(row=row, column=col, padx=4, pady=4)
            self.grid_buttons[pos] = btn

    def _on_grid_size_change(self, event=None):
        self._rebuild_grid_buttons()
        self._clear_all()

    def _on_stage_select(self, event=None):
        key = self._current_stage_key()
        if not key:
            return
        stage = self.custom_stages.get(key)
        if not stage:
            return
        stage_num = int(key)
        auto_gs = 4 if stage_num > 60 else 3
        gs_str = '4×4' if auto_gs == 4 else '3×3'
        if self.grid_size_combo.get() != gs_str:
            self.grid_size_combo.set(gs_str)
            self._rebuild_grid_buttons()
        self.name_var.set(stage.get('name', ''))
        reward = stage.get('reward', {})
        self.unlock_var.set(reward.get('unlock_stage', int(key) + 1))
        exp = reward.get('extra_exp')
        self.exp_var.set(str(exp) if exp else '')
        self.gene_frag_var.set(bool(reward.get('gene_fragment', False)))

        self._clear_all()
        gs = self._get_grid_size()
        _max_pos = gs * gs
        for i, e in enumerate(stage.get('enemies', [])):
            pos = e.get('position')
            if pos is None:
                pos = i if i < _max_pos else i
            is_ol = e.get('is_overlord', False)
            if is_ol:
                occ = _overlord_occupied_positions(pos, gs)
                for p in occ:
                    self.grid_data[p] = dict(e)
                    self.grid_data[p]['position'] = p
                    self._update_grid_button(p)
            else:
                self.grid_data[pos] = dict(e)
                self.grid_data[pos]['position'] = pos
                self._update_grid_button(pos)

        self.selected_pos = None
        self.pos_label.configure(text="未选择")
        self._reset_editor()

    def _select_grid_pos(self, pos):
        self.selected_pos = pos
        gs = self._get_grid_size()
        self.pos_label.configure(text=f"第{pos+1}格 (行{pos//gs+1},列{pos%gs+1})")

        if pos in self.grid_data:
            e = self.grid_data[pos]
            self.enemy_name_var.set(e.get('name', ''))
            for k in ['health', 'attack', 'defense', 'speed']:
                self.stat_vars[k].set(e.get(k, 100))
                self._update_stat_label(k)
            for sk in ALL_SKILLS:
                self.skill_vars[sk].set(sk in e.get('skills', []))
            tname = e.get('template', '')
            self.type_combo.set(tname)
        else:
            self._reset_editor()

    def _apply_template(self, event=None):
        tname = self.type_combo.get()
        if not tname:
            return
        ekey = TEMPLATE_NAMES.get(tname)
        if not ekey:
            return
        tmpl = ENEMY_TEMPLATES[ekey]
        self.enemy_name_var.set(tmpl['name'])
        # Apply base values; adjust for stage later if needed
        if self.selected_pos is None or self.selected_pos not in self.grid_data:
            self.stat_vars['health'].set(tmpl['base_health'])
            self.stat_vars['attack'].set(tmpl['base_attack'])
            self.stat_vars['defense'].set(tmpl['base_defense'])
            self.stat_vars['speed'].set(tmpl['base_speed'])
            for k in ['health', 'attack', 'defense', 'speed']:
                self._update_stat_label(k)

    def _reset_editor(self):
        self.enemy_name_var.set('')
        self.type_combo.set('')
        for k in ['health', 'attack', 'defense', 'speed']:
            self.stat_vars[k].set(100)
            self._update_stat_label(k)
        for sk in ALL_SKILLS:
            self.skill_vars[sk].set(False)

    def _apply_to_grid(self):
        if self.selected_pos is None:
            messagebox.showwarning("警告", "请先点击左侧格子选择位置")
            return
        name = self.enemy_name_var.get().strip()
        if not name:
            messagebox.showwarning("警告", "请输入敌人名称")
            return

        skills = [sk for sk in ALL_SKILLS if self.skill_vars[sk].get()]
        tname = self.type_combo.get()
        is_overlord = (tname == '首领实验体（增强版）')

        enemy = {
            'name': name,
            'health': self.stat_vars['health'].get(),
            'attack': self.stat_vars['attack'].get(),
            'defense': self.stat_vars['defense'].get(),
            'speed': self.stat_vars['speed'].get(),
            'skills': skills,
            'position': self.selected_pos,
            'is_overlord': is_overlord,
            'reward_exp': 50,
        }
        if tname:
            enemy['template'] = tname
            ekey = TEMPLATE_NAMES.get(tname)
            if ekey:
                tmpl = ENEMY_TEMPLATES[ekey]
                if 'purify_interval' in tmpl:
                    enemy['purify_interval'] = tmpl['purify_interval']
                if 'annihilate' in tmpl:
                    enemy['annihilate'] = tmpl['annihilate']

        if is_overlord:
            gs = self._get_grid_size()
            occ = _overlord_occupied_positions(self.selected_pos, gs)
            for p in occ:
                self.grid_data[p] = dict(enemy)
                self.grid_data[p]['position'] = p
                self._update_grid_button(p)
        else:
            self.grid_data[self.selected_pos] = enemy
            self._update_grid_button(self.selected_pos)

    def _update_grid_button(self, pos):
        btn = self.grid_buttons[pos]
        if pos in self.grid_data:
            e = self.grid_data[pos]
            is_overlord = e.get('is_overlord', False)
            if is_overlord:
                gs = self._get_grid_size()
                occ = _overlord_occupied_positions(e.get('position', pos), gs)
                is_primary = (pos == occ[0])
                if is_primary:
                    btn.configure(
                        text=f"【霸】{e['name']}\nHP:{e['health']} ATK:{e['attack']}\n{e.get('speed',0)} SPD | 2x2",
                        bg='#2d004d', fg='#ff0000', font=('微软雅黑', 7, 'bold'),
                    )
                else:
                    btn.configure(text="▣ 2x2占位", bg='#2d004d', fg='#aa0000', font=('微软雅黑', 7))
            else:
                color = '#2d1b4e' if e.get('template') == '首领实验体' else '#1e3a5f'
                fg_color = '#ff6b6b' if e.get('template') == '首领实验体' else ACCENT
                skills_str = ', '.join(e.get('skills', [])[:2])
                if len(e.get('skills', [])) > 2:
                    skills_str += '...'
                btn.configure(
                    text=f"{e['name']}\nHP:{e['health']} ATK:{e['attack']}\n{e.get('speed',0)} SPD | {skills_str or '无技能'}",
                    bg=color, fg=fg_color, font=('微软雅黑', 7),
                )
        else:
            btn.configure(text="— 空 —", bg='#0f3460', fg='#555', font=('微软雅黑', 9))

    def _clear_selected_pos(self):
        if self.selected_pos is not None and self.selected_pos in self.grid_data:
            e = self.grid_data[self.selected_pos]
            if e.get('is_overlord'):
                gs = self._get_grid_size()
                occ = _overlord_occupied_positions(self.selected_pos, gs)
                for p in occ:
                    if p in self.grid_data:
                        del self.grid_data[p]
                        self._update_grid_button(p)
            else:
                del self.grid_data[self.selected_pos]
                self._update_grid_button(self.selected_pos)
            self._reset_editor()

    def _clear_all(self):
        self.grid_data.clear()
        gs = self._get_grid_size()
        for pos in range(gs * gs):
            self._update_grid_button(pos)
        self.selected_pos = None
        self.pos_label.configure(text="未选择")

    def _preview_stage(self):
        key = self._current_stage_key()
        if not key:
            return
        enemies = [self.grid_data[p] for p in sorted(self.grid_data.keys()) if p in self.grid_data]
        if not enemies:
            messagebox.showinfo("预览", "该关卡没有敌人")
            return
        lines = [f"关卡: 第{key}关 - {self.name_var.get()}", f"敌人数: {len(enemies)}", '-' * 40]
        for e in enemies:
            skills = ', '.join(e.get('skills', [])) or '无'
            lines.append(f"[{e.get('position',0)+1}] {e['name']}: HP={e['health']} ATK={e['attack']} DEF={e['defense']} SPD={e['speed']}")
            lines.append(f"     技能: {skills}")
        messagebox.showinfo("关卡预览", '\n'.join(lines))

    def _save_stage(self):
        key = self._current_stage_key()
        if not key:
            messagebox.showwarning("警告", "没有选择的关卡")
            return
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("警告", "请输入关卡名称")
            return

        enemies = [self.grid_data[p] for p in sorted(self.grid_data.keys()) if p in self.grid_data]
        if not enemies:
            ok = messagebox.askyesno("确认", "关卡没有敌人，确定保存？")
            if not ok:
                return

        reward = {
            'unlock_stage': self.unlock_var.get(),
        }
        exp_str = self.exp_var.get().strip()
        if exp_str:
            try:
                reward['extra_exp'] = int(exp_str)
            except ValueError:
                messagebox.showwarning("警告", "额外经验必须是整数")
                return
        else:
            reward['extra_exp'] = None
        reward['gene_fragment'] = self.gene_frag_var.get()

        self.custom_stages[key] = {
            'name': name,
            'enemies': enemies,
            'reward': reward,
        }
        save_custom_stages(self.custom_stages)

        # Update the combo display
        vals = list(self.stage_combo['values'])
        idx = self.stage_combo.current()
        if 0 <= idx < len(vals):
            vals[idx] = f"第{key}关 - {name[:20]}"
            self.stage_combo['values'] = vals

        messagebox.showinfo("保存成功", f"第{key}关「{name}」已保存到 {DATA_FILE}")

    def _import_stage(self):
        d = {}
        for num, stage in STAGES.items():
            d[str(num)] = stage
        for num in sorted(d.keys(), key=int):
            s = d[num]
            s['_stage_num'] = num
            if num not in self.custom_stages:
                self.custom_stages[num] = {
                    'name': s.get('name', ''),
                    'enemies': s.get('enemies', []),
                    'reward': s.get('reward', {}),
                }
        save_custom_stages(self.custom_stages)
        self._load_stage_list()
        messagebox.showinfo("导入完成", f"已导入 {len(d)} 个现有关卡")

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    StageCreator().run()
