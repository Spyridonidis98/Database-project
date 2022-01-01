from database_class import DataModel

db = DataModel("db_project.db")

###create users publishers=True readers=False
db.create_user("ieee","1234","ieee@gmail.com","ieee",True)
db.create_user("oxford press","1234","oxford@gmail.com","oxford press",True)
db.create_user("peter","1234","peter@gmail.com","peter",False)
db.create_user("jim","1234","jim@gmail.com","jim",False)

##create magazines 
db.create_magazine("1111-1111","Antenas and Propagation Magazine", 0)
db.create_magazine("1111-1112", "Electronics and stuff", 0)

db.create_subject("electronics")
db.create_subject("antenas")

db.add_subject_to_magazine("electronics","1111-1111")
db.add_subject_to_magazine("antenas","1111-1111")
db.add_subject_to_magazine("electronics","1111-1112")

db.add_publication_to_magazine("1111-1111",1,1)
db.add_publication_to_magazine("1111-1111",1,2)
db.add_publication_to_magazine("1111-1112",1,1)

db.add_article_to_publication("1.1","an article about antenas", 22 ,"english", 0, "link", "1111-1111", 1, 1)
db.add_article_to_publication("1.2","an article about antenas and electronics", 22, "english", 1, "link", "1111-1111", 1, 2)
db.add_article_to_publication("1.3", "an article about electronics", 30, "english", 0,"link", "1111-1112", 1 , 1)

db.add_subject_to_article("electronics", "1.1")
db.add_subject_to_article("antenas", "1.2")
db.add_subject_to_article("electronics", "1.2")
db.add_subject_to_article("electronics", "1.3")

db.create_author("john", "cena", "a buff dude")
db.create_author("john", "wick", "some one killed his dog and he is out for revenge")
db.create_author("peter", "parker", "he was bitten by a radion active spider and now he can climb walls")

db.add_author_to_article(0, "1.1")
db.add_author_to_article(1, "1.2")
db.add_author_to_article(2, "1.2")
db.add_author_to_article(2, "1.3")

db.create_editor("patric", "star")
db.create_editor("ronnie", "colman")

db.add_editor_to_magazine(0, "1111-1111")
db.add_editor_to_magazine(1, "1111-1112")

db.add_editors_to_publication(0, "1111-1111",1,1)
db.add_editors_to_publication(1, "1111-1112",1,1)

