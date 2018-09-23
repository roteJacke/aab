import copy
import datetime as dt
import game_data as gd
import math
import os
import random as rd
import tkinter as tk
import winsound as ws



class Battle:
	def __init__(self, world, canvas, player, enemy, extract_func, *args, **kwargs):
		self.parent = world.parent
		self.world = world
		self.cn = canvas
		self.extract = extract_func
		self.rsc = self.world.rsc
		self.items = self.world.items
		self.player = player
		self.enemy = enemy
		
		#self.load_resources()
		#self.set_playerstats()
		self.battle(self.player, self.enemy)
		
		self.game_stat = "ongoing"
		self.game_valus = "10/10"
		
	
	def load_resources(self, *args):
		'''
		self.attacks = {
			"Slash": {
				"Damage": 2.5,
				"AP cost": 1.0
			},
			"Chop": {
				"Damage": 4,
				"AP cost": 1.5
			},
			"Shank": {
				"Damage": 0.75,
				"AP cost": 1
			}
		}
		'''
		pass

		
	def place_image(self, x, y, rsc, tags, anchor="west", *args):	
		self.cn.create_image(x, y, anchor=anchor, image=self.rsc[rsc],
			tags=tags)
	
	
	def battle(self, player, enemy, *args):
		# STILL CHANGING VALUE OF MAIN ACTORS?!
		# new battle stats
		self.pbs = {
			"attack": player["stats"][4],
			"defense": player["stats"][3],
			"dodge": player["stats"][2],
			"HC": player["stats"][6],
			"IA": player["stats"][7],
			"CC": player["stats"][8],
			"Cd": player["stats"][9],
		}
		self.ebs = {
			"attack": enemy["stats"][4],
			"defense": enemy["stats"][3],
			"dodge": enemy["stats"][2],
			"HC": enemy["stats"][6],
			"IA": enemy["stats"][7],
			"CC": enemy["stats"][8],
			"Cd": enemy["stats"][9],
		}		
		# init player values
		self.pName = player["name"] 
		self.pHP = player["stats"][0]  # hp_now/hp_max
		#self.pAttk = self.actors[player]["Attack"]  # key for self.attacks
		self.pAttk = "Traveler"  # name only needed
		self.pDAMAGE = player["stats"][4]  # damage already calculated
		# below did not change the dictionary
		ptonic_num = 0
		for i in player["inventory"]:
			if self.items[i]["type"] == "potion":
				ptonic_num += 1
		self.pTonics = ptonic_num  # num. of tonics
		self.pTonics_max = ptonic_num * 1
		self.pAP = player["stats"][1]  # Action Points
		self.pAP_max = player["stats"][1] * 1
		self.pIMG = player["image"]  # battle image
		self.pAvt = player["avatar"]  # battle avatar
		# init enemy values
		self.eName = enemy["name"]
		self.eHP = enemy["stats"][0]  # hp_now/hp_max
		self.eAttk = "Bandit"  # key for self.attacks
		self.eDAMAGE = enemy["stats"][4]
		etonic_num = 0
		for i in enemy["inventory"]:
			if self.items[i]["type"] == "potion":
				etonic_num += 1
		self.eTonics = etonic_num  # num. of tonics
		self.eTonics_max = etonic_num * 1
		self.eAP = enemy["stats"][1]  # Action Points
		self.eAP_max = enemy["stats"][1] * 1
		self.eIMG = enemy["image"]  # battle image
		self.eAvt = enemy["avatar"]  # battle avatar
		
		ws.PlaySound('Volatile_Reaction.wav', ws.SND_ASYNC)
		
		# init game stats
		self.turn_holder = "Player"
		self.round_num = 1
		self.attking = None  # animation
		# roof.after animation
		self.pMOVE = None
		self.eMOVE = None
		self.pdMOVE = None
		self.edMOVE = None
		self.pDODGED = False
		self.eDODGED = False
		self.ani_effect = None  # animation effect
		
		# UI MAKER
		def reset_imgs(*args):
			# reset player and enemy images to original position
			self.cn.delete(self.pIMG, self.eIMG)
			#create_image(90, 140, self.pIMG)  # player img
			#create_image(560, 140, self.eIMG)  # enemy img
			#create_image(115, 140, self.pIMG)  # player img
			#create_image(535, 140, self.eIMG)  # enemy img
			create_image(140, 140, self.pIMG)  # player img
			create_image(530, 140, self.eIMG)  # enemy img
		
		
		def create_image(x, y, rsc, tagn=None, tagOverride=None, anchor=tk.NW):
			t1, t2, tagn = "ui", "battle_ui", tagn if tagn != None else rsc
			if tagOverride is not None:
				ntags = tagOverride
			else:
				ntags = (t1, t2, tagn)
			self.cn.create_image(x, y, anchor=anchor, image=self.rsc[rsc], 
				tags=ntags)
				
		
		def create_text(x, y, txt, tagn=None, anchor="nw", font=("Helvetica",
				12, "bold"), fill="black"):
			#t1, t2 = "ui", "battle_ui"
			t1, t2, tagn = "ui", "battle_ui", tagn if tagn != None else txt
			self.cn.create_text(x, y, text=txt, tags=(t1, t2, tagn), font=font,
				anchor=anchor, fill=fill)
				
		
		def create_rect(x1, y1, x2, y2, tagn, fill, tagOverride=None, width=0):
			t1, t2 = "ui", "battle_ui"
			ntag = (t1, t2, tagn)
			if tagOverride is not None:
				ntag = tagOverride
			self.cn.create_rectangle(x1, y1, x2, y2, tags=ntag,
				fill=fill, width=width)
				
				
		def pznt(num_list):
			# Takes a list of 2 numbers
			num_list = [float(n) for n in num_list]
			return str(int(num_list[0] / num_list[1] * 100))
			
		
		# check drawing for info, x += 20, y += 50
		#create_image(0, 0, "aBg1")	# bg to block world ui
		create_image(20, 50, "aCbg1")  # bg for battle ui
		create_image(30, 85, "aFbg1")  # fight bg
		create_image(30, 60, "aCtui1")  # top ui
		create_image(30, 385, "aClui1")  # lower ui
		#btn_img = ["aSlash0", "aTonic0", "aFlee0"]
		btn_img = ["aBtn0_Slash-0", "aBtn0_Tonic-0", "aBtn0_Flee-0"]
		for i in range(3): # create the buttons
			create_image(300+(i*70), 410, btn_img[i], "btn{}".format(i))
		create_image(140, 410, "aCd1", "bPdl1")  # player stats
		create_image(510, 410, "aCd1", "bEdl1")  # moved position
		#create_image(90, 140, self.pIMG)  # player img
		#create_image(560, 140, self.eIMG)  # enemy img
		#create_image(115, 140, self.pIMG)  # player img
		create_image(140, 140, self.pIMG)  # player img
		#create_image(535, 140, self.eIMG)  # enemy img
		create_image(530, 140, self.eIMG)  # enemy img
		create_image(40, 410, self.pAvt)  # player avatar
		create_image(660, 410, self.eAvt)  # moved position
		create_text(400, 73, "Round {}".format(self.round_num), "round_num", anchor="center")  # self.hcolor
		create_text(400, 98, "{}'s Turn".format(self.turn_holder), "turn_holder", anchor="center")
		
		self.hheight = 20  # height of HP bar
		self.rheight = 15  # height of AP bar
		self.hcolor = "black"  # color of text on hpBar
		self.hpbgc = "light green"  # color of the hp bg box
		self.hstart = 482  # height of stats of hp bar
		
		# Player stats
		#_pAttk = "{}, {} dmg".format(self.pAttk, self.attacks[self.pAttk]["Damage"])
		#_pAttk = "{}, {} dmg".format(self.pAttk, self.pDAMAGE)
		_pAttk = "ATK: {},  DEF: {}".format(
			self.pbs["attack"],
			self.pbs["defense"],
		)
		_pTonics = "{} Tonics".format(self.pTonics)
		_pHP = "{}/{}".format(self.pHP[0], self.pHP[1])
		_pHPpz = "{}%".format(pznt(self.pHP))
		_pAP = "AP: {}".format(self.pAP)
		create_text(144, 415, self.pName, font=("Helvetica",
				12, "bold"), fill="black")
		create_text(144, 440, _pAttk, "pStats_Attack", font=("Helvetica",
				10, "bold"), fill="black")
		create_text(144, 455, _pTonics, "pStats_Tonics", font=("Helvetica",
				10, "bold"), fill="black")
		# HP & AP bars           # reduce by 2p(1side each) to fit screen?
		create_rect(141, 514-self.rheight-self.hheight, 289, 514-self.rheight, "pHP_box", self.hpbgc, width=1)
		create_rect(141, 514-self.rheight-self.hheight, 289, 514-self.rheight, "pHP_color", "white", width=1)
		create_rect(141, 514-self.rheight, 289, 514, "pAP_box", self.hpbgc, width=1)
		create_rect(141, 514-self.rheight, 289, 514, "pAP_color", "light yellow", width=1)
		# Vertical HP bar  - removed
		# HP & AP stats
		create_text(142, self.hstart, _pHP, "pStats_HPcount", fill=self.hcolor)
		create_text(288, self.hstart, _pHPpz, "pStats_HP%", anchor="ne", fill=self.hcolor)
		create_text(142, 500, _pAP, "pStats_AP", font=("Helvetica", 10, "bold"))  # 287, 465 , anchor="ne"
		
		# Enemy stats
		#_eAttk = "{}, {} dmg".format(self.eAttk, self.eDAMAGE)
		_eAttk = "ATK: {},  DEF: {}".format(
			self.ebs["attack"],
			self.ebs["defense"],
		)
		_eTonics = "{} Tonics".format(self.eTonics)
		_eHP = "{}/{}".format(self.eHP[0], self.eHP[1])
		_eHPpz = "{}%".format(pznt(self.eHP))
		_eAP = "AP: {}".format(self.eAP)
		create_text(656, 415, self.eName, anchor="ne", fill="black")  # 512
		create_text(656, 440, _eAttk, "eStats_Attack", anchor="ne", font=("Helvetica",
				10, "bold"), fill="black")
		create_text(656, 455, _eTonics, "eStats_Tonics", anchor="ne", font=("Helvetica",
				10, "bold"), fill="black")
		# HP & AP bars           # reduce by 2p(1side each) to fit screen?
		create_rect(511, 514-self.rheight-self.hheight, 659, 514, "eHP_box", self.hpbgc, width=1)
		create_rect(511, 514-self.rheight-self.hheight, 659, 514, "eHP_color", "white", width=1)
		create_rect(511, 514-self.rheight, 659, 514, "eAP_box", self.hpbgc, width=1)
		create_rect(511, 514-self.rheight, 659, 514, "eAP_color", "light yellow", width=1)
		# Vertical HP bar  - removed
		# HP & AP stats
		#create_text(513, 465, _eAP, "eStats_AP")
		create_text(512, self.hstart, _eHPpz, "eStats_HP%", fill=self.hcolor)
		create_text(658, self.hstart, _eHP, "eStats_HPcount", anchor="ne", fill=self.hcolor)
		create_text(658, 500, _eAP, "eStats_AP", anchor="ne", font=("Helvetica", 10, "bold"))  # 513, 465 , anchor="ne"
		
		
		# BATTLE FUNCTIONS
		def display_effect(mode="Damage", dmg_num=0, *args):
			'''mode:
			Damage :: displays attack damage from dmg_num.
			Tonic :: displays tonic icon.
			Dodge :: displays dodge icon.
			Block :: failed to flee as Player.
			Crit :: critical.
			'''
			x, y = 660, 250
			if self.turn_holder == "Enemy":  # effect being applied to.
				x, y = 75, 250
			if self.ani_effect is not None:
				self.ani_effect = None
				self.cn.delete("battle_effect")
			xname_text = None
			xname = ""  # rsc img name or text
			if mode == "Damage":
				xname = str(dmg_num)
				xname_text = True
			elif mode == "Tonic":
				# reverse
				if self.turn_holder == "Player":
					x, y = 75, 250
				if self.turn_holder == "Enemy":
					x, y = 660, 250
				xname = "aTonic-0"
				xname_text = False
			elif mode == "Block":
				x, y = 75, 250
				xname = "aBlockFail-0"
				xname_text = False
			elif mode == "Crit":
				xname = "aCrit-0"
				xname_text = False
			else:
				xname = "aDodge-0"
				xname_text = False
			if xname_text:
				create_text(x, y, xname, "battle_effect", font=("Helvetica", 24, "bold"))
			else:
				create_image(x, y, xname, "battle_effect")
			animate_effect()
			
		
		def event_txt(text="", mode="display", msec=1000, *args):
			if mode == "display":
				create_image(400, 225, "aEtxt1", "event_txt", anchor="center")
				create_text(400, 225, text, "event_txt", anchor="center", font=("Helvetica",
					42, "bold"), fill="black")
				self.cn.after(msec, lambda: event_txt(mode="delete"))
			else:
				self.cn.delete("event_txt")
			
		
		def animate_effect(num=7, *args):
			if num > 0:
				self.cn.move("battle_effect", 0, -15)
				self.ani_effect = self.parent.after(25, lambda: animate_effect(num-1))
			else:
				self.parent.after(250, lambda: self.cn.delete("battle_effect"))
			
		
		def use_tonic(*args):
			tonic_heal = 10
			if self.turn_holder == "Player" and self.pHP[0] > 0:
				if self.pTonics > 0 and self.pHP[0] < self.pHP[1] and self.pAP >= 1:
					block_btns()  # prevent bugs due to button spam
					new_pHP = self.pHP[0] + tonic_heal
					new_pHP = new_pHP if new_pHP <= self.pHP[1] else self.pHP[1]
					self.pHP[0] = new_pHP  # apply to player 
					self.pTonics -= 1
					self.pAP -= 1  # end attack
					display_effect("Tonic")
					for i in range(len(self.player["inventory"])):
						if self.items[self.player["inventory"][i]]["type"] == "potion":
							del self.player["inventory"][i]
							break
					end_attack()
			elif self.turn_holder == "Enemy" and self.eHP[0] > 0:
				if self.eTonics > 0 and self.eHP[0] < self.eHP[1] and self.eAP >= 1:
					new_eHP = self.eHP[0] + tonic_heal
					new_eHP = new_eHP if new_eHP <= self.eHP[1] else self.eHP[1]
					self.eHP[0] = new_eHP  # apply to enemy 
					self.eTonics -= 1
					self.eAP -= 1  # end attack
					#self.parent.after(500, end_attack)  # delay causes movement error
					display_effect("Tonic")
					end_attack()
			update_display()
			
		
		def update_round(*args):
			self.cn.itemconfigure("round_num", 
				text="Round {}".format(self.round_num))
		
		
		def flee_battle(*args):
			if self.turn_holder == "Player" and self.pHP[0] > 0:
				block_btns()
				roll = rd.randint(1, 10)
				if roll <= 5:  # 50% chance of succeeding
					self.pAP = 0
					display_effect("Block")
					self.parent.after(250, lambda: event_txt("Fleeing!", msec=2500))
					update_display()
					self.turn_holder = "Flee"
					self.cn.itemconfigure("turn_holder", tag="battle_result")
					self.cn.itemconfigure("battle_result", text="Flee-2/10-1-20")
					self.cn.tag_lower("battle_result")  # hide text from view
					self.parent.after(1500, exit_battle)
				else:
					self.pAP = 0
					display_effect("Block")
					self.parent.after(250, lambda: event_txt("Failed to flee!", msec=750))
					update_display()
					self.parent.after(1250, lambda: end_attack())
					
		
		def exit_battle(*args):
			#self.cn.delete("battle_ui")
			# changes value of self.actors, how/why? how do we avoid this
			self.eHP[0] = self.eHP[1]  # reset enemy HP
			self.round_num = 1
			ws.PlaySound(None, ws.SND_PURGE)
			self.extract() 
		
		
		def attack(*args):
			# spamming not stopping
			if self.attking is None:
				###print "attacking"
				self.attcking = True
				# Cancel if there is movement
				if self.pMOVE is not None:
					self.parent.after_cancel(self.pMOVE)
				if self.eMOVE is not None:
					self.parent.after_cancel(self.eMOVE)
				reset_imgs()  # put img in original positions
				block_btns()
				if self.turn_holder == "Enemy":  # make enemy use tonic instead
					if self.eHP[0]/float(self.eHP[1]) <= 0.25 and self.eTonics > 0 and self.eAP >= 1:
						use_tonic()
						#end_attack()
					else:
						# 500 may cause program to crash
						# remove AP from Enemy
						self.eAP -= 1
						#self.eAP = self.eAP if self.eAP >= 0 else 0
						#self.parent.after(100, animate_attack)
						if self.eAP >= 0:
							self.parent.after(100, animate_attack)
						else:
							self.eAP = 0  # reset
							end_attack()
				else:
					#animate_attack()
					#if self.turn_holder == "Player" and self.pHP[0] > 0:
					self.pAP -= 1
					#self.pAP = self.pAP if self.pAP >= 0 else 0
					if self.pAP >= 0:
						self.parent.after(100, animate_attack)
					else:
						self.pAP = 0
						end_attack()
				update_display()
					
		
		def block_btns(block=True):
			if block is True:
				for i in range(3): # create the buttons
					if self.turn_holder == "Player":
						create_image(300+(i*70), 410, "aBtn0_Wait-0", "BLOCK_btn{}".format(i))
					else:
						create_image(300+(i*70), 410, "aBtn0_EnemyTurn-0", "BLOCK_btn{}".format(i))
			elif block is False:
				self.cn.delete("BLOCK_btn0", "BLOCK_btn1", "BLOCK_btn2")
		
		
		def animate_attack(num=20, *args):
			if self.turn_holder == "Player":
				#self.attcking = True
				if num > 0:
					val = -35
					#interval = 17
					interval = 25
					if num == 11:
						x = rd.uniform(0.0, 100.0)
						#if x < 1.5:  # 15% dodge chance
						if x < (self.ebs["dodge"] / 2.0):  # 15% dodge chance
							self.eDODGED = True
							display_effect("Dodge")
						else:
							x1 = rd.uniform(0.0, 100.0)
							if x1 < self.pbs["HC"]:
								apply_dmg()
							else:
								self.eDODGED = True
								display_effect("Dodge")
					if num >= 11:
						val *= -1
					self.cn.move(self.pIMG, val, 0)
					# animate if dodged attack
					coords = 15  # x value
					dcoords = 0  # y value for dodge
					if self.eDODGED:  # values change each time function is called
					#	n = rd.randint(0, 1)
						dcoords = 10  # if n == 0 else -10
					if num <= 11 and num >= 9:
						self.cn.move(self.eIMG, coords, dcoords)
					elif num < 9 and num >= 6:
						self.cn.move(self.eIMG, -coords, -dcoords)
					self.pMOVE = self.parent.after(interval, lambda: animate_attack(num-1))
				elif num == 0:
					end_attack()
					
			elif self.turn_holder == "Enemy":
				#self.attcking = True
				if num > 0:
					val = 35
					#interval = 17
					interval = 25
					if num == 11:
						x = rd.uniform(0.0, 100.0)
						#if x < 2.5:  # 25% dodge chance
						if x < (self.pbs["dodge"] / 2):  # 25% dodge chance
							self.pDODGED = True
							display_effect("Dodge")
						else:
							x1 = rd.uniform(0.0, 100.0)
							if x1 < self.ebs["HC"]:
								apply_dmg()
							else:
								self.pDODGED = True
								display_effect("Dodge")
					if num >= 11:
						val *= -1
					self.cn.move(self.eIMG, val, 0)
					coords = 15
					dcoords = 0
					if self.pDODGED:
						dcoords = 10
					if num <= 11 and num >= 9:
						self.cn.move(self.pIMG, -coords, dcoords)
					elif num < 9 and num >= 6:
						self.cn.move(self.pIMG, coords, -dcoords)
					self.eMOVE = self.parent.after(interval, lambda: animate_attack(num-1))
				elif num == 0:
					end_attack()
		
		
		def end_attack():
			###print "function called"
			# did not stop from spamming that button
			self.attcking = None
			#apply_dmg()
			if self.turn_holder == "Player":
				if self.eHP[0] == 0:
					###print "Game has been won!"
					self.turn_holder = "Victory"
					self.cn.itemconfigure("turn_holder", tag="battle_result")
					self.cn.itemconfigure("battle_result", text="Victory-10/10-0-50")
					self.cn.tag_lower("battle_result")
					block_btns()
					self.parent.after(250, lambda: event_txt("Victory", msec=5000))
					self.parent.after(2700, exit_battle)
				else:
					if self.pAP <= 0 or (self.pAP - self.attacks[self.pAttk]["AP cost"] < 0 and (self.pAP < 1 or self.pTonics <= 0)):
						self.eAP = self.eAP_max
						self.pAP = 0
						###print "Round {}".format(self.round_num)
						self.turn_holder = "Enemy"
						isecs = 250
						self.parent.after(isecs, lambda: self.cn.itemconfigure("turn_holder", font=("Helvetica", 34, "bold")))
						self.parent.after(isecs, lambda: self.cn.itemconfigure("turn_holder", text="{}'s Turn".format(self.turn_holder)))
						# Moved function, since next round always starts after player's AP = 0
						msecs = 750
						self.parent.after(isecs + msecs, lambda: self.cn.itemconfigure("turn_holder", font=("Helvetica",
							12, "bold")))
						self.parent.after(isecs + msecs, update_round) 
						#self.parent.after(isecs + msecs, lambda: self.cn.move("turn_holder", 0, -100))
						self.parent.after(250, attack)
					else:
						self.parent.after(250, lambda: block_btns(False))
						#if self.pAP - self.attacks[self.pAttk]["AP cost"] < 1
			elif self.turn_holder == "Enemy":
				if self.pHP[0] == 0:
					###print "Game Over!"
					self.turn_holder = "Defeat"
					self.cn.itemconfigure("turn_holder", tag="battle_result")
					self.cn.itemconfigure("battle_result", text="Defeat-0/10-2-15")
					self.cn.tag_lower("battle_result")
					block_btns()
					self.parent.after(250, lambda: event_txt("Defeat", msec=5000))
					self.parent.after(2700, exit_battle)
				else:
					if self.eAP <= 0:
						self.pAP = self.pAP_max
						self.turn_holder = "Player"
						self.parent.after(250, lambda: block_btns(False))
						self.round_num += 1
						# Moved function, so round will end after enemy attack.
						# wait a bit
						isecs = 250
						#self.parent.after(isecs, lambda: self.cn.itemconfigure("round_num", font=("Helvetica", 34, "bold")))
						self.parent.after(isecs, lambda: self.cn.itemconfigure("round_num", text="[Round {}]".format(self.round_num)))
						#self.parent.after(isecs, lambda: self.cn.move("round_num", 0, 125))
						self.parent.after(isecs, lambda: self.cn.itemconfigure("turn_holder", font=("Helvetica", 34, "bold")))
						self.parent.after(isecs, lambda: self.cn.itemconfigure("turn_holder", text="{}'s Turn".format(self.turn_holder)))
						# Moved function, since next round always starts after player's AP = 0
						msecs = 750
						self.parent.after(isecs + msecs, lambda: self.cn.itemconfigure("round_num", font=("Helvetica",
							12, "bold")))
						self.parent.after(isecs + msecs, lambda: self.cn.itemconfigure("turn_holder", font=("Helvetica",
							12, "bold")))
						self.parent.after(isecs + msecs, update_round) 
						#self.parent.after(isecs + msecs, lambda: self.cn.move("round_num", 0, -125))
					else:
						self.parent.after(250, attack)
			
			update_display()
			#self.cn.itemconfigure("turn_holder", text=self.turn_holder)
			
		
		def apply_dmg(*args):
			if self.turn_holder == "Player" and self.pHP[0] > 0:
				'''
				self.pAP -= self.attacks[self.pAttk]["AP cost"]
				self.pAP = self.pAP if self.pAP >= 0 else 0
				'''
				pDMG = self.pDAMAGE
				crit = False
				'''
				if self.pAttk == "Shank":
					# add crit chance
					x = rd.uniform(1.0, 10.0)
					if x <= 1.5:  # 15% crit chance
						pDMG *= 2
						##print "Crit! Dealt {} Damage.".format(pDMG)
						crit = True
				'''
				x = rd.uniform(0.0, 100.0)
				if x < self.pbs["CC"]:
					pDMG += (pDMG * (self.pbs["Cd"] / 100.0))
					crit = True
				# apply armor
				pDMG -= (self.ebs["defense"] - (self.ebs["defense"] * (self.pbs["IA"] / 100.0)))
				pDMG = round(pDMG, 1)
				pDMG = 0 if pDMG < 0 else pDMG
				new_eHP = self.eHP[0] - pDMG
				new_eHP = new_eHP if new_eHP >= 0 else 0
				self.eHP[0] = round(new_eHP, 1)  # apply to enemy 
				self.eDODGED = False
				if crit:
					#display_effect("Crit")
					pDMG = "[{}]".format(str(pDMG))
					display_effect("Damage", pDMG)
				else:
					display_effect("Damage", pDMG)
				update_display()  # update info
			elif self.turn_holder == "Enemy" and self.eHP[0] > 0:
				#self.eAP -= self.attacks[self.eAttk]["AP cost"]
				#self.eAP = self.eAP if self.eAP >= 0 else 0
				eDMG = self.eDAMAGE
				crit = False
				x1 = rd.uniform(0.0, 100.0)
				if x1 < self.ebs["CC"]:
					eDMG += (eDMG * (self.ebs["Cd"] / 100.0))
					crit = True
				eDMG -= (self.pbs["defense"] - (self.pbs["defense"] * (self.ebs["IA"] / 100.0)))
				eDMG = round(eDMG, 1)
				eDMG = 0 if eDMG < 0 else eDMG
				new_pHP = self.pHP[0] - eDMG
				new_pHP = new_pHP if new_pHP >= 0 else 0
				self.pHP[0] = round(new_pHP, 1)  # apply to enemy 
				self.pDODGED = False
				if crit:
					#display_effect("Crit")
					eDMG = "[{}]".format(str(eDMG))
					display_effect("Damage", eDMG)
				else:
					display_effect("Damage", eDMG)
				update_display()  # update info
				
		
		def update_display():
			# include tonics next
			self.cn.delete("pHP_color", "eHP_color", "pAP_color", "eAP_color")
			pHP, eHP = self.pHP, self.eHP
			pbox = pHP[0] / float(pHP[1]) * 100.0 * 1.48  # 150x25, 1% = 1.5px    now 1.48
			ebox = eHP[0] / float(eHP[1]) * 100.0 * 1.48
			pAbox = self.pAP / float(self.pAP_max) * 100.0 * 1.48  # calculate px
			eAbox = self.eAP / float(self.eAP_max) * 100.0 * 1.48
			# remade HP & AP bars
			'''
			create_rect(140, 515-self.rheight-self.hheight, 140+pbox, 515-self.rheight, "pHP_color", "white", width=1)
			create_rect(140, 515-self.rheight, 140+pAbox, 515, "pAP_color", "light yellow", width=1)
			create_rect(660-ebox, 515-self.rheight-self.hheight, 660, 515-self.rheight, "eHP_color", "white", width=1)
			create_rect(660-eAbox, 515-self.rheight, 660, 515, "eAP_color", "light yellow", width=1)
			'''
			# 515
			create_rect(141, 514-self.rheight-self.hheight, 141+pbox, 514-self.rheight, "pHP_color", "white", width=1)
			create_rect(141, 514-self.rheight, 141+pAbox, 514, "pAP_color", "white", width=1)
			create_rect(659-ebox, 514-self.rheight-self.hheight, 659, 514-self.rheight, "eHP_color", "white", width=1)
			create_rect(659-eAbox, 514-self.rheight, 659, 514, "eAP_color", "white", width=1)
			# make visible, blocked by HP & AP bars
			self.cn.tag_raise("pStats_HPcount")
			self.cn.tag_raise("pStats_HP%")
			self.cn.tag_raise("pStats_AP")
			self.cn.tag_raise("eStats_HPcount")
			self.cn.tag_raise("eStats_HP%")
			self.cn.tag_raise("eStats_AP")
			
			_pHP = "{}/{}".format(self.pHP[0], self.pHP[1])
			_pHPpz = "{}%".format(pznt(self.pHP))
			_pTonics = "{} Tonics".format(self.pTonics)
			_pAP = "AP: {}".format(self.pAP)
			_eHP = "{}/{}".format(self.eHP[0], self.eHP[1])
			_eHPpz = "{}%".format(pznt(self.eHP))
			_eTonics = "{} Tonics".format(self.eTonics)
			_eAP = "AP: {}".format(self.eAP)
			self.cn.itemconfigure("pStats_HPcount", text=_pHP)
			self.cn.itemconfigure("pStats_HP%", text=_pHPpz)
			self.cn.itemconfigure("pStats_Tonics", text=_pTonics)
			self.cn.itemconfigure("pStats_AP", text=_pAP)
			self.cn.itemconfigure("eStats_HPcount", text=_eHP)
			self.cn.itemconfigure("eStats_HP%", text=_eHPpz)
			self.cn.itemconfigure("eStats_Tonics", text=_eTonics)
			self.cn.itemconfigure("eStats_AP", text=_eAP)
			self.cn.itemconfigure("turn_holder", text="{}'s Turn".format(self.turn_holder))
			
	
		self.cn.tag_bind("btn0", "<Button-1>", attack)
		self.cn.tag_bind("btn1", "<Button-1>", use_tonic)
		self.cn.tag_bind("btn2", "<Button-1>", flee_battle)
		#self.cn.tag_bind("btn2", "<Button-1>", exit_battle)
		update_display()
		#self.place_image(400, 225, "aEtxt1", "event_txt", anchor="center")
		self.parent.after(250, lambda: event_txt("Fight", msec=500))


