from npc import NPC

NPCs = {}


def register_npc(npc_class):
    NPCs[npc_class.identifier] = npc_class


class Maciek(NPC):
    identifier = 'maciek'
    filename = 'rsc/M_03.png'
    metadata_filename = 'rsc/hero_sprite_metadata.json'

    def __init__(self, x, y, current_map):
        super().__init__(x, y, current_map, self.filename, self.metadata_filename)


register_npc(Maciek)
