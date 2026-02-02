import math




def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    dot_prod = 0
    for key in vec1:
        if key in vec2:
            dot_prod += vec1[key]*vec2[key]
    squared_sum_1 = 0
    squared_sum_2 = 0
    for key in vec1:
        squared_sum_1 += vec1[key]**2
    for key in vec2:
        squared_sum_2 += vec2[key]**2
    return dot_prod/((squared_sum_1*squared_sum_2)**0.5)




def build_semantic_descriptors(text):
    semantic = {}
    L =[]
    for sentence in text:
        for word in sentence:
            if not word in L:
                L.append(word)
    for i in L:
        semantic[i] = {}
        for sentence in text:
            if i in sentence:
                for word in sentence:
                    if word != i:
                        if word in semantic[i]:
                            semantic[i][word] += 1
                        else:
                            semantic[i][word] = 1

    return semantic





def build_semantic_descriptors_from_files(filenames):
    L = ""
    sem = []
    new_sem = []
    for i in range(len(filenames)):
        L += open(filenames[i], "r", encoding="latin1").read().replace("\n"," ")
    for end in ["!","?"]:
        L = L.replace(end,".")

    for p in [",", "-", "--", ":", ";"]:
        L = L.replace(p, " ")
    L = L.lower()
    sem = L.split(".")
    for sentence in sem:
        if sentence != " ":
            new_sem.append(sentence.split())
    return build_semantic_descriptors(new_sem)








def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    if word not in semantic_descriptors:
        return choices[0]

    sem_word = semantic_descriptors[word]
    max_score = -2
    max_choice = choices[0]

    for choice in choices:
        if choice not in semantic_descriptors:
            score = -1
        else:
            sem_choice = semantic_descriptors[choice]
            score = similarity_fn(sem_word, sem_choice)

        if score > max_score:
            max_score, max_choice = score, choice

    return max_choice




def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    f = open(filename, "r", encoding="latin1")

    score = 0
    trials = 0

    for line in f:
        parts = line.split()

        if len(parts) < 3:
            continue
        word = parts[0]
        answer = parts[1]
        choices = parts[2:]
        computer = most_similar_word(word, choices, semantic_descriptors, similarity_fn)
        trials +=1
        if computer == answer:
            score += 1
    return (score/trials)*100




if __name__ == "__main__":
    print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))

    bom = [["i", "am", "a", "sick", "man"],
["i", "am", "a", "spiteful", "man"],
["i", "am", "an", "unattractive", "man"],
["i", "believe", "my", "liver", "is", "diseased"],
["however", "i", "know", "nothing", "at", "all", "about", "my",
"disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]
    semd = build_semantic_descriptors(bom)
    word = "i"
    choices = ["am","sick","certain","nothing","me"]


    c_file1 = r"C:\Users\alvin\OneDrive\Documents\UofT 1st Year\ESC180\Projects\syn_tests\c_file1.txt"
    c_file2 = r"C:\Users\alvin\OneDrive\Documents\UofT 1st Year\ESC180\Projects\syn_tests\c_file2.txt"
    c_file3= r"C:\Users\alvin\OneDrive\Documents\UofT 1st Year\ESC180\Projects\syn_tests\c_file3.txt"
    L = [c_file1,c_file2,c_file3]

    print(build_semantic_descriptors_from_files(L))