'''
class GameMenu:
	def __init__(self, world, *arg, **kwarg):
'''		
		
		
class LoadGame:
	def __init__(self, world, *arg, **kwarg):
		self.world = world
		self.parent = world.parent
		self.cn = world.cn
		self.rsc = world.rsc
		self.load_variables()
		#self.load_ui()
		
	
	def leave(self, *args):
		self.cn.delete(self.mtag)
	
	
	def reload_listbox(self, *args):
		self.cn.itemconfigure(self.zbox.m("selected_listbox_text"), text="")
		self.load_listbox.delete(0, tk.END)
		
		fdata = os.listdir("saves\\")
		sav_list = [data[:-4] for data in fdata if data[-4:] == ".sav"]
		for i in sav_list:
			self.load_listbox.insert(tk.END, i)
	
	
	def load_file(self, *args):
		# QUESTS NOT CHANGING ON LOADING, STILL EMPTY, HOW TO AVOID BUGS, DO MUST PROGRAMMERS SPEND THEIR TIME DEBUGGING?
		tag = self.zbox.m("btn_Load_txt")
		btn_txt = self.cn.itemcget(tag, "text")
		filename = self.cn.itemcget(self.zbox.m("selected_listbox_text"), "text")
		if btn_txt == "Load" and filename != "":
			self.cn.itemconfigure(tag, text="Bgn?")
			self.parent.after(500, lambda _=1: self.cn.itemconfigure(tag, text="Load"))
		elif btn_txt == "Bgn?":
			filepath = "saves\\{}.sav".format(filename)
			with open(filepath, "r") as txtr:
				data = txtr.read()
			self.load_data(data)
			self.leave()
			self.world.game_menu_exit()
			self.world.start_screen_exit()
	
	
	def delete_file(self, *args):
		tag = self.zbox.m("btn_Del_txt")
		btn_txt = self.cn.itemcget(tag, "text")
		filename = self.cn.itemcget(self.zbox.m("selected_listbox_text"), "text")
		if btn_txt == "Del" and filename != "":
			self.cn.itemconfigure(tag, text="[X]?")
			self.parent.after(500, lambda _=1: self.cn.itemconfigure(tag, text="Del"))
		elif btn_txt == "[X]?":
			try:
				os.remove("saves\\{}.sav".format(filename))
				self.reload_listbox()
			except OSError:
				pass
	
	
	def load_ui(self, *args):
		def listbox_selected(*args):
			try:
				v = self.load_listbox.get(self.load_listbox.curselection())
				tag = self.zbox.m("selected_listbox_text")
				self.cn.itemconfigure(tag, text=v)
			except:
				#print("Empty List")
				pass
				
		
		x, y = 200, 100
		self.zbox.mrect(x, y, 400, 400, "white", width=3)
		self.zbox.mbtn(x+338, y+17, "X", self.leave, bg="white", w=50, h=35, txty_change=5)
		
		self.zbox.mtxt(x+11, y+13, "Load Game", font=(self.fn[0], 32))
		self.zbox.mrect(x+13, y+68, 259, 25, "white", width=1)
		self.zbox.mtxt(x+15, y+70, "", font=(self.fn[0], 11), tags="selected_listbox_text")
		self.zbox.mbtn(x+345, y+68, "Del", 
			lambda _=1: self.delete_file(),
			bg="white", w=40, h=25, txty_change=2)
		self.zbox.mbtn(x+279, y+68, "Load",
			lambda _=1: self.load_file(),
			bg="white", w=60, h=25, txty_change=2)
		
		self.load_listbox = tk.Listbox(self.parent, width=48, height=13, bd=1,
			relief="solid", cursor="target", font=(self.fn[0], self.fs[0]),
			highlightthickness=0, activestyle="none")
		self.cn.create_window((400, 345), window=self.load_listbox, anchor="center", tags=(self.mtag))
		self.load_listbox.bind("<<ListboxSelect>>", listbox_selected)
		self.reload_listbox()
		
	
	def load_variables(self, *args):
		self.mtag = "loadgameUI"
		self.zbox = Ztoolbox(self.world)
		self.zbox.mtag = self.mtag
		self.fn, self.fs = self.world.fn, self.world.fs
		self.pdata = self.world.characters["THE_PLAYER"]
		self.quests = self.world.quests
		self.containers = self.world.containers
		#self.aktivql = self.world.aktivql  # current active quests  # CHANGE 01
		#self.fertigql = self.world.fertigql  # current completed quests
	
	
	def load_data(self, data, *args):
		# RESET DATA THEN LOAD! RESET QUEST DATA
		def flt_or_int(string):
			if "." in string:
				return float(string)
			else:
				return int(string)
		# PYTHON JSON? THERE IS A BETTER WAY, THIS IS TEDIUS. IF NONE THEN WE WILL PROCEED WITH THIS.
		# PYTHON CSV
		'''
		= first separator ??, separate by line instead
		|| first separator
		* second separator
		'''
		self.quests = gd.quests
		self.world.aktivql = []
		self.world.fertigql = []
		#self.aktivql = []  # CHANGE 01
		#self.fertigql = []
		
		RAW_TEXT = data
		raw_data = RAW_TEXT.split("{MAIN_SEPARATOR}")
		pstats = raw_data[0].split("\n")
		containers = raw_data[1].split("\n")
		quests = raw_data[2].split("\n")
		
		self.pdata["name"] = pstats[0]
		self.pdata["equipped"] = [x if x != "NONE" else None for x in pstats[1].split("||")]
		self.pdata["inventory"] = pstats[2].split("||") if pstats[2] != "EMPTY_INV" else []
		self.pdata["coin"] = flt_or_int(pstats[3])
		
		player_stats = pstats[4].split("||")
		hp = list(map(flt_or_int, player_stats[0].split("*")))
		self.pdata["stats"][0] = [hp[0], hp[1]]
		for i in range(1, 11):
			self.pdata["stats"][i] = flt_or_int(player_stats[i])
		
		player_mods = pstats[5].split("||")
		self.pdata["mods"]["sword"] = list(map(flt_or_int, player_mods[0].split("*"))) 
		self.pdata["mods"]["axe"] = list(map(flt_or_int, player_mods[1].split("*"))) 
		self.pdata["mods"]["mace"] = list(map(flt_or_int, player_mods[2].split("*")))

		player_perks = pstats[6].split("||") if pstats[6] != "[NO PERKS]" else []
		if player_perks == []: self.pdata["perks"] = []
		else:
			for i in range(len(player_perks)):
				raw_perk_data = player_perks[i].split("*")
				perk_data = [raw_perk_data[0], flt_or_int(raw_perk_data[1])]
				self.pdata["perks"].append(perk_data)
		
		self.pdata["avatar"] = pstats[7]
		self.pdata["image"] = pstats[8]
		self.pdata["map_image"] = pstats[9]
		self.pdata["place_image"] = pstats[10]
		self.pdata["place_indoor_image"] = pstats[11]
		coords = pstats[12].split("*")
		self.pdata["location_coords"] = [int(coords[0]), int(coords[1])]
		
		for i in range(len(containers)):
			if containers[i] == "": continue  # skip blanks
			cdata = containers[i].split("||")
			self.containers[cdata[0]]["coin"] = flt_or_int(cdata[1]) 
			self.containers[cdata[0]]["inventory"] = cdata[2].split("*") if cdata[2] != "0" else []
		
		quests = [x for x in quests if x != ""]  # remove blanks
		quests[0] = quests[0].split("||") if quests[0] != "[NO AKTIV QUESTS]" else []
		for i in range(len(quests[0])):
			#if quests[0][i] == "": continue
			qdata = quests[0][i].split("*")
			self.quests[qdata[0]]["stage"][0] = int(qdata[1])
			#self.aktivql.append(qdata[0])  # CHANGE 01
			self.world.aktivql.append(qdata[0])
		
		quests[1] = quests[1].split("||") if quests[1] != "[NO COMPLETED QUESTS]" else []
		for i in range(len(quests[1])):
			#if quests[1][i] == "": continue
			qdata = quests[1][i].split("*")
			self.quests[qdata[0]]["stage"][0] = int(qdata[1])
			#self.fertigql.append(qdata[0]  # CHANGE 01
			self.world.fertigql.append(qdata[0])
		x, y = self.pdata["location_coords"][0], self.pdata["location_coords"][1]
		self.cn.coords(self.world._m("map_player"), (x, y))
		
		
