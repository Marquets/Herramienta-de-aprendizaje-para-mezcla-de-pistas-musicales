import pygame 
#import tkinter
from reaper_python import *
from PIL import Image
from transforms import RGBTransform
# -- Constants

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
TRANSPARENT = ( 0, 0, 0, 0)
screen_width = 1000
screen_height = 700


def startView():
	results = []
	screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
	fondo = pygame.image.load("C:/Program Files (x86)/REAPER/InstallData/Scripts/TFG/fondo.jpg")
	fondo = pygame.transform.scale(fondo,(screen_width, screen_height))
	pygame.display.set_caption("Visual Mixer")
	results.append(screen)
	results.append(fondo)
	return results

def resizeWindow(width, height):
	screen_width = width
	screen_height = height
	screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
	fondo = pygame.image.load("C:/Program Files (x86)/REAPER/InstallData/Scripts/TFG/fondo.jpg")
	fondo = pygame.transform.scale(fondo,(screen_width, screen_height))
	return fondo

def drawSpheres(screen,tracks):
	retval = False
	buf = "" 
	buf_sz = 15
	for i, s in enumerate(tracks[1]):
		screen.blit(s.image,s.rect)
		retval, track, buf, buf_sz = RPR_GetTrackName(tracks[0][i][0], buf, buf_sz )
		#if tracks[1][i].name != buf:
		myfont = pygame.font.SysFont('Arial', 20)
		textsurface = myfont.render(buf, False, (0, 0, 0))
		screen.blit(textsurface,tracks[1][i].rect)
		tracks[1][i].name = buf
		

def drawEffectSpheres(screen,spheres):
	for s in spheres:
		screen.blit(s.image,s.rect)


def removeSpheres(spheres):
	for s in spheres:
		s.image.fill(TRANSPARENT)

def setBackground(fondo) :
	fondo.fill(BLACK)
	fondo = pygame.image.load("C:/Program Files (x86)/REAPER/InstallData/Scripts/TFG/fondo.jpg")
	fondo = pygame.transform.scale(fondo,(screen_width, screen_height))

	return fondo

def setTrackColor(tracks,num_track):

	#for i in range(len(tracks[1])):
	current_color = tracks[1][num_track].color
	if tracks[1][num_track].size >= 126:
		#color saturación (179, 2, 0)
		tracks[1][num_track].color = (179, 2, 0)
	elif tracks[1][num_track].size  <= 20:
		#umbral minimo (112, 122, 203)
		tracks[1][num_track].color = (112, 122, 203)
	else:
		color = RPR_GetTrackColor(tracks[0][num_track][0])
		rOut = 0
		gOut = 0
		bOut = 0
		color, rOut, gOut, bOut = RPR_ColorFromNative(color, rOut, gOut, bOut)
		tracks[1][num_track].color = (rOut, gOut, bOut)

	#if current_color != tracks[1][i].color:
	image = Image.open("C:/Program Files (x86)/REAPER/InstallData/Scripts/TFG/ESFERA.png")
	rgb = RGBTransform().mix_with(tracks[1][num_track].color,factor= .60).applied_to(image)	
	url = "C:/Program Files (x86)/REAPER/InstallData/Scripts/TFG/Track"+ str(num_track + 1) + ".png"
	rgb.save(url)
	tracks[1][num_track].image = pygame.image.load(url).convert_alpha()
	tracks[1][num_track].image = pygame.transform.scale(tracks[1][num_track].image,(tracks[1][num_track].size,tracks[1][num_track].size))		
		
def drawButton(screen):
	#rect = pygame.Rect(50, 700,40, 30)
	# myfont = pygame.font.SysFont('Arial', 20)
	# textsurface = myfont.render("Evaluar", False, (0, 0, 0))
	# fondo.blit(textsurface,rect)
	pygame.draw.rect(screen, WHITE, (200,150,100,50))

		
				