import pygame, random
from pygame.locals import *

LarguraTela = 400
AlturaTela = 800
velocidade = 10
gravidade = 1
VelocidadeJogo = 10

LarguraChao = 2 * LarguraTela
AlturaChao = 100

LarguraCano = 80
AlturaCano = 500

DistanciaCano = 200

class Passaro(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('bluebird-downflap.png').convert_alpha()]

        self.speed = velocidade

        self.current_image = 0

        self.image = pygame.image.load('bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = LarguraTela / 2
        self.rect[1] = AlturaTela / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]

        self.speed += gravidade

        self.rect[1] += self.speed

    def salto(self):
        self.speed = -velocidade

class Cano(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (LarguraCano,AlturaCano))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = AlturaTela - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= VelocidadeJogo

class Chao(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (LarguraChao, AlturaChao))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = AlturaTela - AlturaChao

    def update(self):
        self.rect[0] -= VelocidadeJogo

def fora_de_tela(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def canos_aleatorios(xpos):
    tamanho = random.randint(100, 300)
    cano = Cano(False, xpos, tamanho)
    canoInver = Cano(True, xpos, AlturaTela - tamanho - DistanciaCano)
    return (cano, canoInver)


def jogo():

    pygame.init()
    tela = pygame.display.set_mode((LarguraTela, AlturaTela))

    fundo = pygame.image.load('background-day.png')
    fundo = pygame.transform.scale(fundo, (LarguraTela, AlturaTela))

    passaroGP = pygame.sprite.Group()
    passaro = Passaro()
    passaroGP.add(passaro)

    chaoGP = pygame.sprite.Group()
    for i in range(2):
        chao = Chao(LarguraChao * i)
        chaoGP.add(chao)

    canoGP = pygame.sprite.Group()
    for i in range(2):
        canos = canos_aleatorios(LarguraTela * i + 800)
        canoGP.add(canos[0])
        canoGP.add(canos[1])


    relogio = pygame.time.Clock()

    while True:
        relogio.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    passaro.salto()

        tela.blit(fundo, (0, 0))

        if fora_de_tela(chaoGP.sprites()[0]):
            chaoGP.remove(chaoGP.sprites()[0])

            new_ground = Chao(LarguraChao - 20)
            chaoGP.add(new_ground)

        if fora_de_tela(canoGP.sprites()[0]):
            canoGP.remove(canoGP.sprites()[0])
            canoGP.remove(canoGP.sprites()[0])

            canos = canos_aleatorios(LarguraTela * 2)

            canoGP.add(canos[0])
            canoGP.add(canos[1])

        passaroGP.update()
        chaoGP.update()
        canoGP.update()

        passaroGP.draw(tela)
        canoGP.draw(tela)
        chaoGP.draw(tela)

        pygame.display.update()

        if (pygame.sprite.groupcollide(passaroGP, chaoGP, False, False, pygame.sprite.collide_mask) or
        pygame.sprite.groupcollide(passaroGP, canoGP, False, False, pygame.sprite.collide_mask)):
            input()
            break
jogo()    
