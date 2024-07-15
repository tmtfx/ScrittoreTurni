#!/boot/system/bin/python3
from Be import BApplication, BWindow, BView, BMenu,BMenuBar, BMenuItem, BSeparatorItem, BMessage, window_type, B_NOT_RESIZABLE, B_CLOSE_ON_ESCAPE, B_QUIT_ON_WINDOW_CLOSE
from Be import BButton, BTextView, BTextControl, BAlert, BListItem,BPopUpMenu,BMenuField, BListView, BScrollView,BOutlineListView, BRect, BBox, BFont, InterfaceDefs, BPath, BDirectory, BEntry
from Be import BStringItem, BFile, BStringView,BCheckBox#BNode, TypeConstants, 
from Be import BTranslationUtils, BBitmap
from Be.Button import BBehavior
#from Be.NodeMonitor import *
#from Be.Node import node_ref
from Be.GraphicsDefs import *
from Be.View import *
from Be.Menu import menu_info,get_menu_info
from Be.FindDirectory import *
from Be.View import B_FOLLOW_NONE,set_font_mask,B_WILL_DRAW,B_NAVIGABLE,B_FULL_UPDATE_ON_RESIZE,B_FRAME_EVENTS,B_PULSE_NEEDED
from Be.Alert import alert_type
from Be.InterfaceDefs import border_style,orientation
from Be.ListView import list_view_type
from Be.AppDefs import *
from Be.Font import be_plain_font, be_bold_font
from Be import AppDefs
from Be.FilePanel import *
# from Be.fs_attr import attr_info
from Be.Application import *
from Be.Font import font_height
from Be.Menu import menu_layout
from Be import Entry
from Be.Entry import entry_ref, get_ref_for_path

import os,sys,datetime,time
glock=0

cod_stazioni=[("UD","Udine"),("UDFS","Udine fascio sacca"),("BASL","Basiliano"),("CDRP","Codroipo"),("CSRS","Casarsa"),("CUS","Cusano"),("PN","Pordenone"),("FONT","Fontanafredda"),("SAC","Sacile"),("ORSG","Orsago"),("PIAN","Pianzano"),("CON","Conegliano"),("SUS","Susegana"),("SPR","Spresiano"),("LANC","Lancenigo"),("TVCL","Treviso centrale"),("TVDL","Treviso deposito"),("STRV","San Trovaso"),("PREG","Preganziol"),("MOGL","Mogliano Veneto"),("MSOS","Mestre ospedale"),("MSCL","Mestre centrale"),("MSDL","Mestre deposito"),("VEPM","Venezia porto marghera"),("VESL","Venezia Santa Lucia"),("BUT","Buttrio"),("MANZ","Manzano"),("SGAN","San Giovanni al Natisone"),("CORM","Cormons"),("GOCL","Gorizia centrale"),("SAGR","Sagrado"),("RON","Ronchi nord"),("MONF","Monfalcone"),("SIST","Sistiana"),("BVDA","Bivio d'Aurisina"),("MIRM","Miramare"),("TSCL","Trieste centrale"),("TSDL","Trieste deposito"),("TSA","Trieste airport"),("CRVG","Cervignano"),("SGIO","San Giorgio di Nogaro"),("LAT","Latisana"),("PGRU","Portogruaro"),("SSTI","San Stino di Livenza"),("SDON","San Donà di Piave"),("QUDA","Quarto d'Altino"),("SGDC","San Giovanni di Casarsa"),("SVIT","San Vito al Tagliamento"),("CORD","Cordovado Sesto"),("TEGL","Teglio veneto"),("SACL","Sacile San Liberale"),("BUDJ","Budoia"),("AVNO","Aviano"),("MONT","Montereale valcellina"),("MAN","Maniago"),("TRIC","Tricesimo"),("TARC","Tarcento"),("ARTG","Artegna"),("GEM","Gemona"),("VENZ","Venzone"),("CRNI","Carnia"),("PONT","Pontebba"),("UGOV","Ugovizza"),("TARB","Tarvisio boscoverde"),("PALM","Palmanova"),("RISN","Risano")]
legenda = sorted(cod_stazioni, key=lambda x: x[1])
tipocond=[("Agente solo",1),("Agente Unico",2),("Doppio Agente/1",3),("Doppio Agente/2",4)]
class PButton(BButton):
	def __init__(self,frame,name,label,msg,resizingMode,immagine):
		self.immagine = immagine
		self.frame = frame
		BButton.__init__(self,frame,name,label,msg,resizingMode)

	def Draw(self,rect):
		BButton.Draw(self, rect)
		inset = BRect(4, 4, self.frame.Width()-4, self.frame.Height()-4)#(2, 2, self.frame.Width()-2, self.frame.Height()-2)
		self.DrawBitmap(self.immagine,inset)
class StazionePartenza(BMenuItem):
	def __init__(self,cubie):
		self.name=cubie[1]
		self.code=cubie[0]
		msg=BMessage(605)
		msg.AddString("code",self.code)
		msg.AddString("name",self.name)
		BMenuItem.__init__(self,self.name,msg,self.name[0],0)
class StazioneArrivo(BMenuItem):
	def __init__(self,cubie):
		self.name=cubie[1]
		self.code=cubie[0]
		msg=BMessage(606)
		msg.AddString("code",self.code)
		msg.AddString("name",self.name)
		BMenuItem.__init__(self,self.name,msg,self.name[0],0)
class Condotta(BMenuItem):
	def __init__(self,cubie):
		self.code = cubie[1]
		self.name = cubie[0]
		msg = BMessage(808)
		msg.AddInt8("code",self.code)
		msg.AddString("name",self.name)
		BMenuItem.__init__(self,self.name,msg,self.name[0],0)
class Materiale(BMenuItem):
	def __init__(self,data):
		self.name=data[0]
		self.accp=data[1]
		self.acca=data[2]
		self.prkp=data[3]
		self.prka=data[4]
		self.cb=data[5]
		msg=BMessage(610)
		msg.AddInt8("accp",data[1])
		msg.AddInt8("acca",data[2])
		msg.AddInt8("prkp",data[3])
		msg.AddInt8("prka",data[4])
		msg.AddInt8("cb",data[5])
		msg.AddString("name",self.name)
		BMenuItem.__init__(self,self.name,msg,self.name[0],0)
materiali=[("Rock",30,15,25,10,7),("563/564",30,15,25,10,7),("Ale/Aln 501/502",25,10,20,10,6),("Blues",25,10,20,10,7),("464/MD/Viv",40,20,25,10,10),("464+464/MD",55,30,25,10,10)]
class TipoAcc(BMenuItem):
	def __init__(self,cubie):
		self.name=cubie[0]
		self.code=cubie[1]
		msg=BMessage(607)
		msg.AddInt8("code",self.code)
		msg.AddString("name",self.name)
		BMenuItem.__init__(self,self.name,msg,self.name[0],0)
class TipoAccp(BMenuItem):
	def __init__(self,cubie):
		self.name=cubie[0]
		self.code=cubie[1]
		msg=BMessage(707)
		msg.AddInt8("code",self.code)
		msg.AddString("name",self.name)
		BMenuItem.__init__(self,self.name,msg,self.name[0],0)
class TipoAcca(BMenuItem):
	def __init__(self,cubie):
		self.name=cubie[0]
		self.code=cubie[1]
		msg=BMessage(708)
		msg.AddInt8("code",self.code)
		msg.AddString("name",self.name)
		BMenuItem.__init__(self,self.name,msg,self.name[0],0)
class ParteItem(BMenuItem):
	def __init__(self,valore):
		self.name=valore
		msg=BMessage(608)
		msg.AddInt8("code",self.name)
		msg.AddString("name",str(self.name))
		BMenuItem.__init__(self,str(self.name),msg,str(self.name)[0],0)
class Ia(BMenuItem):
	def __init__(self,valore):
		self.name=valore
		msg=BMessage(666)
		msg.AddInt8("code",self.name)
		msg.AddString("name",str(self.name))
		BMenuItem.__init__(self,str(self.name),msg,str(self.name)[0],0)
class It(BMenuItem):
	def __init__(self,valore):
		self.name=valore
		msg=BMessage(667)
		msg.AddInt8("code",self.name)
		msg.AddString("name",str(self.name))
		BMenuItem.__init__(self,str(self.name),msg,str(self.name)[0],0)
class Ft(BMenuItem):
	def __init__(self,valore):
		self.name=valore
		msg=BMessage(668)
		msg.AddInt8("code",self.name)
		msg.AddString("name",str(self.name))
		BMenuItem.__init__(self,str(self.name),msg,str(self.name)[0],0)
class Fa(BMenuItem):
	def __init__(self,valore):
		self.name=valore
		msg=BMessage(669)
		msg.AddInt8("code",self.name)
		msg.AddString("name",str(self.name))
		BMenuItem.__init__(self,str(self.name),msg,str(self.name)[0],0)
class PartefItem(BMenuItem):
	def __init__(self,valore):
		self.name=valore
		msg=BMessage(908)
		msg.AddInt8("code",self.name)
		msg.AddString("name",str(self.name))
		BMenuItem.__init__(self,str(self.name),msg,str(self.name)[0],0)
class TotaleItem(BMenuItem):
	def __init__(self,valore):
		self.name=valore
		msg=BMessage(609)
		msg.AddInt8("code",self.name)
		msg.AddString("name",str(self.name))
		BMenuItem.__init__(self,str(self.name),msg,str(self.name)[0],0)
