import json


def gen_leonard_numbers(num: int) -> list:
    num1 = num2 = 1
    res = []
    while num1 <= num:
        res.append(num1)
        num1 = num2
        num2 = num1 + res[-1] + 1
    return res


def update_heap(lst: list, p: int, k: int, leonard_nums: list):

    if k >= 2:
        kr = k - 2
        kl = k - 1
        tr = p - 1
        tl = tr - leonard_nums[kr]
        if lst[p][0] < lst[tl][0] or lst[p][0] < lst[tr][0]:
            if lst[tl][0] < lst[tr][0]:
                lst[p], lst[tr] = lst[tr], lst[p]
                update_heap(lst, tr, kr, leonard_nums)
            else:
                lst[p], lst[tl] = lst[tl], lst[p]
                update_heap(lst, tl, kl, leonard_nums)


def sort_list(lst: list) -> list:
    leonard_nums = gen_leonard_numbers(len(lst))
    heap_stack = []
    for i in range(len(lst)):
        fl = True
        if len(heap_stack) >= 2:
            k1 = heap_stack.pop()
            k2 = heap_stack[-1]
            if k2 == k1 + 1:
                heap_stack[-1] += 1
                update_heap(lst, i, k2+1, leonard_nums)
                fl = False
            else:
                heap_stack.append(k1)
        if len(heap_stack) >= 1 and fl:
            k = heap_stack[-1]
            if k == 1:
                heap_stack.append(0)
                fl = False
        if fl:
            heap_stack.append(1)

    for i in range(len(lst)-1, 0, -1):
        mx = lst[i][0]
        ind_mx = i
        k_mx = 0
        k = -1
        for j in heap_stack:
            k += leonard_nums[j]
            if lst[k][0] > mx:
                mx = lst[k][0]
                ind_mx = k
                k_mx = j
        if i != ind_mx:
            lst[i], lst[ind_mx] = lst[ind_mx], lst[i]
            update_heap(lst, ind_mx, k_mx, leonard_nums)
        if heap_stack[-1] > 1:
            st1 = heap_stack[-1]
            heap_stack[-1] -= 1
            heap_stack.append(st1 - 2)
        else:
            heap_stack.pop()

    return lst


def data_to_int(dt: str) -> int:
    return int(dt.replace('-', '', 2))


def check_capacity(max_capacity: int, guests: list) -> bool:
    results = []
    tmp = 0
    for guest in guests:
        results.append([data_to_int(guest['check-in']), 1])
        results.append([data_to_int(guest['check-out']), -1])

    sort_list(results)
    for res in results:
        tmp += res[1]
        if tmp > max_capacity:
            return False
    return True


if __name__ == "__main__":
    # Чтение входных данных
    max_capacity = int(input())
    n = int(input())


    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)


    result = check_capacity(max_capacity, guests)
    print(result)
