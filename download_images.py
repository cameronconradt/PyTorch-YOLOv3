import json
import urllib.request

namedict = {'Player': 0, 'Asteroid': 1, 'Shot': 2, 'Score': 3, 'Lives': 4}
labeldir = 'data/custom/labels/'
imagesdir = 'data/custom/images/'
customdir = 'data/custom/'

with open('Asteroids.json', 'r') as json_file:
    line = json_file.readline()
    count = 1
    output = {'imgs': []}
    trainset = open(customdir + 'train.txt', 'w')
    validset = open(customdir + 'valid.txt', 'w')
    while line:
        data = json.loads(line)
        urllib.request.urlretrieve(data['content'], imagesdir + str(count) + '.jpg')
        annotations = open(labeldir + str(count) + '.txt', 'w')
        for label in data['annotation']:
            points = label['points']
            pos = namedict[label['label'][0]]
            xtot = 0
            ytot = 0
            xmax = 0
            ymax = 0
            xmin = 1
            ymin = 1
            for point in points:
                if point[0] is not None:
                    xtot += point[0]
                    ytot += point[1]
                    if point[0] > xmax:
                        xmax = point[0]
                    elif point[0] < xmin:
                        xmin = point[0]
                    if point[1] > ymax:
                        ymax = point[1]
                    elif point[1] < ymin:
                        ymin = point[1]
            xavg = xtot / len(points)
            yavg = ytot / len(points)
            xheight = xmax - xmin
            yheight = ymax - ymin
            if xavg != 0:
                annotations.write(str(pos) + " " + str(xavg) + " " + str(yavg) + " " + str(xheight) + " " + str(yheight) + "\n")
        data['content'] = str(count) + '.jpg'
        if count % 5 == 0:
            validset.write(imagesdir + str(count) + '.jpg' + '\n')
        else:
            trainset.write(imagesdir + str(count) + '.jpg' + '\n')
        output['imgs'].append(data)
        line = json_file.readline()
        count += 1
    # json_out = open('Asteroids_processed.json', 'w')
    # json.dump(output, json_out)
