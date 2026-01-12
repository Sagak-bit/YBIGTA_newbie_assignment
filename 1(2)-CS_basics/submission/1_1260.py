# (BOJ) Skeleton Code Provided by YBIGTA

from __future__ import annotations
from collections import deque


"""
TODO:
- __init__ 구현하기
- add_edge 구현하기
- dfs 구현하기 (재귀 또는 스택 방식 선택)
- bfs 구현하기
"""


class Graph:
    def __init__(self, n: int) -> None:
        """
        그래프 초기화
        n: 정점의 개수 (1번부터 n번까지) (0-based)
        """
        self.n = n
        self.edge: list[list[int]] = [[] for _ in range(n)]
    
    def add_edge(self, u: int, v: int) -> None:
        """
        양방향 간선 추가
        """
        self.edge[u - 1].append(v - 1)
        self.edge[v - 1].append(u - 1)
        pass
    
    def dfs(self, start: int) -> list[int]:
        """
        깊이 우선 탐색 (DFS)
        
        [구현 방법] 스택 방식: 명시적 스택을 사용하여 반복문으로 구현
        """
        # dfs path to return
        path: list[int] = []

        # visit the smallest vertex first
        for i in range(len(self.edge)):
            self.edge[i].sort(reverse=True)
        
        # array to check if the i-th vertex is visited
        visited = [False] * self.n

        # dfs via stack
        stack = [start - 1]
        while stack:
            # visit the next vertex
            top = stack.pop()
            
            # defensive coding
            if not visited[top]:
                visited[top] = True
                path.append(top + 1)

                # add vertices to the stack
                for neighbor in self.edge[top]:
                    if not visited[neighbor]:
                        stack.append(neighbor)
        
        # return the dfs path order
        return path
    
    def bfs(self, start: int) -> list[int]:
        """
        너비 우선 탐색 (BFS)
        큐를 사용하여 구현
        """
        # bfs path to return
        path: list[int] = []

        # visit the smallest vertex first
        for i in range(len(self.edge)):
            self.edge[i].sort()

        # array to check if the i-th vertex is visited
        visited = [False] * self.n

        # set initial value
        path.append(start)
        visited[start - 1] = True
        dq:deque[int] = deque([start - 1])

        # bfs via queue
        while dq:
            top = dq.popleft()
            
            # append neighbors to the queue
            for neighbor in self.edge[top]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    path.append(neighbor + 1)
                    dq.append(neighbor)

        # return the bfs path order
        return path
    
    def search_and_print(self, start: int) -> None:
        """
        DFS와 BFS 결과를 출력
        """
        dfs_result = self.dfs(start)
        bfs_result = self.bfs(start)
        
        print(' '.join(map(str, dfs_result)))
        print(' '.join(map(str, bfs_result)))


from typing import Callable
import sys


"""
-아무것도 수정하지 마세요!
"""


def main() -> None:
    intify: Callable[[str], list[int]] = lambda l: [*map(int, l.split())]

    lines: list[str] = sys.stdin.readlines()

    N, M, V = intify(lines[0])
    
    graph = Graph(N)  # 그래프 생성
    
    for i in range(1, M + 1): # 간선 정보 입력
        u, v = intify(lines[i])
        graph.add_edge(u, v)
    
    graph.search_and_print(V) # DFS와 BFS 수행 및 출력


if __name__ == "__main__":
    main()
