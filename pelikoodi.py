# TEE RATKAISUSI TÄHÄN:
import pygame
import math
from random import randrange, randint

# Käytetään apuna pygamen sprite-luokkaa
class Botti(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.kuva = pygame.image.load("robo.png").convert_alpha()
        self.leveys = self.kuva.get_width()
        self.korkeus = self.kuva.get_height()

        #Asetetaan botin lähtösijainti
        self.x = 320-self.leveys/2
        self.y = 480-self.korkeus

    # Muutetaan botin väri vihreäksi    
    def muunna(self):
        pixels = pygame.PixelArray(self.kuva)
        pixels.replace((192, 192, 192), (0, 204, 51))
        pixels.replace((128, 128, 128), (0, 204, 51))
        pixels.replace((255, 0, 0), (0, 255, 0))
        del pixels

    def liiku(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

class Moerkoe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.kuva = pygame.image.load("hirvio.png").convert_alpha()
        self.leveys = self.kuva.get_width()
        self.korkeus = self.kuva.get_height()

        #sijainti
        self.x = 0
        self.y = 0

        #nopeus
        self.dx = 1
        self.dy = 0

    def liiku(self):
        if self.dx > 0 and self.x >= 590:
            self.dx = -self.dx
        if self.dx < 0 and self.x <= 0:
            self.dx = -self.dx  
        self.x += self.dx


    # Muutetaan mörön väri violetiksi
    def muunna(self):
        pixels = pygame.PixelArray(self.kuva)
        pixels.replace((0, 0, 0), (153, 0, 255))
        del pixels

class Pommi(pygame.sprite.Sprite):
    def __init__(self, morko: Moerkoe):
        pygame.sprite.Sprite.__init__(self)

        #self.image = pygame.Surface([30, 30])
        #self.image.fill((255,255,255))

        # keskipiste
        self.kp_alussa_x = morko.x
        self.kp_alussa_y = 70
        self.kp_x = morko.x+25
        self.kp_y = 70

        # nopeus
        self.dx = 0
        self.dy = 2

    # Määritellään piikkipallon piikkien koordinaatit
    def maarita_pallo(self):
        global aika
        koord_lista = []
        for i in range (1, 17, 1):
            radius = 20
            if i % 2 == 0:
                radius = 7
            # Kulma muuttuu aikalaskurin mukaan
            kulma = i * math.pi*2 / 16 + aika * math.pi / 20
            x = self.kp_x + math.cos(kulma) * radius
            y = self.kp_y + math.sin(kulma) * radius
            koord_lista.append((x, y))
        return koord_lista
            
    def piirra(self, naytto):
        pygame.draw.polygon(naytto, (0,153,255), self.maarita_pallo())
        pygame.draw.circle(naytto, (0,255,255), (self.kp_x, self.kp_y), 10)
        pygame.draw.circle(naytto, (255,255,255), (self.kp_x, self.kp_y), 5)

    def liiku(self):
        y_muutos = abs(self.kp_y-self.kp_alussa_y)
        lis = ((y_muutos/2)*0.01)**2

        if self.kp_y < 480 - 20:
            self.kp_y += self.dy
            if self.kp_alussa_x < 320:
                self.dx = lis    
            if 320 <= self.kp_alussa_x:
                self.dx = -lis
            self.kp_x += self.dx

        else:
            self.kp_x += self.dx

class Kolikko(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #keskipiste
        self.kp_x = (randrange(8, 640-8))
        self.kp_y = -15

        #nopeus
        self.dx = 0
        self.dy = 1

    def liiku(self):
        self.kp_y += self.dy

    def piirra(self, naytto):
        pygame.draw.circle(naytto, (255,204,0), (self.kp_x, self.kp_y), 15)
        pygame.draw.circle(naytto, (255,153,0), (self.kp_x, self.kp_y), 10)
        pygame.draw.line(naytto, (153, 51, 0), (self.kp_x, self.kp_y -5), (self.kp_x, self.kp_y +5), width=3)

def key_event(key: str, value: bool):
    if value == True:
        if key == pygame.K_LEFT:
            pass
        if key == pygame.K_RIGHT:
            pass
        if key == pygame.K_UP:
            # hyppy
            pass
        if key == pygame.K_DOWN:
            pass    

def ajastin(tapahtuma):
    pygame.time.set_timer(tapahtuma, randint(100,3000))

def ajastin2(tapahtuma):
    pygame.time.set_timer(tapahtuma, randint(2000,3000))    

def pommi_toiminnot(pommit, naytto):
    if len(pommit) > 0:
        for pommi in pommit:
            pommi.piirra(naytto)
            pommi.liiku()

            if pommi.kp_x < -30 or pommi.kp_x > 650:
                pommit.remove(pommi)

def kolikko_toiminnot(kolikot, naytto):
        if len(kolikot) > 0:
            for kolikko in kolikot:
                kolikko.piirra(naytto)
                kolikko.liiku()

                if kolikko.kp_y > 490:
                    kolikot.remove(kolikko)

def paaohjelma():
    pygame.init()
    naytto = pygame.display.set_mode((640, 480))
    kello = pygame.time.Clock()
    global aika
    aika = 0



    # aikalaskuri pommin animointiin
    aikalaskuri = pygame.USEREVENT+1
    pygame.time.set_timer(aikalaskuri, 100)

    # ajastin pommien satunnaiseen tuottamiseen
    uusi_pommi = pygame.USEREVENT+2
    ajastin(uusi_pommi)

    uusi_kolikko = pygame.USEREVENT+3
    ajastin2(uusi_kolikko)
    
    botti = Botti()
    botti.muunna()

    morko = Moerkoe()
    morko.muunna()

    # pommilistan alustaminen
    pommit = []
    kolikot = []

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

            if tapahtuma.type == aikalaskuri:
                if aika < 60:
                    aika += 1
                else:
                    aika = 0

            if tapahtuma.type == uusi_pommi:
                pommit.append(Pommi(morko))
                ajastin(uusi_pommi)

            if tapahtuma.type == uusi_kolikko:
                kolikot.append(Kolikko())
                ajastin2(uusi_kolikko)

            if tapahtuma.type == pygame.QUIT:
                exit()


        naytto.fill((0, 0, 0))

        pommi_toiminnot(pommit, naytto)
        kolikko_toiminnot(kolikot, naytto)
                
        naytto.blit(botti.kuva, (botti.x, botti.y))
        naytto.blit(morko.kuva, (morko.x, morko.y))

        
        morko.liiku()

        pygame.display.flip()

        kello.tick(60)

paaohjelma()