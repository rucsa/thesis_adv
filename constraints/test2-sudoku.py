from constraint import *
import math

def solveSudoku(size = 9, originalGame = None):
    """ Solving Sudoku of any size """
    sudoku = Problem()

    #Defining size of row/col
    rows = range(size)
    cols = range(size)

    #Creating board
    board = [(row, col) for row in rows for col in cols]
    #Defining game variable, a single range will be enough
    sudoku.addVariables(board, range(1, size * size + 1))

    #Row set
    rowSet = [zip([el] * len(cols), cols) for el in rows]
    colSet = [zip(rows, [el] * len(rows)) for el in cols]

    sudoku.addConstraint( InSetConstraint( range(1, size+1) ) )

    #The original board is not empty, we add that constraint to the list of constraint
    if originalGame is not None:
        for i in range(0, size):
            for j in range(0, size):
                #Getting the value of the current game
                o = originalGame[i][j]
                #We apply constraint when the number is set only
                if o > 0:
                    #We get the associated tuple
                    t = (rows[i],cols[j])
                    #We set a basic equal constraint rule to force the system to keep that variable at that place
                    sudoku.addConstraint(lambda var, val=o: var == val, (t,))

    #The constraint are like that : and each row, and each columns, got same final compute value

    for row in rowSet:
        sudoku.addConstraint(AllDifferentConstraint(), row)
    for col in colSet:
        sudoku.addConstraint(AllDifferentConstraint(), col)

    #Every sqrt(size) (3x3 box constraint) got same sum
    sqSize = int(math.floor(math.sqrt(size)))

    #xrange allow to define a step, here sq (wich is sq = 3 in 9x9 sudoku)
    for i in range(0,size,sqSize):
        for j in range(0,size,sqSize):
            #Computing the list of tuple linked to that box
            box = []
            for k in range(0, sqSize):
                for l in range(0, sqSize):
                    #The tuple i+k, j+l is inside that box
                    box.append( (i+k, j+l) )
            #Compute is done, now we can add the constraint for that box
            sudoku.addConstraint(AllDifferentConstraint(), box)

    #Computing and returning final result
    # return sudoku.getSolutions()
    return sudoku.getSolution()


if __name__ == '__main__':
    rg = 9
    #World hardest sudoku
    initValue = [[0, 0, 5, 3, 0, 0, 0, 0, 0],
                 [8, 0, 0, 0, 0, 0, 0, 2, 0],
                 [0, 7, 0, 0, 1, 0, 5, 0, 0],
                 [4, 0, 0, 0, 0, 5, 3, 0, 0],
                 [0, 1, 0, 0, 7, 0, 0, 0, 6],
                 [0, 0, 3, 2, 0, 0, 0, 8, 0],
                 [0, 6, 0, 5, 0, 0, 0, 0, 9],
                 [0, 0, 4, 0, 0, 0, 0, 3, 0],
                 [0, 0, 0, 0, 0, 9, 7, 0, 0]]
    # initValue = [[0, 9, 0, 7, 0, 0, 8, 6, 0],
    # [0, 3, 1, 0, 0, 5, 0, 2, 0],
    # [8, 0, 6, 0, 0, 0, 0, 0, 0],
    # [0, 0, 7, 0, 5, 0, 0, 0, 6],
    # [0, 0, 0, 3, 0, 7, 0, 0, 0],
    # [5, 0, 0, 0, 1, 0, 7, 0, 0],
    # [0, 0, 0, 0, 0, 0, 1, 0, 9],
    # [0, 2, 0, 6, 0, 0, 0, 5, 0],
    # [0, 5, 4, 0, 0, 8, 0, 7, 0]]

    res = solveSudoku(rg, initValue)
    print
    if res is not None:
        # for r in res:
        # for i in range(0, rg):
        # for j in range(0, rg):
        # print r[i, j],
        # print
        # print
        for i in range(0, rg):
            for j in range(0, rg):
                print (res[i, j]),
            print
        print
    else:
        print ("No result to show")