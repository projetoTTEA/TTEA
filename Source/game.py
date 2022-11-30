import pygame
import time
import random

import arquivo
import settings
from settings import *
from background import Background
from car import Car
from pose_tracking import PoseTracking
from target import Target
from obstacle import Obstacle
from camera import Camera
import cv2
import ui

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.background = Background()
        self.pose_tracking = PoseTracking()
        self.car = Car()
        self.config = 'Jogadores/' + arquivo.get_Player() + '_KarTEA_config.csv'


        # Load camera
        self.cap = Camera()

        self.sounds = {}
        self.sounds["slap"] = pygame.mixer.Sound(f"Assets/Kartea/Sounds/point.wav")
        self.sounds["screaming"] = pygame.mixer.Sound(f"Assets/Kartea/Sounds/miss.wav")
        if(arquivo.get_K_SOM(self.config)):
            self.sounds["slap"].set_volume(1)
            self.sounds["screaming"].set_volume(1)
        else:
            self.sounds["slap"].set_volume(0)
            self.sounds["screaming"].set_volume(0)


        settings.TARGETS_MOVE_SPEED = arquivo.get_Nivel()
        if arquivo.get_Nivel() < 3:
            settings.TARGETS_SPAWN_TIME = 8
        elif arquivo.get_Nivel() < 5:
            settings.TARGETS_SPAWN_TIME = 4
        else:
            settings.TARGETS_SPAWN_TIME = 2

        self.targets = []
        self.Last_Obj = -1

        self.score = 0
        self.movimento = 0
        self.alvo = 0
        self.alvo_c = 0
        self.alvo_d = 0
        self.obst = 0
        self.obst_c = 0
        self.obst_d = 0
        self.finish = 0

        settings.score = 0
        settings.movimento = 0
        settings.alvo = 0
        settings.alvo_c = 0
        settings.alvo_d = 0
        settings.obst = 0
        settings.obst_c = 0
        settings.obst_d = 0


        self.SOM = arquivo.get_K_SOM(self.config)
        self.HUD = arquivo.get_K_HUD(self.config)
        settings.GAME_DURATION = arquivo.get_K_TEMPO_NIVEL(self.config)
        self.PAUSE = False

        self.targets_spawn_timer = 0
        self.game_start_time = time.time()
        self.time_left = settings.GAME_DURATION
        settings.TIME_PAST = 0


    def reset(self): # reset all the needed variables
        self.background = Background()
        self.pose_tracking = PoseTracking()
        self.car = Car()

        settings.TARGETS_MOVE_SPEED = arquivo.get_Nivel()
        if arquivo.get_Nivel() < 3:
            settings.TARGETS_SPAWN_TIME = 8
        elif arquivo.get_Nivel() < 5:
            settings.TARGETS_SPAWN_TIME = 4
        else:
            settings.TARGETS_SPAWN_TIME = 2

        self.targets = []
        self.Last_Obj = -1
        self.targets_spawn_timer = 0
        self.game_start_time = time.time()
        self.time_left = settings.GAME_DURATION
        settings.TIME_PAST = 0

        self.score = 0
        self.movimento = 0
        self.alvo = 0
        self.alvo_c = 0
        self.alvo_d = 0
        self.obst = 0
        self.obst_c = 0
        self.obst_d = 0
        self.finish = 0

        settings.score = 0
        settings.movimento = 0
        settings.alvo = 0
        settings.alvo_c = 0
        settings.alvo_d = 0
        settings.obst = 0
        settings.obst_c = 0
        settings.obst_d = 0

    def spawn_targets(self):
        t = time.time()
        if t > self.targets_spawn_timer:
            self.targets_spawn_timer = t + settings.TARGETS_SPAWN_TIME

            # Pega Fase atual do jogador
            fase = arquivo.get_K_FASE(self.config)

            # Pega posicao atual do jogo
            pos = self.background.get_startPos()

            # Cria Target e Obstacle para ser utilizado
            if self.Last_Obj == -1:
                r = random.randint(0, 2)
            else:
                r = self.Last_Obj
                if arquivo.get_Nivel() % 2 == 1:
                    if r == 0:
                        r = 1
                    elif r == 1:
                        while r == self.Last_Obj:
                            r = random.randint(0, 2)
                    else:
                        r = 1
                else:
                    while r == self.Last_Obj:
                        r = random.randint(0, 2)

            self.Last_Obj = r

            target = Target(r)
            obstacle = Obstacle(r)

            print("Last_Obj: ", self.Last_Obj, "time: ", t)

            # Adiciona Target ou Obstacle de acordo com a fase
            if fase == 1:
                self.targets.append(target)
                self.background.lines[pos].target = target
                self.alvo += 1
                settings.Alvo += 1
                arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                    arquivo.get_Nivel(), settings.pista, r, 'Criou Alvo')
            elif fase == 2:
                self.targets.append(obstacle)
                self.background.lines[pos].target = obstacle
                self.obst += 1
                settings.Obst += 1
                arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                    arquivo.get_Nivel(), settings.pista, r, 'Criou Obstaculo')
            else:
                if random.randint(0, 100) < 50:
                    self.targets.append(obstacle)
                    self.background.lines[pos].target = obstacle
                    self.obst += 1
                    settings.Obst += 1
                    arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                    arquivo.get_Nivel(), settings.pista, r, 'Criou Obstaculo')
                else:
                    self.targets.append(target)
                    self.background.lines[pos].target = target
                    self.alvo += 1
                    settings.Alvo += 1
                    arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                    arquivo.get_Nivel(), settings.pista, r, 'Criou Alvo')

    def spawn_finish(self):
        pos = self.background.get_startPos()
        self.background.lines[pos].sprite = pygame.image.load("Assets/Kartea/Finish.png").convert_alpha()
        self.background.lines[pos].spriteX = -0.5

    def load_camera(self):
        self.cap.load_camera()

    def set_feet_position(self):
        self.cap.frame = self.pose_tracking.scan_feets(self.cap.frame)
        (x, y) = self.pose_tracking.get_feet_center()
        Y = SCREEN_HEIGHT - CAR_SIZE/2
        self.car.rect.center = (x, Y)
        #print("x: ", x ," y: ", y)
        """
        if x < SCREEN_WIDTH/3:
            self.car.rect.center = (200, 550)
        elif x >= SCREEN_WIDTH/3 and x <= 2*SCREEN_WIDTH/3:
            self.car.rect.center = (400, 550)
        else:
            self.car.rect.center = (600, 550)
        """

    def draw(self):
        # draw the background

        if not self.PAUSE:
            if arquivo.get_Nivel() < 3:
                self.background.speed1()
            elif arquivo.get_Nivel() < 5:
                self.background.speed2()
            else:
                self.background.speed3()
        else:
            self.background.stop()
        self.background.draw(self.surface)

        # draw the targets
        #for target in self.targets:
        #    target.draw(self.surface)

        # draw the car
        self.car.draw(self.surface)

        if self.HUD:
            # draw the score
            ui.draw_text(self.surface, f"Pontuação : {self.score}", (650, 5), COLORS["score"], font=FONTS["medium"],
                         shadow=True, shadow_color=(255,255,255))
            # draw the time left
            timer_text_color = (160, 40, 0) if self.time_left < 5 else COLORS["timer"] # change the text color if less than 5 s left
            ui.draw_text(self.surface, f"Tempo : {self.time_left}", (350, 5), timer_text_color, font=FONTS["medium"],
                         shadow=True, shadow_color=(255,255,255))
            # draw the fase e nivel
            timer_text_color = (160, 40, 0) if self.time_left < 5 else COLORS["timer"] # change the text color if less than 5 s left
            ui.draw_text(self.surface, f"Fase : {arquivo.get_Fase()}", (5, 5), timer_text_color, font=FONTS["medium"],
                         shadow=True, shadow_color=(255,255,255))
            timer_text_color = (160, 40, 0) if self.time_left < 5 else COLORS["timer"] # change the text color if less than 5 s left
            ui.draw_text(self.surface, f"Nivel : {arquivo.get_Nivel()}", (5, 25), timer_text_color, font=FONTS["medium"],
                         shadow=True, shadow_color=(255,255,255))


    def game_time_update(self):
        #self.time_left = max(round(GAME_DURATION - (time.time() - self.game_start_time), 1), 0)
        self.time_left = settings.GAME_DURATION - int(settings.TIME_PAST/1000)


    def update(self):
        self.load_camera()
        self.set_feet_position()
        if self.PAUSE:
            settings.MENU = 'Pause'
            self.PAUSE = False
            return "menu"
        else:

            self.game_time_update()

            self.draw()

            if self.time_left > 0:
                if self.time_left > (2*settings.TARGETS_SPAWN_TIME):
                    self.spawn_targets()
                else:
                    if self.finish == 0:
                        self.spawn_finish()
                        self.finish += 1
                x, y = self.pose_tracking.get_feet_center() #Obtem posição(x,y) central do jogador
                feet1_x, feet1_y = self.pose_tracking.get_feet1() #Obtem posição(x,y) do pé esquerdo
                feet2_x, feet2_y = self.pose_tracking.get_feet2() #Obtem posição(x,y) do pé direito

                #print("feet1_x: ", feet1_x, ", feet1_y: ", feet1_y, ", feet2_x: ", feet2_x, ", feet2_y: ", feet2_y)
                #print("x: ", x, ", y: ", y, ", feet_x: ", self.feet_x, ", feet_y: ", self.feet_y)

                troca_pista = settings.pista #Armazena a pista que o jogador se encotra
                if (div0_pista <= feet1_x < div1_pista) and (div0_pista <= feet2_x < div1_pista):  #Atualiza a pista do jogador, os 2 pés devem estar na pista
                    settings.pista = 0
                elif (div1_pista <= feet1_x < div2_pista) and (div1_pista <= feet2_x < div2_pista):
                    settings.pista = 1
                elif (div2_pista <= feet1_x < div3_pista) and (div2_pista <= feet2_x < div3_pista):
                    settings.pista = 2
                elif ((feet1_x < div0_pista) and (feet2_x < div0_pista)) or ((feet1_x > div3_pista) and (feet2_x > div3_pista) ):
                    settings.pista = -1 #fora da area de calibracao

                if div0_pista <= x < div1_pista: #Atualiza a pista do jogador de acordo com a posiçao central
                    settings.pista = 0
                elif div1_pista <= x < div2_pista:
                    settings.pista = 1
                elif div2_pista <= x < div3_pista:
                    settings.pista = 2
                else:
                    settings.pista = -1 #fora da area de calibracao

                if settings.pista != troca_pista: #Checa se houve troca de pista
                    print("Trocou da pista ", troca_pista, " para ", settings.pista)
                    if settings.pista != -1 and troca_pista != -1:
                        self.score += 2
                        self.movimento += 1
                        # grava detalhado troca de pista
                        arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                    arquivo.get_Nivel(), settings.pista, troca_pista, 'Trocou de Pista')

                    elif settings.pista == -1:
                        print("Pedeu o Sinal")
                        # gravar detalhado perda sinal
                        arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                                arquivo.get_Nivel(), settings.pista, troca_pista, 'Saiu da area do jogo')
                        self.PAUSE = True
                        settings.pista = 0

                self.car.rect.center = (x, y)
                self.car.left_click = self.pose_tracking.feet_closed
                self.score = self.car.kill_targets(self.surface, self.targets, self.score, self.sounds)
                for alvo in self.targets:
                    if alvo.current_pos[1] > (SCREEN_HEIGHT+100):
                        self.score += alvo.kill(self.surface, self.targets, self.sounds)

            else: # when the game is over
                print("Terminou o Nível!")

                ponto_T = self.alvo * 12 + self.obst * 12

                if self.score >= (3*ponto_T)/4:
                    arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                            arquivo.get_Nivel(), pista, pista,
                                            'Controle Jogo: Avanca Nivel')
                    settings.MENU = 'Feedback_3'
                elif self.score >= ponto_T/4:
                    arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                            arquivo.get_Nivel(), pista, pista,
                                            'Controle Jogo: Permanece Nivel')
                    settings.MENU = 'Feedback_2'
                else:
                    arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                            arquivo.get_Nivel(), pista, pista,
                                            'Controle Jogo: Retrocede Nivel')
                    settings.MENU = 'Feedback_1'

                settings.score = self.score
                settings.movimento = self.movimento
                # Grava sessao
                arquivo.grava_Sessao(arquivo.get_Player(), arquivo.get_Fase(), arquivo.get_Nivel(), self.score,
                                     self.movimento, settings.Alvo_c, settings.Alvo_d, settings.Obst_c, settings.Obst_d)
                return "menu"

            # Eventos Pygame
            for event in pygame.event.get():
                # SAIR
                if event.type == pygame.QUIT:
                    gameExit = True

                    pygame.display.quit()


                if event.type == pygame.KEYDOWN:
                    # Pausar (Space)
                    if event.key == pygame.K_SPACE:
                        print("Space game.py")
                        if self.background.speed == 0:
                            self.PAUSE = False
                            print("Unpause")
                            arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                                    arquivo.get_Nivel(), pista, pista,
                                                    'Controle UFE: Unpause')

                        else:
                            self.PAUSE = True
                            print("Pause")
                            arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                                    arquivo.get_Nivel(), pista, pista,
                                                    'Controle UFE: Pause')
                            self.background.stop()
                            settings.MENU = 'Pause'
                            return "menu"
                    # H/D Som (S)
                    if event.key == pygame.K_s:
                        if self.SOM:
                            self.SOM = False
                            self.sounds["slap"].set_volume(0)
                            self.sounds["screaming"].set_volume(0)
                            arquivo.set_K_SOM(self.config, False)
                            arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                                    arquivo.get_Nivel(), pista, pista,
                                                    'Controle UFE: Desabilita Som')
                        else:
                            self.SOM = True
                            self.sounds["slap"].set_volume(1)
                            self.sounds["screaming"].set_volume(1)
                            arquivo.set_K_SOM(self.config, True)
                            arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                                    arquivo.get_Nivel(), pista, pista,
                                                    'Controle UFE: Habilita Som')
                    # H/D Som (1)
                    if event.key == pygame.K_1:
                        if self.SOM:
                            self.SOM = False
                            self.sounds["slap"].set_volume(0)
                            self.sounds["screaming"].set_volume(0)
                            arquivo.set_K_SOM(self.config, False)
                            arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                                    arquivo.get_Nivel(), pista, pista,
                                                    'Controle UFE: Desabilita Som')
                        else:
                            self.SOM = True
                            self.sounds["slap"].set_volume(1)
                            self.sounds["screaming"].set_volume(1)
                            arquivo.set_K_SOM(self.config, True)
                            arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                                    arquivo.get_Nivel(), pista, pista,
                                                    'Controle UFE: Habilita Som')
                    # H/D HUD (H)
                    if event.key == pygame.K_h:
                        if self.HUD:
                            self.HUD = False
                            arquivo.set_K_HUD(self.config, False)
                            arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                                    arquivo.get_Nivel(), pista, pista,
                                                    'Controle UFE: Desabilita HUD')
                        else:
                            self.HUD = True
                            arquivo.set_K_HUD(self.config, True)
                            arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                                    arquivo.get_Nivel(), pista, pista,
                                                    'Controle UFE: Habilita HUD')
                    # H/D HUD (2)
                    if event.key == pygame.K_2:
                        if self.HUD:
                            self.HUD = False
                            arquivo.set_K_HUD(self.config, False)
                            arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                                    arquivo.get_Nivel(), pista, pista,
                                                    'Controle UFE: Desabilita HUD')
                        else:
                            self.HUD = True
                            arquivo.set_K_HUD(self.config, True)
                            arquivo.grava_Detalhado(arquivo.get_Player(), arquivo.get_Sessao(), arquivo.get_Fase(),
                                                    arquivo.get_Nivel(), pista, pista,
                                                    'Controle UFE: Habilita HUD')

            cv2.waitKey(1)
