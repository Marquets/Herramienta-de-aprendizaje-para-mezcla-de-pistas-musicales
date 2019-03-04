import model
import view
import pygame
import math
import time
from reaper_python import *

all_tracks_info = []
all_tracks_info.insert(0,[])
all_tracks_info.insert(1,[])
effect_spheres = []

def start():
    pygame.init()
    pygame.font.init() 
    screen = view.startView()[0]
    fondo = view.startView()[1]

    # 0 -> tracks ; 1 -> spheres 
    
    
    #view.drawSpheres(screen,fondo,spheres)

    selected = None
    clock = pygame.time. Clock()
    is_running = True
    while is_running:
    # --- events ---
        screen.fill(view.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                #ESTO ES PARA QUE SE BORREN LAS IMAGENES DE LAS ESFERAS (tal vez merece la pena que se conserven cuando guardemos)
                # for i in enumerate(all_tracks_info[1]):
                #     path = "C:/Program Files (x86)/REAPER/InstallData/Scripts/TFG/Track"+ str(i + 1) + ".png"
                #     os.remove(path , *, dir_fd=None)
                #pygame.display.quit()
                return pygame.quit()
     
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False
     
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, s in enumerate(all_tracks_info[1]):
                        if s.rect.collidepoint(event.pos):
                            selected = i
                            mouse_x, mouse_y = event.pos
                            offset_x = all_tracks_info[1][selected].rect.x - mouse_x
                            offset_y = all_tracks_info[1][selected].rect.y - mouse_y
                           
                    for j, s in enumerate(effect_spheres):
                        if s.rect.collidepoint(event.pos): 
                            if s.name == "comp":
                                RPR_TrackFX_GetByName(all_tracks_info[0][i][0], "ReaComp", True)
                                RPR_TrackFX_SetOpen(all_tracks_info[0][i][0], i, True)

                            if s.name == "eq":
                                RPR_TrackFX_GetByName(all_tracks_info[0][i][0], "ReaEQ", True)
                                RPR_TrackFX_SetOpen(all_tracks_info[0][i][0], i, True)

                            if s.name == "fx":
                                RPR_TrackFX_SetOpen(all_tracks_info[0][i][0], i, True)

                                #esto era para abrir la lista de efectos
                                # JS_Window_OnCommand( windowHWND, commandID)


                if event.button == 3:
                    #ESTO A UNA FUNCION AL MODEL
                    for i, s in enumerate(all_tracks_info[1]):
                        if s.rect.collidepoint(event.pos):                            

                            effect_spheres.append(model.Effect_Sphere(s.rect.topright,"comp"))
                            effect_spheres.append(model.Effect_Sphere(s.rect.topleft,"eq"))
                            effect_spheres.append(model.Effect_Sphere(s.rect.midbottom,"fx"))
                            

                if event.button == 4: 
                    for i, s in enumerate(all_tracks_info[1]):
                        if s.rect.collidepoint(event.pos):
                            selected = i

                            view.setTrackColor(all_tracks_info,selected)
                            model.setVolume(all_tracks_info,selected,event)
                               
                if event.button == 5:
                    for i, s in enumerate(all_tracks_info[1]):
                        if s.rect.collidepoint(event.pos):
                            selected = i

                            view.setTrackColor(all_tracks_info,selected)
                            model.setVolume(all_tracks_info,selected,event)

                            

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selected = None
                    
            elif event.type == pygame.MOUSEMOTION:
                if selected is not None: 
                    #ESTO A UNA FUNCION AL MODEL
                    #fondo = view.setBackground(fondo)
                    view.removeSpheres(effect_spheres)
                    model.setPan(all_tracks_info,selected,event, offset_x,offset_y)
                    fx = RPR_TrackFX_GetEQ(all_tracks_info[0][selected][0], True)
                    RPR_TrackFX_SetPreset(all_tracks_info[0][selected][0],fx, "stock - Track Default")
                    RPR_TrackFX_SetParam(all_tracks_info[0][selected][0], fx, 13, mouse_y/700 )

            elif event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
               fondo = view.resizeWindow(event.w, event.h)
                      
            # --- objects events ---
     
            '''
           button.handle_event(event)
           '''
           
        # --- updates ---
     
        RPR_UpdateArrange()
        
        # --- draws ---

        screen.blit(fondo,(0,0))

        num_tracks = RPR_CountTracks(0)
        if num_tracks != 0:
            model.loadTracks(all_tracks_info)
            view.drawSpheres(screen,all_tracks_info)
            #model.setVolumeFromReaper(all_tracks_info)
            #model.setPanFromReaper(all_tracks_info)
            view.drawEffectSpheres(screen,effect_spheres)

            # evaluacion
            model.checkDinamicRange()
            model.checkStereoField(all_tracks_info)
            model.checkVolume(all_tracks_info)

            # función pendiente de borrar pistas
            model.deleteTracks(all_tracks_info)

        pygame.display.update()

        #time.sleep(pygame.time.get_ticks() - clock.get_time())
        
     
    # --- the end ---

    pygame.quit()
if __name__ == "__main__":
    #running controller function
    start()
