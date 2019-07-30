import wfdb
from helpers import *
from multiprocessing import Pool, cpu_count
from pprint import pprint as pp

# The record id's
# Each record is a 30 minute recording of a patient.
recIds = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119, 121, 122, 123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219, 220, 221, 222, 223, 228, 230, 231, 232, 233, 234]

# Not sure what these symbols are
symbolsIgnore = '+~"'

# These symbols are beat annotations.
symbolsToNotIgnore="NLRBAaJSVrFejE/fQ?"


def main():
    # Where to output the csv
    outFile = input("Enter name of output file:")
    
    # We are going to vectorize the operation
    # First, we go through the records and note down
    # the positions of the various annotations.
    # For example, if N (Normal Beat) was found at 
    # 450 in record 100, we push (100,450,N) to
    # queries
    queries = []
    for recId in recIds:
        a  = wfdb.rdann("data/"+str(recId),"atr")
        for sym,samp in zip(a.symbol,a.sample):
            query = (recId,samp,sym)
            if sym in symbolsToNotIgnore:
            	queries.append(query)
                
    # Initialize the multiprocessing queue.
    # Doing this sped up the process more than
    # 15 times on my 16 threads computer.
    pool = Pool( cpu_count() )
    
    # We map getVoltages over the queries.
    signalss = pool.starmap( getVoltages, queries)
    pool.close()
    pool.join()
    
    # We have to unflatten the list and remove the
    # failed getVoltages, failed getVoltages return None
    # Unflattening Example: [[[1,2,3,"A"]],[[4,5,6,"N"]],[[7,8,9,"B"]]]
    # to [[1,2,3,"A"],[4,5,6,"N"],[7,8,9,"B"]]
    signals = []
    for signals_ in signalss:
        if signals_ is not None:
            signals += signals_
            
            
    print("\n{} signals found.".format(len(signals)))
    
    
    # Now we must convert the list to a string of csv.
    # Example: [1,2,3] to "1,2,3"
    strings = list(map( signalListToString , signals ))
    
    # When we are dealing with a massive number of strings,
    # It's better to merge the string and write it at once
    # instead of 1000's of file write operations.
    print("Merging the strings")
    stringToWrite="\n".join(strings)
    
    
    # Write to provided output file.
    print("Writing to file.")
    f = open(outFile,"w+")
    f.write(stringToWrite)
    f.close()


if __name__ == "__main__":
    main()
