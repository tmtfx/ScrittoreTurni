#!/boot/system/bin/python3
from Be import BApplication, BWindow, BView, BMenu,BMenuBar, BMenuItem, BSeparatorItem, BMessage, window_type, B_NOT_RESIZABLE, B_CLOSE_ON_ESCAPE, B_QUIT_ON_WINDOW_CLOSE
from Be import BButton, BTextView, BTextControl, BAlert, BListItem,BPopUpMenu,BMenuField, BListView, BScrollView,BOutlineListView, BRect, BBox, BFont, InterfaceDefs, BPath, BDirectory, BEntry, BTabView, BTab
from Be import BNode, BStringItem, BFile, BPoint, BLooper, BHandler, BTextControl, TypeConstants, BScrollBar, BStatusBar, BStringView, BUrl, BBitmap,BLocker,BCheckBox,BQuery
from Be import BTranslationUtils,BScreen,BAppFileInfo#,BQuery
from Be.Button import BBehavior
from Be.NodeMonitor import *
from Be.Node import node_ref
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
from Be.TextView import text_run, text_run_array
# from Be.fs_attr import attr_info
from Be.Application import *
from Be.Font import font_height
from Be.Menu import menu_layout
from Be import Entry
from Be.Entry import entry_ref, get_ref_for_path

import datetime

