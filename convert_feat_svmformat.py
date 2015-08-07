import sys
import struct
import os
from random import shuffle

feat_dir = sys.argv[1]
score_list_name = sys.argv[2]
score_dict = {}
feat_type = '.fc7'

print 'Read features from', feat_dir , 'with format:', feat_type
print 'genderate score according to', score_list_name

def upack_feature(filename):
    fd = open(filename, 'rb')
    n = struct.unpack('i', fd.read(4))[0]
    c = struct.unpack('i', fd.read(4))[0]
    l = struct.unpack('i', fd.read(4))[0]
    h = struct.unpack('i', fd.read(4))[0]
    w = struct.unpack('i', fd.read(4))[0]
    fc = []
    for i in range(n * c):
        feat = struct.unpack('f', fd.read(4))[0]
        fc.append(feat)
    return fc

def binary_label(s):
    score = float(s)
    if score >= .99:
        return '+1'
    else:
        return '-1'

def feat_svm_format (feat_list):
    tmpS = ''
    i = 0
    # convert to svm format and save as the file
    for i in range(0, len(feat_list)):
        tmpS += str(i+1) + ':' + str(feat_list[i]) + ' '
    return tmpS

# create the dict of score
with open(score_list_name) as f:
    file_content = f.readlines()
for line in file_content:
    line_list = line.split(' ')
    path = line_list[0]
    prefix = path.split('/')[-2].split('-')[1]
    clip_num = line_list[1]
    score = line_list[2].rstrip('\n')
    key = prefix + '-' + clip_num
    score_dict[key] = score

# traverse the dir and extract the feature name
output_name = 'svm_input'
output = open(output_name, 'w+')
output_list = []
for root, dirs, files in os.walk(feat_dir):
    for f in files:
        if f.endswith(feat_type):
            feat_name = f.split('.')[0]
            feat = upack_feature(root + f)
            svm_feat = feat_svm_format(feat)
            score = score_dict[feat_name]
            label = binary_label(score)
            line = label + ' ' + svm_feat + '\n'
            output_list.append(line)
            output.write(line)
print 'Done, all features saved in', output_name
output.close()

output_train = open(output_name + '_train', 'w+')
output_test  = open(output_name + '_test', 'w+')

shuffle(output_list)
total_num = len(output_list)
test_num = total_num /4
train_num = total_num - test_num
train = output_list[:train_num]
test  = output_list[train_num:]
for item in train:
    output_train.write('%s' % item)
for item in test:
    output_test.write('%s' % item)
output_train.close(), output_test.close()
