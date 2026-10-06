#!/usr/bin/env python3
"""spellingbee -- 拼字蜜蜂（Spelling Bee）单词游戏。

玩法：给出 7 个字母（其中 1 个是中心必用字母），拼出尽可能多的
不少于 4 个字母的单词。每个单词必须：
  1. 至少 4 个字母；
  2. 只使用给出的 7 个字母（可重复使用）；
  3. 必须包含中心字母；
  4. 必须在内置词表里。

计分：4 字母词 1 分；5 字母及以上按字母数计分；
      用遍全部 7 个字母的 pangram（全字母词）额外 +7 分。
段位按"已得分数占本局满分百分比"划分。

仅标准库：argparse / sys / random / secrets。
"""

from __future__ import annotations

import argparse
import random
import secrets
import sys

# 内置词表：约 300 个常用单词，全部小写、仅字母、4 字母及以上
WORDS = tuple(sorted({
    "able", "about", "above", "accept", "accord", "across", "action", "actor",
    "added", "admit", "adopt", "after", "again", "agent", "agile", "agree",
    "ahead", "alarm", "album", "alert", "alike", "alive", "allow", "alone",
    "along", "aloud", "angel", "anger", "angle", "ankle", "apple", "apply",
    "arena", "argue", "arise", "armor", "aroma", "arose", "around", "array",
    "arrow", "aside", "avoid", "awake", "award", "bacon", "badge", "baker",
    "balcony", "ballet", "balloon", "banana", "band", "banner", "barrel",
    "base", "basic", "basil", "basin", "basis", "batch", "beacon", "beard",
    "beast", "become", "before", "began", "begin", "behind", "being",
    "believe", "below", "berry", "beside", "better", "beyond", "bigger",
    "bison", "blade", "blank", "blast", "blaze", "blend", "bless", "blind",
    "blink", "block", "blossom", "blush", "board", "boast", "bolder",
    "borrow", "bottle", "bounce", "bound", "bracket", "brain", "brake",
    "branch", "brand", "brass", "brave", "bread", "break", "breeze",
    "brick", "bride", "bridge", "brief", "brighter", "brisk", "bronze",
    "brook", "broom", "brought", "brown", "brush", "bucket", "budget",
    "build", "bundle", "burst", "cabin", "cable", "cache", "camel",
    "camera", "camp", "cancel", "candle", "canyon", "canvas", "carbon",
    "cargo", "carpet", "carrot", "carve", "castle", "catch", "cater",
    "cause", "ceiling", "celebrate", "cellar", "cereal", "chain", "chair",
    "chalk", "charm", "chart", "chase", "cheap", "cheer", "cheese",
    "cherry", "chess", "chicken", "chief", "child", "chime", "choice",
    "choose", "chord", "chorus", "chrome", "chunk", "cinema", "circle",
    "circus", "civil", "claim", "clamp", "clarity", "clash", "clasp",
    "class", "clean", "clear", "clerk", "click", "cliff", "climb",
    "clover", "coach", "coarse", "coast", "cobalt", "cocoa", "coffee",
    "coin", "cold", "collar", "colony", "color", "comet", "comfort",
    "comic", "command", "comment", "common", "compass", "concert",
    "condor", "cookie", "cooler", "copper", "coral", "corner", "cotton",
    "couch", "could", "count", "court", "cousin", "cover", "crack",
    "craft", "crane", "crash", "crawl", "crazy", "cream", "create",
    "creek", "crest", "cricket", "crimson", "crisp", "crochet", "cross",
    "crowd", "crown", "crunch", "crush", "crystal", "curious", "curtain",
    "curve", "cycle", "daily", "dance", "danger", "daring", "darker",
    "dazzle", "decent", "decide", "deck", "decode", "decor", "deeper",
    "defeat", "degree", "delay", "delicate", "delight", "delta",
    "demand", "denser", "desert", "design", "desk", "dessert", "detail",
    "devote", "diamond", "diary", "differ", "dinner", "direct",
    "disease", "display", "divert", "doctor", "document", "dodge",
    "donate", "donkey", "doodle", "double", "doubt", "dough",
    "dragon", "drain", "drama", "dream", "dress", "drift", "drill",
    "drink", "driven", "driver", "drone", "droplet", "drown", "drummer",
    "dryer", "dungeon", "durian", "dusty", "eager", "eagle", "early",
    "earth", "easel", "eaten", "echo", "eclipse", "edge", "editor",
    "elder", "elect", "elegant", "element", "eleven", "elixir", "email",
    "ember", "embrace", "emerge", "empire", "enable", "enamel", "enchant",
    "encore", "engine", "enjoy", "enlarge", "enough", "enter", "entire",
    "entry", "envelope", "envoy", "equal", "erase", "error", "escape",
    "essay", "estate", "ethics", "even", "evening", "event", "every",
    "exact", "examine", "example", "exceed", "except", "excess",
    "excited", "exclude", "excuse", "exhibit", "exist", "expand",
    "expect", "expense", "expert", "export", "extra", "fabric",
    "facade", "factor", "failed", "faint", "fair", "faith", "falcon",
    "fallen", "false", "famous", "fancy", "farmer", "faster", "father",
    "faucet", "favor", "fear", "feast", "feather", "fellow", "fence",
    "fever", "fiber", "field", "fierce", "fifteen", "fight", "figure",
    "filter", "final", "finger", "finish", "first", "fiscal", "flame",
    "flash", "flavor", "fleece", "fleet", "flesh", "flight", "float",
    "flock", "flood", "floor", "floral", "flour", "fluent", "flute",
    "flutter", "focus", "folder", "follow", "forest", "forget", "forge",
    "formal", "format", "former", "fortune", "forum", "forward", "found",
    "fountain", "frame", "frank", "freedom", "fresh", "friction",
    "friday", "friend", "frost", "frozen", "fruit", "fumble", "fungus",
    "funnel", "further", "future", "gadget", "galaxy", "gallery",
    "gallon", "gamble", "garden", "garlic", "gather", "gauge", "gaze",
    "geese", "general", "genius", "gentle", "ghost", "giant", "giggle",
    "ginger", "glacier", "glance", "glare", "glass", "gleam", "glide",
    "glimpse", "globe", "gloom", "glory", "glove", "glower", "gnome",
    "golden", "goose", "gorgeous", "gossip", "govern", "grace", "grade",
    "grain", "grand", "grant", "grape", "graph", "grasp", "grass",
    "grateful", "gravel", "gravity", "gravy", "graze", "greater",
    "green", "greet", "grief", "grill", "grinder", "grocer", "groove",
    "ground", "group", "grove", "growl", "growth", "guard", "guess",
    "guest", "guide", "guild", "guitar", "habit", "harbor", "harder",
    "harmony", "harvest", "hasten", "hatch", "haven", "hazel", "health",
    "heard", "heart", "heater", "heaven", "heavier", "hedge", "height",
    "hello", "helmet", "helper", "herald", "herb", "herd", "hero",
    "hidden", "hiking", "hinder", "hinge", "hippo", "hobby", "hockey",
    "holder", "holiday", "hollow", "honey", "honor", "hooked", "horror",
    "horse", "hotel", "hound", "house", "hover", "humble", "humor",
    "hundred", "hunger", "hunter", "hurdle", "hurricane", "hurry",
    "icicle", "ideal", "ignite", "ignore", "image", "imagine", "impact",
    "import", "improve", "index", "indigo", "indoor", "infant",
    "infect", "infer", "infinite", "inform", "inhale", "inland",
    "inner", "input", "insect", "insert", "inside", "insist", "install",
    "instant", "instead", "intense", "interest", "invent", "invest",
    "invite", "ivory", "jacket", "jaguar", "jargon", "jasmine",
    "jelly", "jewel", "jingle", "join", "joker", "jolly", "journal",
    "journey", "judge", "juice", "jumbo", "jungle", "junior", "karma",
    "kayak", "kebab", "keeper", "kennel", "kernel", "kettle", "keyboard",
    "khaki", "kicker", "kind", "kiosk", "kitchen", "kitten", "knight",
    "knit", "knock", "knot", "known", "label", "labor", "ladder",
    "lantern", "laptop", "larger", "laser", "later", "lather", "laugh",
    "launch", "laurel", "lavish", "layer", "leader", "leaf", "league",
    "learn", "lease", "least", "leather", "leave", "ledge", "legacy",
    "legal", "legend", "lemon", "lender", "length", "lesson", "letter",
    "level", "lever", "light", "lilac", "limit", "linen", "linger",
    "liquid", "listen", "little", "lively", "liver", "lizard", "llama",
    "loader", "local", "locate", "locker", "lodge", "logic", "lonely",
    "look", "loom", "loose", "lorry", "loser", "lotion", "loud",
    "lounge", "lover", "lower", "loyal", "lucky", "luggage", "lumber",
    "lunar", "lunch", "lyric", "magenta", "magic", "magnet", "magnify",
    "maiden", "major", "maker", "mango", "manner", "manor", "maple",
    "marble", "margin", "marina", "market", "marry", "marsh", "marvel",
    "mascot", "mason", "match", "matter", "mature", "mayor", "meadow",
    "meager", "meal", "meaning", "meant", "measure", "meat", "mechanic",
    "medal", "media", "medley", "melody", "mellow", "melon", "melt",
    "member", "memory", "mental", "mentor", "merchant", "mercy",
    "merely", "merge", "merit", "mermaid", "merry", "message", "metal",
    "meteor", "method", "meter", "midnight", "mighty", "migrate",
    "mild", "miller", "mineral", "mingle", "minor", "minute", "mirror",
    "mirth", "misery", "missile", "mistake", "mitten", "mixed",
    "mobile", "model", "moderate", "modern", "modest", "modify",
    "module", "moment", "money", "monitor", "monkey", "monster",
    "month", "monument", "moral", "morale", "morning", "morsel",
    "mortal", "mosaic", "mossy", "motel", "mother", "motion", "motive",
    "motor", "motto", "mound", "mountain", "mouse", "mouth", "mover",
    "movie", "muffin", "mullet", "murmur", "muscle", "museum", "mushroom",
    "music", "mustard", "mutter", "mutual", "mystery", "naive",
    "napkin", "narrow", "nasal", "nasty", "nation", "native", "nature",
    "nautical", "nearby", "nearer", "neat", "nebula", "needle",
    "negotiate", "neighbor", "neon", "nephew", "nervous", "nestle",
    "never", "newer", "newly", "niche", "nickel", "niece", "night",
    "nimble", "noble", "noise", "nomad", "noodle", "normal", "north",
    "notable", "note", "notice", "notify", "notion", "novel",
    "novice", "nowhere", "nugget", "number", "nurse", "nurture",
    "nutrient", "nylon", "oasis", "obey", "object", "oblige", "obscure",
    "observe", "obtain", "obvious", "ocean", "octave", "october",
    "office", "officer", "olive", "omelet", "onion", "online",
    "onward", "oops", "open", "opera", "opinion", "oppose", "option",
    "oracle", "orange", "orbit", "orchard", "orchestra", "order",
    "organ", "orient", "origin", "ornament", "ostrich", "other",
    "otter", "ought", "ounce", "outer", "outlet", "outline", "output",
    "oval", "oven", "overcome", "overtake", "owl", "owner", "oxygen",
    "oyster", "ozone", "paddle", "pager", "paint", "palace", "pallet",
    "panel", "panic", "pansy", "paper", "parade", "parcel", "pardon",
    "parent", "parish", "parka", "parlor", "parrot", "parsley",
    "parsnip", "partly", "pastel", "pasture", "patch", "patent",
    "path", "patrol", "patron", "pattern", "pavement", "peace",
    "peach", "peacock", "peanut", "pearl", "pebble", "pecan",
    "pedal", "penalty", "pencil", "pendant", "penguin", "pennant",
    "pepper", "perceive", "perch", "perfect", "perform", "perfume",
    "perhaps", "peril", "period", "permit", "person", "persuade",
    "petal", "petite", "phase", "phone", "photo", "phrase", "physics",
    "piano", "pick", "pickle", "picnic", "picture", "piece", "pierce",
    "pigeon", "pigment", "pilot", "pincers", "pioneer", "pious",
    "pirate", "pistol", "pitch", "pizza", "place", "plague", "plaid",
    "plain", "planet", "plank", "planner", "plant", "plasma",
    "plaster", "plastic", "plate", "plateau", "platform", "plaza",
    "pleasant", "pleasure", "pledge", "plenty", "plight", "plumber",
    "plume", "plunge", "plural", "pocket", "poetry", "point",
    "poison", "polar", "polish", "polite", "poll", "ponder", "pony",
    "poodle", "popcorn", "poplar", "popular", "porcelain", "porch",
    "pork", "portable", "portal", "portrait", "possum", "postage",
    "poster", "potato", "potent", "pouch", "poultry", "pound",
    "pour", "poverty", "powder", "power", "praise", "prance",
    "prank", "prayer", "preach", "precede", "precise", "predict",
    "prefer", "prefix", "prelude", "prepare", "present", "preserve",
    "press", "pretty", "price", "pride", "priest", "primer", "prince",
    "print", "prism", "prison", "privet", "prize", "probe", "problem",
    "proceed", "proclaim", "produce", "profit", "program", "project",
    "promise", "promote", "prompt", "proof", "proper", "prophet",
    "propose", "prose", "protect", "proud", "prove", "proverb",
    "provide", "prowess", "prune", "public", "puddle", "puffin",
    "pulley", "pulpit", "pulse", "pumpkin", "punch", "punctual",
    "pupil", "puppet", "puppy", "purchase", "pure", "purify",
    "purple", "purpose", "pursue", "puzzle", "quaint", "quaker",
    "qualify", "quality", "quarrel", "quart", "quartz", "queen",
    "query", "quest", "queue", "quicken", "quiet", "quilt", "quince",
    "quirky", "quite", "quiver", "quota", "quote", "rabbit", "racer",
    "radar", "radiant", "radio", "radish", "raffle", "raft", "ragged",
    "railing", "rainbow", "raise", "rally", "ramen", "ranch",
    "ranger", "rapid", "rare", "rascal", "raspberry", "rattle",
    "raven", "ravine", "react", "reader", "ready", "realm", "reason",
    "rebel", "rebirth", "rebound", "recall", "receipt", "receive",
    "recipe", "reckon", "record", "recruit", "rectify", "recycle",
    "redeem", "referee", "refer", "refill", "refine", "reflect",
    "reform", "refrain", "refresh", "refuge", "refund", "regal",
    "regard", "regent", "region", "register", "regret", "regular",
    "rehearse", "reign", "relate", "relax", "relay", "release",
    "relent", "relevant", "relic", "relief", "relieve", "relish",
    "remedy", "remember", "remind", "remote", "remove", "render",
    "renew", "renown", "rental", "repaint", "repair", "repay",
    "repel", "replace", "replica", "reply", "report", "repose",
    "repress", "request", "rescue", "research", "resemble", "resent",
    "reserve", "reside", "resist", "resolute", "resolve", "resort",
    "respect", "respite", "respond", "restful", "restore", "result",
    "resume", "retail", "retainer", "retina", "retire", "retort",
    "retreat", "return", "reunion", "reveal", "revenge", "revenue",
    "revere", "review", "revise", "revive", "revolt", "reward",
    "rhythm", "ribbon", "richer", "riddle", "rider", "ridge",
    "rifle", "rigor", "rinse", "ripple", "riser", "rival", "river",
    "rivet", "roamer", "roast", "robe", "robot", "rocket", "rodeo",
    "rogue", "roller", "romance", "rookie", "room", "rooster",
    "rooted", "roster", "rosy", "rotate", "rotor", "rouge",
    "rough", "round", "route", "royal", "rubber", "rubble", "ruby",
    "rucksack", "rudder", "ruffle", "rugby", "ruin", "ruler",
    "rumble", "rumor", "runner", "runway", "rural", "rustle",
    "saber", "saddle", "safari", "safely", "safer", "saint", "salad",
    "salmon", "salon", "salty", "salute", "samba", "sample",
    "sandal", "satin", "sauce", "sauna", "savor", "savory", "saxophone",
    "scald", "scale", "scallop", "scamper", "scandal", "scarce",
    "scarf", "scary", "scatter", "scenery", "scent", "scheme",
    "scholar", "school", "science", "scissors", "scoff", "scone",
    "scoop", "scooter", "score", "scorn", "scour", "scout", "scrap",
    "scrape", "scratch", "scream", "screen", "screw", "scribe",
    "scrub", "scuffle", "sculpt", "seagull", "seal", "season",
    "second", "secret", "sector", "secure", "sedan", "seedling",
    "seeker", "seem", "seesaw", "segment", "seize", "select",
    "selfie", "seller", "senate", "sender", "senior", "sense",
    "serene", "series", "sermon", "serpent", "server", "settle",
    "seven", "sever", "severe", "sewage", "shack", "shade",
    "shadow", "shady", "shake", "shallow", "shame", "shampoo",
    "shape", "share", "shark", "sharp", "shatter", "shave",
    "sheep", "sheer", "sheet", "shelf", "shell", "shelter",
    "sherbet", "shield", "shift", "shimmer", "shine", "shingle",
    "ship", "shirt", "shock", "shore", "short", "shout", "shovel",
    "showcase", "shower", "shred", "shrewd", "shriek", "shrine",
    "shrink", "shroud", "shrub", "shrug", "shuffle", "shutter",
    "shuttle", "sickle", "sidewalk", "siege", "sierra", "sieve",
    "sight", "signal", "silent", "silicon", "silly", "silver",
    "similar", "simmer", "simple", "sincere", "single", "sister",
    "sizzle", "skate", "sketch", "skilled", "skillet", "skim",
    "skinny", "skipper", "skirt", "skull", "slack", "slain",
    "slang", "slant", "slate", "sled", "sleek", "sleep", "sleet",
    "sleeve", "sleigh", "slice", "slider", "slight", "slimmer",
    "sling", "slogan", "slope", "slouch", "slower", "sludge",
    "slumber", "slush", "slyly", "smack", "small", "smarter",
    "smash", "smear", "smell", "smile", "smoke", "smooth", "snack",
    "snail", "snake", "snappy", "snare", "snarl", "sneaker", "sneeze",
    "snicker", "sniff", "sniper", "snore", "snorkel", "snowfall",
    "snuggle", "soak", "soapy", "sober", "soccer", "social", "socket",
    "sodium", "sofa", "soften", "solar", "soldier", "sole", "solemn",
    "solid", "solo", "solve", "somber", "sonar", "sooner", "soothe",
    "sorrow", "sort", "soul", "sound", "soup", "source", "souvenir",
    "sovereign", "space", "spacer", "spade", "spaghetti", "spaniel",
    "spark", "sparkle", "sparrow", "speak", "speaker", "special",
    "speck", "spectacle", "speech", "speed", "spell", "spelling",
    "spend", "sphere", "spice", "spicy", "spider", "spigot",
    "spike", "spill", "spinach", "spindle", "spine", "spiral",
    "spirit", "spite", "splash", "spleen", "splendid", "splinter",
    "split", "spoil", "sponge", "spoon", "spore", "sport",
    "spotlight", "spouse", "spout", "sprain", "spray", "spread",
    "spring", "sprinkle", "sprint", "sprite", "sprout", "spruce",
    "spun", "spur", "squall", "square", "squash", "squeak",
    "squeal", "squid", "stable", "stack", "stadium", "staff",
    "stage", "stagger", "stain", "stairs", "stake", "stale",
    "stalk", "stall", "stamp", "stance", "stand", "staple",
    "starch", "stare", "startle", "stately", "station", "statue",
    "status", "statute", "steadfast", "steady", "steak", "steal",
    "steam", "steed", "steep", "steer", "stellar", "stench",
    "stencil", "step", "stereo", "stern", "stethoscope", "steward",
    "sticker", "stifle", "still", "sting", "stir", "stitch",
    "stock", "stoker", "stomach", "stone", "stool", "stoop",
    "storage", "store", "storm", "story", "stout", "stove",
    "strain", "strand", "strange", "strap", "strategy", "straw",
    "stray", "streak", "stream", "street", "strength", "stress",
    "stretch", "stride", "strife", "strike", "string", "stripe",
    "strive", "stroke", "stroll", "strong", "struggle", "strut",
    "stucco", "studious", "study", "stuff", "stumble", "stump",
    "stunner", "sturdy", "style", "suave", "subdue", "subject",
    "sublet", "sublime", "submit", "subtle", "suburb", "subway",
    "succeed", "success", "succumb", "suffer", "suffice", "suffix",
    "sugar", "suggest", "suitor", "sulfur", "sullen", "summer",
    "summit", "summon", "sunbeam", "sundae", "sundial", "sunny",
    "sunrise", "sunset", "super", "supper", "supple", "supply",
    "support", "suppose", "supreme", "surge", "surgeon", "surly",
    "surmise", "surmount", "surprise", "surrender", "survey",
    "survive", "suspect", "suspend", "sustain", "swallow", "swamp",
    "swan", "swap", "swarm", "swatch", "sway", "sweater", "sweep",
    "sweet", "swell", "swift", "swimmer", "swindle", "swing",
    "swirl", "switch", "swoop", "sword", "symbol", "symphony",
    "syrup", "table", "tablet", "tackle", "tactic", "taffy",
    "tailor", "talent", "talisman", "taller", "tallow", "tally",
    "tamer", "tandem", "tangle", "tanker", "tapestry", "tapioca",
    "target", "tariff", "tarnish", "tassel", "taste", "tasty",
    "taught", "tavern", "tawny", "taxi", "teacher", "teacup",
    "teapot", "tearful", "tease", "tedious", "teeth", "temple",
    "tempt", "tenant", "tender", "tennis", "tenor", "tense",
    "tension", "tent", "tenure", "terminal", "terrain", "terrible",
    "terrific", "terror", "testify", "textile", "texture", "thankful",
    "thatch", "thaw", "theater", "theft", "theme", "theory",
    "therapy", "thicket", "thief", "thigh", "thimble", "thinner",
    "thirst", "thistle", "thorn", "thorough", "thought", "thousand",
    "thread", "threat", "thresh", "thrift", "thrill", "thrive",
    "throat", "throne", "throng", "throw", "thud", "thumb",
    "thunder", "thwart", "thyme", "ticket", "tidal", "tiger",
    "tighten", "timber", "timer", "timid", "tinker", "tinsel",
    "tissue", "titan", "title", "toaster", "tobacco", "today",
    "toddler", "toenail", "toffee", "together", "toilet", "token",
    "tolerate", "tomato", "tomb", "tomorrow", "tonal", "tongue",
    "tonight", "tonnage", "tooth", "topaz", "topic", "torch",
    "torment", "tornado", "torpedo", "torque", "torrent", "tortoise",
    "total", "touch", "tough", "tourist", "tourney", "toward",
    "towel", "tower", "town", "toxic", "toybox", "trace",
    "track", "tractor", "trade", "tragedy", "trail", "trailer",
    "train", "traitor", "trance", "tranquil", "transfer", "transform",
    "transit", "travel", "trawler", "tray", "treacherous", "tread",
    "treason", "treat", "treaty", "treble", "trekker", "tremble",
    "tremor", "trench", "trend", "trepid", "trespass", "trial",
    "triangle", "tribe", "tribute", "trickle", "trifle", "trigger",
    "trillion", "trilogy", "trim", "trinity", "trinket", "trio",
    "triple", "triumph", "trivia", "trolley", "trombone", "troop",
    "trophy", "tropic", "trouble", "trough", "trounce", "troupe",
    "trout", "trowel", "truce", "truck", "truer", "truffle",
    "trumpet", "trundle", "trunk", "trust", "truth", "trying",
    "tulip", "tumble", "tuna", "tundra", "tunnel", "turban",
    "turbine", "turbulent", "turf", "turkey", "turmoil", "turner",
    "turtle", "tutor", "twang", "tweed", "twice", "twilight",
    "twin", "twinkle", "twirl", "twist", "tycoon", "typhoon",
    "typical", "typist", "typo", "umbrella", "umpire", "unable",
    "unaware", "uncanny", "uncle", "uncouth", "under", "underdog",
    "undo", "undulate", "unearth", "uneasy", "unfair", "unfold",
    "unfriendly", "unify", "union", "unique", "unite", "unity",
    "universe", "unjust", "unknown", "unlock", "unlucky", "unmask",
    "unmoved", "unpack", "unravel", "unrest", "unruly", "unseen",
    "unsteady", "untie", "until", "unusual", "unveil", "unwilling",
    "unwise", "upbeat", "upcoming", "update", "upheld", "uphill",
    "uplift", "upload", "upper", "upright", "uprising", "uproar",
    "uproot", "upset", "upstage", "upstairs", "upstart", "upward",
    "urban", "urge", "urgent", "urgency", "usable", "useful",
    "usher", "usual", "utility", "utmost", "utter", "vacant",
    "vacation", "vaccine", "vacuum", "vague", "valiant", "valley",
    "valor", "value", "valve", "vampire", "vanilla", "vanish",
    "vanity", "vapor", "varied", "variety", "various", "varnish",
    "vase", "vault", "vector", "veil", "velvet", "vendor", "veneer",
    "venom", "vent", "venture", "venue", "verbal", "verify",
    "vermilion", "versatile", "verse", "version", "versus", "vertex",
    "vessel", "vestige", "viable", "vibrate", "vicar", "victim",
    "victor", "victory", "video", "viewer", "vigor", "village",
    "vinegar", "violin", "viper", "viral", "virtual", "virtue",
    "visa", "visage", "vision", "visit", "visual", "vital",
    "vitamin", "vivid", "vixen", "vocal", "vogue", "voice",
    "void", "volcano", "volume", "volunteer", "vortex", "voter",
    "vouch", "vowel", "voyage", "vulgar", "vulture", "waffle",
    "wager", "wagon", "waist", "waiter", "wake", "waken", "walnut",
    "waltz", "wander", "wane", "wangle", "want", "warden",
    "warmer", "warn", "warrior", "waste", "watch", "water",
    "wattle", "wave", "waver", "waylay", "wealth", "weasel",
    "weather", "weave", "wedding", "wedge", "weed", "weekday",
    "weekly", "weigher", "weight", "weird", "welcome", "weld",
    "welfare", "wellness", "western", "wetland", "whack", "whale",
    "wharf", "wheat", "wheel", "wheeze", "whelk", "whelp",
    "where", "whet", "whether", "which", "whiff", "while",
    "whimper", "whimsy", "whine", "whip", "whirl", "whisk",
    "whisper", "whistle", "white", "whittle", "whole", "wholesome",
    "whoosh", "wicked", "wicker", "widen", "widow", "width",
    "wield", "wight", "wiggle", "wild", "wilder", "willow",
    "wilt", "wimple", "wince", "winch", "wind", "windmill", "window",
    "wine", "wing", "wink", "winner", "winter", "wipe",
    "wireless", "wiry", "wisdom", "wisely", "wish", "wisp",
    "wisteria", "witch", "withdraw", "withhold", "within", "witness",
    "wizard", "wobble", "woeful", "wolf", "wolverine", "woman",
    "wombat", "wonder", "wont", "wooden", "woodland", "wool",
    "word", "work", "workshop", "world", "worry", "worth",
    "worthy", "woven", "wrangle", "wrap", "wrath", "wreath",
    "wreck", "wrench", "wrestle", "wretched", "wriggle", "wrinkle",
    "wrist", "writer", "wrong", "wrote", "yacht", "yammer",
    "yard", "yarn", "yawn", "yearly", "yearn", "yeast", "yellow",
    "yesterday", "yield", "yodel", "yoga", "yogurt", "yonder",
    "youth", "zany", "zebra", "zenith", "zephyr", "zero",
    "zest", "zigzag", "zinc", "zipper", "zodiac", "zombie",
}))

