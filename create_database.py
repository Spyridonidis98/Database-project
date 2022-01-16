import sqlite3


conn = sqlite3.connect('db_project.db')

conn.execute('''CREATE TABLE IF NOT EXISTS MAGAZINE_FORMER_TITLE 
                (Mag_issn TEXT,
                 Former_title TEXT,
                 PRIMARY KEY(Mag_issn, Former_title),
                 FOREIGN KEY(Mag_issn) REFERENCES MAGAZINE(Issn)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')
print('Table "MAGAZINE_FORMER_TITLE": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS MAGAZINE
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
print('Table "MAGAZINE": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS EDITOR_WORKS_FOR_MAGAZINE 
                (Editor_id INTEGER, 
                 Mag_issn TEXT,
                 Start_date TEXT,
                 PRIMARY KEY(Editor_id, Mag_issn)
                 FOREIGN KEY(Editor_id) REFERENCES EDITOR(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Mag_issn) REFERENCES MAGAZINE(Issn)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')
print('Table "EDITOR_WORKS_FOR_MAGAZINE": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS EDITOR 
                (Id INTEGER,
                 Fname TEXT,
                 Lname TEXT,
                 PRIMARY KEY(Id));''')
print('Table "EDITOR": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS EDITOR_EDITS_PUBLICATION
                (Editor_id INTEGER,
                 Mag_issn TEXT,
                 Pub_volume INTEGER,
                 Pub_issue INTEGER,
                 PRIMARY KEY(Editor_id, Mag_issn, Pub_volume, Pub_issue) 
                 FOREIGN KEY(Editor_id) REFERENCES EDITOR(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Mag_issn, Pub_volume, Pub_issue) REFERENCES PUBLICATION(Mag_issn, Volume, Issue)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')
print('Table "EDITOR_EDITS_PUBLICATION": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS PUBLISHER
                (User_id INTEGER,
                 PRIMARY KEY(User_id)
                 FOREIGN KEY(User_id) REFERENCES USER(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')
print('Table "PUBLISHER": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS SUBJECT_INVOLVES_MAGAZINE
                (Subject_title TEXT,
                 Mag_issn TEXT,
                 PRIMARY KEY(Subject_title, Mag_issn),
                 FOREIGN KEY(Subject_title) REFERENCES SUBJECT(Title)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Mag_issn) REFERENCES MAGAZINE(Issn)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')
print('Table "SUBJECT_INVOLVES_MAGAZINE": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS SUBJECT
                (Title TEXT,
                 PRIMARY KEY(Title) );''')
print('Table "SUBJECT": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS SUBJECT_INVOLVES_ARTICLE
                (Subject_title TEXT,
                 Article_doi TEXT,
                 PRIMARY KEY(Subject_title, Article_doi),
                 FOREIGN KEY(Subject_title) REFERENCES SUBJECT(Title)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Article_doi) REFERENCES ARTICLE(Doi)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')
print('Table "SUBJECT_INVOLVES_ARTICLE": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS PUBLICATION
                (Mag_issn TEXT,
                 Volume INTEGER,
                 Issue INTEGER,
                 Publication_date TEXT,
                 PRIMARY KEY(Mag_issn, Volume, Issue),
                 FOREIGN KEY(Mag_issn) REFERENCES MAGAZINE(Issn)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')
print('Table "PUBLICATION": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS USER
                (Id INTEGER,
                 Username TEXT UNIQUE,
                 Password TEXT,
                 Email_address TEXT UNIQUE,
                 Display_name TEXT,
                 PRIMARY KEY(Id));''')
print('Table "USER": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS SUBSCRIPTION_PLAN_ALLOWS_ACCESS_TO_MAGAZINE
                (Plan_id INTEGER, 
                 Mag_issn INTEGER,
                 PRIMARY KEY(Plan_id, Mag_issn),
                 FOREIGN KEY(Plan_id) REFERENCES SUBSCRIPTION_PLAN(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Mag_issn) REFERENCES MAGAZINE(Issn)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')
print('Table "SUBSCRIPTION_PLAN_ALLOWS_ACCESS_TO_MAGAZINE": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS SUBSCRIPTION_PLAN
                (Id INTEGER,
                 Value REAL,
                 Duration_months INTEGER,
                 PRIMARY KEY(Id));''')
print('Table "SUBSCRIPTION_PLAN": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS PAYMENT
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
print('Table "PAYMENT": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS ARTICLE 
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
                 FOREIGN KEY(Mag_issn, Pub_volume, Pub_issue) REFERENCES PUBLICATION(Mag_issn, Volume, Issue)
                  ON UPDATE CASCADE ON DELETE SET NULL);''') # articles are kept even after the magazine they were published on gets deleted
print('Table "ARTICLE": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS READER
                (User_id INTEGER,
                 Chosen_plan_id INTEGER,
                 Chosen_plan_date TEXT,
                 Cancels_plan_id INTEGER,
                 Cancels_plan_date INTEGER,
                 PRIMARY KEY(User_id)
                 FOREIGN KEY(User_id) REFERENCES USER(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')
print('Table "READER": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS READER_ACCESSES_ARTICLE 
                (Reader_id INTEGER,
                 Article_doi TEXT,
                 PRIMARY KEY(Reader_id,Article_doi),
                 FOREIGN KEY(Reader_id) REFERENCES READER(User_id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Article_doi) REFERENCES ARTICLE(Doi)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')
print('Table "READER_ACCESSES_ARTICLE": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS AUTHOR_WRITES_ARTICLE
                (Author_id INTEGER,
                 Article_doi INTEGER,
                 PRIMARY KEY(Author_id,Article_doi),
                 FOREIGN KEY(Author_id) REFERENCES AUTHOR(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Article_doi) REFERENCES ARTICLE(Doi)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')
print('Table "AUTHOR_WRITES_ARTICLE": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS READER_RATES_ARTICLE
                (Reader_id INTEGER,
                 Article_doi TEXT,
                 Rating INTEGER,
                 PRIMARY KEY(Reader_id, Article_doi),
                 FOREIGN KEY(Reader_id) REFERENCES READER(User_id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Article_doi) REFERENCES ARTICLE(Doi)
                  ON UPDATE CASCADE ON DELETE CASCADE);''') # rating is NOT stored for deleted users (to account for e.g., banned bot accounts)
print('Table "READER_RATES_ARTICLE": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS ARTICLE_CITES_ARTICLE
                (Cites_doi1 INTEGER,
                 Cites_doi2 INTEGER,
                 PRIMARY KEY(Cites_doi1, Cites_doi2),
                 FOREIGN KEY(Cites_doi1) REFERENCES ARTICLE(Doi)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Cites_doi2) REFERENCES ARTICLE(Doi)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')
print('Table "ARTICLE_CITES_ARTICLE": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS READER_FOLLOWS_AUTHOR
                (Reader_id INTEGER,
                 Author_id INTEGER,
                 PRIMARY KEY(Reader_id, Author_id),
                 FOREIGN KEY(Reader_id) REFERENCES READER(User_id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY(Author_id) REFERENCES AUTHOR(Id)
                  ON UPDATE CASCADE ON DELETE CASCADE);''')
print('Table "READER_FOLLOWS_AUTHOR": ok')

conn.execute('''CREATE TABLE IF NOT EXISTS AUTHOR
                (Id INTEGER,
                 Fname TEXT,
                 Lname TEXT,
                 Biography TEXT,
                 No_citations INTEGER,
                 No_publications INTEGER,
                 PRIMARY KEY(Id));''')
print('Table "AUTHOR": ok')

conn.execute('''CREATE INDEX IF NOT EXISTS MAGAZINE_PUBLISHER_ID
                ON MAGAZINE(Publisher_id);''')
print('Index "MAGAZINE_PUBLISHER_ID": ok')

print('All tables and indices were created successfully, closing connection...')
conn.close()
print('Success!')