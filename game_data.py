characters = {
	"THE_PLAYER": {
		"name": "Lurco",
		"equipped": [None] * 6,  # armor, weapon
		"inventory": ["copper_sword", "hpot0", "hpot0", "hpot0", "hpot0", "hpot0", "hpot0"],
		"coin": 100,
		"stats": [
			[70, 100], 1, 15, 0, 10, 12345,  # HP AP Dodge, D, A, EXP
			60, 15, 25, 25, 0  # HC IA CC CD BD
		],
		"mods": {
			# HC IA CC CD BD
			"sword": [10, -15, -5, 25, 0],
			"axe": [0, 0, -10, 75, 0],
			"mace": [-25, 30, -15, 75, 0],
		},
		"perks": [],
		#"avatar": "czlurco_ava-100x105",
		"avatar": "bw-man0-ava",
		"image": "bw-man0",
		"map_image": "map_lurco-35x35",
		#"place_image": "czlurco_place",
		#"place_image": "bw-player0",
		#"place_indoor_image": "bw-player0I",
		"place_image": "bw-man0",
		"place_indoor_image": "bw-man0",
		#"place_image": "bw-woman0",
		"location": None,  
		"location_coords": [50, 50],  # location of player in map
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
	"cave_lookout": {
		"name": "Lookout",
		"inventory": [],
		"coin": 25,
		"stats": [
			[17, 17], 2, 5, 1, 2, 0,
			60, 15, 15, 25, 0
		],
		"avatar": "bw-man0i-ava",
		"image": "bw-man0i-f",
	},
	"bandit0": {
		"name": "Weak Bandit",
		"inventory": [],
		"coin": 25,
		"stats": [
			[17, 17], 1, 5, 1, 2, 0,
			60, 15, 15, 25, 0
		],
		"avatar": "bw-man0i-ava",
		"image": "bw-man0i-f",
	},
	"mplant0": {
		"name": "Cinder Plant",
		"inventory": [],
		"coin": 0,
		"stats": [
			[5, 25], 2, 1, 0, 1, 100,
			70, 15, 15, 25, 0
		],
		"avatar": "bw-t-fmonster0-ava",
		"image": "bw-t-fmonster0",
	},
}
containers = {
	"hausbox": {
		"name": "Chest",
		"inventory": ["books", "books", "books", "iron_sword", "iron_sword"],
		"coin": 9000,
		"avatar": "czchest_ava-100x105",
		#"box_image": "box3-310x337",
	},
	"cabin_chest": {
		"name": "Chest",
		"inventory": ["books"],
		"coin": 9000,
		"avatar": "czchest_ava-100x105",
	}
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
	"hpot1": {
		"name": "Cinder Extract",
		"type": "potion",
		"image": "invi_potion",
		"descr": "A powerful potion of healing.",
		"price": [127, 67],
		"heal_value": 20,
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
map_markers = {
	"cabin": {
		"name": "Cabin",
		"image": "bw-cabin-35x35",
		"coords": (150, 400),
		"condition": None,
		#"event": "place|cabin",  # future
		#"place": "cabin", redundant as key is the parameter
	},
	"cave": {
		"name": "Cave",
		"image": "bw-cave-35x35",
		"coords": (110, 200),
		"condition": None,
	},
	"forest": {
		"name": "Forest",
		"image": "bw-forest-30x30",
		"coords": (185, 450),
		"condition": None,
	},
	"village": {
		"name": "Village",
		"image": "bw-village-40x40",
		"coords": (355, 250),
		"condition": None,
	},
}
'''
	"vhouse": {
		"name": "?????",
		"image": "bw-vhouse-37x37",
		"coords": (725, 100),
		"condition": None,
		#"event": "place|cabin",  # future
		#"place": "cabin", redundant as key is the parameter
	},
	"fhouse": {
		"name": "?????",
		"image": "bw-fhouse-30x30",
		"coords": (120, 60),
		"condition": None,
		#"event": "place|cabin",  # future
		#"place": "cabin", redundant as key is the parameter
	},
	"hillfort": {
		"name": "?????",
		"image": "bw-hillfort-40x40",
		"coords": (585, 50),
		"condition": None,
		#"event": "place|cabin",  # future
		#"place": "cabin", redundant as key is the parameter
	},
	"church": {
		"name": "?????",
		"image": "bw-church-35x35",
		"coords": (720, 200),
		"condition": None,
		#"event": "place|cabin",  # future
		#"place": "cabin", redundant as key is the parameter
	},
	"house": {
		"name": "House",
		"image": "bw-house-30x30",
		"coords": (530, 180),
		"condition": None,
		#"event": "place|cabin",  # future
		#"place": "cabin", redundant as key is the parameter
	},
	"camp": {
		"name": "Camp",
		"image": "bw-tent-30x30",
		"coords": (630, 300),
		"condition": None,
		#"event": "place|cabin",  # future
		#"place": "cabin", redundant as key is the parameter
	},
'''
world_places = {
	"vhouse": {
		"name": "Camp",
		"type": ["outdoors", "bw-bg_top2", "bw-bg_bot1"],
		"entry_coords": (425, 417),
		"walk_range": "default",
		"events": [
			(None, None, "bw-gate0|245,210"),
			(None, "leave|", "bw-arrow_down|445,545"),
		],
	},
	"fhouse": {
		"name": "Camp",
		"type": ["outdoors", "bw-bg_top2", "bw-bg_bot1"],
		"entry_coords": (425, 417),
		"walk_range": "default",
		"events": [
			(None, None, "bw-gate0|245,210"),
			(None, "leave|", "bw-arrow_down|445,545"),
		],
	},
	"hillfort": {
		"name": "Camp",
		"type": ["outdoors", "bw-bg_top2", "bw-bg_bot1"],
		"entry_coords": (425, 417),
		"walk_range": "default",
		"events": [
			(None, None, "bw-gate0|245,210"),
			(None, "leave|", "bw-arrow_down|445,545"),
		],
	},
	"forest": {
		"name": "Forest",
		"type": ["outdoors", "bw-bg_top1", "bw-bg_bot1"],
		"entry_coords": (425, 417),
		"walk_range": "default",
		"events": [
			("Qstarted|MQ01", "place|forest_inner0*155,345", "bw-arrow_up|700,275"),
			(None, "leave|", "bw-arrow_down|445,545"),
		],
	},
	"forest_inner0": {
		"name": "Forest",
		"type": ["outdoors", "bw-bg_top1", "bw-bg_bot1"],
		"entry_coords": (425, 417),
		"walk_range": "default",
		"events": [
			#(None, "battl|mplant0=test::test::test", "bw-t-fmonster0|545,345"),
			(None, "dialg|mplant0", "bw-t-fmonster0|590,180"),
			(None, "place|forest", "bw-arrow_up|100,275"),
		],
	},
	"church": {
		"name": "Camp",
		"type": ["outdoors", "bw-bg_top2", "bw-bg_bot1"],
		"entry_coords": (425, 417),
		"walk_range": "default",
		"events": [
			(None, None, "bw-gate0|245,210"),
			(None, "leave|", "bw-arrow_down|445,545"),
		],
	},
	#
	"cabin": {
		"name": "Cabin",
		"type": ["outdoors", "bw-bg_top1", "bw-bg_bot1"],
		"entry_coords": (625, 317),
		"walk_range": "default",
		"events": [
			("Qdormant|MQ01", None, "bw-house0|250,170"),
			("Qdormant|MQ01", "place|cabin_indoors", "bw-hdoor0|270,253"),
			("Qstarted|MQ01", None, "bw-house0-z|250,170"),
			("Qdormant|MQ01", "dialg|patience_cabin-0", "bw-woman0|180,225"),
			(None, "leave|", "bw-arrow_up|555,270"),
		],
	},
	"cave": {
		"name": "Cave",
		"type": ["outdoors", "bw-bg_top1", "bw-bg_bot1"],
		"entry_coords": (675, 317),
		"walk_range": "default",
		"events": [
			#(None, None, "bw-cave|100,175"),
			("Qdormant|MQ02", None, "bw-cave|100,175"),
			("Qstage1|MQ02", "dialg|MQ02-1", "bw-cave|100,175"),
			("Qstage2|MQ02", "place|cave_inner", "bw-cave|100,175"),
			(None, "leave|", "bw-arrow_up|705,270"),
		],
	},
	"cave_inner": {
		"name": "Cave",
		"type": ["outdoors", "bw-bg_top3", "bw-bg_bot3"],
		"entry_coords": (675, 317),
		"walk_range": "default",
		"events": [
			#(None, None, "bw-cave|100,175"),
			(None, "place|cave", "bw-arrow_up|705,270"),
		],
	},
	"house": {
		"name": "House",
		"type": ["outdoors", "bw-bg_top1", "bw-bg_bot1"],
		"entry_coords": (625, 317),
		"walk_range": "default",
		"events": [
			(None, None, "bw-house1|250,160"),
			(None, "leave|", "bw-arrow_up|705,270"),
		],
	},
	"camp": {
		"name": "Camp",
		"type": ["outdoors", "bw-bg_top2", "bw-bg_bot1"],
		"entry_coords": (425, 417),
		"walk_range": "default",
		"events": [
			(None, None, "bw-gate0|245,210"),
			(None, "leave|", "bw-arrow_down|445,545"),
		],
	},
	"village_tavern": {
		"name": "Tavern",
		"type": ["indoors", "bw-wall0", "bw-floor0"],
		"entry_coords": (480, 285),
		"walk_range": "default",
		"events": [
			(None, "place|village*312,320", "bw-door0f|432,157"),
			(None, "place|village*312,320", "bw-door0|565,157"),
			#(None, "dialg|MQ01-00", "bw-woman0|180,190"),
			#("Qstage1|MQ01", "dialg|tavern_innkeeper-0", "bw-woman0|180,190"),
			(None, "dialg|tavern_innkeeper-0", "bw-woman0|180,190"),
			(None, None, "bw-counter|65,270"),
			(None, None, "bw-table|80,450"),
			(None, None, "bw-table|538,450"),
		],
	},
	"cabin_indoors": {
		"name": "Cabin",
		"type": ["indoors", "bw-wall0", "bw-floor0"],
		"entry_coords": (480, 285),
		"walk_range": "default",
		"events": [
			(None, "place|cabin*312,320", "bw-door0|412,157"),
			(None, None, "bw-bed0|60, 267"),
			(None, None, "bw-closet0|275, 180"),
			(None, "chest|cabin_chest", "bw-chest0|630,450"),
		],
	},
	"village": {
		"name": "Village",
		"type": ["outdoors", "bw-bg_top0", "bw-bg_bot1"],
		"entry_coords": (625, 317),
		"walk_range": "default",
		"events": [
			# Tavern
			(None, None, "bw-house0|160,170"),
			(None, "store|ferrec", "bw-hdoor0|180,253"),
			(None, None, "bw-house1|-50,160"),
			(None, None, "bw-tavern|245,135"),
			(None, "place|village_tavern", "bw-hdoor0|388,259"),
			# Empty House
			(None, None, "bw-house0|705,170"),
			(None, "dialg|village-empty_house", "bw-hdoor0|722,253"),
			(None, "leave|", "bw-gate0|585,213"),  # Gate
		],
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
					(None, None, "Town Hall", "680-214|h1-155x190"),
					(None, None, "", "5-265|h1-155x190"),
					(None, "dlg|ht02", "Herald", "282-270|czherald_place-50x95"),
					("QA00|1", "box|hausbox", "Dead Herald", "720-260|czherald_place-50x95"),
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
	# MAIN QUEST ACT 1
	"MQ00": {
		"name": "Woman In Illness",
		"stage": [0, 2],
		"stage1": [
			"    I must go to the village and find a health potion." \
			" I should talk to the innkeeper for more information.\n"
		],
		"stage2": [
			"    I got and delivered the health portion."
		],
		"reward": [123, 50, ["hpot0", "hpot0"]]
	},
	"MQ01": {
		"name": "Gathering The Pieces",
		"stage":[0, 3],
		"stage1": [
			"    Once I am able to, I should go to the village for help." \
			" Some of the villagers may have information about the attack." \
			" I am too wounded to fight the bandits and I need time to rest and recover."
		],
		"stage2": [
			"    The Forest near the village contains a plant that contains an extract that could heal the boy." \
			" He could give us a significant amount of information about the bandits if he is well." \
			" I should at least have a sword and a tonic, the innkeeper told me." \
		],
		"stage3": [
			"    I had given the plant extract to the innkeeper as soon as I could." \
			" The mute boy recovered but was still bedridden." \
			" He made shapes out of his fingers and arms, that I could not comprehend." \
			" Finally, the innkeeper turned towards me and uttered, ''The caves to the north west.''."
		],
		"reward": [1250, 10, ["iron_sword"]],
	},
	"MQ02": {
		"name": "Descending The Void",
		"stage":[0, 3],
		"stage1": [
			"A group of bandits are hiding in a cave to the north west. They may be the ones that have attacked the cabin."
		],
		"stage2": [
			"The lookout is dead. I should go further down the cave."
		],
		"stage3": [
			"The bandits are dead. I had rescued a girl, related to the mute boy. She had given me significant information."
		],
		"reward": [2500, 425, ["iron_sword", "iron_sword", "hpot0", "hpot0", "hpot0"]],
	},
	#
	"main_quest0.0": {
		"name": "The Aftermath",
		"stage": [0, 3],
		"stage1": [
			"   1.",
		],
		"stage2": [
			"    2.",
		],
		"stage3": [
			"    completed.",
		],
		"reward": [100, 1, []],
	},
	"squest0.0": {
		"name": "Bring Her A Tonic",
		"stage": [0, 2],
		"stage1": [
			"    She wants a tonic.",
		],
		"stage2": [
			"    I got her a tonic.",
		],
		"reward": [100, 1, ["hpot0"]],
	},
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
























