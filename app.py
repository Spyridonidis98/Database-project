import os
import tkinter as tk
from tkinter import Message, ttk
from tkinter.constants import NONE
import webbrowser
from database_class import DataModel


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Journal Explorer")
        self.root.geometry("800x800+100+100") # make 800x800 pixel window, 100 pixels from each side of the screen
        self.root.minsize(1232, 800)
        self.root.maxsize(1232, 800)
        self.root.tk.call("source", os.path.join("Azure-ttk-theme", "azure.tcl"))
        self.root.tk.call("set_theme", "light")

        self.validateInteger = (self.root.register(self.valInteger), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.validateIssn = (self.root.register(self.valIssn), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.validateEmail = (self.root.register(self.valEmail), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.validateDoi = (self.root.register(self.valDoi), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.validateMonth = (self.root.register(self.valMonth), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.validateDay = (self.root.register(self.valDay), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        if not os.path.exists('db_project.db'):
            print('Please run "create_database.py" first!')
            exit()

        self.db = DataModel("db_project.db")

        self.showLoginScreen()

    # === Login/Register ===
    def showLoginScreen(self):
        self.mainLoginFrame = ttk.Frame(self.root)
        self.mainLoginFrame.pack(fill = "both", expand = True)

        self.loginTitle = ttk.Label(self.mainLoginFrame, text = "Please login to use the app.", font = ("Arial", 20))
        self.loginTitle.pack(anchor = "s", expand = True, pady = 30, padx = 20)

        self.loginInfoFrame = ttk.Frame(self.mainLoginFrame)
        self.loginInfoFrame.pack(anchor = "n", expand = True)

        self.usernameLabel = ttk.Label(self.loginInfoFrame, text = "Username:")
        self.usernameLabel.grid(row = 0, column = 0, sticky="e", pady = 2)

        self.usernameEntry = ttk.Entry(self.loginInfoFrame)
        self.usernameEntry.grid(row = 0, column = 1, pady = 2)

        self.passwordLabel = ttk.Label(self.loginInfoFrame, text = "Password:")
        self.passwordLabel.grid(row = 1, column = 0, sticky="e", pady = 2)

        self.passwordEntry = ttk.Entry(self.loginInfoFrame, show="\u2022") # \u2022 is the bullet symbol: "•"
        self.passwordEntry.grid(row = 1, column = 1, pady = 2)

        self.errorLabel = ttk.Label(self.loginInfoFrame)
        self.errorLabel.grid(row = 2, column = 0, columnspan = 2)

        self.loginButton = ttk.Button(self.loginInfoFrame, text = "Login", command = self.submitLoginInfo)
        self.loginButton.grid(row = 3, column = 0, columnspan = 2, pady = (0, 10))

        self.registerLabel = tk.Label(self.loginInfoFrame, text = "No account? Register!", fg = "dodger blue", font = ("Arial", 10, "underline"))
        self.registerLabel.grid(row = 4, column = 0, columnspan = 2)
        self.registerLabel.bind("<1>", lambda e: self.loginToRegister())

        self.root.bind("<Return>", lambda event: self.submitLoginInfo())

    def destroyLoginScreen(self):
        self.mainLoginFrame.destroy()
        self.root.unbind("<Return>")

    def showRegisterScreen(self):
        self.mainRegisterFrame = ttk.Frame(self.root)
        self.mainRegisterFrame.pack(fill = "both", expand = True)

        self.registerTitle = ttk.Label(self.mainRegisterFrame, text = "Please input the following information:", font = ("Arial", 20))
        self.registerTitle.pack(anchor = "s", expand = True, pady = 30, padx = 20)

        self.registerInfoFrame = ttk.Frame(self.mainRegisterFrame)
        self.registerInfoFrame.pack(anchor = "n", expand = True)

        self.usernameLabel = ttk.Label(self.registerInfoFrame, text = "Username:")
        self.usernameLabel.grid(row = 0, column = 0, sticky="e", pady = 2)

        self.usernameEntry = ttk.Entry(self.registerInfoFrame)
        self.usernameEntry.grid(row = 0, column = 1, pady = 2)

        self.displaynameLabel = ttk.Label(self.registerInfoFrame, text = "Display Name:")
        self.displaynameLabel.grid(row = 1, column = 0, sticky="e", pady = 2)

        self.displaynameEntry = ttk.Entry(self.registerInfoFrame)
        self.displaynameEntry.grid(row = 1, column = 1, pady = 2)

        self.emailLabel = ttk.Label(self.registerInfoFrame, text = "Email:")
        self.emailLabel.grid(row = 2, column = 0, sticky="e", pady = 2)

        self.emailEntry = ttk.Entry(self.registerInfoFrame, validate = 'key', validatecommand = self.validateEmail)
        self.emailEntry.grid(row = 2, column = 1, pady = 2)

        self.passwordLabel = ttk.Label(self.registerInfoFrame, text = "Password:")
        self.passwordLabel.grid(row = 3, column = 0, sticky="e", pady = 2)

        self.passwordEntry = ttk.Entry(self.registerInfoFrame, show="\u2022")
        self.passwordEntry.grid(row = 3, column = 1, pady = 2)

        self.userType = tk.StringVar(self.root, "Reader")

        self.typeReaderRadio = ttk.Radiobutton(self.registerInfoFrame, text = "Reader", variable = self.userType, value = "Reader")
        self.typeReaderRadio.grid(row = 4, column = 1, sticky = "w")

        self.typeArticleRadio = ttk.Radiobutton(self.registerInfoFrame, text = "Publisher", variable = self.userType, value = "Publisher")
        self.typeArticleRadio.grid(row = 5, column = 1, sticky = "w")

        self.errorLabel = ttk.Label(self.registerInfoFrame)
        self.errorLabel.grid(row = 6, column = 0, columnspan = 2)

        self.registerButton = ttk.Button(self.registerInfoFrame, text = "Register", command = self.submitRegisterInfo)
        self.registerButton.grid(row = 7, column = 0, columnspan = 2, pady = (0, 0))

        self.errorLabel2 = ttk.Label(self.registerInfoFrame)
        self.errorLabel2.grid(row = 8, column = 0, columnspan = 2)

    def destroyRegisterScreen(self):
        self.mainRegisterFrame.destroy()

    def loginToRegister(self):
        self.destroyLoginScreen()
        self.showRegisterScreen()

    def submitLoginInfo(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        self.user = self.db.user_loggin(username, password)
        
        if self.user == False:
            self.errorLabel.config(text = "Wrong username/password!")

        elif self.user["User_type"]=="reader":
            self.displayname = self.user["Display_name"]
            self.destroyLoginScreen()
            self.showReaderWindow()
            
        else:
            self.displayname = self.user["Display_name"]
            self.destroyLoginScreen()
            self.showPublisherWindow()

    def submitRegisterInfo(self):
        username = self.usernameEntry.get()
        displayname = self.displaynameEntry.get()
        email = self.emailEntry.get()
        password = self.passwordEntry.get()
        usertype = self.userType.get()

        all_usernames = self.db.get_all_usernames()
        if username in all_usernames:
            self.errorLabel2["text"] = "username exists"
            return
        if username=="" or displayname=="" or email=="" or password=="":
            self.errorLabel2["text"] = "all fields must be included"
            return

        usertype = True if usertype == "Publisher" else False # temporary
        self.db.create_user(username, password, email, displayname, usertype)

        self.destroyRegisterScreen()
        self.showLoginScreen()
        self.errorLabel["text"] = "account created"

    # === Reader ===
    # --- Windows ---
    def showReaderWindow(self):
        self.mainReaderWindowFrame = ttk.Frame(self.root)
        self.mainReaderWindowFrame.pack(fill = "both", expand = True)

        self.topBarFrame = ttk.Frame(self.mainReaderWindowFrame)
        self.topBarFrame.pack(fill = "x", expand = False, anchor = "n")
        self.topBarFrame.grid_columnconfigure(2, weight = 1)

        self.backLabel = ttk.Label(self.topBarFrame, text = "\u25c1", font = ("Arial", 30))
        self.backLabel.grid(row = 0, column = 0, padx = 10)

        self.actionTitle = ttk.Label(self.topBarFrame, text = "Search", font = ("Arial", 16))
        self.actionTitle.grid(row = 0, column = 1, padx = 40)

        self.displayNameLabel = ttk.Label(self.topBarFrame, text = self.displayname, font = ("Arial", 20))
        self.displayNameLabel.grid(row = 0, column = 3, sticky = "e", padx = 10)

        self.topBarSeparator = ttk.Separator(self.topBarFrame)
        self.topBarSeparator.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = "ew", columnspan = 4)

        self.showSearch()

    def destroyReaderWindow(self):
        self.mainReaderWindowFrame.destroy()

    def showSearch(self):
        self.backLabel.config(text = "\u25c1")
        self.backLabel.unbind("<1>")
        self.actionTitle.config(text = "Search")

        self.subscriptionLabel = tk.Label(self.topBarFrame, text = "Manage Subscriptions", font = ("Arial", 12, "underline"), fg = "dodger blue")
        self.subscriptionLabel.grid(row = 0, column = 2)
        self.subscriptionLabel.bind("<1>", lambda e: self.searchToSubscriptions())

        self.searchScrollbar = ttk.Scrollbar(self.mainReaderWindowFrame)
        self.searchScrollbar.pack(side="right", fill="y", pady = 2)

        self.searchCanvas = tk.Canvas(self.mainReaderWindowFrame, yscrollcommand = self.searchScrollbar.set, highlightthickness = 0)
        self.searchCanvas.pack(fill = "both", expand = True)
        self.searchScrollbar.config(command = lambda *args: self.yview(self.searchCanvas, *args))

        self.searchFrame = ttk.Frame(self.searchCanvas)
        self.searchCanvas.create_window((0, 0), window = self.searchFrame, anchor = "nw")
        self.searchFrame.bind("<Configure>", lambda e: self.searchCanvas.configure(scrollregion = self.searchCanvas.bbox("all")))

        self.searchBarFrame = ttk.Frame(self.searchFrame)
        self.searchBarFrame.pack(fill = "x", side = "top")

        self.searchBarFrame.grid_columnconfigure(3, minsize = 100)      

        self.searchBarEntry = ttk.Entry(self.searchBarFrame, width = 156)
        self.searchBarEntry.grid(row = 0, column = 0, padx = 5, columnspan = 4)

        self.searchBarButton = ttk.Button(self.searchBarFrame, text = "Search", command = lambda: self.showSearchResults(self.type.get()))
        self.searchBarButton.grid(row = 0, column = 4, padx = 5, pady = 5)

        self.type = tk.StringVar(self.root, "Magazine")

        self.typeMagazineRadio = ttk.Radiobutton(self.searchBarFrame, text = "Magazine", variable = self.type, value = "Magazine")
        self.typeMagazineRadio.grid(row = 1, column = 0, sticky = "e")

        self.typeArticleRadio = ttk.Radiobutton(self.searchBarFrame, text = "Article", variable = self.type, value = "Article")
        self.typeArticleRadio.grid(row = 1, column = 1, sticky = "w")

        self.searchBarSubjectLabel = ttk.Label(self.searchBarFrame, text = "Subject:")
        self.searchBarSubjectLabel.grid(row = 1, column = 2, sticky = "e")

        self.searchBarSubject = tk.StringVar(self.root, "Any")

        self.all_subjects = self.db.get_all_subjects()

        self.all_subjects = ["", "Any"] + self.all_subjects

        self.searchBarSubjectEntry = ttk.OptionMenu(self.searchBarFrame, self.searchBarSubject, *self.all_subjects)
        self.searchBarSubjectEntry.grid(row = 1, column = 3, sticky = "w", pady = (0, 5))

        self.searchResultsFrame = ttk.Frame(self.searchFrame)
        self.searchResultsFrame.pack(fill = "both", expand = True)

    def destroySearch(self):
        self.subscriptionLabel.destroy()
        self.searchCanvas.destroy()
        self.searchScrollbar.destroy()

    def showSearchResults(self, type):
        self.searchResultsFrame.destroy()
        self.searchResultsFrame = ttk.Frame(self.searchFrame)
        self.searchResultsFrame.pack(fill = "both", expand = True)
        
        results = []
        subjectSelected = self.searchBarSubject.get().replace("'","").replace("(","").replace(")","").replace(",","")

        if type == "Magazine":
            if subjectSelected == "Any":
                mags = self.db.get_magazines_by_title(self.searchBarEntry.get())
                for m in mags:
                    results.append((m["Issn"], m["Title"], self.db.get_magazine_rating(m["Issn"])))
            else:
                mags = self.db.get_magazines_by_title_subject(self.searchBarEntry.get(), subjectSelected)
                for m in mags:
                    results.append((m["Issn"], m["Title"], self.db.get_magazine_rating(m["Issn"])))
        else:
            if subjectSelected == "Any":
                articles = self.db.get_articles_by_title(self.searchBarEntry.get())
                for a in articles:
                    results.append((a["Doi"], a["Title"], self.db.get_article_rating(a["Doi"])))
            else:
                articles = self.db.get_articles_by_title_subject(self.searchBarEntry.get(), subjectSelected)
                for a in articles:
                    results.append((a["Doi"], a["Title"], self.db.get_article_rating(a["Doi"])))

        self.resultFrames = []
        self.resultTitleLabels = []
        self.resultRatingLabels = []
        for r in results:
            self.resultFrames.append(tk.Frame(self.searchResultsFrame, bg = "gray85"))
            self.resultFrames[-1].pack(fill = "x", pady = 2, padx = (2, 0))
            self.resultTitleLabels.append(tk.Label(self.resultFrames[-1], text = r[1], bg = "gray85", font = ("Arial", 14)))
            self.resultTitleLabels[-1].pack()
            self.resultRatingLabels.append(tk.Label(self.resultFrames[-1], text = "Rating: {:.2f}".format(r[2]) if r[2]!=None else "Rating: {}".format(r[2]), bg = "gray85"))
            self.resultRatingLabels[-1].pack()
            self.resultTitleLabels[-1].bind("<1>", lambda e, rid=r[0]: self.showResult(rid, type))
            self.resultRatingLabels[-1].bind("<1>", lambda e, rid=r[0]: self.showResult(rid, type))
            self.resultFrames[-1].bind("<1>", lambda e, rid=r[0]: self.showResult(rid, type))

    def showMagazine(self, issn):
        self.backLabel.config(text = "\u25c0")
        self.backLabel.unbind("<1>")
        self.backLabel.bind("<1>", lambda e: self.magazineToSearch())

        self.magazineScrollbar = ttk.Scrollbar(self.mainReaderWindowFrame)
        self.magazineScrollbar.pack(side="right", fill="y", pady = 2)

        self.magazineCanvas = tk.Canvas(self.mainReaderWindowFrame, yscrollcommand = self.magazineScrollbar.set, highlightthickness = 0)
        self.magazineCanvas.pack(fill = "both", expand = True)
        self.magazineScrollbar.config(command = lambda *args: self.yview(self.magazineCanvas, *args))

        self.magazineFrame = ttk.Frame(self.magazineCanvas)
        self.magazineCanvas.create_window((0, 0), window = self.magazineFrame, anchor = "nw")
        self.magazineFrame.bind("<Configure>", lambda e: self.magazineCanvas.configure(scrollregion = self.magazineCanvas.bbox("all")))

        self.magazineInfoFrame = ttk.Frame(self.magazineFrame)
        self.magazineInfoFrame.pack(fill = "x", expand = False)

        self.magazineTitleLabel = ttk.Label(self.magazineInfoFrame, text = "Title:")
        self.magazineTitleLabel.grid(row = 0, column = 0, sticky = "e")

        self.magazineTitleEntry = ttk.Label(self.magazineInfoFrame)
        self.magazineTitleEntry.grid(row = 0, column = 1, sticky = "w")

        self.magazineISSNLabel = ttk.Label(self.magazineInfoFrame, text = "ISSN:")
        self.magazineISSNLabel.grid(row = 1, column = 0, sticky = "e")

        self.magazineISSNEntry = ttk.Label(self.magazineInfoFrame)
        self.magazineISSNEntry.grid(row = 1, column = 1, sticky = "w")

        self.magazineSubjectLabel = ttk.Label(self.magazineInfoFrame, text = "Subject:")
        self.magazineSubjectLabel.grid(row = 2, column = 0, sticky = "e")

        self.magazineSubjectEntries = []

        self.magazineSubjectEntries.append(ttk.Label(self.magazineInfoFrame))
        self.magazineSubjectEntries[0].grid(row = 2, column = 1, sticky = "w")

        self.magazineEditorLabel = ttk.Label(self.magazineInfoFrame, text = "Editor:")
        self.magazineEditorLabel.grid(row = 3, column = 0, sticky = "e")

        self.magazineEditorEntries = []

        self.magazineEditorEntries.append(ttk.Label(self.magazineInfoFrame))
        self.magazineEditorEntries[0].grid(row = 3, column = 1, sticky = "w")

        self.magazineScoresFrame = ttk.Frame(self.magazineFrame)
        self.magazineScoresFrame.pack(fill = "x")

        self.magazineRatingLabel = ttk.Label(self.magazineScoresFrame, text = "User Rating:", font = ("Arial", 16))
        self.magazineRatingLabel.grid(row = 0, column = 0, padx = 20)

        self.magazineRatingNumberLabel = ttk.Label(self.magazineScoresFrame, text = "", font = ("Arial", 14))
        self.magazineRatingNumberLabel.grid(row = 0, column = 1)

        self.magazineLabelFrame = ttk.Frame(self.magazineFrame)
        self.magazineLabelFrame.pack(fill = "x", expand = False)

        self.magazinePublicationsLabel = ttk.Label(self.magazineLabelFrame, text = "Publications:", font = ("Arial", 20))
        self.magazinePublicationsLabel.grid(row = 0, column = 0, sticky = "w", padx = (5, 1025))

        self.publicationsButtonsFrame = ttk.Frame(self.magazineFrame)
        self.publicationsButtonsFrame.pack(fill = "x", expand = False)


        self.actionTitle.config(text = issn)

        magazine = self.db.get_magazine_by_issn(issn)[0]
        title = magazine["Title"]
        subjects = self.db.get_magazines_subjects(issn)
        editors = [ ed["Fname"]+" "+ed["Lname"] for ed in self.db.get_magazines_editors(issn)]
        impact_factor = 1.594
        eigenfactor = 0.0014
        ais = 0.462
        citescore = 3.7
        rating = self.db.get_magazine_rating(issn)

        publications = [(f'{pub["Volume"]},{pub["Issue"]}',) for pub in self.db.get_magazines_publications(issn)]
        

        self.magazineTitleEntry.config(text = title)

        self.magazineISSNEntry.config(text = issn)

        self.magazineSubjectEntries[0].config(text = subjects[0])
        for s in subjects[1:]:
            self.magazineAddSubject()
            self.magazineSubjectEntries[-1].config(text = s)

        self.magazineEditorEntries[0].config(text = editors[0])
        for e in editors[1:]:
            self.magazineAddEditor()
            self.magazineEditorEntries[-1].config(text = e)

        self.magazineRatingNumberLabel.config(text = "{:.1f}".format(rating) if rating!=None else  "{}".format(rating))

        self.publicationButtons = []
        for i, p in enumerate(publications):
            publicationButton = tk.Button(self.publicationsButtonsFrame, text = p[0], height = 3, width = 40, wraplength = 250, relief = "groove", bd = 5, bg = self.stringToColor(p[0]), command = lambda key=p[0]: self.magazineToPublication(key))
            publicationButton.grid(row = i // 4, column = i % 4, padx = 5, pady = 3)
            self.publicationButtons.append(publicationButton)

    def destroyMagazine(self):
        self.magazineCanvas.destroy()
        self.magazineScrollbar.destroy()

    def showPublication(self, issn, key):
        self.backLabel.config(text = "\u25c0")
        self.backLabel.unbind("<1>")
        self.backLabel.bind("<1>", lambda e: self.publicationToMagazine(issn))

        self.publicationScrollbar = ttk.Scrollbar(self.mainReaderWindowFrame)
        self.publicationScrollbar.pack(side="right", fill="y", pady = 2)

        self.publicationCanvas = tk.Canvas(self.mainReaderWindowFrame, yscrollcommand = self.publicationScrollbar.set, highlightthickness = 0)
        self.publicationCanvas.pack(fill = "both", expand = True)
        self.publicationScrollbar.config(command = lambda *args: self.yview(self.publicationCanvas, *args))

        self.publicationFrame = ttk.Frame(self.publicationCanvas)
        self.publicationCanvas.create_window((0, 0), window = self.publicationFrame, anchor = "nw")
        self.publicationFrame.bind("<Configure>", lambda e: self.publicationCanvas.configure(scrollregion = self.publicationCanvas.bbox("all")))

        self.publicationInfoFrame = ttk.Frame(self.publicationFrame)
        self.publicationInfoFrame.pack(fill = "x", expand = False)

        self.publicationVolumeLabel = ttk.Label(self.publicationInfoFrame, text = "Volume:")
        self.publicationVolumeLabel.grid(row = 0, column = 0, sticky = "e")

        self.publicationVolumeEntry = ttk.Label(self.publicationInfoFrame)
        self.publicationVolumeEntry.grid(row = 0, column = 1, sticky = "w")

        self.publicationIssueLabel = ttk.Label(self.publicationInfoFrame, text = "Issue:")
        self.publicationIssueLabel.grid(row = 1, column = 0, sticky = "e")

        self.publicationIssueEntry = ttk.Label(self.publicationInfoFrame)
        self.publicationIssueEntry.grid(row = 1, column = 1, sticky = "w")

        self.publicationYearLabel = ttk.Label(self.publicationInfoFrame, text = "Publication Year:")
        self.publicationYearLabel.grid(row = 2, column = 0, sticky = "e")

        self.publicationYearEntry = ttk.Label(self.publicationInfoFrame)
        self.publicationYearEntry.grid(row = 2, column = 1, sticky = "w")

        self.publicationMonthLabel = ttk.Label(self.publicationInfoFrame, text = "Publication Month:")
        self.publicationMonthLabel.grid(row = 3, column = 0, sticky = "e")

        self.publicationMonthEntry = ttk.Label(self.publicationInfoFrame)
        self.publicationMonthEntry.grid(row = 3, column = 1, sticky = "w")

        self.publicationEditorLabel = ttk.Label(self.publicationInfoFrame, text = "Editor:")
        self.publicationEditorLabel.grid(row = 4, column = 0, sticky = "e")

        self.publicationEditorEntries = []

        self.publicationEditorEntries.append(ttk.Label(self.publicationInfoFrame))
        self.publicationEditorEntries[0].grid(row = 4, column = 1, sticky = "w")

        self.publicationLabelFrame = ttk.Frame(self.publicationFrame)
        self.publicationLabelFrame.pack(fill = "x", expand = False)

        self.publicationArticlesLabel = ttk.Label(self.publicationLabelFrame, text = "Articles:", font = ("Arial", 20))
        self.publicationArticlesLabel.grid(row = 0, column = 0, sticky = "w", padx = (5, 1080))

        self.articlesButtonsFrame = ttk.Frame(self.publicationFrame)
        self.articlesButtonsFrame.pack(fill = "x", expand = False)

        
        self.actionTitle.config(text = key)

        date =  self.db.get_publication_date(issn, key.split(",")[0], key.split(",")[1])
        year = date.split("-")[0]
        month = date.split("-")[1]
        
        editors =  [f'{ed["Fname"]} {ed["Lname"]}' for ed in self.db.get_publications_editors(issn, key.split(",")[0], key.split(",")[1])]

        articles = [ (art["Doi"],art["Title"]) for art in self.db.get_publications_articles(issn, key.split(",")[0], key.split(",")[1])]

        self.publicationVolumeEntry.config(text = key.split(",")[0])
        self.publicationIssueEntry.config(text = key.split(",")[1])

        self.publicationYearEntry.config(text = year)

        self.publicationMonthEntry.config(text = month)

        self.publicationEditorEntries[0].config(text = editors[0])
        for e in editors[1:]:
            self.publicationAddEditor()
            self.publicationEditorEntries[-1].config(text = e)

        self.articleButtons = []
        for i, a in enumerate(articles):
            articleButton = tk.Button(self.articlesButtonsFrame, text = a[1], height = 3, width = 40, wraplength = 250, relief = "groove", bd = 5, bg = self.stringToColor(a[0]), command = lambda doi=a[0]: self.publicationToArticle(issn, doi))
            articleButton.grid(row = i // 4, column = i % 4, padx = 5, pady = 3)
            self.articleButtons.append(articleButton)

    def destroyPublication(self):
        self.publicationCanvas.destroy()
        self.publicationScrollbar.destroy()

    def showArticle(self, doi, issn = "", key = ""):
        self.backLabel.config(text = "\u25c0")
        self.backLabel.unbind("<1>")
        if issn:
            self.backLabel.bind("<1>", lambda e: self.articleToPublication(issn, key))
        else:
            self.backLabel.bind("<1>", lambda e: self.articleToSearch())

        self.articleScrollbar = ttk.Scrollbar(self.mainReaderWindowFrame)
        self.articleScrollbar.pack(side="right", fill="y", pady = 2)

        self.articleCanvas = tk.Canvas(self.mainReaderWindowFrame, yscrollcommand = self.articleScrollbar.set, highlightthickness = 0)
        self.articleCanvas.pack(fill = "both", expand = True)
        self.articleScrollbar.config(command = lambda *args: self.yview(self.articleCanvas, *args))

        self.articleFrame = ttk.Frame(self.articleCanvas)
        self.articleCanvas.create_window((0, 0), window = self.articleFrame, anchor = "nw")
        self.articleFrame.bind("<Configure>", lambda e: self.articleCanvas.configure(scrollregion = self.articleCanvas.bbox("all")))

        self.articleInfoFrame = ttk.Frame(self.articleFrame)
        self.articleInfoFrame.pack(side = "left", expand = False)

        self.articleDOILabel = ttk.Label(self.articleInfoFrame, text = "DOI:")
        self.articleDOILabel.grid(row = 0, column = 0, sticky = "e")

        self.articleDOIEntry = ttk.Label(self.articleInfoFrame)
        self.articleDOIEntry.grid(row = 0, column = 1, sticky = "w")

        self.articleTitleLabel = ttk.Label(self.articleInfoFrame, text = "Title:")
        self.articleTitleLabel.grid(row = 1, column = 0, sticky = "e")

        self.articleTitleEntry = ttk.Label(self.articleInfoFrame)
        self.articleTitleEntry.grid(row = 1, column = 1, sticky = "w")

        self.articleURLLabel = ttk.Label(self.articleInfoFrame, text = "URL:")
        self.articleURLLabel.grid(row = 2, column = 0, sticky = "e")

        self.articleURLEntry = ttk.Label(self.articleInfoFrame)
        self.articleURLEntry.grid(row = 2, column = 1, sticky = "w")

        self.articleYearLabel = ttk.Label(self.articleInfoFrame, text = "Publication Year:")
        self.articleYearLabel.grid(row = 3, column = 0, sticky = "e")

        self.articleYearEntry = ttk.Label(self.articleInfoFrame)
        self.articleYearEntry.grid(row = 3, column = 1, sticky = "w")

        self.articleMonthLabel = ttk.Label(self.articleInfoFrame, text = "Publication Month:")
        self.articleMonthLabel.grid(row = 4, column = 0, sticky = "e")

        self.articleMonthEntry = ttk.Label(self.articleInfoFrame)
        self.articleMonthEntry.grid(row = 4, column = 1, sticky = "w")

        self.articleDayLabel = ttk.Label(self.articleInfoFrame, text = "Publication Day:")
        self.articleDayLabel.grid(row = 5, column = 0, sticky = "e")

        self.articleDayEntry = ttk.Label(self.articleInfoFrame)
        self.articleDayEntry.grid(row = 5, column = 1, sticky = "w")

        self.articlePagesLabel = ttk.Label(self.articleInfoFrame, text = "Pages:")
        self.articlePagesLabel.grid(row = 6, column = 0, sticky = "e")

        self.articlePagesEntry = ttk.Label(self.articleInfoFrame)
        self.articlePagesEntry.grid(row = 6, column = 1, sticky = "w")

        self.articleLanguageLabel = ttk.Label(self.articleInfoFrame, text = "Language:")
        self.articleLanguageLabel.grid(row = 7, column = 0, sticky = "e")

        self.articleLanguageEntry = ttk.Label(self.articleInfoFrame)
        self.articleLanguageEntry.grid(row = 7, column = 1, sticky = "w")

        self.articleFreeLabel = ttk.Label(self.articleInfoFrame, text = "Free:")
        self.articleFreeLabel.grid(row = 8, column = 0, sticky = "e")

        self.is_free = tk.BooleanVar()
        self.articleFreeCheck = ttk.Checkbutton(self.articleInfoFrame, variable = self.is_free, state = "disabled")
        self.articleFreeCheck.grid(row = 8, column = 1, sticky = "w")

        self.articleSubjectLabel = ttk.Label(self.articleInfoFrame, text = "Subject:")
        self.articleSubjectLabel.grid(row = 9, column = 0, sticky = "e")

        self.articleSubjectEntries = []

        self.articleSubjectEntries.append(ttk.Label(self.articleInfoFrame))
        self.articleSubjectEntries[0].grid(row = 9, column = 1, sticky = "w")

        self.articleAuthorLabel = ttk.Label(self.articleInfoFrame, text = "Author:")
        self.articleAuthorLabel.grid(row = 10, column = 0, sticky = "e")

        self.articleAuthorEntries = []
        self.articleAuthorFollowButtons = []
        
        self.articleAuthorEntries.append(ttk.Label(self.articleInfoFrame))
        self.articleAuthorEntries[0].grid(row = 10, column = 1, sticky = "w")

        self.authors_id  = [ a["Id"] for a in self.db.get_articles_authors(doi)]
        self.articleAuthorFollowButtons.append(ttk.Label(self.articleInfoFrame, text = "\u2606"))
        self.articleAuthorFollowButtons[0].bind("<1>", lambda e, button=self.articleAuthorFollowButtons[0]: self.articleAuthorSwitchFollow(button, self.authors_id[len(self.articleAuthorFollowButtons)-2]))
        self.articleAuthorFollowButtons[0].grid(row = 10, column = 1, sticky = "w", padx=(0,0))

        self.articleCitationLabel = ttk.Label(self.articleInfoFrame, text = "Citation:")
        self.articleCitationLabel.grid(row = 11, column = 0, sticky = "e")

        self.articleCitationEntries = []


        

        self.articleCitationEntries.append(ttk.Label(self.articleInfoFrame))
        self.articleCitationEntries[0].grid(row = 11, column = 1, sticky = "w")

        self.articleScoresFrame = ttk.Frame(self.articleFrame)
        self.articleScoresFrame.pack(side = "right", padx = 100)

        self.articleRatingLabel = ttk.Label(self.articleScoresFrame, text = "User Rating:", font = ("Arial", 16))
        self.articleRatingLabel.grid(row = 0, column = 0)

        self.articleRateFrame = ttk.Frame(self.articleScoresFrame)
        self.articleRateFrame.grid(row = 1, column = 0, columnspan = 2)

        self.articleRateLabel = ttk.Label(self.articleRateFrame, text = "Your Rating:", font = ("Arial", 11))
        self.articleRateLabel.grid(row = 0, column = 0, pady = 5)

        self.articleRateStarLabels = []
        for i in range(5):
            self.articleRateStarLabels.append(ttk.Label(self.articleRateFrame, text = "\u2606"))
            self.articleRateStarLabels[i].bind("<1>", lambda e, count=i+1: self.articleRateSwitchStars(count, self.user["Id"], doi))
            self.articleRateStarLabels[i].grid(row = 0, column = i + 1)

        rating = self.db.get_reader_article_rating(self.user["Id"], doi)
        if rating!=None:
            for i,e in enumerate(self.articleRateStarLabels):
                if i < rating:
                    e.config(text = "\u2605")
                    
                else:
                    e.config(text = "\u2606")

        self.actionTitle.config(text = doi)

        article = self.db.get_article(doi)
        title = article["Title"]
        url = article["Link_to_article"]
        year = article["Publication_date"].split("-")[0]
        month = article["Publication_date"].split("-")[1]
        day = article["Publication_date"].split("-")[2]
        pages = article["No_pages"]
        language = article["Language"]
        is_free = True if article["Is_free"]==1 else False
        subjects = [sub for sub in self.db.get_articles_subjects(doi)]
        authors = [f'{a["Fname"]} {a["Lname"]}' for a in self.db.get_articles_authors(doi)]
        citations = [c["Title"] for c in self.db.get_articles_citations(doi)] # from sql
        rating = self.db.get_article_rating(doi) 
        
        if is_free:
            url_visible = True
        else:
            if self.db.is_reader_subscripted(self.user["Id"]):
                url_visible=True
            else:
                url_visible=False


        self.articleDOIEntry.config(text = doi)

        self.articleTitleEntry.config(text = title)

        if url_visible:
            self.articleURLEntry.config(text = url, width = 50)
            self.articleURLEntry.bind("<1>", lambda e: webbrowser.open(url, new = 2))
        else:
            self.articleURLEntry.config(text = "Subscribe to access the contents of this article", width = 50)

        self.articleYearEntry.config(text = year)

        self.articleMonthEntry.config(text = month)

        self.articleDayEntry.config(text = day)

        self.articlePagesEntry.config(text = pages)

        self.articleLanguageEntry.config(text = language)

        self.is_free.set(is_free)

        self.articleSubjectEntries[0].config(text = subjects[0])
        for s in subjects[1:]:
            self.articleAddSubject()
            self.articleSubjectEntries[-1].config(text = s)

        self.articleAuthorEntries[0].config(text = authors[0])
        for a in authors[1:]:
            self.articleAddAuthor()
            self.articleAuthorEntries[-1].config(text = a)
           
        self.root.update()
        for a,s in zip(self.articleAuthorEntries, self.articleAuthorFollowButtons):
            s.grid(row = s.grid_info()["row"], column = 1, sticky = "w", padx=(a.winfo_width(),0))

        for a,b in zip(self.authors_id, self.articleAuthorFollowButtons):
            follows = self.db.does_reader_follows_author(self.user["Id"], a)
            if follows:
                b.config(text = "\u2605", foreground = "gold")


        if len(citations)!=0:
            self.articleCitationEntries[0].config(text = citations[0])
            for c in citations[1:]:
                self.articleAddCitation()
                self.articleCitationEntries[-1].config(text = c)

        self.articleRatingLabel.config(text = self.articleRatingLabel.cget("text") + " {:.2f}".format(rating) if rating!=None else  self.articleRatingLabel.cget("text") + " {}".format(rating))

    def destroyArticle(self):
        self.articleCanvas.destroy()
        self.articleScrollbar.destroy()

    def showSubscriptions(self):
        self.backLabel.config(text = "\u25c0")
        self.backLabel.unbind("<1>")
        self.backLabel.bind("<1>", lambda e: self.subscriptionsToSearch())

        self.subscriptionFrame = ttk.Frame(self.mainReaderWindowFrame)
        self.subscriptionFrame.pack(fill = "both", expand = True)

        is_subscribed = self.db.is_reader_subscripted(self.user["Id"])
        if not is_subscribed:
            self.subscription1Button = ttk.Button(self.subscriptionFrame, text = "1 MONTH", command = lambda: self.chooseSubscription(1))
            self.subscription1Button.pack(pady = 3)

            self.subscription2Button = ttk.Button(self.subscriptionFrame, text = "3 MONTHS", command = lambda: self.chooseSubscription(2))
            self.subscription2Button.pack(pady = 3)

            self.subscription3Button = ttk.Button(self.subscriptionFrame, text = "6 MONTHS", command = lambda: self.chooseSubscription(3))
            self.subscription3Button.pack(pady = 3)

            self.subscription4Button = ttk.Button(self.subscriptionFrame, text = "12 MONTHS", command = lambda: self.chooseSubscription(4))
            self.subscription4Button.pack(pady = 3)

        else: 
            expiration_date = self.db.get_subscription_expiration_date(self.user["Id"])
            self.subscriptionExpirationLabel = ttk.Label(self.subscriptionFrame, text = "Subscribed until: {}".format(expiration_date))
            self.subscriptionExpirationLabel.pack(pady = 3)

            self.subscriptionCancelButton = ttk.Button(self.subscriptionFrame, text = "Cancel subscription", command = self.cancelSubscription)
            self.subscriptionCancelButton.pack(pady = 3)

    def destroySubscriptions(self):
        self.subscriptionFrame.destroy()

    # --- Add/Remove Fields ---
    def magazineAddSubject(self):
        self.magazineEditorLabel.grid(row = self.magazineEditorLabel.grid_info()["row"] + 1, column = 0, sticky = "e")

        for e in self.magazineEditorEntries:
            e.grid(row = e.grid_info()['row'] + 1, column = 1, sticky = "w")

        self.magazineSubjectEntries.append(ttk.Label(self.magazineInfoFrame))
        self.magazineSubjectEntries[-1].grid(row = self.magazineSubjectEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

    def magazineAddEditor(self):
        self.magazineEditorEntries.append(ttk.Label(self.magazineInfoFrame))
        self.magazineEditorEntries[-1].grid(row = self.magazineEditorEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

    def publicationAddEditor(self):
        self.publicationEditorEntries.append(ttk.Label(self.publicationInfoFrame))
        self.publicationEditorEntries[-1].grid(row = self.publicationEditorEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

    def articleAddSubject(self):
        self.articleSubjectEntries.append(ttk.Label(self.articleInfoFrame))
        self.articleSubjectEntries[-1].grid(row = self.articleSubjectEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

        self.articleAuthorLabel.grid(row = self.articleAuthorLabel.grid_info()["row"] + 1, column = 0, sticky = "e")

        for e in self.articleAuthorEntries:
            e.grid(row = e.grid_info()["row"] + 1, column = 1, sticky = "w")

        for e in self.articleAuthorFollowButtons:
            e.grid(row = e.grid_info()["row"] + 1, column = 1, sticky = "w", padx = 0)

        self.articleCitationLabel.grid(row = self.articleCitationLabel.grid_info()["row"] + 1, column = 0, sticky = "e")

        for e in self.articleCitationEntries:
            e.grid(row = e.grid_info()["row"] + 1, column = 1, sticky = "w")

    def articleAddAuthor(self):
        self.articleAuthorEntries.append(ttk.Label(self.articleInfoFrame))
        self.articleAuthorEntries[-1].grid(row = self.articleAuthorEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

        self.articleAuthorFollowButtons.append(ttk.Label(self.articleInfoFrame, text = "\u2606"))
        self.articleAuthorFollowButtons[-1].bind("<1>", lambda e, button=self.articleAuthorFollowButtons[-1]: self.articleAuthorSwitchFollow(button, self.authors_id[len(self.articleAuthorFollowButtons)-1] ))
        self.articleAuthorFollowButtons[-1].grid(row = self.articleAuthorEntries[-1].grid_info()["row"], column = 1, sticky = "w", padx = 0)

        self.articleCitationLabel.grid(row = self.articleCitationLabel.grid_info()["row"] + 1, column = 0, sticky = "e")


        for e in self.articleCitationEntries:
            e.grid(row = e.grid_info()["row"] + 1, column = 1, sticky = "w")

    def articleAddCitation(self):
        self.articleCitationEntries.append(ttk.Label(self.articleInfoFrame))
        self.articleCitationEntries[-1].grid(row = self.articleCitationEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

    def articleAuthorSwitchFollow(self, button, author_id):
        if button.cget("text") == "\u2606":
            button.config(text = "\u2605", foreground = "gold")
            self.db.reader_follow_author(self.user["Id"], author_id)
        else:
            button.config(text = "\u2606", foreground = "black")
            self.db.reader_unfollow_author(self.user["Id"], author_id)

    def articleRateSwitchStars(self, count, user_id, article_doi):
        for i,e in enumerate(self.articleRateStarLabels):
            if i < count:
                e.config(text = "\u2605")
                
            else:
                e.config(text = "\u2606")
        
        self.db.add_reader_rating_to_article(user_id, article_doi, count)  

    # --- Window Transitions ---
    def showResult(self, rid, type):
        self.destroySearch()
        if type == "Magazine":
            self.showMagazine(rid)
        else:
            self.showArticle(rid)

    def magazineToSearch(self):
        self.destroyMagazine()
        self.showSearch()

    def magazineToPublication(self, key):
        issn = self.magazineISSNEntry.cget("text")
        self.destroyMagazine()
        self.showPublication(issn, key)

    def publicationToMagazine(self, issn):
        self.destroyPublication()
        self.showMagazine(issn)

    def publicationToArticle(self, issn, doi):
        volume = self.publicationVolumeEntry.cget("text")
        issue = self.publicationIssueEntry.cget("text")
        key = ",".join((volume, issue))
        self.destroyPublication()
        self.showArticle(doi, issn, key)

    def articleToPublication(self, issn, key):
        self.destroyArticle()
        self.showPublication(issn, key)

    def articleToSearch(self):
        self.destroyArticle()
        self.showSearch()

    def subscriptionsToSearch(self):
        self.destroySubscriptions()
        self.showSearch()

    def searchToSubscriptions(self):
        self.destroySearch()
        self.showSubscriptions()

    # --- Talk to DB ---
    def chooseSubscription(self, subscription_id):
        self.db.reader_gets_subscription(self.user["Id"], subscription_id)

        self.destroySubscriptions()
        self.showSubscriptions()

    def cancelSubscription(self):
        self.db.cancel_subscription(self.user["Id"])

        self.subscriptionsToSearch()

    # === Publisher ===
    # --- Windows ---
    def showPublisherWindow(self):
        self.mainPublisherWindowFrame = ttk.Frame(self.root)
        self.mainPublisherWindowFrame.pack(fill = "both", expand = True)

        self.topBarFrame = ttk.Frame(self.mainPublisherWindowFrame)
        self.topBarFrame.pack(fill = "x", expand = False, anchor = "n")
        self.topBarFrame.grid_columnconfigure(2, weight = 1)

        self.backLabel = ttk.Label(self.topBarFrame, text = "\u25c1", font = ("Arial", 30))
        self.backLabel.grid(row = 0, column = 0, padx = 10)

        self.actionTitle = ttk.Label(self.topBarFrame, text = "All Magazines", font = ("Arial", 16))
        self.actionTitle.grid(row = 0, column = 1, padx = 40)

        self.displayNameLabel = ttk.Label(self.topBarFrame, text = self.displayname, font = ("Arial", 20))
        self.displayNameLabel.grid(row = 0, column = 2, sticky = "e", padx = 10)

        self.topBarSeparator = ttk.Separator(self.topBarFrame)
        self.topBarSeparator.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = "ew", columnspan = 4)

        self.showMagazines()

    def destroyPublisherWindow(self):
        self.mainPublisherWindowFrame.destroy()

    def showMagazines(self):
        self.backLabel.config(text = "\u25c1")
        self.backLabel.unbind("<1>")
        self.actionTitle.config(text = "All Magazines")

        self.magazinesScrollbar = ttk.Scrollbar(self.mainPublisherWindowFrame)
        self.magazinesScrollbar.pack(side="right", fill="y", pady = 2)

        self.magazinesCanvas = tk.Canvas(self.mainPublisherWindowFrame, yscrollcommand = self.magazinesScrollbar.set, highlightthickness = 0)
        self.magazinesCanvas.pack(fill = "both", expand = True)
        self.magazinesScrollbar.config(command = lambda *args: self.yview(self.magazinesCanvas, *args))

        self.magazinesFrame = ttk.Frame(self.magazinesCanvas)
        self.magazinesCanvas.create_window((0, 0), window = self.magazinesFrame, anchor = "nw")
        self.magazinesFrame.bind("<Configure>", lambda e: self.magazinesCanvas.configure(scrollregion = self.magazinesCanvas.bbox("all")))

        self.magazinesLabelFrame = ttk.Frame(self.magazinesFrame)
        self.magazinesLabelFrame.pack(fill = "x", expand = True)

        self.magazinesLabelFrame.grid_columnconfigure(0, weight = 1)
        self.magazinesLabelFrame.grid_columnconfigure(1, weight = 1)

        self.magazinesLabel = ttk.Label(self.magazinesLabelFrame, text = "Magazines:", font = ("Arial", 20))
        self.magazinesLabel.grid(row = 0, column = 0, sticky = "w", padx = (5, 1040))

        self.magazinesAddLabel = ttk.Label(self.magazinesLabelFrame, text = "+", font = ("Arial", 30))
        self.magazinesAddLabel.grid(row = 0, column = 1, sticky = "e", padx = 5)
        self.magazinesAddLabel.bind("<1>", lambda e: self.magazinesToMagazineInfo("<new>"))

        self.magazinesButtonsFrame = ttk.Frame(self.magazinesFrame)
        self.magazinesButtonsFrame.pack(fill = "x", expand = False)

        self.magazines = self.db.get_publishers_magazines(self.user['Id'])
        magazines = []
        for mag in self.magazines:
            magazines.append((mag["Issn"],mag["Title"]))

        self.magazineButtons = []
        for i, m in enumerate(magazines):
            magazineButton = tk.Button(self.magazinesButtonsFrame, text = m[1], height = 3, width = 40, wraplength = 250, relief = "groove", bd = 5, bg = self.stringToColor(m[0]), command = lambda issn=m[0]: self.magazinesToMagazineInfo(issn))
            magazineButton.grid(row = i // 4, column = i % 4, padx = 5, pady = 3)
            self.magazineButtons.append(magazineButton)

    def destroyMagazines(self):
        self.magazinesCanvas.destroy()
        self.magazinesScrollbar.destroy()

    def showMagazineInfo(self, issn):
        self.backLabel.config(text = "\u25c0")
        self.backLabel.unbind("<1>")
        self.backLabel.bind("<1>", lambda e: self.magazineInfoToMagazines())

        self.magazineInfoScrollbar = ttk.Scrollbar(self.mainPublisherWindowFrame)
        self.magazineInfoScrollbar.pack(side="right", fill="y", pady = 2)

        self.magazineInfoCanvas = tk.Canvas(self.mainPublisherWindowFrame, yscrollcommand = self.magazineInfoScrollbar.set, highlightthickness = 0)
        self.magazineInfoCanvas.pack(fill = "both", expand = True)
        self.magazineInfoScrollbar.config(command = lambda *args: self.yview(self.magazineInfoCanvas, *args))

        self.magazineInfoFrame = ttk.Frame(self.magazineInfoCanvas)
        self.magazineInfoCanvas.create_window((0, 0), window = self.magazineInfoFrame, anchor = "nw")
        self.magazineInfoFrame.bind("<Configure>", lambda e: self.magazineInfoCanvas.configure(scrollregion = self.magazineInfoCanvas.bbox("all")))

        self.magazineInfoInfoFrame = tk.Frame(self.magazineInfoFrame)
        self.magazineInfoInfoFrame.pack(fill = tk.X, expand = False)

        self.magazineInfoTitleLabel = ttk.Label(self.magazineInfoInfoFrame, text = "Title:")
        self.magazineInfoTitleLabel.grid(row = 0, column = 0, sticky = "e")

        self.magazineInfoTitleEntry = ttk.Entry(self.magazineInfoInfoFrame)
        self.magazineInfoTitleEntry.grid(row = 0, column = 1, sticky = "w")

        self.magazineInfoISSNLabel = ttk.Label(self.magazineInfoInfoFrame, text = "ISSN:")
        self.magazineInfoISSNLabel.grid(row = 1, column = 0, sticky = "e")

        self.magazineInfoISSNEntry = ttk.Label(self.magazineInfoInfoFrame)
        self.magazineInfoISSNEntry.grid(row = 1, column = 1, sticky = "w")

        self.magazineInfoSubjectLabel = ttk.Label(self.magazineInfoInfoFrame, text = "Subject:")
        self.magazineInfoSubjectLabel.grid(row = 2, column = 0, sticky = "e")

        self.magazineInfoSubjectEntries = []
        self.magazineInfoSubjectRemoveButtons = []
        self.magazineInfosubjectupdateButtons = []

        self.all_subjects = tuple([e for e in self.db.get_all_subjects() if e[0] not in self.db.get_magazines_subjects(issn) ])
        
        self.magazineInfoSubjectEntries.append(ttk.Combobox(self.magazineInfoInfoFrame, values = self.all_subjects))
        self.magazineInfoSubjectEntries[0].grid(row = 2, column = 1, sticky = "w")
        self.magazineInfoSubjectRemoveButtons.append(tk.Button(self.magazineInfoInfoFrame, text = "x", command = lambda entry=self.magazineInfoSubjectEntries[-1]: self.magazineInfoRemoveSubject(entry), bg = "red", fg = "white", relief = "flat", font = ("Arial", 12)))
        self.magazineInfoSubjectRemoveButtons[-1].grid(row = self.magazineInfoSubjectEntries[-1].grid_info()["row"], column = 2, sticky = "w", padx = 2)
        

        self.magazineInfoSubjectButton = ttk.Button(self.magazineInfoInfoFrame, text = "Add Subject", command = lambda: self.magazineInfoAddSubject(issn))
        self.magazineInfoSubjectButton.grid(row = 3, column = 1, sticky = "w")

        self.magazineInfoEditorLabel = ttk.Label(self.magazineInfoInfoFrame, text = "Editor:")
        self.magazineInfoEditorLabel.grid(row = 4, column = 0, sticky = "e")

        self.magazineInfoEditorEntries = []
        self.magazineInfoEditorRemoveButtons = []

        editors = []
        for ed in self.db.get_all_editors():
            editors.append(ed["Fname"]+" "+ed["Lname"])
        self.all_editors = tuple([e for e in editors if e not in [ ed["Fname"]+" "+ed["Lname"] for ed in self.db.get_magazines_editors(issn)] ])
        
        self.magazineInfoEditorEntries.append(ttk.Combobox(self.magazineInfoInfoFrame, values = self.all_editors))
        self.magazineInfoEditorEntries[0].grid(row = 4, column = 1, sticky = "w")
        self.magazineInfoEditorRemoveButtons.append(tk.Button(self.magazineInfoInfoFrame, text = "x", command = lambda entry=self.magazineInfoEditorEntries[-1]: self.magazineInfoRemoveEditor(entry), bg = "red", fg = "white", relief = "flat", font = ("Arial", 12)))
        self.magazineInfoEditorRemoveButtons[-1].grid(row = self.magazineInfoEditorEntries[-1].grid_info()["row"], column = 2, sticky = "w", padx = 2)


        self.magazineInfoEditorButton = ttk.Button(self.magazineInfoInfoFrame, text = "Add Editor", command = lambda: self.magazineInfoAddEditor(issn))
        self.magazineInfoEditorButton.grid(row = 5, column = 1, sticky = "w")

        self.magazineInfoScoresFrame = ttk.Frame(self.magazineInfoFrame)
        self.magazineInfoScoresFrame.pack(fill = "x", padx=10, pady = 5)

        self.magazineInfoRatingLabel = ttk.Label(self.magazineInfoScoresFrame, text = "User Rating:", font = ("Arial", 16))
        self.magazineInfoRatingLabel.grid(row = 0, column = 0)

        self.magazineInfoRatingNumberLabel = ttk.Label(self.magazineInfoScoresFrame, text = "", font = ("Arial", 14))
        self.magazineInfoRatingNumberLabel.grid(row = 0, column = 2)

        self.magazineInfoLabelFrame = ttk.Frame(self.magazineInfoFrame)
        self.magazineInfoLabelFrame.pack(fill = "x", expand = False)

        self.magazineInfoPublicationsLabel = ttk.Label(self.magazineInfoLabelFrame, text = "Publications:", font = ("Arial", 20))
        self.magazineInfoPublicationsLabel.grid(row = 0, column = 0, sticky = "w", padx = (5, 1025))

        self.magazineInfoAddLabel = ttk.Label(self.magazineInfoLabelFrame, text = "+", font = ("Arial", 30))
        self.magazineInfoAddLabel.grid(row = 0, column = 1, sticky = "e", padx = 5)
        self.magazineInfoAddLabel.bind("<1>", lambda e: self.magazineInfoToPublicationInfo(issn,"<new>"))

        self.publicationsButtonsFrame = ttk.Frame(self.magazineInfoFrame)
        self.publicationsButtonsFrame.pack(fill = "x", expand = False)

        if issn == "<new>":
            self.actionTitle.config(text = "New Magazine")
            self.magazineInfoScoresFrame.destroy()
            self.magazineInfoLabelFrame.destroy()
            self.magazineInfoISSNEntry.destroy()
            self.magazineInfoISSNEntry = ttk.Entry(self.magazineInfoInfoFrame, validate = 'key', validatecommand = self.validateIssn)
            self.magazineInfoISSNEntry.grid(row = 1, column = 1, sticky = "w")
            self.magazineInfoCreateMagazineButton = ttk.Button(self.magazineInfoInfoFrame, text = "Create Magazine", command= lambda : self.createMagazine())
            self.magazineInfoCreateMagazineButton.grid(row=6, column=1, sticky="w")
            

        else:
            self.actionTitle.config(text = issn)
            self.magazineInfoSaveChangesButton = ttk.Button(self.magazineInfoInfoFrame, text="Save Changes", command= lambda: self.updateMagazine(issn))
            self.magazineInfoSaveChangesButton.grid(row=0, column=2, sticky="w", padx=(0,0))
            
            self.magazineInfoDeleteMagazineButton = ttk.Button(self.magazineInfoInfoFrame, text="Delete Magazine", command= lambda: self.deleteMagazine(issn))
            self.magazineInfoDeleteMagazineButton.grid(row=0, column=3, sticky="w", padx=(0,0))

            magazine = None
            for mag in self.magazines:
                if mag["Issn"]==issn:
                    magazine = mag
                    break
            
            title = mag["Title"]
            self.magazineInfoTitle = title
            subjects = self.db.get_magazines_subjects(issn)
            editors = [ ed["Fname"]+" "+ed["Lname"] for ed in self.db.get_magazines_editors(issn)]
            impact_factor = mag["Impact_factor"]
            eigenfactor = mag["Eigen_factor"]
            ais = mag["Article_influence_score"]
            citescore = mag["Cite_score"]
            rating = mag["User_rating"]
            

            publications = [(f'{pub["Volume"]},{pub["Issue"]}',) for pub in self.db.get_magazines_publications(issn)]


            self.magazineInfoTitleEntry.insert(0, title)

            self.magazineInfoISSNEntry["text"] = issn
            
            self.magazineInfoSubjectEntries[0].set(subjects[0])
            for s in subjects[1:]:
                self.magazineInfoAddSubject(issn)
                self.magazineInfoSubjectEntries[-1].set(s)
            
            self.magazineInfoEditorEntries[0].set(editors[0])
            for e in editors[1:]:
                self.magazineInfoAddEditor(issn)
                self.magazineInfoEditorEntries[-1].set(e)

            self.magazineInfoRatingNumberLabel.config(text = "{:.1f}".format(rating) if impact_factor!=None else f"{impact_factor}")

            self.publicationButtons = []
            for i, p in enumerate(publications):
                publicationButton = tk.Button(self.publicationsButtonsFrame, text = p[0], height = 3, width = 40, wraplength = 250, relief = "groove", bd = 5, bg = self.stringToColor(p[0]), command = lambda key=p[0]: self.magazineInfoToPublicationInfo(issn, key))
                publicationButton.grid(row = i // 4, column = i % 4, padx = 5, pady = 3)
                self.publicationButtons.append(publicationButton)

    def destroyMagazineInfo(self):
        self.magazineInfoCanvas.destroy()
        self.magazineInfoScrollbar.destroy()

    def showPublicationInfo(self, issn, key):
        self.backLabel.config(text = "\u25c0")
        self.backLabel.unbind("<1>")
        self.backLabel.bind("<1>", lambda e: self.publicationInfoToMagazineInfo(issn))

        self.publicationInfoScrollbar = ttk.Scrollbar(self.mainPublisherWindowFrame)
        self.publicationInfoScrollbar.pack(side="right", fill="y", pady = 2)

        self.publicationInfoCanvas = tk.Canvas(self.mainPublisherWindowFrame, yscrollcommand = self.publicationInfoScrollbar.set, highlightthickness = 0)
        self.publicationInfoCanvas.pack(fill = "both", expand = True)
        self.publicationInfoScrollbar.config(command = lambda *args: self.yview(self.publicationInfoCanvas, *args))

        self.publicationInfoFrame = ttk.Frame(self.publicationInfoCanvas)
        self.publicationInfoCanvas.create_window((0, 0), window = self.publicationInfoFrame, anchor = "nw")
        self.publicationInfoFrame.bind("<Configure>", lambda e: self.publicationInfoCanvas.configure(scrollregion = self.publicationInfoCanvas.bbox("all")))

        self.publicationInfoInfoFrame = ttk.Frame(self.publicationInfoFrame)
        self.publicationInfoInfoFrame.pack(fill = "x", expand = False)

        self.publicationInfoVolumeLabel = ttk.Label(self.publicationInfoInfoFrame, text = "Volume:")
        self.publicationInfoVolumeLabel.grid(row = 0, column = 0, sticky = "e")

        self.publicationInfoVolumeEntry = ttk.Label(self.publicationInfoInfoFrame)
        self.publicationInfoVolumeEntry.grid(row = 0, column = 1, sticky = "w")

        self.publicationInfoIssueLabel = ttk.Label(self.publicationInfoInfoFrame, text = "Issue:")
        self.publicationInfoIssueLabel.grid(row = 1, column = 0, sticky = "e")

        self.publicationInfoIssueEntry = ttk.Label(self.publicationInfoInfoFrame)
        self.publicationInfoIssueEntry.grid(row = 1, column = 1, sticky = "w")

        self.publicationInfoYearLabel = ttk.Label(self.publicationInfoInfoFrame, text = "Publication Year:")
        self.publicationInfoYearLabel.grid(row = 2, column = 0, sticky = "e")

        self.publicationInfoYearEntry = ttk.Entry(self.publicationInfoInfoFrame, validate = 'key', validatecommand = self.validateInteger)
        self.publicationInfoYearEntry.grid(row = 2, column = 1, sticky = "w")

        self.publicationInfoMonthLabel = ttk.Label(self.publicationInfoInfoFrame, text = "Publication Month:")
        self.publicationInfoMonthLabel.grid(row = 3, column = 0, sticky = "e")

        self.publicationInfoMonthEntry = ttk.Entry(self.publicationInfoInfoFrame, validate = 'key', validatecommand = self.validateMonth)
        self.publicationInfoMonthEntry.grid(row = 3, column = 1, sticky = "w")

        self.publicationInfoEditorLabel = ttk.Label(self.publicationInfoInfoFrame, text = "Editor:")
        self.publicationInfoEditorLabel.grid(row = 4, column = 0, sticky = "e")

        self.publicationInfoEditorEntries = []
        self.publicationInfoEditorRemoveButtons = []

        editors = []
        for ed in self.db.get_all_editors():
            editors.append(ed["Fname"]+" "+ed["Lname"])

        if key!="<new>":
            self.all_editors = [ ed["Fname"]+" "+ed["Lname"] for ed in self.db.get_magazines_editors(issn) if ed["Fname"]+" "+ed["Lname"] not in [f'{ed["Fname"]} {ed["Lname"]}' for ed in self.db.get_publications_editors(issn, key.split(",")[0], key.split(",")[1])]] 
        else :
            self.all_editors =  [ ed["Fname"]+" "+ed["Lname"] for ed in self.db.get_magazines_editors(issn) ]


        self.publicationInfoEditorEntries.append(ttk.Combobox(self.publicationInfoInfoFrame, values = self.all_editors))
        self.publicationInfoEditorEntries[0].grid(row = 4, column = 1, sticky = "w")
        self.publicationInfoEditorRemoveButtons.append(tk.Button(self.publicationInfoInfoFrame, text = "x", command = lambda entry=self.publicationInfoEditorEntries[-1]: self.publicationInfoRemoveEditor(entry), bg = "red", fg = "white", relief = "flat", font = ("Arial", 12)))
        self.publicationInfoEditorRemoveButtons[-1].grid(row = self.publicationInfoEditorEntries[-1].grid_info()["row"], column = 2, sticky = "w", padx=2)

        self.publicationInfoEditorButton = ttk.Button(self.publicationInfoInfoFrame, text = "Add Editor", command = lambda : self.publicationInfoAddEditor(issn, key))
        self.publicationInfoEditorButton.grid(row = 5, column = 1, sticky = "w")

        self.publicationInfoLabelFrame = ttk.Frame(self.publicationInfoFrame)
        self.publicationInfoLabelFrame.pack(fill = "x", expand = False)

        self.publicationInfoArticlesLabel = ttk.Label(self.publicationInfoLabelFrame, text = "Articles:", font = ("Arial", 20))
        self.publicationInfoArticlesLabel.grid(row = 0, column = 0, sticky = "w", padx = (5, 1080))

        self.publicationInfoAddLabel = ttk.Label(self.publicationInfoLabelFrame, text = "+", font = ("Arial", 30))
        self.publicationInfoAddLabel.grid(row = 0, column = 1, sticky = "e", padx = 5)
        self.publicationInfoAddLabel.bind("<1>", lambda e: self.publicationInfoToArticleInfo(issn, "<new>", key))

        self.articlesButtonsFrame = ttk.Frame(self.publicationInfoFrame)
        self.articlesButtonsFrame.pack(fill = "x", expand = False)

        if key == "<new>":
            self.publicationInfoVolumeEntry.destroy()
            self.publicationInfoVolumeEntry = ttk.Entry(self.publicationInfoInfoFrame, validate = 'key', validatecommand = self.validateInteger)
            self.publicationInfoVolumeEntry.grid(row = 0, column = 1, sticky = "w")

            self.publicationInfoIssueEntry.destroy()
            self.publicationInfoIssueEntry = ttk.Entry(self.publicationInfoInfoFrame, validate = 'key', validatecommand = self.validateInteger)
            self.publicationInfoIssueEntry.grid(row = 1, column = 1, sticky = "w")

            self.actionTitle.config(text = "New Publication")
            self.publicationInfoLabelFrame.destroy()
            self.publicationInfoCreatePublicationButton = ttk.Button(self.publicationInfoInfoFrame, text="Create Publication", command= lambda:self.createPublication(issn))
            self.publicationInfoCreatePublicationButton.grid(row=6, column=1, sticky="w")


        else:
            self.actionTitle.config(text = key)
            self.publicationInfoSaveChangesButton = ttk.Button(self.publicationInfoInfoFrame, text="Save Changes", command=lambda:self.updatePublication(issn, key))
            self.publicationInfoSaveChangesButton.grid(row=0,column=2)
            self.publicationInfoDeletePublicationButton = ttk.Button(self.publicationInfoInfoFrame, text="Delete Publication", command= lambda: self.deletePublication(issn, key.split(",")[0], key.split(",")[1] ))
            self.publicationInfoDeletePublicationButton.grid(row=0, column=3, sticky="w", padx=(0,0))
            date =  self.db.get_publication_date(issn, key.split(",")[0], key.split(",")[1])
            year = date.split("-")[0]
            month = date.split("-")[1]
            editors = [f'{ed["Fname"]} {ed["Lname"]}' for ed in self.db.get_publications_editors(issn, key.split(",")[0], key.split(",")[1])]

            articles = [ (art["Doi"],art["Title"]) for art in self.db.get_publications_articles(issn, key.split(",")[0], key.split(",")[1])]

            self.publicationInfoVolumeEntry["text"] = key.split(",")[0]

            self.publicationInfoIssueEntry["text"] = key.split(",")[1]
            
            self.publicationInfoYearEntry.insert(0, year)
            
            self.publicationInfoMonthEntry.insert(0, month)
            
            self.publicationInfoEditorEntries[0].set(editors[0] if len(editors)!=0 else "No editors")

            for e in editors[1:]:
                self.publicationInfoAddEditor(issn, key)
                self.publicationInfoEditorEntries[-1].set(e)

            self.articleButtons = []
            for i, a in enumerate(articles):
                articleButton = tk.Button(self.articlesButtonsFrame, text = a[1], height = 3, width = 40, wraplength = 250, relief = "groove", bd = 5, bg = self.stringToColor(a[0]), command = lambda doi=a[0]: self.publicationInfoToArticleInfo(issn, doi, key))
                articleButton.grid(row = i // 4, column = i % 4, padx = 5, pady = 3)
                self.articleButtons.append(articleButton)

    def destroyPublicationInfo(self):
        self.publicationInfoCanvas.destroy()
        self.publicationInfoScrollbar.destroy()

    def showArticleInfo(self, issn, key, doi):
        self.backLabel.config(text = "\u25c0")
        self.backLabel.unbind("<1>")
        self.backLabel.bind("<1>", lambda e: self.articleInfoToPublicationInfo(issn, key))

        self.articleInfoScrollbar = ttk.Scrollbar(self.mainPublisherWindowFrame)
        self.articleInfoScrollbar.pack(side="right", fill="y", pady = 2)

        self.articleInfoCanvas = tk.Canvas(self.mainPublisherWindowFrame, yscrollcommand = self.articleInfoScrollbar.set, highlightthickness = 0)
        self.articleInfoCanvas.pack(fill = "both", expand = True)
        self.articleInfoScrollbar.config(command = lambda *args: self.yview(self.articleInfoCanvas, *args))

        self.articleInfoFrame = ttk.Frame(self.articleInfoCanvas)
        self.articleInfoCanvas.create_window((0, 0), window = self.articleInfoFrame, anchor = "nw")
        self.articleInfoFrame.bind("<Configure>", lambda e: self.articleInfoCanvas.configure(scrollregion = self.articleInfoCanvas.bbox("all")))

        self.articleInfoInfoFrame = ttk.Frame(self.articleInfoFrame)
        self.articleInfoInfoFrame.pack(side = "left", expand = False)

        self.articleInfoDOILabel = ttk.Label(self.articleInfoInfoFrame, text = "DOI:")
        self.articleInfoDOILabel.grid(row = 0, column = 0, sticky = "e")

        self.articleInfoDOIEntry = ttk.Entry(self.articleInfoInfoFrame, validate = 'key', validatecommand = self.validateDoi)
        self.articleInfoDOIEntry.grid(row = 0, column = 1, sticky = "w")

        self.articleInfoTitleLabel = ttk.Label(self.articleInfoInfoFrame, text = "Title:")
        self.articleInfoTitleLabel.grid(row = 1, column = 0, sticky = "e")

        self.articleInfoTitleEntry = ttk.Entry(self.articleInfoInfoFrame)
        self.articleInfoTitleEntry.grid(row = 1, column = 1, sticky = "w")

        self.articleInfoURLLabel = ttk.Label(self.articleInfoInfoFrame, text = "URL:")
        self.articleInfoURLLabel.grid(row = 2, column = 0, sticky = "e")

        self.articleInfoURLEntry = ttk.Entry(self.articleInfoInfoFrame)
        self.articleInfoURLEntry.grid(row = 2, column = 1, sticky = "w")

        self.articleInfoYearLabel = ttk.Label(self.articleInfoInfoFrame, text = "Publication Year:")
        self.articleInfoYearLabel.grid(row = 3, column = 0, sticky = "e")

        self.articleInfoYearEntry = ttk.Entry(self.articleInfoInfoFrame, validate = 'key', validatecommand = self.validateInteger)
        self.articleInfoYearEntry.grid(row = 3, column = 1, sticky = "w")

        self.articleInfoMonthLabel = ttk.Label(self.articleInfoInfoFrame, text = "Publication Month:")
        self.articleInfoMonthLabel.grid(row = 4, column = 0, sticky = "e")

        self.articleInfoMonthEntry = ttk.Entry(self.articleInfoInfoFrame, validate = 'key', validatecommand = self.validateMonth)
        self.articleInfoMonthEntry.grid(row = 4, column = 1, sticky = "w")

        self.articleInfoDayLabel = ttk.Label(self.articleInfoInfoFrame, text = "Publication Day:")
        self.articleInfoDayLabel.grid(row = 5, column = 0, sticky = "e")

        self.articleInfoDayEntry = ttk.Entry(self.articleInfoInfoFrame, validate = 'key', validatecommand = self.validateDay)
        self.articleInfoDayEntry.grid(row = 5, column = 1, sticky = "w")

        self.articleInfoPagesLabel = ttk.Label(self.articleInfoInfoFrame, text = "Pages:")
        self.articleInfoPagesLabel.grid(row = 6, column = 0, sticky = "e")

        self.articleInfoPagesEntry = ttk.Entry(self.articleInfoInfoFrame, validate = 'key', validatecommand = self.validateInteger)
        self.articleInfoPagesEntry.grid(row = 6, column = 1, sticky = "w")

        self.articleInfoLanguageLabel = ttk.Label(self.articleInfoInfoFrame, text = "Language:")
        self.articleInfoLanguageLabel.grid(row = 7, column = 0, sticky = "e")

        self.articleInfoLanguageEntry = ttk.Entry(self.articleInfoInfoFrame)
        self.articleInfoLanguageEntry.grid(row = 7, column = 1, sticky = "w")

        self.articleInfoFreeLabel = ttk.Label(self.articleInfoInfoFrame, text = "Free:")
        self.articleInfoFreeLabel.grid(row = 8, column = 0, sticky = "e")

        self.is_free = tk.BooleanVar()
        self.articleInfoFreeCheck = ttk.Checkbutton(self.articleInfoInfoFrame, variable = self.is_free)
        self.articleInfoFreeCheck.grid(row = 8, column = 1, sticky = "w")

        self.articleInfoSubjectLabel = ttk.Label(self.articleInfoInfoFrame, text = "Subject:")
        self.articleInfoSubjectLabel.grid(row = 9, column = 0, sticky = "e")

        self.articleInfoSubjectEntries = []
        self.articleInfoSubjectRemoveButtons = []

        self.all_subjects = tuple(self.db.get_magazines_subjects(issn))

        self.articleInfoSubjectEntries.append(ttk.Combobox(self.articleInfoInfoFrame, values = self.all_subjects))
        self.articleInfoSubjectEntries[0].grid(row = 9, column = 1, sticky = "w")
        self.articleInfoSubjectRemoveButtons.append(tk.Button(self.articleInfoInfoFrame, text = "x", command = lambda entry=self.articleInfoSubjectEntries[-1]: self.articleInfoRemoveSubject(entry), bg = "red", fg = "white", relief = "flat", font = ("Arial", 12)))
        self.articleInfoSubjectRemoveButtons[-1].grid(row=self.articleInfoSubjectEntries[-1].grid_info()["row"], column=2, sticky = "w", padx=2)

        self.articleInfoSubjectButton = ttk.Button(self.articleInfoInfoFrame, text = "Add Subject", command = self.articleInfoAddSubject)
        self.articleInfoSubjectButton.grid(row = 10, column = 1, sticky = "w")

        self.articleInfoAuthorLabel = ttk.Label(self.articleInfoInfoFrame, text = "Author:")
        self.articleInfoAuthorLabel.grid(row = 11, column = 0, sticky = "e")

        self.articleInfoAuthorEntries = []
        self.articleInfoAuthorRemoveButtons = []

        self.all_authors = tuple([f'{a["Fname"]} {a["Lname"]}' for a in self.db.get_all_authors()])

        self.articleInfoAuthorEntries.append(ttk.Combobox(self.articleInfoInfoFrame, values = self.all_authors))
        self.articleInfoAuthorEntries[0].grid(row = 11, column = 1, sticky = "w")
        self.articleInfoAuthorRemoveButtons.append(tk.Button(self.articleInfoInfoFrame, text = "x", command = lambda entry=self.articleInfoAuthorEntries[-1]: self.articleInfoRemoveAuthor(entry), bg = "red", fg = "white", relief = "flat", font = ("Arial", 12)))
        self.articleInfoAuthorRemoveButtons[-1].grid(row = self.articleInfoAuthorEntries[-1].grid_info()["row"], column = 2, sticky = "w", padx = 2)

        self.articleInfoAuthorButton = ttk.Button(self.articleInfoInfoFrame, text = "Add Author", command = self.articleInfoAddAuthor)
        self.articleInfoAuthorButton.grid(row = 12, column = 1, sticky = "w")

        self.articleInfoCitationLabel = ttk.Label(self.articleInfoInfoFrame, text = "Citation:")
        self.articleInfoCitationLabel.grid(row = 13, column = 0, sticky = "e")

        self.articleInfoCitedLabel = tk.Label(self.articleInfoInfoFrame, text = "")
        self.articleInfoCitedLabel.grid(row = 1, column = 2, sticky = "w")

        self.articleInfoCitationEntries = []
        self.articleInfoCitationRemoveButtons = []

        self.all_articles = tuple([art["Title"] for art in self.db.get_all_articles()])

        self.articleInfoCitationEntries.append(ttk.Combobox(self.articleInfoInfoFrame, values = self.all_articles))
        self.articleInfoCitationEntries[0].grid(row = 13, column = 1, sticky = "w")
        self.articleInfoCitationRemoveButtons.append(tk.Button(self.articleInfoInfoFrame, text = "x", command = lambda entry=self.articleInfoCitationEntries[-1]: self.articleInfoRemoveCitation(entry), bg = "red", fg = "white", relief = "flat", font = ("Arial", 12)))
        self.articleInfoCitationRemoveButtons[-1].grid(row = self.articleInfoCitationEntries[-1].grid_info()["row"], column = 2, sticky = "w", padx = 2)

        self.articleInfoCitationButton = ttk.Button(self.articleInfoInfoFrame, text = "Add Citation", command = self.articleInfoAddCitation)
        self.articleInfoCitationButton.grid(row = 14, column = 1, sticky = "w")

        self.articleInfoScoresFrame = ttk.Frame(self.articleInfoFrame)
        self.articleInfoScoresFrame.pack(side = "right", padx = 100)

        self.articleInfoRatingLabel = ttk.Label(self.articleInfoScoresFrame, text = "User Rating:", font = ("Arial", 16))
        self.articleInfoRatingLabel.grid(row = 0, column = 0)

        if doi == "<new>":
            self.actionTitle.config(text = "New Article")
            self.articleInfoScoresFrame.destroy()
            self.articleInfoCreateArticleButton = ttk.Button(self.articleInfoInfoFrame, text="Create article", command= lambda: self.createArticle(issn, key))
            self.articleInfoCreateArticleButton.grid(row=15, column=1, sticky="w")
            
        else:
            self.actionTitle.config(text = doi)
            self.articleInfoSaveChangesButton =ttk.Button(self.articleInfoInfoFrame, text="Save Changes", command=lambda: self.updateArticle())
            self.articleInfoSaveChangesButton.grid(row=0, column=2, sticky="w")
            self.articleInfoDeleteArticleButton = ttk.Button(self.articleInfoInfoFrame, text="Delete Article", command=lambda: self.deleteArticle(issn, key, doi))
            self.articleInfoDeleteArticleButton.grid(row=0, column=2, sticky="w", padx=(105,0))

            self.articleInfoDOIEntry.destroy()
            self.articleInfoDOIEntry = ttk.Label(self.articleInfoInfoFrame, text=doi)
            self.articleInfoDOIEntry.grid(row = 0, column = 1, sticky = "w")

            article = self.db.get_article(doi)
            title =article["Title"]
            url = article["Link_to_article"]
            year = article["Publication_date"].split("-")[0]
            month = article["Publication_date"].split("-")[1]
            day = article["Publication_date"].split("-")[2]
            pages = article["No_pages"]
            language = article["Language"]
            is_free = True if article["Is_free"]==1 else 0
            self.articleInfoSubjects = [sub for sub in self.db.get_articles_subjects(doi)]
            self.articleInfoAuthors = [f'{a["Fname"]} {a["Lname"]}' for a in self.db.get_articles_authors(doi)] # from sql
            self.articleInfoCitations = [c["Title"] for c in self.db.get_articles_citations(doi)] # from sql
            rating = None 

            self.articleInfoCitedLabel["text"] = "Cited by:" 
            citedby = self.db.get_citations_to_article(doi)
            if len(citedby)==0:
                self.articleInfoCitedLabel["text"]+="None"
            else:
                self.articleInfoCitedLabel["text"]+=" "+citedby[0]["Title"]
                for a in citedby[1:]:
                    self.articleInfoCitedLabel["text"]+=" ,"+a["Title"]
            
            self.articleInfoTitleEntry.insert(0, title)
            
            self.articleInfoURLEntry.insert(0, url)
            
            self.articleInfoYearEntry.insert(0, year)
            
            self.articleInfoMonthEntry.insert(0, month)
            
            self.articleInfoDayEntry.insert(0, day)
            
            self.articleInfoPagesEntry.insert(0, pages)
            
            self.articleInfoLanguageEntry.insert(0, language)
            
            self.is_free.set(is_free)
            
            self.articleInfoSubjectEntries[0].set(self.articleInfoSubjects[0] if len(self.articleInfoSubjects)!=0 else "No subjects")
            for s in self.articleInfoSubjects[1:]:
                self.articleInfoAddSubject()
                self.articleInfoSubjectEntries[-1].set(s)
            
            self.articleInfoAuthorEntries[0].set(self.articleInfoAuthors[0] if len(self.articleInfoAuthors)!=0 else "No authors")
            for a in self.articleInfoAuthors[1:]:
                self.articleInfoAddAuthor()
                self.articleInfoAuthorEntries[-1].set(a)
            
            self.articleInfoCitationEntries[0].set(self.articleInfoCitations[0] if len(self.articleInfoCitations)!=0 else "")
            for c in self.articleInfoCitations[1:]:
                self.articleInfoAddCitation()
                self.articleInfoCitationEntries[-1].set(c)
            
            self.articleInfoRatingLabel.config(text = self.articleInfoRatingLabel.cget("text") + " {:.2f}".format(rating) if rating!=None else self.articleInfoRatingLabel.cget("text") + "None")

    def destroyArticleInfo(self):
        self.articleInfoCanvas.destroy()
        self.articleInfoScrollbar.destroy()

    # --- Create/Update data in DB ---
    def createMagazine(self):
        issn = self.magazineInfoISSNEntry.get()
        allIssns = self.db.get_all_magazines_issn() 
        if issn in allIssns:
            try:
                self.magazineInfoUpdates.destroy()
            except:
                pass
            
            self.magazineInfoUpdates = ttk.Label(self.magazineInfoInfoFrame, text = "Issn already exists")
            self.magazineInfoUpdates.grid(row=0, column=2 , sticky="s", padx=(0,0))
            return

        title = self.magazineInfoTitleEntry.get()
        pub_id = self.user["Id"]

        subjects = [ sub.get() for sub in self.magazineInfoSubjectEntries if sub.get()!="" ]
        editors = [ ed.get() for ed in self.magazineInfoEditorEntries if ed.get()!="" ]

        allEditors = []
        for ed in self.db.get_all_editors():
            allEditors.append(ed["Fname"]+" "+ed["Lname"])
        allSubjects = [s[0] for s in self.db.get_all_subjects()]

        editorsCreated = []
        subjectsCreated = []

        for e in editors:
            if e not in allEditors:
                editorsCreated.append(e)
        for s in subjects:
            if s not in allSubjects:
                subjectsCreated.append(s)


        if issn!="" and title!="" and len(subjects)!=0 and len(editors)!=0:
            self.db.create_magazine(issn, title, pub_id)

            for sub in subjects:
                if sub in [s[0] for s in self.all_subjects]:
                    self.db.add_subject_to_magazine(sub, issn)
                else:
                    self.db.create_subject(sub)
                    self.db.add_subject_to_magazine(sub,issn)

            for ed in editors:
                if ed in self.all_editors:
                    fname = ed.split(" ")[0]
                    lname = ed.split(" ")[1]
                    id = self.db.get_editor_id(fname, lname)
                    self.db.add_editor_to_magazine(id , issn)
                else:
                    fname = ed.split(" ")[0]
                    lname = ed.split(" ")[1]
                    self.db.create_editor(fname, lname)
                    id = self.db.get_editor_id(fname, lname)
                    self.db.add_editor_to_magazine(id , issn)
            
            self.magazineInfoToMagazines()
            self.magazinesToMagazineInfo(issn)
            try:
             self.magazineInfoUpdates.destroy()
            except:
                pass
            
            message = "Magazine created successfuly"
            
            if len(subjectsCreated)!=0:
                message+= "Subjects created:"
                for s in subjectsCreated:
                    message+=s+", "
            if len(editorsCreated)!=0:
                message+=" Editors created:"
                for e in editorsCreated:
                    message+=e+", "
                
            self.magazineInfoUpdates = ttk.Label(self.magazineInfoInfoFrame, text = message)
            self.magazineInfoUpdates.grid(row=0, column=3 , sticky="s", padx=(130,0))
            
        else:
            try:
             self.magazineInfoUpdates.destroy()
            except:
                pass
            
            self.magazineInfoUpdates = ttk.Label(self.magazineInfoInfoFrame, text = "all fields must be included")
            self.magazineInfoUpdates.grid(row=0, column=2 , sticky="s", padx=(0,0))

    def deleteMagazine(self, issn):
        self.db.delete_magazine(issn)
        self.magazineInfoToMagazines()

    def updateMagazine(self, issn):
        subjectsEntries = [ sub.get() for sub in self.magazineInfoSubjectEntries if sub.get()!="" ]
        editorsEntries = [ ed.get() for ed in self.magazineInfoEditorEntries if ed.get()!="" ]
        
        titleEntrie = self.magazineInfoTitleEntry.get()
        
        magazinesSubjects = self.db.get_magazines_subjects(issn)
        magazinesEditors = [ ed["Fname"]+" "+ed["Lname"] for ed in self.db.get_magazines_editors(issn)]

        allSubjects = [s[0] for s in self.db.get_all_subjects()]
        allEditors = []
        for ed in self.db.get_all_editors():
            allEditors.append(ed["Fname"]+" "+ed["Lname"])

        subjectsAdded = []
        subjectsRemoved = []
        subjectsCreated = []

        editorsAdded = []
        editorsRemoved = []
        editorsCreated = []

        for s in subjectsEntries:
            if s not in magazinesSubjects:
                if s not in allSubjects:
                    subjectsAdded.append(s)
                    subjectsCreated.append(s)
                else:
                    subjectsAdded.append(s)
        for s in magazinesSubjects:
            if s not in subjectsEntries:
                subjectsRemoved.append(s)
        
        for e in editorsEntries:
            if e not in magazinesEditors:
                if e not in allEditors:
                    editorsAdded.append(e)
                    editorsCreated.append(e)
                else:
                    editorsAdded.append(e)
        for e in magazinesEditors:
            if e not in editorsEntries:
                editorsRemoved.append(e)

        errors=""
        if len(set(subjectsEntries))!=len(subjectsEntries):
            errors+="Subjects can only be included once, "

        if len(set(editorsEntries))!=len(editorsEntries):
            errors+="Editors can only be included once"
        
        if errors!="":
            try:
                self.magazineInfoUpdates.destroy()
            except:
                pass
            
            self.magazineInfoUpdates = ttk.Label(self.magazineInfoInfoFrame, text = errors)
            self.magazineInfoUpdates.grid(row=0, column=3 , sticky="s", padx=(0,0))
            return

        for s in subjectsCreated:
            self.db.create_subject(s)
        for s in subjectsAdded:
            self.db.add_subject_to_magazine(s, issn)
        for s in subjectsRemoved:
            self.db.remove_subject_from_magazine(s, issn)
        
        for e in editorsCreated:
            self.db.create_editor(e.split(" ")[0], e.split(" ")[1])
        for e in editorsAdded:
            id = self.db.get_editor_id(e.split(" ")[0], e.split(" ")[1])
            self.db.add_editor_to_magazine(id, issn)
        for e in editorsRemoved:
            id  = self.db.get_editor_id(e.split(" ")[0], e.split(" ")[1])
            self.db.remove_editor_from_magazine(id, issn)

        if titleEntrie!=self.magazineInfoTitle:
            self.db.update_magazine_title(issn, titleEntrie)

        updates = ""
        if len(subjectsCreated)==0 and len(subjectsAdded)==0 and len(subjectsRemoved)==0 and len(editorsAdded)==0 and len(editorsCreated)==0 and len(editorsRemoved)==0 and titleEntrie==self.magazineInfoTitle:
            updates += " No changes were made"
        if len(subjectsAdded)!=0:
            updates += " Subjects added:"
            updates+=subjectsAdded[0]
            for s in subjectsAdded[1:]:
                updates+=","+s
        if len(subjectsRemoved)!=0:
            updates+=" Subjcets removed:"
            updates+=subjectsRemoved[0]
            for s in subjectsRemoved[1:]:
                updates+=","+s
        if len(subjectsCreated)!=0:
            updates+=" New subjects Created:"
            updates+=subjectsCreated[0]
            for s in subjectsCreated[1:]:
                updates+=","+s
        if titleEntrie!=self.magazineInfoTitle:
            updates+=" Title changed"
            self.magazineInfoTitle = titleEntrie

        updates+=" \n"
        if len(editorsAdded)!=0:
            updates+=" Editors added:"
            updates+=editorsAdded[0]
            for e in editorsAdded[1:]:
                updates+=","+e
        if len(editorsRemoved)!=0:
            updates+=" Editors removed:"
            updates+=editorsRemoved[0]
            for e in editorsRemoved[1:]:
                updates+=","+e
        if len(editorsCreated)!=0:
            updates+=" New editors created:"
            updates+=editorsCreated[0]
            for e in editorsCreated[1:]:
                updates+=","+e        

        all_editors =  list(self.all_editors)
        for e in editorsCreated:
            all_editors.append(e)
        for e in  self.magazineInfoEditorEntries:
            e["values"] = all_editors

        all_subjects = list(self.all_subjects)
        for s in subjectsCreated:
            all_subjects.append(s)
        for s in self.magazineInfoSubjectEntries:
            s["values"] = all_subjects


        try:
             self.magazineInfoUpdates.destroy()
        except:
            pass
        
        self.magazineInfoUpdates = ttk.Label(self.magazineInfoInfoFrame, text = updates)
        self.magazineInfoUpdates.grid(row=0, column=4 , sticky="s", padx=(0,0))

        subs = tuple([e for e in self.db.get_all_subjects() if e[0] not in self.db.get_magazines_subjects(issn) ])
        for e in  self.magazineInfoSubjectEntries:
            e["values"] = subs
        
        editors = []
        for ed in self.db.get_all_editors():
            editors.append(ed["Fname"]+" "+ed["Lname"])

        eds = tuple([e for e in editors if e not in [ ed["Fname"]+" "+ed["Lname"] for ed in self.db.get_magazines_editors(issn)] ])
        
        for e in self.magazineInfoEditorEntries:
            e["values"] = eds

    def createPublication(self,issn):
        volume = self.publicationInfoVolumeEntry.get()
        issue = self.publicationInfoIssueEntry.get()
        

        publications = [ f'{pub["Volume"]},{pub["Issue"]}' for pub in self.db.get_magazines_publications(issn)]
        if f"{volume},{issue}" in publications:
            try:
                self.publicationInfoUpdates.destroy()
            except:
                pass
            self.publicationInfoUpdates = ttk.Label(self.publicationInfoInfoFrame, text="volume and issue already exists")
            self.publicationInfoUpdates.grid(row=0, column=2)
            return

        year = self.publicationInfoYearEntry.get()
        month = self.publicationInfoMonthEntry.get()
        pubDate = year+"-"+month+"-"+"01"
        editors = [ ed.get() for ed in self.publicationInfoEditorEntries if ed.get()!="" ]
        editorsCreated = []

        if len(set(editors))!=len(editors):
            try:
                self.publicationInfoUpdates.destroy()
            except:
                pass
            self.publicationInfoUpdates = ttk.Label(self.publicationInfoInfoFrame, text="Editors can only be included once")
            self.publicationInfoUpdates.grid(row=0, column=2)
            return

        if volume!="" and issue!="" and year!="" and month!="" and len(editors)!=0:
            for ed in editors:
                if ed in [ ed["Fname"]+" "+ed["Lname"] for ed in self.db.get_magazines_editors(issn)]:
                    pass
                else:
                    try:
                        self.publicationInfoUpdates.destroy()
                    except:
                        pass
                    self.publicationInfoUpdates = ttk.Label(self.publicationInfoInfoFrame, text="editors must belong to magazine")
                    self.publicationInfoUpdates.grid(row=0, column=2)
                    return

            self.db.add_publication_to_magazine(issn,volume, issue,pubDate)
            for ed in editors:
                if ed in self.all_editors:
                    fname = ed.split(" ")[0]
                    lname = ed.split(" ")[1]
                    id = self.db.get_editor_id(fname, lname)
                    self.db.add_editors_to_publication(id, issn, volume, issue)
                else:
                    fname = ed.split(" ")[0]
                    lname = ed.split(" ")[1]
                    self.db.create_editor(fname, lname)
                    editorsCreated.append(ed)
                    id = self.db.get_editor_id(fname, lname)
                    self.db.add_editors_to_publication(id, issn, volume, issue)

            self.publicationInfoToMagazineInfo(issn)
            key =  volume + "," + issue

            self.magazineInfoToPublicationInfo(issn, key)
            try:
                self.publicationInfoUpdates.destroy()
            except:
                pass
            
            message = "publication created successfully"
            self.publicationInfoUpdates = ttk.Label(self.publicationInfoInfoFrame, text=message)
            self.publicationInfoUpdates.grid(row=0, column=3, padx=(140,0))

        else:
            try:
                self.publicationInfoUpdates.destroy()
            except:
                pass
            self.publicationInfoUpdates = ttk.Label(self.publicationInfoInfoFrame, text="all fields must be included")
            self.publicationInfoUpdates.grid(row=0, column=2)
    
    def deletePublication(self, issn, volume, issue):
        self.db.delete_publication(issn, volume, issue)
        self.publicationInfoToMagazineInfo(issn)

    def updatePublication(self, issn, key):
        date =  self.db.get_publication_date(issn, key.split(",")[0], key.split(",")[1])
        year = date.split("-")[0]
        month = date.split("-")[1]
        day = date.split("-")[2]
        new_year = self.publicationInfoYearEntry.get()
        new_month = self.publicationInfoMonthEntry.get()

        editorEntries = [ ed.get() for ed in self.publicationInfoEditorEntries if ed.get()!="" ]
        magazinesEditors = [ ed["Fname"]+" "+ed["Lname"] for ed in self.db.get_magazines_editors(issn)]
        publicationsEditors = [f'{ed["Fname"]} {ed["Lname"]}' for ed in self.db.get_publications_editors(issn, key.split(",")[0], key.split(",")[1])]

        if len(set(editorEntries))!=len(editorEntries):
            try:
                self.publicationInfoUpdates.destroy()
            except:
                pass
            self.publicationInfoUpdates = ttk.Label(self.publicationInfoInfoFrame, text="Editors can only be included once")
            self.publicationInfoUpdates.grid(row=0, column=4)
            return 

        for ed in editorEntries:
            if ed not in magazinesEditors:
                try:
                    self.publicationInfoUpdates.destroy()
                except:
                    pass
                self.publicationInfoUpdates = ttk.Label(self.publicationInfoInfoFrame, text="Editors must belong to magazine")
                self.publicationInfoUpdates.grid(row=0, column=4)
                return

        editorsAdded = []
        editorsRemoved = []

        for ed in editorEntries:
            if ed not in publicationsEditors:
                editorsAdded.append(ed)
        
        for ed in publicationsEditors:
            if ed not in editorEntries:
                editorsRemoved.append(ed)

        for ed in editorsAdded:
            id = self.db.get_editor_id(ed.split(" ")[0],ed.split(" ")[1])
            self.db.add_editors_to_publication(id, issn, key.split(",")[0], key.split(",")[1])
        for ed in editorsRemoved:
            id = self.db.get_editor_id(ed.split(" ")[0],ed.split(" ")[1])
            self.db.remove_editor_from_publication(id ,issn, key.split(",")[0], key.split(",")[1])

        if year!=new_year or month!=new_month:
            self.db.update_pulication_date(issn, key.split(",")[0], key.split(",")[1], f"{new_year}-{new_month}-{day}")

        update=""
        if len(editorsAdded)==0 and len(editorsRemoved)==0 and year==new_year and month==new_month:
            update+="No changes were made"
        if(len(editorsAdded)!=0):
            update+="Editors added: "
            for ed in editorsAdded:
                update+=ed+", "
        if year!=new_year or month!=new_month:
            update+="date changed"
        update+="\n"
        if(len(editorsRemoved)!=0):
            update+="Editors removed: "
            for ed in editorsRemoved:
                update+=ed+", "
        
        
        try:
            self.publicationInfoUpdates.destroy()
        except:
            pass
        self.publicationInfoUpdates = ttk.Label(self.publicationInfoInfoFrame, text=update)
        self.publicationInfoUpdates.grid(row=0, column=4)

        for e in self.publicationInfoEditorEntries:
            e["values"] = [ ed["Fname"]+" "+ed["Lname"] for ed in self.db.get_magazines_editors(issn) if ed["Fname"]+" "+ed["Lname"] not in [f'{ed["Fname"]} {ed["Lname"]}' for ed in self.db.get_publications_editors(issn, key.split(",")[0], key.split(",")[1])]] 

    def createArticle(self, issn, key):
        doi  = self.articleInfoDOIEntry.get()
        allDois = self.db.get_all_articles_doi()

        if doi in allDois:
            try:
                self.articleInfoUpdates.destroy()
            except:
                pass
            self.articleInfoUpdates = ttk.Label(self.articleInfoInfoFrame, text="Doi exists" )
            self.articleInfoUpdates.grid(row=0, column=2)
            return

        title = self.articleInfoTitleEntry.get()
        url = self.articleInfoURLEntry.get()
        year = self.articleInfoYearEntry.get()
        month = self.articleInfoMonthEntry.get()
        day = self.articleInfoDayEntry.get()
        pages = self.articleInfoPagesEntry.get()
        language = self.articleInfoLanguageEntry.get()
        isFree = True if self.articleInfoFreeCheck.state()==('selected',) else False
        
        subjects = [ sub.get() for sub in self.articleInfoSubjectEntries if sub.get()!="" ]
        authors = [ a.get() for a in self.articleInfoAuthorEntries if a.get()!="" ]
        citations = [ c.get() for c in self.articleInfoCitationEntries if c.get()!="" ]

        allSubjects = [s for s in self.all_subjects]
        allAuthors = self.all_authors
        allArticles = self.all_articles

        errors = ""
        for sub in subjects:
                if sub in allSubjects:
                    pass
                else:
                    errors +="subject must belong to article, "
        for a in authors:
            if a in allAuthors:
                pass
            else:
                errors += "author must exist, "
                
        for c in citations:
            if c in allArticles:
                pass
            else:
                errors += "citation article must exist "
                

        if doi!="" and title!="" and url!="" and year!="" and month!="" and day!="" and pages!="" and language!="" and len(subjects)!=0 and len(authors)!=0 and errors=="":
            self.db.add_article_to_publication(doi, title, pages, language, isFree, url, issn, key.split(",")[0], key.split(",")[1], f"{year}-{month}-{day}")
            for sub in subjects:
                if sub in allSubjects:
                    self.db.add_subject_to_article(sub, doi)
                else:
                    print("subject must belong to article")
            for a in authors:
                if a in allAuthors:
                    author_id = self.db.get_author_id(a.split(" ")[0], a.split(" ")[1])
                    self.db.add_author_to_article(author_id, doi)
                else:
                    print("author must exist")
                    
            for c in citations:
                if c in allArticles:
                    doi_cites = self.db.get_article_doi(c)
                    self.db.add_citation_to_article(doi, doi_cites)
                else:
                    print("citation article must exist")

            self.articleInfoToPublicationInfo(issn,key)
            self.publicationInfoToArticleInfo(issn,doi, key)

            try:
                self.articleInfoUpdates.destroy()
            except:
                pass
            self.articleInfoUpdates = ttk.Label(self.articleInfoInfoFrame, text="article created Successfully")
            self.articleInfoUpdates.grid(row=0, column=3)   

        elif doi!="" and title!="" and url!="" and year!="" and month!="" and day!="" and pages!="" and language!="" and len(subjects)!=0 and len(authors)!=0 and errors!="":
            try:
                self.articleInfoUpdates.destroy()
            except:
                pass
            self.articleInfoUpdates = ttk.Label(self.articleInfoInfoFrame, text=errors)
            self.articleInfoUpdates.grid(row=0, column=2)
        
        elif (doi!="" and title!="" and url!="" and year!="" and month!="" and day!="" and pages!="" and language!="" and len(subjects)!=0 and len(authors)!=0)==False and errors=="":
            try:
                self.articleInfoUpdates.destroy()
            except:
                pass
            self.articleInfoUpdates = ttk.Label(self.articleInfoInfoFrame, text="all fields must be included")
            self.articleInfoUpdates.grid(row=0, column=2)
        else:
            try:
                self.articleInfoUpdates.destroy()
            except:
                pass
            self.articleInfoUpdates = ttk.Label(self.articleInfoInfoFrame, text="all fields must be included "+errors)
            self.articleInfoUpdates.grid(row=0, column=2)

    def deleteArticle(self, issn, key, doi):
        self.db.delete_article(doi)
        self.articleInfoToPublicationInfo(issn, key)

    def updateArticle(self):
        doi = self.articleInfoDOIEntry["text"]
        title = self.articleInfoTitleEntry.get()
        url = self.articleInfoURLEntry.get()
        year = self.articleInfoYearEntry.get()
        month = self.articleInfoMonthEntry.get()
        day = self.articleInfoDayEntry.get()
        pages = self.articleInfoPagesEntry.get()
        language = self.articleInfoLanguageEntry.get()
        isFree = True if self.articleInfoFreeCheck.state()==('selected',) else False

        subjects = [ sub.get() for sub in self.articleInfoSubjectEntries if sub.get()!="" ]
        authors = [ a.get() for a in self.articleInfoAuthorEntries if a.get()!="" ]
        citations = [ c.get() for c in self.articleInfoCitationEntries if c.get()!="" ]

        if len(set(subjects))!=len(subjects):
            try:
                self.articleInfoUpdates.destroy()
            except:
                pass
            self.articleInfoUpdates = ttk.Label(self.articleInfoInfoFrame, text="subjects can only be included once")
            self.articleInfoUpdates.grid(row=0, column=2, sticky="w", padx=(215,0))
            return
        if len(set(authors))!=len(authors):
            try:
                self.articleInfoUpdates.destroy()
            except:
                pass
            self.articleInfoUpdates = ttk.Label(self.articleInfoInfoFrame, text="authors can only be included once")
            self.articleInfoUpdates.grid(row=0, column=2, sticky="w", padx=(215,0))
            return
        if len(set(citations))!=len(citations):
            try:
                self.articleInfoUpdates.destroy()
            except:
                pass
            self.articleInfoUpdates = ttk.Label(self.articleInfoInfoFrame, text="citations can only be included once")
            self.articleInfoUpdates.grid(row=0, column=2, sticky="w", padx=(215,0))
            return

        allSubjects = [s for s in self.all_subjects]
        allAuthors = self.all_authors
        allArticles = self.all_articles

        subjectsAdded = []
        subjectsRemoved = []

        authorsAdded = []
        authorsRemoved = []

        citationsAdded = []
        citationsRemoved = []


        errors = ""
        for sub in subjects:
            if sub in allSubjects:
                pass
            else:
                errors +="subject must belong to article, "
        for a in authors:
            if a in allAuthors:
                pass
            else:
                errors += "author must exist, "
                
        for c in citations:
            if c in allArticles:
                pass
            else:
                errors += "citation article must exist "
    
        for sub in self.articleInfoSubjects:
            if sub not in subjects:
                subjectsRemoved.append(sub)  
        for a in self.articleInfoAuthors:
            if a not in authors:
                authorsRemoved.append(a)
        for c in self.articleInfoCitations:
            if c not in citations:
                citationsRemoved.append(c)

        for sub in subjects:
            if sub not in self.articleInfoSubjects:
                subjectsAdded.append(sub)
        for a in authors:
            if a not in self.articleInfoAuthors:
                authorsAdded.append(a)
        for c in citations:
            if c not in self.articleInfoCitations:
                citationsAdded.append(c)

        if title!="" and url!="" and year!="" and month!="" and day!="" and pages!="" and language!="" and len(subjects)!=0 and len(authors)!=0 and errors=="":
            for s in subjectsAdded:
                self.db.add_subject_to_article(s,doi)
            for s in subjectsRemoved:
                self.db.remove_subject_from_article(s,doi)
            
            for a in authorsAdded:
                id = self.db.get_author_id(a.split(" ")[0],a.split(" ")[1])
                self.db.add_author_to_article(id, doi)
            
            for a in authorsRemoved:
                id = self.db.get_author_id(a.split(" ")[0],a.split(" ")[1])
                self.db.remove_author_from_article(id, doi)

            for c in citationsAdded:
                cited_doi = self.db.get_article_doi(c)
                self.db.add_citation_to_article(doi, cited_doi)

            for c in citationsRemoved:
                cited_doi = self.db.get_article_doi(c)
                self.db.remove_citation_from_article(doi, cited_doi)

            
            self.db.update_article(doi, title, url, f"{year}-{month}-{day}", pages, language, isFree)

            try:
                self.articleInfoUpdates.destroy()
            except:
                pass
            self.articleInfoUpdates = ttk.Label(self.articleInfoInfoFrame, text="article updated \n success")
            self.articleInfoUpdates.grid(row=0, column=2, sticky="w", padx=(215,0))


        elif title!="" and url!="" and year!="" and month!="" and day!="" and pages!="" and language!="" and len(subjects)!=0 and len(authors)!=0 and errors!="":
            try:
                self.articleInfoUpdates.destroy()
            except:
                pass
            self.articleInfoUpdates = ttk.Label(self.articleInfoInfoFrame, text=errors)
            self.articleInfoUpdates.grid(row=0, column=2, sticky="w", padx=(215,0))

        elif (title!="" and url!="" and year!="" and month!="" and day!="" and pages!="" and language!="" and len(subjects)!=0 and len(authors)!=0)==False and errors=="":
            try:
                self.articleInfoUpdates.destroy()
            except:
                pass
            self.articleInfoUpdates = ttk.Label(self.articleInfoInfoFrame, text="all fields must be included")
            self.articleInfoUpdates.grid(row=0, column=2, sticky="w", padx=(215,0))
        else:
            try:
                self.articleInfoUpdates.destroy()
            except:
                pass
            self.articleInfoUpdates = ttk.Label(self.articleInfoInfoFrame, text="all fields must be included "+errors)
            self.articleInfoUpdates.grid(row=0, column=2, sticky="w", padx=(215,0))    
        
    # --- Add/Remove Fields ---
    def magazineInfoAddSubject(self, issn):
        self.all_subjects = tuple([e for e in self.db.get_all_subjects() if e[0] not in self.db.get_magazines_subjects(issn) ])
        self.magazineInfoSubjectEntries.append(ttk.Combobox(self.magazineInfoInfoFrame, values = self.all_subjects))
        self.magazineInfoSubjectEntries[-1].grid(row = self.magazineInfoSubjectEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

        self.magazineInfoSubjectRemoveButtons.append(tk.Button(self.magazineInfoInfoFrame, text = "x", command = lambda entry=self.magazineInfoSubjectEntries[-1]: self.magazineInfoRemoveSubject(entry), bg = "red", fg = "white", relief = "flat", font = ("Arial", 12)))
        self.magazineInfoSubjectRemoveButtons[-1].grid(row = self.magazineInfoSubjectEntries[-1].grid_info()["row"], column = 2, sticky = "w", padx = 2)

        self.magazineInfoSubjectButton.grid(row = self.magazineInfoSubjectButton.grid_info()["row"] + 1, column = 1, sticky = "w")

        self.magazineInfoEditorLabel.grid(row = self.magazineInfoEditorLabel.grid_info()["row"] + 1, column = 0, sticky = "e")

        for e in self.magazineInfoEditorEntries:
            e.grid(row = e.grid_info()['row'] + 1, column = 1, sticky = "w")

        for e in self.magazineInfoEditorRemoveButtons:
            e.grid(row = e.grid_info()['row'] + 1, column = 2, sticky = "w")

        self.magazineInfoEditorButton.grid(row = self.magazineInfoEditorButton.grid_info()["row"] + 1, column = 1, sticky = "w")

        
        try:
            self.magazineInfoCreateMagazineButton.grid(row=self.magazineInfoCreateMagazineButton.grid_info()["row"]+1, column=1, sticky="w")
        except:
            pass

    def magazineInfoRemoveSubject(self, entry):
        if len(self.magazineInfoSubjectEntries)==1:
            try:
             self.magazineInfoUpdates.destroy()
            except:
                pass
            self.magazineInfoUpdates = ttk.Label(self.magazineInfoInfoFrame, text = "magazine must have at least one subject")
            self.magazineInfoUpdates.grid(row=0, column=4 , sticky="s", padx=(0,0))
            return

        remove_index = self.magazineInfoSubjectEntries.index(entry)
        entry.destroy()
        del self.magazineInfoSubjectEntries[remove_index]
        self.magazineInfoSubjectRemoveButtons[remove_index].destroy()
        del self.magazineInfoSubjectRemoveButtons[remove_index]

        for e in self.magazineInfoSubjectEntries[remove_index:]:
            e.grid(row = e.grid_info()['row'] - 1, column = 1, sticky = "w")

        for e in self.magazineInfoSubjectRemoveButtons[remove_index:]:
            e.grid(row = e.grid_info()['row'] - 1, column = 2, sticky = "w")

        self.magazineInfoSubjectButton.grid(row = self.magazineInfoSubjectButton.grid_info()["row"] - 1, column = 1, sticky = "w")

        self.magazineInfoEditorLabel.grid(row = self.magazineInfoEditorLabel.grid_info()["row"] - 1, column = 0, sticky = "e")

        for e in self.magazineInfoEditorEntries:
            e.grid(row = e.grid_info()['row'] - 1, column = 1, sticky = "w")

        for e in self.magazineInfoEditorRemoveButtons:
            e.grid(row = e.grid_info()['row'] - 1, column = 2, sticky = "w")

        self.magazineInfoEditorButton.grid(row = self.magazineInfoEditorButton.grid_info()["row"] - 1, column = 1, sticky = "w")
        
        try:
            self.magazineInfoCreateMagazineButton.grid(row=self.magazineInfoCreateMagazineButton.grid_info()["row"]+1, column=1, sticky="w")
        except:
            pass

    def magazineInfoAddEditor(self, issn):
        editors = []
        for ed in self.db.get_all_editors():
            editors.append(ed["Fname"]+" "+ed["Lname"])
        all_editors = tuple([e for e in editors if e not in [ ed["Fname"]+" "+ed["Lname"] for ed in self.db.get_magazines_editors(issn)] ])
        
        self.magazineInfoEditorEntries.append(ttk.Combobox(self.magazineInfoInfoFrame, values = all_editors))
        self.magazineInfoEditorEntries[-1].grid(row = self.magazineInfoEditorEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

        self.magazineInfoEditorRemoveButtons.append(tk.Button(self.magazineInfoInfoFrame, text = "x", command = lambda entry=self.magazineInfoEditorEntries[-1]: self.magazineInfoRemoveEditor(entry), bg = "red", fg = "white", relief = "flat", font = ("Arial", 12)))
        self.magazineInfoEditorRemoveButtons[-1].grid(row = self.magazineInfoEditorEntries[-1].grid_info()["row"], column = 2, sticky = "w", padx = 2)

        self.magazineInfoEditorButton.grid(row = self.magazineInfoEditorButton.grid_info()["row"] + 1, column = 1, sticky = "w")

        try:
            self.magazineInfoCreateMagazineButton.grid(row=self.magazineInfoCreateMagazineButton.grid_info()["row"]+1, column=1, sticky="w")
        except:
            pass

    def magazineInfoRemoveEditor(self, entry):
        if len(self.magazineInfoEditorEntries)==1:
            try:
             self.magazineInfoUpdates.destroy()
            except:
                pass
            self.magazineInfoUpdates = ttk.Label(self.magazineInfoInfoFrame, text = "magazine must have at least one editor")
            self.magazineInfoUpdates.grid(row=0, column=4 , sticky="s", padx=(0,0))
            return
            
        remove_index = self.magazineInfoEditorEntries.index(entry)
        entry.destroy()
        del self.magazineInfoEditorEntries[remove_index]
        self.magazineInfoEditorRemoveButtons[remove_index].destroy()
        del self.magazineInfoEditorRemoveButtons[remove_index]

        for e in self.magazineInfoEditorEntries[remove_index:]:
            e.grid(row = e.grid_info()['row'] - 1, column = 1, sticky = "w")

        for e in self.magazineInfoEditorRemoveButtons[remove_index:]:
            e.grid(row = e.grid_info()['row'] - 1, column = 2, sticky = "w")

        self.magazineInfoEditorButton.grid(row = self.magazineInfoEditorButton.grid_info()["row"] - 1, column = 1, sticky = "w")

        try:
            self.magazineInfoCreateMagazineButton.grid(row=self.magazineInfoCreateMagazineButton.grid_info()["row"]+1, column=1, sticky="w")
        except:
            pass

    def publicationInfoAddEditor(self, issn, key):
        self.publicationInfoEditorEntries.append(ttk.Combobox(self.publicationInfoInfoFrame, values =  [ ed["Fname"]+" "+ed["Lname"] for ed in self.db.get_magazines_editors(issn)] ))
        self.publicationInfoEditorEntries[-1].grid(row = self.publicationInfoEditorEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

        self.publicationInfoEditorRemoveButtons.append(tk.Button(self.publicationInfoInfoFrame, text = "x", command = lambda entry=self.publicationInfoEditorEntries[-1]: self.publicationInfoRemoveEditor(entry), bg = "red", fg = "white", relief = "flat", font = ("Arial", 12)))
        self.publicationInfoEditorRemoveButtons[-1].grid(row = self.publicationInfoEditorEntries[-1].grid_info()["row"], column = 2, sticky = "w", padx = 2)

        self.publicationInfoEditorButton.grid(row = self.publicationInfoEditorButton.grid_info()["row"] + 1, column = 1, sticky = "w")

        try:
            self.publicationInfoCreatePublicationButton.grid(row=self.publicationInfoCreatePublicationButton.grid_info()["row"]+1, column=1, sticky="w")
        except:
            pass

        if key!="<new>":
            for e in self.publicationInfoEditorEntries:
                e["values"] = [ ed["Fname"]+" "+ed["Lname"] for ed in self.db.get_magazines_editors(issn) if ed["Fname"]+" "+ed["Lname"] not in [f'{ed["Fname"]} {ed["Lname"]}' for ed in self.db.get_publications_editors(issn, key.split(",")[0], key.split(",")[1])]] 
        else:
            for e in self.publicationInfoEditorEntries:
                e["values"] = [ ed["Fname"]+" "+ed["Lname"] for ed in self.db.get_magazines_editors(issn)]

    def publicationInfoRemoveEditor(self, entry):
        if len(self.publicationInfoEditorEntries)==1:
            try:
                self.publicationInfoUpdates.destroy()
            except:
                pass
            self.publicationInfoUpdates = ttk.Label(self.publicationInfoInfoFrame, text="publication must have at least one editor")
            self.publicationInfoUpdates.grid(row=0, column=4)
            return

        remove_index = self.publicationInfoEditorEntries.index(entry)
        entry.destroy()
        del self.publicationInfoEditorEntries[remove_index]
        self.publicationInfoEditorRemoveButtons[remove_index].destroy()
        del self.publicationInfoEditorRemoveButtons[remove_index]

        for e in self.publicationInfoEditorEntries[remove_index:]:
            e.grid(row = e.grid_info()['row'] - 1, column = 1, sticky = "w")

        for e in self.publicationInfoEditorRemoveButtons[remove_index:]:
            e.grid(row = e.grid_info()['row'] - 1, column = 2, sticky = "w")

    def articleInfoAddSubject(self):
        self.articleInfoSubjectEntries.append(ttk.Combobox(self.articleInfoInfoFrame, values =  self.all_subjects))
        self.articleInfoSubjectEntries[-1].grid(row = self.articleInfoSubjectEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

        self.articleInfoSubjectRemoveButtons.append(tk.Button(self.articleInfoInfoFrame, text = "x", command = lambda entry=self.articleInfoSubjectEntries[-1]: self.articleInfoRemoveSubject(entry), bg = "red", fg = "white", relief = "flat", font = ("Arial", 12)))
        self.articleInfoSubjectRemoveButtons[-1].grid(row = self.articleInfoSubjectEntries[-1].grid_info()["row"], column = 2, sticky = "w", padx = 2)

        self.articleInfoSubjectButton.grid(row = self.articleInfoSubjectButton.grid_info()["row"] + 1, column = 1, sticky = "w")

        self.articleInfoAuthorLabel.grid(row = self.articleInfoAuthorLabel.grid_info()["row"] + 1, column = 0, sticky = "e")

        for e in self.articleInfoAuthorEntries:
            e.grid(row = e.grid_info()["row"] + 1, column = 1, sticky = "w")

        for e in self.articleInfoAuthorRemoveButtons:
            e.grid(row = e.grid_info()["row"] + 1, column = 2, sticky = "w")

        self.articleInfoAuthorButton.grid(row = self.articleInfoAuthorButton.grid_info()["row"] + 1, column = 1, sticky = "w")

        self.articleInfoCitationLabel.grid(row = self.articleInfoCitationLabel.grid_info()["row"] + 1, column = 0, sticky = "e")


        for e in self.articleInfoCitationEntries:
            e.grid(row = e.grid_info()["row"] + 1, column = 1, sticky = "w")

        for e in self.articleInfoCitationRemoveButtons:
            e.grid(row = e.grid_info()["row"] + 1, column = 2, sticky = "w")

        self.articleInfoCitationButton.grid(row = self.articleInfoCitationButton.grid_info()["row"] + 1, column = 1, sticky = "w")

        try:
            self.articleInfoCreateArticleButton.grid(row=self.articleInfoCreateArticleButton.grid_info()["row"]+1, column=1, sticky="w")
        except:
            pass

    def articleInfoRemoveSubject(self, entry):
        if len(self.articleInfoSubjectEntries)==1:
            try :
                self.articleInfoUpdates.destroy()
            except:
                pass
            self.articleInfoUpdates = ttk.Label(self.articleInfoInfoFrame, text="article must have at least one subject")
            self.articleInfoUpdates.grid(row=0, column=2, sticky="w", padx= (215,0))
            return 
            
        remove_index = self.articleInfoSubjectEntries.index(entry)
        entry.destroy()
        del self.articleInfoSubjectEntries[remove_index]
        self.articleInfoSubjectRemoveButtons[remove_index].destroy()
        del self.articleInfoSubjectRemoveButtons[remove_index]

        for e in self.articleInfoSubjectEntries[remove_index:]:
            e.grid(row = e.grid_info()['row'] - 1, column = 1, sticky = "w")

        for e in self.articleInfoSubjectRemoveButtons[remove_index:]:
            e.grid(row = e.grid_info()['row'] - 1, column = 2, sticky = "w")

        self.articleInfoSubjectButton.grid(row = self.articleInfoSubjectButton.grid_info()["row"] - 1, column = 1, sticky = "w")

        self.articleInfoAuthorLabel.grid(row = self.articleInfoAuthorLabel.grid_info()["row"] - 1, column = 0, sticky = "e")

        for e in self.articleInfoAuthorEntries:
            e.grid(row = e.grid_info()['row'] - 1, column = 1, sticky = "w")

        for e in self.articleInfoAuthorRemoveButtons:
            e.grid(row = e.grid_info()['row'] - 1, column = 2, sticky = "w")

        self.articleInfoAuthorButton.grid(row = self.articleInfoAuthorButton.grid_info()["row"] - 1, column = 1, sticky = "w")

        self.articleInfoCitationLabel.grid(row = self.articleInfoCitationLabel.grid_info()["row"] - 1, column = 0, sticky = "e")
        

        for e in self.articleInfoCitationEntries:
            e.grid(row = e.grid_info()['row'] - 1, column = 1, sticky = "w")

        for e in self.articleInfoCitationRemoveButtons:
            e.grid(row = e.grid_info()['row'] - 1, column = 2, sticky = "w")

        self.articleInfoCitationButton.grid(row = self.articleInfoCitationButton.grid_info()["row"] - 1, column = 1, sticky = "w")

        try:
            self.articleInfoCreateArticleButton.grid(row=self.articleInfoCreateArticleButton.grid_info()["row"]-1, column=1, sticky="w")
        except:
            pass

    def articleInfoAddAuthor(self):
        self.articleInfoAuthorEntries.append(ttk.Combobox(self.articleInfoInfoFrame, values = self.all_authors))
        self.articleInfoAuthorEntries[-1].grid(row = self.articleInfoAuthorEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

        self.articleInfoAuthorRemoveButtons.append(tk.Button(self.articleInfoInfoFrame, text = "x", command = lambda entry=self.articleInfoAuthorEntries[-1]: self.articleInfoRemoveAuthor(entry), bg = "red", fg = "white", relief = "flat", font = ("Arial", 12)))
        self.articleInfoAuthorRemoveButtons[-1].grid(row = self.articleInfoAuthorEntries[-1].grid_info()["row"], column = 2, sticky = "w", padx = 2)

        self.articleInfoAuthorButton.grid(row = self.articleInfoAuthorButton.grid_info()["row"] + 1, column = 1, sticky = "w")

        self.articleInfoCitationLabel.grid(row = self.articleInfoCitationLabel.grid_info()["row"] + 1, column = 0, sticky = "e")
        

        for e in self.articleInfoCitationEntries:
            e.grid(row = e.grid_info()["row"] + 1, column = 1, sticky = "w")

        for e in self.articleInfoCitationRemoveButtons:
            e.grid(row = e.grid_info()["row"] + 1, column = 2, sticky = "w")

        self.articleInfoCitationButton.grid(row = self.articleInfoCitationButton.grid_info()["row"] + 1, column = 1, sticky = "w")
        
        try:
            self.articleInfoCreateArticleButton.grid(row=self.articleInfoCreateArticleButton.grid_info()["row"]+1, column=1, sticky="w")
        except:
            pass

    def articleInfoRemoveAuthor(self, entry):
        if len(self.articleInfoAuthorEntries)==1:
            try :
                self.articleInfoUpdates.destroy()
            except:
                pass
            self.articleInfoUpdates = ttk.Label(self.articleInfoInfoFrame, text="article must have at least one author")
            self.articleInfoUpdates.grid(row=0, column=2, sticky="w", padx=(215,0))
            return 

        remove_index = self.articleInfoAuthorEntries.index(entry)
        entry.destroy()
        del self.articleInfoAuthorEntries[remove_index]
        self.articleInfoAuthorRemoveButtons[remove_index].destroy()
        del self.articleInfoAuthorRemoveButtons[remove_index]

        for e in self.articleInfoAuthorEntries[remove_index:]:
            e.grid(row = e.grid_info()['row'] - 1, column = 1, sticky = "w")

        for e in self.articleInfoAuthorRemoveButtons[remove_index:]:
            e.grid(row = e.grid_info()['row'] - 1, column = 2, sticky = "w")

        self.articleInfoAuthorButton.grid(row = self.articleInfoAuthorButton.grid_info()["row"] - 1, column = 1, sticky = "w")

        self.articleInfoCitationLabel.grid(row = self.articleInfoCitationLabel.grid_info()["row"] - 1, column = 0, sticky = "e")

        for e in self.articleInfoCitationEntries:
            e.grid(row = e.grid_info()['row'] - 1, column = 1, sticky = "w")

        for e in self.articleInfoCitationRemoveButtons:
            e.grid(row = e.grid_info()['row'] - 1, column = 2, sticky = "w")

        self.articleInfoCitationButton.grid(row = self.articleInfoCitationButton.grid_info()["row"] - 1, column = 1, sticky = "w")

        try:
            self.articleInfoCreateArticleButton.grid(row=self.articleInfoCreateArticleButton.grid_info()["row"]-1, column=1, sticky="w")
        except:
            pass

    def articleInfoAddCitation(self):
        self.articleInfoCitationEntries.append(ttk.Combobox(self.articleInfoInfoFrame, values = self.all_articles))
        self.articleInfoCitationEntries[-1].grid(row = self.articleInfoCitationEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

        self.articleInfoCitationRemoveButtons.append(tk.Button(self.articleInfoInfoFrame, text = "x", command = lambda entry=self.articleInfoCitationEntries[-1]: self.articleInfoRemoveCitation(entry), bg = "red", fg = "white", relief = "flat", font = ("Arial", 12)))
        self.articleInfoCitationRemoveButtons[-1].grid(row = self.articleInfoCitationEntries[-1].grid_info()["row"], column = 2, sticky = "w", padx = 2)

        self.articleInfoCitationButton.grid(row = self.articleInfoCitationButton.grid_info()["row"] + 1, column = 1, sticky = "w")

        try:
            self.articleInfoCreateArticleButton.grid(row=self.articleInfoCreateArticleButton.grid_info()["row"]+1, column=1, sticky="w")
        except:
            pass

    def articleInfoRemoveCitation(self, entry):
        if len(self.articleInfoCitationEntries)==1:
            self.articleInfoCitationEntries[0].set("")
            return

        remove_index = self.articleInfoCitationEntries.index(entry)
        entry.destroy()
        del self.articleInfoCitationEntries[remove_index]
        self.articleInfoCitationRemoveButtons[remove_index].destroy()
        del self.articleInfoCitationRemoveButtons[remove_index]

        for e in self.articleInfoCitationEntries[remove_index:]:
            e.grid(row = e.grid_info()['row'] - 1, column = 1, sticky = "w")

        for e in self.articleInfoCitationRemoveButtons[remove_index:]:
            e.grid(row = e.grid_info()['row'] - 1, column = 2, sticky = "w")

        self.articleInfoCitationButton.grid(row = self.articleInfoCitationButton.grid_info()["row"] - 1, column = 1, sticky = "w")

        try:
            self.articleInfoCreateArticleButton.grid(row=self.articleInfoCreateArticleButton.grid_info()["row"]-1, column=1, sticky="w")
        except:
            pass

    # --- Window Transitions ---
    def magazinesToMagazineInfo(self, issn):
        self.destroyMagazines()
        self.showMagazineInfo(issn)

    def magazineInfoToMagazines(self):
        self.destroyMagazineInfo()
        self.showMagazines()

    def magazineInfoToPublicationInfo(self, issn, key):
        self.destroyMagazineInfo()
        self.showPublicationInfo(issn, key)

    def publicationInfoToMagazineInfo(self, issn):
        self.destroyPublicationInfo()
        self.showMagazineInfo(issn)

    def publicationInfoToArticleInfo(self, issn, doi, key):
        self.destroyPublicationInfo()
        self.showArticleInfo(issn, key, doi)

    def articleInfoToPublicationInfo(self, issn, key):
        self.destroyArticleInfo()
        self.showPublicationInfo(issn, key)

    # === Miscellaneous ===
    def yview(self, canvas, *args):
        if canvas.yview() == (0.0, 1.0): return
        canvas.yview(*args)

    def valInteger(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        for char in value_if_allowed:
            if not char.isdigit(): return False
        return True

    def valIssn(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if len(value_if_allowed) > 9: return False
        for i, char in enumerate(value_if_allowed):
            if i != 4 and not char.isdigit(): return False
            elif i == 4 and char != '-': return False
        return True

    def valEmail(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed.count('@') > 1: return False
        if len(value_if_allowed) and value_if_allowed[0] in '@.': return False
        return True

    def valDoi(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        prefix = value_if_allowed.split('/')[0]
        for char in prefix:
            if char not in '0123456789.': return False
        try:
            if prefix[0] != '1': return False
            if prefix[1] != '0': return False
            if prefix[2] != '.': return False
            if prefix[3] in '0.': return False
            if prefix[4] == '.': return False
            if prefix[5] == '.': return False
            if prefix[6] == '.': return False
        except IndexError:
            pass
        return True

    def valMonth(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        for char in value_if_allowed:
            if not char.isdigit(): return False
        if len(value_if_allowed) and int(value_if_allowed) > 12: return False
        return True

    def valDay(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        for char in value_if_allowed:
            if not char.isdigit(): return False
        if len(value_if_allowed) and int(value_if_allowed) > 31: return False
        return True

    def stringToColor(self, string):
        color_rgb = "{:+07x}".format(hash(string))[-6:]
        color_r = int(color_rgb[0:2], 16)
        color_g = int(color_rgb[2:4], 16)
        color_b = int(color_rgb[4:6], 16)

        color_r = color_r if color_r > 50 else color_r + 100
        color_g = color_g if color_g > 50 else color_g + 100
        color_b = color_b if color_b > 50 else color_b + 100
        color_rgb = "".join((hex(color_r)[2:], hex(color_g)[2:], hex(color_b)[2:]))

        return "#" + color_rgb


if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
