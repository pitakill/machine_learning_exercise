# Requirements
`python 3.6`

# Quick start

### Setup the environment
```
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### To train the model

```
python train.py
```

### To run the model against a phrase

```
python api.py
```
