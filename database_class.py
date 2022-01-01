from os import name
import sqlite3
from sqlite3.dbapi2 import Cursor
import time
import csv
import numpy as np
from datetime import date 

class DataModel():
    '''Κλάση  σύνδεσης με τη βάση δεδομένων και δημιουργίας δρομέα'''
    def __init__(self, filename):
        self.filename = filename
        try:
            self.con = sqlite3.connect(filename)
            self.con.row_factory = sqlite3.Row  # ώστε να πάρουμε τα ονόματα των στηλών του πίνακα
            self.cursor = self.con.cursor()
            print("Επιτυχής σύνδεση στη βάση δεδομένων", filename)
            sqlite_select_Query = "select sqlite_version();"
            self.cursor.execute(sqlite_select_Query)
            record = self.cursor.fetchall()
            for rec in record:
                print("SQLite Database Version is: ", rec[0])
        except sqlite3.Error as error:
            print("Σφάλμα σύνδεσης στη βάση δεδομένων sqlite", error)

    def close(self):
        self.con.commit()
        self.con.close()

    def create_user(self,username, password, email, display_name, is_publisher):
        num_of_users = len(self.cursor.execute("select * from USER").fetchall())
        query = f'''insert into USER values ("{num_of_users}","{username}","{password}","{email}","{display_name}")'''
        self.con.execute(query)
        if(is_publisher):
            query = f'''insert into PUBLISHER values({num_of_users})'''
            self.con.execute(query)

        else:
            query = f'''insert into READER values({num_of_users},{'Null'},{'Null'},{'Null'},{'Null'})'''
            self.con.execute(query)
        self.con.commit()

    def print_table(self,table):
        try:
            print(f"/////////{table}/////////")
            query = f"select * from {table}"
            r = self.con.execute(query).fetchall()
            print(tuple(dict(r[0])))
            for i in r:
                print(tuple(dict(i).values()))
        except:
            print(f"no such table as {table} exists or it is empty")

    def user_loggin(self, username, password):
        query = f"select * from USER,READER where Username='{username}' and Password='{password}' and Id=User_id"
        r = self.con.execute(query).fetchall()
        if(len(r)==1):
            d = dict(r[0])
            d['User_type'] = 'reader'  
            return d
        query = f"select * from USER,PUBLISHER where Username='{username}' and Password='{password}' and Id=User_id"
        r = self.con.execute(query).fetchall()
        if(len(r)==1):
            d = dict(r[0])
            d['User_type'] = 'publisher'
            del d['User_id']
            return d
        return False

    
    def get_publishers_magazines(self, publisher_id):
        r = self.con.execute(f"select * from MAGAZINE where Publisher_id='{publisher_id}'").fetchall()
        d = []
        for i in r:
            d.append(dict(i))
        return d

    def create_magazine(self, issn, title, publisher_id):
        query = f"insert into MAGAZINE values('{issn}','{title}', {'Null'}, {'Null'}, {'Null'}, {'Null'}, {'Null'}, {publisher_id})"
        self.con.execute(query)
        self.con.commit()

    def get_magazines_subjects(self, mag_issn):
        r = self.con.execute(f"select Subject_title from SUBJECT_INVOLVES_MAGAZINE where Mag_issn='{mag_issn}'").fetchall()
        d = []
        for i in r:
            d.append(tuple(dict(i).values())[0])
        return d
    
    def add_subject_to_magazine(self, subject, magazine_issn):
            self.con.execute(f"insert into SUBJECT_INVOLVES_MAGAZINE values('{subject}', '{magazine_issn}')")
            self.con.commit()

    def get_subjects(self):
        r = self.con .execute(f"select * from SUBJECT").fetchall()
        d = []
        for i in r:
            d.append(tuple(dict(i).values()))
        return d

    def create_subject(self, Title):
            self.con.execute(f"insert into SUBJECT values('{Title}')")
            self.con.commit()

    def get_magazines_publications(self, mag_issn):
        r = self.con.execute(f"select * from PUBLICATION where Mag_issn='{mag_issn}' ").fetchall()
        d = []
        for i in r:
            d.append(dict(i))
        return d

    def add_publication_to_magazine(self, mag_issn, volume, issue):
        self.con.execute(f"insert into PUBLICATION values('{mag_issn}',{volume},{issue})")
        self.con.commit()

    def get_publications_articles(self, mag_issn, volume, issue):
        r = self.con.execute(f"select * from ARTICLE where Mag_issn='{mag_issn}' and Pub_volume={volume} and Pub_issue={issue} ")
        d = []
        for i in r:
            d.append(dict(i))
        return d
    
    def add_article_to_publication(self, doi, title, no_pages, language, is_free, link_to_article, mag_issn, volume, issue):
        today = date.today()
        date_now = today.strftime("%d/%m/%Y")
        self.con.execute(f"insert into ARTICLE values('{doi}', '{title}', '{date_now}', {no_pages}, '{language}', {is_free}, '{link_to_article}', '{mag_issn}',{volume},{issue})")
        self.con.commit()

    def get_articles_subjects(self, doi):
        r = self.con.execute(f"select Subject_title from SUBJECT_INVOLVES_ARTICLE where Article_doi = '{doi}' ")
        d = []
        for i in r:
            d.append(tuple(dict(i).values())[0])
        return d

    def add_subject_to_article(self, subject, doi):
        self.con.execute(f"insert into SUBJECT_INVOLVES_ARTICLE values('{subject}', '{doi}')")
        self.con.commit()

    def get_articles_authors(self, doi):
        r = self.con.execute(f"select Id, Fname, Lname, Biography, No_citations, No_publications from AUTHOR_WRITES_ARTICLE, AUTHOR where Article_doi='{doi}' and Author_id=Id")
        d = []
        for i in r:
            d.append(dict(i))
        return d

    def add_author_to_article(self, author_id, article_doi):
        self.con.execute(f"insert into AUTHOR_WRITES_ARTICLE values({author_id},'{article_doi}') ")
        self.con.commit()
    
    def get_authors(self):
        r = self.con.execute(f"select * from AUTHOR")
        d = []
        for i in r:
            d.append(tuple(dict(i).values()))
        return d

    def create_author(self, fname, lname, biography):
        id = len(self.con.execute(f"select * from AUTHOR").fetchall())
        self.con.execute(f"insert into AUTHOR values({id}, '{fname}', '{lname}', '{biography}', {0}, {0})")
        self.con.commit()

    def get_publications_editors(self, mag_issn, volume, issue):
        r = self.con.execute(f"select Id, Fname, Lname from EDITOR, EDITOR_EDITS_PUBLICATION where Editor_id=Id and Mag_issn='{mag_issn}' and Pub_volume={volume} and Pub_issue={issue}").fetchall()
        d = []
        for i in r:
            d.append(dict(i))
        return d

    def add_editors_to_publication(self, id, issn, volume, issue):
        self.con.execute(f"insert into EDITOR_EDITS_PUBLICATION values({id}, '{issn}', {volume}, {issue})")
        self.con.commit()


    def get_magazines_editors(self, mag_issn):
        r = self.con.execute(f"select Id, Fname, Lname, Start_date from EDITOR, EDITOR_WORKS_FOR_MAGAZINE where Editor_id=Id and Mag_issn='{mag_issn}'")
        d = []
        for i in r:
            d.append(dict(i))
        return d
    
    def add_editor_to_magazine(self, editor_id, mag_issn):
        today = date.today()
        date_now = today.strftime("%d/%m/%Y")
        self.con.execute(f"insert into EDITOR_WORKS_FOR_MAGAZINE values('{editor_id}', '{mag_issn}', '{today}')")
        self.con.commit()

    def get_all_editors(self):
        r = self.con.execute(f"select * from EDITOR")
        d = []
        for i in r:
            d.append(tuple(dict(i).values()))
        return d

    def create_editor(self, fname, lname):
        number_of_editors = len(self.con.execute(f"select * from EDITOR").fetchall())
        self.con.execute(f"insert into EDITOR values({number_of_editors}, '{fname}', '{lname}')")
        self.con.commit()
    