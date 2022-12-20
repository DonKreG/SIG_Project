# Localiser les feux de circulation

détecter les feux de circulation et leur emplacement à partir d'images à l'aide de 'Computer vision'.


## Caractéristiques

Le résultat est une carte avec des jonctions ayant des feux de circulation. Une liste des feux tricolores identifiés dans un format structuré est également générée.

<img src="/Projet_SIG/samples/results/images/boxed-IMG_0085.JPEG" width="410">



## Échantillon

Des exemples d'images se trouvent sous [samples/images].

Un exemple de carte et un résumé d'un test sont disponibles dans [samples/results].



## Installation

Vérifiez les prérequis suivants :

- Python 3.6 ou plus récent est requis.

Les scripts utilisent les bibliothèques de machine learning suivantes :

- [OpenCV](https://docs.opencv.org/master/index.html)
- [TensorFlow](https://www.tensorflow.org)

Installez les packages Python requis :

```
pip3 install -r exigences.txt
```


## Utilisation

Mettez à jour les chemins de répertoire et autres paramètres dans le fichier `config.ini`.

Placez les images à analyser dans le répertoire spécifié dans `config.ini`.

Exécutez la commande suivante pour analyser les images.

```python
python3 analyse-images.py
```

Les résultats de l'analyse seront créés dans le répertoire spécifié dans `config.ini`.

**Remarque !** Lors de la première exécution, le chargement de la bibliothèque de vision par ordinateur peut prendre plusieurs minutes. L'initialisation de la bibliothèque ne se produit qu'une seule fois, de sorte que le traitement ultérieur sera plus rapide.

