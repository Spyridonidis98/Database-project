from database_class import DataModel

db = DataModel("db_project.db")

user = db.user_loggin("ieee","1234")
if(user!=False):
    if(user['User_type']=='publisher'):
        print(user)
        mags = db.get_publishers_magazines(user['Id'])
        print(mags)
        mag_subs = db.get_magazines_subjects(mags[0]["Issn"])
        print(mag_subs)
        pubs = db.get_magazines_publications(mags[0]["Issn"])
        print(pubs)
        articles = db.get_publications_articles(pubs[0]['Mag_issn'], pubs[0]['Volume'], pubs[0]['Issue'])
        print(articles)
        art_subs = db.get_articles_subjects(articles[0]["Doi"])
        print(art_subs)
        art_authors = db.get_articles_authors(articles[0]["Doi"])
        print(art_authors)
        pubs_editors = db.get_publications_editors(pubs[0]['Mag_issn'], pubs[0]['Volume'], pubs[0]['Issue'])
        print(pubs_editors)
        mags_editors = db.get_magazines_editors(mags[0]["Issn"])
        print(mags_editors)


    else:
        #to do later 
        print("user is a reader")
else:
    print("the user doesn't exist")
    
db.close()