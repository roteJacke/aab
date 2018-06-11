import copy
import math
import tkinter as tk



class Dialogs:
	def __init__(self, world, dialog, extract=None, *arg, **kwar):
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
		self.zbox.mimg(30, 61, "dtxt_txtbg-530x465")
		self.zbox.mimg(570, 61, self.dialog_image)
		self.zbox.mimg(570, 271, "dtxt_choices-200x255")
		self.zbox.mtxt(40, 76, self.dialogdata["text"][0],  # title
			font=(self.fn[0], self.fs[1], "bold"))
		self.zbox.mtxt(40, 106, self.dialogdata["text"][1], width=510)  # text
		ci = "dtxt_choice-190x30"
		ci2 = "dtxt_choiceO-190x30"
		def dhover(tag, mode=1, *args):
			t = self.zbox.m(tag+"_img")
			if self.dhvr_t != None:
				self.parent.after_cancel(self.dhvr_t)
				self.dhvr_t = None
			if mode == 1:
				self.dhvr_t = self.parent.after(25,
					lambda _=1: self.cn.itemconfigure(t, image=self.rsc[ci2]))
			else: self.cn.itemconfigure(t, image=self.rsc[ci])
		self.tdl = self._check_qreq(copy.deepcopy(self.dialogdata["choices"]))
		for i in range(len(self.tdl)):
			c = self.tdl[i]
			tag0 = "choice_{}".format(c[0])
			tag = self.zbox.m(tag0)
			self.zbox.mimg(575, 281+(i*33), ci, (tag0, tag0+"_img"))
			self.zbox.mtxt(582, 286+(i*33), c[0], tag0)
			self.cn.tag_bind(tag, "<Enter>", lambda _=1, t=tag0: dhover(t))
			self.cn.tag_bind(tag, "<Leave>", lambda _=1, t=tag0: dhover(t, 0))
			if c[1] is None: continue  # next iteration
			cdata = c[1].split("|")
			x = cdata[1]
			if cdata[0] == "plc":  # place
				command = lambda _, n=x, z=c[3], i=i: self._go_plc(i, n, z)
			elif cdata[0] == "dlg":  # dialog
				command = lambda _, n=x, i=i: self._go_dlg(i, n)	
			elif cdata[0] == "str":  # store, trade between 2 characters
				command = lambda _, n=x, i=i: self._go_str(i, n)
			elif cdata[0] == "box":  # lootbox
				command = lambda _, n=x, i=i: self._go_box(i, n)
			elif cdata[0] == "ext":
				command = lambda _=1, i=i: self._leave_dlg(i)	
			self.cn.tag_bind(tag, "<Button-1>", command)
		self.zbox.raise_ctags()	
		
	
	def load_variables(self, *args):
		self.dlist = self.world.dialogs
		self.dialogdata = self.dlist[self.dialog_id]
		self.dialog_bg = self.dialogdata["bg_image"]
		self.dialog_image = self.dialogdata["image"]
		if self.dialogdata["image"] == None:
			self.dialog_image = "dtxt_image_roadtravel"
		self.mtag = "dialogUI_{}".format(self.dialog_id)
		self.pdata = self.world.characters["THE_PLAYER"]
		self.zbox = Ztoolbox(self.world)
		self.zbox.mtag = self.mtag
		self.fn, self.fs = self.world.fn, self.world.fs
		self.dhvr_t = None  # hover id
		self.quests = self.world.quests
		

	def _go_dlg(self, id, dialog_id, *args):
		if not self.world.aktiv_caUI:
			#self.hoverstats_fade()
			self._special_event(id)
			self.cn.delete(self.mtag)
			self.world.start_dialog(dialog_id)
	
	
	def _go_plc(self, id, evt, xy=None, *args):
		if not self.world.aktiv_caUI:
			# id conflicts with xy
			self._special_event(id)
			self.cn.delete(self.mtag)
			self.world.start_place(evt, startxy=xy)
			
	
	def _go_str(self, id, merchant, *args):
		if not self.world.aktiv_caUI:
			self._special_event(id)
			self.world.start_store(merchant)
			
			
	def _go_box(self, id, container, *args):
		if not self.world.aktiv_caUI:
			self._special_event(id)
			bg = self.dialogdata["bg_image"]
			self.world.start_tradebox(container, bg=bg)


	def _leave_dlg(self, id, *args):
		if not self.world.aktiv_caUI:
			self.cn.delete(self.mtag)
			if self.extract is not None:
				self._special_event(id)
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
			elif action == "+A":  # q accepted
				self.world.aktivql.append(name)
				self.quests[name]["stage"][0] += 1
			elif action == "+R":  # give reward and end quest
				stage_now = self.quests[name]["stage"][0]
				txt = "reward|collected"
				rl = self.quests[name]["stage{}".format(stage_now)][1][0]
				x = rl.split("|")
				if x[0] == "reward":
					self.world.give_reward(name)
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
		self.mimg(400, 50, "inv_bg-635x485", anchor="n")
		self.mimg(400, 50, "inv_bgt-635x25", anchor="n")
		# creating party1 info panel
		X, Y = 109, 95  # starting nw coords of the partyl inv panel
		self.mimg(X, Y, "inv_bg1-280x105")
		self.mimg(X, Y, "ava_player-100x105", tags=("p1_ava"))  # default ava
		self.mtxt(X+105, Y+5, "Geralt of Rpivilon", font=self.font1b,
			tags=("p1_name", "p1_stats"))
		self.mrect(X+103, Y+27, 172, 22, "#851122", tags=("p1_hpbar_bg"))
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
				self.mrect(x1, y1, w, h, "#851122", 
					tags=("p1_{}bar_bg".format(txt)))
				self.mrect(x1, y1, w, h, "brown",
					tags=("p1_{}bar".format(txt)))
				self.mtxt(x1 + 2, y1 + 1, s[n][0],
					font=self.font2, tags=("p1_statsn"))
				self.mtxt(x1 + w - 3, y1 + 1, s[n][1], 
					font=self.font2, anchor="ne",
					tags=("p1_{}".format(txt), "p1_statsn"))
		# creating party1 equipped items and other stats
		X1, Y1 = 109, 205  # starting nw coords
		self.mimg(X1, Y1, "bg_inv-280x306")
		self.mimg(X1+65, Y1+17, "img_player-150x200", "p1_img")
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
		self.mrect(X1+67, Y1+222, 146, 15, "#851122", tags=("p1_expbar_bg"))
		self.mrect(X1+67, Y1+222, 73, 15, "brown", tags=("p1_expbar"))
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
				self.mrect(x1, y1, w, h, "#851122", 
					tags=("p1_{}bar_bg".format(txt)))
				self.mrect(x1, y1, w, h, "brown",
					tags=("p1_{}bar".format(txt)))
				self.mtxt(x1 + 2, y1 + 1, c[n][0],
					font=self.font2, tags=("p1_statsn"))
				self.mtxt(x1 + w - 3, y1 + 1, c[n][1],
					font=self.font2, anchor="ne",
					tags=("p1_{}".format(txt), "p1_statsn"))
		# creating place holder img with leave button
		X2, Y2 = 412, 95
		self.mimg(X2, Y2, "inv_bg1-280x105")
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
		self.mrect(X+103, Y+27, l, 22, "brown", tags=("p1_hpbar"))
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
				self.mrect(x1, y1, l, h, "brown", tags=(tag1))
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
		self.mrect(X1+67, Y1+222, l, 15, "brown", tags=("p1_expbar"))
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
				self.mrect(x1, y1, rect_s, h, "brown", tags=(tag1))
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
				self.mrect(xn+3, yn+3, 144, 78, "#776611", tags=mtag)
				self.mrect(xn+3, yn+3, 144, 78, "#776611", tags=mtag)
				self.mrect(xn+3, yn+81, 49, 21, "#774411", tags=mtag)
				self.mrect(xn+52, yn+81, 95, 21, "#773311", tags=mtag)
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
	
	
	def mrect(self, x1, y1, w, h, fill="black", tags=None):
		tags = self.check_tags(tags)  # must be tuple
		self.cn.create_rectangle(x1, y1, x1+w, y1+h, fill=fill, tags=tags,
			outline="")
		
	
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
		self.sxy = startxy if startxy != None else (400, 375)
		self.mlmt = mlmt if mlmt != None else (10, 270, 790, 550)  # move rect range
		# start the ui
		self.load_variables()
		self.load_place_ui()
		self.cn.bind("<Button-1>", self._interactp)
		
	
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
			lx, ly = event.x, event.y - 35
			'''
			if (lx < self.mlmt[0] or lx >= self.mlmt[2] or
				ly < self.mlmt[1] or ly >= self.mlmt[3]):
				#return  # out of range  give max instead
			'''
			if lx < self.mlmt[0]: lx = self.mlmt[0]
			elif lx > self.mlmt[2]: lx = self.mlmt[2]
			if ly < self.mlmt[1]: ly = self.mlmt[1]
			elif ly > self.mlmt[3]: ly = self.mlmt[3]
			if lx < px:
				self.cn.itemconfigure(self.zbox.m("pPlyr"),
					image=self.rsc["{}F".format(self.pdata["place_image"])])
			else:
				self.cn.itemconfigure(self.zbox.m("pPlyr"),
					image=self.rsc[self.pdata["place_image"]])
			x, y = lx-px, ly-py
			dist = math.sqrt(abs(x)**2 + abs(y)**2)
			steps = dist / 4.25  # player speed 5.0 max
			ax = x / steps
			ay = y / steps
			evt = None
			for i in id_tags:
				txt = self.zbox.m("{}_P".format(self.place))
				if i[:len(txt)] == txt:
						evt = self.place_places[i]
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
			self.cn.itemconfigure(self.zbox.m("pPlyr"),
				image=self.rsc[self.pdata["place_image"]])
			if evt is not None:
				evt()
	
	
	def load_place_ui(self, *args):
		self.zbox.mimg(0, 0, self.placedata["image"], "place_image")
		try:
			if self.placedata["leave_btn"]:
				self.zbox.mbtn(717, 548, "Leave", self._leave_place,
					w=80, h=48, font=(self.fn[0], 17), txty_change=8)
		except: pass  # no leave_btn
		e = self.placedata["events"]
		for evt in e:
			tag0 = "{}_P{}".format(self.place, evt[2])
			tag = self.zbox.m(tag0)
			if evt[0] != None: continue  # next iteration
			if evt[1] != None:  # event
				act = evt[1].split("|")
				if act[0] == "plc":  # place
					command = lambda n=act[1]: self._go_plc(n)
				elif act[0] == "dlg":  # dialog
					command = lambda n=act[1]: self._go_dlg(n)
				elif act[0] == "str":  # store, trade between 2 characters
					command = lambda n=act[1]: self._go_str(n)
				elif act[0] == "box":  # lootbox
					command = lambda n=act[1]: self._go_box(n)	
				self.place_places[tag] = command
				#self.cn.tag_bind(tag, "<Button-1>", command)
			# ie: "450-200|map_lurco-50x50"
			img_data = evt[3].split("|")
			coords = [int(x) for x in img_data[0].split("-")]
			img = img_data[1]
			self.place_place(coords[0], coords[1], evt[2], img, tag0)
		self.zbox.mimg(self.sxy[0], self.sxy[1], self.pdata["place_image"],
			"pPlyr", "center")	
		self.zbox.raise_ctags()
		self._reset_aktivui()
		
	
	def load_variables(self, *args):
		self.place_list = self.world.map[self.world.current_region]["places"]
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
	
	
	def place_place(self, x, y, pname, image, tag=None, *args):
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
		self.zbox.mimg(x, y, image, (tag, tag+"_img", "place_image"),
			anchor="center")
		h = int(image[-2:])  # height 99px max
		add = (h / 2) + 8
		self.zbox.mtxt(x, y-add, pname, (tag, tag+"_txt", "place_image"),
			(self.fn[0], 12), "center", fill="#441122")
		#tagn = self.zbox.m(tag+"_img")
		tagn = self.zbox.m(tag)
		self.cn.tag_bind(tagn, "<Enter>", lambda _=1: phover())
		self.cn.tag_bind(tagn, "<Leave>", lambda _=1: phover("l"))
	
	
	def _go_box(self, container, *args):
		def lv_box(s=0, *args):
			if s == 0:
				self.aktiv_ui = True
				self.parent.after(100, lambda _=1: lv_box(1))
			else:
				self.aktiv_ui = False
		if not self.world.aktiv_caUI:
			self.aktiv_ui = True
			bg = self.placedata["image"]
			self.world.start_tradebox(container, extract=lv_box, bg=bg)	
	
	
	def _go_dlg(self, dialog_id, *args):
		if not self.world.aktiv_caUI:
			#self.hoverstats_fade()
			self.cn.delete(self.mtag)
			self.world.start_dialog(dialog_id)
	
	
	def _go_plc(self, evt, *args):
		pass
	
	
	def _go_str(self, merchant, *args):
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
			self.world.start_store(merchant, bg=self.placedata["image"],
				extract=lv_str)
	
	
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
		self.zbox.mimg(20, 50, "dtxt_bg-760x485")
		self.zbox.mimg(30, 61, "dtxt_txtbg-530x465")
		self.zbox.mimg(570, 61, "dtxt_choices-200x466")
		#self.zbox.mtxt(40, 81, "", "title", font=(self.fn[0], 15, "bold"))
		self.zbox.mtxt(295, 81, "", "title", font=(self.fn[0], 15, "bold"), anchor="n")
		self.zbox.mtxt(40, 120, "", "text", width=510)
		self.zbox.mtxt(42, 410, "", "rwd_text", self.ftheme[1], width=510)
		self.zbox.mtxt(670, 85, "Active Quests", None,
			(self.fn[0], 15), "center")
		self.zbox.mtxt(630, 242, "<<<", "ak<<<", (self.fn[1], 16), "center")
		self.zbox.mtxt(710, 242, ">>>", "ak>>>", (self.fn[1], 16), "center")
		self.zbox.mtxt(670, 277, "Leave Quests Screen", "leave_btn",
			(self.fn[1], 14), "center")
		tagl = self.zbox.m("leave_btn")
		self.cn.tag_bind(tagl, "<Enter>", 
			lambda _=1: self.cn.itemconfigure(tagl, fill="orange"))
		self.cn.tag_bind(tagl, "<Leave>",
			lambda _=1: self.cn.itemconfigure(tagl, fill="black"))
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
			x = 100
			self.zbox.mimg(575, x+(i*33), ci, (tag0, tag0+"_img", "akitem"))
			self.zbox.mtxt(582, x+5+(i*33), self.quests[qname]["name"], (tag0, "akitem"))
			self.cn.tag_bind(tag, "<Enter>", lambda _=1, t=tag0: qhover(t))
			self.cn.tag_bind(tag, "<Leave>", lambda _=1, t=tag0: qhover(t, 0))
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
			self.cn.tag_bind(tag, "<Enter>", lambda _=1, t=tag0: qhover(t))
			self.cn.tag_bind(tag, "<Leave>", lambda _=1, t=tag0: qhover(t, 0))
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
		self.zbox.mimg(x, y, "zibox_bg-150x105", tag)
		self.zbox.mrect(x+3, y+3, 144, 78, "#776611", tag)
		self.zbox.mrect(x+3, y+81, 49, 21, "#774411", tag)
		self.zbox.mrect(x+52, y+81, 95, 21, "#773311", tag)
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
		self.cn.itemconfigure(self.zbox.m("brtr_txt"), fill="yellow")
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
		self.zbox.mimg(20, 50, "dtxt_bg-760x485")
		self.zbox.mimg(20, 50, "dtxt_upbar-760x25")
		# player info panel
		X, Y = 45, 93
		self.zbox.mimg(X, Y, "inv_cbg-280x105")
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
			self.zbox.mrect(x0, y0+(i*23), 74, 21, fill="brown")
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
				p = self.items[pnv[n]]["image"] if pnv[n] != "e" else "invi_e"
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
		self.zbox.mimg(X2, Y2, "inv_cbg-280x105")
		self.zbox.mimg(X2+180, Y2, m["avatar"])
		self.zbox.mimg(X2+6, Y2+23, "btn_think-45x75", "b_reset")
		self.zbox.mimg(X2+53, Y2+23, "btn_leave-45x75", "b_leave")
		self.cn.tag_bind(self.zbox.m("b_reset"), "<Button-1>", self.reset_inv)
		self.cn.tag_bind(self.zbox.m("b_leave"), "<Button-1>", self._exit_str)
		self.zbox.mtxt(X2+103, Y2+7, m["name"], font=self.ftheme[1])
		self.zbox.mtxt(X2+9, Y2+5, "Scnr:")
		self.zbox.mtxt(X2+94, Y2+5, m["coin"], "mcoin", anchor="ne")
		x1, y1 = X2 + 102, Y2 + 29
		for i in range(3): self.zbox.mrect(x1, y1+(i*23), 74, 21, "brown")
		# merchant inventory
		inv2 = m["inventory"]
		mnv = inv2 + ["e"] * (24 - len(inv2))
		X3, Y3 = X2, Y2 + 110
		for rw in range(4):
			for cl in range(6):
				n = cl + (rw * 6)
				p = self.items[mnv[n]]["image"] if mnv[n] != "e" else "invi_e"
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
				pnvimg = mnvimg = "invi_e"
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
		self.zbox.mimg(x, y, "zibox_bg-150x105", tag)
		self.zbox.mrect(x+3, y+3, 144, 78, "#776611", tag)
		self.zbox.mrect(x+3, y+81, 49, 21, "#774411", tag)
		self.zbox.mrect(x+52, y+81, 95, 21, "#773311", tag)
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
			self.cn.itemconfigure(tag, fill="yellow")
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
		self.zbox.mimg(400, 50, "trdbox_bg-635x485", anchor="n")
		self.zbox.mimg(400, 50, "trdbox_upbar-635x25", anchor="n")
		# player info panel
		X, Y = 109, 93
		self.zbox.mimg(X, Y, "inv_cbg-280x105")
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
			self.zbox.mrect(x0, y0+(i*23), 74, 21, fill="brown")
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
				p = self.items[pnv[n]]["image"] if pnv[n] != "e" else "invi_e"
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
		X2, Y2 = 412, 93
		''' destroys symmetry.
		X3, Y3 = X2, Y2 + 110
		try:
			self.zbox.mimg(X3-15, Y3-60, self.cdata["box_image"], anchor="nw")
		except: pass
		'''
		self.zbox.mimg(X2, Y2, "inv_cbg-280x105")
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
			self.zbox.mrect(x1, y1+(i*23), 74, 21, "brown")
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
				p = self.items[mnv[n]]["image"] if mnv[n] != "e" else "invi_e"
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
				pnvimg = cnvimg = "invi_e"
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
		self.zbox.mimg(x, y, "zibox_bg-150x105", tag)
		self.zbox.mrect(x+3, y+3, 144, 78, "#776611", tag)
		self.zbox.mrect(x+3, y+81, 49, 21, "#774411", tag)
		self.zbox.mrect(x+52, y+81, 95, 21, "#773311", tag)
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
			self.cn.itemconfigure(tag, fill="yellow")
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
	

	def mrect(self, x1, y1, w, h, fill="black", tags=None, c=None, width=0):
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
			
