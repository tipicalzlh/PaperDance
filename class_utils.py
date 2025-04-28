from sentence_transformers import SentenceTransformer
import ast
class BertRanker:
    '''
        # Load the model
        model = SentenceTransformer("malteos/scincl")

        # Concatenate the title and abstract with the [SEP] token
        papers = [
            "BERT [SEP] We introduce a new language representation model called BERT",
            "Attention is all you need [SEP] The dominant sequence transduction models are based on complex recurrent or convolutional neural networks",
        ]
        # Inference
        embeddings = model.encode(papers)

        # Compute the (cosine) similarity between embeddings
        similarity = model.similarity(embeddings[0], embeddings[1])
        print(similarity.item())
        # => 0.8440517783164978
    '''

    def __init__(self, model_path = "malteos/scincl"):
        self.model = SentenceTransformer(model_path)
        self.sim_fn = self.model.similarity
    
    def rank(self, query_list, candidate_pool):
        '''
            For keyword query:
                query_list is a list of strings, each string is a keyword. For example, query = ['operation system', 'machine learning', 'computer network']
                candidate_pool is a list of dictionary of {"title" : "paper_title", "Abstract" : "paper_abstract"}
            For full paper query:
                both query_list and candidate_pool are list of dictionary of {"title" : "paper_title", "Abstract" : "paper_abstract"}
        '''
        papers = []
        for c in candidate_pool:
            papers.append(f"{c['title']} [SEP] {c['Abstract']}")
        querys = []
        for q in query_list:
            if isinstance(q, dict) :
                querys.append(f"{q['title']} [SEP] {q['Abstract']}")
            else:
                querys.append(q)

        embeddings_c = self.model.encode(papers)
        embeddings_k = self.model.encode(querys)
        result = []
        for id, c in enumerate(embeddings_c):
            max_score = 0.0
            for k in embeddings_k:
                sim = self.sim_fn(c, k)
                max_score = max(sim, max_score) # match the best query for each paper
            result.append((id, max_score, 0))
        
        return result

def extract_title_and_abstract(text):
    # input format: f"title: {result.title}, abstract: {result.summary};"
    if isinstance(text, str):
        # Try evaluating as a dict literal
        try:
            obj = ast.literal_eval(text)
            if isinstance(obj, dict):
                return obj.get('title'), obj.get('abstract')
        except Exception:
            pass

def get_score_bert(model, query_list, candidate_pool):
    
    if extract_title_and_abstract(query_list[0]):
        _query = []
        for q in query_list:
            title, abs = extract_title_and_abstract(q)
            _query.append({
                "title": title,
                "Abstract" : abs
            })
    else:
        _query = query_list
    
    _cd = []
    for c in candidate_pool:
        title, abs = extract_title_and_abstract(c)
        _cd.append({
            "title": title,
            "Abstract" : abs
        })

    print(_query, _cd)
    return model.rank(_query, _cd)