# 段位：(百分比阈值, 中文名, 英文名)
RANKS = (
    (0, "新手上路", "Beginner"),
    (5, "渐入佳境", "Good Start"),
    (10, "稳步上升", "Moving Up"),
    (15, "表现不错", "Good"),
    (25, "实力扎实", "Solid"),
    (40, "相当出色", "Nice"),
    (50, "了不起", "Great"),
    (60, "令人惊叹", "Amazing"),
    (70, "天才", "Genius"),
)


def score_word(word: str) -> int:
    """单个词的分数：4 字母=1 分；更长=字母数；pangram=+7。"""
    n = len(word)
    base = 1 if n == 4 else n
    if len(set(word)) >= 7:  # 用遍 7 个字母 -> pangram
        base += 7
    return base


def valid_words(center: str, others: str) -> list[str]:
    """返回本局所有合法词（按分数降序、字母序）。"""
    letters = set(others + center)
    out = []
    for w in WORDS:
        if len(w) < 4:
            continue
        if center not in w:
            continue
        if set(w) <= letters:
            out.append(w)
    out.sort(key=lambda w: (-score_word(w), w))
    return out


def max_score(center: str, others: str) -> int:
    """本局满分。"""
    return sum(score_word(w) for w in valid_words(center, others))


def rank_for(score: int, total: int) -> tuple[int, str, str]:
    """按得分百分比返回段位 (阈值, 中文名, 英文名)。"""
    pct = 100.0 * score / total if total else 0.0
    rank = RANKS[0]
    for r in RANKS:
        if pct >= r[0]:
            rank = r
    return rank


