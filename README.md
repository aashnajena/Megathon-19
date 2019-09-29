# Fill in the Blank generator

This is an implementation of our project, made as part of Megathon '19 for the problem statement provided by Embibe;

**_"Given a text document, identify relevant factoids and generate fill-in-the-blank type questions for the same, along with the answer keys."_**

## Team Do-Little
Mayank Modi
Aditya Srivastava
Priyank Modi
Aashna Jena

## Instructions
Install all dependencies and run; 
- `python selector_bio/chem_phy.py input_file output_file`

## About
The code implements our heuristic to determine relevant sentences and another to determine the appropriate keys for the same.  
- The raw files are passed through a rule based text cleaning algorithm which tokenizes the file into cleaned and normalized sentences.
- Sentence selection: The cleaned texts are passed through a heuristic which calculates a score for a sentence based on the metrics: 
    - Is it an equative sentence
    - Is it the first sentence of the document
    - Does it contain any abbreviation
    - Does it contain a word in its superlative degree
    - It's position in the document
    - Is it a beginning with a discource connective
    - Number of words in it
    - Frequency of nouns
    - Frequency of pronouns

## Dependencies
- Python 3.6
- spaCy
- nltk
- numpy
- requests