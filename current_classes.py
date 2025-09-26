#make a map
import random
#create a map thru pygame
# map will be 199 yards long for x axis
# y does not matter because visual aspect not that in depth
# map will be 199 yards long for x axis
# y does not matter because visual aspect not that in depth
#2 players will spawn on each side of map with a guaranteed minimum of 25 yards in between them
player_1_x_coordinate = random.randint(0, 87)
player_2_x_coordinate = random.randint(112, 199)
#players will have a hitbox of 3 yards for convienence, if arrow hits any of coordinates, counts as hit
player1_hitbox = [(player_1_x_coordinate - 1), player_1_x_coordinate, (player_1_x_coordinate + 1)]
player2_hitbox = [(player_2_x_coordinate - 1), player_2_x_coordinate, (player_2_x_coordinate + 1)]

#make player classes
class Player():
  def __init__(self, name, health, position):
    self.name = name
    self.health = 100
    self.position = position
    self.bow = Bow()

  def take_damage(self, damage):
    self.health -= damage
    self.health = max(0, self.health)  # Stops health from going negative
    print(f"{self.name} takes {damage} damage. Current health: {self.health}")

#make a class for Bow


 #ask for inputs on each turn to figure out shooting parameters
  #shooting methods, (these can change depending on sub classes)
  
  def shoot(power, arc, player):
    power = int(input("Bow drawback power (1-10): "))
    arc = int(input("Bow degree arc (0°-90°): "))

    print("Player ", player, " is shooting")
#power of 1 shoots 10 yards, so any more power just multiply by 10
    arrow_power_distance = 10 * power #yards
#arrow will travel farthest at 45° because its most opitmal, goes less for anything x < 45 < x
    if arc == 45:
      mulitplier = 2
      arrow_yards_traveled = (arrow_power_distance) * multiplier
  #arc 47° should multiply same as arc 43°

    elif arc < 45 or arc > 45:
      change = abs(arc - 45)
      percent_change = change * 1/100
  #i.e. 47 degree should breed change = 2, thus perc_change = 0.02, thus, (1.0 - percent change) = 0.98
  #2 * 0.98 is something close but less than 2
    multiplier = 2 * (1.0 - percent_change)
    arrow_yards_traveled = (arrow_power_distance) * multiplier
    position = player_x_coordinate + arrow_yards_traveled
    print("arrow has landed at ", position , "yards" )

#conditonals for normal and magic archer
if position in player1_hitbox:
  player1.health -= player2.damage
else:
  next turn
#conditional for bounce
if position in player1_hitbox:
  player1.health -= player2.damage
else:
  #set new bounce distance (1/4 of original distance)
  bounce = (1/4 * arrow_yards_traveled)
  position += bounce
  if position in player1_hitbox:
    #set new bounce damage (1/3 of original dmg)
    bounce_dmg = (player2.damage * 1/3)
    player1.health -= bounce_dmg
  else:
    #set newest bounce distance (1/4 of first bounce)
    bounce2 = (1/4) * (1/4 * arrow_yards_traveled)
    position += bounce2
    if position in player1_hitbox:
      #set new bounce damage (1/3 of first bounce dmg)
      bounce_dmg2 = (1/3) * (player2.damage * 1/3)
      player1.health -= bounce_dmg2

  #classes for 3 selectable characters
#normal bowshooter (superclass), this guy will shoot normally but just do more damage then the others
class Archer(Bow):
  def __init__(self, name, bow, knockback):
   super().__init__("Archer", "Bow", knockback)



  def shoot(power, arc, damage):
    Bow.shoot(power, arc)
    self.damage = 34


#this guy will send an arrow in its general direction, and a small amount before it hits the ground
# the arrow will split into 2 arrows, but it will not land in the exact spot as planned, it will cone the two arrows
#to random spots around 0-25 yards within the original desitnation
#so if an arrow was planned to land at yard 250, two diff arrows may land around 243 and 259
class Magic_archer(Bow):
  def __init__(self, name, bow, knockback):
    super().__init__("Flame Archer", "Flame Bow", knockback)


  def shoot(power, arc, damage, split):
    Bow.shoot(power, arc)
    self.damage = 34
#arrow will bounce twice but the first bounce is double the distance of the second bounce, 
#bounce distance is dependent on the arc

class Bounce_archer(Bow):
  def __init__(self, name, bow, knockback):
    super().__init__("Bounce Archer", "Bouncing Bow", knockback)



  def shoot(power, arc, damage):
#the bounce attribute should make it so that the arrow lands in first designated yard, if hits count it,
#if not, bounce, lower damage by 1/3, if hits, count it, if not, bounce, lower damage again by 1/3
    Bow.shoot(power, arc)
    self.damage = 34

