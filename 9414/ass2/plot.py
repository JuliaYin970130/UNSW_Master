import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('articles.tsv', sep='\t',
                   header=None, quoting=csv.QUOTE_NONE)
topics = np.array(data[2])

# plot the distribution of topics
topic_dict = {}
for i in topics:
    if i not in topic_dict:
        topic_dict[i] = 1
    else:
        topic_dict[i] += 1

topic_classes = sorted(topic_dict.keys())
topic_classes_number = []
for c in topic_classes:
    topic_classes_number.append(topic_dict[c])
print(topic_classes)
print(topic_classes_number)
x = np.arange(len(topic_classes))

plt.xlabel('Topic')
plt.ylabel('Frequency')
plt.title('Frequency distribution over topics')
plt.bar(x, topic_classes_number)
plt.xticks(x, topic_classes, size='xx-small')
for a, b in zip(x, topic_classes_number):
    plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom', fontsize=8)
plt.tight_layout()
plt.savefig('topic_distribution.png')
plt.show()
