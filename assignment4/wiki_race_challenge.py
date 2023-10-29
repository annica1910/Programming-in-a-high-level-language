from typing import List  # isort:skip
from filter_urls import find_articles
from requesting_urls import get_html
from queue import Queue

def find_path(start: str, finish: str) -> List[str]:
    """Find the shortest path from `start` to `finish`

    Arguments:
      start (str): wikipedia article URL to start from
      finish (str): wikipedia article URL to stop at

    Returns:
      urls (list[str]):
        List of URLs representing the path from `start` to `finish`.
        The first item should be `start`.
        The last item should be `finish`.
        All items of the list should be URLs for wikipedia articles.
        Each article should have a direct link to the next article in the list.
    """
    distance_dict = {}

    visited = []
    Q = Queue()
    Q.put([start])
    while not Q.empty():
        path = Q.get()
        if len(path) > 7:
            print("Too many in path")
            continue
        current_page = path[-1]
        if not current_page in visited:
            visited.append(current_page)
            print("Visiting ", current_page)
            articles = find_articles(get_html(current_page))
            for next_page in articles:
                new_path = list(path)
                new_path.append(next_page)
                Q.put(new_path)
                if next_page == finish:
                    return new_path
        
    print("There's no path between the 2 articles")
    return []

if __name__ == "__main__":
    start = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    finish = "https://en.wikipedia.org/wiki/Peace"
    path = find_path(start, finish)
    print(path)
    # assert path[0] == start
    # assert path[-1] == finish
