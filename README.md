NiFi Utilities 
--------------------------------

## Find stopped processor groups 
Following script finds the processor group in which no processor is running. 
```bash
find_stopped_processor_groups.py
```

## Find invalid processor group
Following script finds the processor group which has at least one invalid processor 
```bash
find_invalid_processor_groups.py
```

## Find duplicate processor group 
Following script finds the duplicate processor group based in it's name. 
```bash
find_duplicate_processor_groups.py
```
## Find contoller servies
Following script finds all the databse controller services being used by NiFi 
```bash
find_duplicate_processor_groups.py
```

# How to Install? 
create the Python Virual Environment and install pre-requisites using following script 
```bash
    sh create_venv.sh
```

# How To Run?
script works for either **QA** or **PROD** NiFi only, as Dev Nifi Doesn't have authentication same script won't work. 

* clone the repo 
    ```bash
    git clone https://bitbucket.corp.ad.ctc/scm/bdho/nifiapi.git
    ```

* run code

    ```bash
    [gaurang.shah@hadoop_prod]$ ./run.sh python find_stopped_processor_groups.py
    NiFi Host : localhost
    NiFi Port: 8080 
    Username [gaurang.shah]: gaurang.shah
    Password:
    ```
* After the run corresponding out file will be created (i.e. find_stopped_processor_groups.py.out)

you won't be able to see password when you type it, just like unix :)
