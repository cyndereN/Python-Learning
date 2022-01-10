'''
初始血量为100，轮番攻击，每次打出10-20点伤害，有20%几率防御成功不受伤害
'''
import random

class Player:
    def __init__(self,name):
        self.name = name
        self.health = 100

    def attack(self, target):
        print(self.name + " attack")
        damage = random.randint(10, 20)
        target.defend(damage)

    def defend(self, damage):
        if random.random()>0.2:
            self.health -= damage
            print(f"{self.name}: Taken {damage} damage, {self.health} HP left.")
            if self.health <= 0:
                print(f"{self.name}: Defeated.")
        else:
            print(self.name + ": Successfully defended.")

        print('-------------------------------')

kakarotto = Player('Kakarotto')
piccolo = Player('Piccolo')

while True:
    if kakarotto.health > 0:
        kakarotto.attack(piccolo)
    else:
        break

    if piccolo.health > 0:
        piccolo.attack(kakarotto)
    else:
        break