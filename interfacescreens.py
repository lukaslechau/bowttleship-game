import pygame
import random
#intialize all that
pygame.init()
pygame.font.init()

# colors/screen
display_width = 1000
display_height = 800
black = (0, 0, 0) 
white = (255, 255, 255)
red =(200, 0, 0) 
blue = (0, 0, 200)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
#make the sceen
window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Bow-ttleship")
clock = pygame.time.Clock()

#  only class we need, no new characters
#players become archer objects and take the name either player 1 or 2
#insert paramters as seen
class Archer:
    def __init__(self, position):
        self.position = position
        self.health = 100
        self.character = character
        self.damage = damage
#shows where arrow lands to help provide accurate feedback
    def calculate_arrow_landing(self, power, arc, direction):

        power_distance = 10 * power
        multiplier = 2 if arc == 45 else 2 * (1.0 - abs(arc - 45) / 100)
        distance_traveled = power_distance * multiplier * direction
        return self.position + distance_traveled
#damage if hit
    def take_damage(self, damage):
        self.health -= damage
        
#Knockback so we not shooting the same spot everytime
    def apply_knockback(self, direction):
       
        knockback_distance = random.randint(3, 9)
        self.position += knockback_distance * direction

        # Prevent moving out of bounds
        if self.character == "Player 1" and self.position < 1:
            self.position = 1
        elif self.character == "Player 2" and self.position > 199:
            self.position = 199


# check hit Feedback in order to display hot or cold feedback, used after each input is put into box
def check_hit_feedback(arrow_position, opponent, current_player):
    distance = abs(arrow_position - opponent.position)
    if distance <= 3:  # opponent hit within the hitbox
        opponent.take_damage(current_player.damage)
        knockback_direction = -1 if opponent.character == "Player 1" else 1
        opponent.apply_knockback(knockback_direction)
        print("Hit!")
        return "Hit!"
    elif distance <= 5:
        print("Very Warm!")
        return "Very Warm!"
    elif distance <= 15:
        print("Warm!")
        return "Warm!"
    elif distance <= 50:
        print("Cold!")
        return "Cold!"
    else:
        print("Very Cold!")
        return "Very Cold!"


# copied input box to summon it whenever its a new persons turn
def draw_input_box(input_text):
    pygame.draw.rect(window, white, (350, 650, 300, 50))  # Input box
    input_text_surface = pygame.font.SysFont("comicsansms", 30).render(input_text, True, black)
    window.blit(input_text_surface, (360, 660))


