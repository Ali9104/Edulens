from sklearn.cluster import KMeans
import numpy as np


def cluster_students(list_student):
    avec_notes = []
    sans_notes = []
    for student in list_student:
        if student.grades:
            avec_notes.append(student)
        else:
            sans_notes.append(student)
    if len(avec_notes) < 3:
        mon_dict = {}
        for student in list_student:
            mon_dict[student.id] = "Non évalué"
        return mon_dict
    noms = [s.nom + ' ' + s.prenom for s in avec_notes]
    moyenne = []
    for student in avec_notes:
        notes = [g.note for g in student.grades]
        if notes : 
            moyenne.append(round(sum(notes)/len(notes),2))
        else:
            moyenne.append(0)
    X = np.array(moyenne).reshape(-1, 1)
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(X)
    centre = kmeans.cluster_centers_.flatten()
    ordre = np.argsort(centre)  
    labels_map = {ordre[0]: "En difficulté", ordre[1]: "Moyen", ordre[2]: "Excellent"}
    mon_dict = {}
    for i, student in enumerate(avec_notes):
        mon_dict[student.id] = labels_map[kmeans.labels_[i]]
    for student in sans_notes:
        mon_dict[student.id] = "Non évalué"
    return mon_dict



    
            
        

