# Important classes
from timeit import default_timer as timer
from game.ntxuva_ttt_game import NtxuvaGame
from extra_tools.save_data import Save_data
from extra_tools.elo_rating import EloRater
from agents.qplayerandothers.players import QPlayer,RandomPlayer

start = timer()

EPISODES = 100_000

game = NtxuvaGame(player1=RandomPlayer(mark='X'), player2=QPlayer(mark='O'))

data_saver = Save_data(player1=game.player1, player2=game.player2, filename=f'qlearn_vs_random_{EPISODES}')
p1_rating = data_saver.get_elo(game.player1.player_name)
p2_rating = data_saver.get_elo(game.player2.player_name)

elo = EloRater(game.player1,game.player2,K=1)

for episode in range(EPISODES):

    print(f" -- {episode} -- ")

    winner = game.play()

    if winner is not None:
        winner.wins = winner.wins + 1


    p1_rating[str(len(p1_rating))],p2_rating[str(len(p2_rating))] = \
        elo.new_rating(ra=p1_rating[str(len(p1_rating)-1)], rb=p2_rating[str(len(p2_rating) - 1)], d=elo.d[winner])

    game.reset()

data_saver.save(players={1: game.player1, 2: game.player2}, ratings={1: p1_rating, 2: p2_rating})

end = timer()

print (f"completed in {round(end - start,2)} seconds!")