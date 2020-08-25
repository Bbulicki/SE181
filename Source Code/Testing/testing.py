import GameManager as game
import unittest
import copy

board = game.startGame()

class TestGame(unittest.TestCase):
    """
    Test the startGame function
    """

    def test_startGame(self):
        """
        Test that the addition of two integers returns the correct total
        """
        #board = [[['r', 0], ['n', 0], ['b', 0], ['q', 0], ['k', 0], ['b', 0], ['n', 0], ['r', 0]], [['p', 0], ['p', 0], ['p', 0], ['p', 0], ['p', 0], ['p', 0], ['p', 0], ['p', 0]], [['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2]], [['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2]], [['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2]], [['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2]], [['P', 0], ['P', 0], ['P', 0], ['P', 0], ['P', 0], ['P', 0], ['P', 0], ['P', 0]], [['R', 0], ['N', 0], ['B', 0], ['Q', 0], ['K', 0], ['B', 0], ['N', 0], ['R', 0]]]
        result = game.startGame()
        self.assertEqual(result, board)

    def test_simpleBoard(self):
        w_board = """['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
                    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']
                    ['.', '.', '.', '.', '.', '.', '.', '.']
                    ['.', '.', '.', '.', '.', '.', '.', '.']
                    ['.', '.', '.', '.', '.', '.', '.', '.']
                    ['.', '.', '.', '.', '.', '.', '.', '.']
                    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
                    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']"""
        w_result = game.simpleBoard(board, "w")
        b_result = game.simpleBoard(board, "b")
        self.assertEqual(w_result, game.simpleBoard(board, "w"))
        self.assertIsNot(b_result, w_board)
    
    def test_findMoves(self):
        #for the white side
        self.assertIn([1,0],game.findMoves(board, 0, 0)) #w-left-rook
        self.assertIn([0,1],game.findMoves(board, 0, 0)) #w-left-rook
        self.assertNotIn([4,0],game.findMoves(board, 0, 0)) 
        self.assertIn([2,0],game.findMoves(board, 0, 1)) #w-left-knight
        self.assertIn([2,2],game.findMoves(board, 0, 1)) #w-left-knight
        self.assertIn([1,3],game.findMoves(board, 0, 1)) #w-left-knight
        self.assertNotIn([1,1],game.findMoves(board, 0, 2)) #w-left-bishap
        self.assertNotIn([1,2],game.findMoves(board, 0, 2)) #w-left-bishap
        self.assertNotIn([1,3], game.findMoves(board, 0, 2)) #w-left-bishap
        self.assertNotIn([1,2], game.findMoves(board, 0, 3)) #w-queen
        self.assertIn([1,3], game.findMoves(board, 0, 3)) #w-queen
        self.assertNotIn([1,4], game.findMoves(board, 0, 3)) #w-queen
        self.assertIn([0,4], game.findMoves(board, 0, 3)) #w-queen
        self.assertIn([0,5], game.findMoves(board, 0, 4)) #w-king
        self.assertIn([1,3], game.findMoves(board, 0, 4)) #w-king
        self.assertNotIn([1,4], game.findMoves(board, 0, 5)) #w-right-bishap
        self.assertNotIn([1,6], game.findMoves(board, 0, 5)) #w-right-bishap
        self.assertNotIn([1,3],game.findMoves(board, 0, 6)) #w-right-knight
        self.assertIn([1,4],game.findMoves(board, 0, 6)) #w-right-knight
        self.assertIn([1,7],game.findMoves(board, 0, 7)) #w-right-rook
        self.assertIn([2,0],game.findMoves(board, 1, 0))
        self.assertIn([3,0],game.findMoves(board, 1, 0))
        self.assertNotIn([2,0],game.findMoves(board, 1, 1))
        self.assertIn([2,1],game.findMoves(board, 1, 1))
        self.assertIn([2,2],game.findMoves(board, 1, 2))
        self.assertIn([3,3],game.findMoves(board, 1, 3))
        self.assertNotIn([2,2],game.findMoves(board, 1, 4))
        self.assertNotIn([0,5],game.findMoves(board, 1, 5))
        self.assertIn([3,6],game.findMoves(board, 1, 6))
        self.assertNotIn([2,6],game.findMoves(board, 1, 7))
        #for the black side
        self.assertIn([6,0],game.findMoves(board, 7, 0)) #left-rook
        self.assertNotIn([6,1],game.findMoves(board, 7, 0)) #left-rook
        self.assertIn([5,2],game.findMoves(board, 7, 1)) #left-knight
        self.assertIn([5,0],game.findMoves(board, 7, 1)) #left-knight
        self.assertNotIn([6,1],game.findMoves(board, 7, 2)) #left-bishap
        self.assertNotIn([6,2],game.findMoves(board, 7, 2)) #left-bishap
        self.assertNotIn([6,3], game.findMoves(board, 7, 2)) #left-bishap
        self.assertNotIn([6,2], game.findMoves(board, 7, 3)) #queen
        self.assertIn([6,3], game.findMoves(board, 7, 3)) #queen
        self.assertNotIn([6,4], game.findMoves(board, 7, 3)) #queen
        self.assertIn([7,4], game.findMoves(board, 7, 3)) #queen
        self.assertIn([7,5], game.findMoves(board, 7, 4)) #king
        self.assertIn([6,3], game.findMoves(board, 7, 4)) #king
        self.assertNotIn([7,3], game.findMoves(board, 7, 5)) #right-bishap
        self.assertNotIn([7,6], game.findMoves(board, 7, 5)) #right-bishap
        self.assertNotIn([7,3],game.findMoves(board, 7, 6)) #right-knight
        self.assertIn([6,4],game.findMoves(board, 7, 6)) #right-knight
        self.assertIn([6,7],game.findMoves(board, 7, 7)) #right-rook
        self.assertIn([5,0],game.findMoves(board, 6, 0))
        self.assertIn([4,0],game.findMoves(board, 6, 0))
        self.assertNotIn([5,0],game.findMoves(board, 6, 1))
        self.assertIn([5,1],game.findMoves(board, 6, 1))
        self.assertIn([5,2],game.findMoves(board, 6, 2))
        self.assertIn([4,3],game.findMoves(board, 6, 3))
        self.assertNotIn([5,2],game.findMoves(board, 6, 4))
        self.assertNotIn([7,5],game.findMoves(board, 6, 5))
        self.assertIn([4,6],game.findMoves(board, 6, 6))
        self.assertNotIn([5,6],game.findMoves(board, 6, 7))

        test_board = [[['r', 0], ['n', 0], ['.', 2], ['q', 0], ['k', 0], ['b', 0], ['n', 0], ['r', 0]], [['p', 0], ['p', 0], ['p', 0], ['b', 1], ['p', 0], ['p', 0], ['p', 0], ['p', 0]], [['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2]], [['.', 2], ['.', 2], ['.', 2], ['p', 1], ['.', 2], ['.', 2], ['.', 2], ['.', 2]], [['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2]], [['.', 2], ['p', 1], ['.', 2], ['.', 2], ['.', 2], ['P', 1], ['.', 2], ['.', 2]], [['P', 0], ['.', 2], ['P', 0], ['P', 0], ['P', 0], ['.', 2], ['P', 0], ['P', 0]], [['R', 0], ['N', 0], ['B', 0], ['Q', 0], ['K', 0], ['B', 0], ['N', 0], ['R', 0]]]
        self.assertIn([0,2],game.findMoves(test_board, 0, 3))
        self.assertNotIn([6,1],game.findMoves(test_board, 7, 2))
        self.assertNotIn([6,5],game.findMoves(test_board, 7, 5))

    
    def test_findAttacks(self):
        self.assertIn([1,0],game.findAttacks(board, 0, 0)) #w-left-rook
        self.assertIn([0,1],game.findAttacks(board, 0, 0)) #w-left-rook
        self.assertNotIn([4,0],game.findAttacks(board, 0, 0)) 
        self.assertIn([2,0],game.findAttacks(board, 0, 1)) #w-left-knight
        self.assertIn([2,2],game.findAttacks(board, 0, 1)) #w-left-knight
        self.assertIn([1,3],game.findAttacks(board, 0, 1)) #w-left-knight
        self.assertNotIn([1,1],game.findAttacks(board, 0, 2)) #w-left-bishap
        self.assertNotIn([1,2],game.findAttacks(board, 0, 2)) #w-left-bishap
        self.assertNotIn([1,3], game.findAttacks(board, 0, 2)) #w-left-bishap
        self.assertNotIn([1,2], game.findAttacks(board, 0, 3)) #w-queen
        self.assertIn([1,3], game.findAttacks(board, 0, 3)) #w-queen
        self.assertNotIn([1,4], game.findAttacks(board, 0, 3)) #w-queen
        self.assertIn([0,4], game.findAttacks(board, 0, 3)) #w-queen
        self.assertIn([0,5], game.findAttacks(board, 0, 4)) #w-king
        self.assertIn([1,3], game.findAttacks(board, 0, 4)) #w-king
        self.assertNotIn([1,4], game.findAttacks(board, 0, 5)) #w-right-bishap
        self.assertNotIn([1,6], game.findAttacks(board, 0, 5)) #w-right-bishap
        self.assertNotIn([1,3],game.findAttacks(board, 0, 6)) #w-right-knight
        self.assertIn([1,4],game.findAttacks(board, 0, 6)) #w-right-knight
        self.assertIn([1,7],game.findAttacks(board, 0, 7)) #w-right-rook
        self.assertNotIn([2,0],game.findAttacks(board, 1, 0))
        self.assertNotIn([3,0],game.findAttacks(board, 1, 0))
        self.assertNotIn([2,0],game.findAttacks(board, 1, 1))
        self.assertNotIn([2,1],game.findAttacks(board, 1, 1))
        self.assertNotIn([2,2],game.findAttacks(board, 1, 2))
        self.assertNotIn([3,3],game.findAttacks(board, 1, 3))
        self.assertNotIn([2,2],game.findAttacks(board, 1, 4))
        self.assertNotIn([0,5],game.findAttacks(board, 1, 5))
        self.assertNotIn([3,6],game.findAttacks(board, 1, 6))
        self.assertNotIn([2,6],game.findAttacks(board, 1, 7))


        self.assertIn([6,0],game.findAttacks(board, 7, 0)) #left-rook
        self.assertNotIn([6,1],game.findAttacks(board, 7, 0)) #left-rook
        self.assertIn([5,2],game.findAttacks(board, 7, 1)) #left-knight
        self.assertIn([5,0],game.findAttacks(board, 7, 1)) #left-knight
        self.assertNotIn([6,1],game.findAttacks(board, 7, 2)) #left-bishap
        self.assertNotIn([6,2],game.findAttacks(board, 7, 2)) #left-bishap
        self.assertNotIn([6,3], game.findAttacks(board, 7, 2)) #left-bishap
        self.assertNotIn([6,2], game.findAttacks(board, 7, 3)) #queen
        self.assertIn([6,3], game.findAttacks(board, 7, 3)) #queen
        self.assertNotIn([6,4], game.findAttacks(board, 7, 3)) #queen
        self.assertIn([7,4], game.findAttacks(board, 7, 3)) #queen
        self.assertIn([7,5], game.findAttacks(board, 7, 4)) #king
        self.assertIn([6,3], game.findAttacks(board, 7, 4)) #king
        self.assertNotIn([7,3], game.findAttacks(board, 7, 5)) #right-bishap
        self.assertNotIn([7,6], game.findAttacks(board, 7, 5)) #right-bishap
        self.assertNotIn([7,4], game.findAttacks(board, 7, 5)) #right-bishap
        self.assertNotIn([6,5], game.findAttacks(board, 7, 5)) #right-bishap
        self.assertNotIn([7,6], game.findAttacks(board, 7, 5)) #right-bishap
        self.assertNotIn([7,6], game.findAttacks(board, 7, 5)) #right-bishap
        self.assertNotIn([7,3],game.findAttacks(board, 7, 6)) #right-knight
        self.assertIn([6,4],game.findAttacks(board, 7, 6)) #right-knight
        self.assertIn([5,5],game.findAttacks(board, 7, 6)) #right-knight
        self.assertIn([5,7],game.findAttacks(board, 7, 6)) #right-knight
        self.assertIn([6,7],game.findAttacks(board, 7, 7)) #right-rook
        self.assertNotIn([5,0],game.findAttacks(board, 6, 0))
        self.assertNotIn([4,0],game.findAttacks(board, 6, 0))
        self.assertNotIn([6,1],game.findAttacks(board, 6, 0))
        self.assertIn([5,1],game.findAttacks(board, 6, 0))
        self.assertIn([5,0],game.findAttacks(board, 6, 1))
        self.assertNotIn([5,1],game.findAttacks(board, 6, 1))
        self.assertNotIn([5,2],game.findAttacks(board, 6, 2))
        self.assertNotIn([4,3],game.findAttacks(board, 6, 3))
        self.assertNotIn([5,2],game.findAttacks(board, 6, 4))
        self.assertNotIn([7,5],game.findAttacks(board, 6, 5))
        self.assertNotIn([4,6],game.findAttacks(board, 6, 6))
        self.assertIn([5,6],game.findAttacks(board, 6, 7))
        self.assertNotIn([5,6],game.findAttacks(board, 3, 1))


    def test_friendlyFire(self):
        self.assertNotIn([6,3],game.friendlyFire(board,7, 1, game.findMoves(board, 7, 1)))
        self.assertIn([5,2],game.friendlyFire(board,7, 1, game.findMoves(board, 7, 1)))

    def test_makeMove(self):
        updatedboard = game.makeMove(board, 6, 1, 5, 1)
        self.assertNotEqual(board, updatedboard)
        #print("--")
        #print(updatedboard)
        #print("--")

    def test_moveValidation(self):
        self.assertFalse(game.moveValidation(board, 1, 0, 2, 0, "w"))
        self.assertFalse(game.moveValidation(board, 6, 0, 5, 0, "b"))
        self.assertTrue(game.moveValidation(board, 6, 0, 5, 0, "w"))
        self.assertTrue(game.moveValidation(board, 1, 0, 2, 0, "b"))
        self.assertFalse(game.moveValidation(board, 6, 0, 1, 0, "w"))
    
    def test_isCheck(self):
        self.assertFalse(game.isCheck(board, "w"))
        self.assertFalse(game.isCheck(board, "b"))

        print("====================")
        print(board)
    
    def test_isCheckMate(self):
        final_board = "[[['.', 2], ['.', 2], ['.', 2], ['.', 2], ['k', 0], ['.', 2], ['.', 2], ['.', 2]], [['.', 2], ['.', 2], ['.', 2], ['.', 2], ['P', 1], ['.', 2], ['.', 2], ['.', 2]], [['.', 2], ['.', 2], ['.', 2], ['P', 1], ['K', 1], ['.', 2], ['.', 2], ['.', 2]], [['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2]], [['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2]], [['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2]], [['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2]], [['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2], ['.', 2]]]"
        self.assertFalse(game.isCheckMate(final_board, "b"))
        self.assertFalse(game.isCheckMate(board, "w"))
        self.assertFalse(game.isCheckMate(board, "b"))
    
    def test_pawnPromotion(self):
        copyBoard = copy.deepcopy(board)
        self.assertNotEqual(board, game.pawnPromotion(copyBoard, 1, 1, 'Rook', 'w'))
        self.assertNotEqual(board, game.pawnPromotion(copyBoard, 1, 1, 'Bishop', 'w'))
        self.assertNotEqual(board, game.pawnPromotion(copyBoard, 1, 1, 'Queen', 'w'))
        self.assertNotEqual(board, game.pawnPromotion(copyBoard, 1, 1, 'Knight', 'w'))
        self.assertNotEqual(board, game.pawnPromotion(copyBoard, 7, 7, 'Rook', 'b'))
        self.assertNotEqual(board, game.pawnPromotion(copyBoard, 7, 7, 'Bishop', 'b'))
        self.assertNotEqual(board, game.pawnPromotion(copyBoard, 7, 7, 'Queen', 'b'))
        self.assertNotEqual(board, game.pawnPromotion(copyBoard, 7, 7, 'Knight', 'b'))



if __name__ == '__main__':
    unittest.main()
