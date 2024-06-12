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

import os,datetime

cod_stazioni=[("UD","Udine"),("UDFS","Udine fascio sacca"),("BASL","Basiliano"),("CDRP","Codroipo"),("CSRS","Casarsa"),("CUS","Cusano"),("PN","Pordenone"),("FONT","Fontanafredda"),("SAC","Sacile"),("ORSG","Orsago"),("PIAN","Pianzano"),("CON","Conegliano"),("SUS","Susegana"),("SPR","Spresiano"),("LANC","Lancenigo"),("TVCL","Treviso centrale"),("TVDL","Treviso deposito"),("STRV","San Trovaso"),("PREG","Preganziol"),("MOGL","Mogliano Veneto"),("MSOS","Mestre ospedale"),("MSCL","Mestre centrale"),("MSDL","Mestre deposito"),("VEPM","Venezia porto marghera"),("VESL","Venezia Santa Lucia"),("BUT","Buttrio"),("MANZ","Manzano"),("SGAN","San Giovanni al Natisone"),("CORM","Cormons"),("GOCL","Gorizia centrale"),("SAGR","Sagrado"),("RON","Ronchi nord"),("MONF","Monfalcone"),("SIST","Sistiana"),("BVDA","Bivio d'Aurisina"),("MIRM","Miramare"),("TSCL","Trieste centrale"),("TSDL","Trieste deposito"),("TSA","Trieste airport"),("CRVG","Cervignano"),("SGIO","San Giorgio di Nogaro"),("LAT","Latisana"),("PGRU","Portogruaro"),("SSTI","San Stino di Livenza"),("SDON","San Donà di Piave"),("QUDA","Quarto d'Altino"),("SGDC","San Giovanni di Casarsa"),("SVIT","San Vito al Tagliamento"),("CORD","Cordovado Sesto"),("TEGL","Teglio veneto"),("SACL","Sacile San Liberale"),("BUDJ","Budoia"),("AVNO","Aviano"),("MONT","Montereale valcellina"),("MAN","Maniago"),("TRIC","Tricesimo"),("TARC","Tarcento"),("ARTG","Artegna"),("GEM","Gemona"),("VENZ","Venzone"),("CRNI","Carnia"),("PONT","Pontebba"),("UGOV","Ugovizza"),("TARB","Tarvisio boscoverde"),("PALM","Palmanova"),("RISN","Risano")]
legenda = sorted(cod_stazioni, key=lambda x: x[1])

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
		msg=BMessage(610)
		msg.AddInt8("accp",data[1])
		msg.AddInt8("acca",data[2])
		msg.AddInt8("prkp",data[3])
		msg.AddInt8("prka",data[4])
		msg.AddInt8("cb",data[5])
		msg.AddString("name",self.name)
		BMenuItem.__init__(self,self.name,msg,self.name[0],0)
