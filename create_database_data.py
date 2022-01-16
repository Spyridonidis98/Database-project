from database_class import DataModel
import create_database

db = DataModel("db_project.db")

###create users publishers=True readers=False
db.create_user("ieee","1234","info@ieee.org","ieee",True)
db.create_user("oxford press","1234","oxford@oxford.edu","oxford press",True)
db.create_user("peter","1234","peter@gmail.com","peter",False)
db.create_user("jim","1234","jim@gmail.com","jim",False)

##create magazines 
db.create_magazine("1111-1111","Antennas and Propagation Magazine", 0)
db.create_magazine("1111-1112", "Electronics Magazine", 0)

db.create_subject("electronics")
db.create_subject("antennas")
db.create_subject("math")

db.add_subject_to_magazine("electronics","1111-1111")
db.add_subject_to_magazine("antennas","1111-1111")
db.add_subject_to_magazine("electronics","1111-1112")

db.add_publication_to_magazine("1111-1111",1,1)
db.add_publication_to_magazine("1111-1111",1,2)
db.add_publication_to_magazine("1111-1112",1,1)

db.add_article_to_publication("1.1","an article about antennas", 22 ,"english", 0, "link", "1111-1111", 1, 1)
db.add_article_to_publication("1.2","an article about antennas and electronics", 22, "english", 1, "link", "1111-1111", 1, 2)
db.add_article_to_publication("1.3", "an article about electronics", 30, "english", 0,"link", "1111-1112", 1 , 1)

db.add_subject_to_article("electronics", "1.1")
db.add_subject_to_article("antennas", "1.2")
db.add_subject_to_article("electronics", "1.2")
db.add_subject_to_article("electronics", "1.3")

db.add_citation_to_article("1.2","1.1")#1.2 cites or references 1.1

db.create_author("Michaela", "Crouch", " ")
db.create_author("Humphrey", "Rye", " ")
db.create_author("Brian", "Atkinson", " ")

db.add_author_to_article(0, "1.1")
db.add_author_to_article(1, "1.2")
db.add_author_to_article(2, "1.2")
db.add_author_to_article(2, "1.3")

db.create_editor("Cory", "Jameson")
db.create_editor(" Mitchell", "Waller")

db.add_editor_to_magazine(0, "1111-1111")
db.add_editor_to_magazine(1, "1111-1112")

db.add_editors_to_publication(0, "1111-1111",1,1)
db.add_editors_to_publication(0, "1111-1111",1,2)
db.add_editors_to_publication(1, "1111-1112",1,1)
