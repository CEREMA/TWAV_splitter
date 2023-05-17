# TWAV_Splitter

<p align=center><img src=https://www.vigienature.fr/sites/vigienature/files/styles/1600x576/public/thumbnails/image/bandeau_0.jpg width=100%></p>
<p align=center>Crédits image : https://www.vigienature.fr/fr/chauves-souris</p>

Ce script permet de transformer des fichiers audios T.WAV en .WAV pour une intégration dans la plateforme [Vigie-Chiro](https://www.vigienature.fr/fr/chauves-souris)

[A propos du traitement](#a-propos)

## Démarrage rapide

[Installer python](https://www.python.org/downloads/)  
[Installer Node.js](https://nodejs.org/en/download)  

Ouvrir une invite de commandes Windows
	
	cd votredossier
	git clone https://github.com/CEREMA/TWAV_splitter.git

Cela va créer un dossier TWAV_splitter avec le script. Aller dedans :

	cd TWAV_splitter

Lancer le script :

	python TWAV_splitter.py -i <dossier_source> -o <dossier_sortie>

Pour accélérer les traitements, on peut les exécuter en parallèle avec `-n`

	python TWAV_splitter.py -i <dossier_source> -o <dossier_sortie> -n 6

> La valeur par défaut de n est 2

Le script va parcourir le dossier source et créer les fichiers découpés dans le dossier de sortie selon la même arborescence.

Les fichiers WAV générés dans le dossier de sortie peuvent être versés dans [Vigie-Chiro](https://www.vigienature.fr/fr/chauves-souris)

## Tutoriel
[Si vous avez des difficultés, vous pouvez vous référer à ce tutoriel pas à pas avec des copies d'écran](Tuto_decoup_TWAV.pdf)

## License
L'outil TWAV_splitter utilise la bibliothèque [Audiomoth-utils](https://github.com/OpenAcousticDevices/AudioMoth-Utils) qui est sous Licence MIT.

La licence est la licence MIT

## A propos
Le format T.WAV correspond à des fichiers audio concaténés par les enregistreurs acoustiques AudioMoth®.

Les AudioMoths n'enregistrent que les évènements dont le son dépasse un certain seuil de Décibel et les collent entre-eux ; l'enregistrement est donc discontinu dans le temps.

Il n'est pas possible d'analyser directement un enregistrement T.WAV sur la plateforme [Vigie-Chiro](https://www.vigienature.fr/fr/chauves-souris). Sseuls les fichiers .WAV sont acceptés.

Pour convertir un fichier T.WAV en .WAV, il est nécessaire de rétablir la vraie chronologie des évènements.

Le fichier T.WAV doit être dé-concaténé afin de séparer les évènements et les horodater correctement.

De plus, pour l'analyse Vigie-Chiro, les évènement ne doivent pas durer plus de 5 secondes ; le fichier T.WAV doit donc être découpé en plusieurs fichiers de 5 secondes ou moins.

On peut alors supprimer le 'T' de ces fichiers dé-concaténés et découpés afin de les convertir en fichiers .WAV classiques (Waveform Audio File Format).
