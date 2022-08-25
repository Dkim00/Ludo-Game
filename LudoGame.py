

class LudoGame():
    """Class contains information about players and board movement. Holds information about the player class"""

    def __init__(self):
        """Initalizes players """
    
    def play_game(self, playersList, turns):
        """ takes in game movement information and moves/updates game """
        self._players = playersList  # list of player positions ['A','C'] is two players at position A and C
        # List of tuples with position and number, players will move with turns list instead of dice roll
        self._turnsList = turns
        self._list_of_players = []
        self.init_players()
        returnList = []
        
        for turn in self._turnsList:
            # print("move amount is: " + str(turn[1])) #MOVE TEST@@@@@@@
            
            self.move_token(self.get_player_by_position(turn[0]),self.determine_priority(turn[0],turn[1]),turn[1])
        for player in self._list_of_players:
            returnList.append(player.get_p_pos())
            returnList.append(player.get_q_pos())
            # print(str(player.get_pos()) + " token q count is: " + str(player.get_q_count()))
            # print(str(player.get_pos()) + " token p count is: " + str(player.get_p_count()))
            # print(str(player.get_pos()) + " token q POS is: " + str(player.get_q_pos()))
            # print(str(player.get_pos()) + " token p POS is: " + str(player.get_p_pos()))
            
        return returnList
    
    def init_players(self):
        """initializes list of players"""
        for x in self._players:
            self._list_of_players.append(Player(x))
            

    def get_player_by_position(self, player):
        """returns player object (player = a,b,c,d) as a string"""
        for players in self._list_of_players:
            # print(players.get_pos())
            if players.get_pos() == player:
                return players 
    
        return 'Player not found!'
            
        

    def move_token(self, player, priorityToken, turns):
        """takes in player, token and turns and moves token for the player, also stacks or kicks off other tokens if needed"""

        #returns if both tokens are complete
        if player.get_q_count() == 57 and player.get_p_count() == 57:
            player.set_win('Finished')
            return
       
        # checks if tokens are stacked, then moves both tokens
        if player.get_q_count() == player.get_p_count() and player.get_p_count() > 0 and int(player.get_p_count()) < 50:
            player.set_stacked(True)

        # movement for q token, if at home, on board or near home square
        if priorityToken == 'q': 
            # if 6 is not rolled from home
            if turns != 6 and player.get_q_pos() == 'H':
                return
            # if 6 is rolled from home
            elif turns == 6 and player.get_q_count() == -1:
                player.set_q_count(1) # sets count to 0 
                player.set_q_pos('R')
                
            # when token is going to enter home squares
            elif (player.get_q_count() + turns) > 50 and (player.get_q_count() + turns) < 57:
                player.set_q_count(turns)
                player.set_q_pos(player.get_pos() + str(player.get_q_count() - 50))

            #bounceback when token is over 57
            elif (player.get_q_count() + turns) > 57:
                diff = (player.get_q_count() + turns) - 57
                player.set_q_count(-player.get_q_count()+(57-diff))
                player.set_q_pos(player.get_pos() + str(player.get_q_count() - 50))    
            else:
                player.set_q_count(turns)  # adds the turns to count position
                # adds the turns to board location
                player.set_q_pos(player.get_space_name(player.get_q_count()))
                if player.is_stacked():
                    player.set_p_count(turns)
                    player.set_p_pos(player.get_space_name(player.get_q_count()))
           
         
                

        # movement for p token, same as q token
        if priorityToken == 'p':
            # if 6 is not rolled from home
            if turns != 6 and player.get_p_pos() == 'H':
                return
            # if 6 is rolled from home
            elif turns == 6 and player.get_p_count() == -1:
                player.set_p_count(1) # sets count to 0 
                player.set_p_pos('R')
                
            # when token is going to enter home squares
            elif (player.get_p_count() + turns) > 50 and (player.get_p_count() + turns) < 57:
                player.set_p_count(turns)
                player.set_p_pos(player.get_pos() + str(player.get_p_count() - 50))

            #bounceback if token is over 57
            elif (player.get_p_count() + turns) > 57:
                diff = (player.get_p_count() + turns) - 57
                player.set_p_count(-player.get_p_count() + (57-diff))
                player.set_p_pos(player.get_pos() + str(player.get_p_count() - 50))
                                
            else:
                player.set_p_count(turns)  # adds the turns to count position
                # adds the turns to board location
                player.set_p_pos(player.get_space_name(player.get_p_count()))
                if player.is_stacked():
                    player.set_q_count(turns)
                    player.set_q_pos(player.get_space_name(player.get_p_count()))
                    
        ##TEST @@@@@@@@@@@@@@@@@@@@@
        # print("position is: " + str(player.get_pos()))
        # print("q count is: " + str(player.get_q_count()))
        # print("p count is: " + str(player.get_p_count()))
        # print("q pos is: " + str(player.get_q_pos()))
        # print("p pos is: " + str(player.get_p_pos()))
        # print('\n')
                
        self.check_and_kick(player,priorityToken) 

                            
 

    def check_and_kick(self, curPlayer, token):
        """takes in current player and token and checks to see if token stacks any opponent token and kicks back opponents token, resets stack status"""

        if token == 'q':
            for players in self._list_of_players:
                if players is not curPlayer:
                    if players.get_q_pos() == curPlayer.get_q_pos() and curPlayer.get_q_count() > 0:
                        players.set_q_count(-(players.get_q_count()+1))
                        players.set_q_pos('H')
                        players.set_stacked(False)

                    if players.get_p_pos() == curPlayer.get_q_pos() and curPlayer.get_q_count() > 0:
                        players.set_p_count(-(players.get_p_count()+1))
                        players.set_p_pos('H')
                        players.set_stacked(False)

        elif token == 'p':
            for players in self._list_of_players:
                if players is not curPlayer:
                    if players.get_q_pos() == curPlayer.get_p_pos() and curPlayer.get_p_count() > 0:
                        # print('A')
                        players.set_q_count(-(players.get_q_count()+1))
                        players.set_q_pos('H')
                        players.set_stacked(False)

                    if players.get_p_pos() == curPlayer.get_p_pos() and curPlayer.get_p_count() > 0:
                        players.set_p_count(-(players.get_p_count()+1))
                        players.set_p_pos('H')
                        players.set_stacked(False)

        

    def determine_priority(self, pos, move):
        """takes in player pos, moves to make and returns token with priority """

        player = self.get_player_by_position(pos)  # player object
        pCount = player.get_p_count()
        qCount = player.get_q_count()

        if move == 6:
            # determines if any of the tokens are at the home space and returns that value
            if pCount == -1:
                return 'p'

            elif qCount == -1:
                return 'q'
        # if token is in home square and die roll is exact for final space
        elif pCount + move == 57:
            return 'p'

        elif qCount + move == 57:
            return 'q'

        # token can move and land on opponents token
        for x in self._list_of_players:
            if x is not player:
                # print(x.get_p_pos(), player.get_space_name(pCount + move), (x.get_p_pos() == str(player.get_space_name(player.get_p_count() + move))))
                # print(x.get_p_pos(), player.get_space_name(qCount + move), (x.get_p_pos() == str(player.get_space_name(player.get_q_count() + move))))
                # print(x.get_q_pos(), player.get_space_name(pCount + move), (x.get_q_pos() == str(player.get_space_name(player.get_p_count() + move))))
                # print(x.get_q_pos(), player.get_space_name(qCount + move), (x.get_q_pos() == str(player.get_space_name(player.get_q_count() + move))))
                
                if player.get_p_count() > 0 and (x.get_p_pos() == str(player.get_space_name(player.get_p_count() + move)) or x.get_q_pos() == str(player.get_space_name(player.get_p_count() + move))):
                    return 'p'
                if player.get_q_count() > 0 and (x.get_q_pos() == str(player.get_space_name(player.get_q_count() + move)) or x.get_q_pos() == str(player.get_space_name(player.get_q_count() + move))):
                    return 'q'

        # furthest token away from final space
        if pCount < qCount:
            if pCount  < 0:
                return 'q'
            return 'p'
        else:
            if qCount < 0:
                return 'p'
            return 'q'


