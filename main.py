import pgzrun
from random import randint, choice

# Configurações da Janela
WIDTH = 700
HEIGHT = 400
TITLE = "Galaxy Platformer"

game_active = False
music_on = True
score = 0  # Placar do jogo
lives = 1  # Vidas do jogador
music_playing = False  # Controle da música

ground_level = HEIGHT - 50
player = Actor("player_stand", (100, ground_level))
player.vy = 0  # Velocidade vertical

win_message = False  # Controle para exibir mensagem de vitória

def draw():
    screen.clear()
    screen.blit("background", (0, 0))
    
    if not game_active:
        screen.draw.text("MENU PRINCIPAL", center=(WIDTH//2, HEIGHT//4), fontsize=50, color="white")
        screen.draw.text("[S] - Start Game", center=(WIDTH//2, HEIGHT//2), fontsize=30, color="violet")
        screen.draw.text("[M] - Música: {}".format("ON" if music_on else "OFF"), center=(WIDTH//2, HEIGHT//2 + 40), fontsize=30, color="green")
        screen.draw.text("[Q] - Quit Game", center=(WIDTH//2, HEIGHT//2 + 80), fontsize=30, color="purple")
        
        if lives <= 0:
            screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//3), fontsize=80, color="red")
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
        
        # Exibir pontuação e vidas
        screen.draw.text(f"Score: {score}", (10, 10), fontsize=30, color="yellow")
        screen.draw.text(f"Lives: {lives}", (600, 10), fontsize=30, color="red")
        
        if win_message:
            screen.draw.text("GANHOUUUUUUUUUUU", center=(WIDTH//2, HEIGHT//2), fontsize=80, color="red")

def update():
    global game_active, lives, music_on, music_playing
    if not game_active:
        if keyboard.s:
            reset_game()
            if music_on:
                music.stop()
                music.play("background_music")
                music_playing = True
        elif keyboard.m:
            music_on = not music_on
            if music_on and not music_playing:
                music.play("background_music")
                music_playing = True
            else:
                music.stop()
                music_playing = False
    else:
        handle_player_movement()
        check_coin_collision()
        check_enemy_collision()
        for enemy in enemies:
            enemy.update()

def handle_player_movement():
    global win_message
    player.vy += 0.9  # Gravidade
    player.y += player.vy

    if keyboard.right:
        player.x = min(WIDTH, player.x + 4)
    if keyboard.left:
        player.x = max(0, player.x - 4)
    if keyboard.up and is_on_ground():
        player.vy = -12  # Impulso para cima
    if keyboard.up and player.y < 50:  # Ajuste para ativar a vitória no topo da tela
        player_wins()
        win_message = True
    
    for platform in platforms:
        if player.colliderect(platform) and player.vy > 0:
            player.y = platform.top
            player.vy = 0
    
    if player.y >= ground_level:
        player.y = ground_level
        player.vy = 0

def is_on_ground():
    if player.y >= ground_level:
        return True
    for platform in platforms:
        if player.colliderect(platform) and player.vy >= 0:
            return True
    return False

def check_coin_collision():
    global score
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 10

def check_enemy_collision():
    global lives, game_active, music_playing
    for enemy in enemies:
        if player.colliderect(enemy):
            lives -= 1
            music.stop()
            music.play("defeated_music")
            music_playing = False
            if lives <= 0:
                game_active = False
                   
def player_wins():
    music.stop()
    music.play("victory_music")

def reset_game():
    global game_active, score, lives, player, coins, music_playing, win_message
    game_active = True
    score = 0
    lives = 1
    player.pos = (100, ground_level)
    coins = [Actor("coin_image", (randint(50, WIDTH - 50), randint(50, HEIGHT - 100))) for _ in range(30)]
    music.stop()
    music_playing = False
    win_message = False

# Criar plataformas alinhadas
platforms = [Actor("platform_image", (x * 70, HEIGHT - (y * 50))) for x, y in [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                                                                                (6, 6), (6, 1), (7, 2), (8, 3),
                                                                                (9, 4), (10, 5), (4, 7), (6, 8),
                                                                                (8, 9), (10, 10)]]

# Criar paredes alinhadas
walls = [Actor("wall_image", (x * 80, HEIGHT - (y * 50))) for x, y in [(2, 4), (4, 6), (6, 8), (8, 10)]]

# Criar 30 moedas espalhadas
coins = [Actor("coin_image", (randint(50, WIDTH - 50), randint(50, HEIGHT - 100))) for _ in range(30)]

# Criar inimigos
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
