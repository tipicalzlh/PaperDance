
def get_initial_keyword():
    """
    Get the initial keyword from the user
    """
    # This function should be replaced with the actual implementation
    # For now, we will just return a list of keywords
    return ["machine learning", "operation system", "computer network"]


def get_feedback(paper):
    """
    Get feedback from the user
    """
    # This function should be replaced with the actual implementation
    # For now, we use python interactive input
    feedback = input(f"\nDo you like the paper <{paper}>? (1 like/2 unlike/9 follow/0 exit): ")
    if feedback == "1":
        return "like"
    elif feedback == "2":
        return "unlike"
    elif feedback == "9":
        return "follow"
    elif feedback == "0":
        return "exit"
    else:
        print("Invalid input. Please enter 1, 2, 9, or 0.")
        # You can also raise an exception or handle it in another way
    return feedback