import sys
import pandas as pd
import os

CHEMIN = "chemin_complet"
PREFIXE = "Renommage_prefixe"
fichier = "C:\echantillon-SCRIPT\TEST-renommage.xlsx"


def rename(nom):
    file = pd.read_excel(nom)
    compteur = 0
    for ligne in file.itertuples():
        print(getattr(ligne, CHEMIN))
        for rootdir, dirs, files in os.walk(getattr(ligne, CHEMIN)):
            for f in [f for f in files if f[-4:].lower() == ".wav" and f[-5:].lower() != 't.wav']:
                src = rootdir+"\\"+str(f)
                dest = rootdir+"\\"+f"{getattr(ligne, PREFIXE)}{str(f).split('.')[0]}.wav"
                if src.find(ligne.Renommage_prefixe) == -1:
                    os.renames(src, dest)
                    compteur += 1
    print(f"{compteur} fichier(s) renommé(s)")


def main(argv):
    if argv:
        inputfile = argv[0]
        rename(inputfile)
        return 0
    else:
        print(f"""Utilisation:
                rename.py <inputfile>
        """)
        sys.exit(2)


if __name__ == '__main__':
    main(sys.argv[1:])
