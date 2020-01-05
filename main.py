import requests
import dblp
from get_subjects import getSubjects
from affiliation_merger import affiliation_extracter
from levenshtein import levenshtein

#pylint: disable = no-member

class Publication:
    title = ""
    authors = []
    affiliation = {}
    year = ""
    journal = ""
    conf = ""
    subject = []
    subject_other = []
    subject_specific = []
    doi = ""
    references = []

    def __init__(self, title, authors, affiliation, year, journal, conf, subject, subject_other, subject_specific, doi, references):
        self.title = title
        self.authors = authors
        self.affiliation = affiliation
        self.year = year
        self.journal = journal
        self.conf = conf
        self.subject = subject
        self.subject_other = subject_other
        self.subject_specific = subject_specific
        self.doi = doi
        self.references = references
    
    def get_year(self):
        temp = str(self.year)
        if self.year is not None and temp is not "" and temp.isdigit():
            return int(temp)
        else:
            return 0

    def print_val(self):
        print(self.title)
        print("Authors: ", end="") 
        print(self.authors)
        print(self.affiliation)
        print("Year of Publication: ", end="")
        print(str(self.year))
        print("Journal Name: ",end="") 
        print(self.journal)  
        print("Conference Name: ",end="")
        print(self.conf)
        print("Subject Categories of the Conference/Journal:-")
        print("\tComputer Science: ", end="")
        print(self.subject)
        print("\tOthers: ", end="")
        print(self.subject_other)
        print("Subject Categories of the Publication: ", end='')
        print(self.subject_specific)             
        print(self.doi)
        print("Number of References: ", end="")
        print(len(self.references))
        #To print all the references
        # for item in self.references:
        #    print(item)
        print("***************************************************************************")

def getKey(PubObj):
    return PubObj.get_year()

def isSimilar(auth, pub1, pub2):
    sum = 0
    common = 0
    check = pub1.title + " ; " + pub2.title
    # Name of journal or conference
    if pub1.journal != "" and pub1.journal == pub2.journal:
        sum += 6
        check += " : 6jour"
    if pub1.conf != "" and pub1.conf == pub2.conf:
        sum += 6
        check += " : 6conf"
    # Name of Subjects
    if sum == 0 and pub1.subject != [''] and pub2.subject != ['']:
        temp = list(set(pub1.subject).intersection(pub2.subject))
        if len(temp):
            sum += 3
            check += " : 3sub1"
    if sum == 0 and len(pub1.subject_other) and len(pub2.subject_other):
        temp = list(set(pub1.subject_other).intersection(pub2.subject_other))
        if len(temp):
            sum += 3
            check += " : 3sub2"
    if len(pub1.subject_specific) and len(pub2.subject_specific):
        x = pub1.subject_specific
        y = pub2.subject_specific
        print("##########################################")
        print(x)
        print(y)
        print("##########################################")
        temp = list(set(x).intersection(y))
        n = len(temp)
        if n >= 3:
            sum += 5
            check += " + 5sub3"
        else:
            sum += (2 * n)
            check += " + sub3_" + str(2*n)
    # Co-authors
    for i in range(0, len(pub1.authors)):
        for j in range(0, len(pub2.authors)):
            if pub1.authors[i] == pub2.authors[j]:
                common += 1
    if common > 1:
        sum += (common - 1)*4
        check += " + co_" + str(common*4 - 4)
    if common == 2 and len(pub1.authors) < 5 and len(pub2.authors) < 5:
        sum += 4
        check += ",4 "
    # Affiliation
    if len(pub1.affiliation) > 0 and len(pub2.affiliation) > 0:
        max_r = 0
        aff1 = ""
        aff2 = ""
        for name, aff in pub1.affiliation.items():
            r = levenshtein(name, auth)
            if r > max_r:
                max_r = r
                aff1 = aff
        max_r = 0
        for name, aff in pub2.affiliation.items():
            r = levenshtein(name, auth)
            if r > max_r:
                max_r = r
                aff2 = aff
        lev = levenshtein(aff1, aff2)
        if lev >= 0.5:
            sum += 10
            check += " + 10aff"
        if lev > 0.2 and lev < 0.5:
            count = 0
            if len(aff1) < len(aff2):
                a_min = aff1
                a_max = aff2
            else:
                a_min = aff2
                a_max = aff1
            a = a_min.split(',')
            for item in a:
                item = item.lstrip(' ')
                item = item.rstrip(' ')
                if a_max.find(item) == -1:
                    count -= 1
                else:
                    count += 1
            if count > 0:
                sum += 10
                check += " + 10_aff2"

    # Self-Citation
    common = 0
    for item in pub1.references:
        if pub2.title in item:
            sum += 10
            common = 1
            check += " + 10scit"
            break
    if common == 0:
        for item in pub2.references:
            if pub1.title in item:
                sum += 10
                common = -1
                check += " + 10scit"
                break
    # Bibliographic coupling
    common = 0
    for i in pub1.references:
        for j in pub2.references:
            ratio = levenshtein(i, j)
            if ratio > 0.5:
                common += 1
    if common > 0 and common < 3:
        sum += common*2
        check += " + bib" + str(common*2)
    if common >= 3:
        sum += 5
        check += " + 5bib"
    # Threshold
    print(check)
    if sum >= 11:
        return 1
    else:
        return 0