class VettWindow(BWindow):
	alertWind=[]
	cp=None
	ca=None
	np=None
	na=None
	parte=1
	partef=1
	totale=1
	def __init__(self):
		BWindow.__init__(self, BRect(200,170,800,278), "Vettura", window_type.B_FLOATING_WINDOW,  B_NOT_RESIZABLE|B_CLOSE_ON_ESCAPE)
		self.bckgnd = BView(self.Bounds(), "bckgnd_View", 8, 20000000)
		rect=self.bckgnd.Bounds()
		self.AddChild(self.bckgnd,None)
		self.bckgnd.SetResizingMode(B_FOLLOW_ALL_SIDES)
		a=BFont()
		self.name=BTextControl(BRect(8,8,rect.Width()*2/3-8,12+a.Size()),"nvett-nome", "N.vettura/VOC:","VOC",BMessage(1900))
		
		self.menupt=BMenu("1")
		self.menupf=BMenu("1")
		self.menutt=BMenu("1")
		self.menupt.SetLabelFromMarked(True)
		self.menupf.SetLabelFromMarked(True)
		self.menutt.SetLabelFromMarked(True)
		self.menupt.AddItem(ParteItem(1))
		self.menupt.AddItem(ParteItem(2))
		self.menupf.AddItem(PartefItem(1))
		self.menupf.AddItem(PartefItem(2))
		self.menutt.AddItem(TotaleItem(1))
		self.menutt.AddItem(TotaleItem(2))
		#self.mfparte = BMenuField(BRect(rect.Width()*2/3+8, 8, rect.Width()*2/3+78, 12+a.Size()), 'parte', 'Parte', self.menupt,B_FOLLOW_TOP)
		self.mfparte = BMenuField(BRect(8, rect.Height()/2+a.Size()+4, 78, rect.Height()-8), 'parte_inizio', 'Inizio', self.menupt,B_FOLLOW_TOP)
		self.mfparte.SetDivider(a.StringWidth("Inizio "))
		#self.mftotale = BMenuField(BRect(rect.Width()*2/3+86, 8, rect.Width()*2/3+136, 12+a.Size()), 'totale', 'di', self.menutt,B_FOLLOW_TOP)
		self.mftotale = BMenuField(BRect(86, rect.Height()/2+a.Size()+4, 136, rect.Height()-8), 'totale', 'di', self.menutt,B_FOLLOW_TOP)
		self.mftotale.SetDivider(a.StringWidth("di "))
		self.mfpartef = BMenuField(BRect(146, rect.Height()/2+a.Size()+4, 208, rect.Height()-8), 'parte_fine', 'Fine', self.menupf,B_FOLLOW_TOP)
		self.mfpartef.SetDivider(a.StringWidth("Fine "))
		#self.mftotale_mirror = BMenuField(BRect(218, rect.Height()/2+a.Size()+4, 268, rect.Height()-8), 'totale', 'di', self.menutt,B_FOLLOW_TOP)
		#self.mftotale_mirror.SetDivider(a.StringWidth("di "))
		self.bckgnd.AddChild(self.mfparte,None)
		self.bckgnd.AddChild(self.mftotale,None)
		self.bckgnd.AddChild(self.mfpartef,None)
		#self.bckgnd.AddChild(self.mftotale_mirror,None)
		
		
		self.oi=BTextControl(BRect(8,28+a.Size(),128,32+2*a.Size()),"ora_inizio", "Partenza ore:",str(5),BMessage(1901))
		#print(a.StringWidth("Arrivo ore:"))
		self.oi.SetDivider(90.0)
		self.mi=BTextControl(BRect(136,28+a.Size(),192,32+2*a.Size()),"min_inizio", "min:",str(58),BMessage(1902))
		self.of=BTextControl(BRect(rect.Width()/2,28+a.Size(),rect.Width()/2+105,32+2*a.Size()),"ora_fine", "Arrivo ore:",str(6),BMessage(1903))
		self.of.SetDivider(75.0)
		self.mf=BTextControl(BRect(rect.Width()/2+113,28+a.Size(),rect.Width()/2+169,32+2*a.Size()),"min_fine", "min:",str(38),BMessage(1904))
		self.bckgnd.AddChild(self.name,None)
		self.bckgnd.AddChild(self.oi,None)
		self.bckgnd.AddChild(self.mi,None)
		self.bckgnd.AddChild(self.of,None)
		self.bckgnd.AddChild(self.mf,None)
		self.addBtn=BButton(BRect(rect.Width()/2, rect.Height()/2+a.Size()+4,rect.Width()-8,rect.Height()-8),'AddBtn','Aggiungi',BMessage(1002),B_FOLLOW_BOTTOM|B_FOLLOW_RIGHT)
		self.addBtn.SetEnabled(False)
		
		perc=BPath()
		#find_directory(directory_which.B_SYSTEM_DATA_DIRECTORY,perc,False,None)
		ent=BEntry(os.path.dirname(os.path.realpath(__file__))+"/orloi2.jpg")#"/boot/home/Apps/ScrittoreTurni/orloi.jpg")
		if ent.Exists():
			ent.GetPath(perc)
			img1=BTranslationUtils.GetBitmap(perc.Path(),None)
			self.getTimeBtn=PButton(BRect(rect.Width()/2-40,rect.Height()/2+a.Size()+4,rect.Width()/2-8,rect.Height()-8),'GetTimeButton','',BMessage(1004),B_FOLLOW_BOTTOM|B_FOLLOW_RIGHT,img1)
		else:
			lab="🕒"
			self.getTimeBtn=BButton(BRect(rect.Width()/2-40,rect.Height()/2+a.Size()+4,rect.Width()/2-8,rect.Height()-8),'GetTimeButton',lab,BMessage(1004),B_FOLLOW_BOTTOM|B_FOLLOW_RIGHT)
		self.bckgnd.AddChild(self.getTimeBtn,None)
		
		self.bckgnd.AddChild(self.addBtn,None)
		self.menup=BMenu("Stazione")
		self.menua=BMenu("Stazione")
		self.menup.SetLabelFromMarked(True)
		self.menua.SetLabelFromMarked(True)
		for z in legenda:
			self.menup.AddItem(StazionePartenza(z))
			self.menua.AddItem(StazioneArrivo(z))
		self.pbar = BMenuField(BRect(200, 28+a.Size(), rect.Width()/2-8, 32+2*a.Size()), 'pop1', '', self.menup,B_FOLLOW_TOP)
		self.pbar.SetDivider(0)
		self.bckgnd.AddChild(self.pbar,None)
		self.abar = BMenuField(BRect(rect.Width()/2+177, 28+a.Size(), rect.Width()-8, 32+2*a.Size()), 'pop2', '',self.menua,B_FOLLOW_TOP)
		self.abar.SetDivider(0)
		self.bckgnd.AddChild(self.abar,None)
	def checkvalues(self):
		ret=True
		for testo in {self.oi.Text(),self.mi.Text(),self.of.Text(),self.mf.Text()}:
			try:
				int(testo)
			except:
				ret=False
		if ret:
			for v in {self.ca,self.cp,self.na,self.np}:
				if v == None:
					ret = False
		#if ret:
		#	if self.parte>self.totale:
		#		ret=False
		return ret
	def MessageReceived(self, msg):
		if msg.what==605:
			#stabilisco stazione partenza
			self.cp = msg.FindString("code")
			self.np = msg.FindString("name")
			#if self.checkvalues():
			#	self.addBtn.SetEnabled(True)
			self.addBtn.SetEnabled(self.checkvalues())
			#print(self.cp,self.np)
		elif msg.what==606:
			#stabilisco stazione arrivo
			self.ca = msg.FindString("code")
			self.na = msg.FindString("name")
			#if self.checkvalues():
			#	self.addBtn.SetEnabled(True)
			self.addBtn.SetEnabled(self.checkvalues())
			#print(self.ca,self.na)
		elif msg.what == 608:
			#parte turno inizio giorno
			self.parte = msg.FindInt8("code")
			if self.parte> self.totale:
				self.menutt.FindItem("2").SetMarked(True)
				self.totale=2
				self.menupf.FindItem("2").SetMarked(True)
				self.partef=2
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 609:
			#totale estensione turno in giorni
			self.totale = msg.FindInt8("code")
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 908:
			#parte turno fine giorno
			self.partef = msg.FindInt8("code")
			if self.partef> self.totale:
				self.menutt.FindItem("2").SetMarked(True)#.Invoke()
				self.totale=2
				#self.menutt.ItemAt(1).SetMarked(True)
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what==1002:
			dop=datetime.timedelta(hours=int(self.oi.Text()),minutes=int(self.mi.Text()))
			doa=datetime.timedelta(hours=int(self.of.Text()),minutes=int(self.mf.Text()))
			if self.cp == self.ca:
				ask=BAlert('cle', "Spostamento da/per lo stesso luogo, aggiungere?", 'No', 'Sì',None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_WARNING_ALERT)
				self.alertWind.append(ask)
				ret=ask.Go()
				if ret:
					pass
				else:
					return
			if self.partef>self.parte:
				if (doa+datetime.timedelta(hours=24))-dop>datetime.timedelta(minutes=0):
					mex=BMessage(1002)
					mex.AddInt8("oi",int(self.oi.Text()))
					mex.AddInt8("mi",int(self.mi.Text()))
					mex.AddInt8("of",int(self.of.Text()))
					mex.AddInt8("mf",int(self.mf.Text()))
					mex.AddInt8("parte",self.parte)
					mex.AddInt8("partef",self.partef)
					mex.AddInt8("totale",self.totale)
					mex.AddString("csp",self.cp)
					mex.AddString("csa",self.ca)
					mex.AddString("nsp",self.np)
					mex.AddString("nsa",self.na)
					mex.AddString("name",self.name.Text())
					be_app.WindowAt(0).PostMessage(mex)
				else:
					ask=BAlert('cle', "L'orario di arrivo deve essere posteriore all'orario di partenza", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
					self.alertWind.append(ask)
					ask.Go()
			else:
				if doa-dop>datetime.timedelta(minutes=0):
					mex=BMessage(1002)
					mex.AddInt8("oi",int(self.oi.Text()))
					mex.AddInt8("mi",int(self.mi.Text()))
					mex.AddInt8("of",int(self.of.Text()))
					mex.AddInt8("mf",int(self.mf.Text()))
					mex.AddInt8("parte",self.parte)
					mex.AddInt8("partef",self.partef)
					mex.AddInt8("totale",self.totale)
					mex.AddString("csp",self.cp)
					mex.AddString("csa",self.ca)
					mex.AddString("nsp",self.np)
					mex.AddString("nsa",self.na)
					mex.AddString("name",self.name.Text())
					be_app.WindowAt(0).PostMessage(mex)
				else:
					ask=BAlert('cle', "L'orario di arrivo deve essere posteriore all'orario di partenza", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
					self.alertWind.append(ask)
					ask.Go()
		elif msg.what == 1004:
			#Recupera orario fine elemento precedente
			lt=be_app.WindowAt(0).listaturni.lv
			if lt.CountItems()>1:
				doit=False
				if lt.CurrentSelection()>-1:
					selitm=lt.ItemAt(lt.CurrentSelection())
					if type(selitm) != BStringItem:
						orario=selitm.fine
						partef=selitm.partef
						sta=selitm.sta
						doit=True
				else:
					lastitm=lt.ItemAt(lt.CountItems()-1)
					if type(lastitm) != BStringItem:
						orario=lastitm.fine
						partef=lastitm.partef
						sta=lastitm.sta
						doit=True
				if doit:
					self.menup.FindItem(sta[1]).SetMarked(True)
					self.cp=sta[0]
					self.np=sta[1]
					if partef>1:
						self.menupt.FindItem("2").SetMarked(True)
						self.parte=2
						self.menutt.FindItem("2").SetMarked(True)
						self.totale=2
						self.menupf.FindItem("2").SetMarked(True)
						self.partef=2
					self.mi.SetText(str((orario.seconds % 3600) // 60))
					self.oi.SetText(str(orario.days * 24 + orario.seconds // 3600))
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 1901:
			try:
				numb=int(self.oi.Text())
				if 0<=numb<24:
					self.oi.MarkAsInvalid(False)
					if self.checkvalues():
						self.addBtn.SetEnabled(True)
				else:
					self.oi.MarkAsInvalid(True)
					self.addBtn.SetEnabled(False)
			except:
				self.oi.MarkAsInvalid(True)
				self.addBtn.SetEnabled(False)
		elif msg.what == 1902:
			try:
				numb=int(self.mi.Text())
				if 0<=numb<60:
					self.mi.MarkAsInvalid(False)
					if self.checkvalues():
						self.addBtn.SetEnabled(True)
				else:
					self.mi.MarkAsInvalid(True)
					self.addBtn.SetEnabled(False)
			except:
				self.mi.MarkAsInvalid(True)
				self.addBtn.SetEnabled(False)
		elif msg.what == 1903:
			try:
				numb=int(self.of.Text())
				if 0<=numb<24:
					self.of.MarkAsInvalid(False)
					if self.checkvalues():
						self.addBtn.SetEnabled(True)
				else:
					self.of.MarkAsInvalid(True)
					self.addBtn.SetEnabled(False)
			except:
				self.of.MarkAsInvalid(True)
				self.addBtn.SetEnabled(False)
		elif msg.what == 1904:
			try:
				numb=int(self.mf.Text())
				if 0<=numb<60:
					self.mf.MarkAsInvalid(False)
					if self.checkvalues():
						self.addBtn.SetEnabled(True)
				else:
					self.mf.MarkAsInvalid(True)
					self.addBtn.SetEnabled(False)
			except:
				self.mf.MarkAsInvalid(True)
				self.addBtn.SetEnabled(False)
		return BWindow.MessageReceived(self,msg)
	def QuitRequested(self):
		self.Hide()
class AccWindow(BWindow):
	alertWind=[]
	cp=None
	ca=None
	np=None
	na=None
	ta=None
	codacc=0
	mat=None
	parte=1
	partef=1
	totale=1
	tipoacc=[("Accessori in partenza",1),("Accessori in arrivo",2),("Cambio volante in partenza",3),("Cambio volante in arrivo",4),("Parking in partenza",5),("Parking in arrivo",6),("Cambio banco",7),("Tempi medi",8),("Riserva",9)]
	def __init__(self):
		BWindow.__init__(self, BRect(250,190,850,298), "Accessori", window_type.B_FLOATING_WINDOW,  B_NOT_RESIZABLE|B_CLOSE_ON_ESCAPE)
		self.bckgnd = BView(self.Bounds(), "bckgnd_View", 8, 20000000)
		self.AddChild(self.bckgnd,None)
		self.bckgnd.SetResizingMode(B_FOLLOW_ALL_SIDES)
		a=BFont()
		rect=self.bckgnd.Bounds()
		
		self.menuacc=BMenu("Tipo accessori")
		self.menuacc.SetLabelFromMarked(True)
		for y in self.tipoacc:
			self.menuacc.AddItem(TipoAcc(y))
		self.menuf = BMenuField(BRect(8,8,158,12+a.Size()), 'pop0', '', self.menuacc,B_FOLLOW_TOP)
		self.menuf.SetDivider(0) #<-This works
		self.bckgnd.AddChild(self.menuf,None)
		
		self.treno=BTextControl(BRect(200,8,rect.Width()*2/3-8,12+a.Size()),"treno", "Treno:","",BMessage(1900))
		self.treno.SetDivider(a.StringWidth("Treno:   "))
		self.bckgnd.AddChild(self.treno,None)
		
		self.menupt=BMenu("1")
		self.menupt.SetLabelFromMarked(True)
		self.menupt.AddItem(ParteItem(1))
		self.menupt.AddItem(ParteItem(2))
		self.mfparte = BMenuField(BRect(rect.Width()*2/3, 8, rect.Width()*2/3+70, 12+a.Size()), 'parte', 'Parte', self.menupt,B_FOLLOW_TOP) #rect.Width()*2/3+78 <-- it's ignored if I write 0 the item is fully visible
		self.mfparte.SetDivider(a.StringWidth("Parte ")) #<- This works
		self.bckgnd.AddChild(self.mfparte,None)
		
		self.menutt=BMenu("1")
		self.menutt.SetLabelFromMarked(True)
		self.menutt.AddItem(TotaleItem(1))
		self.menutt.AddItem(TotaleItem(2))
		self.mftotale = BMenuField(BRect(rect.Width()*2/3+74, 8, rect.Width()*2/3+128, 12+a.Size()), 'totale', 'di', self.menutt,B_FOLLOW_TOP)
		self.mftotale.SetDivider(a.StringWidth("di  "))
		self.bckgnd.AddChild(self.mftotale,None)
		
		self.menupf=BMenu("1")
		self.menupf.SetLabelFromMarked(True)
		self.menupf.AddItem(PartefItem(1))
		self.menupf.AddItem(PartefItem(2))
		self.mfpartef = BMenuField(BRect(rect.Width()*2/3+130, 8, rect.Width()-8, 12+a.Size()), 'parte_fine', 'Fine', self.menupf,B_FOLLOW_TOP)
		self.mfpartef.SetDivider(a.StringWidth("Fine "))
		self.bckgnd.AddChild(self.mfpartef,None)
		
		self.oi = BTextControl(BRect(8,28+a.Size(),128,32+2*a.Size()),"ora_inizio", "Inizio ore:",str(5),BMessage(1901))
		self.oi.SetDivider(90.0)
		self.mi = BTextControl(BRect(136,28+a.Size(),192,32+2*a.Size()),"min_inizio", "min:",str(58),BMessage(1902))
		self.of = BTextControl(BRect(rect.Width()/2,28+a.Size(),rect.Width()/2+105,32+2*a.Size()),"ora_fine", "Fine ore:",str(6),BMessage(1903))
		self.of.SetDivider(75.0)
		self.mf = BTextControl(BRect(rect.Width()/2+113,28+a.Size(),rect.Width()/2+169,32+2*a.Size()),"min_fine", "min:",str(38),BMessage(1904))
		self.bckgnd.AddChild(self.oi,None)
		self.bckgnd.AddChild(self.mi,None)
		self.bckgnd.AddChild(self.of,None)
		self.bckgnd.AddChild(self.mf,None)
		
		self.menumat = BMenu("Materiale rotabile")
		self.menumat.SetLabelFromMarked(True)
		for m in materiali:
			self.menumat.AddItem(Materiale(m))
		self.mfmat = BMenuField(BRect(8, rect.Height()-38, rect.Width()/2-8, rect.Height()-8), 'materiale', 'Materiale:', self.menumat,B_FOLLOW_TOP)#48+2*a.Size(),44+3*a.Size()
		#self.mfmat.SetDivider(a.StringWidth("Materiale:  "))
		self.bckgnd.AddChild(self.mfmat,None)
		
		self.addBtn=BButton(BRect(rect.Width()/2, rect.Height()-38,rect.Width()-8,rect.Height()-8),'AddBtn','Aggiungi',BMessage(1003),B_FOLLOW_BOTTOM|B_FOLLOW_RIGHT)
		self.addBtn.SetEnabled(False)
		
		perc=BPath()
		#find_directory(directory_which.B_SYSTEM_DATA_DIRECTORY,perc,False,None)
		ent=BEntry(os.path.dirname(os.path.realpath(__file__))+"/orloi2.jpg")#"/boot/home/Apps/ScrittoreTurni/orloi.jpg")
		if ent.Exists():
			ent.GetPath(perc)
			img1=BTranslationUtils.GetBitmap(perc.Path(),None)
			self.getTimeBtn=PButton(BRect(rect.Width()-40,28+a.Size(),rect.Width()-8,46+2*a.Size()),'GetTimeButton','',BMessage(1004),B_FOLLOW_BOTTOM|B_FOLLOW_RIGHT,img1)
		else:
			lab="🕒"
			self.getTimeBtn=BButton(BRect(rect.Width()-40,28+a.Size(),rect.Width()-8,32+2*a.Size()),'GetTimeButton',lab,BMessage(1004),B_FOLLOW_BOTTOM|B_FOLLOW_RIGHT)
		self.bckgnd.AddChild(self.getTimeBtn,None)
		self.bckgnd.AddChild(self.addBtn,None)
		self.menup=BMenu("Stazione")
		self.menua=BMenu("Stazione")
		self.menup.SetLabelFromMarked(True)
		self.menua.SetLabelFromMarked(True)
		for z in legenda:
			self.menup.AddItem(StazionePartenza(z))
			self.menua.AddItem(StazioneArrivo(z))
		self.pbar = BMenuField(BRect(200, 28+a.Size(), rect.Width()/2-8, 32+2*a.Size()), 'pop1', '', self.menup,B_FOLLOW_TOP)
		self.pbar.SetDivider(0)# <--------     This works!!!!!!!!!
		self.bckgnd.AddChild(self.pbar,None)
		self.abar = BMenuField(BRect(rect.Width()/2+177, 28+a.Size(), rect.Width()-44, 32+2*a.Size()), 'pop2', '',self.menua,B_FOLLOW_TOP)
		self.abar.SetDivider(0)# <--------     This works!!!!!!!!!
		self.bckgnd.AddChild(self.abar,None)
	def checkvalues(self):
		ret=True
		self.addBtn.SetEnabled(True)
		for testo in {self.oi.Text(),self.mi.Text(),self.of.Text(),self.mf.Text()}:
			try:
				int(testo)
			except:
				ret=False
		if ret:
			if self.cp==None or self.ca==None:
				ret=False
			elif self.codacc==0:
				ret=False
			elif self.codacc !=8:
				if self.cp != self.ca:
					ret=False
			elif self.parte>self.totale:
				ret=False
			#TODO	elif int(self.oi.Text())>23:
			#			ret=False
			#		elif int(self.mi.Text())>59:
			#			ret=False
			# ecc.
		return ret
	def MessageReceived(self, msg):
		if msg.what==605:
			#stabilisco stazione partenza
			self.cp = msg.FindString("code")
			self.np = msg.FindString("name")
			#if self.checkvalues():
			#	self.addBtn.SetEnabled(True)
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what==606:
			#stabilisco stazione arrivo
			self.ca = msg.FindString("code")
			self.na = msg.FindString("name")
			#if self.checkvalues():
			#	self.addBtn.SetEnabled(True)
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what==607:
			#stabilisto tipo accessori
			self.codacc = msg.FindInt8("code")
			self.ta = msg.FindString("name")
			if self.mat!=None:
				datoi=datetime.timedelta(hours=int(self.oi.Text()),minutes=int(self.mi.Text()))
				if self.codacc == 1:
					#usa accp
					delt=datetime.timedelta(minutes=self.accp)
				elif self.codacc == 2:
					#usa acca
					delt=datetime.timedelta(minutes=self.acca)
				elif self.codacc == 3:
					#cv in partenza
					delt=datetime.timedelta(minutes=15)
				elif self.codacc == 4:
					#cv in arrivo
					delt=datetime.timedelta(minutes=10)
				elif self.codacc == 5:
					#usa prkp
					delt=datetime.timedelta(minutes=self.prkp)
				elif self.codacc == 6:
					#usa prka
					delt=datetime.timedelta(minutes=self.prka)
				elif self.codacc == 7:
					#cambio banco
					delt=datetime.timedelta(minutes=self.cb)
				elif self.codacc == 8:
					#tempi medi di manovra
					delt=datetime.timedelta(minutes=10)
				elif self.codacc == 9:
					#riserva
					delt=datetime.timedelta(minutes=0)
				dtout=datoi+delt
				self.mf.SetText(str((dtout.seconds % 3600) // 60))
				self.of.SetText(str(dtout.days * 24 + dtout.seconds // 3600))
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 608:
			self.parte = msg.FindInt8("code")
			if self.parte> self.totale:
				self.menutt.FindItem("2").SetMarked(True)
				self.totale=2
				self.menupf.FindItem("2").SetMarked(True)
				self.partef=2
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 609:
			self.totale = msg.FindInt8("code")
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 908:
			self.partef = msg.FindInt8("code")
			if self.partef> self.totale:
				self.menutt.FindItem("2").SetMarked(True)#.Invoke()
				self.totale=2
				#self.menutt.ItemAt(1).SetMarked(True)
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 610:
			#stabilisco materiale
			self.accp=msg.FindInt8("accp")
			self.acca=msg.FindInt8("acca")
			self.prkp=msg.FindInt8("prkp")
			self.prka=msg.FindInt8("prka")
			self.cb=msg.FindInt8("cb")
			self.mat=msg.FindString("name")
			if self.codacc!=0:
				datoi=datetime.timedelta(hours=int(self.oi.Text()),minutes=int(self.mi.Text()))
				if self.codacc == 1:
					#usa accp
					delt=datetime.timedelta(minutes=self.accp)
				elif self.codacc == 2:
					#usa acca
					delt=datetime.timedelta(minutes=self.acca)
				elif self.codacc == 3:
					#cv in partenza
					delt=datetime.timedelta(minutes=15)
				elif self.codacc == 4:
					#cv in arrivo
					delt=datetime.timedelta(minutes=10)
				elif self.codacc == 5:
					#usa prkp
					delt=datetime.timedelta(minutes=self.prkp)
				elif self.codacc == 6:
					#usa prka
					delt=datetime.timedelta(minutes=self.prka)
				elif self.codacc == 7:
					#cambio banco
					delt=datetime.timedelta(minutes=1)
				elif self.codacc == 8:
					#tempi medi di manovra
					delt=datetime.timedelta(minutes=10)
				elif self.codacc == 9:
					#riserva
					delt=datetime.timedelta(minutes=0)
				dtout=datoi+delt
				self.mf.SetText(str((dtout.seconds % 3600) // 60))
				self.of.SetText(str(dtout.days * 24 + dtout.seconds // 3600))
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 1003:
			dop=datetime.timedelta(hours=int(self.oi.Text()),minutes=int(self.mi.Text()))
			doa=datetime.timedelta(hours=int(self.of.Text()),minutes=int(self.mf.Text()))
			if self.partef>self.parte:
				doa+=datetime.timedelta(hours=24)
			if self.codacc==8:
				if self.cp == self.ca:
					ask=BAlert('cle', "Spostamento in manovra da/per lo stesso luogo, aggiungere?", 'No', 'Sì',None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_WARNING_ALERT)
					self.alertWind.append(ask)
					ret=ask.Go()
					if not(ret):
						return
			if doa-dop>datetime.timedelta(minutes=0):
				mex=BMessage(1003)
				mex.AddInt8("oi",int(self.oi.Text())) #ora inizio
				mex.AddInt8("mi",int(self.mi.Text())) #minuto inizio
				mex.AddInt8("of",int(self.of.Text())) #ora fine
				mex.AddInt8("mf",int(self.mf.Text())) #minuto fine
				mex.AddString("csp",self.cp) #codice stazione partenza
				mex.AddString("csa",self.ca) #codice stazione arrivo
				mex.AddString("nsp",self.np) #nome stazione partenza
				mex.AddString("nsa",self.na) #nome stazione arrivo
				mex.AddString("nta",self.ta) #nome tipo accessori
				mex.AddInt8("codacc",self.codacc) #codice accessori
				if self.codacc == 9:
					oldmat=self.mat
					self.mat = ""
					mex.AddString("materiale",self.mat)
					self.mat = oldmat
				else:
					mex.AddString("materiale",self.mat)
				mex.AddInt8("parte",self.parte) #parte del turno inizio
				mex.AddInt8("partef",self.partef) #parte del turno fine
				mex.AddInt8("totale",self.totale) #totale del turno
				mex.AddString("name",self.treno.Text()) #nome accessori/numero treno
				be_app.WindowAt(0).PostMessage(mex)
			else:
				ask=BAlert('cle', "L'orario di fine accessori deve essere posteriore all'orario di inizio accessori", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
				self.alertWind.append(ask)
				ask.Go()
		elif msg.what == 1004:
			#Recupera orario fine elemento precedente
			lt=be_app.WindowAt(0).listaturni.lv
			if lt.CountItems()>1:
				doit=False
				if lt.CurrentSelection()>-1:
					selitm=lt.ItemAt(lt.CurrentSelection())
					if type(selitm) != BStringItem:
						orario=selitm.fine
						partef=selim.partef
						sta=selitm.sta
						doit=True
				else:
					lastitm=lt.ItemAt(lt.CountItems()-1)
					if type(lastitm) != BStringItem:
						orario=lastitm.fine
						partef=lastitm.partef
						sta=lastitm.sta
						doit=True
				if doit:
					self.menup.FindItem(sta[1]).SetMarked(True)
					self.cp=sta[0]
					self.np=sta[1]
					if partef>1:
						self.menupt.FindItem("2").SetMarked(True)
						self.parte=2
						self.menutt.FindItem("2").SetMarked(True)
						self.totale=2
						self.menupf.FindItem("2").SetMarked(True)
						self.partef=2
					self.mi.SetText(str((orario.seconds % 3600) // 60))
					self.oi.SetText(str(orario.days * 24 + orario.seconds // 3600))
			self.addBtn.SetEnabled(self.checkvalues())
		return BWindow.MessageReceived(self,msg)
	def QuitRequested(self):
		self.Hide()
class TrenoWindow(BWindow):
	alertWind=[]
	cp=None
	ca=None
	np=None
	na=None
	tap=None
	codaccp=0
	taa=None
	codacca=0
	mat=None
	ccond=0
	ncond=None
	ina=1
	#int=1
	#fit=1
	fia=1
	#pia=1
	#pt=1
	#pfa=1
	parte=1
	partef=1
	totale=1
	tipoaccp=[("Accessori in partenza",1),("Cambio volante in partenza",3),("Parking in partenza",5)]
	tipoacca=[("Accessori in arrivo",2),("Cambio volante in arrivo",4),("Parking in arrivo",6),("Cambio banco",7)]
	#tipocond=[("Agente solo",1),("Agente Unico",2),("Doppio Agente/1",3),("Doppio Agente/2",4)]
	def __init__(self):
		BWindow.__init__(self, BRect(300,150,1000,365), "Treno", window_type.B_FLOATING_WINDOW,  B_NOT_RESIZABLE|B_CLOSE_ON_ESCAPE)
		self.bckgnd = BView(self.Bounds(), "bckgnd_View", 8, 20000000)
		self.AddChild(self.bckgnd,None)
		self.bckgnd.SetResizingMode(B_FOLLOW_ALL_SIDES)
		a=BFont()
		rect=self.bckgnd.Bounds()
		
		self.boxaccp = BBox(BRect(8,32,rect.Width()/3-8,rect.Height()-46),"Box_acc_partenza",0x0202|0x0404,border_style.B_FANCY_BORDER)
		self.bckgnd.AddChild(self.boxaccp,None)
		baprect=self.boxaccp.Bounds()
		self.chkaccp = BCheckBox(BRect(8,8,rect.Width()/3-8,28),"CheckBox_acc_partenza","Accessori partenza",BMessage(1500))
		self.bckgnd.AddChild(self.chkaccp,None)
		
		self.menuaccp=BMenu("Tipo accessori")
		self.menuaccp.SetLabelFromMarked(True)
		for y in self.tipoaccp:
			self.menuaccp.AddItem(TipoAccp(y))
		self.menufp = BMenuField(BRect(8,8,158,12+a.Size()), 'pop0', '', self.menuaccp,B_FOLLOW_TOP)
		self.menufp.SetDivider(0)
		self.boxaccp.AddChild(self.menufp,None)
		
		self.name=BTextControl(BRect(rect.Width()/3+8,8,rect.Width()*2/3-8,12+a.Size()),"ntreno", "Numero treno:","1234",BMessage(1900))
		self.bckgnd.AddChild(self.name,None)
		
		self.boxacca = BBox(BRect(rect.Width()*2/3+8,32,rect.Width()-8,rect.Height()-46),"Box_acc_arrivo",0x0202|0x0404,border_style.B_FANCY_BORDER)
		self.bckgnd.AddChild(self.boxacca,None)
		baarect=self.boxacca.Bounds()
		self.chkacca = BCheckBox(BRect(rect.Width()*2/3+8,8,rect.Width()-8,28),"CheckBox_acc_arrivo","Accessori arrivo",BMessage(1501))
		self.bckgnd.AddChild(self.chkacca,None)
		self.menuacca=BMenu("Tipo accessori")
		self.menuacca.SetLabelFromMarked(True)
		for y in self.tipoacca:
			self.menuacca.AddItem(TipoAcca(y))
		self.menufa = BMenuField(BRect(8,8,158,12+a.Size()), 'pop0', '', self.menuacca,B_FOLLOW_TOP)
		self.menufa.SetDivider(0)
		self.boxacca.AddChild(self.menufa,None)
		
		# self.menupt=BMenu("1")
		# self.menupt.SetLabelFromMarked(True)
		# self.menupt.AddItem(ParteItem(1))
		# self.menupt.AddItem(ParteItem(2))
		# self.mfparte = BMenuField(BRect(8, rect.Height()-32-a.Size(),78 , rect.Height()-8), 'parte', 'Parte', self.menupt,B_FOLLOW_TOP) #rect.Width()*2/3+78 <-- it's ignored if I write 0 the item is fully visible
		# self.mfparte.SetDivider(a.StringWidth("Parte "))
		# self.bckgnd.AddChild(self.mfparte,None)
		self.menuia=BMenu("1")
		self.menuia.SetLabelFromMarked(True)
		self.menuia.AddItem(Ia(1))
		self.menuia.AddItem(Ia(2))
		self.mfia = BMenuField(BRect(8, rect.Height()-32-a.Size(),62 , rect.Height()-8), 'inizio_accessori', 'Ia:', self.menuia,B_FOLLOW_TOP)
		self.mfia.SetDivider(a.StringWidth("Ia: "))
		self.bckgnd.AddChild(self.mfia,None)
		
		self.menuit=BMenu("1")
		self.menuit.SetLabelFromMarked(True)
		self.menuit.AddItem(It(1))
		self.menuit.AddItem(It(2))
		self.mfit = BMenuField(BRect(66, rect.Height()-32-a.Size(),120 , rect.Height()-8), 'inizio_accessori', 'It:', self.menuit,B_FOLLOW_TOP)
		self.mfit.SetDivider(a.StringWidth("Ia: "))
		self.bckgnd.AddChild(self.mfit,None)
		
		self.menuft=BMenu("1")
		self.menuft.SetLabelFromMarked(True)
		self.menuft.AddItem(Ft(1))
		self.menuft.AddItem(Ft(2))
		self.mfft = BMenuField(BRect(124, rect.Height()-32-a.Size(),178 , rect.Height()-8), 'inizio_accessori', 'Ft:', self.menuft,B_FOLLOW_TOP)
		self.mfft.SetDivider(a.StringWidth("Ft: "))
		self.bckgnd.AddChild(self.mfft,None)
		
		self.menufa=BMenu("1")
		self.menufa.SetLabelFromMarked(True)
		self.menufa.AddItem(Fa(1))
		self.menufa.AddItem(Fa(2))
		self.mffa = BMenuField(BRect(182, rect.Height()-32-a.Size(),238 , rect.Height()-8), 'inizio_accessori', 'Fa:', self.menufa,B_FOLLOW_TOP)
		self.mffa.SetDivider(a.StringWidth("Fa: "))
		self.bckgnd.AddChild(self.mffa,None)
		
		self.menutt=BMenu("1")
		self.menutt.SetLabelFromMarked(True)
		self.menutt.AddItem(TotaleItem(1))
		self.menutt.AddItem(TotaleItem(2))
		self.mftotale = BMenuField(BRect(242, rect.Height()-32-a.Size(), 292, rect.Height()-8), 'totale', 'di', self.menutt,B_FOLLOW_TOP)
		self.mftotale.SetDivider(a.StringWidth("di "))
		self.bckgnd.AddChild(self.mftotale,None)
		
		self.oip = BTextControl(BRect(12,28+a.Size(),132,32+2*a.Size()),"ora_inizio_p", "Inizio ore:",str(5),BMessage(1901))
		self.oip.SetDivider(90.0)
		self.mip = BTextControl(BRect(136,28+a.Size(),192,32+2*a.Size()),"min_inizio_p", "min:",str(58),BMessage(1902))
		self.boxaccp.AddChild(self.oip,None)
		self.boxaccp.AddChild(self.mip,None)
		self.ofa = BTextControl(BRect(12,28+a.Size(),132,32+2*a.Size()),"ora_fine_a", "Fine ore:",str(6),BMessage(1903))
		self.ofa.SetDivider(75.0)
		self.mfa = BTextControl(BRect(136,28+a.Size(),192,32+2*a.Size()),"min_fine_a", "min:",str(38),BMessage(1904))
		self.boxacca.AddChild(self.ofa,None)
		self.boxacca.AddChild(self.mfa,None)
		
		self.menup=BMenu("Stazione")
		self.menua=BMenu("Stazione")
		self.menup.SetLabelFromMarked(True)
		self.menua.SetLabelFromMarked(True)
		for z in legenda:
			self.menup.AddItem(StazionePartenza(z))
			self.menua.AddItem(StazioneArrivo(z))
		self.pstr = BStringView(BRect(rect.Width()/3+8, 32, rect.Width()/2-8, 52),'string_part','Partenza:',B_FOLLOW_TOP)
		self.bckgnd.AddChild(self.pstr,None)
		self.astr = BStringView(BRect(rect.Width()/2+8, 32, rect.Width()*2/3-8, 52),'string_arr','Arrivo:',B_FOLLOW_TOP)
		self.bckgnd.AddChild(self.astr,None)
		self.pbar = BMenuField(BRect(rect.Width()/3+8, 52, rect.Width()/2-8, 72), 'pop1', '', self.menup,B_FOLLOW_TOP)
		self.pbar.SetDivider(0)
		self.bckgnd.AddChild(self.pbar,None)
		self.abar = BMenuField(BRect(rect.Width()/2+8, 52, rect.Width()*2/3-8, 72), 'pop2', '',self.menua,B_FOLLOW_TOP)
		self.abar.SetDivider(0)
		self.bckgnd.AddChild(self.abar,None)
		self.oit = BTextControl(BRect(rect.Width()/3+8,82,rect.Width()/3+48,102),"ora_inizio_treno", "h:",str(5),BMessage(1905))
		self.oit.SetDivider(self.bckgnd.StringWidth("h: "))
		self.mit = BTextControl(BRect(rect.Width()/3+52,82,rect.Width()/3+98,102),"min_inizio_treno", "m:",str(58),BMessage(1906))
		self.mit.SetDivider(self.bckgnd.StringWidth("m: "))
		self.oft = BTextControl(BRect(rect.Width()/2+8,82,rect.Width()/2+48,102),"ora_fine_treno", "h:",str(6),BMessage(1907))
		self.oft.SetDivider(self.bckgnd.StringWidth("h: "))
		self.mft = BTextControl(BRect(rect.Width()/2+52,82,rect.Width()/2+98,102),"min_fine_treno", "m:",str(38),BMessage(1908))
		self.mft.SetDivider(self.bckgnd.StringWidth("m: "))
		self.bckgnd.AddChild(self.oit,None)
		self.bckgnd.AddChild(self.mit,None)
		self.bckgnd.AddChild(self.oft,None)
		self.bckgnd.AddChild(self.mft,None)
		
		self.cond=BMenu("Tipo condotta")
		self.cond.SetLabelFromMarked(True)
		for z in tipocond:
			self.cond.AddItem(Condotta(z))
		self.condmf = BMenuField(BRect(rect.Width()/3+8, 112, rect.Width()*2/3-8, 132), 'pop1', 'Condotta:', self.cond,B_FOLLOW_TOP)
		self.condmf.SetDivider(80.0)
		self.bckgnd.AddChild(self.condmf,None)
		
		self.menumat = BMenu("Materiale rotabile")
		self.menumat.SetLabelFromMarked(True)
		for m in materiali:
			self.menumat.AddItem(Materiale(m))
		self.mfmat = BMenuField(BRect(rect.Width()/3+8, 142, rect.Width()*2/3-8, 162), 'materiale', 'Materiale:', self.menumat,B_FOLLOW_TOP)#48+2*a.Size(),44+3*a.Size()
		self.mfmat.SetDivider(80.0)
		self.bckgnd.AddChild(self.mfmat,None)
		self.addBtn=BButton(BRect(rect.Width()/2, rect.Height()-32-a.Size(),rect.Width()-8,rect.Height()-8),'AddBtn','Aggiungi',BMessage(1112),B_FOLLOW_BOTTOM|B_FOLLOW_RIGHT)
		self.addBtn.SetEnabled(False)
		self.bckgnd.AddChild(self.addBtn,None)
		perc=BPath()
		#find_directory(directory_which.B_SYSTEM_DATA_DIRECTORY,perc,False,None)
		ent=BEntry(os.path.dirname(os.path.realpath(__file__))+"/orloi2.jpg")
		lab='🕒'
		if ent.Exists():
			ent.GetPath(perc)
			img1=BTranslationUtils.GetBitmap(perc.Path(),None)
			self.getTimeBtn=PButton(BRect(rect.Width()/2-48,rect.Height()-32-a.Size(), rect.Width()/2-8,rect.Height()-8),'GetTimeButton',lab,BMessage(1020),B_FOLLOW_TOP|B_FOLLOW_RIGHT,img1)
		else:
			self.getTimeBtn=BButton(BRect(rect.Width()/2-48,rect.Height()-32-a.Size(),rect.Width()/2-8,rect.Height()-8),'GetTimeButton',lab,BMessage(1020),B_FOLLOW_BOTTOM|B_FOLLOW_RIGHT)
		self.bckgnd.AddChild(self.getTimeBtn,None)
	def checkvalues(self):
		ret=True
		if self.chkaccp.Value()==0:
			for testo in {self.oip.Text(),self.mip.Text()}:
				try:
					int(testo)
				except:
					ret=False
			if self.codaccp==0:
				ret=False
		if self.chkacca.Value()==0:
			for testo in {self.ofa.Text(),self.mfa.Text()}:
				try:
					int(testo)
				except:
					ret=False
			if self.codacca==0:
				ret=False
		for testo in {self.oit.Text(),self.mit.Text(),self.oft.Text(),self.mft.Text()}:
			try:
				int(testo)
			except:
				ret=False
		if ret:
			try:
				int(self.name.Text())
			except:
				# print("nome treno sbagliato")
				ret=False
				self.name.MarkAsInvalid(True)
			if self.cp==None or self.ca==None:
				# print("mancano stazione di partenza e/o di arrivo")
				ret=False
			if self.parte>self.totale:
				# print("la parte è superiore al totale")
				ret=False
			
			dtit=datetime.timedelta(hours=int(self.oit.Text()),minutes=int(self.mit.Text()))
			dtft=datetime.timedelta(hours=int(self.oft.Text()),minutes=int(self.mft.Text()))
			if dtit>=dtft:
				if self.partef==self.parte:
					# print("l'ora di partenza è successiva all'ora di arrivo")
					ret=False
			if self.chkaccp.Value()==0:
				dtap=datetime.timedelta(hours=int(self.oip.Text()),minutes=int(self.mip.Text()))
				if dtap>dtit:
					if self.parte==self.ina:
						# print("l'ora di inizio accessori in partenza è successiva all'ora di partenza")
						ret=False
			if self.chkacca.Value()==0:
				dtaa=datetime.timedelta(hours=int(self.ofa.Text()),minutes=int(self.mfa.Text()))
				if dtaa<dtft:
					if self.fia==self.partef:
						# print("l'ora di fine accessori in arrivo è antecedente all'orario di arrivo")
						ret=False
			if self.ccond == 0:
				# print("non è stato selezionato un modulo di condotta")
				ret=False
		print(ret)
		return ret
	def MessageReceived(self, msg):
		print(msg.what)
		if msg.what == 1500:
			if self.chkaccp.Value()==0:
				self.boxaccp.Show()
			else:
				self.boxaccp.Hide()
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 1501:
			if self.chkacca.Value()==0:
				self.boxacca.Show()
			else:
				self.boxacca.Hide()
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 605:
			#stabilisco stazione partenza
			self.cp = msg.FindString("code")
			self.np = msg.FindString("name")
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 606:
			#stabilisco stazione arrivo
			self.ca = msg.FindString("code")
			self.na = msg.FindString("name")
			self.addBtn.SetEnabled(self.checkvalues())
		# elif msg.what == 608:
			# self.parte = msg.FindInt8("code")
			# self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 666:
			self.parte = msg.FindInt8("code")
			self.ina=self.parte
			if self.ina>1:
				self.menutt.FindItem("2").SetMarked(True)
				self.totale = 2
				self.menuit.FindItem("2").SetMarked(True)
				self.parte=2
				self.menuft.FindItem("2").SetMarked(True)
				self.partef=2
				self.menufa.FindItem("2").SetMarked(True)
				self.fia=2
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 667:
			self.parte = msg.FindInt8("code")
			if self.parte>1:
				self.menutt.FindItem("2").SetMarked(True)
				self.totale = 2
				self.menuft.FindItem("2").SetMarked(True)
				self.partef=2
				self.menufa.FindItem("2").SetMarked(True)
				self.fia=2
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 668:
			self.partef = msg.FindInt8("code")
			if self.partef>1:
				self.menutt.FindItem("2").SetMarked(True)
				self.totale = 2
				self.menufa.FindItem("2").SetMarked(True)
				self.fia=2
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 669:
			self.fia = msg.FindInt8("code")
			if self.fia>1:
				self.menutt.FindItem("2").SetMarked(True)
				self.totale = 2
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 609:
			self.totale = msg.FindInt8("code")
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 808:
			self.ccond=msg.FindInt8("code")
			self.ncond=msg.FindString("name")
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 610:
			#selezione materiale
			self.accp=msg.FindInt8("accp")
			self.acca=msg.FindInt8("acca")
			self.prkp=msg.FindInt8("prkp")
			self.prka=msg.FindInt8("prka")
			self.cb=msg.FindInt8("cb2")
			self.mat=msg.FindString("name")
			if self.chkaccp.Value()==0:
				if self.codaccp!=0:
					datoi=datetime.timedelta(hours=int(self.oit.Text()),minutes=int(self.mit.Text()))
					if self.codaccp == 1:
						#usa accp
						delt=datetime.timedelta(minutes=self.accp)
					elif self.codaccp == 3:
						#cv in partenza
						delt=datetime.timedelta(minutes=15)
					elif self.codaccp == 5:
						#usa prkp
						delt=datetime.timedelta(minutes=self.prkp)
					if datoi-delt<datetime.timedelta(minutes=0):
						if self.ina == 2:
							print("non dovrebbe succedere: siamo già nella seconda parte del turno, l'accessorio non può trovarsi ora nella prima parte del turno")
						else:
							if self.parte == 1:
								self.parte = 2
								self.menuit.FindItem("2").SetMarked(True)
								self.totale = 2
								self.menuft.FindItem("2").SetMarked(True)
								self.fia = 2
								self.menufa.FindItem("2").SetMarked(True)
								self.totale = 2
								self.menutt.FindItem("2").SetMarked(True)
							dtout=datoi+datetime.timedelta(hours=24)-delt
					else:
						dtout=datoi-delt
					self.mip.SetText(str((dtout.seconds % 3600) // 60))
					self.oip.SetText(str(dtout.days * 24 + dtout.seconds // 3600))
			if self.chkacca.Value()==0:
				if self.codacca!=0:
					datoi=datetime.timedelta(hours=int(self.oft.Text()),minutes=int(self.mft.Text()))
					if self.codacca == 2:
						#usa acca
						delt=datetime.timedelta(minutes=self.acca)
					elif self.codacca == 4:
						#cv in arrivo
						delt=datetime.timedelta(minutes=10)
					elif self.codacca == 6:
						#usa prka
						delt=datetime.timedelta(minutes=self.prka)
					elif self.codacca == 7:
						#cambio banco
						delt=datetime.timedelta(minutes=self.cb) #TODO verificare se va su giornosucessivo
					dtout=datoi+delt
					if dtout>datetime.timedelta(hours=23,minutes=59):
						if self.partef < 2:
							dtout=dtout-datetime.timedelta(hours=24)
							self.fia=2
							self.menufa.FindItem("2").SetMarked(True)
							self.totale = 2
							self.menutt.FindItem("2").SetMarked(True)
						else:
							print("errore il turno non si può sviluppare su 3 giorni")
					self.mfa.SetText(str((dtout.seconds % 3600) // 60))
					self.ofa.SetText(str(dtout.days * 24 + dtout.seconds // 3600))
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 707:
			self.codaccp = msg.FindInt8("code")
			self.tap = msg.FindString("name")
			if self.mat!=None:
				datoi=datetime.timedelta(hours=int(self.oit.Text()),minutes=int(self.mit.Text()))
				if self.codaccp != 0:
					if self.codaccp == 1:
						#usa accp
						delt=datetime.timedelta(minutes=self.accp)
					elif self.codaccp == 3:
						#cv in partenza
						delt=datetime.timedelta(minutes=15)
					elif self.codaccp == 5:
						#usa prkp
						delt=datetime.timedelta(minutes=self.prkp)
					dtout=datoi-delt
					self.mip.SetText(str((dtout.seconds % 3600) // 60))
					self.oip.SetText(str(dtout.days * 24 + dtout.seconds // 3600))
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 708:
			self.codacca = msg.FindInt8("code")
			self.taa = msg.FindString("name")
			if self.mat!=None:
				datoi=datetime.timedelta(hours=int(self.oft.Text()),minutes=int(self.mft.Text()))
				if self.codacca != 0:
					if self.codacca == 2:
						#usa acca
						delt=datetime.timedelta(minutes=self.acca)
					elif self.codacca == 4:
						#cv in arrivo
						delt=datetime.timedelta(minutes=10)
					elif self.codacca == 6:
						#usa prka
						delt=datetime.timedelta(minutes=self.prka)
					elif self.codacca == 7:
						#cambio banco
						delt=datetime.timedelta(minutes=self.cb)
					dtout=datoi+delt
					self.mfa.SetText(str((dtout.seconds % 3600) // 60))
					self.ofa.SetText(str(dtout.days * 24 + dtout.seconds // 3600))
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 1020:
			#recupera orario e stazione precedente
			lt=be_app.WindowAt(0).listaturni.lv
			if lt.CountItems()>1:
				doit=False
				if lt.CurrentSelection()>-1:
					selitm=lt.ItemAt(lt.CurrentSelection())
					if type(selitm) != BStringItem:
						orario=selitm.fine
						sta=selitm.sta
						doit=True
				else:
					lastitm=lt.ItemAt(lt.CountItems()-1)
					if type(lastitm) != BStringItem:
						orario=lastitm.fine
						sta=lastitm.sta
						doit=True
				if doit:
					mins=str((orario.seconds % 3600) // 60)
					hrs=str(orario.days * 24 + orario.seconds // 3600)
					datp=datetime.timedelta(hours=int(hrs),minutes=int(mins))
					self.menup.FindItem(sta[1]).SetMarked(True)
					self.cp=sta[0]
					self.np=sta[1]
					if self.chkaccp.Value()==0:
						if self.codaccp!=0 and self.mat!=None:
							if self.codaccp == 1:
								#usa accp
								delt=datetime.timedelta(minutes=self.accp)
							elif self.codaccp == 3:
								#cv in partenza
								delt=datetime.timedelta(minutes=15)
							elif self.codaccp == 5:
								#usa prkp
								delt=datetime.timedelta(minutes=self.prkp)
							dtout=datp+delt
							self.mit.SetText(str((dtout.seconds % 3600) // 60))
							self.oit.SetText(str(dtout.days * 24 + dtout.seconds // 3600))
							self.mip.SetText(mins)
							self.oip.SetText(hrs)
						else:
							self.mip.SetText(mins)
							self.oip.SetText(hrs)
							self.mit.SetText(mins)
							self.oit.SetText(hrs)
					else:
						self.mit.SetText(mins)
						self.oit.SetText(hrs)
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 1900:
			try:
				int(self.name.Text())
				self.name.MarkAsInvalid(False)
			except:
				self.name.MarkAsInvalid(True)
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 1901:
			try:
				if -1<int(self.oip.Text())<24:
					self.oip.MarkAsInvalid(False)
				else:
					self.oip.MarkAsInvalid(True)
			except:
				self.name.MarkAsInvalid(True)
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 1902:
			try:
				if -1<int(self.mip.Text())<60:
					self.mip.MarkAsInvalid(False)
				else:
					self.mip.MarkAsInvalid(True)
			except:
				self.name.MarkAsInvalid(True)
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 1903:
			try:
				if -1<int(self.ofa.Text())<24:
					self.ofa.MarkAsInvalid(False)
				else:
					self.ofa.MarkAsInvalid(True)
			except:
				self.name.MarkAsInvalid(True)
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 1904:
			try:
				if -1<int(self.mfa.Text())<60:
					self.mfa.MarkAsInvalid(False)
				else:
					self.mfa.MarkAsInvalid(True)
			except:
				self.name.MarkAsInvalid(True)
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 1905:
			try:
				if -1<int(self.oit.Text())<24:
					self.oit.MarkAsInvalid(False)
					mitvalid=False
					try:
						if -1<int(self.mit.Text())<60:
							mitvalid=True
							self.mit.MarkAsInvalid(False)
					except:
						self.mit.MarkAsInvalid(True)
					if (self.mat!=None) and (self.chkaccp.Value()==0) and (self.codaccp!=0) and mitvalid:
						datoi=datetime.timedelta(hours=int(self.oit.Text()),minutes=int(self.mit.Text()))
						if self.codaccp == 1:
							#usa accp
							delt=datetime.timedelta(minutes=self.accp)
						elif self.codaccp == 3:
							#cv in partenza
							delt=datetime.timedelta(minutes=15)
						elif self.codaccp == 5:
							#usa prkp
							delt=datetime.timedelta(minutes=self.prkp)
						dtout=datoi-delt
						self.mip.SetText(str((dtout.seconds % 3600) // 60))
						self.oip.SetText(str(dtout.days * 24 + dtout.seconds // 3600))
				else:
					self.oit.MarkAsInvalid(True)
			except:
				self.oit.MarkAsInvalid(True)
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 1906:
			try:
				if -1<int(self.mit.Text())<60:
					self.mit.MarkAsInvalid(False)
					oitvalid=False
					try:
						if -1<int(self.oit.Text())<24:
							oitvalid=True
							self.oit.MarkAsInvalid(False)
					except:
						self.oit.MarkAsInvalid(True)
					if (self.mat!=None) and (self.chkaccp.Value()==0) and (self.codaccp!=0) and oitvalid:
						datoi=datetime.timedelta(hours=int(self.oit.Text()),minutes=int(self.mit.Text()))
						if self.codaccp == 1:
							#usa accp
							delt=datetime.timedelta(minutes=self.accp)
						elif self.codaccp == 3:
							#cv in partenza
							delt=datetime.timedelta(minutes=15)
						elif self.codaccp == 5:
							#usa prkp
							delt=datetime.timedelta(minutes=self.prkp)
						dtout=datoi-delt
						self.mip.SetText(str((dtout.seconds % 3600) // 60))
						self.oip.SetText(str(dtout.days * 24 + dtout.seconds // 3600))
				else:
					self.mit.MarkAsInvalid(True)
			except:
				self.mit.MarkAsInvalid(True)
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 1907:
			try:
				if -1<int(self.oft.Text())<24:
					self.oft.MarkAsInvalid(False)
					mftvalid=False
					try:
						if -1<int(self.mft.Text())<60:
							mftvalid=True
							self.mft.MarkAsInvalid(False)
					except:
						self.mft.MarkAsInvalid(True)
					if (self.mat!=None) and (self.chkacca.Value()==0) and (self.codacca!=0) and mftvalid:
						datoi=datetime.timedelta(hours=int(self.oft.Text()),minutes=int(self.mft.Text()))
						if self.codacca == 2:
							#usa acca
							delt=datetime.timedelta(minutes=self.acca)
						elif self.codacca == 4:
							#cv in arrivo
							delt=datetime.timedelta(minutes=10)
						elif self.codacca == 6:
							#usa prka
							delt=datetime.timedelta(minutes=self.prka)
						elif self.codacca == 7:
							#cambio banco
							delt=datetime.timedelta(minutes=self.cb)
						dtout=datoi+delt
						self.mfa.SetText(str((dtout.seconds % 3600) // 60))
						self.ofa.SetText(str(dtout.days * 24 + dtout.seconds // 3600))
				else:
					self.oft.MarkAsInvalid(True)
			except:
				self.oft.MarkAsInvalid(True)
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 1908:
			try:
				if -1<int(self.mft.Text())<60:
					self.mft.MarkAsInvalid(False)
					oftvalid=False
					try:
						if -1<int(self.oft.Text())<24:
							oftvalid=True
							self.oft.MarkAsInvalid(False)
					except:
						self.oft.MarkAsInvalid(True)
					if (self.mat!=None) and (self.chkacca.Value()==0) and (self.codacca!=0) and oftvalid:
						datoi=datetime.timedelta(hours=int(self.oft.Text()),minutes=int(self.mft.Text()))
						if self.codacca == 2:
							#usa acca
							delt=datetime.timedelta(minutes=self.acca)
						elif self.codacca == 4:
							#cv in arrivo
							delt=datetime.timedelta(minutes=10)
						elif self.codacca == 6:
							#usa prka
							delt=datetime.timedelta(minutes=self.prka)
						elif self.codacca == 7:
							#cambio banco
							delt=datetime.timedelta(minutes=self.cb)
						dtout=datoi+delt
						self.mfa.SetText(str((dtout.seconds % 3600) // 60))
						self.ofa.SetText(str(dtout.days * 24 + dtout.seconds // 3600))
				else:
					self.mft.MarkAsInvalid(True)
			except:
				self.mft.MarkAsInvalid(True)
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 1112:
			titanic=True
			if self.chkaccp.Value()==0:
				dtp=datetime.timedelta(hours=int(self.oip.Text()),minutes=int(self.mip.Text()))
				if be_app.WindowAt(0).listaturni.lv.CountItems()>0:
					if be_app.WindowAt(0).listaturni.lv.CurrentSelection()>-1:
						# print("è selezionato qualcosa")
						itm = be_app.WindowAt(0).listaturni.lv.ItemAt(be_app.WindowAt(0).listaturni.lv.CurrentSelection())
						supitm = be_app.WindowAt(0).listaturni.lv.Superitem(itm)
						if supitm != None:
							# print("step 1, selezionato elemento di turno")
							differ = dtp - itm.fine
							if differ < datetime.timedelta(minutes=0):
								titanic=False
					else:
						# print("niente di selezionato")
						if be_app.WindowAt(0).listaturni.lv.CountItems()>1:
							itm = be_app.WindowAt(0).listaturni.lv.ItemAt(be_app.WindowAt(0).listaturni.lv.CountItems()-1)
							supitm = be_app.WindowAt(0).listaturni.lv.Superitem(itm)
							if supitm != None:
								differ = dtp - itm.fine
								if differ < datetime.timedelta(minutes=0):
									titanic=False
			if titanic:
				mex=BMessage(1333)
				if self.chkaccp.Value()==0:
					mex.AddInt8("oip",int(self.oip.Text())) #ora inizio
					mex.AddInt8("mip",int(self.mip.Text())) #minuto inizio
					mex.AddInt8("ofp",int(self.oit.Text())) #ora fine
					mex.AddInt8("mfp",int(self.mit.Text())) #minuto fine
					mex.AddString("cspp",self.cp) #codice stazione partenza
					mex.AddString("csap",self.cp) #codice stazione arrivo
					mex.AddString("nspp",self.np) #nome stazione partenza
					mex.AddString("nsap",self.np) #nome stazione arrivo
					mex.AddString("ntap",self.tap) #nome tipo accessori
					mex.AddInt8("codaccp",self.codaccp) #codice accessori
				mex.AddString("materiale",self.mat)
				mex.AddInt8("parte",self.parte) #parte del turno inizio
				mex.AddInt8("partef",self.partef) #parte del turno fine
				mex.AddInt8("totale",self.totale) #totale del turno
				mex.AddString("name",self.name.Text()) #nome accessori/numero treno
				mex.AddInt8("oit",int(self.oit.Text())) #ora inizio
				mex.AddInt8("mit",int(self.mit.Text())) #minuto inizio
				mex.AddInt8("oft",int(self.oft.Text())) #ora fine
				mex.AddInt8("mft",int(self.mft.Text())) #minuto fine
				mex.AddString("cspt",self.cp) #codice stazione partenza
				mex.AddString("csat",self.ca) #codice stazione arrivo
				mex.AddString("nspt",self.np) #nome stazione partenza
				mex.AddString("nsat",self.na) #nome stazione arrivo
				mex.AddString("ncond",self.ncond) # nome tipo condotta
				mex.AddInt8("ccond",self.ccond) # codice tipo condotta
				if self.chkacca.Value()==0:
					mex.AddInt8("oia",int(self.oft.Text())) #ora inizio
					mex.AddInt8("mia",int(self.mft.Text())) #minuto inizio
					mex.AddInt8("ofa",int(self.ofa.Text())) #ora fine
					mex.AddInt8("mfa",int(self.mfa.Text())) #minuto fine
					mex.AddString("cspa",self.ca) #codice stazione partenza
					mex.AddString("csaa",self.ca) #codice stazione arrivo
					mex.AddString("nspa",self.na) #nome stazione partenza
					mex.AddString("nsaa",self.na) #nome stazione arrivo
					mex.AddString("ntaa",self.taa) #nome tipo accessori
					mex.AddInt8("codacca",self.codacca) #codice accessori
				be_app.WindowAt(0).PostMessage(mex)
			else:
				ask=BAlert('cle', "Mancata corrispondenza ora inizio accessori e rigo precedente", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
				self.alertWind.append(ask)
				ask.Go()
		return BWindow.MessageReceived(self,msg)
	def QuitRequested(self):
		self.Hide()
class PausaWindow(BWindow):
	parte=1
	partef=1
	totale=1
	def __init__(self):
		BWindow.__init__(self, BRect(150,150,586,250), "Pausa", window_type.B_FLOATING_WINDOW,  B_NOT_RESIZABLE|B_CLOSE_ON_ESCAPE)
		self.bckgnd = BView(self.Bounds(), "bckgnd_View", 8, 20000000)
		rect=self.bckgnd.Bounds()
		self.AddChild(self.bckgnd,None)
		self.bckgnd.SetResizingMode(B_FOLLOW_ALL_SIDES)
		a=BFont()
		
		# self.menupt=BMenu("1")
		# self.menupf=BMenu("1")
		# self.menutt=BMenu("1")
		# self.menupt.SetLabelFromMarked(True)
		# self.menupf.SetLabelFromMarked(True)
		# self.menutt.SetLabelFromMarked(True)
		# self.menupt.AddItem(ParteItem(1))
		# self.menupt.AddItem(ParteItem(2))
		# self.menupf.AddItem(ParteItem(1))
		# self.menupf.AddItem(ParteItem(2))
		# self.menutt.AddItem(TotaleItem(1))
		# self.menutt.AddItem(TotaleItem(2))
		# self.mfparte = BMenuField(BRect(8, rect.Height()/2+a.Size()+4, 78, rect.Height()-8), 'parte', 'Parte', self.menupt,B_FOLLOW_TOP)
		# self.mfparte.SetDivider(a.StringWidth("Parte "))
		# self.mfpartef = BMenuField(BRect(146, rect.Height()/2+a.Size()+4, rect.Width()/2-8, rect.Height()-8), 'parte_fine', 'Fine', self.menupf,B_FOLLOW_TOP)#asdfasfdasf
		# self.mfpartef.SetDivider(a.StringWidth("Fine "))
		
		# self.mftotale = BMenuField(BRect(88,rect.Height()/2+a.Size()+4, 142, rect.Height()-8), 'totale', 'di', self.menutt,B_FOLLOW_TOP)
		# self.mftotale.SetDivider(a.StringWidth("di "))
		# self.bckgnd.AddChild(self.mfparte,None)
		# self.bckgnd.AddChild(self.mfpartef,None)
		# self.bckgnd.AddChild(self.mftotale,None)
		
		self.name=BTextControl(BRect(8,8,rect.Width()*2/3-8,12+a.Size()),"pausa_name", "Nome:","Pausa",BMessage(1902))
		self.deltamvalue=BTextControl(BRect(8+rect.Width()/2,rect.Height()/2-a.Size(),rect.Width()-8,rect.Height()/2+a.Size()-4),"delta_min_value", "Minuti:",str(10),BMessage(1900))
		self.deltaovalue=BTextControl(BRect(8,rect.Height()/2-a.Size(),rect.Width()/2-8,rect.Height()/2+a.Size()-4),"delta_ora_value", "Ore:",str(0),BMessage(1901))
		self.bckgnd.AddChild(self.name,None)
		self.bckgnd.AddChild(self.deltamvalue,None)
		self.bckgnd.AddChild(self.deltaovalue,None)
		self.addBtn=BButton(BRect(rect.Width()/2, rect.Height()/2+a.Size()+4,rect.Width()-8,rect.Height()-8),'AddBtn','Aggiungi',BMessage(1001),B_FOLLOW_BOTTOM|B_FOLLOW_RIGHT)
		self.bckgnd.AddChild(self.addBtn,None)
	def checkvalues(self):
		ret=True
		
		for testo in {self.deltamvalue.Text(),self.deltaovalue.Text()}:
			try:
				int(testo)
			except:
				ret=False
		if ret:
			if self.parte>self.totale:
				ret=False
		return ret
	def MessageReceived(self, msg):
		if msg.what==1001:
			mex=BMessage(1001)
			mex.AddInt8("deltam",int(self.deltamvalue.Text()))
			mex.AddInt8("deltao",int(self.deltaovalue.Text()))
			#mex.AddInt8("parte",self.parte)
			#mex.AddInt8("partef",self.partef)
			#mex.AddInt8("totale",self.totale)
			mex.AddString("name",self.name.Text())
			be_app.WindowAt(0).PostMessage(mex)
		# elif msg.what == 608:
			# self.parte = msg.FindInt8("code")
			# if self.parte> self.totale:
				# self.menutt.FindItem("2").SetMarked(True)
				# self.totale=2
				# self.menupf.FindItem("2").SetMarked(True)
				# self.partef=2
			# self.addBtn.SetEnabled(self.checkvalues())
		# elif msg.what == 609:
			# self.totale = msg.FindInt8("code")
			# self.addBtn.SetEnabled(self.checkvalues())
		# elif msg.what == 908:
			# self.partef = msg.FindInt8("code")
			# if self.partef> self.totale:
				# self.menutt.FindItem("2").SetMarked(True)#.Invoke()
				# self.totale=2
				# #self.menutt.ItemAt(1).SetMarked(True)
			# self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 1900:
			try:
				int(self.deltamvalue.Text())
				self.deltamvalue.MarkAsInvalid(False)
				if self.checkvalues():
					self.addBtn.SetEnabled(True)
			except:
				self.deltamvalue.MarkAsInvalid(True)
				self.addBtn.SetEnabled(False)
		elif msg.what == 1901:
			try:
				int(self.deltaovalue.Text())
				self.deltaovalue.MarkAsInvalid(False)
				if self.checkvalues():
					self.addBtn.SetEnabled(True)
			except:
				self.deltaovalue.MarkAsInvalid(True)
				self.addBtn.SetEnabled(False)
		return BWindow.MessageReceived(self,msg)
	def QuitRequested(self):
		self.Hide()
class MainWindow(BWindow):
	tmpWind=[]
	tmpElem=[]
	alertWind=[]
	ntreni = []
	vett_comandate = []
	Menus = (
		('File', ((1, 'Carica turno'),(2, 'Salva turno'),(3, 'Distruggi turni'),(None, None),(int(AppDefs.B_QUIT_REQUESTED), 'Esci'))),('Aggiungi', ((4, 'Accessori'),(5, 'Vettura'),(6, 'Treno'),(7, 'Pausa'))),('Elaborazione', ((10, 'Estrai treni'),(11, 'Componi treni-acc'),(42, 'Crea giornate'))),
		('Aiuto', ((8, 'Judimi'),(23, 'Informazioni')))
		)
	def __init__(self,autoload):
		global tab,name
		BWindow.__init__(self, BRect(50,100,1024,750), "Scrittore turni", window_type.B_TITLED_WINDOW, B_QUIT_ON_WINDOW_CLOSE) #B_NOT_RESIZABLE | B_QUIT_ON_WINDOW_CLOSE)#B_MODAL_WINDOW
		bounds=self.Bounds()
		self.bckgnd = BView(self.Bounds(), "background_View", 8, 20000000)
		self.bckgnd.SetResizingMode(B_FOLLOW_ALL_SIDES)
		bckgnd_bounds=self.bckgnd.Bounds()
		self.AddChild(self.bckgnd,None)
		self.bar = BMenuBar(bckgnd_bounds, 'Bar')
		x, barheight = self.bar.GetPreferredSize()
		for menu, items in self.Menus:
			menu = BMenu(menu)
			for k, name in items:
				if k is None:
					menu.AddItem(BSeparatorItem())
				else:
					mitm=BMenuItem(name, BMessage(k),name[0],0)
					menu.AddItem(mitm)
			self.bar.AddItem(menu)
		a=BFont()
		self.box = BBox(BRect(0,0,bckgnd_bounds.Width(),bckgnd_bounds.Height()),"Underbox",0x0202|0x0404,border_style.B_FANCY_BORDER)
		self.bckgnd.AddChild(self.box, None)
		self.box.AddChild(self.bar, None)
		self.listaturni = ScrollView(BRect(4 , a.Size()+24+barheight, bounds.Width()- 18, bounds.Height() - 4 ), 'OptionsScrollView')
		self.box.AddChild(self.listaturni.sv, None)
		self.turno=BTextControl(BRect(4,4+barheight,150,a.Size()),"turn_name", "FV:","1000",BMessage(1800))
		self.box.AddChild(self.turno, None)
		self.addBtn=BButton(BRect(160, 4+barheight, 300,a.Size()),'AddBtn','Aggiungi turno',BMessage(1801),B_FOLLOW_TOP|B_FOLLOW_LEFT)
		self.box.AddChild(self.addBtn, None)
		self.remBtn=BButton(BRect(305, 4+barheight, 445,a.Size()),'RemBtn','Rimuovi turno/elemento',BMessage(1802),B_FOLLOW_TOP|B_FOLLOW_LEFT)
		self.box.AddChild(self.remBtn, None)
		perc=BPath()
		#find_directory(directory_which.B_SYSTEM_DATA_DIRECTORY,perc,False,None)
		ent=BEntry(os.path.dirname(os.path.realpath(__file__))+"/deselect.jpg")#"/boot/home/Apps/ScrittoreTurni/orloi.jpg")
		if ent.Exists():
			ent.GetPath(perc)
			img1=BTranslationUtils.GetBitmap(perc.Path(),None)
			self.deselectBtn=PButton(BRect(bckgnd_bounds.right-32, 4+barheight, bckgnd_bounds.right-2,34+barheight),'DeselectBtn','▤',BMessage(1020),B_FOLLOW_TOP|B_FOLLOW_RIGHT,img1)#▤⌧
		else:
			lab="▤"#▤⌧
			self.deselectBtn=BButton(BRect(bckgnd_bounds.right-32,4+barheight,bckgnd_bounds.right-2,34+barheight),'DeselectBtn',lab,BMessage(1020),B_FOLLOW_TOP|B_FOLLOW_RIGHT)
		self.box.AddChild(self.deselectBtn, None)
		if autoload!="":
			ofpmsg=BMessage(45371)
			ofpmsg.AddString("path",autoload)
			be_app.WindowAt(0).PostMessage(ofpmsg)
			osdir=os.path.dirname(autoload)
			osfile=os.path.basename(autoload)
		else:
			osdir="/boot/home/Desktop"
			osfile="Turni.trn"
		self.fp=BFilePanel(B_SAVE_PANEL,None,None,0,False, None, None, True, True)#B_SAVE_PANEL)
		self.fp.SetPanelDirectory(osdir)
		self.fp.SetSaveText(osfile)
		self.ofp=BFilePanel(B_OPEN_PANEL,None,None,0,False, None, None, True, True)#B_SAVE_PANEL)
		self.ofp.SetPanelDirectory(osdir)
		self.ofp.SetSaveText(osfile)
		#self.ask=BAlert('cle', "numero argomenti:"+str(len(sys.argv)), 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
		#self.ask.Go()
		#se sys.argv ha un file caricarlo

	def FrameResized(self,x,y):
		resiz=False
		if x<974:
			x=974
			resiz=True
		if y<650:
			y=650
			resiz=True
		if resiz:
			self.ResizeTo(x,y)
		self.box.ResizeTo(x,y)
		self.bar.ResizeTo(x,self.bar.Bounds().bottom)
		xx, barheight = self.bar.GetPreferredSize()
		self.listaturni.sv.ResizeTo(x-self.listaturni.sv.Frame().left-2,self.box.Bounds().Height()-barheight-4)
		self.listaturni.lv.ResizeTo(self.listaturni.sv.Bounds().Width(),self.listaturni.sv.Bounds().Height()-4)
		BWindow.FrameResized(self,x,y)
	def MessageReceived(self, msg):
		if msg.what == 7:#apri finestra inserimento pausa
			try:
				if self.pausa_window.IsHidden():
					self.pausa_window.Show()
				self.pausa_window.Activate()
			except:
				self.pausa_window = PausaWindow()
				self.tmpWind.append(self.pausa_window)
				self.pausa_window.Show()
		elif msg.what == 5:#apri finestra inserimento vettura
			try:
				if self.vett_window.IsHidden():
					self.vett_window.Show()
				self.vett_window.Activate()
			except:
				self.vett_window = VettWindow()
				self.tmpWind.append(self.vett_window)
				self.vett_window.Show()
		elif msg.what == 6:#apri finestra inserimento treno
			try:
				if self.treno_window.IsHidden():
					self.treno_window.Show()
				self.treno_window.Activate()
			except:
				self.treno_window = TrenoWindow()
				self.tmpWind.append(self.treno_window)
				self.treno_window.Show()
		elif msg.what == 4:#apri finestra inserimento accessori
			try:
				if self.acc_window.IsHidden():
					self.acc_window.Show()
				self.acc_window.Activate()
			except:
				self.acc_window = AccWindow()
				self.tmpWind.append(self.acc_window)
				self.acc_window.Show()
		elif msg.what == 10:#estrai treni
			for og in self.listaturni.lv.Items():
				if type(og)!=BStringItem:
					if type(og)!=VettItem and type(og)!=PausItem:
						try:
							#try:
							#	num=int(og.name)
							#except:
							#	print("errore in:",og.name)
							#	num=0
							num=int(og.name)
							go=True
							for x in self.ntreni: #controllo se esiste già in ntreni
								if x[0]==num:
									go=False
									break
							if go:
								#il treno non è in ntreni
								self.ntreni.append((num,[]))
								#if type(og) == TrenoItem:
								#	#print(self.listaturni.lv.Superitem(og).Text())
								#	#oggetto=GTreno(num,og.inizio,og.stp,og.fine,og.sta,int(self.listaturni.lv.Superitem(og).Text()),int(og.parte),int(og.totale))
								#	#ntreni[-1][1].append(oggetto)
								#	oggetto=og
								#elif type(og) == AccItem:
								#	#print(self.listaturni.lv.Superitem(og).Text())
								#	#oggetto=GAcc(num,og.inizio,og.stp,og.fine,og.sta,int(self.listaturni.lv.Superitem(og).Text()),int(og.parte),og.int(totale))
								#	oggetto=og
								self.ntreni[-1][1].append(og)#getto)
							#elif type(og) == VettItem:
							#	oggetto=GVett(
							
							else:
								#il treno esiste in ntreni
								match=[x for x in self.ntreni if x[0] == num]
								#if type(og) == TrenoItem:
								#	#oggetto=GTreno(num,og.inizio,og.stp,og.fine,og.sta,int(self.listaturni.lv.Superitem(og).Text()),int(og.parte),int(og.totale))
								#	##match[0][1].append(oggetto)
								#	oggetto = og
								#elif type(og) == AccItem:
								#	#oggetto=GAcc(num,og.inizio,og.stp,og.fine,og.sta,int(self.listaturni.lv.Superitem(og).Text()),int(og.parte),int(og.totale))
								#	oggetto = og
								#match[0][1].append(oggetto)
								match[0][1].append(og)
						except:
						#	print(og.label)
						#	#si tratta di Riserva #TODO
							pass
							#if type(og) == VettItem:
							#	nam = og.name
					else:
						#gestiamo VettItems o PausItems #TODO
						pass
			#print(ntreni)
			#print(type(self.ntreni))
			#print(self.ntreni)
			sumtreni={}
			for item in self.ntreni:
				pnt=item[0]
				print(pnt)
				if not(pnt in sumtreni):
					l=[]
					for tur in self.listaturni.lv.Items():#self.ntreni:
						if type(tur)==BStringItem:
							pass
						else:
							if str(tur.name)==str(pnt):
								l.append((self.listaturni.lv.Superitem(tur).Text(),tur))#fv,elemento
					sumtreni[pnt]=l
			#print(sumtreni)
			#for k in sumtreni.keys():
			#print(sumtreni)
			try:
				if self.estraz_window.IsHidden():
					self.estraz_window.ReSet(sumtreni)
					self.estraz_window.Show()
				self.estraz_window.Activate()
			except:
				self.estraz_window = EstrazTreni(sumtreni)
				self.tmpWind.append(self.estraz_window)
				self.estraz_window.Show()
		elif msg.what == 11:#componi treni-accessori
			#if len(self.ntreni)>0:
			for x in self.ntreni:
				#lowgacc=(datetime.timedelta(hours=23,minutes=59),(None,None),2,0)#2 è parte turno, esempio. se accessori iniziano alle 23.50, ma il cambio volante inizia alle 00:10 i primi tempi accessori sono 23:50
				#lowgtrenot=datetime.timedelta(hours=23,minutes=59)
				#lowgaccn=x[0]
				#highgacc=(datetime.timedelta(hours=0,minutes=0),(None,None),1,0)
				#hightrenot=datetime.timedelta(hours=0,minutes=0)
				#trno=(datetime.timedelta(hours=23,minutes=59),(None,None),datetime.timedelta(hours=23,minutes=59),(None,None),2,1,0)
				outp=None
				outa=None
				outt=[]
				
				for y in x[1]:
					if type(y)==AccItem:
						if int(y.codacc) in [ 1, 3, 5 ]: #se è un accessorio in partenza
							if outp==None:
								outp=y
							else:
								if y.inizio < outp.inizio:
									#controlla che il delta tra i due accessori non sia esagerato
									#potrebbe indicare un accessorio a cavallo tra due giorni
									dlt=outp.inizio-y.inizio
									if dlt<datetime.timedelta(hours=8,minutes=0):
										outp=y
									else:
										print("potrebbe essere un accessorio a cavallo di due giorni, pertanto questo accessorio è successivo a quello già in memoria")
								else:
									#print("controllo se y.inizio è nel giorno precedente")
									if outp.inizio + datetime.timedelta(hours=24, minutes=0)-y.inizio<datetime.timedelta(hours=8,minutes=0):
										print("potrebbe essere un accessorio a cavallo di due giorni")
										outp=y
							#if int(y.parte) < lowgacc[2]:
							#	lowgacc=(y.inizio,y.stp,int(y.parte),self.listaturni.lv.Superitem(y).Text())
							#	outp=y
							#else:
							#	if y.inizio<=lowgacc[0]:
							#		lowgacc=(y.inizio,y.stp,int(y.parte),self.listaturni.lv.Superitem(y).Text())
							#		outp=y
						elif int(y.codacc) in [ 2,4,6,7 ]:
							if outa==None:
								outa=y
							else:
								if y.fine>outa.fine:
									#controlla che il delta non sia esagerato perché altrimenti potrebbe indicare
									# che l'accessorio in arrivo si sviluppi su più giorni
									dlt=y.fine-outa.fine
									if dlt<datetime.timedelta(hours=8):
										outa=y
									else:
										print("potrebbe essere un accessorio a cavallo di giornata, pertanto mantengo quello vecchio che casca il giorno successivo")
								else:
									#print("controllo se y.fine è nel giorno successivo")
									if y.fine+datetime.timedelta(hours=24)-outa.fine<datetime.timedelta(hours=8,minutes=0):
										print("potrebbe essere un accessorio a cavallo di due giorni")
										outa=y
							#if int(y.parte) > highgacc[2]:
							#	highgacc=(y.fine,y.sta,int(y.parte),self.listaturni.lv.Superitem(y).Text())
							#	outa=y
							#else:
							#	if y.fine>=highgacc[0]:
							#		highgacc=(y.fine,y.sta,int(y.parte),self.listaturni.lv.Superitem(y).Text())
							#		outa=y
					elif type(y)==TrenoItem:
						for item in outt:
							if (item.inizio == y.inizio) and ( item.fine == y.fine ):
								print("elemento già inserito")
								pass
							else:
								outt.append(y)
				
				outt.sort(key=lambda x: x.inizio)
				print(outt)
				def_outt = self.unisci_condotte(outt)
				#print(def_outt)
				#TODO: se un lowgacc non ha un corrispettivo di treno o di highgacc bisogna far risultare accessorio ultimo di partenza (magari parte un triestino o un veneziano)
				#if outp!=None:
					#print("Orario primo accessorio in partenza di",x[0],":",lowgacc[0],lowgacc[1][0])#,lowgacc[2],outp)
				#if outa!=None:
					#print("Orario ultimo accessorio in arrivo di",x[0],":",highgacc[0],highgacc[1][0])#,highgacc[2],outa)
		elif msg.what == 1020:#deseleziona listview
			self.listaturni.lv.DeselectAll()
		elif msg.what == 1800:#controlla nome turno
			try:
				int(self.turno.Text())
				self.turno.MarkAsInvalid(False)
				self.addBtn.SetEnabled(True)
			except:
				self.turno.MarkAsInvalid(True)
				self.addBtn.SetEnabled(False)
		elif msg.what == 1801:#aggiungi turno
			#controlla se c'è già turno
			chk=True
			for tur in self.listaturni.lv.Items():
				if type(tur)==BStringItem:
					if tur.Text() == self.turno.Text():
						chk=False
						ask=BAlert('cle', "Questo turno c\'è già", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
						self.alertWind.append(ask)
						ask.Go()
						break
			if chk:
				if self.listaturni.lv.CurrentSelection()>-1:
					sel=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection())
					if type(sel)==BStringItem:
						isel=self.listaturni.lv.IndexOf(sel)
						iund=self.listaturni.lv.CountItemsUnder(sel,True)
						bli=BStringItem(self.turno.Text())
						self.listaturni.lv.AddItem(bli)
						self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(bli),isel+iund+1)
					else:
						supersel=self.listaturni.lv.Superitem(sel)
						isupsel=self.listaturni.lv.IndexOf(supersel)
						iund=self.listaturni.lv.CountItemsUnder(supersel,True)
						bli=BStringItem(self.turno.Text())
						self.listaturni.lv.AddItem(bli)
						self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(bli),isupsel+iund+1)
				else:
					bli=BStringItem(self.turno.Text())
					self.listaturni.lv.AddItem(bli)
					self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(bli),self.listaturni.lv.CountItems()-1)
					
				self.listaturni.lv.DeselectAll()
			v=int(self.turno.Text())
			v+=1
			self.turno.SetText(str(v))
		elif msg.what == 1802:#rimuovi turno
			if self.listaturni.lv.CountItems()>0:
				if self.listaturni.lv.CurrentSelection()>-1:
					self.listaturni.lv.RemoveItem(self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()))
				else:
					self.listaturni.lv.RemoveItem(self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1))
		elif msg.what == 3:#rimuovi turni
			if self.listaturni.lv.CountItems()>0:
				ask=BAlert('rem', "Questa operazione non è reversibile: rimuovere tutti i turni?", 'Sì', 'No',None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_WARNING_ALERT)
				self.alertWind.append(ask)
				ret=ask.Go()
				if not ret:
					for g in self.listaturni.lv.Items():
						self.listaturni.lv.RemoveItem(g)
		elif msg.what == 2:#pannello salva file turni
			self.fp.Show()
		elif msg.what == 1:#pannello apri file turni
			self.ofp.Show()
		elif msg.what == 45371:#carica turni
			ofpath=msg.FindString("path")
			tlist=[]
			with open(ofpath) as f:
				for r in f:
					tlist.append((r[0],r[1:]))
			#print(tlist)
			i=0
			while i<(len(tlist)):
				t = tlist[i][0]
				s = tlist[i][1]
				if t == "@":
					thisroot=BStringItem(s)
					self.listaturni.lv.AddItem(thisroot)
					self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(thisroot),self.listaturni.lv.CountItems()-1)
				elif t == "#":
					cis=self.listaturni.lv.CountItemsUnder(thisroot,True)
					vett=self.estrai_vett(s)
					self.tmpElem.append(vett)
					self.listaturni.lv.AddUnder(vett,thisroot)
					if cis!=0:
						self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vett),self.listaturni.lv.IndexOf(thisroot)+cis+1)
				elif t == "?":
					cis=self.listaturni.lv.CountItemsUnder(thisroot,True)
					pau=self.estrai_pau(s)
					self.tmpElem.append(pau)
					self.listaturni.lv.AddUnder(pau,thisroot)
					if cis!=0:
						self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(pau),self.listaturni.lv.IndexOf(thisroot)+cis+1)
				elif t == "§":
					cis=self.listaturni.lv.CountItemsUnder(thisroot,True)
					acc=self.estrai_acc(s)
					self.tmpElem.append(acc)
					self.listaturni.lv.AddUnder(acc,thisroot)
					if cis!=0:
						self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(acc),self.listaturni.lv.IndexOf(thisroot)+cis+1)
				elif t == "&":
					cis=self.listaturni.lv.CountItemsUnder(thisroot,True)
					trn=self.estrai_trn(s)
					self.tmpElem.append(trn)
					self.listaturni.lv.AddUnder(trn,thisroot)
					if cis!=0:
						self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(trn),self.listaturni.lv.IndexOf(thisroot)+cis+1)
				i+=1
		elif msg.what == 54173:#Salva turni
			b=entry_ref()
			self.fp.GetPanelDirectory(b)
			c=BEntry(b)
			d=BPath()
			c.GetPath(d)
			savepath=d.Path()
			e = msg.FindString("name")
			completepath = savepath +"/"+ e
			#print(completepath)
			with open(completepath, "a") as myfile:
				i=0
				while i < self.listaturni.lv.CountItems():
				# @,#,§,?
					ita=self.listaturni.lv.ItemAt(i)
					if type(ita)==BStringItem:
						txt="@"+ita.Text()+"\n"
					elif type(ita)==PausItem:
						#delta=ita.fine-ita.inizio
						txt="?"+ita.name+"·"+ita.iout+"·"+ita.fout+"·"+ita.sta[0]+"·"+str(ita.parte)+"·"+str(ita.partef)+"·"+str(ita.totale)+"\n"
					elif type(ita)==AccItem:
						txt="§"+ita.nta+"·"+str(ita.cta)+"·"+ita.name+"·"+ita.iout+"·"+ita.fout+"·"+ita.stp[0]+"·"+ita.sta[0]+"·"+ita.materiale+"·"+str(ita.parte)+"·"+str(ita.partef)+"·"+str(ita.totale)+"\n"
					elif type(ita)==TrenoItem:
						txt="&"+ita.name+"·"+ita.iout+"·"+ita.fout+"·"+ita.stp[0]+"·"+ita.sta[0]+"·"+str(ita.ccond)+"·"+ita.materiale+"·"+str(ita.parte)+"·"+str(ita.partef)+"·"+str(ita.totale)+"\n"
					elif type(ita)==VettItem:
						txt="#"+ita.name+"·"+ita.iout+"·"+ita.fout+"·"+ita.stp[0]+"·"+ita.sta[0]+"·"+str(ita.parte)+"·"+str(ita.partef)+"·"+str(ita.totale)+"\n"
					i+=1
					myfile.write(txt)
		elif msg.what == 1001:#aggiungi pausa
			#print("1001 inserimento pausa")
			dm=msg.FindInt8("deltam")
			do=msg.FindInt8("deltao")
			#parte=msg.FindInt8("parte")
			#partef=msg.FindInt8("partef")
			#totale=msg.FindInt8("totale")
			#parteturno=(parte,partef,totale)
			dt = datetime.timedelta(hours=do,minutes=dm)
			n=msg.FindString("name")
			if self.listaturni.lv.CountItems()>0:
			#se prima riga ignora
				if self.listaturni.lv.CurrentSelection()>-1:
				#è selezionato qualcosa
					selit=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection())
					if type(selit)==BStringItem:
						#è un superitem pertanto vedo se aggiungere pausa alla fine
						it=self.listaturni.lv.CountItemsUnder(selit,True)
						#print("itemsUnder",it)
						
						if it>0:
							#è un superitem compresso pertanto aggiungo alla fine
							self.listaturni.lv.Expand(selit)
							lastund=self.listaturni.lv.ItemUnderAt(selit,True,it-1)
							i=lastund.fine #(or it-1)
							parte=lastund.partef
							if i+dt>datetime.timedelta(hours=24):
								partef=2
								totale=2
							else:
								partef=1
								totale=lastund.totale
							if parte>1:
								partef=2
							parteturno=(parte,partef,totale)
							sta=lastund.sta
							pau=PausItem(n,i,dt,sta,parteturno)
							self.tmpElem.append(pau)
							self.listaturni.lv.AddUnder(pau,selit)
							self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(pau),self.listaturni.lv.IndexOf(lastund))
					else:
						#è un elemento
						i=selit.fine
						sta=selit.sta
						parte=selit.partef
						if selit.fine+dt>datetime.timedelta(hours=24):
							partef=2
							totale=2
						else:
							partef=1
							totale=selit.totale
						if parte>1:
							partef=2
						parteturno=(parte,partef,totale)
						pau=PausItem(n,i,dt,sta,parteturno)
						self.tmpElem.append(pau)
						supit=self.listaturni.lv.Superitem(selit)
						self.listaturni.lv.AddUnder(pau,supit)
						self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(pau),self.listaturni.lv.IndexOf(selit))
				else:
				#fatto
				#non è selezionato nulla eventualmente si aggiunge alla fine
					litm=self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1)
					if type(litm) == BStringItem:
						#è un superitem
						it=self.listaturni.lv.CountItemsUnder(self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1),True)
						self.listaturni.lv.Expand(litm)
						#print("elementi sotto ultimo:", it)
						#controllo se è compresso
						if it>0:
							#posso aggiungere perché è presente un rigo del turno
							i=self.listaturni.lv.ItemUnderAt(litm,True,it-1).fine
							sta=self.listaturni.lv.ItemUnderAt(litm,True,it-1).sta
							parte=self.listaturni.lv.ItemUnderAt(litm,True,it-1).partef
							#totale=self.listaturni.lv.ItemUnderAt(litm,True,it-1).totale
							if i+dt>datetime.timedelta(hours=24):
								partef=2
								totale=2
							else:
								partef=1
								totale=self.listaturni.lv.ItemUnderAt(litm,True,it-1).totale
							if parte>1:
								partef=2
							parteturno=(parte,partef,totale)
							pau=PausItem(n,i,dt,sta,parteturno)
							self.tmpElem.append(pau)
							self.listaturni.lv.AddUnder(pau,litm)
							self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(pau),self.listaturni.lv.CountItems()-1)
						else:
							print("non posso aggiungere perché il turno è vuoto")
					else:
						i=litm.fine
						sta=litm.sta
						parte=litm.partef
						if litm.fine+dt>datetime.timedelta(hours=24):
							partef=2
							totale=2
						else:
							partef=1
							totale=litm.totale
						if parte>1:
							partef=2
						parteturno=(parte,partef,totale)
						pau=PausItem(n,i,dt,sta,parteturno)
						self.tmpElem.append(pau)
						titm=self.listaturni.lv.Superitem(litm)
						self.listaturni.lv.AddUnder(pau,titm)
						self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(pau),self.listaturni.lv.CountItems()-1)
		elif msg.what == 1012:
			#sposta su currentselection
			vet=self.tmpElem[-2]
			itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection())
			titm=self.listaturni.lv.Superitem(itm)
			self.listaturni.lv.AddUnder(vet,titm)
			self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection())
		elif msg.what == 1013:
			#sposta a fine elementi sotto superitem selezionato (o elemento di superitem selezionato)
			vet=self.tmpElem[-2]
			cit=msg.FindInt8("cit")
			itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection())
			r=self.listaturni.lv.AddUnder(vet,itm)
			self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection()+cit+2)
		elif msg.what == 1014:
			#sposta in fondo a elementi dell'ultimo superitem
			vet=self.tmpElem[-2]
			cit=msg.FindInt8("cit")
			itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1)
			titm=self.listaturni.lv.Superitem(itm)
			self.listaturni.lv.AddUnder(vet,titm)
			self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.IndexOf(titm)+cit+2)
		elif msg.what == 1333:#aggiungi treno
			# print("1333 inserimento treno con accessori")
			oip=msg.FindInt8("oip")
			# print("Step parziale")
			oit=msg.FindInt8("oit")
			oia=msg.FindInt8("oia")
			mip=msg.FindInt8("mip")
			mit=msg.FindInt8("mit")
			mia=msg.FindInt8("mia")
			ofp=msg.FindInt8("ofp")
			oft=msg.FindInt8("oft")
			ofa=msg.FindInt8("ofa")
			mfp=msg.FindInt8("mfp")
			mft=msg.FindInt8("mft")
			mfa=msg.FindInt8("mfa")
			cspp=msg.FindString("cspp")
			csap=msg.FindString("csap")
			cspt=msg.FindString("cspt")
			csat=msg.FindString("csat")
			cspa=msg.FindString("cspa")
			csaa=msg.FindString("csaa")
			nspp=msg.FindString("nspp")
			nsap=msg.FindString("nsap")
			nspt=msg.FindString("nspt")
			nsat=msg.FindString("nsat")
			nspa=msg.FindString("nspa")
			nsaa=msg.FindString("nsaa")
			ncond=msg.FindString("ncond")
			ccond=msg.FindInt8("ccond")
			materiale=msg.FindString("materiale")
			n=msg.FindString("name")
			parte=msg.FindInt8("parte")
			partef=msg.Findint8("partef")
			totale=msg.FindInt8("totale")
			codaccp=msg.FindInt8("codaccp")
			codacca=msg.FindInt8("codacca")
			ntap=msg.FindString("ntap")
			ntaa=msg.FindString("ntaa")
			
			dtp = datetime.timedelta(hours=oit,minutes=mit)
			dta = datetime.timedelta(hours=oft,minutes=mft)
			
			ap=False
			if ntap!=None:
				dtpp = datetime.timedelta(hours=oip,minutes=mip)
				ap=True
				accp=AccItem((ntap,codaccp),n,dtpp,dtp,(cspp,nspp),(cspp,nspp),materiale,(parte,parte,totale)) #cambiare parte/partef
				self.tmpElem.append(accp)
			aa=False
			if ntaa!=None:
				# print(ntaa,ofa,mfa)	
				dtaa = datetime.timedelta(hours=ofa,minutes=mfa)
				aa=True
				acca=AccItem((ntaa,codacca),n,dta,dtaa,(csaa,nsaa),(csaa,nsaa),materiale,(partef,partef,totale)) #cambiare parte/partef
				self.tmpElem.append(acca)
			
			
			if self.listaturni.lv.CountItems()>0:
				trn=TrenoItem(n,dtp,dta,(cspt,nspt),(csat,nsat),(ncond,ccond),materiale,(parte,totale))
				self.tmpElem.append(trn)
				if self.listaturni.lv.CurrentSelection()>-1:
					itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection())
					titm=self.listaturni.lv.Superitem(itm)
					if titm != None:
					#esiste superitem ovvero itm è un elemento del turno
						# print("step 1, selezionato elemento di turno")
						if ap:
							differ = dtpp - itm.fine
						else:
							differ = dtp - itm.fine
						if differ < datetime.timedelta(minutes=0):
							ask=BAlert('cle', "Ora accessori/partenza treno anteriore a fine rigo precedente", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
							self.alertWind.append(ask)
							ask.Go()
							return
						else:
							if differ > datetime.timedelta(minutes=0):
								if ap:
									# print("step 1.2 aggiunta pausa accessori treno e accessori in arrivo")
									#prepara BMessage(1001) e crea pausa
									dm=(differ.seconds % 3600) // 60
									do=differ.days * 24 + differ.seconds // 3600
									dt = datetime.timedelta(hours=do,minutes=dm)
									selit = itm
									i=selit.fine
									sta=selit.sta
									partep=selit.partef
									totalep=selit.totale
									if parte>1:
										partefp=2
									pau=PausItem("Pausa",i,dt,sta,(partep,partefp,totalep))
									self.tmpElem.append(pau)
									supit=self.listaturni.lv.Superitem(selit)
									self.listaturni.lv.AddUnder(pau,supit)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(pau),self.listaturni.lv.IndexOf(selit))
									self.listaturni.lv.AddUnder(accp,supit)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(accp),self.listaturni.lv.IndexOf(pau))
									self.listaturni.lv.AddUnder(trn,supit)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(trn),self.listaturni.lv.IndexOf(accp))
									if aa:
										self.listaturni.lv.AddUnder(acca,supit)
										self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(acca),self.listaturni.lv.IndexOf(trn))
								else:
									#aggiungi treno
									dm=(differ.seconds % 3600) // 60
									do=differ.days * 24 + differ.seconds // 3600
									dt = datetime.timedelta(hours=do,minutes=dm)
									selit = itm
									i=selit.fine
									sta=selit.sta
									partep=selit.partef
									totalep=selit.totale
									if parte>1:
										partefp=2
									pau=PausItem("Pausa",i,dt,sta,(partep,partefp,totalep))
									self.tmpElem.append(pau)
									supit=self.listaturni.lv.Superitem(selit)
									self.listaturni.lv.AddUnder(pau,supit)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(pau),self.listaturni.lv.IndexOf(selit))
									self.listaturni.lv.AddUnder(trn,supit)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(trn),self.listaturni.lv.IndexOf(pau))
									if aa:
										self.listaturni.lv.AddUnder(acca,supit)
										self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(acca),self.listaturni.lv.IndexOf(trn))
							elif differ == datetime.timedelta(minutes=0):
								# print("step 1.3")
								if ap:
								#aggiungi senza problemi accessori
									#aggiungi senza problemi treno
									#se aa aggiungi accessori in arrivo
									self.listaturni.lv.AddUnder(accp,titm)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(accp),self.listaturni.lv.CurrentSelection())
									self.listaturni.lv.AddUnder(trn,titm)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(trn),self.listaturni.lv.IndexOf(accp))#self.listaturni.lv.CurrentSelection())
									if aa:
										self.listaturni.lv.AddUnder(acca,titm)
										self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(acca),self.listaturni.lv.IndexOf(trn))#self.listaturni.lv.CountItems()-1)
								else:
									#aggiungi solo treno senza problemi
									self.listaturni.lv.AddUnder(trn,titm)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(trn),self.listaturni.lv.CurrentSelection())
									if aa:
										self.listaturni.lv.AddUnder(acca,titm)
										self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(acca),self.listaturni.lv.IndexOf(trn))
									#se aa aggiungi accessori in arrivo
					else:
						#Selezionato un superitem
						itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()) #this is the superitem
						self.listaturni.lv.Expand(itm)
						# print("step 2, selezionato turno")
						cit=self.listaturni.lv.CountItemsUnder(itm,True)
						if cit>0:
							#controlla ultima ora di fine
							otpf=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()+cit).fine
							# print("otpf:",otpf)
							if ap:
								differ = dtpp - otpf
							else:
								differ = dtp - otpf
							dm=(differ.seconds % 3600) // 60
							do=differ.days * 24 + differ.seconds // 3600
							dt = datetime.timedelta(hours=do,minutes=dm)
							if differ < datetime.timedelta(minutes=0):
								ask=BAlert('cle', "Ora accessori/partenza treno anteriore a fine dell'ultiam riga del turno", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
								self.alertWind.append(ask)
								ask.Go()
								return
							else:
								if differ > datetime.timedelta(minutes=0):
									selit=itm
									lastund=self.listaturni.lv.ItemUnderAt(selit,True,cit-1)
									i=lastund.fine #(or it-1)
									sta=lastund.sta
									partep=lastund.partef
									totalep=lastund.totale
									if parte>1:
										partefp=2
									pau=PausItem("Pausa",i,dt,sta,(partep,partefp,totalep))
									self.tmpElem.append(pau)
									self.listaturni.lv.AddUnder(pau,selit)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(pau),self.listaturni.lv.IndexOf(lastund))
									if ap:
										# print("step 2.2, aggiungi pausa, accessori partenza, treno e accessori arrivo")
										self.listaturni.lv.AddUnder(accp,selit)
										self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(accp),self.listaturni.lv.IndexOf(pau))
										self.listaturni.lv.AddUnder(trn,selit)
										self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(trn),self.listaturni.lv.IndexOf(accp))
										if aa:
											self.listaturni.lv.AddUnder(acca,selit)
											self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(acca),self.listaturni.lv.IndexOf(trn))
									else:
										# print("step 2.2, aggiungi pausa, treno e accessori arrivo")
										self.listaturni.lv.AddUnder(trn,selit)
										self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(trn),self.listaturni.lv.IndexOf(pau))
										if aa:
											self.listaturni.lv.AddUnder(acca,selit)
											self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(acca),self.listaturni.lv.IndexOf(trn))

								elif differ == datetime.timedelta(minutes=0):
									#aggiungi senza problemi
									# print("step 2.3")
									self.listaturni.lv.AddUnder(trn,itm)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(trn),self.listaturni.lv.CurrentSelection()+cit+1)
						else:
						#il superitem è vuoto
							self.listaturni.lv.AddUnder(trn,itm)
							self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(trn),self.listaturni.lv.CurrentSelection()+1)
					self.listaturni.lv.Select(self.listaturni.lv.CurrentSelection())

				else:
					#niente selezionato
					lastit=self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1)
					titm=self.listaturni.lv.Superitem(lastit)
					if titm != None:
						# print("step 3, niente selezionato, ultimo oggetto è elemento di turno")
						cit=self.listaturni.lv.CountItemsUnder(titm,True)
						i= lastit.fine
						sta=lastit.sta
						partep=lastit.partef
						totalep=lastit.totale
						if parte>1:
							partefp=2
						#last item is an element, not a superitem
						if ap:
							differ = dtpp - i
						else:
							differ = dtp - i
						dm=(differ.seconds % 3600) // 60
						do=differ.days * 24 + differ.seconds // 3600
						dt = datetime.timedelta(hours=do,minutes=dm)
						if differ < datetime.timedelta(minutes=0):
								ask=BAlert('cle', "Ora accessori/partenza treno anteriore a fine della ultimo rigo", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
								self.alertWind.append(ask)
								ask.Go()
								return
						else:
							if differ > datetime.timedelta(minutes=0):
								pau=PausItem("Pausa",i,dt,sta,(partep,partefp,totalep))
								self.tmpElem.append(pau)
								self.listaturni.lv.AddUnder(pau,titm)
								self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(pau),self.listaturni.lv.CountItems()-1)
								if ap:
									self.listaturni.lv.AddUnder(accp,titm)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(accp),self.listaturni.lv.CountItems()-1)
								self.listaturni.lv.AddUnder(trn,titm)
								self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(trn),self.listaturni.lv.CountItems()-1)
								if aa:
									self.listaturni.lv.AddUnder(acca,titm)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(acca),self.listaturni.lv.CountItems()-1)
							elif differ == datetime.timedelta(minutes=0):
								if ap:
									self.listaturni.lv.AddUnder(accp,titm)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(accp),self.listaturni.lv.CountItems()-1)
								self.listaturni.lv.AddUnder(trn,titm)
								self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(trn),self.listaturni.lv.CountItems()-1)
								if aa:
									self.listaturni.lv.AddUnder(acca,titm)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(acca),self.listaturni.lv.CountItems()-1)	
					else:
						# print("step 4, niente selezionato, ultimo oggetto è turno FV") # verificare che succede se questo e precedente sono collassati e non selezionati
						fvt=self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1)
						if ap:
							self.listaturni.lv.AddUnder(accp,fvt)
							self.listaturni.lv.AddUnder(trn,fvt)
							self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(trn),self.listaturni.lv.CountItems()-1)	
						else:
							self.listaturni.lv.AddUnder(trn,fvt)
						if aa:
							self.listaturni.lv.AddUnder(acca,fvt)
							self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(acca),self.listaturni.lv.CountItems()-1)	
		elif msg.what == 1002:#aggiungi vettura
			# print("1002 inserimento vettura")
			op=msg.FindInt8("oi")
			mp=msg.FindInt8("mi")
			oa=msg.FindInt8("of")
			ma=msg.FindInt8("mf")
			csp=msg.FindString("csp")
			csa=msg.FindString("csa")
			nsp=msg.FindString("nsp")
			nsa=msg.FindString("nsa")
			n=msg.FindString("name")
			parte=msg.FindInt8("parte")
			partef=msg.FindInt8("partef")
			totale=msg.FindInt8("totale")
			dtp = datetime.timedelta(hours=op,minutes=mp)
			dta = datetime.timedelta(hours=oa,minutes=ma)
			if self.listaturni.lv.CountItems()>0:
				vet=VettItem(n,dtp,dta,(csp,nsp),(csa,nsa),(parte,partef,totale))
				self.tmpElem.append(vet)
				if self.listaturni.lv.CurrentSelection()>-1:
					itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection())
					titm=self.listaturni.lv.Superitem(itm)
					if titm != None: 
					#esiste superitem ovvero sono un elemento del turno
						# print("step 1, selezionato elemento di turno")
						print(vet.parte,itm.partef)
						if vet.parte>itm.partef:
							print("giorno dopo")
							differ=dtp+datetime.timedelta(hours=24)-itm.fine
						else:
							print("stesso giorno")
							differ = dtp - itm.fine
						######################################################################################
						if self.checkpreviouscompatibility(itm,vet): #TODO: controllare se parte attuale è maggiore di partef item precedente
							if differ > datetime.timedelta(minutes=0):
									# print("step 1.2")
									#prepara BMessage(1001) e crea pausa
									minutes=(differ.seconds % 3600) // 60
									hours=differ.days * 24 + differ.seconds // 3600
									mex=BMessage(1001)
									mex.AddInt8("deltam",minutes)
									mex.AddInt8("deltao",hours)
									#mex.AddInt8("parte",parte)
									#mex.AddInt8("totale",totale)
									mex.AddString("name","Pausa")
									be_app.WindowAt(0).PostMessage(mex)
									
									mx2=BMessage(1012)
									be_app.WindowAt(0).PostMessage(mx2)
							elif differ == datetime.timedelta(minutes=0):
									#aggiungi senza problemi
									# print("step 1.3")
									self.listaturni.lv.AddUnder(vet,titm)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection())
						else:
							ask=BAlert('cle', "1 Mancata corrispondenza ora partenza vettura e rigo precedente", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
							self.alertWind.append(ask)
							ask.Go()				
					else:
						#Selezionato un superitem
						itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()) #this is the superitem
						self.listaturni.lv.Expand(itm)
						# print("step 2, selezionato turno")
						cit=self.listaturni.lv.CountItemsUnder(itm,True)
						if cit>0:
							#controlla ultima ora di fine
							otpf=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()+cit).fine
							print(vet.parte,self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()+cit).partef)
							if vet.parte>self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()+cit).partef:
								print("giorno dopo")
								differ=dtp+datetime.timedelta(hours=24)-otpf
							else:
								print("stesso giorno")
								differ = dtp - otpf
							proceed=self.checkpreviouscompatibility(self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()+cit),vet)
							if proceed:
								if differ > datetime.timedelta(minutes=0):
									# print("step 2.2")
									#prepara BMessage(1001) e crea pausa
									minutes=(differ.seconds % 3600) // 60
									hours=differ.days * 24 + differ.seconds // 3600
									mex=BMessage(1001)
									mex.AddInt8("deltam",minutes)
									mex.AddInt8("deltao",hours)
									#mex.AddInt8("parte",parte)
									#mex.AddInt8("totale",totale)
									mex.AddString("name","Pausa")
									be_app.WindowAt(0).PostMessage(mex)
									
									mx2=BMessage(1013)
									mx2.AddInt8("cit",cit)
									be_app.WindowAt(0).PostMessage(mx2)
								elif differ == datetime.timedelta(minutes=0):
									#aggiungi senza problemi
									# print("step 2.3")
									self.listaturni.lv.AddUnder(vet,itm)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection()+cit+1)
							else:
								ask=BAlert('cle', "2 Mancata corrispondenza ora partenza vettura e rigo precedente", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
								self.alertWind.append(ask)
								ask.Go()
						else:
							self.listaturni.lv.AddUnder(vet,itm)
							self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection()+1)
					self.listaturni.lv.Select(self.listaturni.lv.CurrentSelection())
				else:
					lastit=self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1)
					titm=self.listaturni.lv.Superitem(lastit)
					if titm != None:
						# print("step 3, niente selezionato, ultimo oggetto è elemento di turno")
						#last item is an element, not a superitem
						cit=self.listaturni.lv.CountItemsUnder(titm,True)
						#check if otpf è > di vet.inizio
						proceed=self.checkpreviouscompatibility(lastit,vet)
						if proceed:
							print(vet.parte,lastit.partef)
							if vet.parte>lastit.partef:
								print("giorno dopo")
								differ=vet.inizio+datetime.timedelta(hours=24)-lastit.fine
							else:
								print("stesso giorno")
								differ=vet.inizio-lastit.fine
							if differ > datetime.timedelta(minutes=0):
								# print("step 3.1")
								#aggiungi pausa
								minutes=(differ.seconds % 3600) // 60
								hours=differ.days * 24 + differ.seconds // 3600
								mex=BMessage(1001)
								mex.AddInt8("deltam",minutes)
								mex.AddInt8("deltao",hours)
								#mex.AddInt8("parte",parte)
								#mex.AddInt8("totale",totale)
								mex.AddString("name","Pausa")
								be_app.WindowAt(0).PostMessage(mex)
									
								mx2=BMessage(1014)
								mx2.AddInt8("cit",cit)
								be_app.WindowAt(0).PostMessage(mx2)
							elif differ == datetime.timedelta(minutes=0):
								#agiungi senza prolemi
								# print("step 3.2")
								self.listaturni.lv.AddUnder(vet,titm)
								con=self.listaturni.lv.CountItemsUnder(titm,True)
								self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.IndexOf(vet)+con-1)
						else:
							ask=BAlert('cle', "Mancata corrispondenza ora partenza vettura e rigo precedente", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
							self.alertWind.append(ask)
							ask.Go()
					else:
						# print("step 4, niente selezionato, ultimo oggetto è turno") # verificare che succede se questo e precedente sono collassati e non selezionati
						self.listaturni.lv.AddUnder(vet,self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1))
		elif msg.what == 1003:#aggiungi accessori
			# print("1003 inserimento accessori")
			op=msg.FindInt8("oi")
			mp=msg.FindInt8("mi")
			oa=msg.FindInt8("of")
			ma=msg.FindInt8("mf")
			csp=msg.FindString("csp")
			csa=msg.FindString("csa")
			nsp=msg.FindString("nsp")
			nsa=msg.FindString("nsa")
			nta=msg.FindString("nta")
			codacc=msg.FindInt8("codacc")
			materiale=msg.FindString("materiale")
			parte=msg.FindInt8("parte")
			partef=msg.FindInt8("partef")
			totale=msg.FindInt8("totale")
			n=msg.FindString("name")
			dtp = datetime.timedelta(hours=op,minutes=mp)
			dta = datetime.timedelta(hours=oa,minutes=ma)
			if self.listaturni.lv.CountItems()>0:
				acc=AccItem((nta,codacc),n,dtp,dta,(csp,nsp),(csa,nsa),materiale,(parte,partef,totale))
				acc.Details()
				self.tmpElem.append(acc)
				if self.listaturni.lv.CurrentSelection()>-1:
					itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection())
					titm=self.listaturni.lv.Superitem(itm)
					if titm != None: 
					#esiste superitem ovvero sono un elemento del turno
						# print("step 1, selezionato elemento di turno")
						if acc.parte>itm.partef:
							print("giorno dopo")
							differ=dtp+datetime.timedelta(hours=24)-itm.fine
						else:
							print("stesso giorno")
							differ = dtp - itm.fine
						if self.checkpreviouscompatibility(itm,acc):
							if differ > datetime.timedelta(minutes=0):
									# print("step 1.2")
									#prepara BMessage(1001) e crea pausa
									minutes=(differ.seconds % 3600) // 60
									hours=differ.days * 24 + differ.seconds // 3600
									mex=BMessage(1001)
									mex.AddInt8("deltam",minutes)
									mex.AddInt8("deltao",hours)
									#mex.AddInt8("parte",parte)
									#mex.AddInt8("totale",totale)
									mex.AddString("name","Pausa")
									be_app.WindowAt(0).PostMessage(mex)
									
									mx2=BMessage(1012)
									be_app.WindowAt(0).PostMessage(mx2)
							elif differ == datetime.timedelta(minutes=0):
									#aggiungi senza problemi
									# print("step 1.3")
									self.listaturni.lv.AddUnder(acc,titm)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(acc),self.listaturni.lv.CurrentSelection())
						else:
							ask=BAlert('cle', "Mancata corrispondenza ora inizio accessori e rigo precedente", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
							self.alertWind.append(ask)
							ask.Go()				
					else:
						#Selezionato un superitem
						itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()) #this is the superitem
						self.listaturni.lv.Expand(itm)
						# print("step 2, selezionato turno")
						cit=self.listaturni.lv.CountItemsUnder(itm,True)
						if cit>0:
							#controlla ultima ora di fine
							otpf=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()+cit).fine
							if acc.parte>itm.partef:
								print("giorno dopo")
								differ=dtp+datetime.timedelta(hours=24)-otpf
							else:
								print("stesso giorno")
								differ = dtp - otpf
							proceed=self.checkpreviouscompatibility(self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()+cit),acc)
							if proceed:
								if differ > datetime.timedelta(minutes=0):
									# print("step 2.2")
									#prepara BMessage(1001) e crea pausa
									minutes=(differ.seconds % 3600) // 60
									hours=differ.days * 24 + differ.seconds // 3600
									mex=BMessage(1001)
									mex.AddInt8("deltam",minutes)
									mex.AddInt8("deltao",hours)
									#mex.AddInt8("parte",parte)
									#mex.AddInt8("totale",totale)
									mex.AddString("name","Pausa")
									be_app.WindowAt(0).PostMessage(mex)
									
									mx2=BMessage(1013)
									mx2.AddInt8("cit",cit)
									be_app.WindowAt(0).PostMessage(mx2)
								elif differ == datetime.timedelta(minutes=0):
									#aggiungi senza problemi
									# print("step 2.3")
									self.listaturni.lv.AddUnder(acc,itm)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(acc),self.listaturni.lv.CurrentSelection()+cit+1)
							else:
								ask=BAlert('cle', "Mancata corrispondenza ora inizio accessori e rigo precedente", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
								self.alertWind.append(ask)
								ask.Go()
						else:
							self.listaturni.lv.AddUnder(acc,itm)
							self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(acc),self.listaturni.lv.CurrentSelection()+1)
					self.listaturni.lv.Select(self.listaturni.lv.CurrentSelection())
				else:
					lastit=self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1)
					titm=self.listaturni.lv.Superitem(lastit)
					if titm != None:
						# print("step 3, niente selezionato, ultimo oggetto è elemento di turno")
						#last item is an element, not a superitem
						cit=self.listaturni.lv.CountItemsUnder(titm,True)
						# print("elementi sotto superitem",cit)
						#check if otpf è > di acc.inizio
						proceed=self.checkpreviouscompatibility(lastit,acc)
						# print("confronto con:")
						#lastit.Details()
						if proceed:
							if acc.parte>itm.partef:
								print("giorno dopo")
								differ=acc.inizio+datetime.timedelta(hours=24)-lastit.fine
							else:
								print("stesso giorno")
								differ=acc.inizio-lastit.fine
							if differ > datetime.timedelta(minutes=0):
								# print("step 3.1")
								#aggiungi pausa
								minutes=(differ.seconds % 3600) // 60
								hours=differ.days * 24 + differ.seconds // 3600
								mex=BMessage(1001)
								mex.AddInt8("deltam",minutes)
								mex.AddInt8("deltao",hours)
								#mex.AddInt8("parte",parte)
								#mex.AddInt8("totale",totale)
								mex.AddString("name","Pausa")
								be_app.WindowAt(0).PostMessage(mex)
									
								mx2=BMessage(1014)
								mx2.AddInt8("cit",cit)
								be_app.WindowAt(0).PostMessage(mx2)
							elif differ == datetime.timedelta(minutes=0):
								#agiungi senza prolemi
								# print("step 3.2")
								self.listaturni.lv.AddUnder(acc,titm)
								con=self.listaturni.lv.CountItemsUnder(titm,True)
								self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(acc),self.listaturni.lv.IndexOf(acc)+con-1)
						else:
							ask=BAlert('cle', "Mancata corrispondenza ora inizio accessori e rigo precedente", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
							self.alertWind.append(ask)
							ask.Go()
					else:
						# print("step 4, niente selezionato, ultimo oggetto è turno") # verificare che succede se questo e precedente sono collassati e non selezionati
						self.listaturni.lv.AddUnder(acc,self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1))
			glock=0
		return BWindow.MessageReceived(self,msg)
	def unisci_condotte(self,outt):
		i=0
		o=len(outt)
		if len(outt)>1:
			while i<o:
				self.z=i+1
				while z+i<o:
					if outt[i].fine == outt[self.z].inizio:
						self.mergethem(outt,i,self.z) #unisce i due elementi creandone uno nuovo, poi lo mette al posto di outt[i] (sostituendolo)
						o=len(outt)
					elif (outt[self.z].inizio-outt[i].fine<datetime.timedelta(minutes=15)) and (outt[self.z].stp == outt[i].sta):
						self.mergethem(outt,i,self.z)
						o=len(outt)
					z+=1
				i+=1
		return outt
	def mergethem(self,list,i1,i2):
		sost=list[i1]
		sost.partef=list[i2].partef
		sost.totale=list[i2].totale
		sost.fine=list[i2].fine
		sost.sta=list[i2].sta
		sost.label=("Condotta"+"  "+sost.name+"  "+sost.stp[0]+"  "+str(sost.inizio)+"  "+str(sost.parte)+"/"+str(sost.totale)+"  "+sost.sta[0]+"  "+str(sost.fine)+"  "+str(sost.partef)+"/"+str(sost.totale)+"  "+sost.ncond+"  "+sost.materiale)
		del list[i2]
		self.z-=1
	def estrai_vett(self,s):
		cmd=s.split("·")
		hmp=cmd[1].split(":")
		hma=cmd[2].split(":")
		for stz in cod_stazioni:
			if stz[0] == cmd[3]:
				nstp=stz[1]
			if stz[0] == cmd[4]:
				nsta=stz[1]
		stp=(cmd[3],nstp)
		sta=(cmd[4],nsta)
		i=datetime.timedelta(hours=int(hmp[0]),minutes=int(hmp[1]))
		f=datetime.timedelta(hours=int(hma[0]),minutes=int(hma[1]))
		return VettItem(cmd[0],i,f,stp,sta,(cmd[5],cmd[6],cmd[7]))
	def estrai_acc(self,s):
		cmd=s.split("·")
		ta=(cmd[0],cmd[1])
		hmp=cmd[3].split(":")
		hma=cmd[4].split(":")
		i=datetime.timedelta(hours=int(hmp[0]),minutes=int(hmp[1]))
		f=datetime.timedelta(hours=int(hma[0]),minutes=int(hma[1]))
		for stz in cod_stazioni:
			if stz[0] == cmd[5]:
				nstp=stz[1]
			if stz[0] == cmd[6]:
				nsta=stz[1]
		stp=(cmd[5],nstp)
		sta=(cmd[6],nsta)
		return AccItem(ta,cmd[2],i,f,stp,sta,cmd[7],(cmd[8],cmd[9],cmd[10]))
	def estrai_trn(self,s):
		cmd=s.split("·")
		hmp=cmd[1].split(":")
		hma=cmd[2].split(":")
		i=datetime.timedelta(hours=int(hmp[0]),minutes=int(hmp[1]))
		f=datetime.timedelta(hours=int(hma[0]),minutes=int(hma[1]))
		for stz in cod_stazioni:
			if stz[0] == cmd[3]:
				nstp=stz[1]
			if stz[0] == cmd[4]:
				nsta=stz[1]
		stp=(cmd[3],nstp)
		sta=(cmd[4],nsta)
		for cond in tipocond:
			if cond[1]==int(cmd[5]):
				rcond=(cond[0],cond[1])
				break
		return TrenoItem(cmd[0],i,f,stp,sta,rcond,cmd[6],(cmd[7],cmd[8],cmd[9]))
	def estrai_pau(self,s):
		cmd=s.split("·")
		hmp=cmd[1].split(":")
		hma=cmd[2].split(":")
		for stz in cod_stazioni:
			if stz[0] == cmd[3]:
				nstp=stz[1]
		stp=(cmd[3],nstp)
		sta=(cmd[3],nstp)
		i=datetime.timedelta(hours=int(hmp[0]),minutes=int(hmp[1]))
		f=datetime.timedelta(hours=int(hma[0]),minutes=int(hma[1]))
		dt=f-i
		return PausItem(cmd[0],i,dt,stp,(cmd[4],cmd[5],cmd[6]))
		
	def checkpreviouscompatibility(self,prev,ittem):
		ret = True
		if ittem.parte<=prev.partef:
			if prev.fine>ittem.inizio:
				ret=False
		return ret
	def QuitRequested(self):
		wnum = be_app.CountWindows()
		if wnum>1:
			if len(self.tmpWind)>0:
				for wind in self.tmpWind:
					wind.Lock()
					wind.Quit()
		return BWindow.QuitRequested(self)

