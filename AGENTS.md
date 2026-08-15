# GeneCrypt Project Notes

## Key Files
- `gene_game.py` - Main game file (~3295 lines). Pure game logic (Card, Game, BattleSystem). No tkinter/PIL dependencies - Android safe.
- `legacy_gui.py` - Desktop-only tkinter GUI (GeneGameGUI). Excluded from APK build.
- `gene_enhance_config.py` - `STAT_ENHANCE_REGIONS` definitions (generated deterministically with `random.seed(42)`).
- `gene_config.py` - Gene templates, chromosome layouts, skill gene definitions.
- `trait_config.py` - Trait calculation config.
- `tech_config.py` - Tech tree structure.
- `battle_config.py` - Stage/enemy data.

## LSP/Type Errors
~75 pre-existing type-checking errors in `gene_game.py` — all unrelated to quest/genome changes.

## Quest System
- 75 quests in 3 categories: main(40), side(20), challenge(15)
- Quest IDs: `m_01`-`m_40`, `s_01`-`s_20`, `c_01`-`c_15`
- Chain locking via `requires` field referencing previous quest ID in same category
- Categories: `main`, `side`, `challenge`
- Progress types: `clear_stage`, `no_loss_clear`, `kill_any`, `kill_boss`, `submit_card`, `breed_count`, `tech_level`, `tech_level_all`, `have_cards`, `total_tech_levels`
- UI: 3-button vertical category selector on quest tab

### Main Quest Line (40 quests)
- Mix of 10 types across stages 3→200, not just `clear_stage`
- 26×`clear_stage` backbone + 14 variety quests (kill_any×3, breed_count, have_cards×2, no_loss_clear×3, tech_level, kill_boss×2, total_tech_levels, submit_card)
- Spacing: every 3-5 stages early, every 5-6 mid, every 10-20 late
- Quality progression: 0.3→0.35→0.38→0.4→0.42→0.45→0.48→0.5→0.52→0.55→0.57→0.6→0.63→0.65→0.7→0.73→0.75→0.8→0.85→0.9
- 20 card rewards (50% of quests), skills: 冻结→甘霖→快速生长→能量护盾→火焰吐息→冰霜护盾→诅咒→血之渴望→自我修复→状态共鸣→猩红风暴→炼狱之火→永冻领域→剧毒新星→万象终结→绝对零度

## Reward Cards (Fixed)
- `_create_skill_reward_card` uses `_compute_reward_traits(quality)` instead of the broken `_optimize_genome` chain
- Traits are deterministic functions of `quality` only (same quality = same stats)
- Formula:
  - Attack: `int(12 * (1+q)^9)` → q0=12, q0.3=127, q0.5=461, q0.7=1423, q0.9=3872, q0.95=4892
  - Health: `int(60 * (1+q)^6)` → q0=60, q0.3=289, q0.5=683, q0.7=1448, q0.9=2822
  - Defense: `int(5 * (1+q)^6)` → q0=5, q0.3=24, q0.5=56, q0.7=120, q0.9=235
  - Speed: `int(8 * (1+q)^5)` → q0=8, q0.3=29, q0.5=60, q0.7=113, q0.9=198
  - Stamina: `int(20 * (1+q)^5)` / Lifespan: `int(50 * (1+q)^4)`
  - Crit: `int(3 + q*15)` / Dodge: `int(2 + q*10)`
- Quality progression: early 0.3-0.4, mid 0.45-0.55, late 0.6-0.7, endgame 0.8-0.95
- `_optimize_genome` is NOT called for reward cards anymore (it only modifies padding, see Known Issues)

## Breeding Dropdown (Fixed)
- `_claim_quest_action` now calls `self.update_breeding_combos()` after `self.refresh_card_list()`
- Previously: reward cards were added to `self.game.cards` but breeding dropdown was never refreshed, making cards invisible until the next breed operation

## Testing
```bash
# Quick sanity test (quest count + deterministic reward stats)
python -c "import sys; sys.path.insert(0,'.'); import gene_config as gc, gene_enhance_config as gec, trait_config as tc, tech_config as tcc; sys.modules.update({'gene_config':gc,'gene_enhance_config':gec,'trait_config':tc,'tech_config':tcc}); from gene_game import *; g=Game(); print(f'Quests: {len(QUEST_DEFINITIONS)}'); card=g._create_skill_reward_card(['万象终结'],quality=0.8); print(f'Card ATK={card.traits[\"attack\"]} HP={card.traits[\"health\"]}')"
```

## Tech Tree Cost System (Added)
- Every tech (except `card_storage`) has per-level costs in `costs: {level → {resource: amount}}` in `tech_config.py`
- Supported resources: `battle_materials` (🧱), `gacha_currency` (🧬)
- `card_storage` keeps its dynamic `_get_card_storage_cost()` formula (no static costs entry)
- Costs are checked/deducted in `Game.upgrade_tech()` — returns error message if insufficient
- `_refresh_tech_tree_display` shows both materials and gacha in the info bar

