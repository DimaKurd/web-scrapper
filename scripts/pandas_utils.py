import pandas as pd


class Data:
    def __init__(self, name):
        self.data = pd.DataFrame(columns=['address', 'org', 'review', 'score'])
        self.name = name

    def add_new_line(self, address, org, review, review_score):
        pd.DataFrame(columns=['address', 'org', 'review', 'score'],
                     data=[[address, org, review, review_score]]).to_csv(path_or_buf='../data/{}.csv'.format(self.name),
                                                                         mode='a', header=False, index=False)

    def save_progress(self, name):
        self.data.to_csv(path_or_buf='../data/{}.csv'.format(name), mode='a', header=False)

    def get_addresses_from_data(self, path):
        return pd.read_csv(path)['address'].dropna().unique()
