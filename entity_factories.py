from components import level
from components.ai import HostileEnemy
from components import consumable
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

player = Actor(char="@", color=(255, 255, 255), name="Player", ai_cls=HostileEnemy, 
        fighter=Fighter(hp=30, defence=2, attack=5), inventory=Inventory(capacity=26), level=Level(level_up_base=200))

caveman = Actor(char="c", color=(255, 242, 161), name="Caveman", ai_cls=HostileEnemy,
        fighter=Fighter(hp=10, defence=0, attack=3), inventory=Inventory(capacity=0), level=Level(xp_given=30))
savage = Actor(char="S", color=(255, 220, 0), name="Savage", ai_cls=HostileEnemy,
        fighter=Fighter(hp=20, defence=1, attack=4), inventory=Inventory(capacity=0), level=Level(xp_given=75))

cavemoss = Item(char="m", color=(15, 215, 55), name="Cave Moss", consumable=consumable.HealingConsumable(amount=3))
rock = Item(char="r", color=(200, 200, 200), name="Rock", consumable=consumable.RangedDamageConsumable(damage=5, max_range=5))
mushrooms = Item(char="M", color=(255, 100, 100), name="Mushrooms", consumable=consumable.DazedConsumable(number_of_turns=10))
dirtpile = Item(char="d", color=(100, 70, 0), name="Dirt Pile", consumable = consumable.AreaDamageConsumable(damage=4, radius=3))