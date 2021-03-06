import sys, requests
import pandas as pd
        
class Deck:
    """Manage deck statistics here"""
    def __init__(self, deck_name='', export_json=None):
        if export_json != None:
            self.cards = pd.read_json(export_json['cards'])
            self.side_board = pd.read_json(export_json['side_board'])
        else:
            self.cards = pd.DataFrame()
            self.side_board = pd.DataFrame()
        self.name=deck_name
        
    def lookup_card_by_name(self, card_name):
        r = requests.get('https://api.magicthegathering.io/v1/cards', params={'name':card_name})
        
        try:
            card_dict = r.json()['cards'][-1]
            return pd.DataFrame.from_dict(card_dict, orient='index').transpose()
        except Exception as e:
            # Probably misspelled the card name
            sys.exit(e)
    
    def add_card(self, card_name, amount=1, to_sideboard=False):
        card = self.lookup_card_by_name(card_name)
        if to_sideboard:
            self.side_board = self.side_board.append([card for _ in range(amount)], ignore_index=True)
        else:
            self.cards = self.cards.append([card for _ in range(amount)], ignore_index=True)
        
    def get_cards_by_type(self, card_types):
        mask = self.cards['types'].apply(lambda x: bool(set(x).intersection(card_types)))
        return self.cards[mask]
    
    def get_non_land_cards(self):
        mask = self.cards['types'].apply(lambda x: not bool(set(x).intersection(['Land'])))
        return self.cards[mask]
    
    def shuffle(self):
        return self.cards.sample(frac=1).reset_index(drop=True)
    
    def export_json(self):
        card_json = self.cards.to_json()
        side_board_json = self.side_board.to_json()
        return {'cards': card_json, 'side_board': side_board_json}
        