class SaveGame:
	def __init__(self, world, *arg, **kwarg):
		self.world = world
		self.parent = world.parent
		self.cn = world.cn
		self.rsc = world.rsc
		self.load_variables()
		self.load_ui()
		'''
		get list of saves
		display them like quests
		buttons -> save, leave
		ability to overwrite file
		ui for save
		adding tkinter frame, elements to canvas? listbox or same as quests?
		load is similar
		'''
		
	
	def leave(self, *args):
		self.cn.delete(self.mtag)
	
	
	def reload_listbox(self, *args):
		self.cn.itemconfigure(self.zbox.m("selected_listbox_text"), text="")
		self.load_listbox.delete(0, tk.END)
		
		fdata = os.listdir("saves\\")
		sav_list = [data[:-4] for data in fdata if data[-4:] == ".sav"]
		for i in sav_list:
			self.load_listbox.insert(tk.END, i)
	
	
	def save_file(self, *args):
		tag = self.zbox.m("btn_Save/Owrite_txt")
		btn_txt = self.cn.itemcget(tag, "text")
		filename = self.cn.itemcget(self.zbox.m("selected_listbox_text"), "text")
		if btn_txt == "Save/Owrite" and filename != "":
			self.cn.itemconfigure(tag, text="Bgn?")
			self.parent.after(500, lambda _=1: self.cn.itemconfigure(tag, text="Save/Owrite"))
		elif btn_txt == "Bgn?":
			if " New ->  " in filename:
				filename = filename.replace(" New ->  ", "")
			filepath = "saves\\{}.sav".format(filename)
			data = self.prepare_data()
			with open(filepath, "w") as txtw:
				txtw.write(data)
			self.leave()
	
	
	def add_save_option(self, *args):
		time_data =  dt.datetime.now()
		m, d, y = time_data.month, time_data.day, time_data.year
		h, mn, s = time_data.hour, time_data.minute, time_data.second
		nm = self.pdata["name"]
		text = " New ->  {}_{};{};{}_{};{};{}".format(nm, m, d, y, h, mn, s)
		self.load_listbox.insert(0, text)
		
	
	def load_ui(self, *args):
		def listbox_selected(*args):
			try:
				v = self.load_listbox.get(self.load_listbox.curselection())
				tag = self.zbox.m("selected_listbox_text")
				self.cn.itemconfigure(tag, text=v)
			except:
				#print("Empty List")
				pass
				
		
		x, y = 200, 100
		self.zbox.mrect(x, y, 400, 400, "white", width=3)
		self.zbox.mbtn(x+338, y+17, "X", self.leave, bg="white", w=50, h=35, txty_change=5)
		
		self.zbox.mtxt(x+11, y+13, "Save Game", font=(self.fn[0], 32))
		self.zbox.mrect(x+13, y+68, 259, 25, "white", width=1)
		self.zbox.mtxt(x+15, y+70, "", font=(self.fn[0], 11), tags="selected_listbox_text")
		self.zbox.mbtn(x+279, y+68, "Save/Owrite", 
			lambda _=1: self.save_file(), 
			bg="white", w=106, h=25, txty_change=2)
		self.load_listbox = tk.Listbox(self.parent, width=48, height=13, bd=1,
			relief="solid", cursor="target", font=(self.fn[0], self.fs[0]),
			highlightthickness=0, activestyle="none")
		self.cn.create_window((400, 345), window=self.load_listbox, anchor="center", tags=(self.mtag))
		self.load_listbox.bind("<<ListboxSelect>>", listbox_selected)
		self.reload_listbox()
		self.add_save_option()
	
	
	def load_variables(self, *args):
		self.mtag = "creditsUI"
		self.zbox = Ztoolbox(self.world)
		self.zbox.mtag = self.mtag
		self.fn, self.fs = self.world.fn, self.world.fs
		self.pdata = self.world.characters["THE_PLAYER"]
		self.quests = self.world.quests
		self.containers = self.world.containers
		self.aktivql = self.world.aktivql  # current active quests
		self.fertigql = self.world.fertigql  # current completed quests
	
	
	def prepare_data(self, *args):
		# PYTHON JSON? THERE IS A BETTER WAY, THIS IS TEDIUS. IF NONE THEN WE WILL PROCEED WITH THIS.
		# PYTHON CSV
		'''
		= first separator ??, separate by line instead
		|| first separator
		* second separator
		'''
		# prepare player relayed stats
		n = self.pdata["name"]
		
		# get equipped items
		eq = ""  # NONE||NONE||NONE||NONE||NONE||NONE
		for i in range(len(self.pdata["equipped"])):
			if self.pdata["equipped"][i] == None or self.pdata["equipped"][i] == "":
				eq += "NONE"
			else:
				eq += self.pdata["equipped"][i]
			if i < len(self.pdata["equipped"])-1: eq += "||"
		
		# get inventory items
		inv = ""  # hpot0||hpot0||hpot0||hpot0
		for i in range(len(self.pdata["inventory"])):
			if self.pdata["inventory"][i] == None or self.pdata["inventory"][i] == "":
				inv += "NONE"
			else:
				inv += self.pdata["inventory"][i]
			if i < len(self.pdata["inventory"])-1: inv += "||"
		if inv == "": inv = "EMPTY_INV"
		
		c = self.pdata["coin"]
		
		# get player stats
		ps = ""  #  10*10||1||15||0||10||12345||60||15||25||25||0
		for i in range(len(self.pdata["stats"])):
			if i == 0:
				ps += "{}*{}".format(self.pdata["stats"][i][0], self.pdata["stats"][i][1])
			else:
				ps += str(self.pdata["stats"][i])
			if i < len(self.pdata["stats"])-1: ps += "||"
		
		# player mods with weapons
		mds = ""  # 10*-15*-5*25*0||0*0*-10*75*0||-25*30*-15*75*0
		mlist = ["sword", "axe", "mace"]
		for i in range(len(mlist)):
			mds += "{}*{}*{}*{}*{}".format(self.pdata["mods"][mlist[i]][0], self.pdata["mods"][mlist[i]][1], self.pdata["mods"][mlist[i]][2], self.pdata["mods"][mlist[i]][3], self.pdata["mods"][mlist[i]][4])
			if i < len(mlist)-1: mds += "||"	
		
		prks = ""  # dodge0*9||crit0*2
		for i in range(len(self.pdata["perks"])):
			prks += "{}*{}".format(self.pdata["perks"][i][0], self.pdata["perks"][i][1])
			if i < len(self.pdata["perks"])-1: prks += "||"
		if prks == "": prks = "[NO PERKS]"
		
		ava = self.pdata["avatar"]
		pimg = self.pdata["image"]
		pmimg = self.pdata["map_image"]
		plimg = self.pdata["place_image"]
		pliimg = self.pdata["place_indoor_image"]
		#plloc = "{}*{}".format(self.pdata["location_coords"][0], self.pdata["location_coords"][1])
		#x, y = self.world.characters["THE_PLAYER"]["location_coords"]
		ploc = self.cn.coords(self.world._m("map_player"))
		plloc = "{}*{}".format(int(ploc[0]), int(ploc[1]))
		
		prepdata = "{}\n{}\n{}\n{}\n{}\n".format(n, eq, inv, c, ps)
		prepdata += "{}\n{}\n{}\n{}\n".format(mds, prks, ava, pimg)
		prepdata += "{}\n{}\n{}\n{}\n".format(pmimg, plimg, pliimg, plloc)
		prepdata += "{MAIN_SEPARATOR}\n"
		
		# prepare container list
		container_data = ""
		for key, value in self.containers.items():
			cn = self.containers[key]["coin"]
			inv = self.containers[key]["inventory"]
			if len(inv) == 0: inv = 0
			else:
				inv_data = ""
				for i in range(len(inv)):
					inv_data += inv[i]
					if i < len(inv)-1: inv_data += "*"
			container_data += "{}||{}||{}\n".format(key, cn, inv_data)
		prepdata += container_data
		prepdata += "{MAIN_SEPARATOR}\n"
		
		# prepare quest data
		quest_data = ""
		for i in range(len(self.aktivql)):
			quest_data += "{}*{}".format(self.aktivql[i], self.quests[self.aktivql[i]]["stage"][0])
			if i < len(self.aktivql)-1: quest_data += "||"
		if quest_data == "": quest_data = "[NO AKTIV QUESTS]"
		finquest_data = ""
		for i in range(len(self.fertigql)):
			finquest_data += "{}*{}".format(self.fertigql[i], self.quests[self.fertigql[i]]["stage"][0])
			if i < len(self.fertigql)-1: finquest_data += "||"
		if finquest_data == "": finquest_data = "[NO COMPLETED QUESTS]"
		prepdata += quest_data + "\n"
		prepdata += finquest_data
		#print("*"*50)
		#print(prepdata)
		#print("*"*50)
		return prepdata
		'''
		pdata = "{}={}={}={}={}".format(n, eq, inv, c, ps)
		pdata += "={}={}={}={}={}".format(ms, ma, mm)
		pdata += "={}={}={}={}".format()
		'''		
		
		
class Credits:
	def __init__(self, world, *arg, **kwarg):
		self.world = world
		self.parent = world.parent
		self.cn = world.cn
		self.rsc = world.rsc
		self.load_variables()
		self.load_ui()
	
	
	def leave(self, *args):
		self.cn.delete(self.mtag)
	
	
	def load_ui(self, *args):
		x, y = 100, 100
		self.zbox.mrect(x, y, 600, 400, "white", width=3)
		# put credits at center
		self.zbox.mtxt(x+25, y+15, "Credits", font=(self.fn[0], 36))
		self.zbox.mtxt(x+35, y+90, "R. Mandap")
		self.zbox.mbtn(x+535, y+17, "X", self.leave, bg="white", w=50, h=35, txty_change=5)
	
	
	def load_variables(self, *args):
		self.mtag = "creditsUI"
		self.zbox = Ztoolbox(self.world)
		self.zbox.mtag = self.mtag
		self.fn, self.fs = self.world.fn, self.world.fs
	
		
class Dialogs:
	def __init__(self, world, dialog, extract=None, *arg, **kwarg):
		self.world = world
		self.parent = world.parent
		self.cn = world.cn
		self.rsc = world.rsc
		self.extract = extract
		self.dialog_id = dialog
		# start the ui
		self.load_variables()
		self.load_dialog_ui()
		
	
	def _check_qreq(self, list, *args):
		# check quest requirements
		for row in list:
			condition_failed = False
			if len(row) <= 2 or row[2] == "": continue  # next iteration
			data = row[2].split("|")
			stage_now = self.quests[data[0][1:]]["stage"][0]
			pastqn = self.quests[data[0][1:]]["prerequisites"]
			if data[0][0] == "Q":
				if pastqn != None:
					pastq = self.quests[pastqn]
					# previous quest not completed
					if pastq["stage"][0] < pastq["stage"][1]:
						condition_failed = True
				if stage_now != int(data[1]): condition_failed = True
			if condition_failed:
				list[list.index(row)] = "DELETE"
		while "DELETE" in list: list.remove("DELETE")
		return list
		
	
	def load_dialog_ui(self, *args):
		if self.dialog_bg is not None:
			self.zbox.mimg(0, 0, self.dialog_bg)
		self.zbox.mimg(20, 50, "dtxt_bg-760x485")
		self.zbox.mrect(20, 50, 760, 485, fill="white", width=3)
		#self.zbox.mimg(30, 61, "dtxt_txtbg-530x465")
		self.zbox.mrect(30, 61, 530, 465, fill="white", width=1)
		#self.zbox.mrect(30+210, 61, 530, 465, fill="white", width=1)
		self.zbox.mimg(570, 61, self.dialog_image)
		#self.zbox.mimg(570, 271, "dtxt_choices-200x255")
		self.zbox.mrect(570, 271, 200, 255, fill="white", width=1)
		self.zbox.mtxt(39, 66, self.dialogdata["text"][0],  # title
			font=(self.fn[0], 13, "bold"))
		self.zbox.mtxt(37, 106, self.dialogdata["text"][1], width=520)  # text
		ci = "dtxt_choice-190x30"
		ci2 = "dtxt_choiceO-190x30"
		def dhover(tag, mode=1, *args):
			t = self.zbox.m(tag+"_img")
			if self.dhvr_t != None:
				self.parent.after_cancel(self.dhvr_t)
				self.dhvr_t = None
			if mode == 1:
				#self.dhvr_t = self.parent.after(25,
				#	lambda _=1: self.cn.itemconfigure(t, image=self.rsc[ci2]))
				self.dhvr_t = self.parent.after(25,
					lambda _=1: self.cn.itemconfigure(t, width=2))	
			else: self.cn.itemconfigure(t, width=1)
		#self.tdl = self._check_qreq(copy.deepcopy(self.dialogdata["choices"]))
		self.tdl = self.world.check_event_conditions(self.dialogdata["choices"])
		for i in range(len(self.tdl)):
			c = self.tdl[i]
			tag0 = "choice_{}".format(c[2])
			tag = self.zbox.m(tag0)
			#self.zbox.mimg(575, 281+(i*33), ci, (tag0, tag0+"_img"))
			#self.zbox.mrect(575-540, 281+(i*33), 190, 30, tags=(tag0, tag0+"_img"), fill="white", width=1)
			self.zbox.mrect(575, 281+(i*33), 190, 30, tags=(tag0, tag0+"_img"), fill="white", width=1)
			self.zbox.mtxt(582, 286+(i*33), c[2], tag0)
			#self.zbox.mtxt(582-540, 286+(i*33), c[0], tag0)
			self.cn.tag_bind(tag, "<Enter>", lambda _=1, t=tag0: dhover(t))
			self.cn.tag_bind(tag, "<Leave>", lambda _=1, t=tag0: dhover(t, 0))
			if c[1] is None: continue  # next iteration
			cdata = c[1].split("|")
			x = cdata[1]
			if cdata[0] == "place":  # place
				command = lambda _, n=x, z=c, i=i: self._go_plc(i, n, z)
			elif cdata[0] == "dialg":  # dialog
				command = lambda _, n=x, i=i, z=c: self._go_dlg(i, n, z)	
			elif cdata[0] == "store":  # store, trade between 2 characters
				command = lambda _, n=x, i=i, z=c: self._go_str(i, n, z)
			elif cdata[0] == "box":  # lootbox
				command = lambda _, n=x, i=i, z=c: self._go_box(i, n, z)
			elif cdata[0] == "battl":  # battle
				command = lambda _, n=x, i=i, z=c: self._go_btl(i, n, z)	
			elif cdata[0] == "leave":
				command = lambda _=1, i=i: self._leave_dlg(i)	
			self.cn.tag_bind(tag, "<Button-1>", command)
		self.zbox.raise_ctags()	
		
	
	def load_variables(self, *args):
		self.dlist = self.world.dialogs
		self.dialogdata = self.dlist[self.dialog_id]
		try:
			self.dialog_bg = self.dialogdata["bg_image"]
		except:
			self.dialog_bg = None
		try:
			self.dialog_image = self.dialogdata["image"]
			if self.dialogdata["image"] == None:
				self.dialog_image = "dtxt_image_roadtravel"
		except:
			self.dialog_image = "dtxt_image_roadtravel"
		self.mtag = "dialogUI_{}".format(self.dialog_id)
		self.pdata = self.world.characters["THE_PLAYER"]
		self.zbox = Ztoolbox(self.world)
		self.zbox.mtag = self.mtag
		self.fn, self.fs = self.world.fn, self.world.fs
		self.dhvr_t = None  # hover id
		self.quests = self.world.quests
		

	def _go_dlg(self, id, dialog_id, after_event, *args):
		if not self.world.aktiv_caUI:
			#self.hoverstats_fade()
			#self._special_event(id)
			self.world.check_event_events(after_event)
			self.cn.delete(self.mtag)
			self.world.start_dialog(dialog_id)
	
	
	def _go_btl(self, id, battle_data, after_event, *args):
		if not self.world.aktiv_caUI:
			#self.cn.delete(self.mtag)
			a = battle_data.split("=")
			#self._special_event(id)
			enemy = a[0]
			paths = a[1].split("::")
			print(paths)
			#self.world.check_event_events(after_event)
			self._leave_dlg()
			#self.go_place(self.dialogdata["location"])
			self.world.start_battle(enemy, paths)
	
	
	def _go_plc(self, id, evt, after_event, *args):
		if not self.world.aktiv_caUI:
			# id conflicts with xy
			#self._special_event(id)
			#self.world.check_event_events(after_event)
			#self.cn.delete(self.mtag)
			#self.world.start_place(evt, startxy=xy)
			self._leave_dlg()
		
			startxy = None
			edata = evt.split("*")
			evt_name = edata[0]
			if len(edata) > 1:
				a = edata[1].split(",")
				startxy = (int(a[0]), int(a[1]))
			self.world.check_event_events(after_event)	
			self.world.start_place(evt_name, startxy=startxy)
		
	
	def _go_str(self, id, merchant, after_event, *args):
		if not self.world.aktiv_caUI:
			#self._special_event(id)
			self.world.check_event_events(after_event)
			self.world.start_store(merchant)
			
			
	def _go_box(self, id, container, after_event, *args):
		if not self.world.aktiv_caUI:
			#self._special_event(id)
			self.world.check_event_events(after_event)
			bg = self.dialogdata["bg_image"]
			self.world.start_tradebox(container, bg=bg)


	def _leave_dlg(self, *args):
		if not self.world.aktiv_caUI:
			self.cn.delete(self.mtag)
			if self.extract is not None:
				#self._special_event(id)
				self.extract()
	

	def _special_event(self, id, *args):
		if len(self.tdl[id]) < 4: return  # no special event
		try: 
			command = self.tdl[id][3].split("|")
			ctype = command[0][0]
		except: return  # no special event
		name, action = command[0][1:], command[1]
		if ctype == "Q":  # quest
			if action == "+1":  # elevate stage
				self.quests[name]["stage"][0] += 1
				# CONFLICT WITH AAB CHECK QUEST FUNCTION
				#q_act = "Updated"
				#qtxt = "Quest ''{}'' {}".format(self.quests[name]["name"], q_act)
				#self.world.display_event_txt(qtxt)
			elif action == "+A":  # q accepted
				self.world.aktivql.append(name)
				self.quests[name]["stage"][0] += 1
				q_act = "Accepted"
				qtxt = "Quest ''{}'' {}".format(self.quests[name]["name"], q_act)
				self.world.display_event_txt(qtxt)
			elif action == "+R":  # give reward and end quest
				stage_now = self.quests[name]["stage"][0]
				txt = "reward|collected"
				rl = self.quests[name]["stage{}".format(stage_now)][1][0]
				x = rl.split("|")
				if x[0] == "reward":
					self.world.give_reward(name)
					#q_act = "Completed"
					#qtxt = "Quest ''{}'' {}".format(self.quests[name]["name"], q_act)
					#self.world.display_event_txt(qtxt)
					self.quests[name]["stage{}".format(stage_now)][1][0] = txt
					self.world.fertigql.append(name)
					self.world.aktivql.remove(name)
					

