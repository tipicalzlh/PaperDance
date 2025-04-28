import arxiv

def arxiv_fetch(query, max_results=10):
    papers = []
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    for res in search.results():
        papers.append({
            'title': res.title,
            'authors': ", ".join(str(a) for a in res.authors),
            'abstract': f"Published: {res.published.date()}\n\n" + res.summary + f"\nLink: arXiv:{res.entry_id}"
        })
    return papers

if __name__ == "__main__":
    arxiv_fetch()