class EstrazTreni(BWindow):
	def __init__(self,sumtreni):
		BWindow.__init__(self, BRect(50,100,800,600), "Estrazione turni", window_type.B_TITLED_WINDOW, B_QUIT_ON_WINDOW_CLOSE) #B_NOT_RESIZABLE | B_QUIT_ON_WINDOW_CLOSE)#B_MODAL_WINDOW
		bounds=self.Bounds()
		self.bckgnd = BView(self.Bounds(), "background_View", 8, 20000000)
		self.bckgnd.SetResizingMode(B_FOLLOW_ALL_SIDES)
		bckgnd_bounds=self.bckgnd.Bounds()
		self.AddChild(self.bckgnd,None)
		self.listatreni = Scrolltrains(BRect(4 , 4, bounds.Width()/3- 18, bounds.Height() - 4 ), 'Scrolltrains')
		self.listafv = ScrollFv(BRect(bounds.Width()/3 , 4, bounds.Width()*2/3- 18, bounds.Height() - 4 ), 'ScrollFVs')
		self.listael = ScrollElement(BRect(bounds.Width()*2/3 , 4, bounds.Width()- 18, bounds.Height() - 4 ), 'Scrollelements')
		self.bckgnd.AddChild(self.listatreni.sv,None)
		self.bckgnd.AddChild(self.listafv.sv,None)
		self.bckgnd.AddChild(self.listael.sv,None)
		self.sumtreni=sumtreni
		for k in self.sumtreni.keys():
			self.listatreni.lv.AddItem(BStringItem(str(k)))
		self.fvs=[]
		#for k in self.sumtreni.Keys():
	def ReSet(self,sumtreni):
		if self.listatreni.lv.CountItems()>0:
			self.listatreni.lv.RemoveItems(0,self.listatreni.lv.CountItems())
		if self.listafv.lv.CountItems()>0:
			self.listafv.lv.RemoveItems(0,self.listafv.lv.CountItems())
		if self.listael.lv.CountItems()>0:
			self.listael.lv.RemoveItems(0,self.listael.lv.CountItems())
		for k in self.sumtreni.keys():
			self.listatreni.lv.AddItem(BStringItem(str(k)))
		self.sumtreni=sumtreni
		for k in self.sumtreni.keys():
			self.listatreni.lv.AddItem(BStringItem(str(k)))
	def MessageReceived(self, msg):
		if msg.what==774:
			if self.listafv.lv.CountItems()>0:
				self.listafv.lv.RemoveItems(0,self.listafv.lv.CountItems())
			if self.listael.lv.CountItems()>0:
				self.listael.lv.RemoveItems(0,self.listael.lv.CountItems())
			self.fvs = self.sumtreni[int(self.listatreni.lv.ItemAt(self.listatreni.lv.CurrentSelection()).Text())]
			for fv in self.fvs:
				if self.listafv.lv.CountItems()>0:
					doit=True
					for items in self.listafv.lv.Items():
						if items.Text()==str(fv[0]):
							doit = False
							break
					if doit:
						self.listafv.lv.AddItem(BStringItem(str(fv[0])))
				else:
					self.listafv.lv.AddItem(BStringItem(str(fv[0])))
		elif msg.what == 884:
			if self.listael.lv.CountItems()>0:
				self.listael.lv.RemoveItems(0,self.listael.lv.CountItems())
			print(self.fvs)
			for x in self.fvs:
				if str(x[0])==self.listafv.lv.ItemAt(self.listafv.lv.CurrentSelection()).Text():
					self.listael.lv.AddItem(x[1])
				 
			#ss	print([x for y in self.fvs for x in y])
			#popola listael.lv
		elif msg.what == 53:
			pass
			#apri finestra dettagli elemento
	def QuitRequested(self):
		self.Hide()

