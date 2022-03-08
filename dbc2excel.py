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
    # with open('dbc.json', 'w') as f: # save to json file
    #     f.write(json.dumps(jsonData, indent=4)) #   print(df)
    return jsonData
    


def json2df(js):
    """
    Convert a json file to a csv file

    
    """
    # js=json.load(open(json_file)) # load json file
    
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
                    newDict[hd]=""
                    continue
                newDict[hd]=el[hd]
            except:
                newDict[hd]=''
        data.append(newDict)
        for skey in el['signals']:  # loop over all keys in signals
            newDict=dict()
            # print(skey)
            # newDict['name']=skey
            for hd in header:
                if hd=="signals":
                    newDict[hd]=skey
                    continue
                try:
                    newDict[hd]=el['signals'][skey][hd]
                except:
                    newDict[hd]=''
            data.append(newDict)
    df=pd.DataFrame(data)
    return df



def dbc2Excel(dbc_file, excel_file):
    """
    Convert a dbc file to a csv file
    """
    jsfile=dbc2json(dbc_file)
    df=json2df(jsfile)
    df.to_excel(excel_file, index=False) #save to excel


def dbc2csv(dbc_file, csv_file):
    """
    Convert a dbc file to a csv file
    """
    jsfile=dbc2json(dbc_file)
    df=json2df(jsfile)
    df.to_csv(csv_file, index=False) #save to csv

if __name__ == '__main__':
    dbc2csv('can_dbc.dbc', 'can_dbc.csv')
    dbc2Excel('can_dbc.dbc', 'can_dbc.xlsx')