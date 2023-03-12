import random
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

games = {}
users = {}

class Game:
    def __init__(self):
        self.players = []
        self.judge = None
        self.prompt = None
        self.submissions = []
        self.winner = None
    
    def add_player(self, user_id):
        self.players.append(user_id)
    
    def set_judge(self, user_id):
        self.judge = user_id
    
    def set_prompt(self, prompt):
        self.prompt = prompt
    
    def add_submission(self, submission):
        self.submissions.append(submission)
    
    def set_winner(self, submission_id):
        self.winner = submission_id
    

@app.get("/games")
def get_games():
    return JSONResponse(content=jsonable_encoder(games))


@app.post("/games")
def join_game(user_id: str):
    game_found = False
    for game_id, game in games.items():
        if len(game.players) < 10:
            game.add_player(user_id)
            users[user_id] = game_id
            game_found = True
            if len(game.players) == 10:
                start_game(game_id)
            break
    
    if not game_found:
        game_id = len(games) + 1
        game = Game()
        game.add_player(user_id)
        users[user_id] = game_id
        games[game_id] = game
    
    return {"game_id": game_id}


@app.get("/games/{game_id}/updates")
async def game_updates(game_id: int, user_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if user_id not in games[game_id].players:
        raise HTTPException(status_code=404, detail="User not found in this game")
    
    while not games[game_id].winner:
        await asyncio.sleep(1)

    return {"winner": games[game_id].winner}


@app.post("/games/{game_id}/prompt_reply")
def prompt_reply(game_id: int, user_id: str, submission: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if user_id not in games[game_id].players:
        raise HTTPException(status_code=404, detail="User not found in this game")
    
    games[game_id].add_submission({"user_id": user_id, "submission": submission})


@app.post("/games/{game_id}/pick_winner")
def pick_winner(game_id: int, user_id: str, submission_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if user_id != games[game_id].judge:
        raise HTTPException(status_code=401, detail="Only the judge can pick the winner")
    
    games[game_id].set_winner(submission_id)


def start_game(game_id):
    game = games[game_id]
    game.set_judge(game.players[0])
    game.set_prompt("Describe a day in the life of a superhero")
    for player in game.players:
        if player != game.judge:
            prompt = prompt_for_player(player)
            game.add_submission({"user_id": player, "submission": prompt})
    

def prompt_for_player(user_id):
    return " ".join(random.choice(words) for i in range(5))
