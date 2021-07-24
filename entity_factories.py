from components.ai import HostileEnemy
from components.fighter import Fighter
from entity import Actor

player = Actor(char="@", color=(255, 255, 255), name="Player", ai_cls=HostileEnemy, fighter=Fighter(hp=30, defence=2, attack=5),)

caveman = Actor(char="c", color=(255, 242, 161), name="Caveman", ai_cls=HostileEnemy, fighter=Fighter(hp=10, defence=0, attack=3),)
savage = Actor(char="S", color=(255, 220, 0), name="Savage", ai_cls=HostileEnemy, fighter=Fighter(hp=20, defence=1, attack=4),)