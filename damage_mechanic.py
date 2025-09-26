def take_damage(self, damage):
    self.health -= damage
    self.health = max(0, self.health)  # Stops health from going negative
    print(f"{self.name} takes {damage} damage. Current health: {self.health}")