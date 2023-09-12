import numpy as np
import pandas as pd
import yaml

all_magic_key_names = ['inspire', 'believe', 'enchant', 'imagine', 'dream']

def convert_json_to_csv():
    print("Beginning to convert json files to csv files")
    for magic_key_name in all_magic_key_names:
        data = ''
        with open(f'data/{magic_key_name}.json') as f:
            data = f.read()

        calendar_data = yaml.load(data, Loader=yaml.FullLoader)

        df = pd.DataFrame(calendar_data)

        facilities = df['facilities']
        df2 = pd.DataFrame(columns=['DLP_available', 'DLP_blocked', 'DCA_available', 'DCA_blocked'])
        for i in range(len(facilities)):
            dca = facilities[i][0]
            dlp = facilities[i][1]
            df2.loc[i] = [dlp.get('available'), dlp.get('blocked'), dca.get('available'), dca.get('blocked')]

        df = pd.concat([df, df2], axis=1)

        df.drop(columns=['facilities', 'availability', 'dateType'], inplace=True)

        df.to_csv(f'data/{magic_key_name}.csv', index=False)
        print(f"Successfully converted {magic_key_name}.json to {magic_key_name}.csv")