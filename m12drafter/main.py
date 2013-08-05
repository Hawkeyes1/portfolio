import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

from google.appengine.ext import db

import draft as draft_backend
import m12data
import random

class Card(db.Model):
    num = db.IntegerProperty()
    name = db.StringProperty(multiline=False)
    multiplicity = db.IntegerProperty()

class Deck(db.Model):
    name = db.StringProperty(multiline=False)
    cards = db.ListProperty(int,default=None)
    sideboard = db.ListProperty(int,default=None)
    owner = db.UserProperty()

class Draft(db.Model):
    owner = db.UserProperty()
    packs = db.ListProperty(int,default=None)
    decks = db.ListProperty(int,default=None)
    num_picked = db.IntegerProperty()

class Game(db.Model):
    player1 = db.UserProperty()
    player2 = db.UserProperty()
    library1 = db.ListProperty(int,default=None)
    hand1 = db.ListProperty(int,default=None)
    graveyard1 = db.ListProperty(int,default=None)
    life1 = db.IntegerProperty()
    library2 = db.ListProperty(int,default=None)
    hand2 = db.ListProperty(int,default=None)
    graveyard2 = db.ListProperty(int,default=None)
    life2 = db.IntegerProperty()

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            drafts = db.GqlQuery("SELECT * FROM Draft WHERE owner = :1",user).fetch(1000)
            games = db.GqlQuery("SELECT * FROM Game WHERE player1 = :1",user).fetch(1000) + \
                db.GqlQuery("SELECT * FROM Game WHERE player2 = :1",user).fetch(1000)
            url = users.create_logout_url(self.request.uri)
            if users.is_current_user_admin():
                user_decks = db.GqlQuery("SELECT * FROM Deck").fetch(1000)
                public_decks = []
            else:
                user_decks = db.GqlQuery("SELECT * FROM Deck WHERE owner = :1 ORDER BY name DESC",user).fetch(1000)
                public_decks = db.GqlQuery("SELECT * FROM Deck WHERE owner != :1",user).fetch(1000)
            template_values = {
            'public_decks': public_decks,
            'user_decks': user_decks,
            'drafts':drafts,
            'user': user,
            'games':games,
            'logout_url': url,
            'rares':m12data.common
            }
            path = os.path.join(os.path.dirname(__file__), 'main_page.html')
            self.response.out.write(template.render(path, template_values))
        else:
            public_decks = Deck.all().run()
            url = users.create_login_url(self.request.uri)
            template_values = {'url': url, 'public_decks': public_decks}
            path = os.path.join(os.path.dirname(__file__), 'logged_out.html')
            self.response.out.write(template.render(path, template_values))

def runlength(lst):
    lst.sort()
    out = []
    for i in lst:
        if out != [] and out[-1][0] == i:
            out[-1][1] += 1
        else:
            out.append([i,1])
    return out

def card_object(rl_card):
    num,mult = rl_card
    name = m12data.card_text[num][1]
    card = Card(num=num)
    if mult == 1:
        card.name = name
    else:
        card.name = "%dx %s"%(mult,name)
    return card

class DeckPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        key = self.request.get("key")
        deck = Deck.get(key)
        if user:
            url = users.create_logout_url(self.request.uri)
            maindeck = [card_object(x) for x in runlength(deck.cards)]
            sideboard = [card_object(x) for x in runlength(deck.sideboard)]
            template_values = {'maindeck': maindeck, 'sideboard':sideboard}
            if deck.owner == user or users.is_current_user_admin():
                path = os.path.join(os.path.dirname(__file__), 'deck_page_owner.html')
                self.response.out.write(template.render(path, template_values))
            else:
                path = os.path.join(os.path.dirname(__file__), 'deck_page_public.html')
                self.response.out.write(template.render(path, template_values))
        else:
            template_values = {'deck': deck}
            path = os.path.join(os.path.dirname(__file__), 'deck_page_public.html')
            self.response.out.write(template.render(path, template_values))

class GamePage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        key = self.request.get("key")
        game = Game.get(key)
        if game.player1 == user:
            library1 = game.library1
            graveyard1 = game.graveyard1
            hand1 = game.hand1
            life1 = game.life1
            library2 = game.library2
            graveyard2 = game.graveyard2
            hand2 = game.hand2
            life2 = game.life2
        elif game.player2 == user:
            library2 = game.library1
            graveyard2 = game.graveyard1
            hand2 = game.hand1
            life2 = game.life1
            library1 = game.library2
            graveyard1 = game.graveyard2
            hand1 = game.hand2
            life1 = game.life2
        template_values = {'library1':library1,'graveyard1':graveyard1,'life1':life1,'hand1':hand1, 
            'library2':library2,'graveyard2':graveyard2,'life2':life2,'hand2':hand2}
        path = os.path.join(os.path.dirname(__file__), 'game.html')
        self.response.out.write(template.render(path, template_values))

class DraftPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        key = self.request.get("key")
        draft = Draft.get(key)
        packs, decks = draft_backend.draft_unpack(draft.packs,draft.decks,draft.num_picked)
        if user and draft.owner == user:
            template_values = {'pack': packs[0],'deck':decks[0],'key':key}
            path = os.path.join(os.path.dirname(__file__), 'draft_page.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect('/')

class NewSealed(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            cards = draft_backend.new_sealed()
            deck = Deck()
            deck.cards = []
            deck.sideboard = sorted(cards)
            deck.name = "New Sealed Draft"
            deck.owner = user
            deck.put()
            self.redirect('/')
        else:
            url = users.create_login_url(self.request.uri)
            template_values = {'url': url}
            path = os.path.join(os.path.dirname(__file__), 'logged_out.html')
            self.response.out.write(template.render(path, template_values))

class NewGame(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            cards1 = draft_backend.new_sealed()
            cards2 = draft_backend.new_sealed()
            game = Game()
            game.player1 = user
            game.life1 = 20
            game.life2 = 20
            random.shuffle(cards1)
            random.shuffle(cards2)
            game.library1 = cards1[7:]
            game.library2 = cards2[7:]
            game.hand1 = cards1[:7]
            game.hand2 = cards2[:7]
            game.graveyard1 = []
            game.graveyard2 = []
            game.put()
            self.redirect('/')
        else:
            url = users.create_login_url(self.request.uri)
            template_values = {'url': url}
            path = os.path.join(os.path.dirname(__file__), 'logged_out.html')
            self.response.out.write(template.render(path, template_values))

class NewBooster(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            draft = Draft()
            draft.owner = user
            packs, decks, draft.num_picked = draft_backend.new_draft()
            draft.packs, draft.decks = draft_backend.draft_repack(packs,decks)
            draft.put()
            self.redirect('/')
        else:
            url = users.create_login_url(self.request.uri)
            template_values = {'url': url}
            path = os.path.join(os.path.dirname(__file__), 'logged_out.html')
            self.response.out.write(template.render(path, template_values))

class DraftPick(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            key = self.request.get("key")
            card = int(self.request.get("card"))
            draft = Draft.get(key)
            if draft.owner != user:
                self.redirect('/')
            packs,decks = draft_backend.draft_unpack(draft.packs,draft.decks,draft.num_picked)
            packs,decks, draft.num_picked = draft_backend.draft_step(packs,decks, draft.num_picked, card)
            draft.packs,draft.decks = draft_backend.draft_repack(packs,decks)
            if draft.num_picked == 45:
                deck = Deck()
                deck.cards = []
                deck.sideboard = sorted(draft.decks[:45])
                deck.name = "Completed Booster Draft"
                deck.owner = user
                deck.put()
                draft.delete()
                self.redirect('/')
            else:
                draft.put()
                self.redirect('/draft?key=%s'%(key))
        else:
            url = users.create_login_url(self.request.uri)
            template_values = {'url': url}
            path = os.path.join(os.path.dirname(__file__), 'logged_out.html')
            self.response.out.write(template.render(path, template_values))

class Toggle(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            key = self.request.get("key")
            card = int(self.request.get("card"))
            source = self.request.get("source")
            deck = Deck.get(key)
            if deck.owner != user:
                self.redirect('/')
            if source == 'sideboard':
                if card in list(deck.sideboard):
                    deck.sideboard.remove(card)
                    deck.cards.append(card)
                    deck.cards = sorted(deck.cards)
            elif source == 'cards':
                if card in list(deck.cards):
                    deck.cards.remove(card)
                    deck.sideboard.append(card)
                    deck.sideboard = sorted(deck.sideboard)
            deck.put()
            template_values = {}
            path = os.path.join(os.path.dirname(__file__), 'empty.html')
            self.response.out.write(template.render(path, template_values))
        else:
            url = users.create_login_url(self.request.uri)
            template_values = {'url': url}
            path = os.path.join(os.path.dirname(__file__), 'logged_out.html')
            self.response.out.write(template.render(path, template_values))

class Rename(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            key = self.request.get("key")
            name = self.request.get("name")
            deck = Deck.get(key)
            if deck.owner == user:
                deck.name = name
                deck.put()
                url = users.create_logout_url(self.request.uri)
                template_values = {'deck': deck, 'logout_url':url}
                path = os.path.join(os.path.dirname(__file__), 'deck_page_owner.html')
                self.response.out.write(template.render(path, template_values))
        else:
            self.redirect('/')
  
                
class DeleteGame(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            key = self.request.get("key")
            game = Game.get(key)
            if game.player1 == user or  users.is_current_user_admin() or game.player2 == user:
                game.delete()
                self.redirect('/') 
        else:
            self.redirect('/') 
                
class DeleteDeck(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            key = self.request.get("key")
            name = self.request.get("name")
            deck = Deck.get(key)
            if deck.owner == user or  users.is_current_user_admin():
                deck.delete()
                self.redirect('/') 
        else:
            self.redirect('/') 

class DeleteDraft(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            key = self.request.get("key")
            name = self.request.get("name")
            draft = Draft.get(key)
            if draft.owner == user or  users.is_current_user_admin():
                draft.delete()
                self.redirect('/') 
        else:
            self.redirect('/')      

class All(webapp.RequestHandler):
    def get(self):
        url = users.create_login_url(self.request.uri)
        path = os.path.join(os.path.dirname(__file__), 'all.html')
        
        template_values = {'cards':[(i,i) for i in range(1,250)]}
        self.response.out.write(template.render(path, template_values))
       



application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                     ('/deck',DeckPage),
                                     ('/new_sealed',NewSealed),
                                     ('/new_game',NewGame),
                                     ('/toggle',Toggle),
                                     ('/rename',Rename),
                                     ('/delete_deck',DeleteDeck),
                                     ('/delete_draft',DeleteDraft),
                                     ('/delete_game',DeleteGame),
                                     ('/all',All),
                                     ('/draft',DraftPage),
                                     ('/pick',DraftPick),
                                     ('/game',GamePage),
                                     ('/new_booster',NewBooster)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

