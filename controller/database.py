import json
from tinydb import TinyDB
from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match


def save_db(db_name, serialized_data):
    db = TinyDB("data/" + db_name + ".json")

    # Check si l'objet que l'on tente de save n'est pas déjà présent dans la db
    not_in_db = True
    for item in db:
        if serialized_data["name"] != item["name"]:
            not_in_db = True
        else:
            not_in_db = False
            break

    # Si pas présent, on save, sinon on l'update
    if not_in_db:
        db.insert(serialized_data)
        print(f"{serialized_data['name']} sauvegardé avec succès.")
    else:
        db.update(serialized_data)
        print(f"{serialized_data['name']} updaté avec succès.")


def load_db(db_name):
    db = TinyDB("data/" + db_name + ".json")
    return db.all()


def load_player(serialized_player, load_tournament_score=False):
    player = Player(
        serialized_player["name"],
        serialized_player["first_name"],
        serialized_player["dob"],
        serialized_player["sex"],
        serialized_player["total_score"],
        serialized_player["rank"]
    )
    if load_tournament_score:
        player.tournament_score = serialized_player["tournament_score"]
    return player


def load_tournament(serialized_tournament):
    loaded_tournament = Tournament(
        serialized_tournament["name"],
        serialized_tournament["place"],
        serialized_tournament["date"],
        serialized_tournament["time_control"],
        [load_player(player, load_tournament_score=True) for player in serialized_tournament["players"]],
        serialized_tournament["nb_rounds"],
        serialized_tournament["desc"]
    )
    loaded_tournament.rounds = load_rounds(serialized_tournament, loaded_tournament)

    return loaded_tournament


def load_rounds(serialized_tournament, tournament):

    loaded_rounds = []

    # Re-création des pairs avec les instances joueurs créées lors du chargement du tournoi
    for round in serialized_tournament["rounds"]:
        players_pairs = []
        for pair in round["players_pairs"]:
            for player in tournament.players:
                if player.name == pair[0]["name"]:
                    pair_p1 = player
                elif player.name == pair[1]["name"]:
                    pair_p2 = player
            players_pairs.append((pair_p1, pair_p2))
        loaded_round = Round(
            round["name"],
            players_pairs,
            load_match=True
        )
        loaded_round.matchs = [load_match(match, tournament) for match in round["matchs"]]
        loaded_round.start_date = round["start_date"]
        loaded_round.end_date = round["end_date"]
        loaded_rounds.append(loaded_round)

    return loaded_rounds


def load_match(serialized_match, tournament):

    # Re-création des matchs avec les instances joueurs créées lors du chargement du tournoi
    for player in tournament.players:
        if player.name == serialized_match["player1"]["name"]:
            player1 = player
        elif player.name == serialized_match["player2"]["name"]:
            player2 = player

    loaded_match = Match(
        (player1, player2)
    )
    loaded_match.score_player1 = serialized_match["score_player1"]
    loaded_match.color_player1 = serialized_match["color_player1"]
    loaded_match.score_player2 = serialized_match["score_player2"]
    loaded_match.color_player2 = serialized_match["color_player2"]
    loaded_match.winner = serialized_match["winner"]

    return loaded_match










