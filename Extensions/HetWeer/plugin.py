from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.MenuList import MenuList
from Components.Label import Label
from Components.ActionMap import ActionMap, HelpableActionMap
from Components.Pixmap import Pixmap
from twisted.web.client import downloadPage, getPage
from Screens.MessageBox import MessageBox
from enigma import ePicLoad, getDesktop, eTimer
from Components.AVSwitch import AVSwitch
import urllib2, urllib
import os
from Tools.Directories import resolveFilename, SCOPE_CONFIG, SCOPE_PLUGINS
from Screens.HelpMenu import HelpableScreen
from Components.FileList import FileList
#from Screens.InfoBarGenerics import InfoBarAspectSelection

#ikeuze = " "
#sz_w = 200
#sz_h = 300

def getScale():
	return AVSwitch().getFramebufferScale()

class Weermenu(Screen):
	skin = """
		<screen position="center,center" size="360,380" title="Het weer" >
			<widget name="list" position="10,0" size="340,280" scrollbarMode="showOnDemand" />
			<widget name="Text" position="center,280" size="360,100" halign="center" font="Regular;22" />
                </screen>"""
		
	def __init__(self, session, args = 0):
		self.session = session
		Screen.__init__(self, session)
		
		self["list"] = MenuList([])		
		self["Text"] = Label("=--Weer App--=\nMade by DEG 2012~!")
		self["myActionMap"] = ActionMap(["OkCancelActions"], {"ok": self.okClicked, "cancel": self.cancel}, -1)
		
		self.weer = []
		self.weer.append("Neerslag + Wolken Radar")
		self.weer.append("Temperatuur")
		self.weer.append("Onweer")
		self.weer.append("Pluimgrafiek")
		self["list"].setList(self.weer)

	def cancel(self):
		self.close(None)
		
	def okClicked(self):
		iweer = self["list"].getSelectionIndex()
		self.session.open(secondmenu, iweer)

			