materiali=[Materiale(("Rock",30,15,25,10,7)),Materiale(("563/564",30,15,25,10,7)),Materiale(("Ale/Aln 501/502",25,10,20,10,6)),Materiale(("Blues",25,10,20,10,7)),Materiale(("464/MD/Viv",40,20,25,10,10)),Materiale(("464+464/MD",55,30,25,10,10))]
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
		if ret:
			if self.parte>self.totale:
				ret=False
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
			self.parte = msg.FindInt8("code")
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 609:
			self.totale = msg.FindInt8("code")
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
			if doa-dop>datetime.timedelta(minutes=0):
				mex=BMessage(1002)
				mex.AddInt8("oi",int(self.oi.Text()))
				mex.AddInt8("mi",int(self.mi.Text()))
				mex.AddInt8("of",int(self.of.Text()))
				mex.AddInt8("mf",int(self.mf.Text()))
				mex.AddInt8("parte",self.parte)
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
						sta=selitm.sta
						doit=True
				else:
					lastitm=lt.ItemAt(lt.CountItems()-1)
					if type(lastitm) != BStringItem:
						orario=lastitm.fine
						sta=lastitm.sta
						doit=True
				if doit:
					self.menup.FindItem(sta[1]).SetMarked(True)
					self.cp=sta[0]
					self.np=sta[1]
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
		self.mfparte = BMenuField(BRect(rect.Width()*2/3+8, 8, rect.Width()*2/3+78, 12+a.Size()), 'parte', 'Parte', self.menupt,B_FOLLOW_TOP) #rect.Width()*2/3+78 <-- it's ignored if I write 0 the item is fully visible
		self.mfparte.SetDivider(a.StringWidth("Parte ")) #<- This works
		self.bckgnd.AddChild(self.mfparte,None)
		
		self.menutt=BMenu("1")
		self.menutt.SetLabelFromMarked(True)
		self.menutt.AddItem(TotaleItem(1))
		self.menutt.AddItem(TotaleItem(2))
		self.mftotale = BMenuField(BRect(rect.Width()*2/3+86, 8, rect.Width()*2/3+186, 12+a.Size()), 'totale', 'di', self.menutt,B_FOLLOW_TOP)
		self.mftotale.SetDivider(a.StringWidth("di  "))
		self.bckgnd.AddChild(self.mftotale,None)
		
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
			self.menumat.AddItem(m)
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
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 609:
			self.totale = msg.FindInt8("code")
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
				mex.AddString("materiale",self.mat)
				mex.AddInt8("parte",self.parte) #parte del turno
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
						sta=selitm.sta
						doit=True
				else:
					lastitm=lt.ItemAt(lt.CountItems()-1)
					if type(lastitm) != BStringItem:
						orario=lastitm.fine
						sta=lastitm.sta
						doit=True
				if doit:
					self.menup.FindItem(sta[1]).SetMarked(True)
					self.cp=sta[0]
					self.np=sta[1]
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
	ccond=None
	ncond=None
	parte=1
	totale=1
	tipoaccp=[("Accessori in partenza",1),("Cambio volante in partenza",3),("Parking in partenza",5)]
	tipoacca=[("Accessori in arrivo",2),("Cambio volante in arrivo",4),("Parking in arrivo",6),("Cambio banco",7)]
	tipocond=[("Agente solo",1),("Agente Unico",2),("Doppio Agente/1",3),("Doppio Agente/2",4)]
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
		#self.chkaccp.SetValue(True)
		self.bckgnd.AddChild(self.chkaccp,None)
		self.menuaccp=BMenu("Tipo accessori")
		self.menuaccp.SetLabelFromMarked(True)
		for y in self.tipoaccp:
			self.menuaccp.AddItem(TipoAccp(y))
		self.menufp = BMenuField(BRect(8,8,158,12+a.Size()), 'pop0', '', self.menuaccp,B_FOLLOW_TOP)
		self.menufp.SetDivider(0) #<-This works
		self.boxaccp.AddChild(self.menufp,None)
		
		self.name=BTextControl(BRect(rect.Width()/3+8,8,rect.Width()*2/3-8,12+a.Size()),"ntreno", "Numero treno:","1234",BMessage(1900))
		self.bckgnd.AddChild(self.name,None)
		
		self.boxacca = BBox(BRect(rect.Width()*2/3+8,32,rect.Width()-8,rect.Height()-46),"Box_acc_arrivo",0x0202|0x0404,border_style.B_FANCY_BORDER)
		self.bckgnd.AddChild(self.boxacca,None)
		baarect=self.boxacca.Bounds()
		self.chkacca = BCheckBox(BRect(rect.Width()*2/3+8,8,rect.Width()-8,28),"CheckBox_acc_arrivo","Accessori arrivo",BMessage(1501))
		#self.chkacca.SetValue(True)
		self.bckgnd.AddChild(self.chkacca,None)
		
		self.menuacca=BMenu("Tipo accessori")
		self.menuacca.SetLabelFromMarked(True)
		for y in self.tipoacca:
			self.menuacca.AddItem(TipoAcca(y))
		self.menufa = BMenuField(BRect(8,8,158,12+a.Size()), 'pop0', '', self.menuacca,B_FOLLOW_TOP)
		self.menufa.SetDivider(0) #<-This works
		self.boxacca.AddChild(self.menufa,None)
		
		self.menupt=BMenu("1")
		self.menupt.SetLabelFromMarked(True)
		self.menupt.AddItem(ParteItem(1))
		self.menupt.AddItem(ParteItem(2))
		self.mfparte = BMenuField(BRect(8, rect.Height()-32-a.Size(),78 , rect.Height()-8), 'parte', 'Parte', self.menupt,B_FOLLOW_TOP) #rect.Width()*2/3+78 <-- it's ignored if I write 0 the item is fully visible
		self.mfparte.SetDivider(a.StringWidth("Parte "))
		self.bckgnd.AddChild(self.mfparte,None)
		
		self.menutt=BMenu("1")
		self.menutt.SetLabelFromMarked(True)
		self.menutt.AddItem(TotaleItem(1))
		self.menutt.AddItem(TotaleItem(2))
		self.mftotale = BMenuField(BRect(86, rect.Height()-32-a.Size(), 166, rect.Height()-8), 'totale', 'di', self.menutt,B_FOLLOW_TOP)
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
		
		#82-102
		self.cond=BMenu("Tipo condotta")
		self.cond.SetLabelFromMarked(True)
		for z in self.tipocond:
			self.cond.AddItem(Condotta(z))
		self.condmf = BMenuField(BRect(rect.Width()/3+8, 112, rect.Width()*2/3-8, 132), 'pop1', 'Condotta:', self.cond,B_FOLLOW_TOP)
		self.condmf.SetDivider(80.0)
		self.bckgnd.AddChild(self.condmf,None)
		
		#112-132
		self.menumat = BMenu("Materiale rotabile")
		self.menumat.SetLabelFromMarked(True)
		for m in materiali:
			self.menumat.AddItem(m)
		self.mfmat = BMenuField(BRect(rect.Width()/3+8, 142, rect.Width()*2/3-8, 162), 'materiale', 'Materiale:', self.menumat,B_FOLLOW_TOP)#48+2*a.Size(),44+3*a.Size()
		self.mfmat.SetDivider(80.0)
		self.bckgnd.AddChild(self.mfmat,None)
		
		self.addBtn=BButton(BRect(rect.Width()/2, rect.Height()-32-a.Size(),rect.Width()-8,rect.Height()-8),'AddBtn','Aggiungi',BMessage(1112),B_FOLLOW_BOTTOM|B_FOLLOW_RIGHT)
		self.addBtn.SetEnabled(False)
		self.bckgnd.AddChild(self.addBtn,None)
	def checkvalues(self):
		ret=True
		if self.chkaccp.Value()==0:
			print("controllo valori accessori partenza")
			for testo in {self.oip.Text(),self.mip.Text()}:
				try:
					int(testo)
				except:
					ret=False
			if self.codaccp==0:
				ret=False
		if self.chkacca.Value()==0:
			print("controllo valori accessori arrivo")
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
				ret=False
				self.name.MarkAsInvalid(True)
			if self.cp==None or self.ca==None:
				ret=False
			elif self.parte>self.totale:
				ret=False
			dtit=datetime.timedelta(hours=int(self.oit.Text()),minutes=int(self.mit.Text()))
			dtft=datetime.timedelta(hours=int(self.oft.Text()),minutes=int(self.mft.Text()))
			if dtit>=dtft:
				ret=False
			if self.chkaccp.Value()==0:
				dtap=datetime.timedelta(hours=int(self.oip.Text()),minutes=int(self.mip.Text()))
				if dtap>dtit:
					ret=False
			if self.chkacca.Value()==0:
				dtaa=datetime.timedelta(hours=int(self.ofa.Text()),minutes=int(self.mfa.Text()))
				if dtaa<dtft:
					ret=False
		return ret
	def MessageReceived(self, msg):
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
		elif msg.what==605:
			#stabilisco stazione partenza
			self.cp = msg.FindString("code")
			self.np = msg.FindString("name")
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what==606:
			#stabilisco stazione arrivo
			self.ca = msg.FindString("code")
			self.na = msg.FindString("name")
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 608:
			self.parte = msg.FindInt8("code")
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 609:
			self.totale = msg.FindInt8("code")
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what==808:
			self.ccond=msg.FindInt8("code")
			self.ncond=msg.FindString("name")
		elif msg.what == 610:
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
						delt=datetime.timedelta(minutes=self.cb)
					dtout=datoi+delt
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
			#dopt=datetime.timedelta(hours=int(self.oi.Text()),minutes=int(self.mi.Text()))
			#doat=datetime.timedelta(hours=int(self.of.Text()),minutes=int(self.mf.Text()))
			if self.chkaccp.Value()==0:
				mex=BMessage(1003)
				mex.AddInt8("oi",int(self.oip.Text())) #ora inizio
				mex.AddInt8("mi",int(self.mip.Text())) #minuto inizio
				mex.AddInt8("of",int(self.oit.Text())) #ora fine
				mex.AddInt8("mf",int(self.mit.Text())) #minuto fine
				mex.AddString("csp",self.cp) #codice stazione partenza
				mex.AddString("csa",self.cp) #codice stazione arrivo
				mex.AddString("nsp",self.np) #nome stazione partenza
				mex.AddString("nsa",self.np) #nome stazione arrivo
				mex.AddString("nta",self.tap) #nome tipo accessori
				mex.AddInt8("codacc",self.codaccp) #codice accessori
				mex.AddString("materiale",self.mat)
				mex.AddInt8("parte",self.parte) #parte del turno
				mex.AddInt8("totale",self.totale) #totale del turno
				mex.AddString("name",self.name.Text()) #nome accessori/numero treno
				be_app.WindowAt(0).PostMessage(mex)
			mex=BMessge(1102)
			mex.AddInt32("name",int(self.name.Text()))
			mex.AddInt8("oi",int(self.oit.Text())) #ora inizio
			mex.AddInt8("mi",int(self.mit.Text())) #minuto inizio
			mex.AddInt8("of",int(self.oft.Text())) #ora fine
			mex.AddInt8("mf",int(self.mft.Text())) #minuto fine
			mex.AddString("csp",self.cp) #codice stazione partenza
			mex.AddString("csa",self.ca) #codice stazione arrivo
			mex.AddString("nsp",self.np) #nome stazione partenza
			mex.AddString("nsa",self.na) #nome stazione arrivo
			mex.AddString("ncond",self.ncond) # nome tipo condotta
			mex.AddInt8("ccond",self.ccond) # codice tipo condotta
			mex.AddString("materiale",self.mat)
			mex.AddInt8("parte",self.parte) #parte del turno
			mex.AddInt8("totale",self.totale) #totale del turno
			be_app.WindowAt(0).PostMessage(mex)
			if self.chkacca.Value()==0:
				mex=BMessage(1003)
				mex.AddInt8("oi",int(self.oft.Text())) #ora inizio
				mex.AddInt8("mi",int(self.mft.Text())) #minuto inizio
				mex.AddInt8("of",int(self.ofa.Text())) #ora fine
				mex.AddInt8("mf",int(self.mfa.Text())) #minuto fine
				mex.AddString("csp",self.ca) #codice stazione partenza
				mex.AddString("csa",self.ca) #codice stazione arrivo
				mex.AddString("nsp",self.na) #nome stazione partenza
				mex.AddString("nsa",self.na) #nome stazione arrivo
				mex.AddString("nta",self.taa) #nome tipo accessori
				mex.AddInt8("codacc",self.codacca) #codice accessori
				mex.AddString("materiale",self.mat)
				mex.AddInt8("parte",self.parte) #parte del turno
				mex.AddInt8("totale",self.totale) #totale del turno
				mex.AddString("name",self.name.Text()) #nome accessori/numero treno
				be_app.WindowAt(0).PostMessage(mex)
		return BWindow.MessageReceived(self,msg)
	def QuitRequested(self):
		self.Hide()