class Inventory:
	def __init__(self, world, extract_func, *arg, **kwarg):
		# data from world
		self.world = world  # world instance
		self.parent = world.parent
		self.cn = world.cn  # world canvas
		self.items = world.items  # world item data
		self.rsc = self.world.rsc  # world Gif image list
		self.p1data = world.characters["THE_PLAYER"]  # world party1 data
		self.extracts = extract_func  # func before deleting this ui
		self.fn, self.fs = world.fn, world.fs
		self.ftheme = world.ftheme
		# start building the ui
		self.set_variables()
		self.set_ui()  # create basic ui
		self.update_ui()

	
	def set_variables(self, *args):
		# init stats and other variables
		self.wtag = self.world.mtag  # main tag of world
		self.mtag = "caUI_Inv"  # main tag of this ui
		self.gtag = "caUI"  # group tag of this ui
		# for hover stats
		self.hover_cooldown = False
		self.go = None
		self.glowing = None
		# fonts
		self.f1, self.fsz1 = "Book Antiqua", 12
		self.f2, self.fsz2 = "Segoe UI", 11
		self.f3, self.fsz3 = "Book Antiqua", 17
		self.font1 = ("Book Antiqua", 12)  # general
		self.font1b = ("Book Antiqua", 12, "bold")
		self.font2 = ("Segoe UI", 11)  # stats
		self.font2b = ("Segoe UI", 11, "bold")
		self.font3 = ("Book Antiqua", 17)  # buttons
	
	
	def set_ui(self, *args):  # ui skeleton
		#self.mimg(400, 50, "inv_bg-635x485", anchor="n")
		self.mrect(84, 75, 635, 454, fill="white", width=2)
		#self.mimg(400, 50, "inv_bgt-635x25", anchor="n")
		# creating party1 info panel
		X, Y = 109, 95  # starting nw coords of the partyl inv panel
		#self.mimg(X, Y, "inv_bg1-280x105")
		self.mrect(X, Y, 280, 105, fill="white", width=2)
		self.mimg(X, Y, "ava_player-100x105", tags=("p1_ava"))  # default ava
		self.mtxt(X+105, Y+5, "Geralt of Rpivilon", font=self.font1b,
			tags=("p1_name", "p1_stats"))
		self.mrect(X+103, Y+27, 172, 22, "light green", tags=("p1_hpbar_bg"), width=1)
		self.mrect(X+103, Y+27, 172, 22, "brown", tags=("p1_hpbar"))
		self.mtxt(X+105, Y+28, "HP:", font=self.font2, tags=("p1_statsn"))
		self.mtxt(X+272, Y+28, "0", font=self.font2,
			tags=("p1_hp", "p1_statsn"), anchor="ne")
		s = [["Atk:", "0"], ["Def:", "0"], ["D%:", "0"], ["AP:", "0"]]
		for i in range(2):
			for x in range(2):
				w = 84
				h = 22
				x1 = X + 103 + (i * 88)
				y1 = Y + 52 + (x * 25)
				n = x + (i * 2)
				txt = s[n][0][:-1]
				# create stat display
				#self.mrect(x1, y1, w, h, "#851122", 
				#	tags=("p1_{}bar_bg".format(txt)))
				self.mrect(x1, y1, w, h, "light green", width=1, 
					tags=("p1_{}bar_bg".format(txt)))
				self.mrect(x1, y1, w, h, "white",
					tags=("p1_{}bar".format(txt)))
				self.mtxt(x1 + 2, y1 + 1, s[n][0],
					font=self.font2, tags=("p1_statsn"))
				self.mtxt(x1 + w - 3, y1 + 1, s[n][1], 
					font=self.font2, anchor="ne",
					tags=("p1_{}".format(txt), "p1_statsn"))
		# creating party1 equipped items and other stats
		X1, Y1 = 109, 205  # starting nw coords
		#self.mimg(X1, Y1, "bg_inv-280x306")
		self.mrect(X1, Y1, 280, 306, fill="white", width=1)
		self.mrect(X1+65, Y1+14, 150, 200, fill="white", width=1)
		self.mimg(X1+90, Y1+17, "img_player-150x200", "p1_img")
		#b = ["helmet", "armor", "boots", "ring", "weapon", "trinket"]
		b = [None, "armor", None, None, "weapon", None]
		for i in range(2):  # 2x3 item slots
			for x1 in range(3): 
				n = x1 + (i * 3)
				#x = X1 + 18 + (i * 199)
				x = X1-5 + 18 + (i * (199+10))
				y = Y1 + 14 + (x1 * 77)
				if b[n] == None: continue
				tag = "p1_{}".format(b[n])
				self.mimg(x, y, "aInv_e{}0".format(b[n].capitalize()),
					tags=(tag, "equipped_imgs"))
				self.cn.tag_bind(self.m(tag), "<Button-1>",
					lambda _=1, n=n: self.unequip_check(n))
				self.cn.tag_bind(self.m(tag), "<Enter>",
					lambda _, x=x, y=y, n=n: self.hoverstats_inv(0, x, y, n))
				self.cn.tag_bind(self.m(tag), "<Leave>",
					self.hoverstats_inv_fade)
		lvl = self.p1data["stats"][5] // 1000
		self.mtxt(X1+210, Y1+193, "lvl {}".format(lvl), anchor=tk.NE, font=self.font2b, 
			tags="lvl")
		self.mrect(X1+67, Y1+222, 146, 15, "light green", tags=("p1_expbar_bg"), width=1)
		self.mrect(X1+67, Y1+222, 73, 15, "white", tags=("p1_expbar"), width=1)
		c = [
			["Scn:", "0"], ["Exp:", "1"], ["H%:", "2"],
			["IA%:", "3"], ["C%:", "4"], ["Cd%:", "5"]
		]
		for i in range(3):
			for x in range(2):
				w = 84  # width
				h = 22  # height
				x1 = X1 + 5 + (i * (w + 4))
				y1 = Y1 + 251 + (x * (h + 3))
				b = 10
				n = x + (i * 2)
				txt = c[n][0][:-1]
				x1 += 0 if i == 0 else b  # make space due to rect increase
				w += b if i == 0 else 0  # increase size of rect
				# create stat display
				self.mrect(x1, y1, w, h, "light green", width=1,
					tags=("p1_{}bar_bg".format(txt)))
				self.mrect(x1, y1, w, h, "white", width=1,
					tags=("p1_{}bar".format(txt)))
				self.mtxt(x1 + 2, y1 + 1, c[n][0],
					font=self.font2, tags=("p1_statsn"))
				self.mtxt(x1 + w - 3, y1 + 1, c[n][1],
					font=self.font2, anchor="ne",
					tags=("p1_{}".format(txt), "p1_statsn"))
		# creating place holder img with leave button
		X2, Y2 = 412, 95
		#self.mimg(X2, Y2, "inv_bg1-280x105")
		self.mrect(X2, Y2, 280, 105, fill="white", width=2)
		self.mimg(X2+6, Y2+8, "aInv_bg0-220x90")
		self.mimg(X2+229, Y2+15, "img_button2", tags=("leave_btn"))
		self.cn.tag_bind(self.m("leave_btn"), "<Button-1>", self.leave_inv)
		# creating party1 inventory
		X3, Y3 = 412, 205
		w, h = 2, 2  # distance between images
		for row in range(4):
			for col in range(6):
				n = col + (row * 6)
				x = X3 + (col * (45 + w))
				y = Y3 + (row * (75 + h))
				tag = "p1_inv{}".format(n)
				self.mimg(x, y, "inv_empty-45x75", tags=(tag,))  # tuple
				self.cn.tag_bind(self.m(tag), "<Button-1>",
					lambda _=1, n=n: self.equip_check(n))
				self.cn.tag_bind(self.m(tag), "<Enter>",
					lambda _, x=x, y=y, n=n: self.hoverstats_inv(1, x, y, n))
				self.cn.tag_bind(self.m(tag), "<Leave>",
					self.hoverstats_inv_fade)
	
	
	def update_ui(self, *args):
		def m(tags):
			return self.m(tags)
		p1 = self.p1data
		for i in range(len(p1["stats"])):
			if i == 0:
				a = float(p1["stats"][i][0])
				b = float(p1["stats"][i][1])
				p1["stats"][i][0] = round(a, 1)
				p1["stats"][i][1] = round(b, 1)
			elif i in [5, 9]:
				p1["stats"][i] = int(p1["stats"][i])
			else:
				n = float(p1["stats"][i])
				p1["stats"][i] = round(n, 1)
		for k, v in p1["mods"].items():
			for x in range(len(v)):
				v[x] = round(v[x], 1)
		X, Y = 109, 95  # starting nw coords of the partyl inv panel
		X1, Y1 = 109, 205  # starting nw coords party1 equipped items
		self.cn.itemconfigure(m("p1_name"), text=p1["name"])
		self.cn.itemconfigure(m("p1_ava"), image=self.rsc[p1["avatar"]])
		self.cn.delete(m("p1_hpbar"))
		l = 172.0 * (p1["stats"][0][0] / float(p1["stats"][0][1]))
		self.mrect(X+103, Y+27, l, 22, "white", tags=("p1_hpbar"), width=1)
		txt = "{}/{}".format(p1["stats"][0][0], p1["stats"][0][1])
		self.cn.itemconfigure(m("p1_hp"), text=txt)
		self.cn.itemconfigure(m("p1_img"), image=self.rsc[p1["image"]])
		s = [["Atk:", "0"], ["Def:", "0"], ["D%:", "0"], ["AP:", "0"]]
		s1 = [p1["stats"][4], p1["stats"][3], p1["stats"][2], p1["stats"][1]]
		maxn = [100, 100, 100, 10]
		for i in range(2):
			for x in range(2):
				w = 84
				h = 22
				x1 = X + 103 + (i * 88)
				y1 = Y + 52 + (x * 25)
				n = x + (i * 2)
				txt = s[n][0][:-1]
				tag0 = "p1_{}".format(txt)
				tag1 = "p1_{}bar".format(txt)
				# create stat display
				self.cn.itemconfigure(m(tag0), text=s1[n])
				self.cn.delete(m(tag1))
				max = maxn[n]
				l = float(w) * (s1[n] / float(max))
				l = w if l > w else l
				self.mrect(x1, y1, l, h, "white", tags=(tag1), width=1)
		e = p1["equipped"]
		#b = ["helmet", "armor", "boots", "ring", "weapon", "trinket"]
		b = [None, "armor", None, None, "weapon", None]
		for i in range(len(e)):
			if b[i] == None: continue
			tag = "p1_{}".format(b[i])
			self.cn.itemconfigure(m(tag),
				image=self.rsc["aInv_e{}0".format(b[i].capitalize())])
			if e[i] != None:
				img = self.rsc[self.items[e[i]]["image"]]
				self.cn.itemconfigure(m(tag), image=img)
		self.cn.delete(m("p1_expbar"))
		l = 146.0 * (p1["stats"][5] % 1000 / 1000.0)
		self.mrect(X1+67, Y1+222, l, 15, "white", tags=("p1_expbar"), width=1)
		c = [
			["Scn:", "0"], ["Exp:", "1"], ["H%:", "2"],
			["IA%:", "3"], ["C%:", "4"], ["Cd%:", "5"]
		]
		c1 = [
			p1["coin"], p1["stats"][5], p1["stats"][6],
			p1["stats"][7], p1["stats"][8], p1["stats"][9]
		]
		for i in range(3):
			for x in range(2):
				w = 84  # width
				h = 22  # height
				x1 = X1 + 5 + (i * (w + 4))
				y1 = Y1 + 251 + (x * (h + 3))
				b = 10
				n = x + (i * 2)
				txt = c[n][0][:-1]
				x1 += 0 if i == 0 else b  # make space due to rect increase
				w += b if i == 0 else 0  # increase size of rect
				tag0 = "p1_{}".format(txt)
				tag1 = "p1_{}bar".format(txt)
				# config stat display
				self.cn.itemconfigure(m(tag0), text=c1[n])
				if n < 2:
					continue  # skip below, next iteration
				self.cn.delete(m(tag1))
				max = 100 if n < 5 else 1000
				rect_s = float(w) * (c1[n] / float(max))
				if n >= 2:
					rect_s = w if rect_s > w else rect_s
				self.cn.delete(tag1)
				self.mrect(x1, y1, rect_s, h, "white", tags=(tag1), width=1)
		p1_inv = p1["inventory"] + ["empty"] * (24 - len(p1["inventory"]))
		for row in range(4):
			for col in range(6):
				n = col + (row * 6)
				tag = m("p1_inv{}".format(n))
				self.cn.itemconfigure(tag,
					image=self.rsc["inv_empty-45x75"])
		for row in range(4):
			for col in range(6):
				n = col + (row * 6)
				tag = m("p1_inv{}".format(n))
				if p1_inv[n] != "empty":
					self.cn.itemconfigure(tag,
						image=self.rsc[self.items[p1_inv[n]]["image"]])
		# make stats visible
		self.cn.tag_raise(m("p1_statsn"))
		self.cn.tag_raise(m("equipped_imgs"))
		self.cn.delete(m("hover_stats"))
		
	
	def unequip_check(self, iindex, *args):
		p1 = self.p1data
		if p1["equipped"][iindex] != None:
			self.unequip_item(iindex)
		
	
	def equip_check(self, iindex, *args):
		p1 = self.p1data
		p1_inv = p1["inventory"] + ["e"] * (24 - len(p1["inventory"]))
		if p1_inv[iindex] != "e":
			self.equip_item(p1_inv[iindex])
		
	
	def unequip_item(self, iindex, *args):
		player = self.p1data
		iteml = self.items
		if iteml[player["equipped"][iindex]]["type"] == "armor":
			player["stats"][3] -= iteml[player["equipped"][iindex]]["defense_value"]
			player["inventory"].append(player["equipped"][iindex])
			player["equipped"][iindex] = None
		elif iteml[player["equipped"][iindex]]["type"] == "weapon":
			wt = iteml[player["equipped"][iindex]]["weapon_type"]
			for i in range(5):  # HC% IA% CC% CD%
					player["stats"][i+6] -= player["mods"][wt][i]
			atk = iteml[player["equipped"][iindex]]["attack_value"]
			player["stats"][4] -= atk + (atk * player["mods"][wt][4]/100.0)
			player["inventory"].append(player["equipped"][iindex])
			player["equipped"][iindex] = None
		self.update_ui()
		
	
	def equip_item(self, item, *args):
		# THE_PLAYER -> sword0, equip_item("sword0")
		'''
		by column
		Helmet, Ring
		Armor, Weapon
		Boots, Trinket
		'''
		player = self.p1data
		iteml = self.items
		if iteml[item]["type"] == "armor":
			if player["equipped"][1] is not None:
				self.unequip_item(1)
			player["stats"][3] += iteml[item]["defense_value"]
			player["equipped"][1] = item
			del player["inventory"][player["inventory"].index(item)]
		elif iteml[item]["type"] == "weapon":
			if player["equipped"][4] is not None:
				self.unequip_item(4)
			wt = iteml[item]["weapon_type"] 
			for i in range(5):  # HC% IA% CC% CD% DB%
				player["stats"][i+6] += player["mods"][wt][i]
			atk = iteml[item]["attack_value"]
			player["stats"][4] += atk + (atk * player["mods"][wt][4]/100.0)
			player["equipped"][4] = item
			del player["inventory"][player["inventory"].index(item)]
		elif iteml[item]["type"] == "potion":
			php = player["stats"][0][0]
			m = player["stats"][0][1]
			if php < m:
				n = iteml[item]["heal_value"] + php
				n = n if n <= m else m
				player["stats"][0][0] = n
				del player["inventory"][player["inventory"].index(item)]
		self.update_ui()
		
	
	def leave_inv(self, *args):
		self.cn.delete(self.mtag)
		self.extracts()
	
	
	def hoverstats_inv_fade(self, *args):
		if self.go is not None:
			self.parent.after_cancel(self.go)
			self.go = None
		self.cn.delete(self.m("hover_stats"))
	
	
	def hoverstats_inv(self, invn, x, y, item_index, stage=0, *args):
		# separate to prevent crashing, crashes after
		# called multiple times instead of once
		self.cn.delete(self.m("hover_stats"))
		xn = (x + 47) if (x + 152) < 760 else (x-152)
		yn = y - 7
		invnm = "inventory"
		inv0 = self.p1data["equipped"]
		inv1 = self.p1data[invnm] + ["e"] * (24 - len(self.p1data[invnm]))
		inv = [inv0, inv1]
		if inv[invn][item_index] != "e" and inv[invn][item_index] != None:
			if stage == 0:
				self.hoverstats_inv_fade()
				self.go = self.parent.after(250,
					lambda: self.hoverstats_inv(invn, x, y, item_index, stage=1))
			elif stage == 1:
				item_n = self.items[inv[invn][item_index]]["name"]
				item_t = self.items[inv[invn][item_index]]["type"]
				item_p = self.items[inv[invn][item_index]]["price"][1]
				if self.items[inv[invn][item_index]]["type"] != None:
					itp = self.items[inv[invn][item_index]]["type"]
				else: itp = "???"
				if self.items[inv[invn][item_index]]["descr"] != None:
					ids = self.items[inv[invn][item_index]]["descr"]
				else: ids = "?????"
				sn = sv = ""
				if itp == "armor": 
					sn, sv = "D:", self.items[inv[invn][item_index]]["defense_value"]
				elif itp == "potion": 
					sn, sv = "H:", self.items[inv[invn][item_index]]["heal_value"]
				elif itp == "weapon": 
					sn, sv = "A:", self.items[inv[invn][item_index]]["attack_value"]
				mtag = ("hover_stats",)
				self.mimg(xn, yn, image="bg-150x105", tags=mtag)
				'''
				self.mrect(xn+3, yn+3, 144, 78, "#776611", tags=mtag)
				self.mrect(xn+3, yn+3, 144, 78, "#776611", tags=mtag)
				self.mrect(xn+3, yn+81, 49, 21, "#774411", tags=mtag)
				self.mrect(xn+52, yn+81, 95, 21, "#773311", tags=mtag)
				'''
				self.mrect(xn+3, yn+3, 144, 78, "white", tags=mtag)
				self.mrect(xn+3, yn+3, 144, 78, "white", tags=mtag)
				self.mrect(xn+3, yn+81, 49, 21, "white", tags=mtag)
				self.mrect(xn+52, yn+81, 95, 21, "white", tags=mtag)
				self.mtxt(xn+5, yn+4, item_n, mtag, self.ftheme[1])
				self.mtxt(xn+7, yn+18, itp, mtag, (self.fn[1], 9))
				self.mtxt(xn+5, yn+30, ids, mtag, (self.fn[0], 11), width=140)
				self.mtxt(xn+5, yn+102, sn, mtag, anchor="sw")
				self.mtxt(xn+48, yn+102, sv, mtag, anchor="se")
				self.mtxt(xn+95, yn+102, "Scnr:", mtag, anchor="se")
				self.mtxt(xn+145, yn+102, item_p, mtag, anchor="se")					
	
	
	def m(self, tag):
		return "{}_{}".format(self.mtag, tag)
	
	
	def check_tags(self, tags):
		# Input: ("a", "b")
		# Output: (mtag, "mtag_a", "mtag_b")
		if tags is None:
			tags = (self.mtag, self.gtag)
		elif isinstance(tags, str):  # string
			x = [self.m(tags)]
			tags = tuple([self.mtag, self.gtag] + x)
		else:
			x = []
			for i in tags:
				x.append(self.m(i))
			tags = tuple([self.mtag, self.gtag] + x)
		return tags
	
	
	def mrect(self, x1, y1, w, h, fill="black", tags=None, c=None, width=0, *args):
		tags = self.check_tags(tags)  # must be tuple
		self.cn.create_rectangle(x1, y1, x1+w, y1+h, fill=fill, tags=tags,
			outline=c, width=width)
	
	
	def mimg(self, x, y, image, tags=None, anchor=tk.NW, *args):
		tags = self.check_tags(tags)  # must be tuple
		self.cn.create_image(x, y, image=self.rsc[image], tags=tags,
			anchor=anchor)
			
		
	def mtxt(self, x, y, txt, tags=None, font=None, anchor=tk.NW,
		fill="black", width=250, align="left", *args):
		tags = self.check_tags(tags)  # must be tuple
		font = (self.f1, self.fsz1) if font is None else font
		self.cn.create_text(x, y, text=txt, tags=tags, font=font,
			anchor=anchor, fill=fill, width=width, justify=align)
			

