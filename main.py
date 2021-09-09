import pygame
import pickle

pygame.init()
pygame.font.init()

BLACK = (45, 45, 45)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

statfont = pygame.font.Font("assets/fonts/Inter/Inter-Medium.ttf", 18)


class PreviousDay():
    def __init__(self, x, y, percentage):
        self.x = x
        self.y = y

        self.width = 25
        self.height = 75

        self.percentage = percentage

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, GREEN, (self.x, self.y + self.height - int(self.percentage * .75) + 1, self.width, int(self.percentage * .75) + 1))
        pygame.draw.rect(surface, WHITE, (self.x - 2, self.y + self.height - int(self.percentage * .75) + 1, 29, 3))

    def update(self, events):
        pass


class LoadButton():
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = 100
        self.height = 35

    def draw(self, surface):
        pygame.draw.rect(surface, PURPLE, (self.x, self.y, self.width, self.height))

    def update(self, events):
        pos = pygame.mouse.get_pos()

        if self.x <= pos[0] <= self.x + self.width:
            if self.y <= pos[1] <= self.y + self.height:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.load()

    def load(self):
        try:
            window.helpdeskTickets = pickle.load(open("assets/save/helpdeskTickets.p", "rb"))
        except:
            print("assets/save/helpdeskTickets.p not found")

        try:
            window.inpersonTickets = pickle.load(open("assets/save/inpersonTickets.p", "rb"))
        except:
            print("assets/save/inpersonTickets.p not found")


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
                        self.save()

    def save(self):
        pickle.dump(window.helpdeskTickets, open("assets/save/helpdeskTickets.p", "wb"))
        pickle.dump(window.inpersonTickets, open("assets/save/inpersonTickets.p", "wb"))


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
        self.loadButton = LoadButton(275, 85)

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

        self.monday = PreviousDay(25, 400, 30)
        self.tuesday = PreviousDay(75, 400, 57)
        self.wednesday = PreviousDay(125, 400, 69)
        self.thursday = PreviousDay(175, 400, 42)
        self.friday = PreviousDay(225, 400, 77)

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
        self.loadButton.draw(self.screen)

        self.screen.blit(self.statstitle, (25, 145))
        self.screen.blit(self.helpdeskstat, (25, 195))
        self.screen.blit(self.inpersonstat, (25, 170))
        self.screen.blit(self.totalstat, (25, 245))
        self.screen.blit(self.percentstat, (25, 295))
        self.screen.blit(self.averagestat, (25, 320))
        self.screen.blit(self.diffstat, (25, 345))

        self.monday.draw(self.screen)
        self.tuesday.draw(self.screen)
        self.wednesday.draw(self.screen)
        self.thursday.draw(self.screen)
        self.friday.draw(self.screen)

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
        self.loadButton.update(self.events)

        self.helpdeskstat = statfont.render("Helpdesk Tickets: " + str(self.helpdeskTickets), True, WHITE)
        self.inpersonstat = statfont.render("Inperson Tickets: " + str(self.inpersonTickets), True, WHITE)
        self.totalstat = statfont.render("Total Tickets: " + str(int(self.helpdeskTickets + self.inpersonTickets)), True, WHITE)
        self.percentstat = statfont.render("Percent Non Helpdesk: " + str(round(self.percentNonHelpdesk)) + "%", True, WHITE)
        self.diffstat = statfont.render("Difference: " + str(int(self.percentNonHelpdesk - 60)) + "%", True, WHITE)

        self.monday.update(self.events)
        self.tuesday.update(self.events)
        self.wednesday.update(self.events)
        self.thursday.update(self.events)
        self.friday.update(self.events)

        pygame.display.update()
        self.clock.tick(30)

window = Window()
window.start()

pygame.quit()
