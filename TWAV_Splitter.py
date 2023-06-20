import os
import json
import getopt
import sys
import subprocess
import datetime
from multiprocessing import Pool
import tempfile
import shutil


def timing(function):
    def new_func(*args, **kargs):
        print(args)
        print(kargs)
        debut = datetime.datetime.now()
        result = function(*args, **kargs)
        print((datetime.datetime.now() - debut))
        return result
    return new_func


def liste_fichier_twav(dossier_source, dossier_dest=None, first=None):
    liste = {}
    nb_fichiers = 0
    if not first:
        first = dossier_source
    for rootdir, dirs, files in os.walk(dossier_source):
        dossier_desti = os.path.join(dossier_dest, rootdir[(len(first)+1):])
        for file in [f for f in files if f[-5:].lower() == 't.wav']:
            if not os.path.exists(dossier_desti):
                os.makedirs(dossier_desti)
            liste[os.path.join(rootdir, file)] = dossier_desti
            nb_fichiers += 1
    return nb_fichiers, liste


def print_help():
    print(
        f"""Utilisation:
        TWAV_Splitter.py -i <inputdirectory> -o <outputdirectory> [options]
        options:
        -n <nombre de processus> : traitement simultané de plusieurs fichiers
        -p <'chaine_de_caractère'> : chaine de caractères à ajouter comme préfixe des noms de fichier (par défaut '')
        -e <expansionType> : 'EVENT' ou 'DURATION' (par défaut 'EVENT')
        -d <maximumFileDuration> : durée en seconde d'un fichier (par défaut 5)
        -s <generateSilentFiles> : True ou False (par défaut False)
        -a <alignToSecondsTransition> : True ou False (par défaut False)
    """)


@timing
def main(argv):
    prefixe = ''
    exp = 'EVENT'
    duration = 5
    silent = "false"
    align = "false"
    inputdir = None
    outputdir = None
    list_arg = []
    nbthread = 2
    
    try:
        opts, args = getopt.getopt(argv, "hi:o:n:p:e:d:s:a:", ["idir=", "odir=",
                                                               "nbthread=", "prefixe=", "expansionType=",
                                                               "maximumFileDuration=", "generateSilentFiles=",
                                                               "alignToSecondTransitions="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-i", "--idir"):
            inputdir = arg
        elif opt in ("-o", "--odir"):
            outputdir = arg
        elif opt in ("-n", "--nbthread"):
            nbthread = int(arg)
        elif opt in ("-p", "--prefixe"):
            prefixe = arg.replace("'", "")
        elif opt in ("-e", "--expansionType"):
            a = arg.replace("'", "")
            if a not in ["EVENT", "DURATION"]:
                print("""le paramètre -e doit être EVENT ou DURATION""")
                sys.exit(2)
            exp = a
        elif opt in ("-d", "--maximumFileDuration"):
            try:
                duration = int(arg)
            except:
                print("""le paramètre -d doit être un entier""")
                sys.exit(2)
        elif opt in ("-s", "--generateSilentFiles"):
            if arg.lower() == "true":
                silent = "true"
            elif arg.lower() == "false":
                silent = "false"
            else:
                print("""le paramètre -s doit être True ou False""")
                sys.exit(2)
        elif opt in ("-a", "--alignToSecondTransitions"):
            if arg.lower() == "true":
                align = "true"
            elif arg.lower() == "false":
                align = "false"
            else:
                print("""le paramètre -a doit être True ou False""")
                sys.exit(2)
        else:
            print(f"L'option {opt} n'est pas reconnu")

    rep = tempfile.mkdtemp()
    if not (inputdir is None or outputdir is None):
        print("Paramètres trouvés")
        json_dict = {}
        json_dict["nombre"], json_dict["fichiers"] = liste_fichier_twav(inputdir, dossier_dest=outputdir)
        for t in range(nbthread):
            list_arg.append((f"{rep}/fichiers{t}.json", prefixe, exp, duration, silent, align))
        thread_dict = {}
        for n in range(nbthread):
            thread_dict[f"{n}"] = {"nombre": 0,
                                   "fichiers": {}}
        num_file = 0
        for key, value in json_dict["fichiers"].items():
            quotient, num_thread = divmod(num_file, nbthread)
            dic = thread_dict[f"{num_thread}"]
            dic["nombre"] += 1
            fic = dic["fichiers"]
            fic[key] = value
            num_file += 1
        for t in range(nbthread):
            dic = thread_dict[f"{t}"]
            with open(list_arg[t][0], 'w') as fichier_json:
                json.dump(dic, fichier_json, indent=4)
        print("Traitement terminé")
        with Pool(processes=nbthread) as pool:
            pool.map(splitting, list_arg)
        shutil.rmtree(rep)

    else:
        print("Paramètre(s) manquant(s)")
        print_help()


def splitting(args):
    json_file, prefixe, exp, duration, silent, align = args
    subprocess.run(f"node AudioMoth-Utils-master\\_Expand.js {json_file} {prefixe} {exp} {duration} {silent} {align}")
    os.remove(json_file)


if __name__ == '__main__':
    main(sys.argv[1:])