class Player():
    """represents the player object at a specific position"""

    def __init__(self, pos):
        self._position = pos  # A/B/C/D
        self._startEnd = ()  # A(1,50):B(15,8):C(29,22):D(43,36)
        self._token_p_pos = "H"
        self._token_q_pos = "H"  # 'H'Home, 'R' First Space, 'E' Final Space
        self._winStatus = "Playing"  # Win, Finished, Playing
        self._isStacked = False # if the two tokens are stacked
        self._p_count = -1  # used to determine how far the tokens have traveled
        self._q_count = -1
        self.init_startEnd()

    def set_win(self,status):
        """setter for win status"""
        self._winStatus = status
        
    def get_completed(self):
        if self._winStatus != 'Playing':
            return True
        else:
            return False
        
    def get_pos(self):
        """Getter for player position A/B/C/D"""
        return self._position
    
    def set_stacked(self, status):
        """Setter for stacked status"""
        self._isStacked = status

    def is_stacked(self):
        """getter for stacked status"""
        return self._isStacked

    def get_position(self):
        """Getter for position"""
        return self._position

    def get_q_pos(self):
        """getter for q pos"""
        return self._token_q_pos

    def get_p_pos(self):
        """getter for p pos"""
        return self._token_p_pos

    def set_q_pos(self, pos):
        """setter for q token"""
        self._token_q_pos = str(pos)

    def set_p_pos(self, pos):
        """setter for p token"""
        self._token_p_pos = str(pos)

    def get_q_count(self):
        """getter for q count"""
        return self._q_count

    def get_p_count(self):
        """getter for p count"""
        return self._p_count

    def set_q_count(self, count):
        """setter for q count"""
        self._q_count += count

    def set_p_count(self, count):
        """setter for p count"""
        self._p_count += count

    def get_completed(self):
        """Returns true or False if player has finished or not finished"""
        if self._token_p_pos == 'E' and self._token_q_pos == 'E':
            return True
        else:
            return False
        
    def get_token_q_step_count(self):
        """returns total number of steps token q has taken on board"""
        return self._q_count

    def get_token_p_step_count(self):
        """returns total number of steps token p has taken on board"""
        return self._p_count

    def init_startEnd(self):
        """initilizes the start and ending values"""
        if self._position == 'A':
            self._startEnd = [0,50]
            
        elif self._position == 'B':
            self._startEnd = [14,8]  
              
        elif self._position == 'C':
            self._startEnd = [28,22]   
            
        elif self._position == 'D':
            self._startEnd = [42,36] 
                  
    def update_token_pos(self, token, newPos):
        """takes in q or p and updates the position"""
        if token == 'q':
            self._token_q_pos = newPos
        if token == 'p':
            self._token_p_pos = newPos
        else:
            return "Token is invalid"
        
    def get_space_name(self,steps):
        """takes in number of steps and returns where a token would be on the board"""
        # print(steps)
        pos = self._startEnd[0]
        if steps == -1:
            return 'H'
        
        if steps < 1:
            return 'R'
        
        elif steps < 51:
            for x in range(1,steps+1):
                pos += 1
                if pos > 56:
                    pos = 1
            return str(pos) 
        elif steps == 57:
            return 'E'
        elif steps >= 51:
            return (str(self._position) + str(steps - 50))

            
                    
        
            
            


