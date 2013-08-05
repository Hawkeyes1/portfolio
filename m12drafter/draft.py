# Drafting backend (no good AI yet; it just picks using only the mds numbers)

import m12data

def new_sealed():
    cards = []
    for i in range(6):
        cards.extend(m12data.random_pack())
    return cards

def new_draft():
    return [m12data.random_pack() for i in range(8)], [[] for i in range(8)], 0

def ai_pick_fun(pack,deck):
    return min(pack,key=lambda x: m12data.draft_picks[x])

'''    top_colored = [x for x in deck if x in m12data.colored]
    top_colored.sort(key = lambda x: m12data.draft_picks[x])
    if len(top_colored) == 0:
        return min(pack,key=lambda x: m12data.draft_picks[x])
    else:
        top = top_colored[0]
        '''
        

def draft_step(packs,decks,num_picked,player_pick):
    if player_pick in packs[0]:
        packs[0].remove(player_pick)
        decks[0].append(player_pick)
        for i in range(1,8):
            ai_pick = ai_pick_fun(packs[i],decks[i])
            packs[i].remove(ai_pick)
            decks[i].append(ai_pick)
        num_picked += 1
        if num_picked == 15 or num_picked == 30:
            for i in range(8):
                packs[i] = m12data.random_pack()
        else:
            if num_picked < 15 or num_picked > 30:
                # rotate left
                packs = packs[1:] + [packs[0]]
            else:
                # rotate right
                packs = [packs[-1]] + packs[:-1]
    return packs, decks, num_picked

def print_draft(packs, decks, num_picked):
    for i in range(8):
        print "Player %d:"%i
        print "Current pack: %s"%str(packs[i])
        print "Deck: %s"%str(decks[i])
        print ""

def draft_unpack(packs,decks,num_picked):
    n = len(packs)/8
    packs = [packs[i*n:(i+1)*n] for i in range(8)]
    decks = [decks[i*num_picked:(i+1)*num_picked] for i in range(8)]
    return packs,decks

def draft_repack(packs,decks):
    packs1 = []
    decks1 = []
    for i in range(8):
        packs1.extend(packs[i])
        decks1.extend(decks[i])
    return packs1,decks1

def draft_test():
    packs, decks, num_picked = new_draft()
    while num_picked < 45:
        print_draft(packs, decks, num_picked)
        player_pick = input("Player pick?")
        packs, decks, num_picked = draft_step(packs,decks,num_picked,player_pick)
