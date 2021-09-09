import pygame

pygame.init()
pygame.font.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

interfont = pygame.font.Font("assets/fonts/Inter/Inter-Medium.ttf", 28)
statfont = pygame.font.Font("assets/fonts/Inter/Inter-Medium.ttf", 18)

class SaveButton():
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = 100
        self.height = 35

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))

    def update(self, events):
        pos = pygame.mouse.get_pos()

        if self.x <= pos[0] <= self.x + self.width:
            if self.y <= pos[1] <= self.y + self.height:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pass


class IncrementTicketButton():
    def __init__(self, x, y, ticket, title):
        self.x = x
        self.y = y

        self.width = 100
        self.height = 35

        self.ticket = ticket

        self.text = statfont.render(title, True, BLACK)

        if self.ticket == "helpdesk":
            self.color = BLUE
        else:
            self.color = GREEN

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        #surface.blit(self.text, (self.x + 35, self.y))

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
        pygame.draw.rect(surface, WHITE, (self.x + int((self.percentage * 4.5) + 1), self.y - 5, 5, 45)) #Draw the bar that divides the two

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

        self.helpdeskButton = IncrementTicketButton(150, 85, "helpdesk", "HD")
        self.inpersonButton = IncrementTicketButton(25, 85, "inperson", "IP")
        self.saveButton = SaveButton(375, 85)

        try:
            self.percentNonHelpdesk = int((self.inpersonTickets/(self.helpdeskTickets + self.inpersonTickets)) * 100)
        except:
            pass

        self.statstitle = statfont.render("Ticket Origin Stats", True, WHITE)
        self.helpdeskstat = statfont.render("Helpdesk Tickets: " + str(self.helpdeskTickets), True, WHITE)
        self.inpersonstat = statfont.render("Inperson Tickets: " + str(self.inpersonTickets), True, WHITE)
        self.totalstat = statfont.render("Total Tickets: " + str(int(self.helpdeskTickets + self.inpersonTickets)), True, WHITE)
        self.percentstat = statfont.render("Percent Non Helpdesk: " + str(round(self.percentNonHelpdesk)) + "%", True, WHITE)
        self.averagestat = statfont.render("Average Non Helpdesk: 60%", True, WHITE)
        self.diffstat = statfont.render("Difference: " + str(int(self.percentNonHelpdesk - 60)) + "%", True, WHITE)

    def start(self):
        while self.running:
            self.events = pygame.event.get()

            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.draw()

            self.update()

    def draw(self):
        self.screen.fill(BLACK)

        self.percentageBar.draw(self.screen)

        self.helpdeskButton.draw(self.screen)
        self.inpersonButton.draw(self.screen)
        self.saveButton.draw(self.screen)

        self.screen.blit(self.statstitle, (25, 145))
        self.screen.blit(self.helpdeskstat, (25, 195))
        self.screen.blit(self.inpersonstat, (25, 170))
        self.screen.blit(self.totalstat, (25, 245))
        self.screen.blit(self.percentstat, (25, 295))
        self.screen.blit(self.averagestat, (25, 320))
        self.screen.blit(self.diffstat, (25, 345))

    def update(self):
        try:
            self.percentNonHelpdesk = int((self.inpersonTickets/(self.helpdeskTickets + self.inpersonTickets)) * 100)
        except:
            pass

        self.percentageBar.percentage = self.percentNonHelpdesk
        self.percentageBar.update()

        self.helpdeskButton.update(self.events)
        self.inpersonButton.update(self.events)
        self.saveButton.update(self.events)

        self.helpdeskstat = statfont.render("Helpdesk Tickets: " + str(self.helpdeskTickets), True, WHITE)
        self.inpersonstat = statfont.render("Inperson Tickets: " + str(self.inpersonTickets), True, WHITE)
        self.totalstat = statfont.render("Total Tickets: " + str(int(self.helpdeskTickets + self.inpersonTickets)), True, WHITE)
        self.percentstat = statfont.render("Percent Non Helpdesk: " + str(round(self.percentNonHelpdesk)) + "%", True, WHITE)
        self.diffstat = statfont.render("Difference: " + str(int(self.percentNonHelpdesk - 60)) + "%", True, WHITE)

        pygame.display.update()
        self.clock.tick(30)

window = Window()
window.start()

pygame.quit()
