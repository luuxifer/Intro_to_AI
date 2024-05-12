import pygame
import chess

class Display():
    def __init__(self, board):
        self.run = False
        self.intro = True
        self.game_over = False
        self.dim = 500
        # store the address of square: a1, b2, c3, d4, ...
        self.boardPos = {}
        self.boardLayout = {}
        self.show_moves_surf_list = []
        self.selected_square = None
        self.square_to_move_too = None
        self.player_color = None
        self.clock = pygame.time.Clock()
        self.board = board
        self.fen = board.fen()

        pygame.init()
        self.window = pygame.display.set_mode((self.dim, self.dim))
        pygame.display.set_caption("Chess")

        self.chessboard = pygame.image.load("img/Board.jpg").convert_alpha()
        self.chessboard = pygame.transform.scale(self.chessboard, (self.dim, self.dim))

        self.show_moves_surf = pygame.Surface((50, 50), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.show_moves_surf, (0, 200, 0, 100), (25, 25), 20, 0)

        self.board_layout()

        self.update(self.board)

    def board_layout(self):
        for i in range(8):
            for j in range(8):
                self.boardPos[str(chr(i + 97) + str(j + 1))] = [i * 51.5 + 46, 405 - j * 51]

                self.boardLayout[str(chr(i + 97) + str(j + 1))] = None

    def update(self, board):
        for i in range(8):
            for j in range(8):
                self.boardLayout[str(chr(i + 97) + str(j + 1))] = None

        self.board = board 
        self.fen = board.fen()

        boardString = str(self.fen)[0: str(self.fen).find(' ')]
        boardString = boardString + '/'

        for j in range(8, 0, -1):
            dash = boardString.find('/')
            rawCode = boardString[0:dash]
            boardString = boardString[dash + 1 : len(boardString)]

            alphabetCounter = 97
            for char in rawCode:
                if char.isdigit():
                    alphabetCounter += int(char)
                else:
                    self.boardLayout[str(chr(alphabetCounter)) + str(j)] = self.pieceData(char)
                    alphabetCounter += 1

        self.update_screen()
    
    def update_screen(self):
        # This function updates the screen should be run every time a change is made to the board state
        self.window.blit(self.chessboard, (0, 0))
        # Display all pieces in BoardLayout
        for num in self.boardLayout:
            if self.boardLayout[num] != None:
                self.window.blit(self.boardLayout[num].render(), (self.boardPos[num][0], self.boardPos[num][1]))
        # Displays circles that show possible moves
        if self.show_moves_surf_list != []:
            for num in self.show_moves_surf_list:
                self.window.blit(self.show_moves_surf, (num[0], num[1]))

        pygame.display.update()
        self.clock.tick(10)

    def pieceData(self, piece):
        if(piece == 'p'): 
            return Piece("Pawn", "B")
        elif(piece == 'r'):
            return Piece("Rook", "B")
        elif(piece == 'n'):
            return Piece("Knight", "B")
        elif(piece == 'b'):
            return Piece("Bishop", "B")
        elif(piece == 'k'):
            return Piece("King", "B")
        elif(piece == 'q'):
            return Piece("Queen", "B")
        
        elif(piece == 'P'):
            return Piece("Pawn", "W")
        elif(piece == 'R'):
            return Piece("Rook", "W")
        elif(piece == 'N'):
            return Piece("Knight", "W")
        elif(piece == 'B'):
            return Piece("Bishop", "W")
        elif(piece == 'K'):
            return Piece("King", "W")
        elif(piece == 'Q'):
            return Piece("Queen", "W")
        
    # If the player Left Click on block the piece on that block is the one to be moved.
    # If there was a piece already selected  the second  click is the block the selected piece should move to.
    # Except if the second click is on a Piece of same cloro then that piece becomes the Pieced to be movesd
    def square_select(self, pos):
        x_board_pos = ((pos[0] - 45) // 50)
        y_board_pos = -((pos[1] - 405) // 50) + 1
        # Set piece to be moved
        if self.selected_square == None:
            self.square_to_move_too = None
            self.selected_square = str(chr(97 + x_board_pos) + str(y_board_pos))
            self.update_possible_moves()
            return None

        else:
            self.square_to_move_too = str(chr(97 + x_board_pos) + str(y_board_pos))
            result = str(self.selected_square + self.square_to_move_too)
            for move in self.board.legal_moves:
                if str(move) == str(result + "q"):
                    self.remove_square_select()
                    return str(result + "q")
                elif str(move) == result:
                    self.remove_square_select()
                    return result

            if self.boardLayout[str(chr(97 + x_board_pos) + str(y_board_pos))] != None:
                self.square_to_move_too = None
                self.selected_square = str(chr(97 + x_board_pos) + str(y_board_pos))
                self.update_possible_moves()
                return None

    # If RightClick the current selected Piece is set to None.
    def remove_square_select(self):
        self.selected_square = None
        self.square_to_move_too = None
        self.show_moves_surf_list = []
    def update_possible_moves(self):
        # This functions updates where the littler circles appear that show player where certain piece can move
        if self.selected_square != None:
            self.show_moves_surf_list.clear()
            lg = self.board.legal_moves
            for pos in lg:
                if str(pos)[0: 2] == self.selected_square:
                    self.show_moves_surf_list.append((self.boardPos[str(pos)[2: 4]][0], self.boardPos[str(pos)[2: 4]][1]))

    ####################
    # UI game
    def main_menu(self):
        red = (200, 0, 0)
        green = (0, 200, 0)

        bright_red = (255, 0, 0)
        bright_green = (0, 255, 0)

        while self.intro:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    pygame.quit()

            self.window.fill((255,255,255))
            largeText = pygame.font.SysFont("comicsansms", 115)
            TextSurf, TextRect = self.text_objects("Chess", largeText)
            TextRect.center = ((self.dim / 2), (self.dim / 2 - 100))
            self.window.blit(TextSurf, TextRect)

            self.button("WHITE", 50, 300, 100, 50, green, bright_green, 1)
            self.button("BLACK", 350, 300, 100, 50, green, bright_green, 2)
            self.button("Quit", 225, 400, 80, 50, red, bright_red, 3)

            pygame.display.update()
            self.clock.tick(15)

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.window, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                if action == 1:
                    self.player_color = "W"
                    self.run = True
                    self.intro = False
                    self.game_over = False
                elif action == 2:
                    self.player_color = "B"
                    self.run = True
                    self.intro = False
                    self.game_over = False
                elif action == 3:
                    pygame.quit()
                elif action == 4:
                    self.run = False
                    self.intro = True
                    self.game_over = False

        else:
            pygame.draw.rect(self.window, ic, (x, y, w, h))

        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.window.blit(textSurf, textRect)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect()


# Load pieces for board
class Piece():
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.dim = 45

        if(self.color == "W" or self.color == "w"):
            if(self.name == "Knight"):
                self.pieceSurface = pygame.image.load("img/Chess_" + self.name[1] + "lt60.png")
            else:
                self.pieceSurface = pygame.image.load("img/Chess_" + self.name[0] + "lt60.png")
        else: 
            if(self.name == "Knight"):
                self.pieceSurface = pygame.image.load("img/Chess_" + self.name[1] + "dt60.png")
            else:
                self.pieceSurface = pygame.image.load("img/Chess_" + self.name[0] + "dt60.png")

        self.pieceSurface = pygame.transform.scale(self.pieceSurface, (self.dim, self.dim))

    def render(self):
        return self.pieceSurface