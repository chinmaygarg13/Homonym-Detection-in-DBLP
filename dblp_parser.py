import requests
import dblp

search_input = input("Please enter the name of the researcher (case - insensitive): ")
authors = dblp.search(search_input)
if len(authors) == 0:
    print("No matching results found")
    exit()
print("Please select one of the below researchers: (Wait till input is not asked for)")

for i in range(0, len(authors)):
    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    author = authors[i]
    print(str(i+1) + ". " + author.name)
    #print(author.homonyms)
    print("number of publications = " + str(len(author.publications)))
    print("-----------------------------------------")

auth_select_input = input("Please enter the index number: ")

i = int(auth_select_input) - 1
author = authors[i]
pubList = []
for j in range(0, len(author.publications)):
    publication = author.publications[j]
    print(publication.title)
    print(publication.type)    
    print("Authors: ", end="") 
    print(publication.authors)
    print("Year of Publication: ", end="")
    print(str(publication.year))
    print("Journal Name: ",end="") 
    print(publication.journal)  
    print("Conference Name: ",end="")
    print(publication.crossref)
    print("URL: ", end="")
    print(publication.url)             
    print(publication.ee)
    print("School: ", end="")
    print(publication.school)
    print("Series: ", end="")
    print(publication.series)
    print(publication.citations)
    print("**************************************************")