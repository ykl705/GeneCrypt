# GeneCrypt Project Notes

## Key Files
- `gene_game.py` - Main game file (~6901 lines). All quest system + genome optimization code.
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

## Known Issues
- `_optimize_genome` is a **complete no-op** — `STAT_ENHANCE_REGIONS` start positions (120+) are beyond all gene region ends (max 120 on chr1/chr2, 191 on chr3, 70 on chrX). Both `_optimize_genome` and `_apply_genome_enhancements` read/write only padding (random bases), never actual gene data. Not called for reward cards anymore.
- `calculate_traits` uses `sum(ord(b)) % range + min` which is effectively pseudo-random per-instance — quality has no effect on normal card stats. Bred/created cards still use this system.
- `Card.__init__` calls `calculate_traits()` internally with the built-in random sequence, producing random stats independent of quality. Reward cards now override this with `_compute_reward_traits` after construction.
- Attack values for reward cards are now strictly deterministic: same quality → same stats, monotonically increasing with quality.