cod_stazioni=[("UD","Udine"),("UDFS","Udine fascio sacca"),("BASL","Basiliano"),("CDRP","Codroipo"),("CSRS","Casarsa"),("CUS","Cusano"),("PN","Pordenone"),("FONT","Fontanafredda"),("SAC","Sacile"),("ORSG","Orsago"),("PIAN","Pianzano"),("CON","Conegliano"),("SUS","Susegana"),("SPR","Spresiano"),("LANC","Lancenigo"),("TVCL","Treviso centrale"),("TVDL","Treviso deposito"),("STRV","San Trovaso"),("PREG","Preganziol"),("MOGL","Mogliano Veneto"),("MSOS","Mestre ospedale"),("MSCL","Mestre centrale"),("MSDL","Mestre deposito"),("VEPM","Venezia porto marghera"),("VESL","Venezia Santa Lucia"),("BUT","Buttrio"),("MANZ","Manzano"),("SGAN","San Giovanni al Natisone"),("CORM","Cormons"),("GOCL","Gorizia centrale"),("SAGR","Sagrado"),("RON","Ronchi nord"),("MONF","Monfalcone"),("SIST","Sistiana"),("BVDA","Bivio d'Aurisina"),("MIRM","Miramare"),("TSCL","Trieste centrale"),("TSDL","Trieste deposito"),("TSA","Trieste airport"),("CRVG","Cervignano"),("SGIO","San Giorgio di Nogaro"),("LAT","Latisana"),("PGRU","Portogruaro"),("SSTI","San Stino di Livenza"),("SDON","San Donà di Piave"),("QUDA","Quarto d'Altino"),("SGDC","San Giovanni di Casarsa"),("SVIT","San Vito al Tagliamento"),("CORD","Cordovado Sesto"),("TEGL","Teglio veneto"),("SACL","Sacile San Liberale"),("BUDJ","Budoia"),("AVNO","Aviano"),("MONT","Montereale valcellina"),("MAN","Maniago"),("TRIC","Tricesimo"),("TARC","Tarcento"),("ARTG","Artegna"),("GEM","Gemona"),("VENZ","Venzone"),("CRNI","Carnia"),("PONT","Pontebba"),("UGOV","Ugovizza"),("TARB","Tarvisio boscoverde"),("PALM","Palmanova"),("RISN","Risano")]
legenda = sorted(cod_stazioni, key=lambda x: x[1])
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
class TipoAcc(BMenuItem):
	def __init__(self,cubie):
		self.name=cubie[0]
		self.code=cubie[1]
		msg=BMessage(607)
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
	def __init__(self):
		BWindow.__init__(self, BRect(200,170,800,278), "Vettura", window_type.B_FLOATING_WINDOW,  B_NOT_RESIZABLE|B_CLOSE_ON_ESCAPE)
		self.bckgnd = BView(self.Bounds(), "bckgnd_View", 8, 20000000)
		rect=self.bckgnd.Bounds()
		self.AddChild(self.bckgnd,None)
		self.bckgnd.SetResizingMode(B_FOLLOW_ALL_SIDES)
		a=BFont()
		self.name=BTextControl(BRect(8,8,rect.Width()*2/3-8,12+a.Size()),"nvett-nome", "N.vettura/VOC:","VOC",BMessage(1900))
		
		self.menupt=BMenu("1")
		self.menutt=BMenu("1")
		self.menupt.SetLabelFromMarked(True)
		self.menutt.SetLabelFromMarked(True)
		self.menupt.AddItem(ParteItem(1))
		self.menupt.AddItem(ParteItem(2))
		self.menutt.AddItem(TotaleItem(1))
		self.menutt.AddItem(TotaleItem(2))
		self.mfparte = BMenuField(BRect(rect.Width()*2/3+8, 8, rect.Width()*2/3+78, 12+a.Size()), 'parte', 'Parte', self.menupt,B_FOLLOW_TOP)
		self.mfparte.SetDivider(a.StringWidth("Parte "))
		self.mftotale = BMenuField(BRect(rect.Width()*2/3+86, 8, rect.Width()*2/3+136, 12+a.Size()), 'totale', 'di', self.menutt,B_FOLLOW_TOP)
		self.mftotale.SetDivider(a.StringWidth("di "))
		self.bckgnd.AddChild(self.mfparte,None)
		self.bckgnd.AddChild(self.mftotale,None)
		
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
		return ret
	def MessageReceived(self, msg):
		if msg.what==605:
			self.cp = msg.FindString("code")
			self.np = msg.FindString("name")
			if self.checkvalues():
				self.addBtn.SetEnabled(True)
			#print(self.cp,self.np)
		elif msg.what==606:
			self.ca = msg.FindString("code")
			self.na = msg.FindString("name")
			if self.checkvalues():
				self.addBtn.SetEnabled(True)
			#print(self.ca,self.na)
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
			if doa-dop>datetime.timedelta(minutes=0):
				mex=BMessage(1002)
				mex.AddInt8("oi",int(self.oi.Text()))
				mex.AddInt8("mi",int(self.mi.Text()))
				mex.AddInt8("of",int(self.of.Text()))
				mex.AddInt8("mf",int(self.mf.Text()))
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
	tipoacc=[("Accessori in partenza",1),("Accessori in arrivo",2),("Cambio volante in partenza",3),("Cambio volante in arrivo",4),("Parking in partenza",5),("Parking in arrivo",6),("Manovra",7),("Riserva",8)]
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
		self.menuf.SetDivider(0)
		self.bckgnd.AddChild(self.menuf,None)
		
		self.treno=BTextControl(BRect(200,8,rect.Width()*2/3-8,12+a.Size()),"treno", "Treno:","",BMessage(1900))
		self.treno.SetDivider(a.StringWidth("Treno:   "))
		self.bckgnd.AddChild(self.treno,None)
		
		self.menupt=BMenu("1")
		self.menutt=BMenu("1")
		self.menupt.SetLabelFromMarked(True)
		self.menutt.SetLabelFromMarked(True)
		self.menupt.AddItem(ParteItem(1))
		self.menupt.AddItem(ParteItem(2))
		self.menutt.AddItem(TotaleItem(1))
		self.menutt.AddItem(TotaleItem(2))
		self.mfparte = BMenuField(BRect(rect.Width()*2/3+8, 8, rect.Width()*2/3+78, 12+a.Size()), 'parte', 'Parte', self.menupt,B_FOLLOW_TOP)
		self.mfparte.SetDivider(a.StringWidth("Parte "))
		self.mftotale = BMenuField(BRect(rect.Width()*2/3+86, 8, rect.Width()*2/3+136, 12+a.Size()), 'totale', 'di', self.menutt,B_FOLLOW_TOP)
		self.mftotale.SetDivider(a.StringWidth("di "))
		self.bckgnd.AddChild(self.mfparte,None)
		self.bckgnd.AddChild(self.mftotale,None)
		
		
		self.oi=BTextControl(BRect(8,28+a.Size(),128,32+2*a.Size()),"ora_inizio", "Inizio ore:",str(5),BMessage(1901))
		#print(a.StringWidth("Arrivo ore:"))
		self.oi.SetDivider(90.0)
		self.mi=BTextControl(BRect(136,28+a.Size(),192,32+2*a.Size()),"min_inizio", "min:",str(58),BMessage(1902))
		self.of=BTextControl(BRect(rect.Width()/2,28+a.Size(),rect.Width()/2+105,32+2*a.Size()),"ora_fine", "Fine ore:",str(6),BMessage(1903))
		self.of.SetDivider(75.0)
		self.mf=BTextControl(BRect(rect.Width()/2+113,28+a.Size(),rect.Width()/2+169,32+2*a.Size()),"min_fine", "min:",str(38),BMessage(1904))
		self.bckgnd.AddChild(self.oi,None)
		self.bckgnd.AddChild(self.mi,None)
		self.bckgnd.AddChild(self.of,None)
		self.bckgnd.AddChild(self.mf,None)
		self.addBtn=BButton(BRect(rect.Width()/2, rect.Height()/2+a.Size()+4,rect.Width()-8,rect.Height()-8),'AddBtn','Aggiungi',BMessage(1002),B_FOLLOW_BOTTOM|B_FOLLOW_RIGHT)
		self.addBtn.SetEnabled(False)
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
	def MessageReceived(self, msg):
		if msg.what==605:
			self.cp = msg.FindString("code")
			self.np = msg.FindString("name")
			if self.checkvalues():
				self.addBtn.SetEnabled(True)
			#print(self.cp,self.np)
		elif msg.what==606:
			self.ca = msg.FindString("code")
			self.na = msg.FindString("name")
			if self.checkvalues():
				self.addBtn.SetEnabled(True)
		elif msg.what==607:
			self.ca = msg.FindString("code")
			self.na = msg.FindString("name")
			if self.checkvalues():
				self.addBtn.SetEnabled(True)
	def QuitRequested(self):
		self.Hide()
