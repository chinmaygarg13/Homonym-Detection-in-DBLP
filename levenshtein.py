import jellyfish

def levenshtein(i, j):
    dist = jellyfish.damerau_levenshtein_distance(i, j)
    l = max(len(i), len(j))
    if l == 0:
        return 0
    ratio = 1 - (dist/l)
    return ratio

#x = "Department of Computer Science, Shanghai Maritime University, Shanghai, Chin"
#y = "Dept. of Comput. Sci., UC Santa Barbara, Santa Barbara, CA"

#print(levenshtein(x,y))