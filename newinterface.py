import pygame
import time
import random

pygame.init()
pygame.font.init()

class Player:
    def __init__(self, start_range, character):
        self.position = random.randint(start_range[0], start_range[1])
        self.health = 100
        self.character = character  # Archer type (e.g., Normal, Bounce, Magic)

    def take_damage(self, damage):  
        self.health -= damage
        print("Player's health is now", self.health)


class Map:
    def __init__(self):
        print("Game Start! Players, choose your characters.")
        
        # Player 1 setup for picking character
        p1_char = input("Player 1, choose your character (normal archer, bounce archer, magic archer): ")
        
        # Use the dictionary to assign the character to Player 1
        if p1_char in characters:
            self.player1 = Player((1, 88), p1_char)
            print("Player 1 has chosen", p1_char, "and spawned at position", self.player1.position)
        else:
            print("Invalid character choice for Player 1!")

        # Player 2 setup
        p2_char = input("Player 2, choose your character (normal archer, bounce archer, magic archer): ")
        
        # Use the dictionary to assign the character to Player 2
        if p2_char in characters:
            self.player2 = Player((113, 199), p2_char)
            print("Player 2 has chosen", p2_char,"and spawned at position", self.player2.position)
        else:
            print("Invalid character choice for Player 2!")

class Archer:
    def __init__(self, position):
        self.position = position

    def check_hit(self, arrow_position, opponent, damage):
        """Check if arrow hits the opponent and apply damage."""
        if abs(arrow_position - opponent.position) <= 3:  # Direct hit (within 3 spaces)
            opponent.health -= current_player.damage
            print("Arrow hits the target!", opponent.character, "takes", current_player.damage , "damage!")
        else:
            # Hot and cold feedback based on distance
            if abs(arrow_position - opponent.position) <= 5:
                print("Very Warm!")
            elif abs(arrow_position - opponent.position) <= 15:
                print("Warm!")
            elif abs(arrow_position - opponent.position) <= 50:
                print("Cold!")
            else:
                print("Very Cold!")
    
    def take_damage(self, damage):
        """Reduce health and print status after taking damage."""
        self.health -= damage
        print("Opponent's health is now", self.health)

    def knockback(self, opponent):
        """Apply knockback after hit."""
        knockback_distance = random.randint(3, 8)
        if self.position < opponent.position:
            opponent.position += knockback_distance
        else:
            opponent.position -= knockback_distance
        print("Opponent is knocked back to position", opponent.position)
        
    def calculate_arrow_landing(self, power, arc, direction):
        """Calculate where the arrow lands."""
        power_distance = 10 * power
        multiplier = 2 if arc == 45 else 2 * (1.0 - abs(arc - 45) / 100)
        distance_traveled = power_distance * multiplier * direction
        arrow_position = self.position + distance_traveled
        return self.position + distance_traveled


# Normal Archer
class NormalArcher(Archer):
    def __init__(self, position):
        super().__init__(position)
        self.damage = 34

    def shoot(self, power, arc, opponent):
        arrow_position = self.calculate_arrow_landing(power, arc, direction=1)
        print("Normal Archer's arrow landed at",arrow_position)
        self.check_hit(arrow_position, opponent, self.damage)


# Magic Archer
class MagicArcher(Archer):
    def __init__(self, position):
        super().__init__(position)
        self.damage = 25

    def shoot(self, power, arc, opponent):
        print("Magic Archer at position", self.position, " is shooting.")
        arrow_landing_position = self.calculate_arrow_landing(power, arc, direction=1)
        
        # Splitting mechanic
        split_point = arrow_landing_position - 10  # 10 spaces before original landing
        print("Arrow splits at position", split_point)

        # Two new random landing positions around the original landing spot
        arrow_1_position = split_point + random.randint(0, 20)
        arrow_2_position = split_point - random.randint(0, 20)
        
        print("First split arrow lands at",arrow_1_position)
        print("Second split arrow lands at",arrow_2_position)
        
        # Check hits for both arrows
        self.check_hit(arrow_1_position, opponent, self.damage)
        self.check_hit(arrow_2_position, opponent, self.damage)