class TrenoWindow(BWindow):
	alertWind=[]
	cp=None
	ca=None
	np=None
	na=None
	def __init__(self):
		BWindow.__init__(self, BRect(200,150,800,450), "Treno", window_type.B_FLOATING_WINDOW,  B_NOT_RESIZABLE|B_CLOSE_ON_ESCAPE)
		self.bckgnd = BView(self.Bounds(), "bckgnd_View", 8, 20000000)
		self.AddChild(self.bckgnd,None)
		self.bckgnd.SetResizingMode(B_FOLLOW_ALL_SIDES)	
class PausaWindow(BWindow):
	def __init__(self):
		BWindow.__init__(self, BRect(150,150,586,250), "Pausa", window_type.B_FLOATING_WINDOW,  B_NOT_RESIZABLE|B_CLOSE_ON_ESCAPE)
		self.bckgnd = BView(self.Bounds(), "bckgnd_View", 8, 20000000)
		rect=self.bckgnd.Bounds()
		self.AddChild(self.bckgnd,None)
		self.bckgnd.SetResizingMode(B_FOLLOW_ALL_SIDES)
		a=BFont()
		
		self.menupt=BMenu("1")
		self.menutt=BMenu("1")
		self.menupt.SetLabelFromMarked(True)
		self.menutt.SetLabelFromMarked(True)
		self.menupt.AddItem(ParteItem(1))
		self.menupt.AddItem(ParteItem(2))
		self.menutt.AddItem(TotaleItem(1))
		self.menutt.AddItem(TotaleItem(2))
		self.mfparte = BMenuField(BRect(rect.Width()*2/3+8, 8, rect.Width()*2/3+78, 12+a.Size()), 'parte', 'Parte', self.menupt,B_FOLLOW_TOP)
		self.mfparte.SetDivider(a.StringWidth("Parte "))
		self.mftotale = BMenuField(BRect(rect.Width()*2/3+86, 8, rect.Width()*2/3+136, 12+a.Size()), 'totale', 'di', self.menutt,B_FOLLOW_TOP)
		self.mftotale.SetDivider(a.StringWidth("di "))
		self.bckgnd.AddChild(self.mfparte,None)
		self.bckgnd.AddChild(self.mftotale,None)
		
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
		return ret
	def MessageReceived(self, msg):
		if msg.what==1001:
			mex=BMessage(1001)
			mex.AddInt8("deltam",int(self.deltamvalue.Text()))
			mex.AddInt8("deltao",int(self.deltaovalue.Text()))
			mex.AddString("name",self.name.Text())
			be_app.WindowAt(0).PostMessage(mex)
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
	
	Menus = (
		('File', ((1, 'Carica turno'),(2, 'Salva turno'),(3, 'Chiudi turno'),(None, None),(int(AppDefs.B_QUIT_REQUESTED), 'Esci'))),('Aggiungi', ((4, 'Accessori'),(5, 'Vettura'),(6, 'Treno'),(7, 'Pausa'))),('Elaborazione', ((10, 'Estrai treni'),(11, 'Componi treni-acc'),(42, 'Crea giornate'))),
		('Aiuto', ((8, 'Judimi'),(23, 'Informazioni')))
		)
	def __init__(self):
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
		a=BFont() #+ a.Size()
		self.box = BBox(BRect(0,0,bckgnd_bounds.Width(),bckgnd_bounds.Height()),"Underbox",0x0202|0x0404,border_style.B_FANCY_BORDER)
		self.bckgnd.AddChild(self.box, None)
		self.box.AddChild(self.bar, None)
		self.listaturni = ScrollView(BRect(4 , a.Size()+24+barheight, bounds.Width()- 18, bounds.Height() - 4 ), 'OptionsScrollView')# 24 + barheight
		self.box.AddChild(self.listaturni.sv, None)
		self.turno=BTextControl(BRect(4,4+barheight,150,a.Size()),"turn_name", "FV:","1000",BMessage(1800))
		self.box.AddChild(self.turno, None)
		self.addBtn=BButton(BRect(160, 4+barheight, 300,a.Size()),'AddBtn','Aggiungi turno',BMessage(1801),B_FOLLOW_BOTTOM|B_FOLLOW_RIGHT)
		self.box.AddChild(self.addBtn, None)
		self.remBtn=BButton(BRect(305, 4+barheight, 445,a.Size()),'RemBtn','Rimuovi turno/elemento',BMessage(1802),B_FOLLOW_BOTTOM|B_FOLLOW_RIGHT)
		self.box.AddChild(self.remBtn, None)
		#paofrp=BAlert('cle', "La partenza e antecedente all\'ora di fine del rigo precedente", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
		#self.alertWind.append(paofrp)
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
		self.listaturni.sv.ResizeTo(x-self.listaturni.sv.Frame().left-2,self.box.Bounds().Height()-barheight-4	)
		self.listaturni.lv.ResizeTo(self.listaturni.sv.Bounds().Width(),self.listaturni.sv.Bounds().Height()-4)
		BWindow.FrameResized(self,x,y)

	def MessageReceived(self, msg):
		if msg.what == 7:
		#apri finestra inserimento pausa
			try:
				if self.pausa_window.IsHidden():
					self.pausa_window.Show()
				self.pausa_window.Activate()
			except:
				self.pausa_window = PausaWindow()
				self.tmpWind.append(self.pausa_window)
				self.pausa_window.Show()
		elif msg.what == 5:
		#apri finestra inserimento vettura
			try:
				if self.vett_window.IsHidden():
					self.vett_window.Show()
				self.vett_window.Activate()
			except:
				self.vett_window = VettWindow()
				self.tmpWind.append(self.vett_window)
				self.vett_window.Show()
		elif msg.what == 4:
		#apri finestra inserimento accessori
			try:
				if self.acc_window.IsHidden():
					self.acc_window.Show()
				self.acc_window.Activate()
			except:
				self.acc_window = AccWindow()
				self.tmpWind.append(self.acc_window)
				self.acc_window.Show()
		elif msg.what == 1800:
		#controlla nome turno
			try:
				int(self.turno.Text())
				self.turno.MarkAsInvalid(False)
				self.addBtn.SetEnabled(True)
			except:
				self.turno.MarkAsInvalid(True)
				self.addBtn.SetEnabled(False)
		elif msg.what == 1801:
		#aggiungi turno
			#TODO: controlla se c'è già turno
			chk=True
			for tur in self.listaturni.lv.Items():
				if type(tur)==BStringItem:
					if tur.Text() == self.turno.Text():
						chk=False
						ask=BAlert('cle', "Questo turno c\'è già", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
						self.alertWind.append(ask)
						ask.Go()
			if chk:
				if self.listaturni.lv.CurrentSelection()>-1:
					sel=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection())
					if type(sel)==BStringItem:
						print("it is a superitem",sel.Text())
						#è un superitem
						for el in self.listaturni.lv.Items():
							if type(el) == BStringItem:
								self.listaturni.lv.Collapse(el)
						indt=0
						iout=0
						while indt<self.listaturni.lv.CountItems():
							i=self.listaturni.lv.ItemAt(indt)
							if type(i) == BStringItem:
								iout+=1
								iout+=self.listaturni.lv.CountItemsUnder(i,True)
								if i.Text()==sel.Text():
									self.listaturni.lv.AddItem(BStringItem(self.turno.Text()),iout)
									break
							indt+=1
					else:
						print("looking for its superitem")
						#cerca suo superitem
						supersel=self.listaturni.lv.Superitem(sel)
						#collassa tutto e seleziona supersel
						for el in self.listaturni.lv.Items():
							if type(el) == BStringItem:
								self.listaturni.lv.Collapse(el)
						indt=0
						for i in self.listaturni.lv.Items():
							indt+=1
							if type(i) == BStringItem:
								indt+=self.listaturni.lv.CountItemsUnder(i,True)
								if i.Text()==supersel.Text():
									self.listaturni.lv.AddItem(BStringItem(self.turno.Text()),indt)
									break
				else:
					self.listaturni.lv.AddItem(BStringItem(self.turno.Text()))
				self.listaturni.lv.DeselectAll()
			v=int(self.turno.Text())
			v+=1
			self.turno.SetText(str(v))
		elif msg.what == 1802:
		#rimuovi turno
			if self.listaturni.lv.CountItems()>0:#self.listaturni.lv.FullListCountItems()>0:
				if self.listaturni.lv.CurrentSelection()>-1:
					self.listaturni.lv.RemoveItem(self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()))
				else:
					self.listaturni.lv.RemoveItem(self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1))
		elif msg.what == 1001:
		#aggiungi pausa
			dm=msg.FindInt8("deltam")
			do=msg.FindInt8("deltao")
			dt = datetime.timedelta(hours=do,minutes=dm)
			n=msg.FindString("name")
			#print(self.listaturni.lv.CountItems())
			if self.listaturni.lv.CountItems()>0:
			#se prima riga ignora
				if self.listaturni.lv.CurrentSelection()>-1:
				#fatto
				#è selezionato qualcosa
					selit=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection())
					if type(selit)==BStringItem:
						#è un superitem pertanto vedo se aggiungere pausa alla fine
						it=self.listaturni.lv.CountItemsUnder(selit,True)
						print("itemsUnder",it)
						
						if it>0:
							#è un superitem compresso pertanto aggiungo alla fine
							self.listaturni.lv.Expand(selit)
							lastund=self.listaturni.lv.ItemUnderAt(selit,True,it-1)
							i=lastund.fine #(or it-1)
							sta=lastund.sta
							pau=PausItem(n,i,dt,sta)
							self.tmpElem.append(pau)
							self.listaturni.lv.AddUnder(pau,selit)
							self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(pau),self.listaturni.lv.IndexOf(lastund))
					else:
						#è un elemento
						i=selit.fine
						sta=selit.sta
						pau=PausItem(n,i,dt,sta)
						self.tmpElem.append(pau)
						supit=self.listaturni.lv.Superitem(selit)
						#it=self.listaturni.lv.CountItemsUnder(supit,True)
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
						print("elementi sotto ultimo:", it)
						#controllo se è compresso
						if it>0:
							#posso aggiungere perché è presente un rigo del turno
							i=self.listaturni.lv.ItemUnderAt(litm,True,it-1).fine
							sta=self.listaturni.lv.ItemUnderAt(litm,True,it-1).sta
							pau=PausItem(n,i,dt,sta)
							self.tmpElem.append(pau)
							self.listaturni.lv.AddUnder(pau,litm)
							self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(pau),self.listaturni.lv.CountItems()-1)
						else:
							print("non posso aggiungere perché il turno è vuoto")
					else:
						i=litm.fine
						sta=litm.sta
						pau=PausItem(n,i,dt,sta)
						self.tmpElem.append(pau)
						titm=self.listaturni.lv.Superitem(litm)
						self.listaturni.lv.AddUnder(pau,titm)
						self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(pau),self.listaturni.lv.CountItems()-1)
			#scrivi orario fine questo rigo
		elif msg.what ==1012:
			vet=self.tmpElem[-2]
			itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection())
			titm=self.listaturni.lv.Superitem(itm)
			self.listaturni.lv.AddUnder(vet,titm)
			self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection())
		elif msg.what ==1013:
			vet=self.tmpElem[-2]
			cit=msg.FindInt8("cit")
			itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection())
			r=self.listaturni.lv.AddUnder(vet,itm)
			self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection()+cit+2)
		elif msg.what ==1014:
			vet=self.tmpElem[-2]
			cit=msg.FindInt8("cit")
			itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1)
			print(itm.label)
			titm=self.listaturni.lv.Superitem(itm)
			#print(titm.label)
			self.listaturni.lv.AddUnder(vet,titm)
			self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.IndexOf(titm)+cit+2)#self.listaturni.lv.IndexOf(titm)+cit+2)
		elif msg.what == 1002:
		#aggiungi vettura
			op=msg.FindInt8("oi")
			mp=msg.FindInt8("mi")
			oa=msg.FindInt8("of")
			ma=msg.FindInt8("mf")
			csp=msg.FindString("csp")
			csa=msg.FindString("csa")
			nsp=msg.FindString("nsp")
			nsa=msg.FindString("nsa")
			n=msg.FindString("name")
			dtp = datetime.timedelta(hours=op,minutes=mp)
			dta = datetime.timedelta(hours=oa,minutes=ma)
			if self.listaturni.lv.CountItems()>0:
				vet=VettItem(n,dtp,dta,(csp,nsp),(csa,nsa))
				self.tmpElem.append(vet)
				if self.listaturni.lv.CurrentSelection()>-1:
					itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection())
					titm=self.listaturni.lv.Superitem(itm)
					if titm != None: 
					#esiste superitem ovvero sono un elemento del turno
						print("step 1, selezionato elemento di turno")
						differ = dtp - itm.fine
						print(differ)
						if self.checkpreviouscompatibility(itm,vet):
							if differ > datetime.timedelta(minutes=0):
									print("step 1.2")
									print("aggiungi pausa")
									#TODO prepara BMessage(1001) e crea pausa
									minutes=(differ.seconds % 3600) // 60
									hours=differ.days * 24 + differ.seconds // 3600
									print(hours,minutes)
									mex=BMessage(1001)
									mex.AddInt8("deltam",minutes)
									mex.AddInt8("deltao",hours)
									mex.AddString("name","Pausa")
									be_app.WindowAt(0).PostMessage(mex)
									#self.listaturni.lv.AddUnder(vet,titm)
									#self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection())
									mx2=BMessage(1012)
									be_app.WindowAt(0).PostMessage(mx2)
							elif differ == datetime.timedelta(minutes=0):
									print("step 1.3")
									print("aggiungi senza problemi")
									self.listaturni.lv.AddUnder(vet,titm)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection())
						else:
							ask=BAlert('cle', "Mancata corrispondenza ora partenza vettura e rigo precedente", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
							self.alertWind.append(ask)
							ask.Go()				
					else:
						#Selezionato un superitem
						itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()) #this is the superitem
						self.listaturni.lv.Expand(itm)
						print("step 2, selezionato turno")
						cit=self.listaturni.lv.CountItemsUnder(itm,True)
						print("elementi sotto superitem:",cit)
						if cit>0:
							#controlla ultima ora di fine
							otpf=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()+cit).fine
							differ = dtp - otpf
							print("otpf",otpf)
							print("vet-inizio",vet.inizio)
							proceed=self.checkpreviouscompatibility(self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()+cit),vet)
							print("proceed",proceed)
							if proceed:
								if differ > datetime.timedelta(minutes=0):
									print("step 2.2")
									print("aggiungi pausa",differ)
									#TODO prepara BMessage(1001) e crea pausa
									minutes=(differ.seconds % 3600) // 60
									hours=differ.days * 24 + differ.seconds // 3600
									print(hours,minutes)
									mex=BMessage(1001)
									mex.AddInt8("deltam",minutes)
									mex.AddInt8("deltao",hours)
									mex.AddString("name","Pausa")
									be_app.WindowAt(0).PostMessage(mex)
									
									mx2=BMessage(1013)
									mx2.AddInt8("cit",cit)
									be_app.WindowAt(0).PostMessage(mx2)
									#self.listaturni.lv.AddUnder(vet,itm)
									#self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection()+cit+1)
								elif differ == datetime.timedelta(minutes=0):
									print("step 2.3")
									print("aggiungi senza problemi")
									self.listaturni.lv.AddUnder(vet,itm)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection()+cit+1)
							else:
								ask=BAlert('cle', "Mancata corrispondenza ora partenza vettura e rigo precedente", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
								self.alertWind.append(ask)
								ask.Go()
							#if differ < datetime.timedelta(minutes=0):
							#	print("step 2.1")
							#	print("non va aggiunto")
							#	ask=BAlert('cle', "La partenza e antecedente all\'ora di fine del rigo precedente", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
							#	self.alertWind.append(ask)
							#	ask.Go()
							#elif differ > datetime.timedelta(minutes=0):
							#	print("step 2.2")
							#	print("aggiungi pausa")
							#	#TODO prepara BMessage(1001) e crea pausa
							#	self.listaturni.lv.AddUnder(vet,itm)
							#	self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection()+cit+1)
							#elif differ == datetime.timedelta(minutes=0):
							#	print("step 2.3")
							#	print("aggiungi senza problemi")
							#	self.listaturni.lv.AddUnder(vet,itm)
							#	self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection()+cit+1)
						else:
							self.listaturni.lv.AddUnder(vet,itm)
							self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection()+1)
					self.listaturni.lv.Select(self.listaturni.lv.CurrentSelection())
				else:
					lastit=self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1)
					titm=self.listaturni.lv.Superitem(lastit)
					if titm != None:
						print("step 3, niente selezionato, ultimo oggetto è elemento di turno")
						#last item is an element, not a superitem
						cit=self.listaturni.lv.CountItemsUnder(titm,True)
						#print(cit)
						#if cit>0: #sarà sempre > 0 se non è un superitem
						#	otpf=self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1).fine
						#	print(otpf)
						
						#check if otpf è > di vet.inizio
						proceed=self.checkpreviouscompatibility(lastit,vet)
						if proceed:
							differ=vet.inizio-lastit.fine
							if differ > datetime.timedelta(minutes=0):
								print("step 3.1")
								#TODO aggiungi pausa
								minutes=(differ.seconds % 3600) // 60
								hours=differ.days * 24 + differ.seconds // 3600
								#print(hours,minutes)
								mex=BMessage(1001)
								mex.AddInt8("deltam",minutes)
								mex.AddInt8("deltao",hours)
								mex.AddString("name","Pausa")
								be_app.WindowAt(0).PostMessage(mex)
									
								mx2=BMessage(1014)
								mx2.AddInt8("cit",cit)
								be_app.WindowAt(0).PostMessage(mx2)
								#self.listaturni.lv.AddUnder(vet,titm)
								#con=self.listaturni.lv.CountItemsUnder(titm,True)
								#self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.IndexOf(vet)+con-1)
							elif differ == datetime.timedelta(minutes=0):
								print("step 3.2")
								self.listaturni.lv.AddUnder(vet,titm)
								con=self.listaturni.lv.CountItemsUnder(titm,True)
								self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.IndexOf(vet)+con-1)
						else:
							ask=BAlert('cle', "Mancata corrispondenza ora partenza vettura e rigo precedente", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
							self.alertWind.append(ask)
							ask.Go()
					else:
						print("step 4, niente selezionato, ultimo oggetto è turno") # verificare che succede se questo e precedente sono collassati e non selezionati
						self.listaturni.lv.AddUnder(vet,self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1))
				
				
			print("fine messaggio")	
			#ottieni orario fine da rigo precedente
			#scrivi orario fine questo rigo
		
		return BWindow.MessageReceived(self,msg)
	
	def checkpreviouscompatibility(self,prev,vet):
		ret = True
		print(prev)
		print(vet)
		if prev.fine>vet.inizio:
			ret=False
		return ret
		
				
	def QuitRequested(self):
		wnum = be_app.CountWindows()
		if wnum>1:
			if len(self.tmpWind)>0:
				for wind in self.tmpWind:
					wind.Lock()
					wind.Quit()
			#if len(self.papdetW)>0:
			#	for papw in self.papdetW:
			#		papw.Lock()
			#		papw.Quit()
		return BWindow.QuitRequested(self)


