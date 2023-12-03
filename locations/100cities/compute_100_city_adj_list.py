import json
import networkx as nx


def make_adj_list(n):
    data = json.load(open('DistanceMatrix.json'))
    distance_matrix = data['distances']
    city_index_to_name = data['cities']

    ans = dict()

    for i, row in enumerate(distance_matrix):
        city1 = city_index_to_name[i]['name'] + ', ' + city_index_to_name[i]['state']
        if city1 not in ['Honolulu, HI', 'Anchorage, AK'] :
            filtered_row = [(j, entry) for j, entry in enumerate(row) if 'status' in entry and entry['status']=='OK']
            filtered_row.sort(key=lambda x: x[1]['distance']['inMeters'])
            topn = filtered_row[:n]
            topn = [
                {
                    'name': city_index_to_name[j]['name'] + ', ' + city_index_to_name[j]['state'],
                    'distanceInMeters': entry['distance']['inMeters'],
                    'duration': entry['duration']['humanReadable']
                }
                for (j, entry) in topn
            ]
            ans[city1] = topn

    return ans


def check_if_connected(adj_list):
    G = nx.Graph()
    for city1 in adj_list:
        for entry in adj_list[city1]:
            city2 = entry['name']
            G.add_edge(city1, city2)
    return nx.is_connected(G), nx.connected_components(G)


if __name__ == '__main__':
    # for i in range(1, 101):
    #     test = make_adj_list(i)
    #     check, components = check_if_connected(test)
    #     if check:
    #         print(i, True)
    #         break
    #     print(i, False)
    #     for comp in components:
    #         print(comp)
    adj_list = make_adj_list(6)
    f = open('100cities_closest_n_adj_list.json', 'w')
    json.dump(adj_list, f, indent=4)