class PausaWindow(BWindow):
	parte=1
	totale=1
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
		if ret:
			if self.parte>self.totale:
				ret=False
		return ret
	def MessageReceived(self, msg):
		if msg.what==1001:
			mex=BMessage(1001)
			mex.AddInt8("deltam",int(self.deltamvalue.Text()))
			mex.AddInt8("deltao",int(self.deltaovalue.Text()))
			mex.AddInt8("parte",self.parte)
			mex.AddInt8("totale",self.totale)
			mex.AddString("name",self.name.Text())
			be_app.WindowAt(0).PostMessage(mex)
		elif msg.what == 608:
			self.parte = msg.FindInt8("code")
			self.addBtn.SetEnabled(self.checkvalues())
		elif msg.what == 609:
			self.totale = msg.FindInt8("code")
			self.addBtn.SetEnabled(self.checkvalues())
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
			#self.getTimeBtn=PButton(BRect(rect.Width()-40,28+a.Size(),rect.Width()-8,46+2*a.Size()),'GetTimeButton','',BMessage(1004),B_FOLLOW_BOTTOM|B_FOLLOW_RIGHT,img1)
			self.deselectBtn=PButton(BRect(bckgnd_bounds.right-32, 4+barheight, bckgnd_bounds.right-2,34+barheight),'DeselectBtn','▤',BMessage(1020),B_FOLLOW_TOP|B_FOLLOW_RIGHT,img1)#▤⌧
			#tmprect=self.deselectBtn.Bounds()
			#print(tmprect.Width(),tmprect.Height())
		else:
			lab="▤"
			self.deselectBtn=BButton(BRect(bckgnd_bounds.right-32,4+barheight,bckgnd_bounds.right-2,34+barheight),'GetTimeButton',lab,BMessage(1020),B_FOLLOW_TOP|B_FOLLOW_RIGHT)
		#self.deselectBtn=PButton(BRect(305, 4+barheight, 445,a.Size()),'DeselectBtn','▤',BMessage(1802),B_FOLLOW_BOTTOM|B_FOLLOW_RIGHT)#▤⌧
		self.box.AddChild(self.deselectBtn, None)

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
		elif msg.what == 6:
		#apri finestra inserimento treno
			try:
				if self.treno_window.IsHidden():
					self.treno_window.Show()
				self.treno_window.Activate()
			except:
				self.treno_window = TrenoWindow()
				self.tmpWind.append(self.treno_window)
				self.treno_window.Show()
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
			#controlla se c'è già turno
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
			parte=msg.FindInt8("parte")
			totale=msg.FindInt8("totale")
			parteturno=(parte,totale)
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
							pau=PausItem(n,i,dt,sta,parteturno)
							self.tmpElem.append(pau)
							self.listaturni.lv.AddUnder(pau,selit)
							self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(pau),self.listaturni.lv.IndexOf(lastund))
					else:
						#è un elemento
						i=selit.fine
						sta=selit.sta
						pau=PausItem(n,i,dt,sta,parteturno)
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
							pau=PausItem(n,i,dt,sta,parteturno)
							self.tmpElem.append(pau)
							self.listaturni.lv.AddUnder(pau,litm)
							self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(pau),self.listaturni.lv.CountItems()-1)
						else:
							print("non posso aggiungere perché il turno è vuoto")
					else:
						i=litm.fine
						sta=litm.sta
						pau=PausItem(n,i,dt,sta,parteturno)
						self.tmpElem.append(pau)
						titm=self.listaturni.lv.Superitem(litm)
						self.listaturni.lv.AddUnder(pau,titm)
						self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(pau),self.listaturni.lv.CountItems()-1)
		elif msg.what == 1012:
			vet=self.tmpElem[-2]
			itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection())
			titm=self.listaturni.lv.Superitem(itm)
			self.listaturni.lv.AddUnder(vet,titm)
			self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection())
		elif msg.what == 1013:
			vet=self.tmpElem[-2]
			cit=msg.FindInt8("cit")
			itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection())
			r=self.listaturni.lv.AddUnder(vet,itm)
			self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection()+cit+2)
		elif msg.what == 1014:
			vet=self.tmpElem[-2]
			cit=msg.FindInt8("cit")
			itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1)
			titm=self.listaturni.lv.Superitem(itm)
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
			parte=msg.FindInt8("parte")
			totale=msg.FindInt8("totale")
			dtp = datetime.timedelta(hours=op,minutes=mp)
			dta = datetime.timedelta(hours=oa,minutes=ma)
			if self.listaturni.lv.CountItems()>0:
				vet=VettItem(n,dtp,dta,(csp,nsp),(csa,nsa),(parte,totale))
				self.tmpElem.append(vet)
				if self.listaturni.lv.CurrentSelection()>-1:
					itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection())
					titm=self.listaturni.lv.Superitem(itm)
					if titm != None: 
					#esiste superitem ovvero sono un elemento del turno
						print("step 1, selezionato elemento di turno")
						differ = dtp - itm.fine
						if self.checkpreviouscompatibility(itm,vet):
							if differ > datetime.timedelta(minutes=0):
									print("step 1.2")
									#prepara BMessage(1001) e crea pausa
									minutes=(differ.seconds % 3600) // 60
									hours=differ.days * 24 + differ.seconds // 3600
									mex=BMessage(1001)
									mex.AddInt8("deltam",minutes)
									mex.AddInt8("deltao",hours)
									mex.AddInt8("parte",parte)
									mex.AddInt8("totale",totale)
									mex.AddString("name","Pausa")
									be_app.WindowAt(0).PostMessage(mex)
									
									mx2=BMessage(1012)
									be_app.WindowAt(0).PostMessage(mx2)
							elif differ == datetime.timedelta(minutes=0):
									#aggiungi senza problemi
									print("step 1.3")
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
						if cit>0:
							#controlla ultima ora di fine
							otpf=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()+cit).fine
							differ = dtp - otpf
							proceed=self.checkpreviouscompatibility(self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()+cit),vet)
							if proceed:
								if differ > datetime.timedelta(minutes=0):
									print("step 2.2")
									#prepara BMessage(1001) e crea pausa
									minutes=(differ.seconds % 3600) // 60
									hours=differ.days * 24 + differ.seconds // 3600
									mex=BMessage(1001)
									mex.AddInt8("deltam",minutes)
									mex.AddInt8("deltao",hours)
									mex.AddInt8("parte",parte)
									mex.AddInt8("totale",totale)
									mex.AddString("name","Pausa")
									be_app.WindowAt(0).PostMessage(mex)
									
									mx2=BMessage(1013)
									mx2.AddInt8("cit",cit)
									be_app.WindowAt(0).PostMessage(mx2)
								elif differ == datetime.timedelta(minutes=0):
									#aggiungi senza problemi
									print("step 2.3")
									self.listaturni.lv.AddUnder(vet,itm)
									self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(vet),self.listaturni.lv.CurrentSelection()+cit+1)
							else:
								ask=BAlert('cle', "Mancata corrispondenza ora partenza vettura e rigo precedente", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
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
						print("step 3, niente selezionato, ultimo oggetto è elemento di turno")
						#last item is an element, not a superitem
						cit=self.listaturni.lv.CountItemsUnder(titm,True)
						#check if otpf è > di vet.inizio
						proceed=self.checkpreviouscompatibility(lastit,vet)
						if proceed:
							differ=vet.inizio-lastit.fine
							if differ > datetime.timedelta(minutes=0):
								print("step 3.1")
								#aggiungi pausa
								minutes=(differ.seconds % 3600) // 60
								hours=differ.days * 24 + differ.seconds // 3600
								mex=BMessage(1001)
								mex.AddInt8("deltam",minutes)
								mex.AddInt8("deltao",hours)
								mex.AddInt8("parte",parte)
								mex.AddInt8("totale",totale)
								mex.AddString("name","Pausa")
								be_app.WindowAt(0).PostMessage(mex)
									
								mx2=BMessage(1014)
								mx2.AddInt8("cit",cit)
								be_app.WindowAt(0).PostMessage(mx2)
							elif differ == datetime.timedelta(minutes=0):
								#agiungi senza prolemi
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
		elif msg.what == 1003:
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
			totale=msg.FindInt8("totale")
			n=msg.FindString("name")
			dtp = datetime.timedelta(hours=op,minutes=mp)
			dta = datetime.timedelta(hours=oa,minutes=ma)
			if self.listaturni.lv.CountItems()>0:
				acc=AccItem((nta,codacc),n,dtp,dta,(csp,nsp),(csa,nsa),(nta,codacc),materiale,(parte,totale))
				self.tmpElem.append(acc)
				if self.listaturni.lv.CurrentSelection()>-1:
					itm=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection())
					titm=self.listaturni.lv.Superitem(itm)
					if titm != None: 
					#esiste superitem ovvero sono un elemento del turno
						print("step 1, selezionato elemento di turno")
						differ = dtp - itm.fine
						if self.checkpreviouscompatibility(itm,acc):
							if differ > datetime.timedelta(minutes=0):
									print("step 1.2")
									#prepara BMessage(1001) e crea pausa
									minutes=(differ.seconds % 3600) // 60
									hours=differ.days * 24 + differ.seconds // 3600
									mex=BMessage(1001)
									mex.AddInt8("deltam",minutes)
									mex.AddInt8("deltao",hours)
									mex.AddInt8("parte",parte)
									mex.AddInt8("totale",totale)
									mex.AddString("name","Pausa")
									be_app.WindowAt(0).PostMessage(mex)
									
									mx2=BMessage(1012)
									be_app.WindowAt(0).PostMessage(mx2)
							elif differ == datetime.timedelta(minutes=0):
									#aggiungi senza problemi
									print("step 1.3")
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
						print("step 2, selezionato turno")
						cit=self.listaturni.lv.CountItemsUnder(itm,True)
						if cit>0:
							#controlla ultima ora di fine
							otpf=self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()+cit).fine
							differ = dtp - otpf
							proceed=self.checkpreviouscompatibility(self.listaturni.lv.ItemAt(self.listaturni.lv.CurrentSelection()+cit),acc)
							if proceed:
								if differ > datetime.timedelta(minutes=0):
									print("step 2.2")
									#prepara BMessage(1001) e crea pausa
									minutes=(differ.seconds % 3600) // 60
									hours=differ.days * 24 + differ.seconds // 3600
									mex=BMessage(1001)
									mex.AddInt8("deltam",minutes)
									mex.AddInt8("deltao",hours)
									mex.AddInt8("parte",parte)
									mex.AddInt8("totale",totale)
									mex.AddString("name","Pausa")
									be_app.WindowAt(0).PostMessage(mex)
									
									mx2=BMessage(1013)
									mx2.AddInt8("cit",cit)
									be_app.WindowAt(0).PostMessage(mx2)
								elif differ == datetime.timedelta(minutes=0):
									#aggiungi senza problemi
									print("step 2.3")
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
						print("step 3, niente selezionato, ultimo oggetto è elemento di turno")
						#last item is an element, not a superitem
						cit=self.listaturni.lv.CountItemsUnder(titm,True)
						#check if otpf è > di acc.inizio
						proceed=self.checkpreviouscompatibility(lastit,acc)
						if proceed:
							differ=acc.inizio-lastit.fine
							if differ > datetime.timedelta(minutes=0):
								print("step 3.1")
								#aggiungi pausa
								minutes=(differ.seconds % 3600) // 60
								hours=differ.days * 24 + differ.seconds // 3600
								mex=BMessage(1001)
								mex.AddInt8("deltam",minutes)
								mex.AddInt8("deltao",hours)
								mex.AddInt8("parte",parte)
								mex.AddInt8("totale",totale)
								mex.AddString("name","Pausa")
								be_app.WindowAt(0).PostMessage(mex)
									
								mx2=BMessage(1014)
								mx2.AddInt8("cit",cit)
								be_app.WindowAt(0).PostMessage(mx2)
							elif differ == datetime.timedelta(minutes=0):
								#agiungi senza prolemi
								print("step 3.2")
								self.listaturni.lv.AddUnder(acc,titm)
								con=self.listaturni.lv.CountItemsUnder(titm,True)
								self.listaturni.lv.MoveItem(self.listaturni.lv.IndexOf(acc),self.listaturni.lv.IndexOf(acc)+con-1)
						else:
							ask=BAlert('cle', "Mancata corrispondenza ora inizio accessori e rigo precedente", 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_STOP_ALERT)
							self.alertWind.append(ask)
							ask.Go()
					else:
						print("step 4, niente selezionato, ultimo oggetto è turno") # verificare che succede se questo e precedente sono collassati e non selezionati
						self.listaturni.lv.AddUnder(acc,self.listaturni.lv.ItemAt(self.listaturni.lv.CountItems()-1))
		return BWindow.MessageReceived(self,msg)
	def checkpreviouscompatibility(self,prev,ittem):
		ret = True
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


