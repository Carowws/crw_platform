<H1># Galaxy_platform</H1>
Setting a game - escolha: Platformer
PG Zero

Programando em <b>python</b>

import  pgzrun
from random import randint, choice

# Configurações da Janela
WIDTH = 700
HEIGHT = 400
TITLE = "Galaxy Platformer"

game_active = False
music_on = True
score = 0  # Placar do jogo

# Configurações do Jogador
ground_level = HEIGHT - 50
player = Actor("player_stand", (100, ground_level))
player.vy = 0  # Velocidade vertical

def draw():
    screen.clear()
    screen.blit("background", (0, 0))
    
    if not game_active:
        screen.draw.text("MENU PRINCIPAL", center=(WIDTH//2, HEIGHT//4), fontsize=50, color="white")
        screen.draw.text("[S] - Start Game", center=(WIDTH//2, HEIGHT//2), fontsize=30, color="violet")
        screen.draw.text("[M] - Música: {}".format("ON" if music_on else "OFF"), center=(WIDTH//2, HEIGHT//2 + 40), fontsize=30, color="green")
        screen.draw.text("[Q] - Quit Game", center=(WIDTH//2, HEIGHT//2 + 80), fontsize=30, color="purple")
    else:
        player.draw()
        for enemy in enemies:
            enemy.draw()
        for platform in platforms:
            platform.draw()
        for wall in walls:
            wall.draw()
        for coin in coins:
            coin.draw()
        
        # Exibir pontuação
        screen.draw.text(f"Score: {score}", (10, 10), fontsize=30, color="yellow")

def update():
    global game_active, music_on
    if not game_active:
        if keyboard.s:
            game_active = True
            if music_on:
                music.play("background_music")
        elif keyboard.m:
            music_on = not music_on
            if music_on:
                music.play("background_music")
            else:
                music.stop()
        elif keyboard.q:
            exit()
    else:
        handle_player_movement()
        check_coin_collision()
        for enemy in enemies:
            enemy.update()

def handle_player_movement():
    player.vy += 0.8  # Gravidade
    player.y += player.vy

    # Movimento lateral
    if keyboard.right:
        player.x = min(WIDTH, player.x + 4)
    if keyboard.left:
        player.x = max(0, player.x - 4)

    # Pulo
    if keyboard.up and is_on_ground():
        player.vy = -12  # Impulso para cima

    # Colisão com plataformas
    for platform in platforms:
        if player.colliderect(platform) and player.vy > 0:
            player.y = platform.top
            player.vy = 0

    # Garante que o jogador não caia do chão
    if player.y >= ground_level:
        player.y = ground_level
        player.vy = 0

def is_on_ground():
    """Verifica se o jogador está no chão ou em uma plataforma"""
    if player.y >= ground_level:
        return True
    for platform in platforms:
        if player.colliderect(platform) and player.vy >= 0:
            return True
    return False

def check_coin_collision():
    """Verifica se o jogador toca nas moedas e remove a moeda"""
    global score
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 10  # Adiciona pontos

// Criar plataformas em escada e espalhadas como um labirinto
platforms = [Actor("platform_image", (x * 70, HEIGHT - (y * 50))) for x, y in [(1, 1), (2, 2), (3, 3), (4, 4),
                                                                                (6, 1), (7, 2), (8, 3), (9, 4),
                                                                                (3, 5), (5, 6), (7, 7), (2, 8),
                                                                                (4, 9), (6, 10), (8, 11)]]

// Criar paredes como obstáculos
walls = [Actor("wall_image", (randint(100, 600), randint(100, 500))) for _ in range(10)]

// Criar 25 moedas espalhadas
coins = [Actor("coin_image", (randint(50, WIDTH - 50), randint(50, HEIGHT - 100))) for _ in range(25)]

// Criar inimigos
class Enemy(Actor):
    def __init__(self, image, pos):
        super().__init__(image, pos)
        self.speed = choice([-3, -2, 2, 3])
    def update(self):
        self.x += self.speed
        if self.x >= WIDTH or self.x <= 0:
            self.speed = -self.speed

enemies = [Enemy("enemy_image", (randint(50, WIDTH - 50), randint(100, HEIGHT - 200))) for _ in range(5)]

pgzrun.go()
