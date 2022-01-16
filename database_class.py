from os import name
from select import select
import sqlite3
from sqlite3.dbapi2 import Cursor
import time
import csv
from tkinter.tix import Tree
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
            # print("Επιτυχής σύνδεση στη βάση δεδομένων", filename)
            print("Επιτυχής σύνδεση στη βάση δεδομένων")
            # sqlite_select_Query = "select sqlite_version();"
            # self.cursor.execute(sqlite_select_Query)
            # record = self.cursor.fetchall()
            # for rec in record:
            #     print("SQLite Database Version is: ", rec[0])
            self.cursor.execute("PRAGMA foreign_keys = ON;")
        except sqlite3.Error as error:
            # print("Σφάλμα σύνδεσης στη βάση δεδομένων sqlite", error)
            print("Σφάλμα σύνδεσης στη βάση δεδομένων sqlite")

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

    def is_reader_subscripted(self, id):
        r = self.con.execute(" select Chosen_plan_id from reader where User_id= ?",(id,)).fetchone()
        if dict(r)["Chosen_plan_id"] == None:
            return False
        else :
            return True

    def reader_gets_subscription(self, reader_id, plan_id):
        date_now = date.today().strftime("%Y-%m-%d")
        self.con.execute("update READER set Chosen_plan_id = ?, Chosen_plan_date = ? where User_id=?",(plan_id, date_now, reader_id))
        self.con.commit()

    def get_subscription_expiration_date(self, reader_id):
        r = self.con.execute("select Chosen_plan_id from READER where User_id=?",(reader_id,)).fetchone()
        r = dict(r)["Chosen_plan_id"]
        if r==1:
            duration = 1
        elif r==2:
            duration = 3
        elif r==3:
            duration = 6
        else:
            duration = 12
        r = self.con.execute(f"select date(Chosen_plan_date, '+{duration} month') as Expiration_date from READER  where User_id={reader_id} ").fetchone()
        r = dict(r)["Expiration_date"]
        return r 
    
    def cancel_subscription(self, user_id):
        self.con.execute(f"update READER set Chosen_plan_id=Null where User_id=?",(user_id,))
        self.con.commit()

    def get_all_usernames(self):
        r = self.con.execute("select Username from User")
        d = []
        for i in r:
            d.append(dict(i)["Username"])
        return d

    def print_table(self,table):
        try:
            print(f"/////////{table}/////////")
            query = f'''select * from '{table}' '''
            r = self.con.execute(query).fetchall()
            print(tuple(dict(r[0])))
            for i in r:
                print(tuple(dict(i).values()))
        except:
           print(f"no such table as {table} exists or it is empty")
            

    def user_loggin(self, username, password):
        query = f"select * from USER,READER where Username=? and Password=? and Id=User_id"
        r = self.con.execute(query,(username,password)).fetchall()
        if(len(r)==1):
            d = dict(r[0])
            d['User_type'] = 'reader'  
            return d
        query = "select * from USER,PUBLISHER where Username=? and Password=? and Id=User_id"
        r = self.con.execute(query,(username,password)).fetchall()
        if(len(r)==1):
            d = dict(r[0])
            d['User_type'] = 'publisher'
            del d['User_id']
            return d
        return False

    
    def get_publishers_magazines(self, publisher_id):
        r = self.con.execute("select * from MAGAZINE where Publisher_id=?",(publisher_id,)).fetchall()
        d = []
        for i in r:
            d.append(dict(i))
        return d

    def create_magazine(self, issn, title, publisher_id):
        query = f"insert into MAGAZINE values(?,?,?,?,?,?,?,?)"
        self.con.execute(query,(issn,title,None,None,None,None,None,publisher_id))
        self.con.commit()

    def delete_magazine(self, issn):
        self.con.execute("delete from MAGAZINE where Issn=?",(issn,))
        self.con.commit()

    def get_magazine_rating(self, issn):
        rating = self.con.execute("SELECT avg(Rating) from MAGAZINE, ARTICLE, READER_RATES_ARTICLE where Issn=Mag_issn and Article_doi=Doi and Issn=? group by Issn",(issn,)).fetchone()
        if rating!=None:
            rating = dict(rating)["avg(Rating)"]
        return rating

    def get_all_magazines_issn(self):
        r = self.con.execute("select Issn from MAGAZINE").fetchall()
        d = []
        for i in r:
            d.append(dict(i)["Issn"])
        return d

    def update_magazine_title(self, issn, title):
        self.con.execute("update MAGAZINE set Title=? where Issn=?",(title,issn))
        self.con.commit()

    def get_magazines_subjects(self, mag_issn):
        r = self.con.execute("select Subject_title from SUBJECT_INVOLVES_MAGAZINE where Mag_issn=?",(mag_issn,)).fetchall()
        d = []
        for i in r:
            d.append(tuple(dict(i).values())[0])
        return d
    
    def get_magazine_by_issn(self, issn):
        r = self.con.execute("select * from MAGAZINE where Issn=?",(issn,)).fetchall()
        d = []
        for i in r:
            d.append(dict(i))
        return d

    def add_subject_to_magazine(self, subject, magazine_issn):
            self.con.execute("insert into SUBJECT_INVOLVES_MAGAZINE values(?,?)",(subject, magazine_issn))
            self.con.commit()

    def remove_subject_from_magazine(self, subject, magazine_issn):
            self.con.execute("delete from SUBJECT_INVOLVES_MAGAZINE where Subject_title=? and Mag_issn=?",(subject, magazine_issn))
            self.con.commit()

    def get_all_subjects(self):
        r = self.con .execute("select * from SUBJECT").fetchall()
        d = []
        for i in r:
            d.append(tuple(dict(i).values()))
        return d

    def create_subject(self, Title):
            self.con.execute("insert into SUBJECT values(?)",(Title,))
            self.con.commit()

    def get_magazines_publications(self, mag_issn):
        r = self.con.execute("select * from PUBLICATION where Mag_issn=? ",(mag_issn,)).fetchall()
        d = []
        for i in r:
            d.append(dict(i))
        return d

    def add_publication_to_magazine(self, mag_issn, volume, issue, d=None):
        if d==None:
            today = date.today()
            date_now = today.strftime("%Y-%m-%d")
        else:
            date_now = d
        self.con.execute("insert into PUBLICATION values(?,?,?,?)",(mag_issn,volume,issue,date_now))
        self.con.commit()

    def delete_publication(self, issn, volume, issue):
        self.con.execute("delete from PUBLICATION where Mag_issn=? and Volume=? and Issue=?", (issn, volume, issue))
        self.con.commit()

    def get_publications_articles(self, mag_issn, volume, issue):
        r = self.con.execute("select * from ARTICLE where Mag_issn=? and Pub_volume=? and Pub_issue=?",(mag_issn, volume, issue)).fetchall()
        d = []
        for i in r:
            d.append(dict(i))
        return d
    
    def get_publication_date(self, mag_issn, volume, issue):
        r = self.con.execute("select Publication_date from PUBLICATION where Mag_issn=? and Volume=? and Issue=?",(mag_issn, volume, issue)).fetchone()
        return dict(r)["Publication_date"]

    def get_article(self, doi):
        r = self.con.execute("select * from ARTICLE where Doi = ?",(doi,)).fetchone()
        r = dict(r)
        return r

    def get_article_rating(self,doi):
        r = self.con.execute("select avg(Rating) from ARTICLE,READER_RATES_ARTICLE where Doi=Article_doi and Doi=?",(doi,)).fetchone()
        if r == None:
            return None
        else:
            return dict(r)["avg(Rating)"]

    def get_article_doi(self, title):
        r = self.con.execute("select Doi from ARTICLE where Title = ?",(title,)).fetchone()
        r = tuple(dict(r).values())[0]
        return r

    def get_articles_by_title(self, title):
        r = self.con.execute(f"select * from article where Title like '%{title}%' ").fetchall()
        d = []
        for i in r:
            d.append(dict(i))
        return d
    
    def get_articles_by_title_subject(self, title, subject):
        r = self.con.execute(f"select * from ARTICLE, SUBJECT_INVOLVES_ARTICLE where Article_doi=Doi and Subject_title='{subject}' and Title like '%{title}%' ").fetchall()
        d = []
        for i in r:
            d.append(dict(i))
        return d

    def get_all_articles(self):
        r = self.con.execute("select * from ARTICLE").fetchall()
        d = []
        for i in r:
            d.append(dict(i))
        return d 

    def get_all_articles_doi(self):
        r = self.con.execute("select Doi from ARTICLE").fetchall()
        d = []
        for i in r:
            d.append(dict(i)["Doi"])
        return d 

    def add_article_to_publication(self, doi, title, no_pages, language, is_free, link_to_article, mag_issn, volume, issue, pub_date = None):
        if pub_date==None:
            today = date.today()
            date_now = today.strftime("%Y-%m-%d")
        else:
            date_now = pub_date
        self.con.execute("insert into ARTICLE values(?,?,?,?,?,?,?,?,?,?)",(doi, title, date_now, no_pages, language, is_free, link_to_article, mag_issn, volume, issue))
        self.con.commit()
    
    def add_reader_rating_to_article(self, reader_id, article_doi, rating):
        rating_exists = dict(self.con.execute("select count(1) from READER_RATES_ARTICLE where Reader_id=? and Article_doi=?",(reader_id, article_doi)).fetchone())["count(1)"]
        if rating_exists==0:
            self.con.execute("insert into READER_RATES_ARTICLE values(?,?,?)",(reader_id, article_doi, rating))
            self.con.commit()
        else:
            self.con.execute("update READER_RATES_ARTICLE set Rating=? where Reader_id=? and Article_doi=?",(rating, reader_id, article_doi))
            self.con.commit()

    def get_reader_article_rating(self, reader_id, article_doi):
        rating = self.con.execute("select Rating from READER_RATES_ARTICLE where Reader_id=? and Article_doi=?",(reader_id, article_doi)).fetchone()
        if rating!=None:
            rating=dict(rating)["Rating"]
        return rating


    def does_reader_follows_author(self, reader_id, author_id):
        r = dict(self.con.execute("select count(1) from READER_FOLLOWS_AUTHOR where Reader_id=? and Author_id=?",(reader_id, author_id)).fetchone())["count(1)"]
        if r==0:
            return False
        else:
            return True

    def reader_follow_author(self, reader_id, author_id):
        self.con.execute("insert into READER_FOLLOWS_AUTHOR values(?,?)",(reader_id, author_id))
        self.con.commit()

    def reader_unfollow_author(self, reader_id, author_id):
        self.con.execute("delete from READER_FOLLOWS_AUTHOR where Reader_id=? and Author_id=?",(reader_id, author_id))
        self.con.commit()

    def delete_article(self, doi):
        self.con.execute("delete from ARTICLE where Doi=? ", (doi,))
        self.con.commit()

    def update_article(self, doi, title, url, date, pages, language, is_free):
        self.con.execute("update ARTICLE set Title=?, Link_to_article=?, Publication_date=?, No_pages=?, Language=?, Is_free=? where Doi=?", (title,url,date,pages,language, is_free, doi))
        self.con.commit()
        

    def get_articles_subjects(self, doi):
        r = self.con.execute("select Subject_title from SUBJECT_INVOLVES_ARTICLE where Article_doi = ? ",(doi,))
        d = []
        for i in r:
            d.append(tuple(dict(i).values())[0])
        return d

    def add_subject_to_article(self, subject, doi):
        self.con.execute("insert into SUBJECT_INVOLVES_ARTICLE values(?, ?)",(subject,doi))
        self.con.commit()

    def remove_subject_from_article(self, subject, doi):
        self.con.execute("delete from SUBJECT_INVOLVES_ARTICLE where Subject_title=? and Article_doi=?",(subject, doi))
        self.con.commit()

    def get_articles_authors(self, doi):
        r = self.con.execute("select Id, Fname, Lname, Biography, No_citations, No_publications from AUTHOR_WRITES_ARTICLE, AUTHOR where Article_doi=? and Author_id=Id",(doi,))
        d = []
        for i in r:
            d.append(dict(i))
        return d

    def get_articles_citations(self,doi):
        r = self.con.execute("select Doi, Title from ARTICLE_CITES_ARTICLE,ARTICLE where Cites_doi1 = ? and Doi=Cites_doi2",(doi,)).fetchall()
        d = []
        for i in r:
            d.append(dict(i))
        return d

    def get_citations_to_article(self,doi):
        r = self.con.execute("select Doi, Title from ARTICLE_CITES_ARTICLE,ARTICLE where Cites_doi2 = ? and Doi=Cites_doi1",(doi,)).fetchall()
        d = []
        for i in r:
            d.append(dict(i))
        return d

    def add_citation_to_article(self,doi1, doi2):
        self.con.execute("insert into ARTICLE_CITES_ARTICLE values(?,?)",(doi1, doi2))
        self.con.commit()

    def remove_citation_from_article(self, doi1, doi2):
        self.con.execute("delete from ARTICLE_CITES_ARTICLE where Cites_doi1=? and  Cites_doi2=?",(doi1, doi2))
        self.con.commit()


    def add_author_to_article(self, author_id, article_doi):
        self.con.execute("insert into AUTHOR_WRITES_ARTICLE values(?,?)",(author_id, article_doi))
        self.con.commit()
    
    def remove_author_from_article(self, author_id, article_doi):
        self.con.execute("delete from AUTHOR_WRITES_ARTICLE where Author_id=? and Article_doi=?",(author_id, article_doi))
        self.con.commit()

    def get_all_authors(self):
        r = self.con.execute("select * from AUTHOR").fetchall()
        d = []
        for i in r:
            d.append(dict(i))
        return d

    def create_author(self, fname, lname, biography):
        id = len(self.con.execute("select * from AUTHOR").fetchall())
        self.con.execute("insert into AUTHOR values(?,?,?,?,?,?)",(id, fname, lname, biography, 0, 1))
        self.con.commit()

    def get_author_id(self, fname, lname):
        r = self.con.execute("select Id from AUTHOR where Fname=? and Lname=?",(fname,lname)).fetchone()
        if r != None:
            return tuple(dict(r).values())[0]
        return None

    def get_publications_editors(self, mag_issn, volume, issue):
        r = self.con.execute("select Id, Fname, Lname from EDITOR, EDITOR_EDITS_PUBLICATION where Editor_id=Id and Mag_issn=? and Pub_volume=? and Pub_issue=?",(mag_issn,volume,issue)).fetchall()
        d = []
        for i in r:
            d.append(dict(i))
        return d

    def add_editors_to_publication(self, id, issn, volume, issue):
        self.con.execute("insert into EDITOR_EDITS_PUBLICATION values(?,?,?,?)",(id,issn,volume,issue))
        self.con.commit()
    
    def update_pulication_date(self, issn, volume, issue, date):
        self.con.execute("update PUBLICATION set Publication_date = ? where Mag_issn = ? and Volume = ? and Issue = ?",(date, issn, volume, issue))
        self.con.commit()

    def remove_editor_from_publication(self, id, issn, volume, issue):
        self.con.execute("delete from EDITOR_EDITS_PUBLICATION where Editor_id=? and Mag_issn=? and Pub_volume=? and Pub_issue=?",(id,issn,volume,issue))
        self.con.commit()

    def get_magazines_editors(self, mag_issn):
        r = self.con.execute("select Id, Fname, Lname, Start_date from EDITOR, EDITOR_WORKS_FOR_MAGAZINE where Editor_id=Id and Mag_issn=?",(mag_issn,))
        d = []
        for i in r:
            d.append(dict(i))
        return d
    
    def get_magazines_by_title(self, title):
        r = self.con.execute(f"select * from MAGAZINE where Title like '%{title}%' ").fetchall()
        d = []
        for i in r:
            d.append(dict(i))
        return d

    def get_magazines_by_title_subject(self, title, subject):
        r = self.con.execute(f"select * from MAGAZINE, SUBJECT_INVOLVES_MAGAZINE where Mag_issn=Issn and Subject_title='{subject}' and Title like '%{title}%' ").fetchall()
        d = []
        for i in r:
            d.append(dict(i))
        return d

    def add_editor_to_magazine(self, editor_id, mag_issn):
        today = date.today()
        date_now = today.strftime("%Y-%m-%d")
        self.con.execute("insert into EDITOR_WORKS_FOR_MAGAZINE values(?,?,?)",(editor_id, mag_issn, date_now))
        self.con.commit()

    def remove_editor_from_magazine(self, id, issn):
        self.con.execute("delete from EDITOR_WORKS_FOR_MAGAZINE where Editor_id=? and mag_Issn=?",(id, issn))
        self.con.commit()

    def get_all_editors(self):
        r = self.con.execute("select * from EDITOR")
        d = []
        for i in r:
            d.append(dict(i))
        return d

    def get_editor_id(self, fname, lname):
        r = self.con.execute("select Id from EDITOR where Fname=? and Lname=?",(fname,lname)).fetchone()
        if r != None:
            return tuple(dict(r).values())[0]
        return None

    def create_editor(self, fname, lname):
        number_of_editors = len(self.con.execute(f"select * from EDITOR").fetchall())
        self.con.execute("insert into EDITOR values(?,?,?)",(number_of_editors,fname,lname))
        self.con.commit()

        
    