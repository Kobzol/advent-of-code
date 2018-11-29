#pragma once

#include <fstream>
#include <string>
#include <iostream>
#include <vector>
#include <unordered_set>
#include <queue>
#include <tuple>
#include <algorithm>
#include <unordered_map>

class GraphVertex
{
public:
	int id;
	int x;
	int y;
	std::vector<GraphVertex*> edges;
};

int bfs(const std::vector<std::string>& graph, int startX, int startY, int destination)
{
	std::unordered_set<std::string> visited;
	std::queue<std::tuple<int, int, int>> queue;
	queue.push(std::tuple<int, int, int>{startX, startY, 0});
	visited.insert(std::to_string(startX) + "#" + std::to_string(startY));

	int positions[4][2] = {
		{0, 1},
		{1, 0},
		{0, -1},
		{-1, 0}
	};

	while (!queue.empty())
	{
		std::tuple<int, int, int> node = queue.front();
		queue.pop();

		for (int i = 0; i < 4; i++)
		{
			int newX = std::get<0>(node) + positions[i][0];
			int newY = std::get<1>(node) + positions[i][1];

			if (newX >= 0 && newX < graph.size() && newY >= 0 && newY < graph[0].size() && !visited.count(std::to_string(newX) + "#" + std::to_string(newY)) && graph[newX][newY] != '#')
			{
				visited.insert(std::to_string(newX) + "#" + std::to_string(newY));
				queue.push({ newX, newY, std::get<2>(node) + 1 });
			}

			if (graph[newX][newY] == destination + '0')
			{
				return std::get<2>(node) + 1;
			}
		}
	}

	return -1;
}

void day24()
{
	std::fstream fs("input.txt", std::ios::in);

	const int verticesCount = 8;

	GraphVertex vertices[verticesCount];
	std::vector<std::string> graph;

	std::string row;
	while (std::getline(fs, row))
	{
		for (size_t i = 0; i < row.size(); i++)
		{
			if (isdigit(row[i]))
			{
				vertices[row[i] - '0'] = GraphVertex{ row[i] - '0', (int) graph.size(), (int) i };
			}
		}
		graph.push_back(row);
	}

	std::vector<int> nodes;
	for (size_t i = 1; i < verticesCount; i++)
	{
		nodes.push_back((int) i);
	}

	std::unordered_map<std::string, int> distances;

	int steps = INT_MAX;
	do
	{
		if (!distances.count("0#" + std::to_string(nodes[0])))
		{
			distances["0#" + std::to_string(nodes[0])] = bfs(graph, vertices[0].x, vertices[0].y, nodes[0]);
		}
		int currentSteps = distances["0#" + std::to_string(nodes[0])];

		for (int i = 0; i < nodes.size() - 1; i++)
		{
			if (!distances.count(std::to_string(nodes[i]) + "#" + std::to_string(nodes[i + 1])))
			{
				distances[std::to_string(nodes[i]) + "#" + std::to_string(nodes[i + 1])] = bfs(graph, vertices[nodes[i]].x, vertices[nodes[i]].y, nodes[i + 1]);
			}
			currentSteps += distances[std::to_string(nodes[i]) + "#" + std::to_string(nodes[i + 1])];
		}

		if (!distances.count(std::to_string(nodes[nodes.size() - 1]) + "#0"))
		{
			distances[std::to_string(nodes[nodes.size() - 1]) + "#0"] = bfs(graph, vertices[nodes[nodes.size() - 1]].x, vertices[nodes[nodes.size() - 1]].y, 0);
		}
		currentSteps += distances[std::to_string(nodes[nodes.size() - 1]) + "#0"];

		steps = std::min(steps, currentSteps);
	} while (std::next_permutation(nodes.begin(), nodes.end()));

	std::cout << steps << std::endl;
}