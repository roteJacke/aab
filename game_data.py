characters = {
	"THE_PLAYER": {
		"name": "Lurco",
		"equipped": [None] * 6,  # armor, weapon
		"inventory": ["copper_sword"],
		"coin": 1000,
		"stats": [
			[3, 10], 1, 15, 0, 1, 12345,  # HP AP Dodge, D, A, EXP
			60, 15, 25, 25, 0  # HC IA CC CD BD
		],
		"mods": {
			# HC IA CC CD BD
			"sword": [10, -15, -5, 25, 0],
			"axe": [0, 0, -10, 75, 0],
			"mace": [-25, 30, -15, 75, 0],
		},
		"perks": [],
		"avatar": "czlurco_ava-100x105",
		"image": "player_img",
		"map_image": "map_lurco-35x35",
		"place_image": "czlurco_place",
		"location": None,
	},
	# NPCs -------------------------------------
	"ferrec": {  # merchant,
		"name": "Ferrec",
		"coin": 475,
		"inventory": ["books", "books", "hpot0"],
		"avatar": "czferrec_ava-100x105",
		# default inv? to reset auto, optional
	},
	"innkeeper": {  # merchant and ?quest giver
		"name": "Innlady",
		"coin": 12,
		"inventory": ["hpot0", "hpot0", "hpot0", "copper_sword"],
		"avatar": "czinnkeeper_ava-100x105",
		# default inv? to reset auto, optional, not implemented yet
		#"default_inventory": (12, ["hpot0"] * 5),
	},
	# Enemies ----------------------------------
	"bandit0": {
		"name": "Weak Bandit",
		"inventory": [],
		"coin": 25,
		"stats": [
			[17, 17], 1, 5, 1, 2, 0,
			50, 15, 15, 25, 0
		],
		"avatar": None,
		"image": None,
	},
}
containers = {
	"hausbox": {
		"name": "Chest",
		"inventory": ["books", "books", "books", "iron_sword", "iron_sword"],
		"coin": 1,
		"avatar": "czchest_ava-100x105",
		#"box_image": "box3-310x337",
	},
}
items = {
	# armor ------------------------------------
	"cloak_shield0": {
		"name": "Cloak and Shield",
		"type": "armor",
		"image": "invi_cloaknshield",
		"descr": None,
		"price": [61, 30],
		# unique variables
		"defense_value": 1,
	},
	# potion -----------------------------------
	"hpot0": {
		"name": "Health Potion",
		"type": "potion",
		"image": "invi_potion",
		"descr": "A bitter potion of healing.",
		"price": [47, 27],
		#"quality": ("Uncommon", "#776611"),
		# unique variables
		"heal_value": 7,
	},
	# treasure ---------------------------------
	"books": {  # make quality list later
		"name": "Books",
		"type": "treasure",
		"image": "invi_books",
		"descr": "Valuable to the wealthy and few.",
		"quality": ("Uncommon", "#776611"),
		# buy/sell
		"price": [250, 125],
	},
	# weapon -----------------------------------
	"copper_axe": {
		"name": "Copper Axe",
		"type": "weapon",
		"image": None,
		"descr": None,
		"price": [107, 49],
		# unique variables
		"weapon_type": "axe",
		"attack_value": 3,
	},
	"copper_mace": {
		"name": "Copper Mace",
		"type": "weapon",
		"image": None,
		"descr": None,
		"price": [149, 75],
		# unique variables
		"weapon_type": "mace",
		"attack_value": 5,
	},
	"copper_sword": {
		"name": "Copper Sword",
		"type": "weapon",
		"image": "invi_swordc",
		"descr": "A useful tool for slicing paper.",
		"price": [87, 45],
		# unique variables
		"weapon_type": "sword",
		"attack_value": 1,
	},
	"iron_sword": {
		"name": "Iron Sword",
		"type": "weapon",
		"image": "invi_swordi",
		"descr": "A popular weapon for killing peasants.",
		"price": [261, 129],
		# unique variables
		"weapon_type": "sword",
		"attack_value": 7
	},
}
perks = {
	# % % r r r
	# "HP", "AP", "Dodge%", "Def", "Atk"
	# %/raw for each type, not both to avoid errors
	#"sym": ["HP", "AP", "Dodge%", "Def", "Atk"],
	"swordDMG0": {
		"name": "Sword Mastery I",
		"desc": "Increases sword damage by 13.5%",
		"level": [0, 10],
		"affects": ["swordDB"], 
		"change": ["13.5raw"],
		"prerequisite": None,
		"img": "perk_swordi-40x40",
	},
	"swordHC0": {
		"name": "Fruit Slicer",
		"desc": "Increases sword hit chance by 4.5%",
		"level": [0, 5],
		"affects": ["swordHC"], 
		"change": ["4.5raw"],
		"prerequisite": ("swordDMG0", 3),
		"img": "perk_fruitslicer-40x40",
	},
	"swordCC0": {
		"name": "Piercing Strike",
		"desc": "Increase sword critical hit chance by 7.5%",
		"level": [0, 4],
		"affects": ["swordCC"], 
		"change": ["7.5raw"],
		"prerequisite": ("swordDMG0", 2),
		"img": "perk_piercingstrike-40x40",
	},
	"swordMX0": {
		"name": "Sword Adept",
		"desc": "Increases sword damage by 75%",
		"level": [0, 1],
		"affects": ["swordDB"], 
		"change": ["75raw"],
		"prerequisite": ("swordHC0", 5),
		"img": "perk_swordadept-40x40",
	},
	"dodge0": {
		"name": "Fast Reflexes",
		"desc": "Increases dodge by 2.9%",
		"level": [0, 9],
		"affects": ["Dodge%"], 
		"change": ["2.9raw"],
		"prerequisite": None,
		"img": "perk_fastreflex-40x40",
	},
	"dodgeMX0": {
		"name": "Faster Reflexes",
		"desc": "Increases dodge by 7.5%",
		"level": [0, 1],
		"affects": ["Dodge%"], 
		"change": ["7.5raw"],
		"prerequisite": ("dodge0", 9),
		"img": "perk_fasterreflex-40x40",
	},
}
map = {
	"Badlands": {  # region
		"places": {
			"hilltown": {
				"name": "Hilltown",
				"map_image": "map_htown-175x66",
				"image": "place_htown",
				"descr": "A fledgling colony on the far reaches of The Empire.",
				"type": "Settlement",
				"coords": (380, 200),
				# events
				"events": [  # condition  event  hovertext  location+image
					(None, "dlg|ht00", "Tavern", "510-225|picon_mug-42x42"),
					(None, "str|ferrec", "Store", "142-247|picon_gpot-42x42"),
					(None, "dlg|ht02", "Herald", "372-242|czherald_place-50x95"),
					("QA00|0", "box|hausbox", "Dead Herald", "720-260|czherald_place-50x95"),
					#("", "dialog|first_visit_hilltown_tavern", "Tavern=It's good for your health.", "450-200|b0.a-40x40"),
				],
				"leave_btn": True,
			},
		},
		"image": "map_badlands",
	},
}
# Only one (1) requirement to adv stage unless items
quests = {  # Quest added to fertigql if reward is given
	# Main Quests
	"A00": {
		"name": "The Beginning",
		"prev|next": [None, None],  # prev q need to be completed to be available
		"prerequisites": None,
		"stage": [1, 5],
		"stage1": [
			"    You woke up once more. It had been days since the attack. You " \
			"sit down with your back against the tree and begin to think. H" \
			"ours of hiking through the forest without rest took a toll on " \
			"your legs. You realize you need to gain back your strength bef" \
			"ore confronting the ones who killed your wife. They may as wel" \
			 "l be gone forever. You could regain your strength and money in" \
			"Hilltown. The townspeople might have information about the ban" \
			"dits. \n",
			["item|CRYSTAL_FIRE|x"]
		],
		"stage2": ["", [""]],
	},
	# Misc Quests
	"mq00": {
		"name": "A Want For A Book",
		"prerequisites": None,
		"prev|next": None,
		"reward": [450, 37, ["hpot0"] * 1],  # exp, gold, items
		"stage": [0, 3],
		"stage1": [
			"    The innkeeper has a want for a book. She said she'd give m" \
			"e something nice in return. Books are expensive after all. An " \
			"easier option is to buy it from a store but it would cost me a" \
			" lot. I need the money. I should ask the locals for more infor" \
			"mation. \n",
			["item|books|x"]  # req to advance stage
		],
		"stage2": [
			"    The woman wants a book and now you have it. You should go " \
			"back to the innkeeper in Hilltown. \n",
			["reward|waiting..."]  # length to 1 for now when giving reward
		],
		"stage3": [  # text display quest completed future
			"    I found a book and gave it to the innkeeper. She was pleas" \
			"ed and gave me a small reward.",
			None
		],
	},
	"mq01": {  # fix later
		"name": "A Need For A Book",
		"prerequisites": "mq00",
		"prev|next": None,
		"reward": [360, 437, ["hpot0"] * 2],  # exp, gold, items
		"stage": [0, 3],
		"stage1": [
			"    The innkeeper has a need for a book. She said she'd give m" \
			"e something good in return. Books are expensive after all. An " \
			"easier option is to buy it from a store but it would cost me a" \
			" lot. I need the money. I should ask the locals for more infor" \
			"mation. \n",
			["item|books|x", "item|books|x", "item|books|x"]
		],
		"stage2": [
			"    The woman needs a book and now you have it. You should go " \
			"back to the innkeeper in Hilltown. \n",
			["reward|waiting..."]  # length to 1 for now when giving reward
		],
		"stage3": [  # text display quest completed future
			"    I found books and gave it to the innkeeper. She was please" \
			"d and gave me a nice reward.",
			None
		],
	},
}