def check_guess(word: str, center: str, others: str) -> tuple[bool, str]:
    """校验猜测，返回 (是否合法, 原因/分数说明)。"""
    word = word.strip().lower()
    letters = set(others + center)
    if len(word) < 4:
        return False, "太短了，单词至少 4 个字母"
    if not word.isalpha():
        return False, "只能用字母"
    if any(ch not in letters for ch in word):
        return False, "只能用给出的 7 个字母"
    if center not in word:
        return False, f"必须包含中心字母 {center.upper()}"
    if word not in WORDS:
        return False, "词表里没有这个词"
    return True, ""


def generate_puzzle(rng: random.Random, min_words: int = 15) -> tuple[str, str]:
    """随机生成一局：返回 (center, others)。

    从词表中挑一个恰好含 7 个不同字母的词作为 pangram 种子，
    保证每局至少有 1 个 pangram 且合法词数达标。
    """
    candidates = [w for w in WORDS if len(set(w)) == 7]
    for _ in range(2000):
        pangram = rng.choice(candidates)
        letters = sorted(set(pangram))
        center = rng.choice(letters)
        others = "".join(c for c in letters if c != center)
        if len(valid_words(center, others)) >= min_words:
            return center, others
    # 兜底：固定一局（已知有充足合法词 + pangram）
    return "e", "adlnrt"


