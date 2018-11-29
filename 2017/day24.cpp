#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>
#include <iomanip>

struct Port
{
    int id;
    int ports[2];

    int value() const
    {
        return this->ports[0] + this->ports[1];
    }
};

static int MAX_LENGTH = 0;
static int visit(int node, int side, int depth, int currValue, std::vector<bool>& visited,
                 std::unordered_map<int, std::vector<int>>& portsById, const std::vector<Port>& ports)
{
    if (visited[node]) return 0;
    visited[node] = true;

    if (depth >= MAX_LENGTH)
    {
        std::cout << depth << " " << currValue + ports[node].value() << std::endl;
        MAX_LENGTH = depth;
    }

    int value = 0;
    int connector = ports[node].ports[1 - side];
    for (auto other: portsById[connector])
    {
        auto& neighbour = ports[other];
        int targetSide = neighbour.ports[0] == connector ? 0 : 1;
        int val = visit(other, targetSide, depth + 1, currValue + ports[node].value(),
                        visited, portsById, ports) + ports[node].value();
        value = std::max(value, val);
    }

    visited[node] = false;
    return value;
}

static int findPath(int start, std::unordered_map<int, std::vector<int>>& portsById, const std::vector<Port>& ports)
{
    std::vector<bool> visited(ports.size(), false);
    return visit(start, 0, 1, 0, visited, portsById, ports);
}

void day24()
{
    std::fstream input("input.txt");
    std::string line;

    std::vector<Port> ports;
    std::unordered_map<int, std::vector<int>> portsById;
    while (std::getline(input, line))
    {
        int first = std::stoi(line.substr(0, line.find('/')));
        int second = std::stoi(line.substr(line.find('/') + 1));
		portsById[first].push_back(ports.size());
		portsById[second].push_back(ports.size());
        ports.push_back(Port{(int)ports.size(), {first, second}});
    }

    int maximum = 0;
    for (auto start: portsById[0])
    {
        maximum = std::max(maximum, findPath(start, portsById, ports));
    }

    std::cout << maximum << std::endl;
}
