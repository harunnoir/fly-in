# ── Fix existing task ──
task modify 3 project:1337.fly-in.parsing

# ── Parser ──
task add project:1337.fly-in.parsing \
  "Implement parse() core loop — read file, dispatch line types"
task add project:1337.fly-in.parsing \
  "Parse zone definitions (start_hub, end_hub, hub) with metadata [zone= color= max_drones=]"
task add project:1337.fly-in.parsing \
  "Parse connection definitions with metadata [max_link_capacity=]"
task add project:1337.fly-in.parsing \
  "Wire up error handling — raise ParsingError subclasses per invalid input"
task add project:1337.fly-in.parsing \
  "Test parser against all 11 map files"

# ── Pathfinding ──
task add project:1337.fly-in.pathfinding \
  "Implement shortest-path algorithm (BFS/Dijkstra with zone-type costs: normal=1, restricted=2, priority=1)"
task add project:1337.fly-in.pathfinding \
  "Multi-drone path distribution — split drones across disjoint/overlapping paths"
task add project:1337.fly-in.pathfinding \
  "Strategic waiting logic — turn scheduling to avoid path conflicts"

# ── Simulation ──
task add project:1337.fly-in.simulation \
  "Implement turn-based simulation engine (drone states, turn resolution)"
task add project:1337.fly-in.simulation \
  "Zone occupancy — enforce max_drones per zone (start/end are exceptions)"
task add project:1337.fly-in.simulation \
  "Connection capacity — enforce max_link_capacity per connection per turn"
task add project:1337.fly-in.simulation \
  "Restricted-zone movement — 2-turn transit, forced arrival at destination"
task add project:1337.fly-in.simulation \
  "Simultaneous move resolution — free departing capacity before placing arrivals"
task add project:1337.fly-in.simulation \
  "Deadlock detection and resolution"

# ── CLI & Main ──
task add project:1337.fly-in.cli \
  "Build main.py — read from stdin, orchestrate parse -> simulate -> output"
task add project:1337.fly-in.cli \
  "Implement output formatter — D1-zone D2-zone per turn"
task add project:1337.fly-in.cli \
  "Optional: --visual / --graphical CLI flags"

# ── Visual ──
task add project:1337.fly-in.visual \
  "Colored terminal output with colorama — show zones, drones, types"
task add project:1337.fly-in.visual \
  "Animated turn-by-turn display (re-render each turn)"

# ── Docs ──
task add project:1337.fly-in.docs \
  "Full README.md — attribution, Description, Instructions, Resources, algorithm strategy, visual features"

# ── Quality ──
task add project:1337.fly-in.quality \
  "Write pytest unit tests (parser, pathfinding, simulation edge cases)"
task add project:1337.fly-in.quality \
  "Validate against all map benchmarks (easy <=10, medium <=30, hard <=60)"
task add project:1337.fly-in.quality \
  "Final flake8 + mypy cleanup"