class ScrollElement:
	HiWhat = 53
	SectionSelection = 54
	def __init__(self, rect, name):
		self.lv = BListView(rect, name, list_view_type.B_SINGLE_SELECTION_LIST)#B_MULTIPLE_SELECTION_LIST
		self.lv.SetResizingMode(B_FOLLOW_TOP_BOTTOM)
		self.lv.SetSelectionMessage(BMessage(self.SectionSelection))
		self.lv.SetInvocationMessage(BMessage(self.HiWhat))
		self.sv = BScrollView(name, self.lv,B_FOLLOW_NONE,0,False,True,border_style.B_FANCY_BORDER)
		self.sv.SetResizingMode(B_FOLLOW_TOP_BOTTOM)

class ScrollFv:
	HiWhat = 883
	SectionSelection = 884
	def __init__(self, rect, name):
		self.lv = BListView(rect, name, list_view_type.B_SINGLE_SELECTION_LIST)#B_MULTIPLE_SELECTION_LIST
		self.lv.SetResizingMode(B_FOLLOW_TOP_BOTTOM)
		self.lv.SetSelectionMessage(BMessage(self.SectionSelection))
		self.lv.SetInvocationMessage(BMessage(self.HiWhat))
		self.sv = BScrollView(name, self.lv,B_FOLLOW_NONE,0,False,True,border_style.B_FANCY_BORDER)
		self.sv.SetResizingMode(B_FOLLOW_TOP_BOTTOM)

