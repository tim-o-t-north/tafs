'''
TAF Programme designed to return a graphical interpretation

@TODO: Graphical Output
       Create Class for each change group
'''

EXAMPLE = '''EGXE 161400Z 1615/1702 22015KT 9999 FEW020 SCT025
TEMPO 1622/1702 24022G32KT SCT020
BECMG 1615/1619 5000 -RA 30010KT'''
SPLITS = ['BECMG', 'TEMPO', 'PROB40', 'PROB30']


def get_taf_as_dict(taf):
    '''
    Function to return a dictionary each item of which is a change group
    item 0 will always be the base conditions
    item zero in each key will always be the change group
    '''

    taf = taf.split(' ')
    taf_dict_key = 0
    taf_dict = {0: []}
    for word_from_taf in taf:
        if word_from_taf in SPLITS:
            taf_dict_key = taf_dict_key + 1
            taf_dict[taf_dict_key] = [word_from_taf]
        else:
            taf_dict[taf_dict_key] = taf_dict[taf_dict_key] + [word_from_taf]
    return taf_dict


class TafGroup():
    '''
    comments
    '''
    def __init__(self, start_group, end_group=None, is_base=False):
        self.raw = start_group
        self.start = self.pull_apart(start_group)
        self.end = end_group
        self.is_base = is_base

    def __str__(self):
        return str(self.start)

    def get_cloud_group_dict(self, clouds, mil_rules=True):
        '''
        Returns a list of dictionaries, one for each cloud
        group and one for the lowest cloud height
        '''
        if mil_rules is True:
            sig_cloud = ['SCT', 'BKN', 'OVC']
        elif mil_rules is False:
            sig_cloud = ['BKN', 'OVC']
        out = []
        for cloud in clouds:
            detail = {'height': int(cloud[3:]) * 100, 'amt': cloud[:3]}
            out.append(detail)
        lowest_base = 10000
        for cloud in out:
            if cloud['height'] < lowest_base and cloud['amt'] in sig_cloud:
                lowest_base = cloud['height']
        out.append({'lowest_base': lowest_base})
        return out

    def cloud_analysis(self, clouds):
        '''
        takes a list of clouds in string form and returns dicts
        '''
        if len(clouds) == 0:
            return ['nsc']
        else:
            clouds = self.get_cloud_group_dict(clouds)
            return clouds

    def pull_apart(self, group):
        '''
        takes taf data and turns it into a dict.
        '''
        out = {'clouds': [], 'wx': [], 'duration': 0}
        clouds = []
        for word in group:
            if '/' in word:
                out['time_group'] = word
                out['hour_start'] = word.split('/')[0][2:]
                out['hour_end'] = word.split('/')[1][2:]
                out['day_start'] = word.split('/')[0][:2]
                out['day_end'] = word.split('/')[1][:2]
                end_time = 24 * int(out['day_end']) + int(out['hour_end'])
                start_time = 24 * int(out['day_start']) + int(out['hour_start'])
                out['duration'] = end_time - start_time
            elif word in SPLITS:
                out['change_type'] = word
            elif len(word) == 4 and isinstance(int(word), int):
                out['vis'] = int(word)
            elif word[-2:] == "KT":
                out['wind'] = word
                out['max_wind'] = word[-4:-2]
            elif len(word) == 6:
                clouds.append(word)
            else:
                out['wx'].append(word)
        out['clouds'] = self.cloud_analysis(clouds)
        return out


def main():
    '''
    blah
    '''
    eg_taf = get_taf_as_dict(EXAMPLE)
    for key, _ in eg_taf.iteritems():
        if key != 0:
            eg_class = TafGroup(get_taf_as_dict(EXAMPLE)[key])
            print eg_class
        else:
            eg_class = TafGroup(get_taf_as_dict(EXAMPLE)[key][2:], is_base=True)
            print eg_class

if __name__ == "__main__":
    main()
