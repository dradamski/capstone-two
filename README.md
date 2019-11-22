# New York Water Quality Analysis
===============================

By using New York City Harbor Water Quality data, I created a tool to help local 
governments shrink monitoring costs and predict poor water quality readings by 
reducing the amount of sampling needed to draw conclusions. Utilizing a variety of
exploratory techniques like Network Analysis, Geostatistics, Frequentist 
Statistics, and Supervised and Unsupervised Machine Learning, I developed a model 
to solve this problem.

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │       └── Clean_Harbor_Water_Quality.csv
    │   ├── processed      <- The final, canonical data sets for modeling.
    │       └── Final_Clean_Harbor_Water_Quality.csv
    │   └── raw            <- The original, immutable data dump.
    │       └── Harbor_Water_Quality.csv
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │   ├── [1.0-dra-data-wrangling.ipynb](https://github.com/dradamski/capstone-two/blob/master/notebooks/1.0-dra-data-wrangling.ipynb)
    │   ├── [2.0-dra-data-exploration.ipynb] (https://github.com/dradamski/capstone-two/blob/master/notebooks/2.0-dra-data-exploration.ipynb)
    │   ├── [3.1-dra-indepth-analysis.ipynb] (https://github.com/dradamski/capstone-two/blob/master/notebooks/3.1-dra-indepth-analysis.ipynb)
    │   └── [3.2-dra-indepth-analysis.ipynb] (https://github.com/dradamski/capstone-two/blob/master/notebooks/3.2-dra-indepth-analysis.ipynb)
    │
    ├── references          <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports             <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   ├── Final_Rep_NYC_WQ.pdf
    │   └── NYC_WQ_Pres.pptx 
    │                      
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    │
    └── src                <- Source code for use in this project.
        └── data           <- Scripts to download or generate data
           └── make_dataset.py


<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
