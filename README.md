# Project
Hackbright final demo web application

# Developing

## Updating translations
```
# extract
pybabel extract -F babel.cfg -o messages.pot --ignore-dirs=env .
# update
pybabel update -i messages.pot -l es -d translations
pybabel update -i messages.pot -l en -d translations

# now translate files

# compile
pybabel compile -d translations
```
