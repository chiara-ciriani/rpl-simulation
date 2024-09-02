# Performance Evaluation

## Introduction

To do

## Requirements

Install dependencies: 
```bash
    python -m pip install -r requirements.txt
```  

## Program execution

From src directory: 
```bash
    cd src
```

### Single Path and Multi Path alternatives number of transmissions

The following program creates a CDF with the transmission number of each approach.

```bash
    > python3 script_test_approaches.py
```

There is a global variable ```"MULTIPATH"``` that defines whether the versions are to be executed in single path or multi path.

### Multi Path metrics

The following program creates a CDF of the probability that all street lights receive the message sent by a street light origin.
Also, for the metrics of Minimum Vertex Cut and Edge Cut, that are useful metrics to give an idea of the reliability of each approach.

```bash
    > python3 script_test_domains_metrics.py
```