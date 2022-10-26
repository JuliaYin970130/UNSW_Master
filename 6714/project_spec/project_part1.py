import numpy as np
import heapq


class Node:
    def __init__(self, score, docid):
        self.score = score
        self.docid = docid

    def __lt__(self, other):
        if self.score == other.score:
            return self.docid > other.docid
        else:
            return self.score < other.score

    def __str__(self):
        return "(%s, %s)" % (self.score, self.docid)


def to_list(heap):
    return [(nd.score, nd.docid) for nd in heap]


def WAND_Algo(query_terms, top_k, inverted_index):
    U, c_w, candidate = [], [], []
    score = []
    for t in range(len(query_terms)):
        word = query_terms[t]
        for x in inverted_index[word]:
            for y in x:
                score.append(y)
        U.append(0 if len(inverted_index[word]) == 0 else max(score))
        # max([max(y) for y in x for x in a])
        # np.max([w[1] for w in inverted_index[word]]
        c_w.append(iter(inverted_index[word]))
        #         print(word, inverted_index[word])
        #         print(U[-1])
        try:
            candidate.append(next(c_w[-1]) + (t,))
        except:
            pass
    theta = float('-inf')
    ans, full_eval = [], 0
    while len(candidate) > 0:
        candidate.sort()
        score_limit, pivot = 0, 0
        while pivot < len(candidate):
            score_limit += U[candidate[pivot][2]]
            if score_limit > theta:
                break
            pivot = pivot + 1
        if score_limit <= theta:
            break
        #         print("pivot, theta, score, candidate:", pivot, theta, score_limit, candidate)
        if candidate[0][0] == candidate[pivot][0]:
            pivot_docid = candidate[pivot][0]
            #             print("***", pivot_docid)
            full_eval += 1
            s, t = 0, 0
            rm_idx = []
            while t < len(candidate) and candidate[t][0] == pivot_docid:
                s = s + candidate[t][1]
                try:
                    candidate[t] = next(c_w[candidate[t][2]]) + (candidate[t][2],)
                except:
                    rm_idx.append(t)
                t = t + 1
            cnt = 0
            for idx in rm_idx:
                del candidate[idx - cnt]
                cnt += 1
            if s > theta:
                if len(ans) < top_k:
                    heapq.heappush(ans, Node(s, pivot_docid))
                else:
                    if s > ans[0].score:
                        heapq.heappop(ans)
                        heapq.heappush(ans, Node(s, pivot_docid))
                    if len(ans) == top_k:
                        theta = ans[0].score
        else:
            new_candidate = []
            for t in range(pivot):
                flag = True
                while candidate[t][0] < candidate[pivot][0]:
                    try:
                        candidate[t] = next(c_w[candidate[t][2]]) + (candidate[t][2],)
                    except:
                        flag = False
                        break
                if flag:
                    new_candidate.append(candidate[t])
            candidate = new_candidate[:] + candidate[pivot:]
    #         print(to_list(ans))
    if len(ans) > 0:
        ans = to_list(ans)
        ans.sort(key=lambda x: x[1])
        ans.sort(key=lambda x: x[0], reverse=True)
    return ans, full_eval