class secondmenu(Screen):
	skin = """
		<screen position="center,center" size="360,290" title="Het weer" >
			<widget name="list" position="10,0" size="340,200" scrollbarMode="showOnDemand" />
			<widget name="Text" position="center,210" size="360,90" halign="center" font="Regular;22" />
		</screen>"""
	
	def __init__(self, session, iweer, ktekst = None ,urlpart1 = None):
		self.skin = secondmenu.skin
		Screen.__init__(self, session)
		
		self["list"] = MenuList([])
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.okClicked, "cancel": self.cancel}, -1)
		self.options = []
		self.iweerOptie = iweer
		self.urlp1 = urlpart1
		dir = "/tmp/HetWeer/"
		if not os.path.exists(dir):
			os.makedirs(dir)
		#if os.path.exists("/tmp/HetWeer/") is not True:
		#	os.path.mkdir("/tmp/HetWeer/")
		if self.iweerOptie == 40:
			#self["Text"] = Label("=--blabla App--=\nMade by DEG 2012~!")
			self["Text"] = Label(_("=--%s--=\nMade by DEG 2012~!") %(ktekst))
		else:
			self["Text"] = Label("=--Weer App--=\nMade by DEG 2012~!")
		self.onLayoutFinish.append(self.lijst)
		
	def cancel(self):
		self.close(None)
		
	def lijst(self):
		print "text ", self.iweerOptie
		if self.iweerOptie == 0:
			#neerslag radar
			self.options = []
			self.imgurl = []
			
			self.options.append("Buienradar NL")
			self.options.append("2 uur vooruit NL")
			self.options.append("(Sat)Bewolking NL")
			self.options.append("(Sat)Bewolking Eu")
			self.options.append("Meteox Eu")
			self.options.append("3 Dagen vooruit Eu")
			self.options.append("Sneeuw NL")
			self.options.append("Buienradar Belgie")
			
			self.imgurl.append("http://www.buienradar.nl")
			self.imgurl.append("http://www.buienradar.nl")
			self.imgurl.append("http://sat24.com/nl/nl")
			self.imgurl.append("http://sat24.com/nl/eu")
			self.imgurl.append("http://europa.buienradar.nl/h.aspx?r=&jaar=-3&soort=loop1uur")
			self.imgurl.append("http://europa.buienradar.nl/3daagse.aspx")
			self.imgurl.append("http://www.onweer-online.nl/images/maps/sneeuwradar.gif")
			self.imgurl.append("http://www.buienradar.be")
			
			self["list"].setList(self.options)
			
		elif self.iweerOptie == 1:
			#Temperatuur
			self.options = []
			self.imgurl = []
			self.options.append("Knmi")
			self.options.append("Gevoelstemperatuur")
			self.options.append("Weerplaza")
			self.options.append("Weerplaza grond")
			self.options.append("Weerplaza Weerbeeld")
			
			self.imgurl.append("http://www.onweer-online.nl/images/maps/tempknmi.png")
			self.imgurl.append("http://www.onweer-online.nl/images/maps/knmi_windchill.png")
			self.imgurl.append("http://www.onweer-online.nl/images/maps/weerplaza_temperatuu.png")
			self.imgurl.append("http://www.onweer-online.nl/images/maps/temperatuur_10_cm.png")
			self.imgurl.append("http://www.onweer-online.nl/images/maps/weerplaza_weerbeeld.jpg")
			
			self["list"].setList(self.options)
			
		elif self.iweerOptie == 2:
			#Onweer
			self.options = []
			self.imgurl = []
			self.options.append("Bliksem.nu")
			self.options.append("Station Woerden")
			self.options.append("Station Mechelen")
			self.options.append("Station Zoetermeer")
			self.options.append("Blids.de")
			
			self.imgurl.append("http://www.onweer-online.nl/images/maps/Bliksem.nu.png")
			self.imgurl.append("http://www.onweer-online.nl/images/maps/weerstation_woerden.png")
			self.imgurl.append("http://www.onweer-online.nl/images/maps/weerstation_mechelen.png")
			self.imgurl.append("http://www.onweer-online.nl/images/maps/weerzoetermeer.png")
			self.imgurl.append("http://www.onweer-online.nl/images/maps/blids.jpg")
			
			self["list"].setList(self.options)
			
		elif self.iweerOptie == 3:
			#Pluimen
			self.options = []
			self.imgurl = []
			self.options.append("Noord")
			self.options.append("Noord-West")
			self.options.append("Noord-Oost")
			self.options.append("Midden-West")
			self.options.append("Midden")
			self.options.append("Midden-Oost")
			self.options.append("Zuid-West")
			self.options.append("Zuid")
			self.options.append("Zuid-Oost")
			
			
			self.imgurl.append("http://grafiek.buienradar.nl/chart.ashx?w=1180&h=550&region=NL020")
			self.imgurl.append("http://grafiek.buienradar.nl/chart.ashx?w=1180&h=550&region=NL015")
			self.imgurl.append("http://grafiek.buienradar.nl/chart.ashx?w=1180&h=550&region=NL018")
			self.imgurl.append("http://grafiek.buienradar.nl/chart.ashx?w=1180&h=550&region=NL011")
			self.imgurl.append("http://grafiek.buienradar.nl/chart.ashx?w=1180&h=550&region=NL012")
			self.imgurl.append("http://grafiek.buienradar.nl/chart.ashx?w=1180&h=550&region=NL009")
			self.imgurl.append("http://grafiek.buienradar.nl/chart.ashx?w=1180&h=550&region=NL002")
			self.imgurl.append("http://grafiek.buienradar.nl/chart.ashx?w=1180&h=550&region=NL004")
			self.imgurl.append("http://grafiek.buienradar.nl/chart.ashx?w=1180&h=550&region=NL001")
			
			
			self["list"].setList(self.options)
			
			
		elif self.iweerOptie == 40:
			#Pluimen
			self.options = []
			self.imgurl = []
			self.options.append("Neerslag")
			self.options.append("Temperatuur")
			self.options.append("Dauwpunt")
			self.options.append("Windrichting")
			self.options.append("Windsnelheid")
			self.options.append("Windstoten")
			self.options.append("Sneeuw/hagel/ijs neerslag")
			self.options.append("Bewolking")
			
			
			self.imgurl.append("&ecmwftype=13011&ctype=3")
			self.imgurl.append("&ecmwftype=12004&ctype=3")
			self.imgurl.append("&ecmwftype=12006&ctype=3")
			self.imgurl.append("&ecmwftype=11011&ctype=3")
			self.imgurl.append("&ecmwftype=11012&ctype=3")
			self.imgurl.append("&ecmwftype=11041&ctype=3")
			self.imgurl.append("&ecmwftype=13233&ctype=3")
			self.imgurl.append("&ecmwftype=20010&ctype=3")
			
			
			self["list"].setList(self.options)
			
			
	def okClicked(self):
		ioptie = self["list"].getSelectionIndex()
		iweeroption = self.imgurl[ioptie]
		self.keuzetekst = self.options[ioptie]
		self.url = iweeroption
		try:
			if self.iweerOptie == 3:
				iweer = 40
				self.urlpart1 = iweeroption
				self.session.open(secondmenu, iweer, self.keuzetekst, self.urlpart1)
			elif self.iweerOptie == 40:
				url = self.urlp1 + self.url
				downloadPage(url,"/tmp/HetWeer.png").addCallback(self.downloadDone).addErrback(self.downloadError)
			elif self.keuzetekst == "Buienradar NL":
				getPage(self.url).addCallback(self.BRdone).addErrback(self.downloadError)
			elif self.keuzetekst == "2 uur vooruit NL":
				getPage(self.url).addCallback(self.BRVdone).addErrback(self.downloadError)
			elif self.keuzetekst == "Buienradar Belgie":
				getPage(self.url).addCallback(self.BRBEdone).addErrback(self.downloadError)
			elif self.keuzetekst == "Meteox Eu":
				getPage(self.url).addCallback(self.BRMEdone).addErrback(self.downloadError)
			elif self.keuzetekst == "3 Dagen vooruit Eu":
				getPage(self.url).addCallback(self.BR3Ddone).addErrback(self.downloadError)
			elif self.keuzetekst == "(Sat)Bewolking NL" or self.keuzetekst == "(Sat)Bewolking Eu":
				getPage(self.url).addCallback(self.Sat24done).addErrback(self.downloadError)
			else:
				downloadPage(self.url,"/tmp/HetWeer.png").addCallback(self.downloadDone).addErrback(self.downloadError)
		except:
			return
		


	def downloadError(self, raw):
		print "[e2Fetcher.fetchPage]: download Error", raw
		try:
			self.session.open(MessageBox, text = _("Error downloading"), type = MessageBox.TYPE_ERROR)
		except:
			return
		
	def downloadDone(self,raw):
		self.session.open(PictureScreen)
		
	def BRdone(self,raw):
		i = 0
		j = 0
		iurllast = " "
		self.urls = []
		n0 = 0
		n1 = raw.find('<div class="time-list"><ul class="time-list-cols">', (n0+15))
		print "n1 = ", n1
		while i<15:
			n2 = raw.find('href="',(n1+2))
			if n2<0:
				break
				
			print "n2 = ", n2	
			n3 = raw.find('/',(n2+8))
			if n3<0:
				break
			
			checkn2n3 = raw[(n2+6):(n3+1)]
			print checkn2n3
			checkradar = checkn2n3.find('/radar/',0)
			checkradaronweer = checkn2n3.find('/radar-onweer/',0)
			if checkradar<0 and checkradaronweer<0:
				print "break radar or onweer"
				break
						
			n4 = raw.find('"',(n2+8))
			if n4<0:
				break
			#http://www.buienradar.nl/image/?time=201211201645&type=lightning&extension=png
			iurl = "http://www.buienradar.nl/image/?time=" + raw[(n3+1):(n4)] + "&type=lightning&extension=png"
			print iurl
			check = iurl.find('20',0)
			if check<0:
				break
			#print raw[(n2+2):(n3)]
			print j
			if j>9:
				png = "/tmp/HetWeer/%s.png" % j
			else:
				png = "/tmp/HetWeer/0%s.png" % j
			print png
			try:
				urllib.urlretrieve(iurl, png)
			except:
				break
			
				
			n1 = (n3+1)
			j=j+1
			i=i+1
		
		
		try:
			self.session.open(View_Slideshow, j)
		except:
			return
		
		
		
	def BRVdone(self,raw):
		i = 0
		j = 0
		iurllast = " "
		self.urls = []
		n0 = raw.find('<div class="time-list"><ul class="time-list-cols">', 0)
		n1 = raw.find('<div class="time-list"><ul class="time-list-cols">', (n0+15))
		print "n1 = ", n1
		while i<25:
			n2 = raw.find('href="',(n1+2))
			if n2<0:
				break
				
			print "n2 = ", n2	
			n3 = raw.find('/',(n2+8))
			if n3<0:
				break
			
			checkn2n3 = raw[(n2+6):(n3+1)]
			print checkn2n3
			checkradar = checkn2n3.find('/radar-verwachting/',0)
			if checkradar<0:
				print "break verwachting"
				break
						
			n4 = raw.find('"',(n2+8))
			if n4<0:
				break
			#http://www.buienradar.nl/image/?time=201211201645&type=lightning&extension=png
			iurl = "http://www.buienradar.nl/image/?time=" + raw[(n3+1):(n4)] + "&type=forecast&extension=png"
			print iurl
			check = iurl.find('20',0)
			if check<0:
				break
			#print raw[(n2+2):(n3)]
			print j
			if j>9:
				png = "/tmp/HetWeer/B%s.png" % j
			else:
				png = "/tmp/HetWeer/B0%s.png" % j
			print png
			try:
				urllib.urlretrieve(iurl, png)
			except:
				break
			
				
			n1 = (n3+1)
			j=j+1
			i=i+1
		
		print "shuffle time"
		last=j-1
		j = 0
		print last
		while last>-1:
			
			if j>9:
				png = "/tmp/HetWeer/%s.png" % j
			else:
				png = "/tmp/HetWeer/0%s.png" % j
				
			if last>9:
				before = "/tmp/HetWeer/B%s.png" % last
			else:
				before = "/tmp/HetWeer/B0%s.png" % last
			
			print before
			print png
			try:
				os.rename(before, png)
			except:
				break
			
			last = last-1
			j=j+1



		try:
			self.session.open(View_Slideshow, j)
		except:
			return
			
			
		
	def BRBEdone(self,raw):
		i = 0
		j = 0
		iurllast = " "
		self.urls = []
		n0 = 0
		print "n0 = ", n0
		n1 = raw.find('<ul class="timeurls">', (n0+15))
		print "n1 = ", n1
		while i<11:
			n2 = raw.find('href="',(n1+2))
			if n2<0:
				break
				
			print "n2 = ", n2	
			n3 = raw.find('/',(n2+8))
			if n3<0:
				break
				
			checkn2n3 = raw[(n2+6):(n3+1)]
			print checkn2n3
			checkradar = checkn2n3.find('/radar/',0)
			checkradaronweer = checkn2n3.find('/radar-onweer/',0)
			if checkradar<0 and checkradaronweer<0:
				print "break radar or onweer"
				break
						
			n4 = raw.find('"',(n2+8))
			if n4<0:
				break	
			iurl = "http://www.buienradar.be/image/?time=" + raw[(n3+1):(n4)]
			print iurl
			print j
			if j>9:
				png = "/tmp/HetWeer/%s.png" % j
			else:
				png = "/tmp/HetWeer/0%s.png" % j
			print png
			try:
				urllib.urlretrieve(iurl, png)
			except:
				break
				
			n1 = (n3+1)
			j=j+1
			i=i+1
		
		try:
			self.session.open(View_Slideshow, j)
		except:
			return
		
	def BRMEdone(self,raw):
		i = 0
		j = 0
		iurllast = " "
		self.urls = []

		n1 = raw.find('<span id="ctl00_lblTabel">', 0)
		print "n1 = ", n1
		while i<14:
			n2 = raw.find('<a href="h.aspx?',(n1+11))
			if n2<0:
				break
				
			print "n2 = ", n2	
			n3 = raw.find('"',(n2+10))
			if n3<0:
				break
				
			print "n3 = ", n3	
			iurl = "http://europa.buienradar.nl/images.aspx?" + raw[(n2+16):(n3)]
			print iurl

			print j
			if j>9:
				png = "/tmp/HetWeer/%s.png" % j
			else:
				png = "/tmp/HetWeer/0%s.png" % j
			print png
			try:
				urllib.urlretrieve(iurl, png)
			except:
				break

				
			n1 = (n3+1)
			j=j+1
			i=i+1
		

		try:
			self.session.open(View_Slideshow, j)
		except:
			return
		
		
	def BR3Ddone(self,raw):
		i = 0
		j = 0
		iurllast = " "
		self.urls = []

		n1 = raw.find('<table style="text-align:center" align="center">', 0)
		print "n1 = ", n1
		while i<24:
			n2 = raw.find('<a href="3daagse.aspx?',(n1+11))
			if n2<0:
				break
				
			print "n2 = ", n2	
			n3 = raw.find('"',(n2+10))
			if n3<0:
				break
				
			print "n3 = ", n3	
			iurl = "http://europa.buienradar.nl/images.aspx?" + raw[(n2+22):(n3)]
			print iurl
			#print raw[(n2+2):(n3)]
			print j
			if j>9:
				png = "/tmp/HetWeer/B%s.png" % j
			else:
				png = "/tmp/HetWeer/B0%s.png" % j
			print png
			try:
				urllib.urlretrieve(iurl, png)
			except:
				break

				
			n1 = (n3+1)
			j=j+1
			i=i+1
		
		print "shuffle time"
		last=j-1
		j = 0
		print last
		while last>-1:
			
			if j>9:
				png = "/tmp/HetWeer/%s.png" % j
			else:
				png = "/tmp/HetWeer/0%s.png" % j
				
			if last>9:
				before = "/tmp/HetWeer/B%s.png" % last
			else:
				before = "/tmp/HetWeer/B0%s.png" % last
			
			print before
			print png
			try:
				os.rename(before, png)
			except:
				break
			
			last = last-1
			j=j+1


		
		try:
			self.session.open(View_Slideshow, j)
		except:
			return
		
		
	def Sat24done(self,raw):
		i = 0
		j = 0
		iurllast = " "
		self.urls = []
		#n0 = raw.find('<div id="leftnav">',0)
		n0 = 0
		#if n0<0:
		#	break
		print "n0 = ", n0
		n1 = raw.find('var imageUrls', (n0+10))
		print "n1 = ", n1
		while i<9:
			n2 = raw.find('/image2.ashx?region',(n1+11))
			if n2<0:
				break
				
			print "n2 = ", n2	
			n3 = raw.find('"',(n2+10))
			if n3<0:
				break
				
			print "n3 = ", n3	
			iurl = "http://www.sat24.com" + raw[(n2):(n3)]
			print iurl
			#print raw[(n2+2):(n3)]
			print j
			if j>9:
				png = "/tmp/HetWeer/%s.png" % j
			else:
				png = "/tmp/HetWeer/0%s.png" % j
			print png
			try:
				urllib.urlretrieve(iurl, png)
			except:
				break

				
			n1 = (n3+1)
			j=j+1
			i=i+1
		

		try:
			self.session.open(View_Slideshow, j)
		except:
			return
			
			
			
