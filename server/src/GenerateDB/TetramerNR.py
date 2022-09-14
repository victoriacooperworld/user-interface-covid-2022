import DatabaseInit


if __name__ == '__main__':
    db = DatabaseInit.databaseInit()
    # inputDir = r'D:\OutputFiles\TetramerID\Merged\Merged\Merged'
    inputDir = r'E:\Vic\TetramerID\Merged'
    db.insertTetramer(inputDir)