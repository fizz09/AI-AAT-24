outcomes = lambda: expando
outcomes.inProgress = "0 in progress"
outcomes.lose = "1 lose"
outcomes.tie = "2 tie"
outcomes.win = "3 win"

getNextPlayer = {"X": "O", "O": "X"}.get

cells = [(r,c) for r in range(3) for c in range(3)]

lines = [
    [(0,0),(0,1),(0,2)],
    [(1,0),(1,1),(1,2)],
    [(2,0),(2,1),(2,2)],

    [(0,0),(1,0),(2,0)],
    [(0,1),(1,1),(2,1)],
    [(0,2),(1,2),(2,2)],

    [(0,0),(1,1),(2,2)],
    [(2,0),(1,1),(0,2)],
]

def getMoves(player, board):
    return [(r,c) for (r,c) in cells if board[r][c] == "_"]

def makeMove(player, board, move):
    moved = board[:]
    moved[move[0]] = moved[move[0]][:]
    moved[move[0]][move[1]] = player
    return moved

def isWinning(player, board):
    return any(all(board[r][c] == player for (r,c) in line) for line in lines)

def getStatus(player, board):
    if isWinning(player, board): return outcomes.win
    elif isWinning(getNextPlayer(player), board): return outcomes.lose
    elif any("_" in row for row in board): return outcomes.inProgress
    else: return outcomes.tie

def getBestMove(player, board):
    moves = getMoves(player, board)
    if len(moves) in [1, 9]: return moves[0]

    boards = {move: makeMove(player, board, move) for move in moves}
    for move in moves:
        if isWinning(player, boards[move]): return move

    outcomes = {move: getOutcome(player, boards[move]) for move in moves}
    best = max(outcomes.values())
    for move in moves:
        if outcomes[move] == best: return move

def getOutcome(player, board):
    opponent = getNextPlayer(player)
    moves = getMoves(opponent, board)

    status = getStatus(player, board)
    if not moves or status == outcomes.win: return status

    return min(getOpponentOutcome(opponent, makeMove(opponent, board, move)) for move in moves)

def getOpponentOutcome(opponent, board):
    player = getNextPlayer(opponent)
    moves = getMoves(player, board)

    status = getStatus(player, board)
    if not moves or status == outcomes.lose: return status

    return max(getOutcome(player, makeMove(player, board, move)) for move in moves)

def nextMove(player, board):
    move = getBestMove(player, board)
    print(move[0], move[1])

player = input().strip()  # Read player input
board = []
for i in range(3):
    board.append(list(input().strip()))  # Read each row of the board

nextMove(player, board)