class Perks:
	def __init__(self, world, party1data, extract_func, pf1=None, *arg, **kwarg):
		# data from world
		self.world = world  # world instance
		self.parent = world.parent
		self.cn = world.cn  # world canvas
		self.items = world.items  # world item data
		self.perksl = copy.deepcopy(world.perks)  # list of perks
		self.rsc = self.world.rsc  # world Gif image list
		self.p1data = copy.deepcopy(party1data)  # world party1 data
		self.playerdata = copy.deepcopy(world.perks)
		self.pl = copy.deepcopy(party1data)
		self.extract = extract_func  # utility func
		self.pf1 = pf1
		# start building the ui
		self.set_variables()
		self.set_ui()  # create basic ui
		self.update_ui()
		# should copy only, save only to real data after save btn
	
	
	def set_variables(self, *args):
		# init stats and other variables
		self.wtag = self.world.mtag  # main tag of world
		self.mtag = "caUI_Perks"  # main tag of this ui
		self.gtag = "caUI"  # group tag of this ui
		# for hover stats
		self.hover_cooldown = False
		self.go = None
		self.go1 = None
		self.go2 = None
		self.glowing = None
		# fonts
		self.f1, self.fsz1 = "Book Antiqua", 12
		self.f2, self.fsz2 = "Segoe UI", 11
		self.f3, self.fsz3 = "Book Antiqua", 17
		self.font1 = ("Book Antiqua", 12)  # general
		self.font1b = ("Book Antiqua", 12, "bold")
		self.font2 = ("Segoe UI", 11)  # stats
		self.font2b = ("Segoe UI", 11, "bold")
		self.font3 = ("Book Antiqua", 17)  # buttons
		#self.c = "#671111"  # perk line border color
		#self.c = "#675511"  # perk line border color
		#self.c1 = "#a5951f"
		#self.c1 = "black"
		self.c, self.c1 = "brown", "black"
		

	def save_perks(self, *args):
		if self.pf1 is not None:
			self.pf1()
			self.cn.tag_lower(self.m("btn_Save Perks"))
			self.cn.tag_lower(self.m("btn_Cancel"))
			self.update_ui()
	

	def count_perkpoints(self, *args):
		self.perkpoints = self.p1data["stats"][5] // 1000
		self.perkcount = 0
		for i in self.p1data["perks"]:
			self.perkcount += i[1]
		self.perks_available = self.perkpoints - self.perkcount
		txt = "{} Perks(s) Available".format(self.perks_available)
		self.cn.itemconfigure(self.m("p1_perks"), text=txt)
	
		
	def update_ui(self, *args):
		def m(tags):
			return self.m(tags)
		p1 = self.p1data
		self.cn.itemconfigure(m("p1_name"), text=p1["name"])
		self.cn.itemconfigure(m("p1_ava"), image=self.rsc[p1["avatar"]])
		self.set_playerstats()
		self.cn.delete(self.m("ptree"))
		self.create_perktree()
		self.count_perkpoints()
		self.cn.tag_raise(self.m("hover_stats"))
		#self.cn.delete(self.m("hover_stats"))
	
	
	def addcheck_perk(self, perk, stage=0, *args):
		if stage == 0 and self.perks_available > 0:
			if self.go2 is not None:
				self.parent.after_cancel(self.go2)
				self.go2 = None
			self.cn.tag_raise(self.m("btn_Save Perks"))
			self.cn.tag_raise(self.m("btn_Cancel"))
			self.go2 = self.parent.after(100, lambda: self.addcheck_perk(perk, stage=1))
		elif stage == 1:
			p = self.perksl[perk]
			tag = self.m("perk_{}".format(perk))
			s = "unlocked"
			if p["prerequisite"] != None:
				a = p["prerequisite"]
				if self.perksl[a[0]]["level"][0] < a[1]:
					s = "locked"
			if s == "unlocked":
				n = p["level"][0] + 1
				if n <= p["level"][1]:
					p["level"][0] += 1
					self.add_perk(perk)
			self.update_ui()
	
	
	def unequip_item(self, iindex, *args):
		player = self.p1data
		iteml = self.items
		if iteml[player["equipped"][iindex]]["type"] == "armor":
			player["stats"][3] -= iteml[player["equipped"][iindex]]["defense_value"]
			player["inventory"].append(player["equipped"][iindex])
			player["equipped"][iindex] = None
		elif iteml[player["equipped"][iindex]]["type"] == "weapon":
			wt = iteml[player["equipped"][iindex]]["weapon_type"]
			for i in range(5):  # HC% IA% CC% CD%
					player["stats"][i+6] -= player["mods"][wt][i]
			atk = iteml[player["equipped"][iindex]]["attack_value"]
			player["stats"][4] -= atk + (atk * player["mods"][wt][4]/100.0)
			player["inventory"].append(player["equipped"][iindex])
			player["equipped"][iindex] = None
		
	
	def equip_item(self, item, *args):
		# THE_PLAYER -> sword0, equip_item("sword0")
		'''
		by column
		Helmet, Ring
		Armor, Weapon
		Boots, Trinket
		'''
		player = self.p1data
		iteml = self.items
		if iteml[item]["type"] == "armor":
			if player["equipped"][1] is not None:
				self.unequip_item(1)
			player["stats"][3] += iteml[item]["defense_value"]
			player["equipped"][1] = item
			del player["inventory"][player["inventory"].index(item)]
		elif iteml[item]["type"] == "weapon":
			if player["equipped"][4] is not None:
				self.unequip_item(4)
			wt = iteml[item]["weapon_type"] 
			for i in range(5):  # HC% IA% CC% CD%
				player["stats"][i+6] += player["mods"][wt][i]
			atk = iteml[item]["attack_value"]
			atk1 = atk + (atk * player["mods"][wt][4]/100.0)
			#atk1 = round(atk1, 1)
			player["stats"][4] += atk1
			player["equipped"][4] = item 
			del player["inventory"][player["inventory"].index(item)]
		elif iteml[item]["type"] == "potion":
			php = player["stats"][0][0]
			m = player["stats"][0][1]
			if php < m:
				n = iteml[item]["heal_value"] + php
				n = n if n <= m else m
				player["stats"][0][0] = n
				del player["inventory"][player["inventory"].index(item)]
	
	
	def change_weaponstats(self, wchange, change_num, *arg):
		player = self.p1data
		iteml = self.items
		slots = []
		for i in range(6):
			if player["equipped"][i] != None:
				slots.append(player["equipped"][i])
				self.unequip_item(i)
		# change weapon stats
		z = ["HC", "IA", "CC", "Cd", "DB"]
		if wchange[:5] == "sword":
			i = z.index(wchange[5:])
			player["mods"]["sword"][i] += change_num
		elif wchange[:3] == "axe":
			i = z.index(wchange[3:])
			player["mods"]["axe"][i] += change_num
		elif wchange[:4] == "mace":
			i = z.index(wchange[4:])
			player["mods"]["mace"][i] += change_num
		for i in slots:
			self.equip_item(i)
	

	def add_perk(self, perk, mode="normal", *args):
		person = self.p1data
		stats = person["stats"]  # HP AP Dodge% Def Atk Exp
		perk_info = self.perksl[perk]
		sym = ["HP", "AP", "Dodge%", "Def", "Atk"]
		n = 1 if mode == "normal" else -1  # reverse
		for i in range(len(perk_info["affects"])):
			try:
				stat = sym.index(perk_info["affects"][i])  # index
			except:
				stat = 42  # unused/stopper
			change_type = perk_info["change"][i][-3:]  # (%) or raw
			change_num = float(perk_info["change"][i][:-3])
			if change_type == "(%)":
				change_num /= 100
				if stat == 0:  # HP [12/12]
					if n == -1:
						stats[stat][0] /= (change_num + 1)
						stats[stat][1] /= (change_num + 1)
					else:
						stats[stat][0] += (stats[stat][0] * change_num * n)
						stats[stat][1] += (stats[stat][1] * change_num * n)
					# limit decimals
					#stats[stat][0] = float("{0:.1f}".format(stats[stat][0]))
					#stats[stat][1] = float("{0:.1f}".format(stats[stat][1]))
				elif stats == 42:
					pass
				else:
					if n == -1:
						stats[stat] /= (change_num + 1)
					else:
						stats[stat] += (stats[stat] * change_num * n)
					#stats[stat] = float("{0:.1f}".format(stats[stat]))
			elif change_type == "raw":
				try:
					statz = stats[stat]
				except:
					statz = 42  # unused/stopper
				if stat == 0:  # HP [12/12]
					statz[0] += change_num * n
					statz[1] += change_num * n
					statz[0] = 0.1 if statz[0] < 0 else statz[0]
					statz[1] = 0.1 if statz[1] < 0 else statz[1]
				elif statz == 42:
					w = perk_info["affects"][i][:5]
					wchange = perk_info["affects"][i]
					if w == "sword":
						self.change_weaponstats(wchange, change_num)
				else:
					#statz += change_num * n  # doesn't work
					stats[stat] += change_num * n
					#stats[stat] = float("{0:.1f}".format(stats[stat]))
			else:
				pass
				##print "'{}' unknown".format(change_type)
		if n == - 1:
			#del person["perks"][person["perks"].index(perk)]
			pass
		else:
			perk_exists, pindex = False, 0
			for i in range(len(person["perks"])):
				if person["perks"][i][0] == perk:
					perk_exists = True
					pindex = i
					break
			if perk_exists:
				person["perks"][pindex][1] += 1
			else:
				person["perks"].append([perk, 1])
	
	
	def square_it(self, perk, *args):
		coords = self.cn.coords(self.m("perk_{}".format(perk)))
		x, y = coords[0], coords[1]
		c = self.c
		#c = "brown"
		tag = ("sqrlock_{}".format(perk), "ptree", "pi")  # "perk_{}".format(perk),
		self.mrect(x, y, 40, 3, fill=c, tags=tag)
		self.mrect(x, y, 3, 40, fill=c, tags=tag)
		self.mrect(x + 37, y, 3, 40, fill=c, tags=tag)
		self.mrect(x, y + 37, 40, 3, fill=c, tags=tag)
		self.mrect(x + 40, y + 1, 7, 38, fill=self.c, tags=tag)
	

	def line_it_n(self, preperk0, x0, y0, perk1, x1, y1, *args):
		perk0 = preperk0[0]
		diff = self.perksl[perk0]["level"][0] / float(preperk0[1])  # % in decimals
		distance = y1 - y0
		tag = "perk_{}2perk_{}".format(perk0, perk1)
		#c = "#672211"
		#c1 = "#421111"
		c, c1 = self.c, self.c1
		self.mrect(x0-2, y0, 3, distance, fill=c, tags=(tag, "ptree"))
		if diff >= 1:
			self.cn.itemconfigure(self.m(tag), fill=c1)
		elif diff > 0:
			n = distance * diff
			n = n if n <= distance else distance
			self.mrect(x0-2, y0, 3, n, fill=c1, 
				tags=(tag, "ptree"))
	
	
	def line_it_nw(self, preperk0, x0, y0, perk1, x1, y1, *args):
		# FIX FUNCTIONS, COMMENT, REFACTOR, SEPARATE
		perk0 = preperk0[0]
		diff = self.perksl[perk0]["level"][0] / float(preperk0[1])  # % in decimals
		distance = y1 - y0
		tag = "perk_{}2perk_{}".format(perk0, perk1)
		#c = "#672211"
		#c1 = "#421111"
		c, c1 = self.c, self.c1
		l = x1 - x0
		sl = distance / 2.0
		# create border lines
		self.mrect(x0 - 2, y0, 3, sl, fill=c,
			tags=(tag, "ptree", "{}s1".format(tag)))
		self.mrect(x0 - 2, y0 + sl, l, 3, fill=c, 
			tags=(tag, "ptree", "{}s2".format(tag)))
		self.mrect(x1 - 2, y1, 3, -sl, fill=c,
			tags=(tag, "ptree", "{}s3".format(tag)))
		# create progress lines
		lsize = l + distance  # length of border line
		lunits = lsize * diff  # length of line
		llist = [
			((x0-2), y0, (distance / 2.0)), 
			((x0-2), (y0 + sl), ((distance / 2.0) + l)), 
			((x1-2), (y0 + sl), (distance + l))
		]
		for i in range(3):
			if lunits >= llist[i][2]:
				self.cn.itemconfigure(self.m("{}s{}".format(tag, i + 1)),
					fill=c1)
			elif lunits != 0:
				if i != 1:
					w, h = 3, sl
					z = 0 if i == 0 else llist[i-1][2]
					nunits = lunits - z
					#h = sl * (nunits / sl)
					h = nunits
				else:
					w, h = l, 3
					nunits = lunits - llist[i-1][2]
					#w = l * (nunits / l)
					w = nunits
				self.mrect(llist[i][0], llist[i][1], w, h, fill=c1,
					tags=(tag, "ptree", "{}s{}q".format(tag, i + 1)))
				break	
	
	
	def line_it_ne(self, preperk0, x0, y0, perk1, x1, y1, *args):
		# FIX FUNCTIONS, COMMENT, REFACTOR, SEPARATE
		perk0 = preperk0[0]
		diff = self.perksl[perk0]["level"][0] / float(preperk0[1])  # % in decimals
		distance = y1 - y0
		tag = "perk_{}2perk_{}".format(perk0, perk1)
		#c = "#672211"
		#c1 = "#421111"
		c, c1 = self.c, self.c1
		l = x0 - x1
		sl = distance / 2.0
		# create border lines
		self.mrect(x0 - 2, y0, 3, sl, fill=c,
			tags=(tag, "ptree", "{}s1".format(tag)))
		change = 3
		l = -l
		self.mrect(x0 - 2 + change, y0 + sl, l, 3, fill=c, 
			tags=(tag, "ptree", "{}s2".format(tag)))
		self.mrect(x1 - 2, y1, 3, -sl, fill=c,
			tags=(tag, "ptree", "{}s3".format(tag)))
		# create progress lines
		distance = -distance
		lsize = l + distance  # length of border line
		lunits = lsize * diff  # length of line
		distance *= -1
		llist = [
			((x0-2), y0, (distance / 2.0)), 
			((x0-2 + change), (y0 + sl), ((distance / 2.0) - l)), 
			((x1-2), (y0 + sl), (distance - l))
		]
		for i in range(3):
			if abs(lunits) >= abs(llist[i][2]):
				self.cn.itemconfigure(self.m("{}s{}".format(tag, i + 1)),
					fill=c1)
			elif abs(lunits) != 0:
				if i != 1:
					w, h = 3, sl
					z = 0 if i == 0 else llist[i-1][2]
					nunits = abs(lunits) - z
					h = sl * (nunits / sl)
				else:
					w, h = l, 3
					nunits =  llist[i-1][2] - abs(lunits)
					w = l * (nunits / l)
				self.mrect(llist[i][0], llist[i][1], w, h, fill=c1,
					tags=(tag, "ptree", "{}s{}q".format(tag, i + 1)))
				break
	
	
	def line_it(self, preq_perk, perk1, *args):
		# creates a line from perk to perk
		# preq_perk must be on higher than perk1
		perk0 = preq_perk[0]
		coords0 = self.cn.coords(self.m("perk_{}_img".format(perk0)))
		coords1 = self.cn.coords(self.m("perk_{}_img".format(perk1)))
		x0, y0 = coords0[0] + 20, coords0[1] + 40
		x1, y1 = coords1[0] + 20, coords1[1]
		# perk1 is below perk0
		if x0 == x1:
			self.line_it_n(preq_perk, x0, y0, perk1, x1, y1)
		elif x0 < x1:
			self.line_it_nw(preq_perk, x0, y0, perk1, x1, y1)
		elif x0 > x1:
			self.line_it_ne(preq_perk, x0, y0, perk1, x1, y1)
			
	
	def create_perk(self, x, y, perk, *args):
		# 609 / 3 = 203 per class tree
		# nw coord, 40x40img 
		p = self.perksl[perk]
		self.mimg(x, y, p["img"],
			("perk_{}_img".format(perk), "perk_{}".format(perk), "ptree", "pi"))
		self.mrect(x + 40, y + 1, 7, 38, tags=("pi"), fill="black")
		h = float(34) * (p["level"][0] / float(p["level"][1]))
		if p["level"][0] > 0:
			self.mrect(x + 41, y + 37, 5, -h, fill="brown", tags=("ptree", "pi"))
		# hover_stats
		if p["prerequisite"] != None:
			a = p["prerequisite"]
			if self.perksl[a[0]]["level"][0] < a[1]:  # perk lvl < req. lvl
				self.square_it(perk)
				id = self.m("perk_{}2perk_{}".format(a[0], perk))
			self.line_it(a, perk)
		tag = self.m("perk_{}".format(perk))
		self.cn.tag_bind(tag, "<Button-1>",
			lambda _=1, perk=perk: self.addcheck_perk(perk, 0))
		self.cn.tag_bind(tag, "<Enter>",
			lambda _=1, x=x, y=y, perk=perk: self.hoverstats_perks(x, y, perk))
		self.cn.tag_bind(tag, "<Leave>",
			lambda _=1: self.hoverstats_perks_fade())
		self.cn.tag_raise(self.m("pi"))  # make perk imgs visible
		
		
	def create_perktree(self, *args):
		#self.create_perk(195, 265, "swordDMG0")
		x0, y0 = 190, 345
		self.create_perk(x0-87, y0, "dodge0")
		self.create_perk(x0-87, y0+(52 * 2), "dodgeMX0")
		self.create_perk(x0, y0, "swordDMG0")
		self.create_perk(x0, y0+52, "swordHC0")
		self.create_perk(x0+52, y0+52, "swordCC0")
		self.create_perk(x0+52, y0+(52 * 2), "swordMX0")
		
	
	def set_playerstats(self, *args):
		def m(tags):
			return self.m(tags)
		p1 = self.p1data
		#X, Y = 95, 85  # starting nw coords of the partyl inv panels
		X, Y = 95, 95  # starting nw coords of the partyl inv panels
		'''
		a = [  # Name, Value, Cap
			["HP:", p1["stats"][0][0], p1["stats"][0][1]],
			["Atk:", p1["stats"][4], 100], 
			["D%:", p1["stats"][2], 100], 
			["H%:", p1["stats"][6], 100], 
			["C%:", p1["stats"][8], 100],
			["lvl:", p1["stats"][5]/1000, None], 
			["Def:", p1["stats"][3], 100], 
			["AP:",  p1["stats"][1], 10], 
			["IA%:", p1["stats"][7], 100], 
			["Cd%:", p1["stats"][9], 1000]
		]
		'''
		a = [  # Name, Value, Cap
			["HP:", round(p1["stats"][0][0], 1), round(p1["stats"][0][1], 1)],
			["Atk:", round(p1["stats"][4], 1), 100], 
			["D%:", round(p1["stats"][2], 1), 100], 
			["H%:", round(p1["stats"][6], 1), 100], 
			["C%:", round(p1["stats"][8], 1), 100],
			["lvl:", int(p1["stats"][5]/1000), None], 
			["Def:", round(p1["stats"][3], 1), 100], 
			["AP:",  round(p1["stats"][1], 1), 10], 
			["IA%:", round(p1["stats"][7], 1), 100], 
			["Cd%:", int(p1["stats"][9]), 1000]
		]
		self.cn.delete(m("pmain_stats"))
		for row in range(2):
			for col in range(5):
				n = col + (row * 5)
				w, h = 125 if col == 0 else 78, 22
				x1, y1 = X + 106 + (col * (w + 4)), Y + 27 + (row * (h + 3))
				b = 47
				x1 += 0 if col == 0 else b  # make space due to rect increase
				txt, astat_txt = a[n][0][:-1], a[n][1]
				'''
				if n == 0: # HP
					a1, a2, = round(a[n][1], 1), round(a[n][2], 1) 
					astat_txt = "{}/{}".format(a1, a2)
				elif n in [1, 2, 3, 4, 6, 7, 8]:
					astat_txt = round(astat_txt, 1)
				else:
					astat_txt = int(astat_txt)
				'''
				l = w
				if a[n][2] != None:
					l = float(w) * (a[n][1] / float(a[n][2]))
					l = w if l > w else l
				# create stat display
				self.mrect(x1, y1, w, h, "light green", width=1, 
					tags=("p1_{}bar_bg".format(txt), "pmain_stats"))
				self.mrect(x1, y1, l, h, "white", width=1,
					tags=("p1_{}bar".format(txt), "pmain_stats"))
				self.mtxt(x1 + 2, y1 + 1, a[n][0],
					font=self.font2, tags=("pmain_stats"))
				self.mtxt(x1 + w - 3, y1 + 1, astat_txt,
					font=self.font2, anchor="ne",
					tags=("p1_{}".format(txt), "pmain_stats"))
 		
	
	def set_ui(self, *args):  # ui skeleton
		#self.mimg(400, 50, "inv_bg-635x485", anchor="n")
		self.mrect(84, 75, 635, 454, fill="white", width=2)
		#self.mimg(400, 50, "inv_bgt-635x25", anchor="n")
		#X, Y = 95, 85  # starting nw coords of the partyl inv panel
		X, Y = 95, 95  # starting nw coords of the partyl inv panel
		self.mimg(X, Y, "ava_player-100x105", tags=("p1_ava"))  # default ava
		self.mtxt(X+106, Y+5, "Geralt of Rpivilon", font=self.font1b,
			tags=("p1_name", "p1_stats"))
		self.mtxt(X+558, Y+5, "0 Perk(s) Available", font=self.font1,
			anchor="ne", tags=("p1_perks", "p1_stats"))
		self.set_playerstats()
		self.count_perkpoints()
		self.create_perktree()
		self.mtxt(702, Y-5, "Leave", font=(self.f1, 11), anchor="ne")
		self.mimg(706, Y+15, "img_button2", tags=("leave_btn"), anchor="ne")	
		self.cn.tag_bind(self.m("leave_btn"), "<Button-1>", self.leave_perks_ui)
		for i in range(3):
			x = 94 + (i * 205)
			y = 210
			self.mimg(x, y, "s{}-203x300".format(i+1))
		self.mbtn(498, 178, "Save Perks", self.save_perks)
		self.mbtn(597, 178, "Cancel", self.reset_perks)
		self.cn.tag_lower(self.m("btn_Save Perks"))
		self.cn.tag_lower(self.m("btn_Cancel"))
		#self.cn.tag_bind(self.m("p1_ava"), "<Button-1>", self.save_perks)
		
		
	def leave_perks_ui(self, *args):
		self.cn.delete(self.mtag)
		self.extract()
		
	
	def reset_perks(self, *args):
		self.world.start_perks("THE_PLAYER", override=True)
		

	def hoverstats_perks_fade(self, stage=0, *args):
		if stage == 0:
			if self.go is not None:
				self.parent.after_cancel(self.go)
				self.go = None
			if self.go1 is not None:
				self.parent.after_cancel(self.go1)
				self.go1 = None
			self.go1 = self.parent.after(100, lambda: self.hoverstats_perks_fade(1))
		elif stage == 1:
			self.cn.delete(self.m("hover_stats"))
		
	
	def hoverstats_perks(self, x, y, perk, stage=0, *args):
		# separate to prevent crashing, crashes after called multiple times instead of once
		#self.cn.delete(self.m("hover_stats"))
		xn = x + 49
		yn = y - 7
		if stage == 0:
			if self.go is not None:
				self.parent.after_cancel(self.go)
				self.go = None
			self.go = self.parent.after(125, lambda: self.hoverstats_perks(x, y, perk, stage=1))
		elif stage == 1:
			pl = self.perksl
			pname = pl[perk]["name"]
			pdesc = pl[perk]["desc"]
			pdesc = "" if pdesc == None else pdesc
			paffects = ""
			for i in range(len(pl[perk]["affects"])):
				a = pl[perk]["affects"][i]
				c = pl[perk]["change"][i][:-3]
				z = pl[perk]["level"]
				paffects += "lvl: {}/{}".format(z[0], z[1])
				'''
				n = "+" if c > 0 else "-"
				z = "%" if pl[perk]["change"][i][-3:] == "(%)" else ""
				b = "{}{}{}".format(n, c, z)
				#x = " {}: {}".format(a, b)
				x = " {}".format(b)
				paffects += x
				'''
			mtag = "hover_stats"
			self.mimg(xn, yn, image="hover_stats", tags=mtag)
			self.mtxt(xn+5, yn+5, txt=pname, font=self.font1b, tags=mtag)
			self.mtxt(xn+7, yn+5+17, txt=pdesc, font=self.font2, tags=mtag, width=125)
			#self.make_txt(xn+150-5-67, yn-3+105, txt="Scnr:", font=self.font1, tags=mtag, anchor="se")
			self.mtxt(xn+150-5, yn-3+105, txt=paffects, font=self.font1, tags=mtag, anchor="se")
		
		
	def m(self, tag):
		return "{}_{}".format(self.mtag, tag)
	
	
	def check_tags(self, tags):
		# Input: ("a", "b")
		# Output: (mtag, "mtag_a", "mtag_b")
		if tags is None:
			tags = (self.mtag, self.gtag)
		elif isinstance(tags, str):  # string
			x = [self.m(tags)]
			tags = tuple([self.mtag, self.gtag] + x)
		else:
			x = []
			for i in tags:
				x.append(self.m(i))
			tags = tuple([self.mtag, self.gtag] + x)
		return tags
	
	
	def mbtn(self, x1, y1, text, command, w=None, *args):
		if w is None:
			w = 4 + (9 * len(text))
		tag = "btn_{}".format(text)
		self.mrect(x1, y1, w, 25, "white", tag, "black", 1)
		x2, y2 = x1 + (w / 2) - 1, y1 + 1
		self.mtxt(x2, y2, text, tag, anchor=tk.N, width=w)
		if command is not None:
			self.cn.tag_bind(self.m(tag), "<Button-1>", lambda _=1: command())
	
	
	def mrect(self, x1, y1, w, h, fill="black", tags=None, c=None, width=0):
		tags = self.check_tags(tags)  # must be tuple
		self.cn.create_rectangle(x1, y1, x1+w, y1+h, fill=fill, tags=tags,
			outline=c, width=width)
		
	
	def mimg(self, x, y, image, tags=None, anchor=tk.NW, *args):
		tags = self.check_tags(tags)  # must be tuple
		self.cn.create_image(x, y, image=self.rsc[image], tags=tags,
			anchor=anchor)
			
		
	def mtxt(self, x, y, txt, tags=None, font=None, anchor=tk.NW,
		fill="black", width=250, align="left", *args):
		tags = self.check_tags(tags)  # must be tuple
		font = (self.f1, self.fsz1) if font is None else font
		self.cn.create_text(x, y, text=txt, tags=tags, font=font,
			anchor=anchor, fill=fill, width=width, justify=align)			

	
