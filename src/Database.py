import os.path
import pickle as pickle
from src.RecordTable import RecordTable
from src.Challenge import Challenge

class Database:
    def __init__(self):
    
        self.__SAVE_PATH = "save_state.pkl"
    
        self.record_tables = []
        
        if os.path.exists(self.__SAVE_PATH):
            print("loading saved state...", end="")
            with open(self.__SAVE_PATH, 'rb') as inp:
                self.record_tables = pickle.load(inp)
            print("done")
    
    @property
    def tables(self):
        return self.record_tables
    
    def add_table(self, challenge: Challenge, max_record_holders: int = 3):
        record_table = RecordTable(challenge, max_record_holders)
        if record_table in self.record_tables:
            print("Challenge already exists")
            return
        self.record_tables.append(record_table)
        self.__save()
        
    def remove_table(self, challenge: Challenge):
        rt = RecordTable(challenge)
        for table in self.record_tables:
            if (table == rt):
                self.record_tables.remove(table)
                break
        self.__save()
    
    def __save(self):
        print("saving state...", end="")
        with open(self.__SAVE_PATH, 'wb') as outp:
            pickle.dump(self.record_tables, outp, pickle.HIGHEST_PROTOCOL)
        print("done")