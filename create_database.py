import sqlite3

conn = sqlite3.connect('db_project.db')

conn.execute('''CREATE TABLE MAGAZINE_FORMER_TITLE 
                (Mag_issn TEXT,
                 Former_title TEXT,
                 PRIMARY KEY(Mag_issn, Former_title),
                 FOREIGN KEY(Mag_issn) REFERENCES MAGAZINE(Issn)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.execute('''CREATE TABLE MAGAZINE
                (Issn TEXT,
                 Title TEXT,
                 Impact_factor REAL,
                 Eigen_factor REAL,
                 Article_influence_score REAL,
                 Cite_score REAL,
                 User_rating REAL, 
                 Publisher_id INTEGER,
                 PRIMARY KEY(Issn),
                 FOREIGN KEY(Publisher_id) REFERENCES PUBLISHER(User_id)
                  ON UPDATE CASCADE ON DELETE SET NULL);''') # if a publisher were to delete their account, their published magazines would remain in the datebase

conn.execute('''CREATE TABLE EDITOR_WORKS_FOR_MAGAZINE 
                (Editor_id INTEGER, 
                 Mag_issn TEXT,
                 Start_date TEXT,
                 PRIMARY KEY(Editor_id, Mag_issn)
                 FOREIGN KEY(Editor_id) REFERENCES EDITOR(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Mag_issn) REFERENCES MAGAZINE(Issn)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.execute('''CREATE TABLE EDITOR 
                (Id INTEGER,
                 Fname TEXT,
                 Lname TEXT,
                 PRIMARY KEY(Id));''')

conn.execute('''CREATE TABLE EDITOR_EDITS_PUBLICATION
                (Editor_id INTEGER,
                 Mag_issn TEXT,
                 Pub_volume INTEGER,
                 Pub_issue INTEGER,
                 PRIMARY KEY(Editor_id, Mag_issn, Pub_volume, Pub_issue) 
                 FOREIGN KEY(Editor_id) REFERENCES EDITOR(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Mag_issn) REFERENCES PUBLICATION(Mag_issn)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Pub_volume) REFERENCES PUBLICATION(Volume)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Pub_issue) REFERENCES PUBLICATION(Issue)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.execute('''CREATE TABLE PUBLISHER
                (User_id INTEGER,
                 PRIMARY KEY(User_id)
                 FOREIGN KEY(User_id) REFERENCES USER(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.execute('''CREATE TABLE SUBJECT_INVOLVES_MAGAZINE
                (Subject_title TEXT,
                 Mag_issn TEXT,
                 PRIMARY KEY(Subject_title, Mag_issn),
                 FOREIGN KEY(Subject_title) REFERENCES SUBJECT(Title)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Mag_issn) REFERENCES MAGAZINE(Issn)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.execute('''CREATE TABLE SUBJECT
                (Title TEXT,
                 PRIMARY KEY(Title) );''')

conn.execute('''CREATE TABLE SUBJECT_INVOLVES_ARTICLE
                (Subject_title TEXT,
                 Article_doi TEXT,
                 PRIMARY KEY(Subject_title, Article_doi),
                 FOREIGN KEY(Subject_title) REFERENCES SUBJECT(Title)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Article_doi) REFERENCES ARTICLE(Doi)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.execute('''CREATE TABLE PUBLICATION
                (Mag_issn TEXT,
                 Volume INTEGER,
                 Issue INTEGER,
                 PRIMARY KEY(Mag_issn, Volume, Issue),
                 FOREIGN KEY(Mag_issn) REFERENCES MAGAZINE(Issn)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.execute('''CREATE TABLE USER
                (Id INTEGER,
                 Username TEXT,
                 Password TEXT,
                 Email_address TEXT, 
                 Display_name TEXT,
                 PRIMARY KEY(Id));''')

conn.execute('''CREATE TABLE SUBSCRIPTION_PLAN_ALLOWS_ACCESS_TO_MAGAZINE
                (Plan_id INTEGER, 
                 Mag_issn INTEGER,
                 PRIMARY KEY(Plan_id, Mag_issn),
                 FOREIGN KEY(Plan_id) REFERENCES SUBSCRIPTION_PLAN(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Mag_issn) REFERENCES MAGAZINE(Issn)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.execute('''CREATE TABLE SUBSCRIPTION_PLAN
                (Id INTEGER,
                 Value REAL,
                 Duration_months INTEGER,
                 PRIMARY KEY(Id));''')

conn.execute('''CREATE TABLE PAYMENT
                (Plan_id INTEGER,
                 Payment_id INTEGER,
                 Price REAL, 
                 Expiration_date TEXT,
                 Date_sent TEXT,
                 Reader_id INTEGER,
                 Date_payed TEXT,
                 PRIMARY KEY(Plan_id, Payment_id),
                 FOREIGN KEY(Plan_id) REFERENCES SUBSCRIPTION_PLAN(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Reader_id) REFERENCES READER(User_id)
                  ON UPDATE CASCADE ON DELETE SET NULL);''') # keep payment history after a user deletes their account

conn.execute('''CREATE TABLE ARTICLE 
                (Doi TEXT,
                 Title TEXT,
                 Publication_date TEXT,
                 No_pages INTEGER,
                 Language TEXT,
                 Is_free INTEGER,
                 Link_to_article TEXT,
                 Mag_issn TEXT,
                 Pub_volume INTEGER,
                 Pub_issue INTEGER,
                 PRIMARY KEY(Doi),
                 FOREIGN KEY(Mag_issn) REFERENCES PUBLICATION(Mag_issn)
                  ON UPDATE CASCADE ON DELETE SET NULL,
                 FOREIGN KEY(Pub_volume) REFERENCES PUBLICATION(Volume)
                  ON UPDATE CASCADE ON DELETE SET NULL,
                 FOREIGN KEY(Pub_issue) REFERENCES PUBLICATION(Issue)
                  ON UPDATE CASCADE ON DELETE SET NULL);''') # articles are kept even after the magazine they were published on gets deleted

conn.execute('''CREATE TABLE ARTICLE_AFFILIATION
                (Art_doi TEXT,
                 Affiliation TEXT,
                 PRIMARY KEY(Art_doi, Affiliation),
                 FOREIGN KEY(Art_doi) REFERENCES ARTICLE(Doi)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.execute('''CREATE TABLE READER
                (User_id INTEGER,
                 Chosen_plan_id INTEGER,
                 Chosen_plan_date TEXT,
                 Cancels_plan_id INTEGER,
                 Cancels_plan_date INTEGER,
                 PRIMARY KEY(User_id)
                 FOREIGN KEY(User_id) REFERENCES USER(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.execute('''CREATE TABLE READER_ACCESSES_ARTICLE 
                (Reader_id INTEGER,
                 Article_doi TEXT,
                 PRIMARY KEY(Reader_id,Article_doi),
                 FOREIGN KEY(Reader_id) REFERENCES READER(User_id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Article_doi) REFERENCES ARTICLE(Doi)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.execute('''CREATE TABLE AUTHOR_WRITES_ARTICLE
                (Author_id INTEGER,
                 Article_doi INTEGER,
                 PRIMARY KEY(Author_id,Article_doi),
                 FOREIGN KEY(Author_id) REFERENCES AUTHOR(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Article_doi) REFERENCES ARTICLE(Doi)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.execute('''CREATE TABLE READER_RATES_ARTICLE
                (Reader_id INTEGER,
                 Article_doi TEXT,
                 PRIMARY KEY(Reader_id, Article_doi),
                 FOREIGN KEY(Reader_id) REFERENCES READER(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Article_doi) REFERENCES ARTICLE(Doi)
                  ON UPDATE CASCADE ON DELETE CASCADE);''') # rating is NOT stored for deleted users (to account for e.g., banned bot accounts)

conn.execute('''CREATE TABLE ARTICLE_CITES_ARTICLE
                (Cites_doi1 INTEGER,
                 Cites_doi2 INTEGER,
                 PRIMARY KEY(Cites_doi1, Cites_doi2),
                 FOREIGN KEY(Cites_doi1) REFERENCES ARTICLE(Doi)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Cites_doi2) REFERENCES ARTICLE(Doi)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.execute('''CREATE TABLE AUTHOR_PUBLICATION_TOPICS
                (Author_id INTEGER,
                 Publication_topics INTEGER,
                 PRIMARY KEY(Author_id, Publication_topics),
                 FOREIGN KEY(Author_id) REFERENCES AUTHOR(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Publication_topics) REFERENCES SUBJECT(Title)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.execute('''CREATE TABLE READER_FOLLOWS_AUTHOR
                (Reader_id INTEGER,
                 Author_id INTEGER,
                 PRIMARY KEY(Reader_id, Author_id),
                 FOREIGN KEY(Reader_id) REFERENCES READER(User_id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Author_id) REFERENCES AUTHOR(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.execute('''CREATE TABLE AUTHOR_AFFILIATION
                (Author_id INTEGER,
                 Affiliation INTEGER,
                 PRIMARY KEY(Author_id, Affiliation),
                 FOREIGN KEY(Author_id) REFERENCES AUTHOR(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Affiliation) REFERENCES AUTHOR(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.execute('''CREATE TABLE AUTHOR
                (Id INTEGER,
                 Fname TEXT,
                 Lname TEXT,
                 Biography TEXT,
                 No_citations INTEGER,
                 No_publications INTEGER,
                 PRIMARY KEY(Id));''')

conn.execute('''CREATE TABLE AUTHOR_HAS_BEEN_COAUTHORS_WITH_AUTHOR
                (Author_id1 INTEGER,
                 Author_id2 INTEGER,
                 PRIMARY KEY(Author_id1, Author_id2),
                 FOREIGN KEY(Author_id1) REFERENCES AUTHOR(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Author_id2) REFERENCES AUTHOR(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')

conn.close()