class Scrolltrains:
	HiWhat = 773
	SectionSelection = 774
	def __init__(self, rect, name):
		self.lv = BListView(rect, name, list_view_type.B_SINGLE_SELECTION_LIST)#B_MULTIPLE_SELECTION_LIST
		self.lv.SetResizingMode(B_FOLLOW_TOP_BOTTOM)
		self.lv.SetSelectionMessage(BMessage(self.SectionSelection))
		self.lv.SetInvocationMessage(BMessage(self.HiWhat))
		self.sv = BScrollView(name, self.lv,B_FOLLOW_NONE,0,False,True,border_style.B_FANCY_BORDER)
		self.sv.SetResizingMode(B_FOLLOW_TOP_BOTTOM)


class TrenoItem(BListItem):
	# (n,dtp,dta,(csp,nsp),(csa,nsa),(ncond,ccond),materiale,(parte,totale))
	def __init__(self,name,inizio,fine,stp,sta,tipocond,materiale,parteturno):
		fon=BFont()
		self.materiale = materiale
		self.parte=parteturno[0]
		self.partef=parteturno[1]
		self.totale=parteturno[2]
		self.font_height_value=font_height()
		fon.GetHeight(self.font_height_value)
		self.ccond=tipocond[1]
		self.ncond=tipocond[0]
		self.name=name
		self.inizio=inizio
		self.fine=fine
		self.stp=stp
		self.sta=sta
		mi=(inizio.seconds % 3600) // 60
		oi=inizio.days * 24 + inizio.seconds // 3600
		of=fine.days * 24 + fine.seconds // 3600
		mf=(fine.seconds % 3600) // 60
		self.iout=str(oi)+":"+str(mi)
		self.fout=str(of)+":"+str(mf)
		self.label=("Condotta"+"  "+self.name+"  "+stp[0]+"  "+str(self.inizio)+"  "+str(parteturno[0])+"/"+str(parteturno[2])+"  "+sta[0]+"  "+str(self.fine)+"  "+str(parteturno[1])+"/"+str(parteturno[2])+"  "+self.ncond+"  "+self.materiale)
		BListItem.__init__(self)
	def Details(self):
		print(self.label)
	def DrawItem(self, owner, frame, complete):
		owner.SetHighColor(255,255,0,255)
		owner.SetLowColor(0,0,0,0)
		if self.IsSelected() or complete:
			owner.SetHighColor(200,200,200,255)
			owner.SetLowColor(200,200,200,255)
		owner.FillRect(frame)
		owner.SetHighColor(0,0,0,0)
		owner.MovePenTo(frame.left+5,frame.bottom-self.font_height_value.descent)
		owner.DrawString("Condotta",None)
		owner.MovePenTo(frame.left+250,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.name,None)
		owner.MovePenTo(frame.left+300,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.stp[0],None)
		owner.MovePenTo(frame.left+350,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.sta[0],None)
		owner.MovePenTo(frame.left+400,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.iout,None)
		owner.MovePenTo(frame.left+450,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.fout,None)
		owner.MovePenTo(frame.left+500,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.ncond,None)
		owner.MovePenTo(frame.left+600,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.materiale,None)
		owner.MovePenTo(frame.left+700,frame.bottom-self.font_height_value.descent)
		owner.DrawString(str(self.parte)+"/"+str(self.totale),None)
		owner.SetLowColor(255,255,255,255)
