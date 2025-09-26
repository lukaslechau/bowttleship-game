
import random

class Player:
    def __init__(self, start_range, character):
        self.position = random.randint(start_range[1], start_range[199])
        self.health = 100
        self.character = character  # Archer type (e.g., Normal, Bounce, Magic)

    def take_damage(self, damage):
        """Reduce health and print status after taking damage."""
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

    def start_game():
        # Start game, Player 1 takes the first turn
        current_player = self.player1
        opponent = self.player2
        while self.player1.health > 0 and self.player2.health > 0:
            print(current_player.character.capitalize(),"'s turn!")
            
            # Get power and arc input for the shot
            power = int(input(f"Enter power (1-10) for {current_player.character}: "))
            arc = int(input(f"Enter arc (degrees 0-90) for {current_player.character}: "))
            
            # Player shoots
            hit = current_player.character.shoot(power, arc, opponent)

            if hit:
                if opponent.health <= 0:
                    print("Player 2 is out of health! Player 1 wins!")
                    break
                else:
                    # Switch turn to opponent
                    current_player, opponent = opponent, current_player
            else:
                print(current_player.character.capitalize(), "s shot missed! Switching turns.")

                # Switch turn to opponent
                current_player, opponent = opponent, current_player
    
    def end_game():
        exit pygame with an exit button



# Base Archer Class


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
    'normal archer': NormalArcher(),
    'bounce archer': BounceArcher(),
    'magic archer': MagicArcher()
}

    # Start game, Player 1 takes the first turn
    current_player = player1
    opponent = player2



start_game()
end_game()

