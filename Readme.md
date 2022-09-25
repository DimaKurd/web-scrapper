# Web scrapper of reviews  from yandex maps

## Description
This project uses googlechrome webdriver, selenium, some pandas and list of required addresses

to get all reviews and scores from yandex maps
## How to run
> execute command `python test.py <doc_name> <left_border> <right_border> <output>` from folder scripts
>
>`doc_name` - name of csv file of addresses you want to scrap
>
>`left_border`, `right_border` - borders of addresses
>
>`output` - name of csv file for extracting data

## Examples
>`data/polikliniks_addresses_fixed.csv` - list of medical buildings
> 
> `data/test1.csv` - example of executing the command `python test.py 'data/polikliniks_addresses_fixed.csv' 0 500 'data/test1.csv'`