import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class PercentageBar():
    def __init__(self):
        

class Window():
    def __init__(self):
        self.screen = pygame.display.set_mode([500, 500])
        pygame.display.set_caption("Helpdesk V2")

        self.running = True
        self.clock = pygame.time.Clock()
        self.events = pygame.event.get()

    def start(self):
        while self.running:
            self.events = pygame.event.get()

            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.draw()

            self.update()

    def draw(self):
        self.screen.fill(WHITE)

    def update(self):
        pygame.display.update()
        self.clock.tick(30)

window = Window()
window.start()

pygame.quit()