#show picture:

class PictureScreen(Screen):
	sz_w = getDesktop(0).size().width()
	sz_h = getDesktop(0).size().height()
	
	skin="""
		<screen name="Na Regen Komt Zonneschijn" position="center,center" size="%d,%d" title="Picture Screen" backgroundColor="noTransBG" scrollbarMode="showOnDemand" >
			<widget name="myPic" position="center,center" size="%d,%d" zPosition="1" alphatest="on" scrollbarMode="showOnDemand" />
		</screen>"""%( sz_w, sz_h, (sz_w - 55), (sz_h - 50) )

	def __init__(self, session):
		Screen.__init__(self, session)
		print "[PictureScreen] __init__\n"
		self.picPath = "/tmp/HetWeer.png"
		self.Scale = AVSwitch().getFramebufferScale()
		self.PicLoad = ePicLoad()
		self["myPic"] = Pixmap()
		self["myActionMap"] = ActionMap(["SetupActions"],
			{
				"ok": self.cancel,
				"cancel": self.cancel
			}, -1)
		self.PicLoad.PictureData.get().append(self.DecodePicture)
		self.onLayoutFinish.append(self.ShowPicture)
		
	def ShowPicture(self):
		if self.picPath is not None:
			self.PicLoad.setPara([
					self["myPic"].instance.size().width(),
					self["myPic"].instance.size().height(),
					self.Scale[0],
					self.Scale[1],
					0,
					1,
			"#002C2C39"])
			self.PicLoad.startDecode(self.picPath)
			
	def DecodePicture(self, PicInfo = ""):
		if self.picPath is not None:
			ptr = self.PicLoad.getData()
			self["myPic"].instance.setPixmap(ptr)
			
	def cancel(self):
		print "[PictureScreen] - cancel\n"
		self.close(None)
		
		
		
