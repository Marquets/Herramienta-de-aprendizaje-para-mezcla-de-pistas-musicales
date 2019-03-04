from reaper_python import *
import pygame
import view
import math
import numpy as np
import random



# Clase Sphere: Esta clase se utiliza para representar cada pista/instrumento que queremos mezclar
# Atributos: - int size, pos x, pos y, nombre de pista /instrumento, url imagen
# 
# 
BLOCK_SIZE = 50

class Sphere(pygame.sprite.Sprite):
	def __init__(self,position):
		super().__init__()
		self.size = 200  #50
		self.name = "esfera"
		self.volume_val = 0.5  #1
		self.pan = 0
		self.position = position
		self.color = None
		self.image = pygame.image.load("C:/Program Files (x86)/REAPER/InstallData/Scripts/TFG/ESFERA.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (self.size,self.size))
		self.rect = self.image.get_rect()
		self.rect.center = self.position

	def resizeSphere(self,image):
		self.image = image
		self.image = pygame.transform.scale(self.image,(self.size,self.size)).convert_alpha()
		self.rect = self.image.get_rect()
	

class Effect_Sphere(pygame.sprite.Sprite):
	def __init__(self,position,name):
		super().__init__()
		self.size = 50
		self.name = name
		self.position = position
		if self.name == "comp":
			self.image = pygame.image.load("C:/Program Files (x86)/REAPER/InstallData/Scripts/TFG/ESFERA-AZUL.png").convert_alpha()
		elif self.name =="eq":
			self.image = pygame.image.load("C:/Program Files (x86)/REAPER/InstallData/Scripts/TFG/ESFERA-VERDE.png").convert_alpha()
		elif self.name == "fx":
			self.image = pygame.image.load("C:/Program Files (x86)/REAPER/InstallData/Scripts/TFG/ESFERA-VIOLETA.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (self.size,self.size))
		self.rect = self.image.get_rect()
		self.rect.center = self.position
		


def loadTracks(all_info):
	num_tracks = RPR_CountTracks(0)
	if num_tracks > len(all_info[0]):
		new_tracks = num_tracks - len(all_info[0])
		for x in range(new_tracks):
			track = RPR_GetSelectedTrack(0,x)
			pos = int(RPR_GetMediaTrackInfo_Value(track,"IP_TRACKNUMBER"))
			all_info[0].insert(pos - 1,(track,RPR_GetMediaTrackInfo_Value(track,"D_VOL"),RPR_GetMediaTrackInfo_Value(track,"D_PAN")))
			RPR_SetMediaTrackInfo_Value(all_info[0][pos - 1],"D_VOL", 0.5)
			all_info[1].insert(pos - 1,Sphere((random.randint(0,view.screen_width),random.randint(0,view.screen_height))))


def deleteTracks(tracks):
	num_tracks = RPR_CountTracks(0)
	if num_tracks < len(tracks[0]):
		for i, s in enumerate(tracks[0]):
			valide = RPR_ValidatePtr2(0, tracks[0][i][0] , "MediaTrack*")
			if valide == False:
				tracks[0].pop(i)
				tracks[1].pop(i)


def setVolume(tracks,num_track,event):
	
	vol_val = RPR_GetMediaTrackInfo_Value( tracks[0][num_track][0], "D_VOL" )

	#if 0 <= tracks[1][num_track].size <= 210:

	vol_db = 20*math.log(vol_val,10)

	if event.button == 4:
		vol_db += 0.1 * 10
	else:
		vol_db -= 0.1 * 10

	vol_val = math.fabs(10**(vol_db/20))
	tracks[1][num_track].volume_val = vol_val
	RPR_SetMediaTrackInfo_Value(tracks[0][num_track][0],"D_VOL", tracks[1][num_track].volume_val)
	tracks[1][num_track].size = int (tracks[1][num_track].volume_val * 200)
	tracks[1][num_track].resizeSphere(tracks[1][num_track].image)
	tracks[1][num_track].rect.center = (event.pos[0],event.pos[1])

def setVolumeFromReaper(tracks):
	for i in range(len(tracks)):
		if RPR_IsTrackSelected(tracks[0][i][0]):
			vol_val = RPR_GetMediaTrackInfo_Value( tracks[0][i][0], "D_VOL" )
			if vol_val != tracks[1][i].volume_val:
				tracks[1][i].volume_val = vol_val
				RPR_SetMediaTrackInfo_Value(tracks[0][i][0],"D_VOL", tracks[1][i].volume_val)
				tracks[1][i].size = int (tracks[1][i].volume_val * 200)
				tracks[1][i].resizeSphere(tracks[1][i].image)
				

def setPan(tracks,num_track,event,offset_x,offset_y):
	mouse_x, mouse_y = event.pos
	tracks[1][num_track].rect.x = mouse_x + offset_x
	RPR_SetMediaTrackInfo_Value(tracks[0][num_track][0],"D_PAN",(mouse_x/(view.screen_width//2)) - 1 )
	tracks[1][num_track].rect.y = mouse_y + offset_y


def setPanFromReaper(tracks):
	for i in range(len(tracks)):
		if RPR_IsTrackSelected(tracks[0][i][0]):
			pan_val = RPR_GetMediaTrackInfo_Value( tracks[0][i][0], "D_PAN" )
			if pan_val != tracks[1][i].pan:
				tracks[1][i].pan = pan_val
				RPR_SetMediaTrackInfo_Value(tracks[0][i][0],"D_PAN", tracks[1][i].pan)
				tracks[1][i].rect.x = (2*(tracks[1][i].pan + 1))/view.screen_width
				

def checkDinamicRange():
	x = 0
	num_tracks = RPR_CountTracks(0)
	master = RPR_GetTrack(0,0)
	# Sacamos el peak del master
	peak = RPR_Track_GetPeakInfo(master, 1)
	# Sacamos el RMS de todas las pistas
	for i in range(num_tracks):
		peak_value = RPR_Track_GetPeakInfo(RPR_GetTrack(0,i), 1)
		x += peak_value**2

	rms = math.sqrt(x/num_tracks)

	# Hacemos diferencia
	dif = peak - rms
	# Guardamos en .txt
	f = open("C:/Program Files (x86)/REAPER/InstallData/Scripts/TFG/Analisis.txt", "w")
	f.write("--------Analisis de mezcla--------\n")
	f.write("----------------------------------" + "\n")
	f.write("Rango dinámico " + "\n")
	f.write("Peak: " + str(peak) +"\n")
	f.write("RMS: " + str(rms) +"\n")
	f.write("El rango dinámico de la mezcla es: " + str(dif) +"\n")
	f.write("----------------------------------" + "\n")
	f.close()

#Planos de mezcla
# Usar los peaks de las pistas?
def checkVolume(tracks):
	volumenes = []
	for i in range(len(tracks)):
		volumenes.append(tracks[1][i].volume_val)

	media = np.median(volumenes)
	desviación = np.std(volumenes)

	f = open("C:/Program Files (x86)/REAPER/InstallData/Scripts/TFG/Analisis.txt", "a")
	f.write("Planos de mezcla " + "\n")
	f.write("Media: " + str(media) +"\n")
	f.write("Desviación típica: " + str(desviación) +"\n")
	f.write("----------------------------------" + "\n")

	# Creo que habría que calcular una variable estadistica como la desviación típica (0, +infinito)
	# Cuanto menor es el valor de la d.t mayor es la concentración de los valores alrededor de la media.
	# Luego si hay tres esferas con valores (3,4,5) la media sería como 4,5 luego la desvición típica será pequeña y
	# querrá decir que los valores estan muy cerca de la media luego no hay planos notables

#Campo estereo de la mezcla
# Se trataría de calcular la distancia de las esferas al eje central y la mayor o
# menor concentración de esferas en el centro.
# También se dan por hecho varias "normas" de mezcla: 
# - bajo, bombo y voz deben estar muy cerca del eje central
# - Elementos rítmicos, coros, teclados abiertos a izquierda y derecha.
def checkStereoField(tracks):

	posiciones = []
	for i in range(len(tracks)):
		posiciones.append(math.fabs(500 - tracks[1][i].position[0]))

	media = np.median(posiciones)

	f = open("C:/Program Files (x86)/REAPER/InstallData/Scripts/TFG/Analisis.txt", "a")
	f.write("Campo estereo " + "\n")
	f.write("Media: " + str(media) +"\n")
	f.write("----------------------------------" + "\n")