class Places:
	def __init__(self, world, place, extract=None, startxy=None,
		mlmt=None, *arg, **kwarg):
		self.world = world
		self.parent = world.parent
		self.cn = world.cn
		self.extract = extract
		self.place = place
		self.sxy = self.world.world_places[place]["entry_coords"]
		if startxy != None:
			self.sxy = startxy
		self.mlmt = self.world.world_places[place]["walk_range"]
		if self.mlmt == "default":
			if self.world.world_places[self.place]["type"][0] == "outdoors":
				self.mlmt = (35, 300, 765, 535)
			else:
				self.mlmt = (75, 285, 725, 430)
		#self.sxy = startxy if startxy != None else (400, 375)
		#self.mlmt = mlmt if mlmt != None else (100, 270, 700, 550)  # move rect range
		# start the ui
		self.load_variables()
		self.load_place_ui()
		self.cn.bind("<Button-1>", self._interactp)
		#self.cn.tag_bind(self.zbox.m("pPlyr"), "<Button-1>",
		#	lambda _=1: self.world.start_player_inv())
		
	
	def _interactp(self, event, *args):
		id_num = self.cn.find_closest(event.x, event.y)[0]
		id_tags = self.cn.gettags(id_num)
		if self.zbox.m("place_image") in id_tags and not self.aktiv_ui:
			if self.place_move is not None:
				self.parent.after_cancel(self.place_move)
				self.place_move = None
			# calculate variables
			coords = self.cn.coords(self.zbox.m("pPlyr"))
			px, py = coords[0], coords[1]
			lx, ly = event.x, event.y - 80
			'''
			if (lx < self.mlmt[0] or lx >= self.mlmt[2] or
				ly < self.mlmt[1] or ly >= self.mlmt[3]):
				#return  # out of range  give max instead
			'''
			if lx < self.mlmt[0]: lx = self.mlmt[0]
			elif lx > self.mlmt[2]: lx = self.mlmt[2]
			if ly < self.mlmt[1]: ly = self.mlmt[1]
			elif ly > self.mlmt[3]: ly = self.mlmt[3]
			pimg = self.pdata["place_image"]
			speed = 7.25
			if self.world.world_places[self.place]["type"][0] != "outdoors":
				pimg = self.pdata["place_indoor_image"]
				speed = 6.19
			if lx < px:
				self.cn.itemconfigure(self.zbox.m("pPlyr"),
					image=self.rsc["{}-f".format(pimg)])
			else:
				self.cn.itemconfigure(self.zbox.m("pPlyr"),
					image=self.rsc[pimg])
			x, y = lx-px, ly-py
			dist = math.sqrt(abs(x)**2 + abs(y)**2)
			steps = dist / speed  # player speed 5.0 max
			ax = x / steps
			ay = y / steps
			evt = None
			for i in id_tags:
				txt = self.zbox.m("{}_P".format(self.place))
				if i[:len(txt)] == txt:
						try:
							evt = self.place_places[i]
						except:
							evt = None
						break
				'''
				try:
					if i[:len(txt)] == txt:
						evt = self.place_places[i]
						break
				except:
					print("_interact error")
				'''
			self._move2locp(ax, ay, steps, evt)
	
	
	def _move2locp(self, x_add, y_add, steps, evt=None, *args):
		if steps >= 0 and not self.aktiv_ui and not self.world.aktiv_caUI:
			self.cn.move(self.zbox.m("pPlyr"), x_add, y_add)
			steps -= 1
			self.place_move = self.parent.after(50, lambda _=1: 
				self._move2locp(x_add, y_add, steps, evt))
		elif steps < 0:
			self.place_move = None
			pimg = self.pdata["place_image"]
			if self.world.world_places[self.place]["type"][0] != "outdoors":
				pimg = self.pdata["place_indoor_image"]
			self.cn.itemconfigure(self.zbox.m("pPlyr"),
				image=self.rsc[pimg])
			if evt is not None:
				evt()
	
	
	def load_place_ui(self, *args):
		#self.zbox.mimg(0, 0, self.placedata["image"], "place_image")
		if self.world.world_places[self.place]["type"][0] == "outdoors":
			self.zbox.mimg(0, 0, self.world.world_places[self.place]["type"][1], "place_image")
			self.zbox.mimg(0, 330, self.world.world_places[self.place]["type"][2], "place_image")
		else:
			self.zbox.mrect(0, 0, 800, 600, fill="#331122", tags="place_image")
			for i in range(4):
				x = 50 + (i * 175)
				self.zbox.mimg(x, 100, self.world.world_places[self.place]["type"][1], "place_image")
				self.zbox.mimg(x, 350, self.world.world_places[self.place]["type"][2], "place_image")
		try:
			if self.placedata["leave_btn"]:
				self.zbox.mbtn(717, 548, "Leave", self._leave_place,
					w=80, h=48, font=(self.fn[0], 17), txty_change=8)
		except: pass  # no leave_btn
		e = self.placedata["events"]
		e1 = self.world.check_event_conditions(e)
		xc = 0
		for evt in e1:
			tag0 = "{}_P{}-{}".format(self.place, evt[2], xc)
			tag = self.zbox.m(tag0)
			xc += 1
			if evt[1] != None:  # event
				act = evt[1].split("|")
				if act[0] == "place":  # place
					command = lambda n=act[1], e=evt: self._go_plc(n, e)
				elif act[0] == "dialg":  # dialog
					command = lambda n=act[1], e=evt: self._go_dlg(n, e)
				elif act[0] == "store":  # store, trade between 2 characters
					command = lambda n=act[1], e=evt: self._go_str(n, e)
				elif act[0] == "chest":  # lootbox
					command = lambda n=act[1], e=evt: self._go_box(n, e)	
				elif act[0] == "leave":  # lootbox
					command = lambda _=1: self._leave_place()	
				self.place_places[tag] = command
				#self.cn.tag_bind(tag, "<Button-1>", command)
			# ie: "map_lurco-50x50|450, 200"
			img_data = evt[2].split("|")
			coords = [int(x) for x in img_data[1].split(",")]
			img = img_data[0]
			self.place_place(coords[0], coords[1], "", img, tag0, anchor="nw")
		pimg = self.pdata["place_image"]
		if self.world.world_places[self.place]["type"][0] != "outdoors":
			pimg = self.pdata["place_indoor_image"]
		self.zbox.mimg(self.sxy[0], self.sxy[1], pimg,
			"pPlyr", "center")	
		self.zbox.raise_ctags()
		self.cn.tag_raise(self.zbox.m("raise_tag"))
		self._reset_aktivui()
		
	
	def load_variables(self, *args):
		#self.place_list = self.world.map[self.world.current_region]["places"]
		self.place_list = self.world.world_places
		self.placedata = self.place_list[self.place]
		self.rsc = self.world.rsc
		self.mtag = "placeUI_{}".format(self.placedata["name"])
		self.pdata = self.world.characters["THE_PLAYER"]
		self.zbox = Ztoolbox(self.world)
		self.zbox.mtag = self.mtag
		self.phvr_t = None  # hover id
		self.place_move = None  # move id
		self.fn, self.fs = self.world.fn, self.world.fs
		self.place_places = {}
		self.aktiv_ui = False
	
	
	def place_place(self, x, y, pname, image, tag=None, anchor="center", *args):
		def phover(mode="enter", *args):
			tn = self.zbox.m(tag+"_txt")
			if self.phvr_t != None:
				self.parent.after_cancel(self.phvr_t)
				self.phvr_t = None
			if mode == "enter":
				self.phvr_t = self.parent.after(125,
					lambda _=1: self.cn.itemconfigure(tn, fill="yellow"))
			else:
				self.cn.itemconfigure(tn, fill="#441122")
		e = "no_raise"
		if y >= 450: e = "raise_tag"
		self.zbox.mimg(x, y, image, (tag, tag+"_img", "place_image", e),
			anchor=anchor)
		#h = int(image[-2:])  # height 99px max
		#h = int(image.split("-")[1].split("x")[1])
		#ha = -10 if h >= 100 else 5
		#add = (h / 2) + ha
		#self.zbox.mtxt(x, y-add, pname, (tag, tag+"_txt", "place_image"),
		#	(self.fn[0], 12), "center", fill="#441122")
		#tagn = self.zbox.m(tag+"_img")
		#tagn = self.zbox.m(tag)
		#self.cn.tag_bind(tagn, "<Enter>", lambda _=1: phover())
		#self.cn.tag_bind(tagn, "<Leave>", lambda _=1: phover("l"))
	
	
	def _go_box(self, container, after_event, *args):
		def lv_box(s=0, *args):
			if s == 0:
				self.aktiv_ui = True
				self.parent.after(100, lambda _=1: lv_box(1))
			else:
				self.aktiv_ui = False
		if not self.world.aktiv_caUI:
			self.world.check_event_events(after_event)
			self.aktiv_ui = True
			#bg = self.placedata["image"]
			self.world.start_tradebox(container, extract=lv_box)	
	
	
	def _go_dlg(self, dialog_id, after_event, *args):
		if not self.world.aktiv_caUI:
			#self.hoverstats_fade()
			#self.cn.delete(self.mtag)
			self.world.check_event_events(after_event)
			self.world.start_dialog(dialog_id)
	
	
	def _go_plc(self, evt, after_event, *args):
		self._leave_place()
		startxy = None
		edata = evt.split("*")
		evt_name = edata[0]
		if len(edata) > 1:
			a = edata[1].split(",")
			startxy = (int(a[0]), int(a[1]))
		self.world.check_event_events(after_event)	
		self.world.start_place(evt_name, startxy=startxy)
	
	
	def _go_str(self, merchant, after_event, *args):
		#def exit_str(*args):  # redundant
		#	pass
		def lv_str(s=0, *args):
			if s == 0:
				self.aktiv_ui = True
				self.parent.after(100, lambda _=1: lv_str(1))
			else:
				self.aktiv_ui = False
		if not self.world.aktiv_caUI:
			#self.zbox.mimg(0, 0, self.placedata["image"], "str_bg")  # redundant
			self.aktiv_ui = True
			self.world.check_event_events(after_event)
			self.world.start_store(merchant, extract=lv_str)
	
	
	def _leave_place(self, *args):
		if not self.world.aktiv_caUI:
			#self.hoverstats_fade()
			if self.place_move is not None:
				self.parent.after_cancel(self.place_move)
				self.place_move = None
			self.cn.delete(self.mtag)
			if self.extract is not None:
				self.extract()

	
	def _reset_aktivui(self, s=0, *args):
		if s == 0:
			self.aktiv_ui = True
			self.parent.after(100, lambda _=1: self._reset_aktivui(1))
		else:
			self.aktiv_ui = False
				

class Quests:
	def __init__(self, world, extract=None, *arg, **kwarg):
		self.world = world
		self.parent = world.parent
		self.cn = world.cn
		self.rsc = world.rsc
		self.extract = extract
		self.quests = self.world.quests
		# start the ui
		self.load_variables()
		self.load_basic_ui()
		self.set_akpages()
		self.set_fgpages()
		try: self.display_qinfo(self.aktivql[0])
		except: pass
		
	
	def load_basic_ui(self, *args):
		'''
		self.zbox.mimg(20, 50, "dtxt_bg-760x485")
		self.zbox.mimg(30, 61, "dtxt_txtbg-530x465")
		self.zbox.mimg(570, 61, "dtxt_choices-200x466")
		'''
		self.zbox.mrect(20, 50, 760, 485, fill="white", width=2)
		self.zbox.mrect(30, 61, 530, 465, fill="white", width=1)
		self.zbox.mrect(570, 61, 200, 466, fill="white", width=1)
		#self.zbox.mtxt(40, 81, "", "title", font=(self.fn[0], 15, "bold"))
		self.zbox.mtxt(295, 81, "", "title", font=(self.fn[0], 15, "bold"), anchor="n")
		self.zbox.mtxt(40, 120, "", "text", width=510)
		self.zbox.mtxt(42, 410, "", "rwd_text", self.ftheme[1], width=510)
		self.zbox.mtxt(670, 120, "Active Quests", None,
			(self.fn[0], 15), "center")
		self.zbox.mtxt(630, 242, "<<<", "ak<<<", (self.fn[1], 16), "center")
		self.zbox.mtxt(710, 242, ">>>", "ak>>>", (self.fn[1], 16), "center")
		tag0 = "leave_btn"
		tagl = self.zbox.m(tag0)
		y = 68
		self.zbox.mrect(575, y, 190, 30, "white", (tag0, tag0+"_rect"), width=1)
		self.zbox.mtxt(670, y+14, "Exit Quests Screen",
			(tag0, tag0+"_txt"), (self.fn[1], 14), "center")
		self.cn.tag_bind(tagl, "<Enter>", 
			lambda _=1: self.cn.itemconfigure(self.zbox.m(tag0+"_rect"), width=2))
		self.cn.tag_bind(tagl, "<Leave>",
			lambda _=1: self.cn.itemconfigure(self.zbox.m(tag0+"_rect"), width=1))
		self.cn.tag_bind(tagl, "<Button-1>", self._leave_quest)
		self.zbox.mtxt(670, 312, "Completed Quests", None,
			(self.fn[0], 14), "center")
		self.zbox.mtxt(630, 502, "<<<", "fg<<<", (self.fn[1], 16), "center")
		self.zbox.mtxt(710, 502, ">>>", "fg>>>", (self.fn[1], 16), "center")
		self.cn.tag_bind(self.zbox.m("ak<<<"), "<Button-1>", lambda _=1: self.change_akpage(-1))
		self.cn.tag_bind(self.zbox.m("ak>>>"), "<Button-1>", lambda _=1: self.change_akpage(1))
		self.cn.tag_bind(self.zbox.m("fg<<<"), "<Button-1>", lambda _=1: self.change_fgpage(-1))
		self.cn.tag_bind(self.zbox.m("fg>>>"), "<Button-1>", lambda _=1: self.change_fgpage(1))
	
	
	def change_akpage(self, page_change, *args):
		if page_change == -1:
			if (self.current_page_akq - 1) >= 0:
				self.set_akpages(self.current_page_akq - 1)
				self.current_page_akq -= 1
				self.cn.delete(self.zbox.m("rwd_item"))
				self.cn.itemconfigure(self.zbox.m("rwd_text"), text="")
		elif page_change == 1:
			if self.current_page_akq < self.aql_pages:
				self.set_akpages(self.current_page_akq + 1)
				self.current_page_akq += 1
				self.cn.delete(self.zbox.m("rwd_item"))
				self.cn.itemconfigure(self.zbox.m("rwd_text"), text="")
	
	
	def change_fgpage(self, page_change, *args):
		if page_change == -1:
			if (self.current_page_fgq - 1) >= 0:
				self.set_fgpages(self.current_page_fgq - 1)
				self.current_page_fgq -= 1
				self.cn.delete(self.zbox.m("rwd_item"))
				self.cn.itemconfigure(self.zbox.m("rwd_text"), text="")
		elif page_change == 1:
			if self.current_page_fgq < self.fql_pages:
				self.set_fgpages(self.current_page_fgq + 1)
				self.current_page_fgq += 1
				self.cn.delete(self.zbox.m("rwd_item"))
				self.cn.itemconfigure(self.zbox.m("rwd_text"), text="")
				
	
	def set_akpages(self, page=0, *args):
		self.cn.delete(self.zbox.m("akitem"))
		ci = "dtxt_choice-190x30"
		ci2 = "dtxt_choiceO-190x30"
		def qhover(tag, mode=1, *args):
			t = self.zbox.m(tag+"_img")
			if self.qhvr_t != None:
				self.parent.after_cancel(self.qhvr_t)
				self.qhvr_t = None
			if mode == 1:
				self.qhvr_t = self.parent.after(25,
					lambda _=1: self.cn.itemconfigure(t, image=self.rsc[ci2]))
			else: self.cn.itemconfigure(t, image=self.rsc[ci])
		inum = 0
		for i in range(4):  # aktiv quests per page
			iindex = i + (4 * page)
			try:
				if self.aktivql[iindex] == "":
					continue
				qname = self.aktivql[iindex]
			except: continue
			tag0 = "qitem_{}".format(qname)
			tag = self.zbox.m(tag0)
			x = 135
			self.zbox.mimg(575, x+(i*33), ci, (tag0, tag0+"_img", "akitem"))
			self.zbox.mtxt(582, x+5+(i*33), self.quests[qname]["name"], (tag0, "akitem"))
			#self.cn.tag_bind(tag, "<Enter>", lambda _=1, t=tag0: qhover(t))
			#self.cn.tag_bind(tag, "<Leave>", lambda _=1, t=tag0: qhover(t, 0))
			self.cn.tag_bind(tag, "<Button-1>", 
				lambda _=1, n=qname: self.display_qinfo(n))
			inum += 1
		if inum < 4: self.cn.itemconfigure(self.zbox.m("ak>>>"), text="")
		else: self.cn.itemconfigure(self.zbox.m("ak>>>"), text=">>>")
		if page <= 0: self.cn.itemconfigure(self.zbox.m("ak<<<"), text="")
		else: self.cn.itemconfigure(self.zbox.m("ak<<<"), text="<<<")
		
		
	def set_fgpages(self, page=0, *args):
		self.cn.delete(self.zbox.m("fgitem"))
		ci = "dtxt_choice-190x30"
		ci2 = "dtxt_choiceO-190x30"
		def qhover(tag, mode=1, *args):
			t = self.zbox.m(tag+"_img")
			if self.qhvr_t != None:
				self.parent.after_cancel(self.qhvr_t)
				self.qhvr_t = None
			if mode == 1:
				self.qhvr_t = self.parent.after(25,
					lambda _=1: self.cn.itemconfigure(t, image=self.rsc[ci2]))
			else: self.cn.itemconfigure(t, image=self.rsc[ci])
		jnum = 0
		for i in range(5):  # fertig quests per page
			iindex = i + (5 * page)
			try:
				if self.fertigql[iindex] == "":
					continue
				qname = self.fertigql[iindex]
			except: continue
			tag0 = "qitem_{}".format(qname)
			tag = self.zbox.m(tag0)
			x = 327
			self.zbox.mimg(575, x+(i*33), ci, (tag0, tag0+"_img", "fgitem"))
			self.zbox.mtxt(582, x+5+(i*33), self.quests[qname]["name"], (tag0, "fgitem"))
			#self.cn.tag_bind(tag, "<Enter>", lambda _=1, t=tag0: qhover(t))
			#self.cn.tag_bind(tag, "<Leave>", lambda _=1, t=tag0: qhover(t, 0))
			self.cn.tag_bind(tag, "<Button-1>", 
				lambda _=1, n=qname: self.display_qinfo(n))
			jnum += 1
		if jnum < 4: self.cn.itemconfigure(self.zbox.m("fg>>>"), text="")
		else: self.cn.itemconfigure(self.zbox.m("fg>>>"), text=">>>")
		if page <= 0: self.cn.itemconfigure(self.zbox.m("fg<<<"), text="")
		else: self.cn.itemconfigure(self.zbox.m("fg<<<"), text="<<<")
		
		
	'''
	def set_pages(self, akqpage=0, fgqpage=0, *args):
		ci = "dtxt_choice-190x30"
		ci2 = "dtxt_choiceO-190x30"
		def qhover(tag, mode=1, *args):
			t = self.zbox.m(tag+"_img")
			if self.qhvr_t != None:
				self.parent.after_cancel(self.qhvr_t)
				self.qhvr_t = None
			if mode == 1:
				self.qhvr_t = self.parent.after(25,
					lambda _=1: self.cn.itemconfigure(t, image=self.rsc[ci2]))
			else: self.cn.itemconfigure(t, image=self.rsc[ci])
		inum = 0
		for i in range(4):  # aktiv quests per page
			iindex = i + (akqpage * i)
			try:
				if self.aktivql[iindex] == "":
					continue
				qname = self.aktivql[iindex]
			except: continue
			tag0 = "qitem_{}".format(qname)
			tag = self.zbox.m(tag0)
			x = 100
			self.zbox.mimg(575, x+(i*33), ci, (tag0, tag0+"_img"))
			self.zbox.mtxt(582, x+5+(i*33), self.quests[qname]["name"], tag0)
			self.cn.tag_bind(tag, "<Enter>", lambda _=1, t=tag0: qhover(t))
			self.cn.tag_bind(tag, "<Leave>", lambda _=1, t=tag0: qhover(t, 0))
			self.cn.tag_bind(tag, "<Button-1>", 
				lambda _=1, n=qname: self.display_qinfo(n))
			inum += 1
		if inum < 4: self.cn.itemconfigure(self.zbox.m("ak>>>"), text="")
		if akqpage <= 0: self.cn.itemconfigure(self.zbox.m("ak<<<"), text="")
		jnum = 0
		for i in range(5):  # fertig quests per page
			iindex = i + (fgqpage * i)
			try:
				if self.fertigql[iindex] == "":
					continue
				qname = self.fertigql[iindex]
			except: continue
			tag0 = "qitem_{}".format(qname)
			tag = self.zbox.m(tag0)
			x = 327
			self.zbox.mimg(575, x+(i*33), ci, (tag0, tag0+"_img"))
			self.zbox.mtxt(582, x+5+(i*33), self.quests[qname]["name"], tag0)
			self.cn.tag_bind(tag, "<Enter>", lambda _=1, t=tag0: qhover(t))
			self.cn.tag_bind(tag, "<Leave>", lambda _=1, t=tag0: qhover(t, 0))
			self.cn.tag_bind(tag, "<Button-1>", 
				lambda _=1, n=qname: self.display_qinfo(n))
			jnum += 1
		if jnum < 4: self.cn.itemconfigure(self.zbox.m("fg>>>"), text="")
		if fgqpage <= 0: self.cn.itemconfigure(self.zbox.m("fg<<<"), text="")
	'''
	
		
	def display_qinfo(self, qinfo, *args):
		self.cn.delete(self.zbox.m("rwd_item"))
		ci = "dtxt_choice-190x30"
		ci2 = "dtxt_choiceO-190x30"
		tag = "qitem_{}".format(qinfo)
		t = self.zbox.m(tag+"_img")
		for i in self.aktivql:
			t1 = self.zbox.m("qitem_"+i+"_img")
			self.cn.itemconfigure(t1, image=self.rsc[ci])
		for i in self.fertigql:
			t1 = self.zbox.m("qitem_"+i+"_img")
			self.cn.itemconfigure(t1, image=self.rsc[ci])	
		self.cn.itemconfigure(t, image=self.rsc[ci2])
		
		qdata = self.quests[qinfo]
		qtitle = qdata["name"]
		qstage = qdata["stage"][0]
		qtitle = qdata["name"]
		qtext = qdata["stage{}".format(qstage)][0]
		self.cn.itemconfigure(self.zbox.m("title"), text=qtitle)
		self.cn.itemconfigure(self.zbox.m("text"), text=qtext)
		if qstage != qdata["stage"][1]:
			self.cn.itemconfigure(self.zbox.m("rwd_text"), text="")
			return  # show reward after quest
		rwd = qdata["reward"]  # exp gold items
		rtxt = "Reward:    {}coin(s),  {}exp".format(rwd[1], rwd[0])
		self.cn.itemconfigure(self.zbox.m("rwd_text"), text=rtxt)
		for i in range(len(rwd[2])):
			x, y = 42 + (i * 47), 435
			img = self.items[rwd[2][i]]["image"]
			tag0 = "{}{}".format(rwd[2][i], i)
			tag = self.zbox.m(tag0)
			self.zbox.mimg(x, y, img, (tag0, "rwd_item"))
			self.cn.tag_bind(tag, "<Enter>",
				lambda _=1, x=x, y=y, n=rwd[2][i]: self._hvr_inv(x, y, n))
			self.cn.tag_bind(tag, "<Leave>", self._hvr_fade)
			
	
	def load_variables(self, *args):
		self.mtag = "questUI"
		self.pdata = self.world.characters["THE_PLAYER"]
		self.zbox = Ztoolbox(self.world)
		self.zbox.mtag = self.mtag
		self.items = self.world.items
		# reversed to show latest
		self.aktivql = self.world.aktivql[::-1]
		self.fertigql = self.world.fertigql[::-1]
		# to give only 0 as remainder
		self.aktivql += [""] * (len(self.aktivql) % 4)
		self.fertigql += [""] * (len(self.aktivql) % 5)
		self.aql_pages = len(self.aktivql) // 4 
		self.fql_pages = len(self.fertigql) // 5
		# font names, sizes, themes
		self.fn, self.fs = self.world.fn, self.world.fs
		self.ftheme = self.world.ftheme
		self.qhvr_t = None  # qhover id
		self.ihvr_t = None  # hover id
		self.current_page_akq = 0
		self.current_page_fgq = 0
	
	
	def zibox(self, x, y, item, buyorsell=1, *args):  # item hover box
		tag = "hover_obj"
		inm = self.items[item]["name"]
		if self.items[item]["type"] != None: itp = self.items[item]["type"]
		else: itp = "???"
		if self.items[item]["descr"] != None: ids = self.items[item]["descr"]
		else: ids = "?????"
		if self.items[item]["price"] != None:
			ipr = self.items[item]["price"][buyorsell]
		else: ipr = "???"
		sn = sv = ""
		if itp == "armor": sn, sv = "D:", self.items[item]["defense_value"]
		elif itp == "potion": sn, sv = "H:", self.items[item]["heal_value"]
		elif itp == "weapon": sn, sv = "A:", self.items[item]["attack_value"]
		# what it means when cat curls its tail
		# add later
		self.zbox.mimg(x, y, "hover_stats", tag)
		'''
		self.zbox.mrect(x+3, y+3, 144, 78, "#776611", tag)
		self.zbox.mrect(x+3, y+81, 49, 21, "#774411", tag)
		self.zbox.mrect(x+52, y+81, 95, 21, "#773311", tag)
		'''
		self.zbox.mrect(x+3, y+3, 144, 78, "white", tag)
		self.zbox.mrect(x+3, y+81, 49, 21, "white", tag)
		self.zbox.mrect(x+52, y+81, 95, 21, "white", tag)
		self.zbox.mtxt(x+5, y+4, inm, tag, self.ftheme[1])
		self.zbox.mtxt(x+7, y+18, itp, tag, (self.fn[1], 9))
		self.zbox.mtxt(x+5, y+30, ids, tag, (self.fn[0], 11), width=140)
		self.zbox.mtxt(x+5, y+102, sn, tag, anchor="sw")
		self.zbox.mtxt(x+48, y+102, sv, tag, anchor="se")
		self.zbox.mtxt(x+95, y+102, "Scnr:", tag, anchor="se")
		self.zbox.mtxt(x+145, y+102, ipr, tag, anchor="se")
	
	
	def _hvr_fade(self, *args):
		if self.ihvr_t is not None:
			self.parent.after_cancel(self.ihvr_t)
			self.ihvr_t = None
		self.cn.delete(self.zbox.m("hover_obj"))
	
	
	def _hvr_inv(self, x, y, iname, invn=0, stage=0, *args):
		xn = (x + 47) if (x + 152) < 760 else (x - 152)
		yn = y - 7
		if stage == 0:
			self._hvr_fade()
			self.ihvr_t = self.parent.after(325,
				lambda: self._hvr_inv(x, y, iname, invn, stage=1))
		elif stage == 1:
			self.zibox(xn, yn, iname)
	
	
	def _leave_quest(self, *args):
		#if not self.world.aktiv_caUI:
		self.cn.delete(self.mtag)
		if self.extract is not None:
			self.extract()	
		
				