def puzzle_stats(center: str, others: str) -> dict:
    words = valid_words(center, others)
    return {
        "words": words,
        "count": len(words),
        "total": sum(score_word(w) for w in words),
        "pangrams": [w for w in words if len(set(w)) == 7],
    }


def play(center: str, others: str, show_all: bool = False) -> int:
    """交互主循环，返回最终得分。"""
    stats = puzzle_stats(center, others)
    words = set(stats["words"])
    found: set[str] = set()
    score = 0
    total = stats["total"]

    print("🐝 拼字蜜蜂 Spelling Bee")
    print(f"中心字母（必须用）: {center.upper()}")
    print(f"全部字母: {' '.join(sorted((others + center).upper()))}")
    print(f"本局共有 {stats['count']} 个词，满分 {total} 分")
    print("输入单词猜（:help 看帮助，:rank 看段位，:quit 退出）\n")

    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            raw = ":quit"
        cmd = raw.lower()
        if cmd in (":quit", ":q", "quit", "exit"):
            break
        if cmd in (":help", ":h", "?"):
            print("规则：单词 ≥4 字母、只用给出的 7 个字母、必须含中心字母、"
                  "必须在词表里。4 字母词 1 分，更长按字母数计分，"
                  "用遍 7 字母的 pangram 额外 +7 分。")
            continue
        if cmd in (":rank", ":r"):
            th, zh, en = rank_for(score, total)
            print(f"当前 {score}/{total} 分（{100*score/max(total,1):.1f}%）— "
                  f"段位：{zh} ({en})")
            continue
        if cmd in (":words", ":w"):
            print(f"已找到 {len(found)}/{stats['count']} 个词："
                  + (", ".join(sorted(found)) or "（暂无）"))
            continue
        ok, msg = check_guess(cmd, center, others)
        if not ok:
            print(f"❌ {msg}")
            continue
        if cmd in found:
            print("已经猜过这个词啦")
            continue
        found.add(cmd)
        pts = score_word(cmd)
        score += pts
        tag = " 🌟 PANGRAM!" if len(set(cmd)) == 7 else ""
        print(f"✅ +{pts} 分{tag}  （{score}/{total}）")

    th, zh, en = rank_for(score, total)
    print(f"\n本局结束：{score}/{total} 分（{100*score/max(total,1):.1f}%），"
          f"段位 {zh} ({en})，找到 {len(found)}/{stats['count']} 个词")
    if show_all:
        print("\n全部答案：")
        for w in stats["words"]:
            print(f"  {w}  (+{score_word(w)})")
    else:
        missed = [w for w in stats["words"] if w not in found]
        if missed:
            print(f"没猜出的词还有 {len(missed)} 个，加 --answers 可看全部答案")
    return score