#funziona ma non salva come VettItem ma come BListItem non salvando self.inizio e self.fine ecc.
#class VettItem(BStringItem):
#	def __init__(self,name,inizio,fine):
#		self.name=name
#		self.inizio=inizio
#		self.fine=fine
#		self.label=(str(self.inizio)+"\t"+self.name+"\t"+str(self.fine))
#		BStringItem.__init__(self,self.label)
#	def fine(self):
#		return self.fine

class AccItem(BListItem):
	def __init__(self,tipo,name,inizio,fine,stp,sta,condotta,materiale,parteturno):
		self.name=name
		#self.label=self.name
		fon=BFont()
		self.stp=stp
		self.sta=sta
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
		self.label=("vettura"+"  "+self.name+"  "+stp[0]+"  "+sta[0]+"  "+str(self.inizio)+"  "+str(self.fine))
		BListItem.__init__(self)
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
		mi=(inizio.seconds % 3600) // 60
		oi=inizio.days * 24 + inizio.seconds // 3600
		of=fine.days * 24 + fine.seconds // 3600
		mf=(fine.seconds % 3600) // 60
		self.iout=str(oi)+":"+str(mi)
		self.fout=str(of)+":"+str(mf)
		self.label=("vettura"+"  "+self.name+"  "+stp[0]+"  "+sta[0]+"  "+str(self.inizio)+"  "+str(self.fine))
		BListItem.__init__(self)

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
		owner.MovePenTo(frame.left+50,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.name,None)
		owner.MovePenTo(frame.left+100,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.stp[0],None)
		owner.MovePenTo(frame.left+150,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.sta[0],None)
		owner.MovePenTo(frame.left+200,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.iout,None)#str(self.inizio),None)
		owner.MovePenTo(frame.left+250,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.fout,None)#str(self.fine),None)
		#if self.unread:
		#	owner.SetFont(be_bold_font)
		#else:
		#	owner.SetFont(be_plain_font)
		#owner.DrawString(self.label,None)
		#if not self.consistent:
		#	sp=BPoint(3,frame.bottom-((frame.bottom-frame.top)/2))
		#	ep=BPoint(frame.right-3,frame.bottom-(frame.bottom-frame.top)/2)
		#	owner.StrokeLine(sp,ep)
		#owner.SetLowColor(255,255,255,255)