class AccItem(BListItem):
# AccItem((nta,codacc),n,dtp,dta,(csp,nsp),(csa,nsa),(nta,codacc),materiale,(parte,totale))
	def __init__(self,ta,name,inizio,fine,stp,sta,materiale,parteturno):
		self.name=name
		#self.label=self.name
		self.nta=ta[0]
		self.cta=ta[1]
		self.codacc=ta[1]
		fon=BFont()
		self.stp=stp
		self.sta=sta
		self.materiale = materiale
		self.parte=parteturno[0]
		self.partef=parteturno[1]
		self.totale=parteturno[2]
		self.font_height_value=font_height()
		fon.GetHeight(self.font_height_value)
		self.inizio=inizio
		self.fine=fine
		mi=(inizio.seconds % 3600) // 60
		oi=inizio.days * 24 + inizio.seconds // 3600
		of=fine.days * 24 + fine.seconds // 3600
		mf=(fine.seconds % 3600) // 60
		self.iout=str(oi)+":"+str(mi)
		self.fout=str(of)+":"+str(mf)
		self.label=(self.nta+"  "+self.name+"  "+stp[0]+"  "+str(self.inizio)+"  "+str(parteturno[0])+"/"+str(parteturno[2])+"  "+sta[0]+"  "+str(self.fine)+"  "+str(parteturno[1])+"/"+str(parteturno[2])+"  "+self.materiale)
		BListItem.__init__(self)
	def Details(self):
		print(self.label)
	def DrawItem(self, owner, frame, complete):
		#owner.SetHighColor(200,255,255,255)
		#owner.SetLowColor(0,0,0,0)
		if self.IsSelected() or complete:
			owner.SetHighColor(200,200,200,255)
			owner.SetLowColor(200,200,200,255)
			owner.FillRect(frame)
		owner.SetHighColor(0,0,0,0)
		owner.MovePenTo(frame.left+5,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.nta,None)
		owner.MovePenTo(frame.left+250,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.name,None)
		owner.MovePenTo(frame.left+300,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.stp[0],None)
		owner.MovePenTo(frame.left+350,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.sta[0],None)
		owner.MovePenTo(frame.left+400,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.iout,None)
		owner.MovePenTo(frame.left+450,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.fout,None)
		owner.MovePenTo(frame.left+600,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.materiale,None)
		owner.MovePenTo(frame.left+700,frame.bottom-self.font_height_value.descent)
		owner.DrawString(str(self.parte)+"/"+str(self.totale),None)
		owner.SetLowColor(255,255,255,255)
