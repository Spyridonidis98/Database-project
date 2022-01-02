import tkinter as tk
from tkinter import ttk
import os
import webbrowser
from database_class import DataModel

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x800+100+100") # make 800x800 pixel window, 100 pixels from each side of the screen
        self.root.minsize(1232, 800)
        self.root.maxsize(1232, 800)
        self.root.tk.call("source", os.path.join("Azure-ttk-theme", "azure.tcl"))
        self.root.tk.call("set_theme", "light")
        self.showLoginScreen()
        
        self.db = DataModel("db_project.db")
        self.user = None
        self.magazines = None
        self.magazines_publications = None
        self.magazines_subjects = None
        self.magazines_editors = None

    # === Login ===
    def showLoginScreen(self):
        self.mainLoginFrame = ttk.Frame(self.root)
        self.mainLoginFrame.pack(fill = "both", expand = True)

        self.loginTitle = ttk.Label(self.mainLoginFrame, text = "Please login to use the app.", font = ("Arial", 20))
        self.loginTitle.pack(anchor = "s", expand = True, pady = 30, padx = 20)

        self.loginInfoFrame = ttk.Frame(self.mainLoginFrame)
        self.loginInfoFrame.pack(anchor = "n", expand = True)

        self.usernameLabel = ttk.Label(self.loginInfoFrame, text = "Username/Email:")
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
        self.loginButton.grid(row = 3, column = 0, columnspan = 2, pady = (0, 30))

        self.root.bind("<Return>", lambda event: self.submitLoginInfo())

    def destroyLoginScreen(self):
        self.mainLoginFrame.destroy()
        self.root.unbind("<Return>")

    def submitLoginInfo(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        self.user  = self.db.user_loggin(username, password)
        if self.user==False:
            self.errorLabel.config(text = "Wrong username/password!")
        elif self.user['User_type']=="reader":
            self.destroyLoginScreen()
            self.showReaderWindow()
        else:
            self.destroyLoginScreen()
            self.showPublisherWindow()
        

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

        self.displayNameLabel = ttk.Label(self.topBarFrame, text = "Display-Name", font = ("Arial", 20))
        self.displayNameLabel.grid(row = 0, column = 2, sticky = "e", padx = 10)

        self.topBarSeparator = ttk.Separator(self.topBarFrame)
        self.topBarSeparator.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = "ew", columnspan = 4)

        self.showSearch()

    def destroyReaderWindow(self):
        self.mainReaderWindowFrame.destroy()

    def showSearch(self):
        self.backLabel.config(text = "\u25c1")
        self.backLabel.unbind("<1>")
        self.actionTitle.config(text = "Search")

        self.searchScrollbar = ttk.Scrollbar(self.mainReaderWindowFrame)
        self.searchScrollbar.pack(side="right", fill="y")

        self.searchCanvas = tk.Canvas(self.mainReaderWindowFrame, yscrollcommand = self.searchScrollbar.set, highlightthickness = 0)
        self.searchCanvas.pack(fill = "both", expand = True)
        self.searchScrollbar.config(command = self.searchCanvas.yview)

        self.searchFrame = ttk.Frame(self.searchCanvas)
        self.searchCanvas.create_window((0, 0), window = self.searchFrame, anchor = "nw")
        self.searchFrame.bind("<Configure>", lambda e: self.searchCanvas.configure(scrollregion = self.searchCanvas.bbox("all")))

        self.searchBarFrame = ttk.Frame(self.searchFrame)
        self.searchBarFrame.pack(fill = "x", side = "top")

        self.searchBarFrame.grid_columnconfigure(3, minsize = 100)      

        self.searchBarEntry = ttk.Entry(self.searchBarFrame, width = 156)
        self.searchBarEntry.grid(row = 0, column = 0, padx = 5, columnspan = 4)

        self.searchBarButton = ttk.Button(self.searchBarFrame, text = "Search", command = self.showSearchResults)
        self.searchBarButton.grid(row = 0, column = 4, padx = 5, pady = 5)

        self.type = tk.StringVar(self.root, "Magazine")

        self.typeMagazineRadio = ttk.Radiobutton(self.searchBarFrame, text = "Magazine", variable = self.type, value = "Magazine")
        self.typeMagazineRadio.grid(row = 1, column = 0, sticky = "e")

        self.typeArticleRadio = ttk.Radiobutton(self.searchBarFrame, text = "Article", variable = self.type, value = "Article")
        self.typeArticleRadio.grid(row = 1, column = 1, sticky = "w")

        self.searchBarSubjectLabel = ttk.Label(self.searchBarFrame, text = "Subject:")
        self.searchBarSubjectLabel.grid(row = 1, column = 2, sticky = "e")

        self.searchBarSubject = tk.StringVar(self.root, "Any")

        self.searchBarSubjectEntry = ttk.OptionMenu(self.searchBarFrame, self.searchBarSubject, *("", "Any", "Subject 1", "Subject 2", "Subject 3"))
        self.searchBarSubjectEntry.grid(row = 1, column = 3, sticky = "w", pady = (0, 5))

        self.searchResultsFrame = ttk.Frame(self.searchFrame)
        self.searchResultsFrame.pack(fill = "both", expand = True)

    def destroySearch(self):
        self.searchCanvas.destroy()
        self.searchScrollbar.destroy()

    def showSearchResults(self):
        self.searchResultsFrame.destroy()
        self.searchResultsFrame = ttk.Frame(self.searchFrame)
        self.searchResultsFrame.pack(fill = "both", expand = True)

        results = [
            ("id1", "Title 1", 3.5),
            ("id2", "Title 2", 3),
            ("id3", "Title 3", 4),
            ("id4", "Title 4", 4.2)
        ]

        self.resultFrames = []
        self.resultTitleLabels = []
        self.resultRatingLabels = []
        for r in results:
            self.resultFrames.append(tk.Frame(self.searchResultsFrame, bg = "gray85"))
            self.resultFrames[-1].pack(fill = "x", pady = 2, padx = (2, 0))
            self.resultTitleLabels.append(tk.Label(self.resultFrames[-1], text = r[1], bg = "gray85", font = ("Arial", 14)))
            self.resultTitleLabels[-1].pack()
            self.resultRatingLabels.append(tk.Label(self.resultFrames[-1], text = "Rating: {:.2f}".format(r[2]), bg = "gray85"))
            self.resultRatingLabels[-1].pack()
            self.resultTitleLabels[-1].bind("<1>", lambda e, rid=r[0]: self.showResult(rid))
            self.resultRatingLabels[-1].bind("<1>", lambda e, rid=r[0]: self.showResult(rid))
            self.resultFrames[-1].bind("<1>", lambda e, rid=r[0]: self.showResult(rid))

    def showMagazine(self, issn):
        self.backLabel.config(text = "\u25c0")
        self.backLabel.unbind("<1>")
        self.backLabel.bind("<1>", lambda e: self.magazineToSearch())

        self.magazineScrollbar = ttk.Scrollbar(self.mainReaderWindowFrame)
        self.magazineScrollbar.pack(side="right", fill="y")

        self.magazineCanvas = tk.Canvas(self.mainReaderWindowFrame, yscrollcommand = self.magazineScrollbar.set, highlightthickness = 0)
        self.magazineCanvas.pack(fill = "both", expand = True)
        self.magazineScrollbar.config(command=self.magazineCanvas.yview)

        self.magazineFrame = ttk.Frame(self.magazineCanvas)
        self.magazineCanvas.create_window((0, 0), window = self.magazineFrame, anchor = "nw")
        self.magazineFrame.bind("<Configure>", lambda e: self.magazineCanvas.configure(scrollregion = self.magazineCanvas.bbox("all")))

        self.magazineInfoFrame = ttk.Frame(self.magazineFrame)
        self.magazineInfoFrame.pack(fill = "x", expand = False)

        # self.magazineInfoFrame.grid_columnconfigure(0, weight = 1)
        # self.magazineInfoFrame.grid_columnconfigure(1, weight = 1)

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

        self.magazineLabelFrame = ttk.Frame(self.magazineFrame)
        self.magazineLabelFrame.pack(fill = "x", expand = False)

        self.magazinePublicationsLabel = ttk.Label(self.magazineLabelFrame, text = "Publications:", font = ("Arial", 20))
        self.magazinePublicationsLabel.grid(row = 0, column = 0, sticky = "w", padx = (5, 1025))

        self.publicationsButtonsFrame = ttk.Frame(self.magazineFrame)
        self.publicationsButtonsFrame.pack(fill = "x", expand = False)


        self.actionTitle.config(text = issn)

        # fetch info
        title = "Magazine Title" # from sql
        self.magazineTitleEntry.config(text = title)

        self.magazineISSNEntry.config(text = issn)

        subjects = ["Subject 1", "Subject 3"] # from sql
        self.magazineSubjectEntries[0].config(text = subjects[0])
        for s in subjects[1:]:
            self.magazineAddSubject()
            self.magazineSubjectEntries[-1].config(text = s)

        editors = ["Editor 3", "Editor 1", "Editor 2"] # from sql
        self.magazineEditorEntries[0].config(text = editors[0])
        for e in editors[1:]:
            self.magazineAddEditor()
            self.magazineEditorEntries[-1].config(text = e)

        # fetch publications
        publications = [
            ("01,01",),
            ("01,02",),
            ("01,03",),
            ("02,01",),
            ("02,02",)
        ]

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
        self.publicationScrollbar.pack(side="right", fill="y")

        self.publicationCanvas = tk.Canvas(self.mainReaderWindowFrame, yscrollcommand = self.publicationScrollbar.set, highlightthickness = 0)
        self.publicationCanvas.pack(fill = "both", expand = True)
        self.publicationScrollbar.config(command=self.publicationCanvas.yview)

        self.publicationFrame = ttk.Frame(self.publicationCanvas)
        self.publicationCanvas.create_window((0, 0), window = self.publicationFrame, anchor = "nw")
        self.publicationFrame.bind("<Configure>", lambda e: self.publicationCanvas.configure(scrollregion = self.publicationCanvas.bbox("all")))

        self.publicationInfoFrame = ttk.Frame(self.publicationFrame)
        self.publicationInfoFrame.pack(fill = "x", expand = False)

        # self.publicationInfoFrame.grid_columnconfigure(0, weight = 1)
        # self.publicationInfoFrame.grid_columnconfigure(1, weight = 1)

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

        # fetch info
        self.publicationVolumeEntry.config(text = key.split(",")[0])

        self.publicationIssueEntry.config(text = key.split(",")[1])

        year = 2021
        self.publicationYearEntry.config(text = year)

        month = 12
        self.publicationMonthEntry.config(text = month)

        editors = ["Editor 3", "Editor 2"] # from sql
        self.publicationEditorEntries[0].config(text = editors[0])
        for e in editors[1:]:
            self.publicationAddEditor()
            self.publicationEditorEntries[-1].config(text = e)

        # fetch articles
        articles = [
            ("doi:10.1000/181", "Article 1"),
            ("doi:10.1000/182", "Article 2"),
            ("doi:10.1000/183", "Article 3"),
            ("doi:10.1000/184", "Article 4"),
            ("doi:10.1000/185", "Article 5"),
            ("doi:10.1000/186", "Article 6")
        ]

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
        self.articleScrollbar.pack(side="right", fill="y")

        self.articleCanvas = tk.Canvas(self.mainReaderWindowFrame, yscrollcommand = self.articleScrollbar.set, highlightthickness = 0)
        self.articleCanvas.pack(fill = "both", expand = True)
        self.articleScrollbar.config(command=self.articleCanvas.yview)

        self.articleFrame = ttk.Frame(self.articleCanvas)
        self.articleCanvas.create_window((0, 0), window = self.articleFrame, anchor = "nw")
        self.articleFrame.bind("<Configure>", lambda e: self.articleCanvas.configure(scrollregion = self.articleCanvas.bbox("all")))

        self.articleInfoFrame = ttk.Frame(self.articleFrame)
        self.articleInfoFrame.pack(fill = "x", expand = False)

        # self.articleInfoFrame.grid_columnconfigure(0, weight = 1)
        # self.articleInfoFrame.grid_columnconfigure(1, weight = 1)

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

        self.articleAuthorEntries.append(ttk.Label(self.articleInfoFrame))
        self.articleAuthorEntries[0].grid(row = 10, column = 1, sticky = "w")

        self.articleCitationLabel = ttk.Label(self.articleInfoFrame, text = "Citation:")
        self.articleCitationLabel.grid(row = 11, column = 0, sticky = "e")

        self.articleCitationEntries = []

        self.articleCitationEntries.append(ttk.Label(self.articleInfoFrame))
        self.articleCitationEntries[0].grid(row = 11, column = 1, sticky = "w")


        self.actionTitle.config(text = doi)

        # fetch info
        self.articleDOIEntry.config(text = doi)
        
        title = "Article Title" # from sql
        self.articleTitleEntry.config(text = title)

        url = "https://www.researchgate.net/profile/Nikoleta-Yiannoutsou/publication/232806353_A_Review_of_Mobile_Location-based_Games_for_Learning_across_Physical_and_Virtual_Spaces/links/53d0c9090cf2f7e53cfb9b9f/A-Review-of-Mobile-Location-based-Games-for-Learning-across-Physical-and-Virtual-Spaces.pdf"
        self.articleURLEntry.config(text = url)
        # self.articleURLEntry.bind("<1>", lambda e: os.startfile(url)) # only works on windows
        self.articleURLEntry.bind("<1>", lambda e: webbrowser.open(url, new = 2))

        year = 2021
        self.articleYearEntry.config(text = year)

        month = 12
        self.articleMonthEntry.config(text = month)

        day = 25
        self.articleDayEntry.config(text = day)

        pages = 101
        self.articlePagesEntry.config(text = pages)

        language = "Dutch"
        self.articleLanguageEntry.config(text = language)

        is_free = True
        self.is_free.set(is_free)

        subjects = ["Subject 3", "Subject 2"] # from sql
        self.articleSubjectEntries[0].config(text = subjects[0])
        for s in subjects[1:]:
            self.articleAddSubject()
            self.articleSubjectEntries[-1].config(text = s)

        authors = ["Author 2"] # from sql
        self.articleAuthorEntries[0].config(text = authors[0])
        for a in authors[1:]:
            self.articleAddAuthor()
            self.articleAuthorEntries[-1].config(text = a)

        citations = ["Article 1", "Article 3", "Article 2"] # from sql
        self.articleCitationEntries[0].config(text = citations[0])
        for c in citations[1:]:
            self.articleAddCitation()
            self.articleCitationEntries[-1].config(text = c)

    def destroyArticle(self):
        self.articleCanvas.destroy()
        self.articleScrollbar.destroy()

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

        self.articleCitationLabel.grid(row = self.articleCitationLabel.grid_info()["row"] + 1, column = 0, sticky = "e")

        for e in self.articleCitationEntries:
            e.grid(row = e.grid_info()["row"] + 1, column = 1, sticky = "w")

    def articleAddAuthor(self):
        self.articleAuthorEntries.append(ttk.Label(self.articleInfoFrame))
        self.articleAuthorEntries[-1].grid(row = self.articleAuthorEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

        self.articleCitationLabel.grid(row = self.articleCitationLabel.grid_info()["row"] + 1, column = 0, sticky = "e")

        for e in self.articleCitationEntries:
            e.grid(row = e.grid_info()["row"] + 1, column = 1, sticky = "w")

    def articleAddCitation(self):
        self.articleCitationEntries.append(ttk.Label(self.articleInfoFrame))
        self.articleCitationEntries[-1].grid(row = self.articleCitationEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

    # --- Window Transitions ---
    def showResult(self, rid):
        self.destroySearch()
        if self.type.get() == "Magazine":
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

        self.displayNameLabel = ttk.Label(self.topBarFrame, text = "Display-Name", font = ("Arial", 20))
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
        self.magazinesScrollbar.pack(side="right", fill="y")

        self.magazinesCanvas = tk.Canvas(self.mainPublisherWindowFrame, yscrollcommand = self.magazinesScrollbar.set, highlightthickness = 0)
        self.magazinesCanvas.pack(fill = "both", expand = True)
        self.magazinesScrollbar.config(command = self.magazinesCanvas.yview)

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

        #fetch publishers magazines
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
        self.magazineInfoScrollbar.pack(side="right", fill="y")

        self.magazineInfoCanvas = tk.Canvas(self.mainPublisherWindowFrame, yscrollcommand = self.magazineInfoScrollbar.set, highlightthickness = 0)
        self.magazineInfoCanvas.pack(fill = "both", expand = True)
        self.magazineInfoScrollbar.config(command=self.magazineInfoCanvas.yview)

        self.magazineInfoFrame = ttk.Frame(self.magazineInfoCanvas)
        self.magazineInfoCanvas.create_window((0, 0), window = self.magazineInfoFrame, anchor = "nw")
        self.magazineInfoFrame.bind("<Configure>", lambda e: self.magazineInfoCanvas.configure(scrollregion = self.magazineInfoCanvas.bbox("all")))

        self.magazineInfoInfoFrame = ttk.Frame(self.magazineInfoFrame)
        self.magazineInfoInfoFrame.pack(fill = "x", expand = False)

        # self.magazineInfoInfoFrame.grid_columnconfigure(0, weight = 1)
        # self.magazineInfoInfoFrame.grid_columnconfigure(1, weight = 1)

        self.magazineInfoTitleLabel = ttk.Label(self.magazineInfoInfoFrame, text = "Title:")
        self.magazineInfoTitleLabel.grid(row = 0, column = 0, sticky = "e")

        self.magazineInfoTitleEntry = ttk.Entry(self.magazineInfoInfoFrame)
        self.magazineInfoTitleEntry.grid(row = 0, column = 1, sticky = "w")

        self.magazineInfoISSNLabel = ttk.Label(self.magazineInfoInfoFrame, text = "ISSN:")
        self.magazineInfoISSNLabel.grid(row = 1, column = 0, sticky = "e")

        self.magazineInfoISSNEntry = ttk.Entry(self.magazineInfoInfoFrame)
        self.magazineInfoISSNEntry.grid(row = 1, column = 1, sticky = "w")

        self.magazineInfoSubjectLabel = ttk.Label(self.magazineInfoInfoFrame, text = "Subject:")
        self.magazineInfoSubjectLabel.grid(row = 2, column = 0, sticky = "e")

        self.magazineInfoSubjectEntries = []
        self.magazineInfoSubjectRemoveButtons = [None]

        self.magazineInfoSubjectEntries.append(ttk.Combobox(self.magazineInfoInfoFrame, values = ("Subject 1", "Subject 2", "Subject 3")))
        self.magazineInfoSubjectEntries[0].grid(row = 2, column = 1, sticky = "w")

        self.magazineInfoSubjectButton = ttk.Button(self.magazineInfoInfoFrame, text = "Add Subject", command = self.magazineInfoAddSubject)
        self.magazineInfoSubjectButton.grid(row = 3, column = 1, sticky = "w")

        self.magazineInfoEditorLabel = ttk.Label(self.magazineInfoInfoFrame, text = "Editor:")
        self.magazineInfoEditorLabel.grid(row = 4, column = 0, sticky = "e")

        self.magazineInfoEditorEntries = []
        self.magazineInfoEditorRemoveButtons = [None]

        self.magazineInfoEditorEntries.append(ttk.Combobox(self.magazineInfoInfoFrame, values = ("Editor 1", "Editor 2", "Editor 3")))
        self.magazineInfoEditorEntries[0].grid(row = 4, column = 1, sticky = "w")

        self.magazineInfoEditorButton = ttk.Button(self.magazineInfoInfoFrame, text = "Add Editor", command = self.magazineInfoAddEditor)
        self.magazineInfoEditorButton.grid(row = 5, column = 1, sticky = "w")

        self.magazineInfoLabelFrame = ttk.Frame(self.magazineInfoFrame)
        self.magazineInfoLabelFrame.pack(fill = "x", expand = False)

        self.magazineInfoPublicationsLabel = ttk.Label(self.magazineInfoLabelFrame, text = "Publications:", font = ("Arial", 20))
        self.magazineInfoPublicationsLabel.grid(row = 0, column = 0, sticky = "w", padx = (5, 1025))

        self.magazineInfoAddLabel = ttk.Label(self.magazineInfoLabelFrame, text = "+", font = ("Arial", 30))
        self.magazineInfoAddLabel.grid(row = 0, column = 1, sticky = "e", padx = 5)
        self.magazineInfoAddLabel.bind("<1>", lambda e: self.magazineInfoToPublicationInfo("<new>"))

        self.publicationsButtonsFrame = ttk.Frame(self.magazineInfoFrame)
        self.publicationsButtonsFrame.pack(fill = "x", expand = False)

        if issn == "<new>":
            self.actionTitle.config(text = "New Magazine")
        else:
            self.actionTitle.config(text = issn)

            # fetch mag
            mag = None
            for m in self.magazines:
                if m["Issn"] == issn:
                    mag = m

            title = mag["Title"]
                    
            self.magazineInfoTitleEntry.insert(0, title)

            self.magazineInfoISSNEntry.insert(0, issn)

            #fetch subjects
            self.magazines_subjects = self.db.get_magazines_subjects(mag["Issn"])
            subjects = []
            for s in self.magazines_subjects:
                subjects.append(s)

            self.magazineInfoSubjectEntries[0].set(subjects[0])
            for s in subjects[1:]:
                self.magazineInfoAddSubject()
                self.magazineInfoSubjectEntries[-1].set(s)

            #fetch mags editors 
            editors = [] 
            self.magazines_editors = self.db.get_magazines_editors(mag["Issn"])
            for e in self.magazines_editors:
                editors.append(e["Fname"]+" "+e["Lname"])

            self.magazineInfoEditorEntries[0].set(editors[0])
            for e in editors[1:]:
                self.magazineInfoAddEditor()
                self.magazineInfoEditorEntries[-1].set(e)

            # fetch magazines publications
            self.magazines_publications = self.db.get_magazines_publications(issn)
            publications = []
            for pub in self.magazines_publications:
                publications.append((f"{pub['Volume']},{pub['Issue']}",))


            self.publicationButtons = []
            for i, p in enumerate(publications):
                publicationButton = tk.Button(self.publicationsButtonsFrame, text = p[0], height = 3, width = 40, wraplength = 250, relief = "groove", bd = 5, bg = self.stringToColor(p[0]), command = lambda key=p[0]: self.magazineInfoToPublicationInfo(key))
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
        self.publicationInfoScrollbar.pack(side="right", fill="y")

        self.publicationInfoCanvas = tk.Canvas(self.mainPublisherWindowFrame, yscrollcommand = self.publicationInfoScrollbar.set, highlightthickness = 0)
        self.publicationInfoCanvas.pack(fill = "both", expand = True)
        self.publicationInfoScrollbar.config(command=self.publicationInfoCanvas.yview)

        self.publicationInfoFrame = ttk.Frame(self.publicationInfoCanvas)
        self.publicationInfoCanvas.create_window((0, 0), window = self.publicationInfoFrame, anchor = "nw")
        self.publicationInfoFrame.bind("<Configure>", lambda e: self.publicationInfoCanvas.configure(scrollregion = self.publicationInfoCanvas.bbox("all")))

        self.publicationInfoInfoFrame = ttk.Frame(self.publicationInfoFrame)
        self.publicationInfoInfoFrame.pack(fill = "x", expand = False)

        # self.publicationInfoInfoFrame.grid_columnconfigure(0, weight = 1)
        # self.publicationInfoInfoFrame.grid_columnconfigure(1, weight = 1)

        self.publicationInfoVolumeLabel = ttk.Label(self.publicationInfoInfoFrame, text = "Volume:")
        self.publicationInfoVolumeLabel.grid(row = 0, column = 0, sticky = "e")

        self.publicationInfoVolumeEntry = ttk.Entry(self.publicationInfoInfoFrame)
        self.publicationInfoVolumeEntry.grid(row = 0, column = 1, sticky = "w")

        self.publicationInfoIssueLabel = ttk.Label(self.publicationInfoInfoFrame, text = "Issue:")
        self.publicationInfoIssueLabel.grid(row = 1, column = 0, sticky = "e")

        self.publicationInfoIssueEntry = ttk.Entry(self.publicationInfoInfoFrame)
        self.publicationInfoIssueEntry.grid(row = 1, column = 1, sticky = "w")

        self.publicationInfoYearLabel = ttk.Label(self.publicationInfoInfoFrame, text = "Publication Year:")
        self.publicationInfoYearLabel.grid(row = 2, column = 0, sticky = "e")

        self.publicationInfoYearEntry = ttk.Entry(self.publicationInfoInfoFrame)
        self.publicationInfoYearEntry.grid(row = 2, column = 1, sticky = "w")

        self.publicationInfoMonthLabel = ttk.Label(self.publicationInfoInfoFrame, text = "Publication Month:")
        self.publicationInfoMonthLabel.grid(row = 3, column = 0, sticky = "e")

        self.publicationInfoMonthEntry = ttk.Entry(self.publicationInfoInfoFrame)
        self.publicationInfoMonthEntry.grid(row = 3, column = 1, sticky = "w")

        self.publicationInfoEditorLabel = ttk.Label(self.publicationInfoInfoFrame, text = "Editor:")
        self.publicationInfoEditorLabel.grid(row = 4, column = 0, sticky = "e")

        self.publicationInfoEditorEntries = []
        self.publicationInfoEditorRemoveButtons = [None]

        self.publicationInfoEditorEntries.append(ttk.Combobox(self.publicationInfoInfoFrame, values = ("Editor 1", "Editor 2", "Editor 3")))
        self.publicationInfoEditorEntries[0].grid(row = 4, column = 1, sticky = "w")

        self.publicationInfoEditorButton = ttk.Button(self.publicationInfoInfoFrame, text = "Add Editor", command = self.publicationInfoAddEditor)
        self.publicationInfoEditorButton.grid(row = 5, column = 1, sticky = "w")

        self.publicationInfoLabelFrame = ttk.Frame(self.publicationInfoFrame)
        self.publicationInfoLabelFrame.pack(fill = "x", expand = False)

        self.publicationInfoArticlesLabel = ttk.Label(self.publicationInfoLabelFrame, text = "Articles:", font = ("Arial", 20))
        self.publicationInfoArticlesLabel.grid(row = 0, column = 0, sticky = "w", padx = (5, 1080))

        self.publicationInfoAddLabel = ttk.Label(self.publicationInfoLabelFrame, text = "+", font = ("Arial", 30))
        self.publicationInfoAddLabel.grid(row = 0, column = 1, sticky = "e", padx = 5)
        self.publicationInfoAddLabel.bind("<1>", lambda e: self.publicationInfoToArticleInfo(issn, "<new>"))

        self.articlesButtonsFrame = ttk.Frame(self.publicationInfoFrame)
        self.articlesButtonsFrame.pack(fill = "x", expand = False)

        if key == "<new>":
            self.actionTitle.config(text = "New Publication")
        else:
            self.actionTitle.config(text = key)

            # fetch info
            
            self.publicationInfoVolumeEntry.insert(0, key.split(",")[0])

            self.publicationInfoIssueEntry.insert(0, key.split(",")[1])

            year = "to check"
            self.publicationInfoYearEntry.insert(0, year)

            month = "to check"
            self.publicationInfoMonthEntry.insert(0, month)

            pub_editors = self.db.get_publications_editors(issn, key.split(",")[0], key.split(",")[1])
            editors = []
            for e in pub_editors:
                editors.append(e["Fname"]+" "+e["Lname"])

            self.publicationInfoEditorEntries[0].set(editors[0])
            for e in editors[1:]:
                self.publicationInfoAddEditor()
                self.publicationInfoEditorEntries[-1].set(e)

            # fetch articles
            pub_articles = self.db.get_publications_articles(issn, key.split(",")[0], key.split(",")[1])
            articles = []
            for p in pub_articles:
                articles.append((p["Doi"], p["Title"]))

            self.articleButtons = []
            for i, a in enumerate(articles):
                articleButton = tk.Button(self.articlesButtonsFrame, text = a[1], height = 3, width = 40, wraplength = 250, relief = "groove", bd = 5, bg = self.stringToColor(a[0]), command = lambda doi=a[0]: self.publicationInfoToArticleInfo(issn, doi))
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
        self.articleInfoScrollbar.pack(side="right", fill="y")

        self.articleInfoCanvas = tk.Canvas(self.mainPublisherWindowFrame, yscrollcommand = self.articleInfoScrollbar.set, highlightthickness = 0)
        self.articleInfoCanvas.pack(fill = "both", expand = True)
        self.articleInfoScrollbar.config(command=self.articleInfoCanvas.yview)

        self.articleInfoFrame = ttk.Frame(self.articleInfoCanvas)
        self.articleInfoCanvas.create_window((0, 0), window = self.articleInfoFrame, anchor = "nw")
        self.articleInfoFrame.bind("<Configure>", lambda e: self.articleInfoCanvas.configure(scrollregion = self.articleInfoCanvas.bbox("all")))

        self.articleInfoInfoFrame = ttk.Frame(self.articleInfoFrame)
        self.articleInfoInfoFrame.pack(fill = "x", expand = False)

        # self.articleInfoInfoFrame.grid_columnconfigure(0, weight = 1)
        # self.articleInfoInfoFrame.grid_columnconfigure(1, weight = 1)

        self.articleInfoDOILabel = ttk.Label(self.articleInfoInfoFrame, text = "DOI:")
        self.articleInfoDOILabel.grid(row = 0, column = 0, sticky = "e")

        self.articleInfoDOIEntry = ttk.Entry(self.articleInfoInfoFrame)
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

        self.articleInfoYearEntry = ttk.Entry(self.articleInfoInfoFrame)
        self.articleInfoYearEntry.grid(row = 3, column = 1, sticky = "w")

        self.articleInfoMonthLabel = ttk.Label(self.articleInfoInfoFrame, text = "Publication Month:")
        self.articleInfoMonthLabel.grid(row = 4, column = 0, sticky = "e")

        self.articleInfoMonthEntry = ttk.Entry(self.articleInfoInfoFrame)
        self.articleInfoMonthEntry.grid(row = 4, column = 1, sticky = "w")

        self.articleInfoDayLabel = ttk.Label(self.articleInfoInfoFrame, text = "Publication Day:")
        self.articleInfoDayLabel.grid(row = 5, column = 0, sticky = "e")

        self.articleInfoDayEntry = ttk.Entry(self.articleInfoInfoFrame)
        self.articleInfoDayEntry.grid(row = 5, column = 1, sticky = "w")

        self.articleInfoPagesLabel = ttk.Label(self.articleInfoInfoFrame, text = "Pages:")
        self.articleInfoPagesLabel.grid(row = 6, column = 0, sticky = "e")

        self.articleInfoPagesEntry = ttk.Entry(self.articleInfoInfoFrame)
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
        self.articleInfoSubjectRemoveButtons = [None]

        self.articleInfoSubjectEntries.append(ttk.Combobox(self.articleInfoInfoFrame, values = ("Subject 1", "Subject 2", "Subject 3")))
        self.articleInfoSubjectEntries[0].grid(row = 9, column = 1, sticky = "w")

        self.articleInfoSubjectButton = ttk.Button(self.articleInfoInfoFrame, text = "Add Subject", command = self.articleInfoAddSubject)
        self.articleInfoSubjectButton.grid(row = 10, column = 1, sticky = "w")

        self.articleInfoAuthorLabel = ttk.Label(self.articleInfoInfoFrame, text = "Author:")
        self.articleInfoAuthorLabel.grid(row = 11, column = 0, sticky = "e")

        self.articleInfoAuthorEntries = []
        self.articleInfoAuthorRemoveButtons = [None]

        self.articleInfoAuthorEntries.append(ttk.Combobox(self.articleInfoInfoFrame, values = ("Author 1", "Author 2", "Author 3")))
        self.articleInfoAuthorEntries[0].grid(row = 11, column = 1, sticky = "w")

        self.articleInfoAuthorButton = ttk.Button(self.articleInfoInfoFrame, text = "Add Author", command = self.articleInfoAddAuthor)
        self.articleInfoAuthorButton.grid(row = 12, column = 1, sticky = "w")

        self.articleInfoCitationLabel = ttk.Label(self.articleInfoInfoFrame, text = "Citation:")
        self.articleInfoCitationLabel.grid(row = 13, column = 0, sticky = "e")

        self.articleInfoCitationEntries = []
        self.articleInfoCitationRemoveButtons = [None]

        self.articleInfoCitationEntries.append(ttk.Combobox(self.articleInfoInfoFrame, values = ("Article 1", "Article 2", "Article 3")))
        self.articleInfoCitationEntries[0].grid(row = 13, column = 1, sticky = "w")

        self.articleInfoCitationButton = ttk.Button(self.articleInfoInfoFrame, text = "Add Citation", command = self.articleInfoAddCitation)
        self.articleInfoCitationButton.grid(row = 14, column = 1, sticky = "w")

        if doi == "<new>":
            self.actionTitle.config(text = "New Article")
        else:
            article = self.db.get_article(doi)

            self.actionTitle.config(text = doi)

            # fetch article info
            self.articleInfoDOIEntry.insert(0, doi)
            
            title = article["Title"] # from sql
            self.articleInfoTitleEntry.insert(0, title)

            url = article["Link_to_article"]
            self.articleInfoURLEntry.insert(0, url)

            year = article["Publication_date"].split("/")[2]
            self.articleInfoYearEntry.insert(0, year)

            month = article["Publication_date"].split("/")[1]
            self.articleInfoMonthEntry.insert(0, month)

            day = article["Publication_date"].split("/")[0]
            self.articleInfoDayEntry.insert(0, day)

            pages = article["No_pages"]
            self.articleInfoPagesEntry.insert(0, pages)

            language = article["Language"]
            self.articleInfoLanguageEntry.insert(0, language)


            is_free = False
            if article["Is_free"]==1:
                is_free = True

            self.is_free.set(is_free)

            article_subs = self.db.get_articles_subjects(doi)
            subjects = [] # from sql
            for s in article_subs:
                subjects.append(s)
            if len(subjects)==0:
                subjects.append("None to do")

            self.articleInfoSubjectEntries[0].set(subjects[0])
            for s in subjects[1:]:
                self.articleInfoAddSubject()
                self.articleInfoSubjectEntries[-1].set(s)

            art_authors = self.db.get_articles_authors(doi)
            authors = [] # from sql
            for a in art_authors:
                authors.append(a["Fname"]+" "+a["Lname"])

            self.articleInfoAuthorEntries[0].set(authors[0])
            for a in authors[1:]:
                self.articleInfoAddAuthor()
                self.articleInfoAuthorEntries[-1].set(a)

            citations = ["To do"] # from sql
            self.articleInfoCitationEntries[0].set(citations[0])
            for c in citations[1:]:
                self.articleInfoAddCitation()
                self.articleInfoCitationEntries[-1].set(c)

    def destroyArticleInfo(self):
        self.articleInfoCanvas.destroy()
        self.articleInfoScrollbar.destroy()

    # --- Add/Remove Fields ---
    def magazineInfoAddSubject(self):
        self.magazineInfoSubjectEntries.append(ttk.Combobox(self.magazineInfoInfoFrame, values = ("Subject 1", "Subject 2", "Subject 3")))
        self.magazineInfoSubjectEntries[-1].grid(row = self.magazineInfoSubjectEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

        self.magazineInfoSubjectRemoveButtons.append(tk.Button(self.magazineInfoInfoFrame, text = "x", command = lambda entry=self.magazineInfoSubjectEntries[-1]: self.magazineInfoRemoveSubject(entry)))
        self.magazineInfoSubjectRemoveButtons[-1].grid(row = self.magazineInfoSubjectEntries[-1].grid_info()["row"], column = 2, sticky = "w")

        self.magazineInfoSubjectButton.grid(row = self.magazineInfoSubjectButton.grid_info()["row"] + 1, column = 1, sticky = "w")

        self.magazineInfoEditorLabel.grid(row = self.magazineInfoEditorLabel.grid_info()["row"] + 1, column = 0, sticky = "e")

        for e in self.magazineInfoEditorEntries:
            e.grid(row = e.grid_info()['row'] + 1, column = 1, sticky = "w")

        for e in self.magazineInfoEditorRemoveButtons[1:]:
            e.grid(row = e.grid_info()['row'] + 1, column = 2, sticky = "w")

        self.magazineInfoEditorButton.grid(row = self.magazineInfoEditorButton.grid_info()["row"] + 1, column = 1, sticky = "w")

    def magazineInfoRemoveSubject(self, entry):
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

        for e in self.magazineInfoEditorRemoveButtons[1:]:
            e.grid(row = e.grid_info()['row'] - 1, column = 2, sticky = "w")

        self.magazineInfoEditorButton.grid(row = self.magazineInfoEditorButton.grid_info()["row"] - 1, column = 1, sticky = "w")

    def magazineInfoAddEditor(self):
        self.magazineInfoEditorEntries.append(ttk.Combobox(self.magazineInfoInfoFrame, values = ("Editor 1", "Editor 2", "Editor 3")))
        self.magazineInfoEditorEntries[-1].grid(row = self.magazineInfoEditorEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

        self.magazineInfoEditorRemoveButtons.append(tk.Button(self.magazineInfoInfoFrame, text = "x", command = lambda entry=self.magazineInfoEditorEntries[-1]: self.magazineInfoRemoveEditor(entry)))
        self.magazineInfoEditorRemoveButtons[-1].grid(row = self.magazineInfoEditorEntries[-1].grid_info()["row"], column = 2, sticky = "w")

        self.magazineInfoEditorButton.grid(row = self.magazineInfoEditorButton.grid_info()["row"] + 1, column = 1, sticky = "w")

    def magazineInfoRemoveEditor(self, entry):
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

    def publicationInfoAddEditor(self):
        self.publicationInfoEditorEntries.append(ttk.Combobox(self.publicationInfoInfoFrame, values = ("Editor 1", "Editor 2", "Editor 3")))
        self.publicationInfoEditorEntries[-1].grid(row = self.publicationInfoEditorEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

        self.publicationInfoEditorRemoveButtons.append(tk.Button(self.publicationInfoInfoFrame, text = "x", command = lambda entry=self.publicationInfoEditorEntries[-1]: self.publicationInfoRemoveEditor(entry)))
        self.publicationInfoEditorRemoveButtons[-1].grid(row = self.publicationInfoEditorEntries[-1].grid_info()["row"], column = 2, sticky = "w")

        self.publicationInfoEditorButton.grid(row = self.publicationInfoEditorButton.grid_info()["row"] + 1, column = 1, sticky = "w")

    def publicationInfoRemoveEditor(self, entry):
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
        self.articleInfoSubjectEntries.append(ttk.Combobox(self.articleInfoInfoFrame, values = ("Subject 1", "Subject 2", "Subject 3")))
        self.articleInfoSubjectEntries[-1].grid(row = self.articleInfoSubjectEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

        self.articleInfoSubjectRemoveButtons.append(tk.Button(self.articleInfoInfoFrame, text = "x", command = lambda entry=self.articleInfoSubjectEntries[-1]: self.articleInfoRemoveSubject(entry)))
        self.articleInfoSubjectRemoveButtons[-1].grid(row = self.articleInfoSubjectEntries[-1].grid_info()["row"], column = 2, sticky = "w")

        self.articleInfoSubjectButton.grid(row = self.articleInfoSubjectButton.grid_info()["row"] + 1, column = 1, sticky = "w")

        self.articleInfoAuthorLabel.grid(row = self.articleInfoAuthorLabel.grid_info()["row"] + 1, column = 0, sticky = "e")

        for e in self.articleInfoAuthorEntries:
            e.grid(row = e.grid_info()["row"] + 1, column = 1, sticky = "w")

        for e in self.articleInfoAuthorRemoveButtons[1:]:
            e.grid(row = e.grid_info()["row"] + 1, column = 2, sticky = "w")

        self.articleInfoAuthorButton.grid(row = self.articleInfoAuthorButton.grid_info()["row"] + 1, column = 1, sticky = "w")

        self.articleInfoCitationLabel.grid(row = self.articleInfoCitationLabel.grid_info()["row"] + 1, column = 0, sticky = "e")

        for e in self.articleInfoCitationEntries:
            e.grid(row = e.grid_info()["row"] + 1, column = 1, sticky = "w")

        for e in self.articleInfoCitationRemoveButtons[1:]:
            e.grid(row = e.grid_info()["row"] + 1, column = 2, sticky = "w")

        self.articleInfoCitationButton.grid(row = self.articleInfoCitationButton.grid_info()["row"] + 1, column = 1, sticky = "w")

    def articleInfoRemoveSubject(self, entry):
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

        for e in self.articleInfoAuthorRemoveButtons[1:]:
            e.grid(row = e.grid_info()['row'] - 1, column = 2, sticky = "w")

        self.articleInfoAuthorButton.grid(row = self.articleInfoAuthorButton.grid_info()["row"] - 1, column = 1, sticky = "w")

        self.articleInfoCitationLabel.grid(row = self.articleInfoCitationLabel.grid_info()["row"] - 1, column = 0, sticky = "e")

        for e in self.articleInfoCitationEntries:
            e.grid(row = e.grid_info()['row'] - 1, column = 1, sticky = "w")

        for e in self.articleInfoCitationRemoveButtons[1:]:
            e.grid(row = e.grid_info()['row'] - 1, column = 2, sticky = "w")

        self.articleInfoCitationButton.grid(row = self.articleInfoCitationButton.grid_info()["row"] - 1, column = 1, sticky = "w")

    def articleInfoAddAuthor(self):
        self.articleInfoAuthorEntries.append(ttk.Combobox(self.articleInfoInfoFrame, values = ("Author 1", "Author 2", "Author 3")))
        self.articleInfoAuthorEntries[-1].grid(row = self.articleInfoAuthorEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

        self.articleInfoAuthorRemoveButtons.append(tk.Button(self.articleInfoInfoFrame, text = "x", command = lambda entry=self.articleInfoAuthorEntries[-1]: self.articleInfoRemoveAuthor(entry)))
        self.articleInfoAuthorRemoveButtons[-1].grid(row = self.articleInfoAuthorEntries[-1].grid_info()["row"], column = 2, sticky = "w")

        self.articleInfoAuthorButton.grid(row = self.articleInfoAuthorButton.grid_info()["row"] + 1, column = 1, sticky = "w")

        self.articleInfoCitationLabel.grid(row = self.articleInfoCitationLabel.grid_info()["row"] + 1, column = 0, sticky = "e")

        for e in self.articleInfoCitationEntries:
            e.grid(row = e.grid_info()["row"] + 1, column = 1, sticky = "w")

        for e in self.articleInfoCitationRemoveButtons[1:]:
            e.grid(row = e.grid_info()["row"] + 1, column = 2, sticky = "w")

        self.articleInfoCitationButton.grid(row = self.articleInfoCitationButton.grid_info()["row"] + 1, column = 1, sticky = "w")

    def articleInfoRemoveAuthor(self, entry):
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

        for e in self.articleInfoCitationRemoveButtons[1:]:
            e.grid(row = e.grid_info()['row'] - 1, column = 2, sticky = "w")

        self.articleInfoCitationButton.grid(row = self.articleInfoCitationButton.grid_info()["row"] - 1, column = 1, sticky = "w")

    def articleInfoAddCitation(self):
        self.articleInfoCitationEntries.append(ttk.Combobox(self.articleInfoInfoFrame, values = ("Article 1", "Article 2", "Article 3")))
        self.articleInfoCitationEntries[-1].grid(row = self.articleInfoCitationEntries[-2].grid_info()["row"] + 1, column = 1, sticky = "w")

        self.articleInfoCitationRemoveButtons.append(tk.Button(self.articleInfoInfoFrame, text = "x", command = lambda entry=self.articleInfoCitationEntries[-1]: self.articleInfoRemoveCitation(entry)))
        self.articleInfoCitationRemoveButtons[-1].grid(row = self.articleInfoCitationEntries[-1].grid_info()["row"], column = 2, sticky = "w")

        self.articleInfoCitationButton.grid(row = self.articleInfoCitationButton.grid_info()["row"] + 1, column = 1, sticky = "w")

    def articleInfoRemoveCitation(self, entry):
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

    # --- Window Transitions ---
    def magazinesToMagazineInfo(self, issn):
        self.destroyMagazines()
        self.showMagazineInfo(issn)

    def magazineInfoToMagazines(self):
        self.destroyMagazineInfo()
        self.showMagazines()

    def magazineInfoToPublicationInfo(self, key):
        # save or update magazine info
        issn = self.magazineInfoISSNEntry.get()
        self.destroyMagazineInfo()
        self.showPublicationInfo(issn, key)

    def publicationInfoToMagazineInfo(self, issn):
        self.destroyPublicationInfo()
        self.showMagazineInfo(issn)

    def publicationInfoToArticleInfo(self, issn, doi):
        # save or update publication info
        volume = self.publicationInfoVolumeEntry.get()
        issue = self.publicationInfoIssueEntry.get()
        key = ",".join((volume, issue))
        self.destroyPublicationInfo()
        self.showArticleInfo(issn, key, doi)

    def articleInfoToPublicationInfo(self, issn, key):
        self.destroyArticleInfo()
        self.showPublicationInfo(issn, key)

    # === Miscellaneous ===
    def stringToColor(self, string):
        return "#" + "{:+07x}".format(hash(string))[-6:]


if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()