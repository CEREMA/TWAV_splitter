import queue
import threading
import sys
import pandas as pd
import subprocess
import os

CHEMIN = "chemin_complet"
PREFIXE = "Renommage_prefixe"
SUFFIXE = "Renommage_suffixe"
DOSSIER = "nom_dossier"
ANNEE = "Année"
MAILLE = "Maille_Vigie_Chiro"
NUMZ = "num_Z"
PASSAGE = "Passage"
dossier_zip = "c:\\zip"
fichier = "C:\\vigie\\renom_echantillon.xlsx"


def main(argv):
    if argv:
        inputfile = argv[0]
        zip_dir = argv[1]
        nb_thread = None
        if len(argv) == 3:
            nb_thread = int(argv[2])
        zipper(inputfile, zip_dir, nb_thread)
        return 0
    else:
        print(f"""Utilisation:
                zip.py <inputfile> <zip_dir> [nb_thread]
        """)
        sys.exit(2)


def worker(q):
    while True:
        item = q.get()
        print(f'Working on {item}')
        subprocess.run(item)
        print(f'Finished {item}')
        q.task_done()


def zipper(nom_fichier, nom_rep, nb_thread):
    file = pd.read_excel(nom_fichier, index_col=0)
    if not os.path.exists(nom_rep):
        os.makedirs(nom_rep)
    q = queue.Queue()
    for ligne in file.itertuples():
        # fichier = f"{str(getattr(ligne, ANNEE))}-{str(getattr(ligne, MAILLE))}" \
        #           f"-{str(getattr(ligne, NUMZ))}-{str(getattr(ligne, PASSAGE))}"
        dossier = f"{nom_rep}\\{DOSSIER}"
        if not os.path.exists(dossier):
            os.makedirs(dossier)
        for rootdir, dirs, files in os.walk(ligne.chemin_complet):
            q.put(f"c:\\Program Files\\7-Zip\\7z.exe a {dossier}\\{DOSSIER}.zip {rootdir}\\*.wav -r -v700M")
    nb_dossier = q.qsize()
    if nb_thread:
        for i in range(nb_thread):
            threading.Thread(target=worker, args=(q,), daemon=True).start()
    else:
        threading.Thread(target=worker, args=(q,), daemon=True).start()
    q.join()
    nb_dossier_traite = nb_dossier - q.qsize()
    print(f"{nb_dossier_traite} dossiers traités")


if __name__ == '__main__':
    main(sys.argv[1:])