class VettItem(BListItem):
	def __init__(self,name,inizio,fine,stp,sta,parteturno):
		self.name=name
		#self.label=self.name
		fon=BFont()
		self.stp=stp
		self.sta=sta
		self.font_height_value=font_height()
		fon.GetHeight(self.font_height_value)
		self.inizio=inizio
		self.fine=fine
		self.parte=parteturno[0]
		self.totale=parteturno[2]
		self.partef=parteturno[1]
		mi=(inizio.seconds % 3600) // 60
		oi=inizio.days * 24 + inizio.seconds // 3600
		of=fine.days * 24 + fine.seconds // 3600
		mf=(fine.seconds % 3600) // 60
		self.iout=str(oi)+":"+str(mi)
		self.fout=str(of)+":"+str(mf)
		self.label=("vettura"+"  "+self.name+"  "+stp[0]+"  "+str(self.inizio)+"  "+str(parteturno[0])+"/"+str(parteturno[2])+"  "+sta[0]+"  "+str(self.fine)+"  "+str(parteturno[1])+"/"+str(parteturno[2]))
		BListItem.__init__(self)
	def Details(self):
		print(self.label)
	def DrawItem(self, owner, frame, complete):
		owner.SetHighColor(200,255,255,255)
		owner.SetLowColor(0,0,0,0)
		if self.IsSelected() or complete:
			owner.SetHighColor(200,200,200,255)
			owner.SetLowColor(200,200,200,255)
		owner.FillRect(frame)
		owner.SetHighColor(0,0,0,0)
		owner.MovePenTo(frame.left+5,frame.bottom-self.font_height_value.descent)
		owner.DrawString("Vettura",None)
		owner.MovePenTo(frame.left+250,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.name,None)
		owner.MovePenTo(frame.left+300,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.stp[0],None)
		owner.MovePenTo(frame.left+350,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.sta[0],None)
		owner.MovePenTo(frame.left+400,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.iout,None)
		owner.MovePenTo(frame.left+450,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.fout,None)
		owner.MovePenTo(frame.left+700,frame.bottom-self.font_height_value.descent)
		owner.DrawString(str(self.parte)+"/"+str(self.totale),None)
