# Frapalyzer

The project provides an algorithm of apocope search in French text. Everything is written in Python except for the simplest (single-page) crawlers.

**Note:** To get the code up and running without headaches, you can use the [Anaconda](https://store.continuum.io/cshop/anaconda/) distribution of Python. It includes all necessary libraries, as well as a good IDE and the shell.

## Project content

- To access the console menu run [user_interface.py](/user_interface.py).

- The corpus of apocopes can be found in [dict_apo_auto.csv](/data/dict_apo_auto.csv). It currently contains 1295 apocopes with their full forms.

- Some relevant statistics can be found in [dict_apo_aug.csv](/data/dict_apo_aug.csv).

- The list of full forms used by our algorithm (based on Le Grand Robert) can be found in [list_words.csv](/data/list_words.csv).

- The list of words encountered in the articles parsed from [Le Point](http://www.lepoint.fr) can be found in [datasets.csv](/data/datasets.csv).
