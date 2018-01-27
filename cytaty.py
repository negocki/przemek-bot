import random
import sqlite3

class Cytaty:
    def __init__(self,conn):
        self.conn = conn
        self.curs = self.conn.cursor()
        print("Cytaty gotowe")

    def dodaj_cytat(self,login,text):

        self.curs.execute("INSERT INTO cytaty(login,cytat,data) VALUES (? , ? , CURRENT_TIMESTAMP )",(str(login),str(text)))
        self.conn.commit()

        print("Dodano cytat do bazy: ",login,text)

    def cytat(self,numer):

        wynik = None
        self.curs.execute("SELECT * FROM cytaty WHERE id = ?",(numer,))
        wynik = self.curs.fetchone()
        if wynik == None:
            print("Nie znaleziono cytatu ",numer)
            return (0,0,0)
        else:

            hasz = wynik[1].find("#")
            cytat_author = wynik[1][:hasz]
            print("Wysylam cytat ", numer)
            return (cytat_author,wynik[2],wynik[3])


    def losuj_cytat(self):
        wynik = None
        self.curs.execute("SELECT COUNT(*) FROM cytaty")
        row = self.curs.fetchone()
        cytat_count = int(row[0])

        while(wynik == None):
            print("Losuje id cytatu do ",cytat_count)
            rand_id = random.randint(1,cytat_count)
            print("Wylosowano cytat ",rand_id)
            self.curs.execute("SELECT * FROM cytaty WHERE id = ?", (rand_id,))
            wynik = self.curs.fetchone()
            hasz = wynik[1].find("#")
            cytat_author = wynik[1][:hasz]
            return (cytat_author,wynik[2],wynik[3])

        print()
