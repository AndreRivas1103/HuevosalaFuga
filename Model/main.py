import pygame
import json
import os

# Inicialización
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Huevos a la Fuga")

# Colores y FPS
WHITE = (255, 255, 255)
FPS = 60

# Rutas
SAVE_FILE = "progreso.json"

# Clases principales
class Huevo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 255, 0))  # Amarillo huevo
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT - 100)
        self.vel_y = 0
        self.vidas = 3
        self.en_el_suelo = True
        self.invulnerable = False
        self.invuln_timer = 0

    def update(self):
        self.vel_y += 1  # Gravedad
        self.rect.y += self.vel_y

        if self.rect.bottom >= HEIGHT:  # Piso
            self.rect.bottom = HEIGHT
            self.vel_y = 0
            self.en_el_suelo = True

        if self.invulnerable:
            self.invuln_timer -= 1
            if self.invuln_timer <= 0:
                self.invulnerable = False

    def mover(self, dx):
        self.rect.x += dx

    def saltar(self):
        if self.en_el_suelo:
            self.vel_y = -15
            self.en_el_suelo = False

    def recibir_dano(self):
        if not self.invulnerable:
            self.vidas -= 1
            self.invulnerable = True
            self.invuln_timer = FPS * 2

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto, tipo):
        super().__init__()
        self.image = pygame.Surface((ancho, alto))
        self.tipo = tipo
        if tipo == "aceite":
            self.image.fill((0, 0, 0))
        elif tipo == "sarten":
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.tipo = tipo
        if tipo == "cascaron":
            self.image.fill((200, 200, 255))
        elif tipo == "salto":
            self.image.fill((100, 255, 100))
        elif tipo == "aluminio":
            self.image.fill((192, 192, 192))
        self.rect = self.image.get_rect(center=(x, y))

class Juego:
    def __init__(self):
        self.jugador = Huevo()
        self.todos = pygame.sprite.Group()
        self.todos.add(self.jugador)
        self.obstaculos = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.reloj = pygame.time.Clock()
        self.cargar_progreso()

    def cargar_progreso(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as file:
                datos = json.load(file)
                print("Progreso cargado:", datos)
        else:
            print("No hay progreso previo.")

    def guardar_progreso(self):
        progreso = {"nivel": 1}
        with open(SAVE_FILE, "w") as file:
            json.dump(progreso, file)

    def run(self):
        corriendo = True
        while corriendo:
            self.reloj.tick(FPS)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT]:
                self.jugador.mover(-5)
            if teclas[pygame.K_RIGHT]:
                self.jugador.mover(5)
            if teclas[pygame.K_SPACE]:
                self.jugador.saltar()

            self.todos.update()

            # Colisiones
            for obstaculo in self.obstaculos:
                if self.jugador.rect.colliderect(obstaculo.rect):
                    if obstaculo.tipo == "sarten":
                        print("¡Derrota instantánea!")
                        corriendo = False
                    elif obstaculo.tipo == "aceite":
                        print("¡Resbalón!")
                        self.jugador.mover(10)
                        self.jugador.recibir_dano()

            for powerup in self.powerups:
                if self.jugador.rect.colliderect(powerup.rect):
                    if powerup.tipo == "cascaron":
                        self.jugador.vidas += 1
                    elif powerup.tipo == "salto":
                        self.jugador.vel_y = -20
                    elif powerup.tipo == "aluminio":
                        self.jugador.invulnerable = True
                        self.jugador.invuln_timer = FPS * 3
                    powerup.kill()

            # Fin del juego si se rompe
            if self.jugador.vidas <= 0:
                print("¡El huevo se rompió!")
                corriendo = False

            # Dibujar
            screen.fill(WHITE)
            self.todos.draw(screen)
            self.obstaculos.draw(screen)
            self.powerups.draw(screen)
            pygame.display.flip()

        self.guardar_progreso()
        pygame.quit()

# Ejecución del juego
if __name__ == "__main__":
    juego = Juego()
    juego.run()
