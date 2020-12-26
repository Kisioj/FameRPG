from npc import NPC

NPCs = {}


def register_npc(npc_class):
    NPCs[npc_class.identifier] = npc_class


OPPOSITE_DIRECTION_MAP = {
    'LEFT': 'RIGHT',
    'RIGHT': 'LEFT',
    'DOWN': 'UP',
    'UP': 'DOWN',
}

class Maciek(NPC):
    identifier = 'maciek'
    filename = 'rsc/M_03.png'
    metadata_filename = 'rsc/hero_sprite_metadata.json'

    def __init__(self, x, y, current_map):
        super().__init__(x, y, current_map, self.filename, self.metadata_filename)

    def talk(self, player):
        self.dir = OPPOSITE_DIRECTION_MAP[player.dir]
        print(f'{self.identifier}: Witaj!')


register_npc(Maciek)
