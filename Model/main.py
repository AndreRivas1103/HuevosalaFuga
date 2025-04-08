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

# Clase del nivel con solo suelo y ventana en el piso
class Level:
    def _init_(self):
        self.platforms = []
        self.egg = None
        self.goal = None
        self._create_level()

    def _create_level(self):
        # Suelo base (más corto para dejar espacio a la ventana)
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH - 100, 20))

        # Huevo
        self.egg = Egg(100, SCREEN_HEIGHT - 60)  # Posicionado sobre el suelo

        # Meta (ventana en el piso al final)
        self.goal = Goal(SCREEN_WIDTH - 80, SCREEN_HEIGHT - 40)

    def update(self):
        # Actualizar huevo
        self.egg.update(self.platforms)

        # Comprobar colisión con meta
        if self.egg.rect.colliderect(self.goal.rect):
            return "victory"

        # Comprobar límites de pantalla
        if self.egg.y > SCREEN_HEIGHT:
            return "death"

        return None

    def draw(self, screen):
        # Fondo
        screen.fill((200, 200, 220))

        # Dibujar plataformas (solo el suelo)
        for platform in self.platforms:
            platform.draw(screen)

        # Dibujar meta (ventana en el piso)
        self.goal.draw(screen)

        # Dibujar huevo
        self.egg.draw(screen)


# Clase principal del juego
class Game:
    def _init_(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Huevos a la Fuga")
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.current_level = None

    def run(self):
        running = True
        while running:
            # Gestión de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.state == GameState.MENU:
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE and self.state == GameState.PLAYING:
                        self.state = GameState.MENU

            # Actualizar
            if self.state == GameState.PLAYING:
                keys = pygame.key.get_pressed()

                # Movimiento del huevo
                if keys[pygame.K_LEFT]:
                    self.current_level.egg.move(-1)
                elif keys[pygame.K_RIGHT]:
                    self.current_level.egg.move(1)
                else:
                    self.current_level.egg.move(0)

                # Salto
                if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                    self.current_level.egg.jump()

                # Actualizar nivel
                result = self.current_level.update()

                # Comprobar resultado
                if result == "victory":
                    self.state = GameState.MENU
                elif result == "death":
                    self.state = GameState.MENU

            # Renderizar
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.current_level.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def start_game(self):
        self.current_level = Level()
        self.state = GameState.PLAYING

    def draw_menu(self):
        self.screen.fill((200, 200, 220))

        # Fuentes
        font_large = pygame.font.SysFont("Arial", 48)
        font_medium = pygame.font.SysFont("Arial", 36)

        # Título
        title = font_large.render("Huevos a la Fuga", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Instrucciones
        instr2 = font_medium.render("Flechas para moverse, Espacio para saltar", True, BLACK)
        instr2_rect = instr2.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(instr2, instr2_rect)

        # Iniciar juego
        start = font_medium.render("Presiona ENTER para comenzar", True, BLACK)
        start_rect = start.get_rect(center=(SCREEN_WIDTH // 2, 350))
        self.screen.blit(start, start_rect)

        # Salir
        exit_text = font_medium.render("ESC para volver al menú", True, BLACK)
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(exit_text, exit_rect)



# Punto de entrada principal
if __name__ == "__main__":
    game = Game()
    game.run()