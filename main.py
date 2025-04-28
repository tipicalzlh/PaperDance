from LLM_utils import *
from ranker import *
from arxiv_api import *
from frontend import *

import random
import math

def rm_paper_redundant(candidate, rcm_history):
    rcm_his_set = set(rcm_history)
    candidate[:] = [a for a in candidate if extract_title(a) not in rcm_his_set]


def recommend(mode, model, keywords, his_rcm, refer_paper=None):
    """
    Recommend a paper based on the reference paper and mode
    """
    candidate_paper = []
    # first prepare candidate paper list
    if len(keywords) >= 5:
        kw_batch = random.sample(keywords, 5)  
    else:
        kw_batch = keywords.copy()
        random.shuffle(kw_batch)
    
    print(f"fetching paper from: <{kw_batch}>")
    for keyword in kw_batch:
        candidate_paper.extend(arxiv_fetch(keyword, max_results=5))
    candidate_paper = list(set(candidate_paper))
    rm_paper_redundant(candidate_paper, his_rcm)
    # rank the candidate paper
    if mode == 1 and refer_paper is not None and len(refer_paper) > 5:
        score = get_score(model, refer_paper, candidate_paper)
    elif mode == 1 or mode == 2: 
        score = get_score(model, keywords, candidate_paper)
    else:
        print("Invalid mode. Please provide '1'(liked) or '2'(following).")
        return
    
    # score = parse_llm(score_text, "score")
    top_id = sorted(score, key=lambda x: x[1]+math.sqrt(x[2]), reverse=True)[:5]
    
    probs = [0.4, 0.25, 0.2, 0.1, 0.05]
    sampled = random.choices(list(range(5)), weights=probs, k=1)[0] #randomly pick paper from top5
    return candidate_paper[top_id[sampled][0]]


def main():
    keyword_liked, keyword_following, paper_liked = [], [], []
    his_rcm = []  # history of recommended paper, to avoid repeated recommendation

    init_kw = get_initial_keyword()  #from frontend
    keyword_liked.extend(init_kw)
    keyword_following.extend(init_kw)


    genai.configure(api_key="AIzaSyBUIHQSPqqLuFlZ8iJUGHZ2QJY5RpDBXHc")
    # model = genai.GenerativeModel("gemini-1.5-flash")
    model = genai.GenerativeModel("gemini-2.0-flash")

    mode = 2
    while True:
        if mode == 1:
            paper_rcm = recommend(1, model, keyword_liked, his_rcm, paper_liked)
        elif mode == 2:
            paper_rcm = recommend(2, model, keyword_following, his_rcm)
        his_rcm.append(extract_title(paper_rcm))
        fdbk = get_feedback(his_rcm[-1])  # from frontend
        if fdbk == "like":
            # paper_liked.append(paper_rcm)
            kw_curr = get_keyword(model, paper_rcm) # get current keyword
            update_liked(kw_curr, paper_rcm, keyword_liked, paper_liked)
        elif fdbk == "follow":
            kw_curr = get_keyword(model, paper_rcm)
            update_following(kw_curr, keyword_following)
        elif fdbk == "unlike":
            pass
        elif fdbk == "exit":
            break
        else:
            # handle other possible cases
            pass


if __name__ == "__main__":
    main()