def clusterize(auth, pubList):
    clusterList = []    
    while len(pubList) > 0:
        cluster = []
        cluster.append(pubList[0])
        cluster[0].print_val
        pubList.pop(0)
        i = 0
        while i < len(cluster):
            j = 0
            while j < len(pubList):
                if isSimilar(auth, cluster[i], pubList[j]):
                    cluster.append(pubList[j])
                    pubList.pop(j)
                else:
                    j += 1
            i += 1
        clusterList.append(cluster)
    print("\n\n======================================================================================================\n\n")
    print("Number of Clusters formed are: ", end="")
    print(len(clusterList))
    for item in clusterList:
        print(len(item), end=" ")
    print('\n\n')
    for i in range(0, len(clusterList)):
        print("Cluster ", end="")
        print(i, end="")
        print(". \tNumber of Publications: ", end="")
        print(len(clusterList[i]))
        sortedList = sorted(clusterList[i], key = getKey)
        for j in range(0, len(clusterList[i])):
            #clusterList[i][j].print_val()
            sortedList[j].print_val()
        print("--------------------------------------------------------------------------------------------------")





pubList = []

search_input = input("Please enter the name of the researcher (case - insensitive): ")
authors = dblp.search(search_input)
if len(authors) == 0:
    print("No matching results found")
    exit()
print("Please select one of the below researchers: (Wait till input is not asked for)")

for i in range(0, len(authors)):
    author = authors[i]
    print(str(i+1) + ". " + author.name)
    print("number of publications = " + str(len(author.publications)))
    print("-----------------------------------------")
opt_intput = input("Type 1 for affiliation timeline. Type 2 for clusterization.\n")

if opt_intput == "1":
    auth_index = input('Please select one of the Author Index: ')
    i = int(auth_index) - 1
    author = authors[i]
    affDict = {}
    for publication in author.publications:
        if publication.year is None:
            continue
        if publication.ee is None:
            continue
        if publication.year in affDict.keys():
            continue
        affiliation, ref = affiliation_extracter(publication.ee)
        if len(affiliation) == 0:
            continue
        max_r = 0
        aff1 = ""
        for name, aff in affiliation.items():
            r = levenshtein(name, author.name)
            if r > max_r:
                max_r = r
                aff1 = aff
        if len(aff1) == 0:
            continue
        affDict[publication.year] = aff1
    for j in sorted(affDict):
        print(j, end=": ")
        print(affDict[j])

else:
    str_arr = input('Please enter one or more Index Numbers: ').split(' ') 
    arr = [int(num) for num in str_arr]

    for num in arr:
        #auth_select_input = input("Please enter the index number: ")

        #if int(auth_select_input) == 0:
        #    break

        #i = int(auth_select_input) - 1
        i = num - 1
        author = authors[i]
        for j in range(0, len(author.publications)):
            publication = author.publications[j]

            affiliation = {}
            subject_both = []
            references = []

            if publication.title is None:
                publication.title = ""
            if publication.authors is None:
                publication.authors = []
                publication.authors.append(author.name)
            if publication.year is None:
                publication.year = ""    
            if publication.url is not None:
                temp = publication.url.split("/")
                if temp[1] == "journals":
                    publication.journal = temp[2]
                    publication.crossref = ""
                    subject_both = getSubjects(temp[2], "journal", publication.title)
                elif temp[1] == "conf":
                    publication.crossref = temp[2]
                    publication.journal = ""
                    subject_both = getSubjects(temp[2], "conf", publication.title)
            else:
                publication.journal = ""
                publication.crossref = ""

            if publication.ee is None:
                publication.ee = ""
            else:       
                affiliation, references = affiliation_extracter(publication.ee)
            if len(subject_both) == 0:
                subject_both.append('')
                subject_both.append('')
                subject_both.append('')

            for i in range(len(publication.authors)):
                publication.authors[i] = publication.authors[i].rstrip('0123456789 ') 

            obj = Publication(publication.title, publication.authors, affiliation, publication.year, publication.journal, publication.crossref, subject_both[0], subject_both[1], subject_both[2], publication.ee, references)
            pubList.append(obj)
            #pubList[j].print_val()

    clusterize(author.name.rstrip('1234567890 '), pubList)