class Stores:  # COMPLETED
	def __init__(self, world, merchant, extract=None, *arg, **kwarg):
		self.world = world
		self.parent = world.parent
		self.cn = world.cn
		self.rsc = world.rsc
		self.extract = extract
		self.merchant = merchant
		self.load_variables()
		self.load_store_basic_ui()
		self.update_ui()
	
	
	def barter(self, *args):
		txt_color = self.cn.itemcget(self.zbox.m("b_brtr_txt"), "fill")
		if txt_color == "black" and (self.sell_val != 0 or self.buy_val != 0):
			ev = self.buy_val - self.sell_val
			self.pdata["coin"] = self.pdata["coin"] - (ev)
			self.mdata["coin"] = self.mdata["coin"] + (ev)
			self.pescrow, self.mescrow = [], []
			self.update_ui()
			self._gold_glow()
	
	
	def barter_status(self, *args):
		self.sell_val, self.buy_val = 0, 0
		for item in self.pescrow:
			self.sell_val += self.items[item]["price"][1]
		for item in self.mescrow:
			self.buy_val += self.items[item]["price"][0]
		ev = self.buy_val - self.sell_val
		pgleft = self.pdata["coin"] - (ev)
		mgleft = self.mdata["coin"] + (ev)
		p_hasgold = True if pgleft >= 0 else False
		m_hasgold = True if mgleft >= 0 else False
		self.cn.itemconfigure(self.zbox.m("b_brtr_txt"), fill="green")
		self.cn.itemconfigure(self.zbox.m("brtr_txt"), fill="green")
		tgs = ["stat_brtr"]
		if p_hasgold and m_hasgold: tgs.append("b_brtr_txt")
		if p_hasgold: tgs.append("stat_pbuy")
		if m_hasgold: tgs.append("stat_mbuy")
		for i in tgs:
			self.cn.itemconfigure(self.zbox.m(i), fill="black")
		data = [
			["stat_pbuy", "You need {} more Sconarii".format(abs(pgleft))],
			["stat_mbuy", "They need {} more Sconarii".format(abs(mgleft))],
			["stat_brtr", "You will give or receive Sconarii"],
			["stat_pinv", "Your inventory has space"],
			["stat_minv", "Their inventory has space"],
		]
		if p_hasgold: data[0][1] = "You have enough Sconarii"
		if m_hasgold: data[1][1] = "They have enough Sconarii"
		if ev > 0: 
			data[2][1] = "You must pay {} Sconarii".format(ev)
		elif ev < 0:
			data[2][1] = "You will receive {} Sconarii".format(abs(ev))
		if self.buy_val > 0:
			data[3][1] = "Buying items worth {} coins".format(self.buy_val)
		if self.sell_val > 0:
			data[4][1] = "Selling items worth {} coins".format(self.sell_val)
		for i in range(len(data)):
			self.cn.itemconfigure(self.zbox.m(data[i][0]), text=data[i][1])
	

	def load_store_basic_ui(self, *args):
		# prepare variables
		aimg, wimg = "invi_earmor", "invi_eweapon"
		if self.pdata["equipped"][1] != None: 
			aimg = self.items[self.pdata["equipped"][1]]["image"]
		if self.pdata["equipped"][4] != None: 
			wimg = self.items[self.pdata["equipped"][4]]["image"]
		pnm = self.pdata["name"]
		plvl = self.pdata["stats"][5] // 1000
		pcoin = self.pdata["coin"]
		# build the ui
		#self.zbox.mimg(20, 50, "dtxt_bg-760x485")
		#self.zbox.mimg(20, 50, "dtxt_upbar-760x25")
		self.zbox.mrect(20, 60, 760, 475, fill="white", width=2)
		# player info panel
		X, Y = 45, 93
		self.zbox.mrect(X, Y, 280, 105, fill="white", width=2)
		self.zbox.mimg(X, Y, self.pdata["avatar"])
		self.zbox.mimg(X+182, Y+23, aimg, "parmor")
		self.zbox.mimg(X+229, Y+23, wimg, "pweapon")
		
		if self.pdata["equipped"][1] != None: 
			self.cn.tag_bind(self.zbox.m("parmor"), "<Enter>",
				lambda _=1: self._hvr_inv(227, 116, 1, 2))
			self.cn.tag_bind(self.zbox.m("parmor"), "<Leave>", self._hvr_fade)	
		if self.pdata["equipped"][4] != None: 
			print("called0")
			self.cn.tag_bind(self.zbox.m("pweapon"), "<Enter>",
				lambda _=1: self._hvr_inv(274, 116, 4, 2))
			self.cn.tag_bind(self.zbox.m("pweapon"), "<Leave>", self._hvr_fade)	
		
		self.zbox.mtxt(X+103, Y+7, pnm, font=self.ftheme[1])
		self.zbox.mtxt(X+95, Y+83, plvl, "plvl", self.ftheme[1], "ne")
		self.zbox.mtxt(X+185, Y+5, "Scnr:", font=self.ftheme[0])
		self.zbox.mtxt(X+270, Y+5, pcoin, "pcoin", self.ftheme[0], "ne")
		x0, y0 = X + 104, Y + 29
		pstats = self.pdata["stats"]
		a = [
			["", "{}/{}".format(pstats[0][0], pstats[0][1])],
			["Atk", "{}".format(int(pstats[4]))],
			["Def", "{}".format(int(pstats[3]))],
		]
		for i in range(len(a)):
			self.zbox.mrect(x0, y0+(i*23), 74, 21, fill="white", width=1)
			self.zbox.mtxt(x0+2, y0+(i*23), a[i][0], font=self.ftheme[2])
			self.zbox.mtxt(x0+70, y0+(i*23), a[i][1], font=self.ftheme[2],
				anchor="ne")
		# player inventory
		inv1 = self.pdata["inventory"]
		pnv = inv1 + ["e"] * (24 - len(inv1))
		X1, Y1 = X, Y + 110
		for rw in range(4):
			for cl in range(6):
				n = cl + (rw * 6)
				p = self.items[pnv[n]]["image"] if pnv[n] != "e" else "inv_empty-45x75"
				x, y = X1+(cl*47), Y1+(rw*77)
				invslot_tag0 = "pinv_slot{}".format(n)
				invslot_tag = self.zbox.m("pinv_slot{}".format(n))
				self.zbox.mimg(x, y, p, invslot_tag0)
				self.cn.tag_bind(invslot_tag, "<Button-1>",
					lambda _, n=n: self.transfer_item(n, 1))
				self.cn.tag_bind(invslot_tag, "<Enter>",
					lambda _, x=x, y=y, n=n: self._hvr_inv(x, y, n, 0))
				self.cn.tag_bind(invslot_tag, "<Leave>", self._hvr_fade)
		# merchant info panel
		m = self.mdata
		X2, Y2 = 475, 93
		#self.zbox.mimg(X2, Y2, "inv_cbg-280x105")
		self.zbox.mrect(X2, Y2, 280, 105, fill="white", width=2)
		self.zbox.mimg(X2+180, Y2, m["avatar"])
		self.zbox.mimg(X2+6, Y2+23, "btn_think-45x75", "b_reset")
		self.zbox.mimg(X2+53, Y2+23, "btn_leave-45x75", "b_leave")
		self.cn.tag_bind(self.zbox.m("b_reset"), "<Button-1>", self.reset_inv)
		self.cn.tag_bind(self.zbox.m("b_leave"), "<Button-1>", self._exit_str)
		self.zbox.mtxt(X2+103, Y2+7, m["name"], font=self.ftheme[1])
		self.zbox.mtxt(X2+9, Y2+5, "Scnr:")
		self.zbox.mtxt(X2+94, Y2+5, m["coin"], "mcoin", anchor="ne")
		x1, y1 = X2 + 102, Y2 + 29
		for i in range(3): self.zbox.mrect(x1, y1+(i*23), 74, 21, "white", width=1)
		# merchant inventory
		inv2 = m["inventory"]
		mnv = inv2 + ["e"] * (24 - len(inv2))
		X3, Y3 = X2, Y2 + 110
		for rw in range(4):
			for cl in range(6):
				n = cl + (rw * 6)
				p = self.items[mnv[n]]["image"] if mnv[n] != "e" else "inv_empty-45x75"
				x, y = X3+(cl*47), Y3+(rw*77)
				invslot_tag0 = "minv_slot{}".format(n)
				invslot_tag = self.zbox.m("minv_slot{}".format(n))
				self.zbox.mimg(x, y, p, invslot_tag0)
				self.cn.tag_bind(invslot_tag, "<Button-1>",
					lambda _, n=n: self.transfer_item(n, 0))
				self.cn.tag_bind(invslot_tag, "<Enter>",
					lambda _, x=x, y=y, n=n: self._hvr_inv(x, y, n, 1))
				self.cn.tag_bind(invslot_tag, "<Leave>", self._hvr_fade)
		# middle display
		self.zbox.mimg(400, 275, "btn_store-85x45", "b_brtr", anchor="center")
		self.cn.tag_bind(self.zbox.m("b_brtr"), "<Button-1>", self.barter)
		self.zbox.mtxt(400, 275, "Barter", ("b_brtr", "b_brtr_txt"),
			self.ftheme[4], "center")
		w = 135
		self.zbox.mtxt(400, 150, "You have enough Sconarii",
			("stat_pbuy", "brtr_txt"), anchor="n", width=w, align="center")
		self.zbox.mtxt(400, 200, "You will give or receive Sconarii",
			("stat_brtr", "brtr_txt"), anchor="n", width=w, align="center")
		self.zbox.mtxt(400, 310, "They have enough Sconarii",
			("stat_mbuy", "brtr_txt"), anchor="n", width=w, align="center")
		self.zbox.mtxt(400, 360, "Your inventory has space",
			("stat_pinv"), anchor="n", width=w, align="center")
		self.zbox.mtxt(400, 410, "Their inventory has space",
			("stat_minv"), anchor="n", width=w, align="center")
		self.zbox.raise_ctags()
		
	
	def load_variables(self, *args):
		self.items = self.world.items
		self.pdata = copy.deepcopy(self.world.characters["THE_PLAYER"])
		self.mdata = copy.deepcopy(self.world.characters[self.merchant])
		self.mtag = "storeUI_{}".format(self.merchant)
		self.zbox = Ztoolbox(self.world)
		self.zbox.mtag = self.mtag
		self.ihvr_t = None  # hover id
		self.fn, self.fs = self.world.fn, self.world.fs
		self.ftheme = self.world.ftheme
		self.pescrow, self.mescrow = [], []
	

	def reset_inv(self, *args):
		for i in range(len(self.pescrow)):
			self.pdata["inventory"].append(self.pescrow[i])	
		for i in range(len(self.pescrow)):
			x = self.mdata["inventory"].index(self.pescrow[i])
			del self.mdata["inventory"][x]
		for i in range(len(self.mescrow)):
			self.mdata["inventory"].append(self.mescrow[i])
		for i in range(len(self.mescrow)):
			x = self.pdata["inventory"].index(self.mescrow[i])
			del self.pdata["inventory"][x]
		self.buy_val, self.sell_val = 0, 0
		self.pescrow, self.mescrow = [], []
		self.update_ui()
		
	
	def transfer_item(self, iindex, receiver_invn, *args):
		rinv = receiver_invn
		sinv = 0 if rinv == 1 else 1
		try:
			inv = [self.pdata["inventory"], self.mdata["inventory"]]
			escrow = (self.pescrow, self.mescrow)
			if len(inv[rinv]) < 24:
				inv[rinv].append(inv[sinv][iindex])
				if inv[sinv][iindex] in escrow[rinv]:  # give item back
					del escrow[rinv][escrow[rinv].index(inv[sinv][iindex])]
				else:
					escrow[sinv].append(inv[sinv][iindex])  # to calc price
				del inv[sinv][iindex]
		except: pass  # empty slot
		self.update_ui()
		self._hvr_again(iindex, sinv)
	
	
	def update_ui(self, *args):
		inv0, inv1 = self.pdata["inventory"], self.mdata["inventory"]
		pnv = inv0 + ["e"] * (24 - len(inv0))
		mnv = inv1 + ["e"] * (24 - len(inv1))
		for rw in range(4):
			for cl in range(6):
				n = cl + (rw * 6)
				pnvimg = mnvimg = "inv_empty-45x75"
				if pnv[n] != "e": pnvimg = self.items[pnv[n]]["image"]
				if mnv[n] != "e": mnvimg = self.items[mnv[n]]["image"]
				ptag = self.zbox.m("pinv_slot{}".format(n))
				mtag = self.zbox.m("minv_slot{}".format(n))
				self.cn.itemconfigure(ptag, image=self.rsc[pnvimg])
				self.cn.itemconfigure(mtag, image=self.rsc[mnvimg])
		self.cn.itemconfigure(self.zbox.m("pcoin"), text=self.pdata["coin"])
		self.cn.itemconfigure(self.zbox.m("mcoin"), text=self.mdata["coin"])
		self._hvr_fade()
		self.barter_status()
	

	def zibox(self, x, y, item, buyorsell, *args):  # item hover box
		tag = "hover_obj"
		inm = self.items[item]["name"]
		if self.items[item]["type"] != None: itp = self.items[item]["type"]
		else: itp = "???"
		if self.items[item]["descr"] != None: ids = self.items[item]["descr"]
		else: ids = "?????"
		if self.items[item]["price"] != None:
			ipr = self.items[item]["price"][buyorsell]
		else: ipr = "???"
		sn = sv = ""
		if itp == "armor": sn, sv = "D:", self.items[item]["defense_value"]
		elif itp == "potion": sn, sv = "H:", self.items[item]["heal_value"]
		elif itp == "weapon": sn, sv = "A:", self.items[item]["attack_value"]
		# what it means when cat curls its tail
		# add later
		self.zbox.mimg(x, y, "hover_stats", tag)
		'''
		self.zbox.mrect(x+3, y+3, 144, 78, "#776611", tag)
		self.zbox.mrect(x+3, y+81, 49, 21, "#774411", tag)
		self.zbox.mrect(x+52, y+81, 95, 21, "#773311", tag)
		'''
		self.zbox.mtxt(x+5, y+4, inm, tag, self.ftheme[1])
		self.zbox.mtxt(x+7, y+18, itp, tag, (self.fn[1], 9))
		self.zbox.mtxt(x+5, y+30, ids, tag, (self.fn[0], 11), width=140)
		self.zbox.mtxt(x+5, y+102, sn, tag, anchor="sw")
		self.zbox.mtxt(x+48, y+102, sv, tag, anchor="se")
		self.zbox.mtxt(x+95, y+102, "Scnr:", tag, anchor="se")
		self.zbox.mtxt(x+145, y+102, ipr, tag, anchor="se")

	
	def _exit_str(self, *args):
		self.reset_inv()
		self.cn.delete(self.mtag)
		self.extract()
	

	def _gold_glow(self, glowing=False, *args):
		tag = self.zbox.m("pcoin")
		if glowing:
			self.cn.itemconfigure(tag, fill="black")
		else:
			self.cn.tag_raise(tag)
			self.cn.itemconfigure(tag, fill="green")
			self.parent.after(500, lambda: self._gold_glow(True))
	
	
	def _hvr_again(self, iindex, invn, *args):
		rw = iindex // 6
		cl = iindex % 6
		X, Y = 45, 203  # p inv start
		if invn == 1: X, Y = 475, 203
		x, y = X+(cl*47), Y+(rw*77)
		self._hvr_inv(x, y, iindex, invn)
	
	
	def _hvr_fade(self, *args):
		if self.ihvr_t is not None:
			self.parent.after_cancel(self.ihvr_t)
			self.ihvr_t = None
		self.cn.delete(self.zbox.m("hover_obj"))
	
	
	def _hvr_inv(self, x, y, iindex, invn, stage=0, *args):
		xn = (x + 47) if (x + 152) < 760 else (x - 152)
		yn = y - 7
		inv0 = [self.pdata["inventory"], self.mdata["inventory"], self.pdata["equipped"]]
		inv = [[], [], []]
		inv[0] = inv0[0] + ["e"] * (24 - len(inv0[0]))
		inv[1] = inv0[1] + ["e"] * (24 - len(inv0[1]))
		for i in range(len(inv0[2])):
			if inv0[2][i] == None:
				inv[2].append("e")
			else:
				inv[2].append(inv0[2][i])
		if inv[invn][iindex] != "e":
			if stage == 0:
				self._hvr_fade()
				self.ihvr_t = self.parent.after(325,
					lambda: self._hvr_inv(x, y, iindex, invn, stage=1))
			elif stage == 1:
				n = 1 if invn == 0 else 0
				self.zibox(xn, yn, inv[invn][iindex], n)
		

