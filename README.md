# Parser-Rezultate-Vot 🗳️
Parser for the website: https://rezultatevot.ro/elections/114/results.

The website offers defalcated results for each election, per county (which is extremely useful). 
However, I did not find aggregated data. This might also be useful for future insights.

## Run
Generate the spreadsheet for the 2024 elections by running:
```bash
python3 parser_rezultate_vot/main.py
```
The script can be used for other elections, just replace the `election_type_id` in the dictionary in `parser_rezultate_vot/constants.py`

## Setup
Install the dependencies:
```bash
pip install -r requirements.txt
```