class TrenoItem(BListItem):
	def __init__(self,name,inizio,fine,stp,sta,tipocond,materiale,parteturno):
		fon=BFont()
		self.materiale = materiale
		self.parte=parteturno[0]
		self.totale=parteturno[1]
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
		self.label=("Condotta"+"  "+self.name+"  "+stp[0]+"  "+sta[0]+"  "+str(self.inizio)+"  "+str(self.fine)+"  "+self.ncond+"  "+self.materiale+"  "+str(parteturno[0])+"/"+str(parteturno[1]))
		BListItem.__init__(self)
	def DrawItem(self, owner, frame, complete):
		owner.SetHighColor(200,255,200,255)
		owner.SetLowColor(0,0,0,0)
		if self.IsSelected() or complete:
			owner.SetHighColor(200,200,200,255)
			owner.SetLowColor(200,200,200,255)
		owner.FillRect(frame)
		owner.SetHighColor(0,0,0,0)
		owner.MovePenTo(frame.left+5,frame.bottom-self.font_height_value.descent)
		owner.DrawString("condotta",None)
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
	def __init__(self,ta,name,inizio,fine,stp,sta,tipo,materiale,parteturno):
		self.name=name
		#self.label=self.name
		self.nta=ta[0]
		self.codacc=ta[1]
		fon=BFont()
		self.stp=stp
		self.sta=sta
		self.materiale = materiale
		self.parte=parteturno[0]
		self.totale=parteturno[1]
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
		self.label=(self.nta+"  "+self.name+"  "+stp[0]+"  "+sta[0]+"  "+str(self.inizio)+"  "+str(self.fine)+"  "+self.materiale+"  "+str(parteturno[0])+"/"+str(parteturno[1]))
		BListItem.__init__(self)
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
		self.totale=parteturno[1]
		mi=(inizio.seconds % 3600) // 60
		oi=inizio.days * 24 + inizio.seconds // 3600
		of=fine.days * 24 + fine.seconds // 3600
		mf=(fine.seconds % 3600) // 60
		self.iout=str(oi)+":"+str(mi)
		self.fout=str(of)+":"+str(mf)
		self.label=("vettura"+"  "+self.name+"  "+stp[0]+"  "+sta[0]+"  "+str(self.inizio)+"  "+str(self.fine)+"  "+str(parteturno[0])+"/"+str(parteturno[1]))
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
		self.font_height_value=font_height()
		fon.GetHeight(self.font_height_value)
		self.inizio=inizio
		self.fine=inizio + deltat
		self.parte=parteturno[0]
		self.totale=parteturno[1]
		mi=(inizio.seconds % 3600) // 60
		oi=inizio.days * 24 + inizio.seconds // 3600
		of=self.fine.days * 24 + self.fine.seconds // 3600
		mf=(self.fine.seconds % 3600) // 60
		self.iout=str(oi)+":"+str(mi)
		self.fout=str(of)+":"+str(mf)
		self.label=(self.name+"        "+dove[0]+"  "+dove[0]+"  "+str(self.inizio)+"  "+str(self.fine)+"  "+str(parteturno[0])+"/"+str(parteturno[1]))
		BListItem.__init__(self)
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