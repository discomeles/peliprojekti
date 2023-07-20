# TEE RATKAISUSI TÄHÄN:
import pygame
from random import randrange

class Olio():
    def __init__(self, kuva: str):
        # olion grafiikka
        self.image = pygame.image.load(kuva)
        self.leveys = self.image.get_width()
        self.korkeus = self.image.get_height()

        #olion sijainti
        self.x = 0
        self.y = 0

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

class Botti(Olio):
    def __init__(self, kuva: str):
       super().__init__(kuva)

    def move(self, dx: int, dy: int):
        super().move(dx, dy)

class Kivi(Olio):
    def __init__(self, kuva: str):
        super().__init__(kuva)

    def move(self, dx: int, dy: int):
        super().move(dx, dy)


def key_event(key: str, value: bool):
    if value == True:
        if key == pygame.K_LEFT:
            pass
        if key == pygame.K_RIGHT:
            pass
        if key == pygame.K_UP:
            pass
        if key == pygame.K_DOWN:
            pass    

def evaluoi(olio: Olio):
    pass

def init_olio():
    olio = Olio()
    return olio

def paaohjelma():
    pygame.init()
    naytto = pygame.display.set_mode((640, 480))
    kello = pygame.time.Clock()
   
    
    botti = init_olio("robo.png")
    x_max = 640 - botti.leveys
    y_max = 480 - botti.korkeus

    x_koord = -1
    y_koord = -1

    # peliluuppi
    while True:
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                key_event(tapahtuma.key, True)

            if tapahtuma.type == pygame.KEYUP:
                key_event(tapahtuma.key, False)

            if tapahtuma.type == pygame.QUIT:
                exit()


        naytto.fill((0, 0, 0))

        evaluoi(botti)
        naytto.blit(botti.image, (botti.x, botti.y))
        pygame.display.flip()

        kello.tick(60)

paaohjelma()