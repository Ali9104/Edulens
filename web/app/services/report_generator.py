from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import os


def generate_report(student):
    filepath = os.path.join(os.path.dirname(__file__), '..', f"rapport_{student.nom}_{student.prenom}.pdf")
    doc = SimpleDocTemplate(filepath, pagesize = A4)
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_titre = styles["Title"]
    story = []
    story.append(Spacer(1, 12))
    story.append(Paragraph("Rapport EduLens", style_titre))
    nom = student.nom
    prenom = student.prenom
    groupe = student.groupe
    story.append(Paragraph(f"Nom : {nom}", style_normal))
    story.append(Paragraph(f"Prenom : {prenom}", style_normal))
    story.append(Paragraph(f"Groupe : {groupe}", style_normal))
    notes = [g.note for g in student.grades]
    average = sum(notes) / len(notes) if notes else 0
    story.append(Paragraph(f"Moyenne : {average}", style_normal))
    semestres = {}
    for grade in student.grades:
        if grade.semestre not in semestres:
            semestres[grade.semestre] = []
        semestres[grade.semestre].append(grade)
    for semestre, grades in semestres.items():
        story.append(Paragraph(f"Semestre : {semestre}", style_titre))
        for g in grades:
            story.append(Paragraph(f"{g.matiere} : {g.note}/20", style_normal))
        notes_sem = [g.note for g in grades]
        moyenne_sem = round(sum(notes_sem)/len(notes_sem), 2)
        story.append(Paragraph(f"Moyenne du semestre : {moyenne_sem}", style_normal))
    doc.build(story)
    return filepath