'''
	"Misc00": {
		"name": "",
		"prerequisites": None,
		"prev|next": None,
		"quest_line": "Misc",
		"reward": "",
		"stage": [0, 3],
		"s1data": ["", ["item|special_book"]],
		"s2data": ["", ["reward|collected"]],
		"s3data": ["", None],
	},
	"Misc00a": {
		"name": "A Want For A Book",
		"requirements": [], # quest, lvl, gold, ? req to start quest
		"reward": [],
		"stage": [0, 3],
		"stage1": {
			"descr": "",
			
		},  # txt, req to next stage, function to check quest conditions
		"type": "misc",
	},
	"M00": {
		# dialogs ui will advance quest stages
		"name": "A Want For A Book",
		"prev|next": [None, "M01"],  # prev, next quest
		"reward": [0, []],  # gold, items
		"stage": [0, 3],  # -1 locked, 0 available, max completed
		"stage1_descr": None,  # accepted
		"stage2_descr": None,  # objective achieved
		"stage3_descr": None,  # reward collected, unlocks next quest
	},
	"A00": {
		"name": "The Beginning",
		"status": "accepted",  # locked, available, accepted, completed
		"prev|next": [None, None],  # prev q need to be completed to be available
		"prerequisites": [],
		"stage": [0, 5],
		"stage00_descr": (
			"You woke up once more. It had been days since the attack. You " \
			"sit down with your back against the tree and begin to think. H" \
			"ours of hiking through the forest without rest took a toll on " \
			"your legs. You realize you need to gain back your strength bef" \
			"ore confronting the ones who killed your wife. They may as wel" \
			 "l be gone forever. You could regain your strength and money in" \
			"Hilltown. The townspeople might have information about the ban" \
			"dits. \n"
		),
	},
	"m00": {
		"name": "A need for enlightenment",
		"desc": "The innkeeper wants a book to read. She said that she woul" \
			"d pay 275 sconariis for it. She likes books.",
		"stages": 2,
		"quest_status": "available",
	},
'''	
























