'''
TAF Programme designed to return a graphical interpretation

@TODO: Graphical Output
       Create Class for each change group
'''

EXAMPLE = 'EGXE 161400Z 1615/1702 22015KT 9999 FEW020 TEMPO 1622/1702 24022G32KT SCT020 BECMG 1615/1619 5000 30010KT'

def get_taf_as_dict(taf):
    '''
    Function to return a dictionary each item of which is a change group
    item 0 will always be the base conditions
    item zero in each key will always be the change group
    '''
    splits = ['BECMG', 'TEMPO', 'PROB40', 'PROB30']
    taf = taf.split(' ')
    taf_dict_key = 0
    taf_dict = {0:[]}
    for word_from_taf in taf:
        if word_from_taf in splits:
            taf_dict_key = taf_dict_key + 1
            taf_dict[taf_dict_key] = [word_from_taf]
        else:
            taf_dict[taf_dict_key] = taf_dict[taf_dict_key]+[word_from_taf]
    return taf_dict


class taf_group():
    '''
    comments
    '''
    def __init__(self, start_group, end_group=None, is_base=False):
        self.raw = start_group
        self.start = self.pull_apart(start_group)
        self.end = end_group

    def __str__(self):
        return str(self.raw)

    def pull_apart(self, group):
        out = {'cloud':[], 'wx':[], 'duration':0}        
        for word in group:
            if '/' in word:
                out['time_group'] = word
                out['hour_start'] = word.split('/')[0][2:]
                out['hour_end'] = word.split('/')[1][2:]
                out['day_start'] = word.split('/')[0][:2]
                out['day_end'] = word.split('/')[1][:2]
                out['duration'] = 24 * int(out['day_end']) + int(out['hour_end']) - 24 * int(out['day_start']) - int(out['hour_start'])
                    
            elif len(word) == 4 and isinstance(int(word), int):
                out['vis'] = word
            elif word[-2:] == "KT":
                out['wind'] = word
                out['max_wind'] = word[-4:-2]


            elif len(word) == 6:
                out['cloud'].append(word)
            elif len(word) == 4 or len(word) == 2 or len(word) == 6:
                out['wx'].append(word)

            for cloud_group in out['cloud']:
                amt = cloud_group[:3]
                height = int(cloud_group[3:]) * 100
                print height, amt                

        print out
            



def main():
    eg_taf = get_taf_as_dict(EXAMPLE)
    #print eg_taf[0]
    for key, item in eg_taf.iteritems():
        if key != 0:
            eg_class = taf_group(get_taf_as_dict(EXAMPLE)[key])
            #print eg_class
        else:
            eg_class = taf_group(get_taf_as_dict(EXAMPLE)[key][2:], is_base=True)
            #print eg_class

if __name__ == "__main__":
    main()
