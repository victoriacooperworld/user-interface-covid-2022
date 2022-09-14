import heapq


heap = []
heap_size = 5
test= [1,2,3,4,5,6,7,9,0,10,90]
for k in test:
    heapq.heappush(heap,-k)
    if len(heap)>heap_size:
        heapq.heappop(heap)
print(heap)