def main():
    # game = LudoGame()
    
    # game = LudoGame()
    # game.play_game(['A', 'B', 'C', 'D'], [])

    # player_b = game.get_player_by_position('B')

    # space_1 = player_b.get_space_name(1)
    # # <class 'str'> 15
    # print(f'{type(space_1)} {space_1}')

    # space_56 = player_b.get_space_name(56)
    # # <class 'str'> B6
    # print(f'{type(space_56)} {space_56}')
    
    # game = LudoGame()
    # game.play_game(['A', 'B'], [])

    # player_a = game.get_player_by_position('A')
    # print(player_a.get_space_name(-1))  # should print 'H'
    # print(player_a.get_space_name(0))   # should print 'R'
    # print(player_a.get_space_name(57))  # should print 'E'

    # player_b = game.get_player_by_position('B')
    # print(player_b.get_space_name(-1))  # should print 'H'
    # print(player_b.get_space_name(0))   # should print 'R'
    # print(player_b.get_space_name(57))  # should print 'E'
    
    
    # players = ['A', 'B']
    # turns = [('A', 6), ('A', 4), ('A', 5), ('A', 4), ('B', 6), ('B', 4), ('B', 1), ('B', 2), ('A', 6), ('A', 4), ('A', 6), ('A', 3), ('A', 5), ('A', 1), ('A', 5), ('A', 4)]
    # game = LudoGame()
    # current_tokens_space = game.play_game(players, turns)
    # player_A = game.get_player_by_position('A')
    # print(player_A.get_completed())
    # print(player_A.get_token_p_step_count())
    # print(current_tokens_space)
    # player_B = game.get_player_by_position('B')
    # print(player_B.get_space_name(55))
    
    # CASE 1
    # player =  ['A','B','C','D']
    # turns = [('A', 6),('A', 1),('B', 6),('B', 2),('C', 6)]
    # # ['1', 'H', '16', 'H', '31', 'H', '46', 'H']
    # game.play_game(player,turns)
    
    # playA = game.get_player_by_position('D')
    # print(playA.get_space_name(20))
    # #CASE 2
    # players = ['A','B']
    # turns = [('B', 6),('B', 4),('B', 5),('B', 4),('B', 4),('B', 3),('B', 4),('B', 5),('B', 4),('B', 4),('B', 5),('B', 4),('B', 1),('B',4),('B', 5),('B', 5),('B', 5)]
    #['H', 'H', 'B6', 'H']
    
    # #CASE 3
    # players = ['A','B']
    # turns = [('A', 6),('A', 3),('A', 6),('A', 3),('A', 6),('A', 5),('A', 4),('A', 6),('A', 4)]
    #['28', '28', 'H', 'H']
    
    # #CASE 4
    # players = ['A','C']
    # turns = [('A', 6),('A', 4),('A', 4),('A', 4),('A', 5),('A', 6),('A', 4),('A', 6),('A', 4),('A', 6),('A', 6),('A', 6),('A', 4),('A', 6),('A', 6),('C', 6),('C', 4)]
    # #['33', 'H', '32', 'H']
    
    #CASE 5
    # players = ['A','B']
    # turns = [('A', 6),('A', 4),('A', 4),('A', 4),('A', 5),('A', 6),('A', 4),('A', 6),('A', 4),('A', 6),('A', 6),('A', 4),('A', 6),('A', 4),('A', 6),('A', 6),('A', 4),('A', 6),('A', 6),('A', 4),('A', 6),('A', 6),('A', 4),('A', 6),('A', 3),('A', 6),('B', 6),('A', 6)]
    #['E', 'E', 'R', 'H']

    #CASE 6
    # players = ['A','B']
    # turns = [('A', 6),('A', 2),('A', 2),('A', 6),('A', 4),('A', 5),('A', 4),('A', 4),('B', 6),('B', 3),('A', 6),('A', 3)]
    #'3', 'H', '17', 'H'
    
    # #CASE 7
    # players = ['A','B']
    # turns = [('A', 6),('A', 4),('A', 5),('A', 4),('A', 4),('A', 4),('A', 5),('A', 4),('A', 5),('A', 5),('A', 3),('A', 5),('A', 3),('A', 6)]
    #['A1', 'R', 'H', 'H']
   
    #CASE 8
    # players = ['A','B']
    # turns = [('A', 6),('A', 4),('A', 5),('A', 4),('A', 4),('A', 4),('A', 5),('A', 4),('A', 5),('A', 5),('A', 3),('A', 5),('A', 5),('A', 6),('A', 5),('A', 5),('A', 3),('B', 6),('B', 3),('A', 4)]
    #['E', '13', '17', 'H']
    
    # #CASE 9
    # players = ['A','B']
    # turns = [('A', 6),('A', 4),('A', 4),('A', 4),('A', 6),('A', 5),('A', 3),('B', 6),('B', 2),('A', 2),('A', 4)]
    # #['16', '10', 'H', 'H']
    
    # players = ['A','B']
    # turns = [('A', 6),('A',5),('A',6),('A',4),('B',6),('B',6),('B',2), ('B',2),('A',6),('A',6)]
    
    #[5,16,h,h]
    
    
    # players = ['A','B']
    # turns = [('B', 6),('B', 4),('B', 5),('B', 4),('B', 4),('B', 3),('B', 4),('B', 5),('B', 4),('B', 4),('B', 5),('B', 4),('B', 1),('B',4),('B', 5),('B', 5)]
    # ['A3', 'H', 'H', 'H'] 
  
        # playerA = game.get_player_by_position('A')
    
    # print(playerA.get_p_count())
    # print(game.determine_priority('A',5))
    
    # playerB = game.get_player_by_position('B')
    # print(playerA.get_space_name(50))
    # print(playerB.get_space_name(2))
    
    # playerC = game.get_player_by_position('C')
    # print(playerC.get_space_name(51))
    
    
    
    # print(game.play_game(players,turns))
    return


main()