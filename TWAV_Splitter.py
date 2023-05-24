import os
import json
import getopt, sys
import subprocess
import datetime
from multiprocessing import Pool, TimeoutError
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


def liste_fichier_twav(dossier_source, dossier_dest=None, liste={}, first=None):
    nb_fichiers = 0
    if not first:
        first = dossier_source
    for rootdir, dirs, files in os.walk(dossier_source):
        complement = rootdir[len(first):]
        dossier_desti = os.path.join(dossier_dest, rootdir[(len(first)+1):])
        for file in [f for f in files if f[-5:].lower() == 't.wav']:
            if not os.path.exists(dossier_desti):
                os.makedirs(dossier_desti)
            liste[os.path.join(rootdir, file)] = dossier_desti
            nb_fichiers += 1
    return nb_fichiers, liste

@timing
def main(argv):
    
    inputdir = None
    outputdir = None
    json_file = []
    nbthread = 2
    
    try:
        opts, args = getopt.getopt(argv, "hi:o:n:", ["idir=", "odir=", "nbthread="])
    except getopt.GetoptError:
        print(f"""Utilisation:
                TWAV_Splitter.py -i <inputdirectory> -o <outputdirectory> [-n <nombre de processus simultanés>]
        """)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print(f"""Utilisation:
                    TWAV_Splitter.py -i <inputdirectory> -o <outputdirectory> [-n <nombre de processus simultanés>]
            """)
            sys.exit()
        elif opt in ("-i", "--idir"):
            inputdir = arg
        elif opt in ("-o", "--odir"):
            outputdir = arg
        elif opt in ("-n", "--nbthread"):
            nbthread = int(arg)
            
    if not json_file:
        rep = tempfile.mkdtemp() # Create temp directory
    if not (inputdir is None or outputdir is None):
        print("Paramètres trouvés")
        json_dict = {}
        json_dict["nombre"], json_dict["fichiers"] = liste_fichier_twav(inputdir, dossier_dest=outputdir)
        for t in range(nbthread):
            json_file.append(f"{rep}/fichiers{t}.json")
        thread_dict = {}
        for n in range(nbthread):
            thread_dict[f"{n}"] = {"nombre": 0,
                                   "fichiers":{}}
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
            with open(json_file[t], 'w') as fichier_json:
                json.dump(dic, fichier_json, indent=4)
        print("Traitement terminé")
        with Pool(processes=nbthread) as pool:
            pool.map(splitting, json_file)
        shutil.rmtree(rep) # Remove temp dir

    else:
        print("Paramètre(s) manquant(s)")
        print(f"""Utilisation:
        vigie.py -i <inputdirectory> -o <outputdirectory> [-n <nombre de processus simultanés>]
""")

def splitting(json_file):
    subprocess.run(f"node AudioMoth-Utils-master\Expand_V2.js {json_file}")
    os.remove(json_file)

if __name__ == '__main__':
    main(sys.argv[1:])
