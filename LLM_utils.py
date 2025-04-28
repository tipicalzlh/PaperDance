from arxiv_api import *
import google.generativeai as genai


def get_keyword(model, paper_list):
    prompt = f"""
        You are a helpful research assistant that're good at paper summary. 
        You are given titles and abstracts of a set of papers, and you need to summary three keywords for each of them: \n
        {paper_list}
        Answer the keywords only, separate different paper with semicolon.
        Example: Reinforcement Learning, Large Language Models, Down-Sampling; Vision-language model, policy optimization, knowledge distillation
    """

    response = model.generate_content(prompt)
    # print(response.text)
    return parse_llm(response.text, "keyword")

def get_score(model, query_list, candidate_pool):
    prompt = f"""
    You are a helpful research assistant that helps researchers find relevant papers.
    You are given a set of keywords/papers that the user is interested in, and you need to select a new paper 
        to be recommended to the user from candidate papers.

    keywords/papers that the user is interested in: "{query_list}"

    Candidate Papers:
    {candidate_pool}

    which paper is more relevant to the user's interest?
    Answer for each paper without any explanation or words, in the following format: index(starting from 0), similarity score(0-10), your confidence(0-1).
    do not include '\n'
    Example: 0, 8, 0.9; 1, 7, 0.3; 2, 5, 0.6
    """
    response = model.generate_content(prompt)
    # print(response.text)
    return parse_llm(response.text, "score")

def parse_llm(output_text, mode):
    result, index = [], 0
    entries = output_text.strip().split(';')
    for entry in entries:
        if entry.strip():
            parts = entry.strip().split(',')
            if len(parts) == 3:
                if mode == "keyword":
                    result.extend([parts[0].strip(), parts[1].strip(), parts[2].strip()])
                elif mode == "score":
                    # Assuming the format is "index, score, confidence"
                    # index = int(parts[0].strip()) #in case index is wrong, not used
                    score = int(parts[1].strip())
                    confidence = float(parts[2].strip())
                    result.append((index, score, confidence))
                    index += 1
            else:
                print(parts)
                print(f"Unexpected format in entry: {entry}")
    return result

def extract_title(text):
    # input format: f"title: {result.title}, abstract: {result.summary};"
    prefix = "title:"
    sep = ", abstract:"
    
    start = text.find(prefix)
    end = text.find(sep)
    
    if start != -1 and end != -1:
        title = text[start + len(prefix):end].strip()
        return title
    return None


# query = ["Second-order Optimization of Gaussian Splats with Importance Sampling", 
#          "Hessian stability and convergence rates for entropic and Sinkhorn potentials via semiconcavity",
#          "Wasserstein Distributionally Robust Regret Optimization"]
# paper = ["Multi-objective Bayesian Optimization With Mixed-categorical Design Variables for Expensive-to-evaluate Aeronautical Applications",
#          "Existence and smoothness of density function of solution to Mckean--Vlasov Equation with general coefficients", 
#          "Stochastic Momentum ADMM for nonconvex and nonsmooth optimization with application to PnP algorithm", 
#          "Efficient Swept Volume-Based Trajectory Generation for Arbitrary-Shaped Ground Robot Navigation"]