# copied button 
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(window, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(window, ic, (x, y, w, h))

    font = pygame.font.SysFont("verdana", 30)
    text_surface = font.render(msg, True, black)
    text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
    window.blit(text_surface, text_rect)


def game_loop(): #NEED CHRISTIAN INTRO SCREEN TO POP UP
    # random spawn ranges 
    player1 = Archer(random.randint(1, 87), "Player 1", 34)
    player2 = Archer(random.randint(112, 199), "Player 2", 34)

    turn = 1  
    input_active = False #so input box doesnt appear right away
    input_text = ""
    game_running = True #so while loop continues game
    message = "" #need to keep emptying the input box
    #this is the variable taht input becomes
#copied button funcitonality 
    while game_running:
        for event in pygame.event.get(): #manages each time input is used
            if event.type == pygame.QUIT: #if they click red x top left
                pygame.quit()
                quit()

            if input_active: #norammly false, waiting till clicked
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  #click enter to submit shot
                        try:
                            power, arc = map(int, input_text.split(",")) #turns the power and arc into separate stings
                            if 1 <= power <= 10 and 0 <= arc <= 90: #take in paramters for button and input arrow landing to get results
                      
                                current_player = player1 if turn == 1 else player2 
                                #current player is player 1 if the turn is set to 1, if not, player 2 turn
                                opponent = player2 if turn == 1 else player1 #kinda redundant but doesnt run without
                                direction = 1 if turn == 1 else -1 #players must shoot left (negative) or right (positive)
                                arrow_position = current_player.calculate_arrow_landing(power, arc, direction) 
                                if arrow_position < 0 or arrow_position > 199: #after shooting, check if out of bounds
                                    message = "Arrow landed at " + str(round(arrow_position, 1))+"--Out of Bounds!" #round to nearest tenth
                                    input_active = False #reset input box if so
                                    input_text = ""
                                else:
                                    # cont with hit detection if arrow is within bounds
                                    feedback = check_hit_feedback(arrow_position, opponent, current_player)
                                    message = "Arrow landed at " + str(round(arrow_position, 2)) + ". Feedback: " + feedback
                                    

                                if opponent.health <= 0: #decide how to get winner
                                    winner = current_player.character  #current shooter is winner
                                    #outro_screen(winner)               # call ryan func
                                    return

                                # Switch turn after arrow shot and message displayed
                                turn = 1 if turn == 2 else 2
                                input_active = False #disable the input button to reset it 
                                input_text = "" #reset text insode of the input box
                            else: #rebuttal for the false parameters
                                message = "Invalid input! Power must be 1-10, arc 0-90."
                        except ValueError:
                            message = "Invalid input! Enter as power,arc (e.g., 5,45)."
                            input_text = ""
                    elif event.key == pygame.K_BACKSPACE: #delete funciton in case ppl wanna delete
                        input_text = input_text[:-1] #this delete function was so copied from documentation lol
                    else:
                        input_text += event.unicode

            #  Shoot button 
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if turn == 1 and 50 <= mouse[0] <= 200 and 700 <= mouse[1] <= 750 and not input_active:
                    input_active = True #differentiates which player button is shooting for based on turn
                    #ensures we puttin in paramters for player 1 to shoot vice versa
                elif turn == 2 and 800 <= mouse[0] <= 950 and 700 <= mouse[1] <= 750 and not input_active:
                    input_active = True

        #  game screen
        window.fill(black)
        pygame.draw.rect(window, blue, (0, 0, display_width // 2, display_height))
        pygame.draw.rect(window, red, (display_width // 2, 0, display_width // 2, display_height))
        pygame.draw.line(window, black, (500, 0), (500, 800), 10)
        #white box behind names
        pygame.draw.rect(window, white, (40, 60, 200, 60))
        pygame.draw.rect(window, white, (display_width - 260, 60, 200, 60))

        #  player info printed
        player1_name = pygame.font.SysFont("comicsansms", 50).render("Player 1", True, black)
        player2_name = pygame.font.SysFont("comicsansms", 50).render("Player 2", True, black)
        window.blit(player1_name, (50, 50))
        window.blit(player2_name, (display_width - 255, 50))
        #white box behind names
        pygame.draw.rect(window, white, (40, 120, 200, 50))
        pygame.draw.rect(window, white, (display_width - 260, 120, 200, 50))

        player1_health = pygame.font.SysFont("comicsansms", 30).render("Health: " + str(player1.health), True, black)
        player2_health = pygame.font.SysFont("comicsansms", 30).render("Health: " + str(player2.health), True, black)
        window.blit(player1_health, (50, 120))
        window.blit(player2_health, (display_width - 250, 120))

        # cahnge the turn on screen using turn
        if turn == 1:
            turn_text = pygame.font.SysFont("comicsansms", 50).render("Player 1's Turn", True, white)
            window.blit(turn_text, (50, 200))
        else: #player 2 switch to player 2 side
            turn_text = pygame.font.SysFont("comicsansms", 50).render("Player 2's Turn", True, white)
            window.blit(turn_text, (display_width - 430, 200))

        # Shoot button
        if not input_active: #shoot button changes for player 1 and two but look the same
            if turn == 1:
                button("Shoot", 50, 700, 150, 50, bright_green, bright_red, action=None) #show red if mouse hovering over,green otherwise
            else:
                button("Shoot", 800, 700, 150, 50, bright_green, bright_red, action=None)

        #show the message
        if message:
            window.blit(feedback_font.render(message, True, white), (display_width // 2 - 300, 180))

      
        window.blit(font.render(f"{'Player 1' if current_player == player1 else 'Player 2'}'s Turn", True, white), (50, 700))

        #call shoot button on screen here
        button("Shoot", 400, 700, 200, 50, bright_green, bright_red)

        #reveal the input box
        if input_active: #after click
            instruction_text = pygame.font.SysFont("comicsansms", 30).render(
                "Enter your power and arc separated by a comma (e.g., 5,45):", True, white
            )
            window.blit(instruction_text, (50, 600))
            draw_input_box(input_text)

        pygame.display.update()
        clock.tick(60)



# Run the game
game_loop()
pygame.quit()
