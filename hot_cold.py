#time to create a mechanic which displays "Warm" and "Cold" depending on where the arrow lands relative to the opponent
#if the arrow lands within 5 spaces, display "Very Warm"
#if the arrow lands within 15 spaces, display "Warm"
#if arrow lands farther than 15, display "Cold"
#if the arrow lands farther than 50 spaces, display "Very Cold"

the shoot() method will shoot an object (Arrow) some number of spaces, "Arrow" will land at a  "position" (position will be 3 spaces 
to make a 3 space hitbox) where the opponent is standing
code will look as seen

after shoot()

if arrow in position:
  PlayerX.TakeDamage() #THIS WILL DEPEND ON WHICH CHARACTER SHOOTER IS BECAUSE THERE ARE DIFF ARROWS THAT DO DIFF DAMAGE
  
elif arrow in (position - 5 , position -1) or (position + 5 , position + 1): #These parentheses are ranges of spaces between the person and arrow
  print("Very Warm!")
  
elif arrow in (position - 15, position - 6) or (position + 15 , position + 6): 
  print("Warm')
  
elif arrow in (position - 50, position - 16) or (position + 50 , position + 16): 
  print("Cold")
  
else:
 print("Very Cold")

switch_turn() #PLAYER TURN SHOULD SWITCH AFTER ARROW IS SHOT
