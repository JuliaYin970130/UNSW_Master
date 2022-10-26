import re

from nltk import word_tokenize
tokens = 'Benitez to launch Morientes bid  Liverpool may launch an 8m January bid for longtime target Fernando Morientes according to reports  The Real Madrid striker has been linked with a move to Anfield since the summer and is currently behind Raul Ronaldo and Michael Owen at the Bernabeu Liverpool boss Rafael Benitez is keen to bolster his forward options with Djibril Cisse out until next season If there is an attractive propostition it could be I would be keen to leave admitted the 28yearold Morientes He added Unfortunately Im not in control of the situation Im under contract to Real and they will make any decisions The fee could put Liverpool off a prospective deal but Real are keen to net the cash as they are reported to be preparing a massive summer bid for Inter Milan striker Adriano The Reds are currently sixth in the Premiership 15 points behind leaders Chelsea'

t = 'wwwsupport.apple.com/zh-cn/guide/numbers/tan71c6a7a38/mac !2323'


token = re.sub('^((www.)\S+)','',t)
# token = ''
# list = t.split(' ')
# for i in list:
#     # print(i)
#     if "www." in i:
#         continue
#     else:
#         token += i + ' '

print(token)



# result = ''
# for i in tokens:
#     if ".com" in i:
#         continue
#     else:
#         result += i + ' '
#
# print(result)


