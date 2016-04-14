import requests
from itertools import islice
from io import StringIO
import pandas as pd

def chunketize(x,y):
        i = iter(x)
        if len(x) % y == 0:
                chunks = range((len(x)//y))
        else:
                chunks = range((len(x)//y)+1)
        dic = []
        for chunk in chunks:
                dic.append(list(islice(i,y)))
        return dic

def geocode(x):
    url = 'http://geocoding.geo.census.gov/geocoder/locations/addressbatch'
    census_year = {'benchmark': 'Public_AR_Current'}
    data_chunks = chunketize(str(x),1000)
    buff = StringIO()
    for i in range(len(data_chunks)):
        files = {'addressFile': ''.join(data_chunks[i])}
        response = requests.post(url, data=census_year, files=files)
        for block in response.iter_content(1024):
            block = block.decode()
            buff.write(block)
    outraw = buff.getvalue().strip()
    cnames = ['id_number', 'input_address', 'match_status', 'match_type', 'matched_address', 'lonlat', 'tigerline_id', 'street_orientation']
    df = pd.read_csv(StringIO(outraw), names=cnames, sep=',', dtype={'lonlat' : 'str'})
    #add malformed file handling
    df['longitude'] = df['lonlat'].str.split(',', expand=True)[0]
    df['latitude'] = df['lonlat'].str.split(',', expand=True)[1]
    final_order = ['id_number', 'input_address', 'match_status', 'match_type', 'matched_address', 'latitude', 'longitude', 'tigerline_id', 'street_orientation']
    buff.truncate(0)
    df[cnames].to_csv(buff, index=False)
    return buff.getvalue()

def main():
    print("Don't run me...")

if __name__ == '__main__':
    main()
