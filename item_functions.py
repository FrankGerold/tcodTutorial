import tcod
from game_messages import Message

def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You\'re already at full health!', tcod.green)})

    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('You start to feel better!', tcod.green)})

    return results
