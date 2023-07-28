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

        # Asetetaan botin lähtösijainti
        self.x = 320-self.leveys/2
        self.y = 480-self.korkeus

        # Botin rect kolliisioiden tarkistusta varten on ladattua kuvaa pienempi
        self.rect = pygame.Rect(self.x+10, self.y+1, 30, 82)
        
        # Botin liikestatus
        self.oikea = False
        self.vasen = False
        self.hyppy = False
        self.hyppylaskuri = 40

    # Alustaa botin lähtösijainnin ja liikestatuksen
    def alusta(self):        
        self.x = 320-self.leveys/2
        self.y = 480-self.korkeus
        self.liiku(0,0)
        self.oikea = False
        self.vasen = False
        self.hyppy = False
        self.hyppylaskuri = 40

    # Muutetaan botin väri vihreäksi    
    def muunna(self):
        pixels = pygame.PixelArray(self.kuva)
        pixels.replace((192, 192, 192), (0, 204, 51))
        pixels.replace((128, 128, 128), (0, 204, 51))
        pixels.replace((255, 0, 0), (0, 255, 0))
        del pixels

    # Liikutetaan botti
    def liiku(self, dx: int, dy: int):
        self.x += dx
        self.y += dy
        #liikutetaan myös rect
        self.rect.x = self.x
        self.rect.y = self.y

    # Tarkistetaan liikutetaanko bottia
    def eval_liike(self):
        if self.vasen == True and self.x > 0:
            self.liiku(-2,0)
        if self.oikea == True and self.x < 590:
            self.liiku(2,0)
        if self.hyppy == True:
            if self.hyppylaskuri >= -40:
                liike = -(self.hyppylaskuri*0.3)
                self.liiku(0, liike)
                self.hyppylaskuri -= 1
            else:
                self.hyppylaskuri = 40
                self.hyppy = False

class Moerkoe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.kuva = pygame.image.load("hirvio.png").convert_alpha()
        self.leveys = self.kuva.get_width()
        self.korkeus = self.kuva.get_height()
        self.rect = self.kuva.get_rect()

        # sijainti
        self.x = 0
        self.y = 0

        # nopeus
        self.dx = 1
        self.dy = 0

    # Alustaa mörön paikan
    def alusta(self):
        self.x = 0
        self.y = 0

    # Liikuttaa mörköä edestakaisin
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

# Luokka väisteltävien "pommien" käsittelyyn
class Pommi(pygame.sprite.Sprite):
    def __init__(self, morko: Moerkoe):
        pygame.sprite.Sprite.__init__(self)
        
        # Pommit ilmestyvät mörön alapuolelle
        # niiden keskipiste on mörön leveyden keskikohdassa
        self.kp_alussa_x = morko.x+25
        self.kp_alussa_y = 70
        self.kp_x = morko.x+25
        self.kp_y = 70

        # Kolliisiotarkastusta varten määritetään rect 
        # lasketaan vasemman yläkulman koordinaatti keskipisteestä
        self.rect = pygame.Rect(self.kp_x-20, self.kp_y-20, 40, 40)

        # nopeus
        self.dx = 0
        self.dy = 2

    # Määritellään piikkipallon piikkien koordinaatit piirtämistä varten
    def maarita_pallo(self):
        global aika
        koord_lista = []
        for i in range (1, 17, 1):
            radius = 20
            # Joka toisella kehäpisteellä säde on pienempi, jotta saadaan piikit
            if i % 2 == 0:
                radius = 7
            # Kulma muuttuu aikalaskurin mukaan, jotta pallo näyttää pyörivän
            kulma = i * math.pi*2 / 16 + aika * math.pi / 20
            x = self.kp_x + math.cos(kulma) * radius
            y = self.kp_y + math.sin(kulma) * radius
            koord_lista.append((x, y))
        return koord_lista

    # Piirretään pommi edellä laskettujen koordinaattien avulla            
    def piirra(self, naytto):
        pygame.draw.polygon(naytto, (0,153,255), self.maarita_pallo())
        pygame.draw.circle(naytto, (0,255,255), (self.kp_x, self.kp_y), 10)
        pygame.draw.circle(naytto, (255,255,255), (self.kp_x, self.kp_y), 5)

    # Pommi liikkuu paraabelikäyrää pitkin
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

        # Kun pommi on ruudun alareunassa, se jatkaa liikettä ulos ruudusta
        else:
            self.kp_x += self.dx

        # Siirretään myös rect
        self.rect.x = self.kp_x-20
        self.rect.y = self.kp_y-20