def cmd_answers(center: str, others: str) -> int:
    stats = puzzle_stats(center, others)
    print(f"中心字母: {center.upper()}  字母: {' '.join(sorted((others+center).upper()))}")
    print(f"共 {stats['count']} 个词，满分 {stats['total']} 分\n")
    for w in stats["words"]:
        star = " ★" if len(set(w)) == 7 else ""
        print(f"{w:<14} +{score_word(w)}{star}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="spellingbee",
        description="拼字蜜蜂 Spelling Bee：用 7 个字母拼出尽可能多的单词",
    )
    p.add_argument("--seed", type=int, default=None, help="随机种子（可复现同一局）")
    p.add_argument("--answers", action="store_true",
                   help="直接列出本局全部合法词与分数（不进入游戏）")
    p.add_argument("--letters", type=str, default=None,
                   help="指定 7 个字母，第 1 个为中心字母，如 --letters eadlnrt")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rng = random.Random(args.seed) if args.seed is not None else secrets.SystemRandom()

    if args.letters:
        s = args.letters.strip().lower()
        if len(s) != 7 or not s.isalpha() or len(set(s)) != 7:
            print("错误：--letters 必须是 7 个不重复的字母", file=sys.stderr)
            return 2
        center, others = s[0], s[1:]
    else:
        center, others = generate_puzzle(rng)

    if args.answers:
        return cmd_answers(center, others)
    play(center, others, show_all=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
