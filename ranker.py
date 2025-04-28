from LLM_utils import *

def update_liked(keyword, paper, keyword_liked, paper_liked):
    """
    Update the liked paper list
    """
    max_size = 10
    assert isinstance(paper, str), f"paper should be string, but got {type(paper)}"
    assert isinstance(keyword, list), f"keyword should be list, but got {type(keyword)}"
    assert isinstance(keyword[0], str), f"keyword should be list of strings, but got {type(keyword[0])}"
    keyword_liked.extend(keyword)
    paper_liked.append(paper)
    print(f"Paper <{extract_title(paper)}> added to liked list.")
    
    if len(keyword_liked) > 3* max_size:
        del keyword_liked[:(len(keyword_liked) - 3* max_size)]
    if len(paper_liked) > max_size:
        del paper_liked[:(len(paper_liked) - max_size)]

def update_following(keyword, keyword_following):
    """
    Update the following paper list
    """
    if isinstance(keyword, str):
        keyword_following.append(keyword)
    elif isinstance(keyword, list):
        keyword_following.extend(keyword)
    else:
        print("Invalid keyword type. Please provide a string or a list of strings.")
    
    
