from hashlib import new
import cantools
from pprint import pprint
import pandas as pd
import json

def dbc2json(dbc_file):
    """
    Convert a dbc file to a json file
    """
    dbc = cantools.db.load_file(dbc_file)
    jsonData=[]

    for message in dbc.messages: # loop over all messages in the dbc file
        candt=dict()
        candt['name']=message.name
        candt['id']=hex(message.frame_id)
        candt['length']=message.length
        candt['comments']=message.comment
        signals=dict()

        
        for signal in message.signals: # loop through signals in message 
            signals[signal.name]={}
            signals[signal.name]['start']=signal.start
            signals[signal.name]['bit_length']=signal.length
            signals[signal.name]['is_signed']=signal.is_signed
            signals[signal.name]['is_float']=signal.is_float
            signals[signal.name]['offset']=signal.offset
            signals[signal.name]['scale']=signal.scale
            signals[signal.name]['minimum']=signal.minimum
            signals[signal.name]['maximum']=signal.maximum
            signals[signal.name]['unit']=signal.unit
            signals[signal.name]['multiplexer_ids']=signal.multiplexer_ids
            signals[signal.name]['unit']=signal.unit
            signals[signal.name]['receivers']=signal.receivers
            # signals[signal.name]['dbc_specifics']=signal.dbc_specifics
            signals[signal.name]['comment']=signal.comment
            # signals[signal.name]['decimal']=signal.decimal
            signals[signal.name]['byte_order']=signal.byte_order
            candt['signals']=signals
        
        jsonData.append(candt) # append to json data
    with open('dbc.json', 'w') as f: # save to json file
        f.write(json.dumps(jsonData, indent=4)) #   print(df)
    


def json2csv(json_file, excel_file):
    """
    Convert a json file to a csv file

    
    """
    js=json.load(open(json_file)) # load json file
    
    data=[]
    header=[]
    for elkey in js[0]: # loop over all keys in json file
        
        header.append(elkey)
        if elkey=='signals':  # if key is signals
            sigs=js[0][elkey]
            for sigkey in sigs:  # loop over all keys in signals
                for sigel in sigs[sigkey]:
                    header.append(sigel)
                break
            break
    for el in js:  # loop over all elements in json file
        newDict=dict()
        for hd in header:
            try:
                if hd=="signals":
                    newDict[hd]=hd
                    continue
                newDict[hd]=el[hd]
            except:
                newDict[hd]=''
        data.append(newDict)
        for skey in el['signals']:  # loop over all keys in signals
            newDict=dict()
            for hd in header:
                if hd=="signals":
                    newDict[hd]=""
                    continue
                try:
                    newDict[hd]=el['signals'][skey][hd]
                except:
                    newDict[hd]=''
            data.append(newDict)
    df=pd.DataFrame(data)
    df.to_csv(excel_file, index=False) # save to csv
    df.to_excel("dbc.xlsx", index=False) #save to excel

if __name__ == '__main__':
    dbc2json('can_dbc.dbc')
    json2csv('dbc.json', 'dbc.csv')