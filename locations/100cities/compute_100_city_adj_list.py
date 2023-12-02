import json
import networkx as nx


def make_adj_list(n):
    data = json.load(open('DistanceMAtrix.json'))
    distance_matrix = data['distances']
    city_index_to_name = data['cities']

    ans = dict()

    for i, row in enumerate(distance_matrix):
        city1 = city_index_to_name[i]['name'] + ', ' + city_index_to_name[i]['state']
        if city1 != 'Honolulu, HI':
            filtered_row = [(j, entry) for j, entry in enumerate(row) if 'status' in entry and entry['status']=='OK']
            filtered_row.sort(key=lambda x: x[1]['distance']['inMeters'])
            top5 = filtered_row[:n]
            top5 = [
                {
                    'name': city_index_to_name[j]['name'] + ', ' + city_index_to_name[j]['state'],
                    'distanceInMeters': entry['distance']['inMeters'],
                    'duration': entry['duration']['humanReadable']
                }
                for (j, entry) in top5
            ]
            ans[city1] = top5

    return ans

def check_if_connected(adj_list):
    G = nx.Graph()
    for city1 in adj_list:
        for entry in adj_list[city1]:
            city2 = entry['name']
            G.add_edge(city1, city2)
    return nx.is_connected(G)


if __name__ == '__main__':
    # for i in range(1, 101):
    #     test = make_adj_list(i)
    #     if check_if_connected(test):
    #         print(i, True)
    #         break
    #     print(i, False)
    adj_list = make_adj_list(6)
    f = open('100cities_closest_n_adj_list.json', 'w')
    json.dump (adj_list, f)
    