# Bounce Archer
class BounceArcher(Archer):
    def __init__(self, position):
        super().__init__(position)
        self.base_damage = 30

    def shoot(self, power, arc, opponent):
        print("Bounce Archer at position", self.position,"is shooting.")
        arrow_landing_position = self.calculate_arrow_landing(power, arc, direction=1)
        print("Arrow lands at position", arrow_landing_position)
        self.handle_bounce(arrow_landing_position, power, arc, opponent)

    def handle_bounce(self, initial_landing, power, arc, opponent):
        # First, check if the original shot hits
        hit = self.check_hit(initial_landing, opponent, self.base_damage)
        if hit:
            return True
        
        # First bounce is 1/4 distance of the original trajectory
        first_bounce_distance = (1/4) * (10 * power) * (arc / 90)
        first_bounce_position = initial_landing + first_bounce_distance
        print("Arrow bounces to position", first_bounce_position)
        # First bounce does 1/3 damage of original trajectory
        first_bounce_damage = (1/3) * self.base_damage
        hit = self.check_hit(first_bounce_position, opponent, first_bounce_damage)
        if hit:
            return True
        
        # Second bounce is 1/4 distance of the first bounce
        second_bounce_distance = (1/4) * first_bounce_distance
        second_bounce_position = first_bounce_position + second_bounce_distance
        print("Arrow bounces again to position", second_bounce_position)
        # Second bounce does 1/3 damage of the first bounce
        second_bounce_damage = (1/3) * first_bounce_damage
        self.check_hit(second_bounce_position, opponent, second_bounce_damage)
        return False



characters = {
    'normal archer': NormalArcher(10),
    'bounce archer': BounceArcher(10),
    'magic archer': MagicArcher(10)
}
#############
#############

display_width = 1000
display_height = 800

black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
blue = (0,0,200)

bright_red = (255,0,0)
bright_green = (0,255,0)

block_color = (53,115,255)

car_width = 73

window = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Bow-ttleship')
clock = pygame.time.Clock()



def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()




def quitgame():
    pygame.quit()
    quit()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(window, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    window.blit(textSurf, textRect)


 #display arrow landed at (coordinate)
def display_arrow_landing():
    
        
        landingfont = pygame.font.SysFont("comicsansms",35)
        landingtext= landingfont.render(f"arrow has landed at {arrow_position}", False, (0,0,0) ) #show where arrow landed on screen
        window.blit(landingtext , (400, 500))
        hotcoldtext = landingfont.render(str(check_hit())) #show hot or cold on the screen
        window.blit(hotcoldtext , (400, 600)) #display below the landingtext


def game_loop():
    # Create players
    player1 = Player((1, 88), "normal archer")
    player2 = Player((113, 199), "magic archer")

    # Initialize game state
    current_player = player1
    opponent = player2
    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Check for turn switch (e.g., SPACE key)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                current_player, opponent = opponent, current_player

        # Fill the screen and draw static elements
        window.fill((0, 0, 0))  # Fill the screen with black as the base color
        pygame.draw.rect(window, blue, (0, 0, display_width // 2, display_height))  # Left half
        pygame.draw.rect(window, red, (display_width // 2, 0, display_width // 2, display_height))  # Right half
        pygame.draw.line(window, black, (500, 0), (500, 800), 10)  # Dividing line

        # Display player names at the top
        player1_name = pygame.font.SysFont("comicsansms", 50).render("Player 1", True, black)
        window.blit(player1_name, (50, 50))  # Left side
        player2_name = pygame.font.SysFont("comicsansms", 50).render("Player 2", True, black)
        window.blit(player2_name, (display_width - 300, 50))  # Right side

        # Display whose turn it is
        if current_player == player1:
            shooting_text = pygame.font.SysFont("comicsansms", 50).render("Player 1 is shooting...", True, black)
            window.blit(shooting_text, (50, 700))  # Left side
        else:
            shooting_text = pygame.font.SysFont("comicsansms", 50).render("Player 2 is shooting...", True, black)
            window.blit(shooting_text, (display_width - 450, 700))  # Right side

        # Display player health
        player1_health = pygame.font.SysFont("comicsansms", 30).render(f"Health: {player1.health}", True, black)
        window.blit(player1_health, (50, 300))
        player2_health = pygame.font.SysFont("comicsansms", 30).render(f"Health: {player2.health}", True, black)
        window.blit(player2_health, (display_width - 200, 300))

        # Character images
        p1charimage = pygame.image.load("characters/archer.png")
        p1charimage = pygame.transform.scale(p1charimage, (300, 300))
        window.blit(p1charimage, (100, 400))

        p2charimage = pygame.image.load("characters/bounce.png")
        p2charimage = pygame.transform.scale(p2charimage, (300, 300))
        window.blit(p2charimage, (600, 400))

        # Update the display
        pygame.display.update()
        clock.tick(60)
