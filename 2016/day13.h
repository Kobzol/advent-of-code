#pragma once

#include <iostream>
#include <string>
#include <queue>
#include <unordered_set>

struct GraphNode
{
	int x, y, distance;
};

int popcnt(int number)
{
	int count = 0;

	while (number > 0)
	{
		count++;
		number &= number - 1;
	}

	return count;
}
int isOpenSpace(int x, int y, int magicNumber)
{
	return popcnt(x * x + 3 * x + 2 * x * y + y + y * y + magicNumber) % 2 == 0;
}
std::string hashPos(int x, int y)
{
	return std::to_string(x) + "-" + std::to_string(y);
}

int bfs(int targetX, int targetY, int magicNumber)
{
	std::queue<GraphNode> nodes;
	nodes.push(GraphNode{ 1, 1, 0 });

	std::unordered_set<std::string> visited;
	visited.insert(hashPos(nodes.front().x, nodes.front().y));

	int positions[4][2] = {
		{-1, 0},
		{0, -1},
		{1, 0},
		{0, 1}
	};

	while (!nodes.empty())
	{
		GraphNode node = nodes.front();
		nodes.pop();

		if (node.distance >= 50) continue;

		for (int i = 0; i < 4; i++)
		{
			int posX = node.x + positions[i][0];
			int posY = node.y + positions[i][1];

			if (posX >= 0 && posY >= 0 && isOpenSpace(posX, posY, magicNumber))
			{
				std::string hash = hashPos(posX, posY);
				if (!visited.count(hash))
				{
					nodes.push({ GraphNode{posX, posY, node.distance + 1} });
					visited.insert(hash);
				}
			}
		}
	}

	return visited.size();
}

void day13()
{
	std::cout << bfs(31, 39, 1364) << std::endl;
}