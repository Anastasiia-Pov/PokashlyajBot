# PokashlyajBot on aiogram

This TG-Bot (@PokashlyajBot) is considered as a pet-project to get acquainted with aiogram asynchronous framework written in Python.
The project is implemented in virtual environment with Python version 3.12.2.

# Requirements
Python 3.12 with all the [requirements.txt](https://github.com/Anastasiia-Pov/TarotDiabloBot/blob/main/requirements.txt) dependencies installed.

# Files
```
├─ main.py - entry point
├─ app/ - contains component files
│  ├─ comands.py - commands that are installed in bot
│  ├─ handlers.py - handlers of the bot
│  ├─ keyboards.py - keyboards used in the bot
│  ├─ localization.py - file with texts for en-ru bot's answers
├─ database/ - contains code for DB
│  ├─ models.py - models of DBs
│  ├─ requests.py - handler for requests in DB
├─ sub_processes/ - processes, such as diagramming, saved ml-model
├─ research_on_features/ - all the files to extract features and research on finding out the best model for classififcation
│  ├─ extract_gemaps.py - file with function to transform ogg to wav, to extract features vector from voice message and tranform feature vector in input-suitable format for a model
│  ├─ model_research.ipynb - file with the tests of ml-models
│  ├─ sorting.ipynb - file for sorting files into three sets: train, validation, test and extracting features
├─ assets/ - png examples
```
*Config file is not published in this repository as long as it contains private information of the developer.

# Database
Database is developed on PostgreSQL with use of ORM SQLAlchemy. There are 3 databases:
1. Storing info about users: name, age, gender, region.
2. Storing info about localization (tg_id - 'ru'/'en').
3. Stroing info about users voice messages with cough (tg_id - file_id is used for file name).

# Localization
Implemented localization for EN-RU languages.

# Admins interface
Admins have an oportunity to observe statistics on users according to age and region.
Diagrams are constructed with ```matplotlib.pyplot``` and code can be observed in [sub_processes
/diagrams.py](https://github.com/Anastasiia-Pov/PokashlyajBot/blob/main/sub_processes/diagrams.py)

Fig. 1 Example of a diagram about statistics by age groups
<img src=https://github.com/Anastasiia-Pov/PokashlyajBot/blob/main/assets/age.png width=500 />

Fig. 2 Example of a diagram about statistics by regions
<img src=https://github.com/Anastasiia-Pov/PokashlyajBot/blob/main/assets/region.png width=500 />

# Implemented features:
- admins interface (statistics);
- localization (EN-RU);
- support chat;
- user can update their registered data: name, age, gender, region;
- processing sound (voice message) into gemaps features - [extract_gemaps.py](https://github.com/Anastasiia-Pov/PokashlyajBot/blob/main/research_on_features/extract_gemaps.py).
- classifying voice message (transformed into 1D vector) with the ml-model - [model_svm_rbf.pickle](https://github.com/Anastasiia-Pov/PokashlyajBot/blob/main/sub_processes/model_svm_rbf.pickle).

## ML-algorithm:
At this moment in the bot implemented binary classification: healthy and unhealthy cough.
## Database:
For training, validation and testing is used [COUGHVID dataset](https://www.kaggle.com/datasets/nasrulhakim86/coughvid-wav). From json-files were extracted cough statuses such as 'healthy' for healthy group and 'symptomatic' and 'COVID-19' as unhealthy group.
## Extracted features:
[GeMAPS](https://sail.usc.edu/publications/files/eyben-preprinttaffc-2015.pdf) features were extracted with the help of [openSMILE](https://audeering.github.io/opensmile/index.html). Example of the function of features extraction is shown in [extract_gemaps.py](https://github.com/Anastasiia-Pov/PokashlyajBot/blob/main/research_on_features/extract_gemaps.py) - ```opensmile_extractor``` function.
## Models research:
Research on models was conducted, models reasearch represented in file [models_research.ipynb](https://github.com/Anastasiia-Pov/PokashlyajBot/blob/main/research_on_features/Models-research.ipynb).
Model test is in [ml_model_test.ipynb](https://github.com/Anastasiia-Pov/PokashlyajBot/blob/main/research_on_features/ml_model_test.ipynb).
## The best result:
The best result of all models was achieved by SVM-rbf
**SVM-rbf (result on validation set)**
|  Class             |  F1-score |    Recall   | Precision |
|--------------------|-----------|-------------|-----------|
|healthy/здоровый    |   0.556   |    0.558    |   0.554   |
|unhealthy/нездоровый|   0.553   |    0.551    |   0.555   |
|                                                          |
| Weighted average Precision |  0.554  |                    |
| Weighted average Recall |  0.554  |                       |
| Weighted average F1 |  0.554  |                           |
| Accuracy |  0.554 |                                      |

**SVM-rbf (result on test set)**
|  Class             |  F1-score |    Recall   | Precision |
|--------------------|-----------|-------------|-----------|
|healthy/здоровый    |   0.526   |    0.528    |   0.524   |
|unhealthy/нездоровый|   0.522   |    0.520    |   0.524   |
|                                                          |
| Weighted average Precision |  0.524                      |
| Weighted average Recall |  0.524                         |
| Weighted average F1 |  0.524                             |
| Accuracy |  0.524                                        |

**!! Still, there is room for improvement, we are working on it !!**