class PausItem(BListItem):
	def __init__(self,name,inizio,deltat,dove,parteturno):
		self.name=name
		#self.label=self.name
		fon=BFont()
		self.stp=dove
		self.sta=dove
		self.font_height_value=font_height()
		fon.GetHeight(self.font_height_value)
		self.inizio=inizio
		#print("pausa inizio",inizio)
		self.fine=inizio + deltat
		mi=(inizio.seconds % 3600) // 60
		oi=inizio.days * 24 + inizio.seconds // 3600
		of=self.fine.days * 24 + self.fine.seconds // 3600
		mf=(self.fine.seconds % 3600) // 60
		self.iout=str(oi)+":"+str(mi)
		self.fout=str(of)+":"+str(mf)
		#print("pausa fine",deltat)
		self.label=(self.name+"        "+dove[0]+"  "+dove[0]+"  "+str(self.inizio)+"  "+str(self.fine))
		
		BListItem.__init__(self)
		
	def DrawItem(self, owner, frame, complete):
		if self.IsSelected() or complete:
			owner.SetHighColor(200,200,200,255)
			owner.SetLowColor(200,200,200,255)
			owner.FillRect(frame)
		owner.SetHighColor(0,0,0,0)
		owner.MovePenTo(frame.left+5,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.name,None)
		owner.MovePenTo(frame.left+100,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.stp[0],None)
		owner.MovePenTo(frame.left+150,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.sta[0],None)
		owner.MovePenTo(frame.left+200,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.iout,None)
		owner.MovePenTo(frame.left+250,frame.bottom-self.font_height_value.descent)
		owner.DrawString(self.fout,None)
		
		
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
	def ReadyToRun(self):
		self.window = MainWindow()
		self.window.Show()
	def MessageReceived(self,msg):
		msg.PrintToStream()
		BApplication.MessageReceived(self,msg)

#	def Pulse(self):
#		if self.window.enabletimer:
#			be_app.WindowAt(0).PostMessage(BMessage(66))



def main():
    global be_app
    be_app = App()
    be_app.Run()
	
 
if __name__ == "__main__":
    main()