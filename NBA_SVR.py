from sklearn import svm
import base64
import requests
import json
import matplotlib.pyplot as plt
import numpy as np



def current_season_stat():
    data = []
    name_list = []
    # Request
    try:
        response = requests.get(
            url="https://api.mysportsfeeds.com/v1.2/pull/nba/2018-2019-regular/overall_team_standings.json",
            params={
                "fordate": "20190512"
            },
            headers={
                "Authorization": "Basic " + base64.b64encode('{}:{}'.format("96c5a8df-8829-4b52-ac58-2b04cb","sandy34").encode('utf-8')).decode('ascii')
            }
        )

        content = json.loads(response.content)
        for team in content["overallteamstandings"]["teamstandingsentry"]:

            name = team["team"]["Name"]
            fgpct = team["stats"]["FgPct"]["#text"]
            threeptspct = team["stats"]["Fg3PtPct"]["#text"]
            plusMinus = team["stats"]["PlusMinusPerGame"]["#text"]
            blk = team["stats"]["BlkPerGame"]["#text"]
            stl = team["stats"]["StlPerGame"]["#text"]
            reb = team["stats"]["RebPerGame"]["#text"]
            ft = team["stats"]["FtPct"]["#text"]
            ast = team["stats"]["AstPerGame"]["#text"]
            wins = team["stats"]["Wins"]["#text"]

            data.append([float(wins), float(fgpct), float(threeptspct), float(ast), float(plusMinus)])
            name_list.append(name)

        return data, name_list

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def read_previous__seasons_data():
    fr = open("nba_stat.txt", "r")
    lines = fr.readlines()

    print len(lines)

    train_list = []
    label_list = []

    for data in lines[1:]:
        lines = data.split("\t")
        fgpct = lines[8]
        three_pct = lines[11]
        free_pct = lines[14]
        reb = lines[17]
        ast = lines[18]
        stl = lines[20]
        blk = lines[21]
        plus_min = lines[25]
        label = lines[26]

        train_list.append([float(lines[1]), float(fgpct), float(three_pct), float(ast), float(plus_min)])
        label_list.append(float(label))

        # print '2%: ' + lines[8] + '\t3%: ' + lines[11] + '\tF%: ' + lines[14] + '\treb: ' + lines[17] + '\tast: ' + \
        #   lines[18] + '\tstl: ' + lines[20] + '\tblk: ' + lines[21] + '\tplus: ' + lines[25] + '\tlabel: ' + lines[26]

    fr.close()

    return train_list, label_list


def scatter_plots():
    print 'scatter plot'
    plt.xlabel('How far did the team go')
    plt.ylabel('Wins (games)')

    fr = open("nba_stat.txt", "r")
    lines = fr.readlines()

    wins = []
    ylabel = []

    print len(lines)

    for data in lines[1:]:
        lines = data.split("\t")
        fg_pct = lines[8]
        three_pct = lines[11]
        free_pct = lines[14]
        reb = lines[17]
        ast = lines[18]
        stl = lines[20]
        blk = lines[21]
        plus_min = lines[25]
        label = lines[26]

        wins.append(float(lines[1]))
        ylabel.append(float(label))

    area = np.pi * 3
    plt.scatter(ylabel, wins, s=area, alpha=0.8)
    plt.show()


def main():

    # scatter_plots()

    train, label = read_previous__seasons_data()
    clf = svm.SVR(gamma='auto')
    clf.fit(train, label)

    predict_data, name = current_season_stat()
    results = clf.predict(predict_data)

    map = []
    for x in range(0, len(results)):
        # print 'Name: ' + name[x] + '\tScore: ' + str(results[x])
        map.append([name[x], results[x]])

    map = sorted(map, key=lambda i: i[1], reverse=True)

    for teams in map[:8]:
        print 'Name: ' + teams[0] + '\t\tScore: ' + str(teams[1])


main()