##########################


		
#------------------------------------------------------------------------------------------
#---------------------- class InfoBarAspectSelection --------------------------------------
#------------------------------------------------------------------------------------------

class InfoBarAspectSelection:
	STATE_HIDDEN = 0
	STATE_ASPECT = 1
	STATE_RESOLUTION = 2
	def __init__(self):
		self["AspectSelectionAction"] = HelpableActionMap(self, "InfobarAspectSelectionActions",
			{
				"aspectSelection": (self.ExGreen_toggleGreen, _("Aspect list...")),
			})
		self.__ExGreen_state = self.STATE_HIDDEN

	def ExGreen_doAspect(self):
		self.__ExGreen_state = self.STATE_ASPECT
		self.aspectSelection()

	def ExGreen_doResolution(self):
		self.__ExGreen_state = self.STATE_RESOLUTION
		self.resolutionSelection()

	def ExGreen_doHide(self):
		self.__ExGreen_state = self.STATE_HIDDEN

	def ExGreen_toggleGreen(self, arg=""):
		if debug: print pluginPrintname, self.__ExGreen_state
		if self.__ExGreen_state == self.STATE_HIDDEN:
			if debug: print pluginPrintname, "self.STATE_HIDDEN"
			self.ExGreen_doAspect()
		elif self.__ExGreen_state == self.STATE_ASPECT:
			if debug: print pluginPrintname, "self.STATE_ASPECT"
			self.ExGreen_doResolution()
		elif self.__ExGreen_state == self.STATE_RESOLUTION:
			if debug: print pluginPrintname, "self.STATE_RESOLUTION"
			self.ExGreen_doHide()

	def aspectSelection(self):
		selection = 0
		tlist = []
		tlist.append((_("Resolution"), "resolution"))
		tlist.append(("", ""))
		tlist.append((_("Letterbox"), "letterbox"))
		tlist.append((_("PanScan"), "panscan"))
		tlist.append((_("Non Linear"), "non"))
		tlist.append((_("Bestfit"), "bestfit"))
		mode = open("/proc/stb/video/policy").read()[:-1]
		if debug: print pluginPrintname, mode
		for x in range(len(tlist)):
			if tlist[x][1] == mode:
				selection = x
		keys = ["green", "",  "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ]
		self.session.openWithCallback(self.aspectSelected, ChoiceBox, title=_("Please select an aspect ratio..."), list = tlist, selection = selection, keys = keys)

	def aspectSelected(self, aspect):
		if not aspect is None:
			if isinstance(aspect[1], str):
				if aspect[1] == "resolution":
					self.ExGreen_toggleGreen()
				else:
					open("/proc/stb/video/policy", "w").write(aspect[1])
					self.ExGreen_doHide()
		return		
#----------
# player pics

class View_Slideshow(Screen, InfoBarAspectSelection):

	def __init__(self, session, pindex, startslide=True):

		#pindex = 0 
		print "SlideShow is running ......."
		self.textcolor = "#ffffff"
		self.bgcolor = "#000000"
		space = 35
		size_w = getDesktop(0).size().width()
		size_h = getDesktop(0).size().height()

		self.skindir = "/tmp"
		self.skin = "<screen name=\"Na Regen Komt Zonneschijn\" position=\"0,0\" size=\"" + str(size_w) + "," + str(size_h) + "\" flags=\"wfNoBorder\" > \
			<eLabel position=\"0,0\" zPosition=\"0\" size=\""+ str(size_w) + "," + str(size_h) + "\" backgroundColor=\""+ self.bgcolor +"\" /> \
			<widget name=\"pic\" position=\"" + str(space) + "," + str(space) + "\" size=\"" + str(size_w-(space*2)) + "," + str(size_h-(space*2)) + "\" zPosition=\"1\" alphatest=\"on\" /> \
			<widget name=\"file\" position=\""+ str(space+45) + "," + str(space+10) + "\" size=\""+ str(size_w-(space*2)-50) + ",25\" font=\"Regular;20\" halign=\"left\" foregroundColor=\"" + self.textcolor + "\" zPosition=\"2\" noWrap=\"1\" transparent=\"1\" /> \
			</screen>"
		Screen.__init__(self, session)

		InfoBarAspectSelection.__init__(self)
		self["actions"] = ActionMap(["OkCancelActions", "MediaPlayerActions", "DirectionActions", "MovieSelectionActions"],
			{
				"cancel": self.Exit,
				"playpauseService": self.PlayPause,
				"play": self.PlayPause,
				"pause": self.PlayPause,
				"left": self.prevPic,
				"right": self.nextPic,
				"seekFwd": self.nextPic,
				"seekBack": self.prevPic,
			}, -1)

		self["pic"] = Pixmap()
		self["file"] = Label(_("Please wait, photo is being loaded ..."))
		self.old_index = 0
		self.picfilelist = []
		self.lastindex = pindex - 1
		self.currPic = []
		self.shownow = True
		self.dirlistcount = 0
		#speed to play! (self.speed*100)
		self.speed = 8

		devicepath = "/tmp/HetWeer/"
		currDir = devicepath
		self.filelist = FileList(currDir, showDirectories = False, matchingPattern = "^.*\.(png)", useServiceRef = False)

		for x in self.filelist.getFileList():
			if x[0][1] == False:
				try:
					self.picfilelist.append(currDir + x[0][0])
				except:
					break
			else:
				self.dirlistcount += 1

		self.maxentry = pindex - 1
		#len(self.picfilelist)-1
		self.pindex = pindex - 1
		if self.pindex < 0:
			self.pindex = 0
		self.picload = ePicLoad()
		self.picload.PictureData.get().append(self.finish_decode)
		self.slideTimer = eTimer()
		self.slideTimer.callback.append(self.slidePic)
		if self.maxentry >= 0:
			self.onLayoutFinish.append(self.setPicloadConf)
		if startslide == True:
			self.PlayPause();

	def setPicloadConf(self):
		sc = getScale()
		self.picload.setPara([self["pic"].instance.size().width(), self["pic"].instance.size().height(), sc[0], sc[1], 0, int(0), self.bgcolor])
		if False == False:
			self["file"].hide()
		self.start_decode()

	def ShowPicture(self):
		if self.shownow and len(self.currPic):
			self.shownow = False
			self["file"].setText(self.currPic[0].replace(".png",""))
			self.lastindex = self.currPic[1]
			self["pic"].instance.setPixmap(self.currPic[2].__deref__())
			self.currPic = []
			self.next()
			self.start_decode()

	def finish_decode(self, picInfo=""):
		ptr = self.picload.getData()
		if ptr != None:
			text = ""
			try:
				text = picInfo.split('\n',1)
				text = "(" + str(self.pindex+1) + "/" + str(self.maxentry+1) + ") " + text[0].split('/')[-1]
			except:
				pass
			self.currPic = []
			self.currPic.append(text)
			self.currPic.append(self.pindex)
			self.currPic.append(ptr)
			self.ShowPicture()

	def start_decode(self):
		self.picload.startDecode(self.picfilelist[self.pindex])

	def next(self):
		self.pindex -= 1
		if self.pindex < 0:
			self.pindex = self.maxentry

	def prev(self):
		self.pindex += 1
		if self.pindex > self.maxentry:
			self.pindex = 0

	def slidePic(self):
		print "slide to next Picture index=" + str(self.lastindex)
		if True==False and self.lastindex == self.maxentry:
			self.PlayPause()
		self.shownow = True
		self.ShowPicture()

	def PlayPause(self):
		if self.slideTimer.isActive():
			self.slideTimer.stop()
		else:
			self.slideTimer.start(self.speed*100)
			self.nextPic()

	def prevPic(self):
		self.currPic = []
		self.pindex = self.lastindex
		self.prev()
		self.start_decode()
		self.shownow = True

	def nextPic(self):
		self.shownow = True
		self.ShowPicture()

	def Exit(self):
		#del self.picload
		#for file in self.picfilelist:
		#	print 'filelist ', file
		#	try:
		#		if debug: print pluginPrintname, file
		#		os.unlink(file)
		##	except:
		#		pass
		try:
			self.removedir = '/tmp/HetWeer/'
			#self.png = '.png'
			start = 0
			print 'max files: ', self.maxentry
			if self.maxentry < 10:
				print 'Less then 10'
				while start < (self.maxentry + 1):
					print 'go'
					pngfile = '/tmp/HetWeer/0' + str(start) + '.png'
					print pngfile
					os.remove(pngfile)
					start += 1
					print start
			
			elif self.maxentry > 9:
				print 'more then 9'
				while start < (self.maxentry + 1):
					print 'go'
					if start < 10:
						print 'under 10'
						pngfile = '/tmp/HetWeer/0' + str(start) + '.png'
						print pngfile
						os.remove(pngfile)
						start += 1
						print start
					else:
						print "over 9"
						pngfile = '/tmp/HetWeer/' + str(start) + '.png'
						print pngfile
						os.remove(pngfile)
						start += 1
						print start
			
			print "unlink done"
		except:
			print "ah damn"
			pass
				
		self.close()
		
		
		
#-- main:

def main(session, **kwargs):
	session.open(Weermenu)

def Plugins(**kwargs):
	return PluginDescriptor(name=_("Het Weer"), description=_("Weer Informatie"), where=[PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU], fnc=main)