class PausItem(BListItem):
	def __init__(self,name,inizio,deltat,dove,parteturno):
		self.name=name
		fon=BFont()
		self.stp=dove
		self.sta=dove
		self.parte=parteturno[0]
		self.totale=parteturno[2]
		self.partef=parteturno[1]
		if self.parte==None:
			self.parte=1
		if self.totale==None:
			self.totale=1
		if self.partef==None:
			self.partef=1
		#todo: recuperare parteturno rigo precedente se 2 assegnarlo a quello attuale
		self.font_height_value=font_height()
		fon.GetHeight(self.font_height_value)
		self.inizio=inizio
		self.fine=inizio + deltat
		if self.fine>datetime.timedelta(hours=24):
			self.fine=self.fine-datetime.timedelta(hours=24)
			self.partef=2
			self.totale=2
		mi=(inizio.seconds % 3600) // 60
		oi=inizio.days * 24 + inizio.seconds // 3600
		of=self.fine.days * 24 + self.fine.seconds // 3600
		mf=(self.fine.seconds % 3600) // 60
		self.iout=str(oi)+":"+str(mi)
		self.fout=str(of)+":"+str(mf)
		self.label=(self.name+"        "+dove[0]+"  "+str(self.inizio)+"  "+str(self.parte)+"/"+str(self.totale)+"  "+dove[0]+"  "+str(self.fine))#+"  "+str(parteturno[1])+"/"+str(parteturno[2]))
		BListItem.__init__(self)
	def Details(self):
		print(self.label)
	def DrawItem(self, owner, frame, complete):
		if self.IsSelected() or complete:
			owner.SetHighColor(200,200,200,255)
			owner.SetLowColor(200,200,200,255)
			owner.FillRect(frame)
		owner.SetHighColor(0,0,0,0)
		owner.MovePenTo(frame.left+5,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.name,None)
		owner.MovePenTo(frame.left+300,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.stp[0],None)
		owner.MovePenTo(frame.left+350,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.sta[0],None)
		owner.MovePenTo(frame.left+400,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.iout,None)
		owner.MovePenTo(frame.left+450,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.fout,None)
		owner.MovePenTo(frame.left+700,frame.bottom-self.font_height_value.descent)
		owner.DrawString(str(self.parte)+"/"+str(self.totale),None)
		#if not self.consistent:
		#	sp=BPoint(3,frame.bottom-((frame.bottom-frame.top)/2))
		#	ep=BPoint(frame.right-3,frame.bottom-(frame.bottom-frame.top)/2)
		#	owner.StrokeLine(sp,ep)
		owner.SetLowColor(255,255,255,255)

class ScrollView:
	HiWhat = 53 #Doppioclick
	SectionSelection = 54

	def __init__(self, rect, name):
		self.lv = BOutlineListView(rect, name, list_view_type.B_SINGLE_SELECTION_LIST)#B_MULTIPLE_SELECTION_LIST
		self.lv.SetResizingMode(B_FOLLOW_TOP_BOTTOM)
		self.lv.SetSelectionMessage(BMessage(self.SectionSelection))
		self.lv.SetInvocationMessage(BMessage(self.HiWhat))
		self.sv = BScrollView(name, self.lv,B_FOLLOW_NONE,0,False,True,border_style.B_FANCY_BORDER)
		self.sv.SetResizingMode(B_FOLLOW_TOP_BOTTOM)

class App(BApplication):
	def __init__(self):
		BApplication.__init__(self, "application/x-python-Scripturn")
		self.autoload=""
	def ReadyToRun(self):
		self.window = MainWindow(self.autoload)
		self.window.Show()
	def ArgvReceived(self,num,args):
		#with open('testargvreceived.txt', 'w') as writer:
		#	writer.write(str(args))
		#print("numero argomenti:",num)
		#self.ask=BAlert('cle', "numero argomenti:"+str(num), 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
		#self.ask.Go()
		self.autoload=args[-1]# argvReceived is executed before readytorun, we pass the last argument
		
		
		#print("argomenti:",args)
	def RefsReceived(self, msg):
		if msg.what == B_REFS_RECEIVED:
			i = 0
			while True:
				try:
					bitul=False
					er = entry_ref()
					rito=msg.FindRef("refs", i,er)
					entry = BEntry(er,True)
					# p=BPath()
					# entry.GetPath(p)
					#print(rito,er,p.Path(),entry.Exists())
					if entry.Exists():
						# print("dentro entry.exists()")
						percors=BPath()
						entry.GetPath(percors)
						ofpmsg=BMessage(45371)
						ofpmsg.AddString("path",percors.Path())
						be_app.WindowAt(0).PostMessage(ofpmsg)
					else:
						break
				except:
					#er = None
					bitul=True
				# print(er)
				#if er is None:
				if bitul:
					# print("rompo loop")
					break
				i+=1
			# print("terminata ricerca refs")
		BApplication.RefsReceived(self,msg)
	def MessageReceived(self,msg):
		if msg.what == B_SAVE_REQUESTED:
			e = msg.FindString("name")
			messaggio = BMessage(54173)
			messaggio.AddString("name",e)
			be_app.WindowAt(0).PostMessage(messaggio)
			return
		elif msg.what == B_ARGV_RECEIVED:
			self.asku=BAlert('cle', "ricevuto argv", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
			self.asku.Go()
		BApplication.MessageReceived(self,msg)

#	def Pulse(self):
#		if self.window.enabletimer:
#			be_app.WindowAt(0).PostMessage(BMessage(66))



def main():
	global be_app
	#with open('test.txt', 'w') as writer:
	#	writer.write(str(sys.argv))
	#print(sys.argv)
	be_app = App()
	be_app.Run()
	
 
if __name__ == "__main__":
    main()