## Tech Tree Tooltip (Added)
- Hover over any tech node shows a tooltip with: name, branch, level, description, next-level effect, material costs (with current balance), unlock requirements if locked
- Tooltip uses `tk.Toplevel` with `overrideredirect(True)` (no window chrome), auto-positioned near cursor
- Methods: `_show_tech_tooltip(event, tech_name)` / `_hide_tech_tooltip()`
- Bound via `canvas.tag_bind` `<Enter>`/`<Leave>` on `node_{tech_name}` tags in `_redraw_tech_tree`

## GitHub Actions Build (Final Successful)
- **Build #10** (b09bce6) succeeded after fixing linker error `unable to find library -lGL`
- Root cause: Kivy's `cgl_gl`/`cgl_glew` backends hardcode `-lGL` (desktop OpenGL), not available in Android NDK
- Fix: Create `libGL.so -> libGLESv2.so` symlink in NDK sysroot `usr/lib/aarch64-linux-android/21/`
- Also required: `GL/gl.h` and `GL/glext.h` compat headers pointing to GLES2 equivalents
- `__USE_OPENGL_ES2=1` is passed via CFLAGS but Kivy's `config.h` defines it to `0` — command-line `-D` flag takes precedence
- APK: `genecrypt-0.1.0-arm64-v8a-debug.apk` (~34MB), available as GitHub Actions artifact

## Content & Balance Overhaul (2026-08)
- `challenge_factors.py` — 118 challenge factors engine; hooks: apply_pre_battle /
  on_enemy_action / on_player_action / process_deaths / process_tick /
  try_spawn_next_wave. BattleSystem takes `challenge_factors` param.
  Engine exceptions caught+logged, never crash battle.
- Genome quality system: `Card.genome_quality` scored from dominant
  stat/skill/gacha genes (vital excluded, recessive inverted, chrG ×1.0).
  Homologs built independently (25% allele dominance + random stat-gene
  sequences); breeding crossover+mutation can flip dominance (35% on
  gene mutation, also writes dominant sequence).
- Skills are fully gene-determined (技能说明.md): all skill genes
  recessive — express only when BOTH alleles dominant (homozygous).
  Starters draw 2 skills from STARTER_SKILL_POOL (4 shared genes) so
  early breeding keeps skills; gacha rare activates 2 dormant genes;
  ultra injects chrG gacha gene. Passives (荆棘/暗杀者/条件反射/分裂)
  activate via B-sequence prefix on BOTH homologs; 分裂 (skill_split,
  chr3 tail) needs AA@[0:2]+CC@[6:8] on both homologs — on death splits
  into two half-stat units (no re-split).
- Gene enhancement regions (`STAT_ENHANCE_REGIONS` in
  gene_enhance_config.py): long regions (add 40-70 bases, mul 20-35 bases)
  placed in the padding AFTER genes on chr1/chr2/chr3/chrX (many chromosome
  pairs, both homologs count). Add rules = per-base flat values (positive
  + negative bases); mul rules = per-base exponential factors (e.g.
  1.04^C) applied on base+add. Strength scales with main-quest progress:
  `Card._enhance_power = 0.4 + 1.2×(main claimed/40)` (0.4 early → 1.6 at
  quest 40). Padding bases are random per card and inherited via genome
  crossover — breeding concentrates good regions.
- `calculate_traits` = `_compute_base_traits` (genome + QUALITY_EXPONENTS:
  atk 8.5 / hp 7.5 / def 4.5 / spd 4.0) + multipliers (star/modules/equip/
  sets/stat_break/genome_boost/building). Reward cards keep deterministic
  `_reward_traits_formula` via `_reward_quality` — star-up no longer
  destroys their stats.
- Difficulty: MILESTONE_BONUS smoothed (1.08-1.35); SPECIAL_SKIP_EXTRA
  includes bosses+support units (no extra_count inflation); defense floor
  = 15% raw damage; enemy healing halved; stage 99/100 boss counts cut.
- New systems: PvP bot ladder (5 tiers, rating, rewards), infinity mode
  button, base building effects, equipment set bonuses, auto-breeding,
  spirit card drops, hidden achievements, submit_card quest popup,
  tech tree UI (works), gacha API fix, battle modes (campaign/pvp/
  pvp_ladder/challenge/dungeon/infinity) isolate victory rewards.
- Local test harness (no kivy installed): headless BattleSystem sims at
  `%TEMP%\opencode\test_curve.py`, `test_factors.py`, `test_pvp.py`.

## Known Issues
- `_optimize_genome` / `_apply_genome_enhancements` still read padding —
  old padding-randomizing logic replaced by STAT_GENE_SEGMENTS
  (in-gene add/mul segments); `genome_boost` tech instead multiplies
  stats directly in `calculate_traits`.
- Desktop-only `card_creator.py` and `gene_game_PC版.py` are untracked
  dev tools (tkinter) — excluded from APK build; don't commit them.
