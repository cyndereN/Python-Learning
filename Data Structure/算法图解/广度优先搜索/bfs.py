from typing import Deque


def search(name):
    search_queue = deque()
    search_queue += graph[name];
    searched = []

    while search_queue:
        person = search_queue.popleft()
        if person not in searched:
            if is_seller(person):
                print (person+"is a mango seller!")
                return True
            else:
                search_queue += graph[person]
                searched.append(person)
    return False
search(root)