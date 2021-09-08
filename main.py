import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class IncrementTicketButton():
    def __init__(self, x, y, ticket):
        self.x = x
        self.y = y

        self.width = 100
        self.height = 35

        self.ticket = ticket

        if self.ticket == "helpdesk":
            self.color = BLUE
        else:
            self.color = GREEN

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def update(self, events):
        pos = pygame.mouse.get_pos()

        if self.x <= pos[0] <= self.x + self.width:
            if self.y <= pos[1] <= self.y + self.height:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.incrementTicket()

    def incrementTicket(self):
        if self.ticket == "helpdesk":
            window.helpdeskTickets += 1
        else:
            window.inpersonTickets += 1


class PercentageBar():
    def __init__(self):
        self.x = 25
        self.y = 25
        self.width = 450
        self.height = 35

        self.percentage = 0

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.width, self.height)) #Draw the base bar
        pygame.draw.rect(surface, GREEN, (self.x, self.y, int((self.percentage * 4.5) + 1), self.height)) #Draw the percentage bar
        pygame.draw.rect(surface, BLACK, (self.x + int((self.percentage * 4.5) + 1), self.y - 5, 5, 45)) #Draw the bar that divides the two

    def update(self):
        pass


class Window():
    def __init__(self):
        self.screen = pygame.display.set_mode([500, 500])
        pygame.display.set_caption("Helpdesk V2")

        self.running = True
        self.clock = pygame.time.Clock()
        self.events = pygame.event.get()

        self.percentageBar = PercentageBar()

        self.helpdeskTickets = 0
        self.inpersonTickets = 0

        self.percentNonHelpdesk = 0

        self.helpdeskButton = IncrementTicketButton(150, 85, "helpdesk")
        self.inpersonButton = IncrementTicketButton(25, 85, "inperson")

        try:
            self.percentNonHelpdesk = int((self.inpersonTickets/(self.helpdeskTickets + self.inpersonTickets)) * 100)
        except:
            pass

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

        self.percentageBar.draw(self.screen)

        self.helpdeskButton.draw(self.screen)
        self.inpersonButton.draw(self.screen)

    def update(self):
        try:
            self.percentNonHelpdesk = int((self.inpersonTickets/(self.helpdeskTickets + self.inpersonTickets)) * 100)
        except:
            pass

        self.percentageBar.percentage = self.percentNonHelpdesk
        self.percentageBar.update()

        self.helpdeskButton.update(self.events)
        self.inpersonButton.update(self.events)

        pygame.display.update()
        self.clock.tick(30)

window = Window()
window.start()

pygame.quit()
