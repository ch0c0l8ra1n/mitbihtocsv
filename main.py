import wfdb
from helpers import *
from multiprocessing import Pool, cpu_count

recIds = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119, 121, 122, 123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219, 220, 221, 222, 223, 228, 230, 231, 232, 233, 234]

symbolsIgnore = '+~"'

rsas = {}

def main():
    outFile = input("Enter name of output file:")
    queries = []
    for recId in recIds:
        a  = wfdb.rdann("data/"+str(recId),"atr")
        for sym,samp in zip(a.symbol,a.sample):
            query = (recId,samp,sym)
            queries.append(query)

    pool = Pool( cpu_count() )
    signalss = pool.starmap( getVoltages, queries)
    pool.close()
    pool.join()

    signals = []
    for signals_ in signalss:
        if signals_ is not None:
            signals += signals_
    
    print("\n{} signals found.".format(len(signals)))

    print("Converting list to string")
    pool = Pool( cpu_count() )
    strings = pool.map( signalListToString , signals )
    pool.close()
    pool.join()

    print("Merging the strings")
    stringToWrite="\n".join(strings)
        
    print("Writing to file.")
    f = open(outFile,"w+")
    f.write(stringToWrite)
    f.close()


if __name__ == "__main__":
    main()