# Luokka kerättävien esineiden käsittelyyn
class Kolikko(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Esineiden x-koordinaatti määritellään satunnaisesti
        # Keskipiste
        self.kp_x = (randrange(8, 640-8))
        self.kp_y = -15

        self.rect = pygame.Rect(self.kp_x-15, self.kp_y-15, 30, 30)

        # Kerättävät esineet liikkuvat suoraan alaspäin
        # Nopeus
        self.dx = 0
        self.dy = 1

    # Liikutetaan esinettä
    def liiku(self):
        self.kp_y += self.dy

        # Siirretään myös rect
        self.rect.x = self.kp_x-30
        self.rect.y = self.kp_y-30

    # Piirretään esine 
    def piirra(self, naytto):
        pygame.draw.rect(naytto, (102, 204, 0), (self.kp_x-15, self.kp_y-15, 30, 30))
        pygame.draw.line(naytto, (255, 204, 0), (self.kp_x-3, self.kp_y -14), (self.kp_x-3, self.kp_y+14), width=3)
        pygame.draw.line(naytto, (255, 204, 0), (self.kp_x-10, self.kp_y), (self.kp_x+14, self.kp_y), width=3)
        pygame.draw.line(naytto, (255, 204, 0), (self.kp_x-14, self.kp_y+14), (self.kp_x-10, self.kp_y), width=3)
        pygame.draw.line(naytto, (255, 204, 0), (self.kp_x+3, self.kp_y -14), (self.kp_x+3, self.kp_y), width=3)
        pygame.draw.rect(naytto, (255, 204, 0), (self.kp_x+8, self.kp_y-10, 4, 4))
        pygame.draw.rect(naytto, (102, 102, 102), (self.kp_x-5, self.kp_y-5, 10, 10))

# Tuotetaan valikko pelin aluksi        
def aloitusvalikko(naytto):
    naytto.fill((0, 0, 0))
    fontti1 = pygame.font.SysFont('mono', 40, bold = True)
    fontti2 = pygame.font.SysFont('mono', 20, bold = True)
    otsikko = fontti1.render('Robohamsteri 2100', True, (0, 204, 51))
    alkubotti = Botti()
    alkubotti.muunna()
    kolikko = Kolikko()
    kolikko.kp_x = 220
    kolikko.kp_y = 215
    ohje = fontti2.render('Aloita painamalla s', True, (0, 204, 51))
    naytto.blit(otsikko, (320 - otsikko.get_width()/2, 80))
    kolikko.piirra(naytto)
    naytto.blit(alkubotti.kuva, (alkubotti.x, 170))
    kolikko.kp_x = 420
    kolikko.kp_y = 215
    kolikko.piirra(naytto)
    naytto.blit(ohje, (320 - ohje.get_width()/2, 300))
    pygame.display.update()

# Tuotetaan valikko, kun peli on loppunut
def loppuvalikko(naytto):
    global laskuri
    naytto.fill((0, 0, 0))
    fontti1 = pygame.font.SysFont('mono', 40, bold = True)
    fontti2 = pygame.font.SysFont('mono', 20, bold = True)
    otsikko = fontti1.render('Botti tuhoutui!', True, (0, 204, 51))
    pisteet = fontti2.render(f'Pisteet: {laskuri}', True, (0, 204, 51))
    valikko = fontti2.render('Jatka K/E?', True, (0, 204, 51))
    naytto.blit(otsikko, (320 - otsikko.get_width()/2, 80))
    naytto.blit(pisteet, (320 - pisteet.get_width()/2, 240))
    naytto.blit(valikko, (320 - valikko.get_width()/2, 260))
    pygame.display.update()

# Ajastaa pommien ilmestymisen
def ajastin(tapahtuma):
    pygame.time.set_timer(tapahtuma, randint(100,3000))

# Ajastaa kerättävien esineiden ilmestymisen
def ajastin2(tapahtuma):
    pygame.time.set_timer(tapahtuma, randint(2000,3000))    

# Käsitellään pommit -spriteryhmän toiminnot pommi kerrallaan
def pommi_toiminnot(pommit, naytto):
    if len(pommit) > 0:
        for pommi in pommit:
            pommi.piirra(naytto)
            pommi.liiku()

            if pommi.kp_x < -30 or pommi.kp_x > 650:
                pommit.remove(pommi)

# Käsitellään kolikot -spriteryhmän toiminnot kerättävä esine kerrallaan
def kolikko_toiminnot(kolikot, naytto):
        if len(kolikot) > 0:
            for kolikko in kolikot:
                kolikko.piirra(naytto)
                kolikko.liiku()

                if kolikko.kp_y > 490:
                    kolikot.remove(kolikko)

# Tarkistetaan onko tapahtunut kolliisioita botin ja pommien
# tai botin ja kerättävien kanssa
def tarkista_kolliisiot(botti, pommit, kolikot):
    global laskuri
    global terveys

    pisteet = pygame.sprite.spritecollide(botti, kolikot, True)
    for n in pisteet:
        laskuri += 1

    damage = pygame.sprite.spritecollide(botti, pommit, True)
    for m in damage:
        terveys -= 1

# Alustetaan peli ja muuttujat, kun peli on loppunut ja
# pelaaja haluaa jatkaa pelaamista
def alusta_peli(pommit, kolikot, botti, morko):
    # Nollataan globaali pistelaskuri
    global laskuri
    laskuri = 0
    # Alustetaan robotin terveyslaskuri
    global terveys 
    terveys = 3
    # Tyhjennetään pommilista ja kolikkolista
    pommit.empty()
    kolikot.empty()
    # Alustetaan botin ja mörön paikat
    botti.alusta()
    morko.alusta()
    
# Pelin pääohjelma
def paaohjelma():
    pygame.init()

    # pelin tila: aloitusvalikko / peli / loppu
    tila = "aloitusvalikko"

    # alustetaan näyttö ja kello
    naytto = pygame.display.set_mode((640, 480))
    kello = pygame.time.Clock()
    fontti = pygame.font.SysFont('mono', 20, bold=True)
    
    # Alustetaan globaalit laskurit: aika, pistelaskuri ja botin terveys
    global aika
    aika = 0
    global laskuri
    laskuri = 0
    global terveys 
    terveys = 3

    # Aikalaskuri pommin animointiin
    aikalaskuri = pygame.USEREVENT+1
    pygame.time.set_timer(aikalaskuri, 100)

    # Ajastin pommien satunnaiseen tuottamiseen
    uusi_pommi = pygame.USEREVENT+2
    ajastin(uusi_pommi)

    # Ajastin kerättävien esineiden satunnaiseen tuottamiseen
    uusi_kolikko = pygame.USEREVENT+3
    ajastin2(uusi_kolikko)
    
    # Alustetaan botti ja mörkö oliot ja muunnetaan niiden värit
    botti = Botti()
    botti.muunna()
    morko = Moerkoe()
    morko.muunna()

    # Alustetaan pommilista ja kolikkolista
    pommit = pygame.sprite.Group()
    kolikot = pygame.sprite.Group()

    # Peliluuppi
    while True:
        for tapahtuma in pygame.event.get():
            # Otetaan vastaan keydown-tapahtumat vain kun peli on "peli" -tilassa
            if tapahtuma.type == pygame.KEYDOWN and tila == "peli":
                if tapahtuma.key == pygame.K_a or tapahtuma.key == pygame.K_LEFT:
                    botti.vasen = True
                if tapahtuma.key == pygame.K_d or tapahtuma.key == pygame.K_RIGHT:
                    botti.oikea = True
                if tapahtuma.key == pygame.K_SPACE and botti.hyppy == False:
                    botti.hyppy = True

            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_a or tapahtuma.key == pygame.K_LEFT:
                    botti.vasen = False
                if tapahtuma.key == pygame.K_d or tapahtuma.key == pygame.K_RIGHT:
                    botti.oikea = False

            if tapahtuma.type == aikalaskuri:
                if aika < 60:
                    aika += 1
                else:
                    aika = 0

            # Generoidaan pommeja kun peli on "peli" -tilassa
            if tapahtuma.type == uusi_pommi and tila == "peli":
                pommit.add(Pommi(morko))
                ajastin(uusi_pommi)

            # Generoidaan kerättäviä kun peli on "peli" -tilassa
            if tapahtuma.type == uusi_kolikko and tila == "peli":
                kolikot.add(Kolikko())
                ajastin2(uusi_kolikko)

            if tapahtuma.type == pygame.QUIT:
                exit()

        pygame.display.set_caption("Robohamsteri 2100")

        # Toiminnot kun peli on "aloitusvalikko" -tilassa
        if tila == "aloitusvalikko":
            aloitusvalikko(naytto)
            # Kun pelaaja painaa s-näppäintä, peli vaihtaa "peli" -tilaan
            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                tila = "peli"

        # Toiminnot kun peli on "peli" -tilassa
        elif tila == "peli":

            naytto.fill((0, 0, 0))

            pommi_toiminnot(pommit, naytto)
            kolikko_toiminnot(kolikot, naytto)
            botti.eval_liike()
                            
            naytto.blit(botti.kuva, (botti.x, botti.y))
            naytto.blit(morko.kuva, (morko.x, morko.y))

            morko.liiku()
            tarkista_kolliisiot(botti, pommit, kolikot)

            # Tulostetaan näytölle pisteet ja botin terveys
            teksti = fontti.render(f"pisteet: {laskuri} terveys: {terveys}/3", True, (0, 204, 51))
            naytto.blit(teksti, (5, 5))

            # Kun botti on saanut liikaa vahinkoa, peli menee tilaan "loppu"
            if terveys <= 0:
                tila = "loppu"

        # Toiminnot, kun peli on "loppu" -tilassa
        elif tila == "loppu":
            loppuvalikko(naytto)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_k]:
                alusta_peli(pommit, kolikot, botti, morko)
                tila = "peli"
            if keys[pygame.K_e]:
                pygame.quit()
                quit()

        pygame.display.flip()
        kello.tick(60)

# Ajetaan pääohjelma
paaohjelma()