dialogs = {
	"test": {
		"text": [ "TEST",
			"    Test dialogs." \
		],
		"choices": [
			(None, "leave|", "Leave"),
		],
	},
	# Enemies
	"mplant0": {
		"text": [ "A Dangerous Plant",
			"    It looks sharp."
		],
		"choices": [
			(None, "battl|mplant0=mplant0-win::test::test", "Fight It"),
			(None, "leave|", "Leave"),
		],
	},
	"mplant0-win": {
		"text": [ "A Dangerous Plant",
			"    It looks dead. You collect its extract."
		],
		"reward": [125, 0, ["hpot1", "hpot1"]],
		"choices": [
			(None, "leave|", "Leave"),
		],
	},
	# Main And Side Characters
	"patience_cabin-0": {
		"text": [ "Patience Before You",
			"    Your relatively hot girlfriend. She's a redhead." \
			" She looks ill."
		],
		"choices": [
			("Qdormant|MQ00", "dialg|patience_cabin-1", "''Need Anything?''"),
			(["Qactive|MQ00", "Ihas|hpot0"], "dialg|patience_cabin-3", "''I have it.''", ["Qcomplete|MQ00", "I-|hpot0"]),
			(None, "leave|", "Leave"),
		],
	},
	"tavern_innkeeper-0": {
		"text": [ "The Innkeeper",
			"    "
		],
		"choices": [
			("Qstage1|MQ01", "dialg|MQ01-0", "Vengeance"),
			(["Qstage2|MQ01", "Ihas|hpot1"], "dialg|MQ01-2", "''I have the extract.''", "Qcomplete|MQ01"),
			(None, "leave|", "Leave"),
		],
	},
	# MQ00
	"patience_cabin-1": {
		"text": [ "Illness In Patience",
			"    ''I need a tonic.''"
		],
		"choices": [
			(None, "dialg|patience_cabin-2", "Accept", "Qstart|MQ00"),
			(None, "leave|", "Decline"),
		],
	},
	"patience_cabin-2": {
		"text": [ "Illness In Patience",
			"    ''Thanks. Please Hurry. I don't feel so good.''"
		],
		"choices": [
			(None, "leave|", "Leave"),
		],
	},
	"patience_cabin-3": {
		"text": [ "Illness In Patience",
			"    Before you could hand her the tonic, bandits pour out of the woods in all directions." \
			" You do what you can as one of them charges at you."
		],
		"choices": [
			(None, "battl|bandit0=MQ00battle0::MQ00battle0::MQ00battle0", "Fight"),  # WTF ''!'' caused the ERROR
		],
	},
	"MQ00battle0": {
		"text": [ "The Battle",
			"    You got knocked out eventually. You survived the attack."
		],
		"choices": [
			(None, "dialg|MQ00battle0-end", "Vengeance", "Qstart|MQ01"),
		],
	},
	"MQ00battle0-end": {
		"text": [ "The Battle",
			"    Vengeance!!"
		],
		"choices": [
			(None, "place|cabin*332,340", "Leave"),
		],
	},
	# MQ01
	"MQ01-0": {
		"text": [ "Gathering The Pieces",
			"    Recovery, Basic Information."
		],
		"choices": [
			(None, "dialg|MQ01-1", "Continue"),
		],
	},
	"MQ01-1": {
		"text": [ "Gathering The Pieces",
			"    Mute Boy, Location Of Healing Item."
		],
		"choices": [
			(None, "place|village*312,320", "Leave", "Qstage+|MQ01"),
		],
	},
	"MQ01-2": {
		"text": [ "Gathering The Pieces",
			"    Cinder Extract Recovered. Mute Boy Recovering."
		],
		"choices": [
			(None, "dialg|MQ01-3", "Continue", "Qstart|MQ02"),  # auto start MQ02
		],
	},
	"MQ01-3": {
		"text": [ "Gathering The Pieces",
			"    Mute boy gives information"
		],
		"choices": [
			(None, "leave|", "Leave"),
		],
	},
	# MQ02
	"MQ02-1": {
		"text": [ "Descending The Void",
			"Lookout near cave entrance. What do you do?"
		],
		"choices": [
			(None, "battl|cave_lookout=MQ02-2::test::test", "Fight"),
			(None, "leave|", "Leave"),
		],
	},
	"MQ02-2": {
		"text": [ "Descending The Void",
			"The Lookout is dead."
		],
		"choices": [
			(None, "place|cave_inner", "Continue", "Qstage+|MQ02"),
		],
	},
	"MQ02-3": {
		"text": [ "Descending The Void",
			""
		],
		"choices": [()],
	},
	
	
	"patience_cabin-descr": {
		"text": [ "",
			"    Your relatively hot girlfriend. She's a redhead."
		],
		"choices": [
			("Qdormant|squest0.0", "dialg|patience_cabin-drmnt-squest0.0", "''Need anything?''"),
			(["Qactive|squest0.0", "Ihas|hpot0"], "dialg|patience_cabin-cmplt-squest0.0", "''I have it.''", ["Qcomplete|squest0.0", "I-|hpot0"]),
			(None, "leave|", "Leave"),
		],
	},
	"patience_cabin-drmnt-squest0.0": {
		"text": [ "",
			"Hey, buy me a tonic from the village."
		],
		"choices": [
			(None, "dialg|patience_cabin-thanks", "''Consider it done.''", "Qstart|squest0.0"),
			(None, "leave|", "''No.''"),
		],
	},
	"patience_cabin-cmplt-squest0.0": {
		"text": [ "",
			"THANKS, attack starts"
		],
		"choices": [
			(None, "battl|bandit0=q-The_Aftermath::q-The_Aftermath::q-The_Aftermath", "Fight"),
		],
	},
	"patience_cabin-thanks": {
		"text": [ "",
			"Thanks!"
		],
		"choices": [(None, "leave|", "Leave"),],
	},
	
	"village-empty_house": {
		"text": [ "The Empty House",
			"    The door is locked.\n"
		],
		"choices": [
			("G+|9", "dialg|village-empty_house1", "Try to Unlock", "Qstart|mq01"),
			("G+|9", "leave|", "Leave"),
		],
	},
	"village-empty_house1": {
		"text": [ "The Empty House",
			"    The door is locked.\n"
		],
		"choices": [
			("G+|9", "leave|", "Leave"),
		],
	},
	"mq00a": { 
		"text": [ "A Want For A Book",
			"    ''I want a book. Any kind of book will do. I don't have mu" \
			"ch with me but I'll give you something in return.'' The innkee" \
			"per said without looking at you. \n" \
			"    She puts the glass on the counter and rubs the hands with " \
			"a table cloth. You glance at her lean figure. She looks at you" \
			". \n" \
			"    ''Well? Will you bring me a book or not?'' The woman sighe" \
			"d. She is staring at you. What will you say? \n"
		],
		"bg_image": "place_htown",
		"image": "dtxt_image_innkeeper",
		"choices": [
			("''I accept''", "dlg|ht00", "", "Qmq00|+A"),
			("''I am indisposed''", "dlg|ht00"),
		],
	},
	"mq00b": { 
		"text": [ "A Want For A Book",
			"    ''Thhannk you.'' The woman said with a smile. It was one o" \
			"f the fakest things that you have seen in your entire life. It" \
			" made her face a bit painful to look at. \n" \
			"    Your thoughts were interrupted as coins battered the count" \
			"er. You sense that you are being watched. Something tells you " \
			"not to turn around but you do it anyway. There was nothing but" \
			" it was quick, too quick. Not enough time to judge. The ground" \
			"shakes from several footsteps behind you. Nothing there. \n"
			"    You grab the reward as fast as you could. The innkeeper re" \
			"sumes cleaning the endless pile of plates, her back facing you" \
			". You faintly smile and head back to your table. \n"
		],
		"bg_image": "place_htown",
		"image": "dtxt_image_innkeeper",
		"choices": [  # give reward?
			("Head back to your table", "dlg|ht00"),
		],
	},
	"mq01a": { 
		"text": [ "A Need For A Book",
			"    ''I want a book. Any kind of book will do. I don't have mu" \
			"ch with me but I'll give you something in return.'' The innkee" \
			"per said without looking at you. \n" \
			"    She puts the glass on the counter and rubs the hands with " \
			"a table cloth. You glance at her lean figure. She looks at you" \
			". \n" \
			"    ''Well? Will you bring me a book or not?'' The woman sighe" \
			"d. She is staring at you. What will you say? \n"
		],
		"bg_image": "place_htown",
		"image": "dtxt_image_innkeeper",
		"choices": [
			("''I accept''", "dlg|ht00", "", "Qmq01|+A"),
			("''I am indisposed''", "dlg|ht00"),
		],
	},
	"mq01b": { 
		"text": [ "A Need For A Book",
			"    ''Thhannk you.'' The woman said with a smile. It was one o" \
			"f the fakest things that you have seen in your entire life. It" \
			" made her face a bit painful to look at. \n" \
			"    Your thoughts were interrupted as coins battered the count" \
			"er. You sense that you are being watched. Something tells you " \
			"not to turn around but you do it anyway. There was nothing but" \
			" it was quick, too quick. Not enough time to judge. The ground" \
			"shakes from several footsteps behind you. Nothing there. \n"
			"    You grab the reward as fast as you could. The innkeeper re" \
			"sumes cleaning the endless pile of plates, her back facing you" \
			". You faintly smile and head back to your table. \n"
		],
		"bg_image": "place_htown",
		"image": "dtxt_image_innkeeper",
		"choices": [  # give reward?
			("Head back to your table", "dlg|ht00"),
		],
	},
	"A00": {
		"text": [ "Memories",
			""
		],
		"bg_image": None,
		"image": None,
		"choices": [
			("The Recent Past", "dlg|A01"),
			("Close Memories", "ext|"),
		],
	},
	"A01": {
		"text": [ "The Recent Past",
			"    You woke up wounded and with no memory of past events. An " \
			"attractive young widow nursed you back to health within weeks." \
			" She gave you a place to stay until you could remember what ha" \
			"ppend. You develop a liking to the woman. She felt the same. M" \
			"onths go by and you remember only fragments of your past life." \
			" The ship, a storm, and then a wizard and then death. Your wif" \
			"e hugs you from behind, ending your trail of thoughts. She sme" \
			"lls of lavender, her favorite flower. Your first memory of the" \
			" scent of that purple flower was at that faithful day. \n" \
			"    You where crawling and leaving a trail of blood. Through t" \
			"he cobbled path, you looked at the door in front of you. Screa" \
			"ming wildly as heavy rain battered your mutilated body. At tha" \
			"t moment, the door opened. A woman with red hair in modest clo" \
			"thing ran and dropped to the ground, kneeling womanly. With so" \
			"me effort, she carefully rested your head on her legs. Time sl" \
			"owed down and everything was silent. The shouts of nature were" \
			" muted and in that very moment, you gazed deeply into each oth" \
			"er's eyes. \n" \
		],
		"bg_image": None,
		"image": None,
		"choices": [
			("Continue...", "dlg|A02"),
		],
	},
	"A02": {
		"text": [ "The Recent Past",
			"    She giggled as you pulled your hand back from the side of " \
			"her face. You are in total happiness. All that happened before" \
			" didn't matter anymore. Everything changed when your wife took" \
			" a sword through the back of her spine, as raging flames burne" \
			"d down your modest home. Your attacker bashes you with a mace." \
			" You fall to the ground. His fellows carried their loot as he " \
			"kicked your stomach several times. The malevolent man only sto" \
			"pped when blood started squirting out of your mouth in waves. " \
			"He looked proudly at his handiwork for a final time before joi" \
			"ning the others. You painfully turned your body around, facing" \
			" your dying wife. You never knew her name. One last gaze. The " \
			"light in her precious eyes disappeared forever. Vengeance.\n"
		],
		"bg_image": None,
		"image": None,
		"choices": [
			("Memories", "dlg|A00"),
			("Previous", "dlg|A01"),
			("Close Memories", "ext|"),
		],
	},
	"ht00": {  # htown tavern
		"text": [ "The Tavern", 
			"    The tavern is almost deserted once more. You walk and take" \
			" a seat as stale air wrinkles your nose. You hear voices shout" \
			"ing at your left ear in whispers. You see a fair maiden sittin" \
			"g on a table near the stage. She listens to a bard while sippi" \
			"ng a cup of wine. Sharp voices are heard outside the walls. Th" \
			"ey sting. The usual tavern girl approaches. \n" \
			"    You tell her off and quickly resume your thoughts. You are" \
			" not hungry. You could look around some more. The innkeeper mi" \
			"ght be able to give you some work, or information. A few patro" \
			"ns might be available for a simple conversation. \n"
		],
		"bg_image": "place_htown",
		"image": "dtxt_image_tavern",
		# choices should add additional text
		"choices": [  # we will add complexity in the future
			("Chat with the innkeeper", "dlg|ht01"),
			("Talk to the pale maiden", None),
			("Go outside", "plc|hilltown", "", (460, 270)),  # exit coords
		],
		#"place": "hilltown",
	},
	"ht01": {
		"text": [ "The Innkeeper",
			"    The Innkeeper is wiping another glass taken from a huge pi" \
			"le of mugs and dishes. She holds it close to her face and insp" \
			"ects it thoroughly. You see the woman's face as you approach t" \
			"he counter. She stops cleaning and faces you. \n" \
			"    ''What is this place? What can you tell me about this town" \
			"?'' you asked. \n" \
			"    ''It is a nice place.'' said the frail woman. \n"
		],
		"bg_image": "place_htown",
		"image": "dtxt_image_innkeeper",
		"choices": [
			("''You want something?''", "dlg|mq00a", "Qmq00|0"),
			("''I have the book''", "dlg|mq00b", "Qmq00|2", "Qmq00|+R"),
			("''You need something?''", "dlg|mq01a", "Qmq01|0"),
			("''I have the books''", "dlg|mq01b", "Qmq01|2", "Qmq01|+R"),
			("Head back to your table", "dlg|ht00"),
			("''Show me what you got''", "str|innkeeper", "Qmq00|3", ""),
			("Go outside", "plc|hilltown", "", (460, 270)),
		],
		#"place": "hilltown",
	},
	"ht02": {
		"text": [ "Herald",
			"    ''Oi! You theree! Fak off, I'm busy preaachingggg my sermo" \
			"n to my followers! You are disturbing us! Begone!!'' barked th" \
			"e local. \n" \
			"    You look around. You are the only person listening to the " \
			"man. Pieces of dirt fly towards your legs. The preacher adjust" \
			"s his robe, revealing tattered shoes. \n" \
			"    He spits at you but it pathetically falls on his clothes. " \
			"The high priest clutches his legs and vomits to the ground. A " \
			"full minute of coughing passes. He glares at you, as if expect" \
			"ing you to do something. \n"
		],
		"bg_image": "place_htown",
		"image": "dtxt_image_herald",
		"choices": [
			("Hit him in the face", "btl|bandit0=ht00::ht00::ht00"),
			("Lootbox", "box|hausbox"),
			("Leave", "plc|hilltown", "", (230, 280)),
		],
		#"place": "hilltown",
	},
}