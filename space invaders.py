import pygame #importa o modulo de jogos do python 
import os
import time
import random
pygame.font.init() #inicializa a fonte que vamos usar pra escrever depois

WIDTH, HEIGHT = 750, 750 #tamanho da janela que vai ser criada
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #cria a função WIN e define que ela sempre usará o WIDHT e HEIGHT definidos 
pygame.display.set_caption("Space Shooters") #define o que vai ser escrito na descrição da janela 

# Load images
# Sintaxes usadas para carregar as imagens que serão usadas no jogo, criando uma função para chama-las dinamicamente depois
#assets = nome da pasta onde as imagens estão
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red.png")) 
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
# Player ship
YELLOW_SPACE_SHIP = pygame.image.load (os.path.join("assets", "pixel_ship_yellow.png"))
# Lasers
RED_LASER = pygame.image.load (os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load (os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load (os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load (os.path.join("assets", "pixel_laser_yellow.png"))

#Background
BG = pygame.transform.scale (pygame.image.load (os.path.join("assets", "background-black.png")), (WIDTH,HEIGHT))
# usando transform acima para redimensionar o tamanho da imagem  usada pra background para preencher a tela inteira do jogo 


class Ship:
    def __init__(self, x, y, health=100): #define as características do objeto na classe Ship
        self.x = x #define coordenada x
        self.y = y #define coordenada y
        self.health = health #define que a vida do objeto será baseada no parametro health
        self.ship_img = None #define a imagem que será usada para ser a imagem da nave
        self.laser_img = None #define qual laser será usado por imagem 
        self.lasers = []
        self.cool_down_counter = 0 #define um tempo de intervalo para que o jogador nao consiga usar infinitamente o seu laser

    def draw(self, window):
        window.blit(self.ship_img ,(self.x, self.y))
    
    def get_width(self):
        return self.ship_img.get_width() #dá as coordenadas de tamanho e largura da imagem escolhida para colisões

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health) #super vai chamar as características da classe que herdou (no caso a classe Player vai herdar características da classe Ship)
        self.ship_img = YELLOW_SPACE_SHIP #define qual vai ser a nave da classe Player
        self.laser_img = YELLOW_LASER #define o laser da classe Player
        self.mask = pygame.mask.from_surface(self.ship_img) #módulo MASK diz possibilita o jogo a ter colisões perfeitamente na escala de pixel-pixel
        self.max_health = health
    
class Enemy(Ship):
    COLOR_MAP = { # cria os placeholders para cada cor no momento de criar as naves inimigas
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
                }

    def __init__(self, x, y, color, health=100): 
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)


    def move(self, vel):
        self.y += vel 

def main():
    run = True # valor default do loop
    FPS = 60 # velocidade que o jogo rodará
    level = 0 # numero do nível inicial
    lives = 6 # vidas iniciais do jogador
    main_font = pygame.font.SysFont("comicsans", 50) #define qual fonte e qual tamanho da fonte irá usar
    lost_font = pygame.font.SysFont("comicsans", 60) #define uma variação da fonte para ser usada na tela de "game over"
    player_vel = 5 # define a velocidade do movimento da nave do player
    player = Player (300,650) #define onde a nave irá aparecer inicialmente , armazenando no parametro do objeto ship self.y e self.x
    clock = pygame.time.Clock()
    enemies = [] #cria a lista de inimigos
    wave_length = 5 #determina o numero de inimigos que será gerado em cada onda 
    enemy_vel = 1 #determina a velocidade inicial do inimigo
    lost = False 
    lost_count = 0 #numero inicial do contador de vidas perdidas

    def redraw_window():
        WIN.blit(BG, (0, 0))
        #draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10,10)) # usa o método blit para escrever o label lives na coordenada 10,10 da tela
        WIN.blit(level_label, (WIDTH - level_label.get_width()-10,10)) #usa o metodo get_width e -10 ,10 pixels de coornedana para escrever na direita da tela independente do tamanho da tela]

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw (WIN) #comando para desenhar a variável player na janela 

        if lost:
            lost_label = lost_font.render ("You Lost!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 -lost_label.get_width()/2,350))

        pygame.display.update() #comando para atualizar a janela do jogo

    while run:
        clock.tick(FPS) #determina que o tickrate do jogo será baseado no FPS setado na constante

        redraw_window() #chama a função redraw_window

        if lives <= 0 or player.health <= 0: 
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3: #comando para fechar o jogo
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100),random.randrange(-1500,-100), random.choice(["red", "blue", "green"])) #escolhe randomicamente onde e qual cor de inimigo vai spawnar , definidos por range
                enemies.append(enemy)

        for event in pygame.event.get():  #determina que o loop deverá se encerrar se o evento QUIT acontecer
            if event.type == pygame.QUIT:
                run = False 

        keys = pygame.key.get_pressed() #movimentação da nave usando a função de tecla pressionada
        if keys[pygame.K_a] and player.x -player_vel > 0: #move left , se a tecla "a" for pressionada , e a nave não estiver de acordo com sua velocidade em uma coordenada menor que 0 , a nave irá se deslocar no eixo X 
            player.x -= player_vel # deslocando na direção negativa da coorndenada x , na velocidade definida na constante "player_vel"
        
        if keys[pygame.K_d] and player.x +player_vel + player.get_width() < WIDTH : #move right , se a tecla "d" for pressionada e a nave não estiver em uma coordenada maior que a largura da tela ou a largura da superficie a nave irá se deslocar positivamente na relação do eixo x 
            player.x += player_vel # deslocando na velocidade definida na constante "player_vel"
        
        if keys[pygame.K_w] and player.y -player_vel > 0: #move up , mesmo conceito de "move left"
            player.y -= player_vel
        
        if keys[pygame.K_s] and player.y +player_vel + player.get_height() <  HEIGHT : #move down , mesmo conceito de "move right"
            player.y += player_vel

        for enemy in enemies[:]: #[:] faz uma cópia da lista enemies para que nao altere na lista inicial
            enemy.move(enemy_vel) #indica que o enemy vai se mover na velocidade correta indicada
            if enemy.y + enemy.get_height() > HEIGHT: #feito para quando o inimigo sair da tela de jogo seja subtraido uma das vidas e aquele inimigo seja removido da lista 
                lives -=1
                enemies.remove (enemy)

        
main()
