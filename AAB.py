import copy
import game_data
import game_dialogs
import game_ui
import math
import os
import random as rd
import tkinter as tk
#import winsound as ws



class AAB:
	def __init__(self, parent, *arg, **kwarg):
		self.parent = parent
		self.parent.title("Anhero of Amporal Belitz")
		self.parent.geometry("800x600")
		self.parent.resizable(0, 0)
		center(self.parent, 0, -35)
		self.mainframe = tk.Frame(self.parent, highlightthickness=0, bd=0)
		self.mainframe.pack()
		self.cn = tk.Canvas(self.mainframe, width=800, height=600, bg="black",
			highlightthickness=0, bd=0, cursor="target")
		self.cn.pack()
		# init game data
		self.load_resources()
		self.load_fonts()
		self.load_variables()
		self.load_game_data()
		self.load_basic_ui()
		# test functions
		#self.check_condition("Q|mq01")
		#self.check_event_conditions([(["Qactive|mq01", "G+|100"], "place|cabin_indoors", "bw-hdoor0|270,253")])
		self.start_screen()
		#self._mbtn(300, 300, "Perks", lambda: print(self.aktivql))
		self._mbtn(10, 10, "Save Test", lambda: self.saveload_test())
		self._mbtn(10, 40, "Perks", lambda: print(self.characters["THE_PLAYER"]["perks"]))
	
	
	def saveload_test(self, *args):
		self.go_save = game_ui.SaveGame(self)
		a = self.go_save.prepare_data()
		a = a.replace("Lurco", "Montezuma")
		self.go_load = game_ui.LoadGame(self)
		self.go_load.load_data(a)
		print("*"*50)
		print(a)
		print("*"*50)
		

	def start_screen(self, *args):
		self._uistatus("aktiv")
		self._mrect(0, 0, 800, 600, "white", tags="start_screen", width=5)
		self._mtxt(400, 125, "AAA", "start_screen", (self.fn[0], 52), "center")
		self._mbtn(300, 200+(0*47), "New", 
			lambda _=1: self.start_screen_exit(),
			(self.fn[0], 20), 200, 40, "white", 3)
		self._mbtn(300, 200+(1*47), "Continue", None, (self.fn[0], 20), 200, 40, "white", 3)
		self._mbtn(300, 200+(2*47), "Load", None, (self.fn[0], 20), 200, 40, "white", 3)
		self._mbtn(300, 200+(3*47), "Credits", 
			lambda _=1: self.start_credits(),
			(self.fn[0], 20), 200, 40, "white", 3)
		self._mbtn(300, 200+(4*47), "Exit", None, (self.fn[0], 20), 200, 40, "white", 3)
		'''
		btxt = ["New", "Continue", "Load", "Credits", "Exit"]
		for i in range(len(btxt)):
			self._mbtn(300, 200+(i*47), btxt[i], None, (self.fn[0], 20), 200, 40, "white", 3)
		self.cn.itemconfigure(self._m("btn_New"), command=lambda _=1: map(self.cn.delete, btxt))	
		'''
	
	
	def start_screen_exit(self, stage=0, *args):
		# disable going to location after exit
		# we need more time, 3days, 7hours alone just to fix the start screen.
		# 3hours for save system
		# 3hours for bug checking
		# 2hours left
		# 15hours, doable within 5-7days
		btxt = ["New", "Continue", "Load", "Credits", "Exit"]
		btxt = [self._m("btn_"+x) for x in btxt]
		self._delete(btxt, self._m("start_screen"))
		self._uistatus("inaktiv")
		'''
		if stage == 0:
			self._uistatus("aktiv")
			self.parent.after(250, self.start_screen_exit(1))
		else:
			btxt = ["New", "Continue", "Load", "Credits", "Exit"]
			btxt = [self._m("btn_"+x) for x in btxt]
			self._delete(btxt, self._m("start_screen"))
			self._uistatus("inaktiv")
		'''
		
	def check_event_events(self, event_list, *args):
		# checks for events to be executed
		if len(event_list) < 4: return  # No events
		elif (event_list[3] == None or
			event_list[3] == "" or
			event_list[3] == []):
			return
		data = event_list[3]
		if isinstance(data, str):
			self.check_event(data)
		else:
			for i in data:
				self.check_event(i)
	
	
	def check_event(self, event, *args):
		'''
		Qstage+|qname
		Qstart|qname
		Qcomplete|qname automatically give reward
		I+|item*n
		I-|item*n
		G+|int
		HP+|int
		Exp+|int
		'''
		f, p = event.split("|")
		player_stats = self.characters["THE_PLAYER"]
		current_stage = max_stage = None 
		if f[0] == "Q":
			# using current_stage = max_stage not working
			current_stage = self.quests[p]["stage"][0] 
			max_stage = self.quests[p]["stage"][1]
		if f == "Qcomplete": 
			self.quests[p]["stage"][0] = max_stage
			txt = "''{}'' Completed".format(self.quests[p]["name"])
			self.display_event_txt(txt)
			self.give_reward(p)
			self.fertigql.append(p)
			self.aktivql.remove(p)
		elif f == "Qstage+":
			self.quests[p]["stage"][0] += 1
			txt = "''{}'' Updated".format(self.quests[p]["name"])
			self.display_event_txt(txt)
		elif f == "Qstart":
			self.quests[p]["stage"][0] = 1
			self.aktivql.append(p)
			txt = "''{}'' Started".format(self.quests[p]["name"])
			self.display_event_txt(txt)
		elif f[0] == "I":
			n = 1
			pdata = p.split("*")
			if len(pdata) > 1: n = pdata[1]
			if f[1] == "+": player_stats["inventory"] += [pdata[0]] * n
			else:
				for i in range(n):
					player_stats["inventory"].remove(pdata[0])
		elif f == "G+": player_stats["coin"] += int(p)
		elif f == "HP+":
			m = player_stats["stats"][0][0] + int(p)
			m = 1 if m < 1 else m
			if m > player_stats["stats"][0][1]:
				m = player_stats["stats"][0][1]
			player_stats["stats"][0][0] = m
		elif f == "Exp+": player_stats["stats"][5] += int(p)
		#pass
		# apply to other changes to dialog
		# modify dialog for default values
		# apply to store
		# do first quest
		
		
	def check_event_conditions(self, event_data, *args):
		# checks conditions of data in events
		revised_event_data = []
		for edata in event_data:
			if (edata[0] is None or 
				edata[0] == "" or 
				edata[0] == []):
				revised_event_data.append(edata)
				continue
			condition_met = False
			if isinstance(edata[0], str):
				condition_met = self.check_condition(edata[0])
			else:
				clist = list(map(self.check_condition, edata[0]))
				if False not in clist: condition_met = True
			if condition_met: revised_event_data.append(edata)
		return revised_event_data
	
	
	def check_condition(self, condition, *args):
		f, p = condition.split("|")
		player_stats = self.characters["THE_PLAYER"]
		current_stage = max_stage = None 
		if f[0] == "Q":
			current_stage = self.quests[p]["stage"][0] 
			max_stage = self.quests[p]["stage"][1]
		if f == "Qactive":
			if current_stage > 0 and current_stage < max_stage: return True
		elif f == "Qcompleted":
			if current_stage == max_stage: return True
		elif f == "Qdormant":
			if current_stage == 0: return True
		elif f[:-1] == "Qstage":
			if current_stage == int(f[-1]): return True
		elif f == "Qstarted":
			if current_stage >= 1: return True
		elif f == "G+":
			coin = player_stats["coin"]
			if coin >= int(p): return True
		elif f == "L+":
			lvl = player_stats["stats"][5] // 1000
			if lvl >= int(p): return True
		elif f == "Ihas":
			inv = player_stats["inventory"]
			n = p.split("*")
			req = 1 if len(n) == 1 else int(n[1])
			num = inv.count(n[0])
			if num >= req: return True
		return False
		

	def check_events(self, event_list, *args):
		'''
		
		'''
		pass
	
	
	def check_quests(self, *args):
		# check quest conditions to adv stage
		aktivq = []
		inv = self.characters["THE_PLAYER"]["inventory"]
		q_act = ""
		for k, v in self.quests.items():  # find active quests
			qstage = self.quests[k]["stage"][0]
			if (0 < qstage < self.quests[k]["stage"][1]):
				aktivq.append(k)
		for q in aktivq:  # check conditions to adv stage
			stage_now = self.quests[q]["stage"][0]
			req2adv = self.quests[q]["stage{}".format(stage_now)][1]
			hasreq = []  # boolean list to check if requirements met
			for req in req2adv:
				condition = req.split("|")
				if condition[0] == "item":
					if condition[2] == "*":  # already met
						hasreq.append(True)
						continue  # skip to next iteration
					if condition[1] in inv:
						inv.remove(condition[1])
						# update quest data
						reqn = "item|{}|*".format(condition[1])
						req2adv[req2adv.index(req)] = reqn
						hasreq.append(True)
						#q_act = "Updated"
					else: hasreq.append(False)
				elif condition[0] == "reward":
					if condition[1] == "collected":
						hasreq.append(True)
						#q_act = "Completed"
					else: hasreq.append(False)
			if False not in hasreq: 
				self.quests[q]["stage"][0] += 1
				if (self.quests[q]["stage"][0] != self.quests[q]["stage"][1] and
					self.quests[q]["stage"][0] > 1):
					q_act = "Updated"	
				elif self.quests[q]["stage"][0] == self.quests[q]["stage"][1]:
					q_act = "Completed"
				#elif self.quests[q]["stage"][0] >= 0:
				#	q_act = "Accepted"	
				if q_act != "":
					qtxt = "Quest ''{}'' {}".format(self.quests[q]["name"], q_act)
					self.display_event_txt(qtxt)
	
	
	def display_event_txt(self, txt, *args):
		# minor problems
		def set2none():
			self.evt_txt_id = None
		def display_words(index, txt_list):
			self.cn.tag_raise(self._m("Etxt"))
			go_nxt, start_new = True, False
			if index == 0:
				font = (self.fn[0], 36, "bold")
				color = "black"
				self._mtxt(400, 200, txt_list[index], "Etxt", font=font,
					fill=color, anchor="center", width=750, align="center")
			elif index < len(txt_list):
				txt = self.cn.itemcget(self._m("Etxt"), "text")
				txt += " {}".format(txt_list[index])
				#txt += "{}".format(txt_list[index])
				self.cn.itemconfigure(self._m("Etxt"), text=txt)
			else:	
				go_nxt = False
				del self.evt_txt_list[0]
				self.parent.after(2000,
					lambda _=1: self.cn.delete(self._m("Etxt")))
				if len(self.evt_txt_list) >= 1: 
					start_new = True
				else:
					pass
					#self.parent.after(2000, lambda _=1: set2none())
			if go_nxt:
				#self.evt_txt_id = self.parent.after(100, 
				#	lambda _=1: display_words(index+1, txt_list))
				self.evt_txt_id = self.parent.after(80, 
					lambda _=1: display_words(index+1, txt_list))	
			elif start_new:
				self.parent.after(2200,
					lambda _=1: display_words(0, self.evt_txt_list[0]))
			else: self.evt_txt_id = None
		txt_list = txt.split(" ")
		#txt_list = [x for x in txt]
		self.evt_txt_list.append(txt_list)
		if self.evt_txt_id is None:
			display_words(0, self.evt_txt_list[0])

	
	def give_reward(self, quest_name, *args):
		p = self.characters["THE_PLAYER"]
		reward = self.quests[quest_name]["reward"]
		p["stats"][5] += reward[0]  # exp, scale later
		p["coin"] += reward[1]
		p["inventory"] += reward[2]  # items
		
		
	def load_basic_ui(self, *args):
		#self.load_map(self.current_region)
		self.load_map()
		# create player image on map and set movement
		self._mimg(280, 370, self.characters["THE_PLAYER"]["map_image"],
			"map_player", "center")	
		self.cn.bind("<Button-1>", self._interact)
		'''
		self._mimg(2, 547, "chr_ava-50x50", "btn_Avatar")
		self._mbtn(54, 558, "Lurco", None, w=76, h=38, font=(self.fn[0], 14), txty_change=5)
		self._mbtn(54+(1*79), 558, "Perks", None, w=76, h=38, font=(self.fn[0], 14), txty_change=5)
		self._mbtn(54+(2*79), 558, "Quest", None, w=76, h=38, font=(self.fn[0], 14), txty_change=5)
		self.cn.tag_bind(self._m("btn_Quest"), "<Button-1>", self.start_quest)
		self.cn.tag_bind(self._m("btn_Lurco"), "<Button-1>", lambda _=1: self.start_player_inv())
		self.cn.tag_bind(self._m("btn_Perks"), "<Button-1>", lambda _=1: self.start_perks())
		self._mbtn(54+(3*79), 558, "Map", None, w=76, h=38, font=(self.fn[0], 14), txty_change=5)
		'''
		#self._mbtn(60, 545, "Inventory", None)
		#self.cn.tag_bind(self._m("btn_Avatar"), "<Button-1>",
		#	lambda _=1: self.start_dialog("A00"))
		#self.cn.tag_bind(self._m("map_player"), "<Button-1>",
		#	lambda _=1: self.start_player_inv())
		#self._mimg(5, 5, "bw-i_coin", ("menu_icons"))
		bilist = ["bpack", "scroll", "book", "settings"]
		for i in range(len(bilist)):
			n = (i+1)*-1
			img = "bw-i_{}".format(bilist[n])
			x, y = 755+(i*-45), 5
			self._mimg(x, y, img, ("mi_"+bilist[n], "menu_icons"))
		self.cn.tag_bind(self._m("mi_book"), "<Button-1>", self.start_quest)
		self.cn.tag_bind(self._m("mi_bpack"), "<Button-1>", lambda _=1: self.start_player_inv())
		self.cn.tag_bind(self._m("mi_scroll"), "<Button-1>", lambda _=1: self.start_perks())
		
	
	def load_fonts(self, *args):
		self.fn = [
			"Book Antiqua", "Segoe UI"
		]
		self.fs = [
			12, 11
		]
		self.ftheme = [
			("Book Antiqua", 12),
			("Book Antiqua", 12, "bold"),
			("Segoe UI", 11),
			("Segoe UI", 11, "bold"),
			("Book Antiqua", 17),
		]
	
	
	def load_game_data(self, *args):
		self.characters = game_data.characters
		self.containers = game_data.containers
		self.dialogs = game_dialogs.dialogs
		self.items = game_data.items
		#self.map = game_data.map
		self.map = game_data.map_markers
		self.world_places = game_data.world_places
		self.map_places = {}
		self.perks = game_data.perks
		self.quests = game_data.quests
		self.aktivql = ["A00"]  # current active quests
		self.fertigql = []  # current completed quests
		# places
		# quests
		self.weapon_stats = {
			# HC, IA, CC, CD
			"sword": [80, 0, 20, 1.5],
			"axe": [70, 10, 15, 2.0],
			"mace": [60, 50, 10, 2.5],
		}
		
	'''
	def load_map(self, map, *args):
		self._mimg(0, 0, self.map[map]["image"], ("map_obj"))
		for k, v in self.map[map]["places"].items():
			n = self.map[map]["places"][k]
			self.placemarker(n["coords"][0], n["coords"][1],
				n["name"], n["map_image"],
				lambda _=1, k=k: self.start_place(k), k)
	'''

	def load_map(self, *args):
		#self._mimg(0, 0, self.map[map]["image"], ("map_obj"))
		self._mimg(0, 0, "map_badlands", ("map_obj"))
		for k, v in self.map.items():
			n = self.map[k]
			self.placemarker(n["coords"][0], n["coords"][1],
				n["name"], n["image"],
				lambda _=1, k=k: self.start_place(k), k)
	
	
	def load_resources(self, *args):
		floc = "resources\\"  # file location of the Gif images
		fdata = os.listdir(floc)  # get all files in the directory
		# separate GIFs from the rest and gives the filename location
		glist = [data[:-4] for data in fdata if data[-4:] == ".gif"]  # Gif
		llist = [floc + data for data in fdata if data[-4:] == ".gif"]  # path
		self.rsc = {}
		for gif in range(len(glist)):
			self.rsc[glist[gif]] = tk.PhotoImage(file = llist[gif])
		glist2 = [data[:-4] for data in fdata if data[-4:] == ".png"]  # Gif
		llist2 = [floc + data for data in fdata if data[-4:] == ".png"]  # path	
		for gif2 in range(len(glist2)):
			self.rsc[glist2[gif2]] = tk.PhotoImage(file = llist2[gif2])
			
	
	def load_variables(self, *args):
		self.aktiv_caUI = False
		self.aktiv_ui = False
		self.current_region = "Badlands"
		self.in_battle = False
		self.mapicon_t = None  # placemarker hover t
		self.hvrt = None  # btn hover id
		self.evt_txt_id = None  # evt text id
		self.map_move = None
		self.mtag = "mainUI"  # main tag of the game
		self.evt_txt_list = []
	
	
	def placemarker(self, x, y, place_name, image,
		evts=None, tag=None, x_add=0, y_add=0, *args):
		tag = tag if tag != None else place_name
		tag = "w-{}".format(tag)
		def _phover(mode="enter", *args):
			tn = self._m(tag+"_image")
			i2 = image[:image.index("-")] + "O" + image[image.index("-"):]
			if self.mapicon_t != None:
				self.parent.after_cancel(self.mapicon_t)
				self.mapicon_t = None
			if mode == "enter":
				self.mapicon_t = self.parent.after(150,
					lambda _=1: self.cn.itemconfigure(tn, image=self.rsc[i2]))
			else:
				self.cn.itemconfigure(tn, image=self.rsc[image])
		h = int(image[-2:])  # height 99px max
		add = ((h / 2) + 8) * -1
		self._mimg(x, y, image, ("map_obj", tag, tag+"_image"), "center")
		self._mtxt(x+x_add, y-add, place_name, ("map_obj", tag, tag+"_txt"),
			anchor="center", font=(self.fn[0], self.fs[1]), fill="#441122")
		self.map_places[self._m(tag)] = evts
		#self.cn.tag_bind(self._m(tag), "<Enter>", lambda _=1: _phover())
		#self.cn.tag_bind(self._m(tag), "<Leave>", lambda _=1: _phover("l"))
	
	
	def raise_ctags(self, *args):
		a = ["Avatar", "Lurco", "Perks", "Quest", "Map"]
		for i in range(len(a)):
			tag = self._m("btn_{}".format(a[i]))
			self.cn.tag_raise(tag)
		self.cn.tag_raise(self._m("menu_icons"))
		
	
	def start_battle(self, enemy, paths=None, player="THE_PLAYER", *args):
		def end_fight(paths, *args):
			self._uistatus("inaktiv")
			self.cn.move(self._m("menu_icons"), 0, 75)
			#self.disable_cm(0)
			#self.in_battle = False
			# paths: 3 functions for win, defeat, flee. respectively. 0, 1, 2
			self.battle_result = self.cn.itemcget("battle_result", "text")
			self.cn.delete("battle_ui", "battle_result")
			self.characters[player] = copy.deepcopy(sc.player)
			#self.char[player]["coin"] += copy.deepcopy(sc.enemy["coin"])
			if paths != None:
				if "Victory" in self.battle_result:
					self.start_dialog(paths[0])
					# temp 
					#self.dialog[paths[0]]["rewards"][1] = self.scale_exp(self.dialog[paths[0]]["rewards"][1])
					try: 
						self.characters[player]["stats"][5] += self.dialogs[paths[0]]["reward"][0]
					except: pass
					try:
						self.characters[player]["coin"] += self.dialogs[paths[0]]["reward"][1]
					except: pass
					try:
						self.characters[player]["inventory"] += self.dialogs[paths[0]]["reward"][2]
					except: pass
				elif "Defeat" in self.battle_result:
					x = rd.randint(0, 10)
					if x <= 5:
						self.start_dialog(paths[2])
					else:
						#self._mimg(0, 0, "aBg1")
						self.start_dialog(paths[1])
				elif "Flee" in self.battle_result:
					self.start_dialog(paths[2])
				else:
					pass
					#print self.battle_result
		#self.cn.delete("dialogUI")
		#sc = aBtl1.Battle(self.parent, self.cn, self.e["AnEncounterOnTheRoad-FleePass"])
		'''
		sc = aBtl1.Battle(self.parent, self.cn, lambda: end_fight(
			[self.e["AnEncounterOnTheRoad-FightPass"], 
			self.e["AnEncounterOnTheRoad-FightFail"],
			self.e["AnEncounterOnTheRoad-FleePass"]]))
		sc.battle("The Player", "Brigands0")
		'''
		sc = game_ui.Battle(self, self.cn, self.characters[player], self.characters[enemy], 
			lambda _=1: end_fight(paths))
		self._uistatus("aktiv")
		#self.disable_cm()
		self.cn.delete("caUI")
		self.cn.move(self._m("menu_icons"), 0, -75)
		#self.in_battle = True
	
	
	def start_credits(self, *args):
		self.go_start_credits = game_ui.Credits(self)
	
	
	def start_dialog(self, dialog_id, extract=None, *args):
		def lv_(s=0, *args):
			if s == 0:
				try: self.go_place.aktiv_ui = True
				except: pass
				self.parent.after(100, lambda _=1: lv_(1))
			else:
				try: self.go_place.aktiv_ui = False
				except: pass
		def end_dialog():
			self._uistatus("inaktiv")
			lv_()
			if extract is not None:
				extract()
		if not self.aktiv_caUI:
			try: self.go_place.aktiv_ui = True
			except: pass
			self._uistatus("aktiv")
			#self.check_quests()
			self.go_dialog = game_ui.Dialogs(self, dialog_id, end_dialog)
	
	
	def start_perks(self, party1="THE_PLAYER", extract=None, override=False, *args):
		def lv_(s=0, *args):
			if s == 0:
				try: self.go_place.aktiv_ui = True
				except: pass
				self.parent.after(100, lambda _=1: lv_(1))
			else:
				try: self.go_place.aktiv_ui = False
				except: pass
		def end_perkbox(*args):
			self.aktiv_caUI = False
			self._uistatus("inaktiv")
			self.cn.move(self._m("menu_icons"), 0, 75)
			lv_()
			if extract is not None:
				extract()
		def perksg1(*args):
			# copy to not mix values with real ones.
			self.characters[party1] = copy.deepcopy(self.go_perks.p1data)
			self.perks = copy.deepcopy(self.go_perks.perksl)
			for i in range(len(self.characters[party1]["stats"])):
				if i == 0:
					a = float(self.characters[party1]["stats"][i][0])
					b = float(self.characters[party1]["stats"][i][1])
					self.characters[party1]["stats"][i][0] = round(a, 1)
					self.characters[party1]["stats"][i][1]= round(b, 1)
				elif i in [5, 9]:
					self.characters[party1]["stats"][i] = int(self.characters[party1]["stats"][i])
				else:
					n = float(self.characters[party1]["stats"][i])
					self.characters[party1]["stats"][i] = round(n, 1)
			for k, v in self.characters[party1]["mods"].items():
				for x in range(len(v)):
					v[x] = round(v[x], 1)
		if not self.aktiv_caUI or override == True:
			self.aktiv_caUI = True
			try: self.go_place.aktiv_ui = True
			except: pass
			self._uistatus("aktiv")
			self.cn.delete("caUI")
			self.aktiv_caUI = True
			self.cn.move(self._m("menu_icons"), 0, -75)
			self.go_perks = game_ui.Perks(self, self.characters[party1], end_perkbox, perksg1)
	
	
	def start_place(self, place, extract=None, startxy=None, mlmt=None, *args):
		def end_place():
			self._uistatus("inaktiv")
			self.cn.bind("<Button-1>", self._interact)
			if extract is not None: extract()
		#self.check_quests()
		try: self.go_place._leave_place()
		except: pass
		self._uistatus("aktiv")
		self.go_place = game_ui.Places(self, place, end_place, startxy)
	
	
	def start_player_inv(self, extract=None, *args):
		def lv_(s=0, *args):
			if s == 0:
				try: self.go_place.aktiv_ui = True
				except: pass
				self.parent.after(100, lambda _=1: lv_(1))
			else:
				try: self.go_place.aktiv_ui = False
				except: pass
		def end_player_inv():
			self.aktiv_caUI = False
			self._uistatus("inaktiv")
			self.cn.move(self._m("menu_icons"), 0, 75)
			self.characters["THE_PLAYER"] = self.go_inv.p1data
			lv_()
			if extract is not None:
				extract()
		if not self.aktiv_caUI:
			self.aktiv_caUI = True
			try: self.go_place.aktiv_ui = True
			except: pass
			self._uistatus("aktiv")
			self.cn.move(self._m("menu_icons"), 0, -75)
			self.go_inv = game_ui.Inventory(self, end_player_inv)
			
	
	def start_quest(self, *args):
		def end_quest():
			self._uistatus("inaktiv")
			self._caUIstatus("inaktiv")
			self.cn.move(self._m("menu_icons"), 0, 75)
			#lv_()
			#if extract is not None:
			#	extract()
		#try: self.go_place.aktiv_ui = True
		#except: pass
		self._uistatus("aktiv")
		self.aktiv_caUI = True
		self.cn.move(self._m("menu_icons"), 0, -75)
		#self.check_quests()
		self.go_quest = game_ui.Quests(self, end_quest)
	
	
	def start_store(self, merchant, extract=None, bg=None, *args):
		def end_store(*args):
			#self.disable_cm(0)
			self.cn.delete(self._m("str_bg"))
			self.cn.move(self._m("menu_icons"), 0, 75)
			self.characters["THE_PLAYER"] = self.go_store.pdata
			if extract is not None:
				extract()
		if not self.aktiv_caUI:
			#self.disable_cm()
			#self.check_quests()
			self.cn.move(self._m("menu_icons"), 0, -75)
			if bg is not None: self._mimg(0, 0, bg, "str_bg")
			self.go_store = game_ui.Stores(self, merchant, end_store)
	
	
	def start_tradebox(self, container, extract=None, bg=None, *args):
		def end_tradebox(*args):
			#self.disable_cm(0)
			self.cn.delete(self._m("trd_bg"))
			self.cn.move(self._m("menu_icons"), 0, 75)
			self.characters["THE_PLAYER"] = self.go_tradebox.pdata
			self.containers[container] = self.go_tradebox.cdata
			if extract is not None:
				extract()
		if not self.aktiv_caUI:
			#self.disable_cm()
			#self.check_quests()
			self.cn.move(self._m("menu_icons"), 0, -75)
			if bg is not None: self._mimg(0, 0, bg, "trd_bg")
			self.go_tradebox = game_ui.Tradebox(self, container, end_tradebox)
	
	
	def _check_tags(self, tags):
		# Input: ("a", "b")
		# Output: (mtag, "mtag_a", "mtag_b")
		if tags is None:
			tags = self.mtag
		elif isinstance(tags, str):  # string
			x = [self._m(tags)]
			tags = tuple([self.mtag] + x)
		else:
			x = []
			for i in tags:
				x.append(self._m(i))
			tags = tuple([self.mtag] + x)
		return tags
		

	def _delete(self, itemlist_to_delete=None, string_to_delete=None, *args):
		if itemlist_to_delete != None:
			for i in itemlist_to_delete:
				self.cn.delete(i)
		if string_to_delete != None:
			self.cn.delete(string_to_delete)
	
	
	def _interact(self, event, *args):
		id_num = self.cn.find_closest(event.x, event.y)[0]
		id_tags = self.cn.gettags(id_num)
		if self._m("map_obj") in id_tags and self.aktiv_ui is False:
			if self.map_move is not None:
				self.parent.after_cancel(self.map_move)
				self.map_move = None
			# calculate variables
			coords = self.cn.coords(self._m("map_player"))
			px, py = coords[0], coords[1]
			lx, ly = event.x, event.y
			x, y = lx-px, ly-py
			dist = math.sqrt(abs(x)**2 + abs(y)**2)
			steps = dist / 3.75  # player speed 5.0 max
			ax = x / steps
			ay = y / steps
			evt = None
			for i in id_tags:
				txt = "{}_w-".format(self.mtag)
				try:
					if i[:len(txt)] == txt:
						evt = self.map_places[i]
						break
				except:
					print("_interact error")
			self._move2loc(ax, ay, steps, evt)
	
	
	def _m(self, tag):
		return "{}_{}".format(self.mtag, tag)
	

	def _mbtn(self, x1, y1, text, command, font=None, w=None, h=None,
		bg="#776611", txty_change=0, *args):
		w = w if w is not None else 4 + (9 * len(text))
		h = 25 if h is None else h
		tag = "btn_{}".format(text)
		def _bhover(mode="enter", *args):
			tn = self._m(tag+"_rect")
			if self.hvrt != None:
				self.parent.after_cancel(self.hvrt)
				self.hvrt = None
			if mode == "enter":
				self.hvrt = self.parent.after(100,
					lambda _=1: self.cn.itemconfigure(tn, fill="orange"))
			else: self.cn.itemconfigure(tn, fill=bg)
		self._mrect(x1, y1, w, h, bg, (tag, tag+"_rect"), "black", 2)
		x2, y2 = x1 + (w / 2) - 1, y1 + 1
		self._mtxt(x2, y2+txty_change, text, (tag, tag+"_txt"), font=font,
			anchor=tk.N, width=w)
		if command is not None:
			self.cn.tag_bind(self._m(tag), "<Button-1>", lambda _=1: command())
		#ntag = self._m(tag+"_txt")
		ntag = self._m(tag)
		self.cn.tag_bind(ntag, "<Enter>", lambda _=1: _bhover())
		self.cn.tag_bind(ntag, "<Leave>", lambda _=1: _bhover("l"))
	
	
	def _mimg(self, x, y, image, tags=None, anchor=tk.NW, *args):
		tags = self._check_tags(tags)  # must be tuple
		self.cn.create_image(x, y, image=self.rsc[image], tags=tags,
			anchor=anchor)
	
	
	def _move2loc(self, x_add, y_add, steps, evt=None, *args):
		if steps >= 0 and self.aktiv_ui is False:
			self.cn.move(self._m("map_player"), x_add, y_add)
			steps -= 1
			self.map_move = self.parent.after(50, lambda _=1: 
				self._move2loc(x_add, y_add, steps, evt))
		elif steps < 0:
			self.map_move = None
			if evt is not None:
				evt()
	

	def _mrect(self, x1, y1, w, h, fill="black", tags=None, c=None, width=0):
		tags = self._check_tags(tags)  # must be tuple
		self.cn.create_rectangle(x1, y1, x1+w, y1+h, fill=fill, tags=tags,
			outline=c, width=width)
		
	def _mtxt(self, x, y, txt, tags=None, font=None, anchor=tk.NW,
		fill="black", width=250, align="left", *args):
		tags = self._check_tags(tags)  # must be tuple
		font = (self.fn[0], self.fs[0]) if font is None else font
		self.cn.create_text(x, y, text=txt, tags=tags, font=font,
			anchor=anchor, fill=fill, width=width, justify=align)

	
	def _caUIstatus(self, state, *args):
		if state == "aktiv":
			self.aktiv_caUI = True
		elif state == "inaktiv":
			self.aktiv_caUI = True
			self.parent.after(100, lambda _=1: self._caUIstatus("2inaktiv"))
		elif state == "2inaktiv":  # prevents moving immediately
			self.aktiv_caUI = False	
			
	
	def _uistatus(self, state, *args):
		if state == "aktiv":
			self.aktiv_ui = True
		elif state == "inaktiv":
			self.aktiv_ui = True
			self.parent.after(100, lambda _=1: self._uistatus("2inaktiv"))
		elif state == "2inaktiv":  # prevents moving immediately
			self.aktiv_ui = False
			
	
def center(win, x_add=0, y_add=0):
	win.update_idletasks()
	width = win.winfo_width()
	height = win.winfo_height()
	x = (win.winfo_screenwidth() // 2) - (width // 2)
	y = (win.winfo_screenheight() // 2) - (height //2)
	win.geometry("{}x{}+{}+{}".format(width, height, x+x_add, y+y_add))


if __name__ == "__main__":
	root = tk.Tk()
	app = AAB(root)
	root.mainloop()