class Tradebox:
	def __init__(self, world, container, extract=None, *arg, **kwarg):
		self.world = world
		self.parent = world.parent
		self.cn = world.cn
		self.rsc = world.rsc
		self.extract = extract
		self.container = container
		self.load_variables()
		self.load_basic_ui()
		self.update_ui()
		
	
	def load_basic_ui(self, *args):
		# prepare variables
		aimg, wimg = "invi_earmor", "invi_eweapon"
		if self.pdata["equipped"][1] != None: aimg = self.items[self.pdata["equipped"][1]]["image"]
		if self.pdata["equipped"][4] != None: wimg = self.items[self.pdata["equipped"][4]]["image"]
		pnm = self.pdata["name"]
		plvl = self.pdata["stats"][5] // 1000
		pcoin = self.pdata["coin"]
		# build the ui
		#self.zbox.mimg(400, 50, "trdbox_bg-635x485", anchor="n")
		#self.zbox.mimg(400, 50, "trdbox_upbar-635x25", anchor="n")
		self.zbox.mrect(84, 75, 635, 454, fill="white", width=2)
		# player info panel
		X, Y = 109, 95
		#self.zbox.mimg(X, Y, "inv_cbg-280x105")
		self.zbox.mrect(X, Y, 280, 105, fill="white", width=2)
		self.zbox.mimg(X, Y, self.pdata["avatar"])
		self.zbox.mimg(X+182, Y+23, aimg, "parmor")
		self.zbox.mimg(X+229, Y+23, wimg, "pweapon")
		if self.pdata["equipped"][1] != None: 
			self.cn.tag_bind(self.zbox.m("parmor"), "<Enter>",
				lambda _=1: self._hvr_inv(227, 116, 1, 2))
			self.cn.tag_bind(self.zbox.m("parmor"), "<Leave>", self._hvr_fade)	
		if self.pdata["equipped"][4] != None: 
			print("called0")
			self.cn.tag_bind(self.zbox.m("pweapon"), "<Enter>",
				lambda _=1: self._hvr_inv(274, 116, 4, 2))
			self.cn.tag_bind(self.zbox.m("pweapon"), "<Leave>", self._hvr_fade)	
		self.zbox.mtxt(X+103, Y+7, pnm, font=self.ftheme[1])
		self.zbox.mtxt(X+95, Y+83, plvl, "plvl", self.ftheme[1], "ne")
		self.zbox.mtxt(X+185, Y+5, "Scnr:", font=self.ftheme[0])
		self.zbox.mtxt(X+270, Y+5, pcoin, "pcoin", self.ftheme[0], "ne")
		x0, y0 = X + 104, Y + 29
		pstats = self.pdata["stats"]
		a = [
			["", "{}/{}".format(pstats[0][0], pstats[0][1])],
			["Atk", "{}".format(int(pstats[4]))],
			["Def", "{}".format(int(pstats[3]))],
		]
		for i in range(len(a)):
			self.zbox.mrect(x0, y0+(i*23), 74, 21, fill="white", width=1)
			self.zbox.mtxt(x0+2, y0+(i*23), a[i][0], font=self.ftheme[2])
			self.zbox.mtxt(x0+70, y0+(i*23), a[i][1], font=self.ftheme[2],
				anchor="ne")
		# player inventory
		inv1 = self.pdata["inventory"]
		pnv = inv1 + ["e"] * (24 - len(inv1))
		X1, Y1 = X, Y + 110
		for rw in range(4):
			for cl in range(6):
				n = cl + (rw * 6)
				p = self.items[pnv[n]]["image"] if pnv[n] != "e" else "inv_empty-45x75"
				x, y = X1+(cl*47), Y1+(rw*77)
				invslot_tag0 = "pinv_slot{}".format(n)
				invslot_tag = self.zbox.m("pinv_slot{}".format(n))
				self.zbox.mimg(x, y, p, invslot_tag0)
				self.cn.tag_bind(invslot_tag, "<Button-1>",
					lambda _, n=n: self.transfer_item(n, 1))
				self.cn.tag_bind(invslot_tag, "<Enter>",
					lambda _, x=x, y=y, n=n: self._hvr_inv(x, y, n, 0))
				self.cn.tag_bind(invslot_tag, "<Leave>", self._hvr_fade)
		# container info panel
		m = self.cdata
		X2, Y2 = 412, 95
		''' destroys symmetry.
		X3, Y3 = X2, Y2 + 110
		try:
			self.zbox.mimg(X3-15, Y3-60, self.cdata["box_image"], anchor="nw")
		except: pass
		'''
		self.zbox.mrect(X2, Y2, 280, 105, fill="white", width=2)
		self.zbox.mimg(X2+180, Y2, m["avatar"])
		self.zbox.mimg(X2+6, Y2+23, "btn_think-45x75", "b_reset")
		self.zbox.mimg(X2+53, Y2+23, "btn_leave-45x75", "b_leave")
		self.cn.tag_bind(self.zbox.m("b_reset"), "<Button-1>", self.reset_inv)
		self.cn.tag_bind(self.zbox.m("b_leave"), "<Button-1>", self._exit_box)
		self.zbox.mtxt(X2+103, Y2+7, m["name"], font=self.ftheme[1])
		self.zbox.mtxt(X2+9, Y2+5, "Scnr:")
		self.zbox.mtxt(X2+94, Y2+5, m["coin"], "ccoin", anchor="ne")
		x1, y1 = X2 + 102, Y2 + 29
		#b = [["+All", "-100"], ["+1k", "-1k"], ["+100", "-All"]]
		b = [["-All", "+100"], ["-1k", "+1k"], ["-100", "+All"]]
		for i in range(3): 
			self.zbox.mrect(x1, y1+(i*23), 74, 21, "white", width=1)
			self.zbox.mtxt(x1+2, y1+(i*23), b[i][0], b[i][0], self.ftheme[2])
			self.zbox.mtxt(x1+72, y1+(i*23), b[i][1], b[i][1],
				self.ftheme[2], "ne")
			self.cn.tag_bind(self.zbox.m(b[i][0]), "<Button-1>", 
				lambda _, i=i: self._transfergold(b[i][0]))
			self.cn.tag_bind(self.zbox.m(b[i][1]), "<Button-1>",
				lambda _, i=i: self._transfergold(b[i][1]))
		# container inventory
		inv2 = m["inventory"]
		mnv = inv2 + ["e"] * (24 - len(inv2))
		X3, Y3 = X2, Y2 + 110
		for rw in range(4):
			for cl in range(6):
				n = cl + (rw * 6)
				p = self.items[mnv[n]]["image"] if mnv[n] != "e" else "inv_empty-45x75"
				x, y = X3+(cl*47), Y3+(rw*77)
				invslot_tag0 = "cinv_slot{}".format(n)
				invslot_tag = self.zbox.m("cinv_slot{}".format(n))
				self.zbox.mimg(x, y, p, invslot_tag0)
				self.cn.tag_bind(invslot_tag, "<Button-1>",
					lambda _, n=n: self.transfer_item(n, 0))
				self.cn.tag_bind(invslot_tag, "<Enter>",
					lambda _, x=x, y=y, n=n: self._hvr_inv(x, y, n, 1))
				self.cn.tag_bind(invslot_tag, "<Leave>", self._hvr_fade)
		self.zbox.raise_ctags()
		
	
	def load_variables(self, *args):
		self.items = self.world.items
		self.pdata = copy.deepcopy(self.world.characters["THE_PLAYER"])
		self.cdata = copy.deepcopy(self.world.containers[self.container])
		# reset values, more simple
		self.pdata1 = copy.deepcopy(self.world.characters["THE_PLAYER"])
		self.cdata1 = copy.deepcopy(self.world.containers[self.container])
		self.mtag = "tradeboxUI_{}".format(self.container)
		self.zbox = Ztoolbox(self.world)
		self.zbox.mtag = self.mtag
		self.ihvr_t = None  # hover id
		self.fn, self.fs = self.world.fn, self.world.fs
		self.ftheme = self.world.ftheme
	
	
	def reset_inv(self, *args):
		self.pdata = copy.deepcopy(self.pdata1)
		self.cdata = copy.deepcopy(self.cdata1)
		self.update_ui()
		
	
	def transfer_item(self, iindex, receiver_invn, *args):
		rinv = receiver_invn
		sinv = 0 if rinv == 1 else 1
		try:
			inv = [self.pdata["inventory"], self.cdata["inventory"]]
			if len(inv[rinv]) < 24:
				inv[rinv].append(inv[sinv][iindex])
				del inv[sinv][iindex]
		except: pass  # empty slot
		self.update_ui()
		self._hvr_again(iindex, sinv)
	
	
	def update_ui(self, *args):
		inv0, inv1 = self.pdata["inventory"], self.cdata["inventory"]
		pnv = inv0 + ["e"] * (24 - len(inv0))
		cnv = inv1 + ["e"] * (24 - len(inv1))
		for rw in range(4):
			for cl in range(6):
				n = cl + (rw * 6)
				pnvimg = cnvimg = "inv_empty-45x75"
				if pnv[n] != "e": pnvimg = self.items[pnv[n]]["image"]
				if cnv[n] != "e": cnvimg = self.items[cnv[n]]["image"]
				ptag = self.zbox.m("pinv_slot{}".format(n))
				ctag = self.zbox.m("cinv_slot{}".format(n))
				self.cn.itemconfigure(ptag, image=self.rsc[pnvimg])
				self.cn.itemconfigure(ctag, image=self.rsc[cnvimg])
		self.cn.itemconfigure(self.zbox.m("pcoin"), text=self.pdata["coin"])
		self.cn.itemconfigure(self.zbox.m("ccoin"), text=self.cdata["coin"])
		b = ["+All", "+100", "+1k", "-All", "-100", "-1k"]
		for i in range(len(b) // 2):
			z1 = z2 = "brown"
			n = [0, 100, 1000]
			if self.pdata["coin"] >= n[i]: z1 = "black"
			if self.cdata["coin"] >= n[i]: z2 = "black"
			self.cn.itemconfigure(self.zbox.m(b[i]), fill=z1)
			self.cn.itemconfigure(self.zbox.m(b[i+3]), fill=z2)
		self._hvr_fade()
	
	
	def zibox(self, x, y, item, buyorsell=1, *args):  # item hover box
		tag = "hover_obj"
		inm = self.items[item]["name"]
		if self.items[item]["type"] != None: itp = self.items[item]["type"]
		else: itp = "???"
		if self.items[item]["descr"] != None: ids = self.items[item]["descr"]
		else: ids = "?????"
		if self.items[item]["price"] != None:
			ipr = self.items[item]["price"][buyorsell]
		else: ipr = "???"
		sn = sv = ""
		if itp == "armor": sn, sv = "D:", self.items[item]["defense_value"]
		elif itp == "potion": sn, sv = "H:", self.items[item]["heal_value"]
		elif itp == "weapon": sn, sv = "A:", self.items[item]["attack_value"]
		# what it means when cat curls its tail
		# add later
		self.zbox.mimg(x, y, "hover_stats", tag)
		'''
		self.zbox.mrect(x+3, y+3, 144, 78, "#776611", tag)
		self.zbox.mrect(x+3, y+81, 49, 21, "#774411", tag)
		self.zbox.mrect(x+52, y+81, 95, 21, "#773311", tag)
		'''
		self.zbox.mtxt(x+5, y+4, inm, tag, self.ftheme[1])
		self.zbox.mtxt(x+7, y+18, itp, tag, (self.fn[1], 9))
		self.zbox.mtxt(x+5, y+30, ids, tag, (self.fn[0], 11), width=140)
		self.zbox.mtxt(x+5, y+102, sn, tag, anchor="sw")
		self.zbox.mtxt(x+48, y+102, sv, tag, anchor="se")
		self.zbox.mtxt(x+95, y+102, "Scnr:", tag, anchor="se")
		self.zbox.mtxt(x+145, y+102, ipr, tag, anchor="se")
	
	
	def _exit_box(self, *args):
		self.cn.delete(self.mtag)
		self.extract()
	
	
	def _gold_glow(self, glowing=False, *args):
		tag = self.zbox.m("pcoin")
		if glowing:
			self.cn.itemconfigure(tag, fill="black")
		else:
			self.cn.tag_raise(tag)
			self.cn.itemconfigure(tag, fill="green")
			self.parent.after(500, lambda: self._gold_glow(True))
	
	
	def _hvr_again(self, iindex, invn, *args):
		rw = iindex // 6
		cl = iindex % 6
		X, Y = 45, 203  # p inv start
		if invn == 1: X, Y = 412, 203
		x, y = X+(cl*47), Y+(rw*77)
		self._hvr_inv(x, y, iindex, invn)
	
	
	def _hvr_fade(self, *args):
		if self.ihvr_t is not None:
			self.parent.after_cancel(self.ihvr_t)
			self.ihvr_t = None
		self.cn.delete(self.zbox.m("hover_obj"))
	
	
	def _hvr_inv(self, x, y, iindex, invn, stage=0, *args):
		xn = (x + 47) if (x + 152) < 760 else (x - 152)
		yn = y - 7
		inv0 = [self.pdata["inventory"], self.cdata["inventory"]]
		inv = [[], []]
		inv[0] = inv0[0] + ["e"] * (24 - len(inv0[0]))
		inv[1] = inv0[1] + ["e"] * (24 - len(inv0[1]))
		if inv[invn][iindex] != "e":
			if stage == 0:
				self._hvr_fade()
				self.ihvr_t = self.parent.after(325,
					lambda: self._hvr_inv(x, y, iindex, invn, stage=1))
			elif stage == 1:
				self.zibox(xn, yn, inv[invn][iindex])
	
	
	def _transfergold(self, txt, *args):
		coin_inv = [self.pdata["coin"], self.cdata["coin"]]
		receiver = 1 if txt[0] == "+" else 0
		sender = 0 if receiver == 1 else 1
		amount = txt[1:]
		glow_gold = True
		if amount == "All":
			coin_inv[receiver] += coin_inv[sender]
			coin_inv[sender] = 0
		elif amount == "100":
			if coin_inv[sender] >= 100:
				coin_inv[sender] -= 100
				coin_inv[receiver] += 100
			else: glow_gold = False
		elif amount == "1k":
			if coin_inv[sender] >= 1000:
				coin_inv[sender] -= 1000
				coin_inv[receiver] += 1000
			else: glow_gold = False
		self.pdata["coin"] = coin_inv[0]
		self.cdata["coin"] = coin_inv[1]
		if glow_gold: self._gold_glow()
		self.update_ui()
		
		
class Ztoolbox:
	def __init__(self, world, *arg, **kwarg):
		self.world = world
		self.parent = world.parent
		self.cn = world.cn
		self.rsc = world.rsc
		self.mtag = world.mtag
		self.fn = world.fn
		self.fs = world.fs
		self.hvrt = None  # hover id
		
	
	def check_tags(self, tags):
		# Input: ("a", "b")
		# Output: (mtag, "mtag_a", "mtag_b")
		if tags is None:
			tags = self.mtag
		elif isinstance(tags, str):  # string
			x = [self.m(tags)]
			tags = tuple([self.mtag] + x)
		else:
			x = [self.m(i) for i in tags]
			tags = tuple([self.mtag] + x)
		return tags
		
	
	def m(self, tag):
		return "{}_{}".format(self.mtag, tag)
	
	
	def mbtn(self, x1, y1, text, command, font=None, w=None, h=None,
		bg="#776611", txty_change=0, *args):
		w = w if w is not None else 4 + (9 * len(text))
		h = 25 if h is None else h
		tag = "btn_{}".format(text)
		def _bhover(mode="enter", *args):
			tn = self.m(tag+"_rect")
			if self.hvrt != None:
				self.parent.after_cancel(self.hvrt)
				self.hvrt = None
			if mode == "enter":
				self.hvrt = self.parent.after(100,
					lambda _=1: self.cn.itemconfigure(tn, fill="orange"))
			else: self.cn.itemconfigure(tn, fill=bg)
		self.mrect(x1, y1, w, h, bg, (tag, tag+"_rect"), "black", 2)
		x2, y2 = x1 + (w / 2) - 1, y1 + 1
		self.mtxt(x2, y2+txty_change, text, (tag, tag+"_txt"), font=font,
			anchor=tk.N, width=w)
		if command is not None:
			self.cn.tag_bind(self.m(tag), "<Button-1>", lambda _=1: command())
		ntag = self.m(tag+"_txt")
		self.cn.tag_bind(ntag, "<Enter>", lambda _=1: _bhover())
		self.cn.tag_bind(ntag, "<Leave>", lambda _=1: _bhover("l"))
		
	
	def mimg(self, x, y, image, tags=None, anchor=tk.NW, *args):
		tags = self.check_tags(tags)
		self.cn.create_image(x, y, image=self.rsc[image], tags=tags,
			anchor=anchor)
	

	def mrect(self, x1, y1, w, h, fill="black", tags=None, c=None, width=0, *args):
		tags = self.check_tags(tags)
		self.cn.create_rectangle(x1, y1, x1+w, y1+h, fill=fill, tags=tags,
			outline=c, width=width)
	
		
	def mtxt(self, x, y, txt, tags=None, font=None, anchor=tk.NW,
		fill="black", width=250, align="left", *args):
		tags = self.check_tags(tags)
		font = (self.fn[0], self.fs[0]) if font is None else font
		self.cn.create_text(x, y, text=txt, tags=tags, font=font,
			anchor=anchor, fill=fill, width=width, justify=align)

			
	def raise_ctags(self, *args):
		self.world.raise_ctags()
			
