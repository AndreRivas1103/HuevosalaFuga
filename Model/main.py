import pygame

# Inicialización de PyGame
pygame.init()

# Constantes globales
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
JUMP_FORCE = -12
MOVE_SPEED = 5

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)


# Estados del juego
class GameState:
    MENU = 0
    PLAYING = 1


# Clase para el jugador (huevo)
class Egg:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

        # Crear imagen del huevo
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)
        pygame.draw.ellipse(self.image, YELLOW, (0, 0, self.width, self.height))

        self.rect = pygame.Rect(x, y, self.width, self.height)

    def move(self, direction):
        self.vel_x = direction * MOVE_SPEED

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_FORCE
            self.on_ground = False

    def update(self, platforms):
        # Gravedad
        if not self.on_ground:
            self.vel_y += GRAVITY

        # Actualizar posición
        self.x += self.vel_x
        self.y += self.vel_y

        # Límites de pantalla
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width

        # Resetear on_ground para comprobar colisiones
        self.on_ground = False

        # Actualizar rectángulo de colisión
        self.rect.x = self.x
        self.rect.y = self.y

        # Colisiones con plataformas
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Colisión desde arriba
                if self.vel_y > 0 and self.rect.bottom > platform.rect.top and self.rect.top < platform.rect.top:
                    self.y = platform.rect.top - self.height
                    self.vel_y = 0
                    self.on_ground = True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


# Clase para plataformas
class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

        # Crear imagen de plataforma
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


# Clase para la meta (ventana en el piso)
class Goal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 40  # Más baja para que esté en el piso
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Crear imagen de ventana
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
        pygame.draw.rect(self.image, WHITE, (10, 5, 60, 30))
        pygame.draw.line(self.image, BLACK, (40, 5), (40, 35), 2)
        pygame.draw.line(self.image, BLACK, (10, 20), (70, 20), 2)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))





# Punto de entrada principal
if __name__ == "__main__":
    game = Game()
    game.run()