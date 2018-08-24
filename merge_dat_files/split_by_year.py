#!/nfs/foe-data-32/export/ncas/lecjlg/Documents/anaconda3/bin/python

src_path = "output/"
main_file = "sorted.csv"
import csv
import collections
import pprint

with open(main_file, "r") as fp:
    root = csv.reader(fp, delimiter=',')
    result = collections.defaultdict(list)
    for row in root:
        year = row[0].split("-")[0]
        result[year].append(row)

#pprint.pprint(result)

for i,j in result.items():
    file_path = "%s%s.csv"%(src_path, i)
    with open(file_path, 'w') as fp:
        writer = csv.writer(fp, delimiter=',')
        writer.writerows(j)




