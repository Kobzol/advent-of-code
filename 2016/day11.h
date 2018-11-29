#pragma once

#include <iostream>
#include <string>
#include <unordered_set>
#include <vector>
#include <algorithm>
#include <queue>

struct RadAct
{
	std::string element;
	bool microchip;
};

struct Node
{
	std::vector<std::vector<RadAct>> configuration;
	int elevator;
	int distance;
};

std::string hashFloors(std::vector<std::vector<RadAct>> floors, int elevator)
{
	std::string hash = "elevator" + std::to_string(elevator) + "-";
	for (auto& floor : floors)
	{
		std::sort(floor.begin(), floor.end(), [](RadAct& lhs, RadAct& rhs) -> bool
		{
			if (lhs.element < rhs.element) return true;
			else if (lhs.element > rhs.element) return false;
			else return (int) lhs.microchip < (int) rhs.microchip;
		});
		hash += "floor-" + std::to_string(floor.size()) + "--";

		for (auto& radAct : floor)
		{
			hash += radAct.element + "#" + std::to_string((int)radAct.microchip) + ";";
		}
	}

	return hash;
}
bool isFinal(std::vector<std::vector<RadAct>>& floors)
{
	return
		floors[0].size() == 0 &&
		floors[1].size() == 0 &&
		floors[2].size() == 0;
}
bool isValid(std::vector<std::vector<RadAct>>& floors)
{
	for (int i = 0; i < floors.size(); i++)
	{
		for (int j = 0; j < floors[i].size(); j++)
		{
			if (floors[i][j].microchip)
			{
				bool otherGenerator = false;
				bool sameGenerator = false;
				for (int k = 0; k < floors[i].size(); k++)
				{
					if (!floors[i][k].microchip)
					{
						if (floors[i][k].element == floors[i][j].element)
						{
							sameGenerator = true;
						}
						else otherGenerator = true;
					}
				}

				if (!sameGenerator && otherGenerator)
				{
					return false;
				}
			}
		}
	}

	return true;
}
std::vector<std::tuple<int, int>> generateDoubles(int count)
{
	std::vector<std::tuple<int, int>> doubles;
	if (count < 2) return doubles;

	int leftIndex = 0;
	int rightIndex = 1;

	while (leftIndex < count)
	{
		while (rightIndex < count)
		{
			doubles.push_back(std::tuple<int, int>{leftIndex, rightIndex});
			rightIndex++;
		}
		leftIndex++;
		rightIndex = leftIndex + 1;
	}

	return doubles;
}

void addToQueue(Node& node, std::queue<Node>& queue)
{
	// moving single
	for (int i = 0; i < node.configuration[node.elevator].size(); i++)
	{
		RadAct moved = node.configuration[node.elevator][i];

		if (node.elevator < 3)
		{
			std::vector<std::vector<RadAct>> newFloors = node.configuration;
			newFloors[node.elevator].erase(newFloors[node.elevator].begin() + i);
			newFloors[node.elevator + 1].push_back(moved);

			if (isValid(newFloors))
			{
				queue.push(Node{ newFloors, node.elevator + 1, node.distance + 1 });
			}
		}
		if (node.elevator > 0)
		{
			std::vector<std::vector<RadAct>> newFloors = node.configuration;
			newFloors[node.elevator].erase(newFloors[node.elevator].begin() + i);
			newFloors[node.elevator - 1].push_back(moved);
			if (isValid(newFloors))
			{
				queue.push(Node{ newFloors, node.elevator - 1, node.distance + 1 });
			}
		}
	}

	std::vector<std::tuple<int, int>> doubles = generateDoubles(node.configuration[node.elevator].size());

	// moving double
	for (auto& tuple : doubles)
	{
		int firstIndex = std::get<0>(tuple);
		int secondIndex = std::get<1>(tuple);
		int biggerIndex = std::max(firstIndex, secondIndex);
		int smallerIndex = std::min(firstIndex, secondIndex);

		assert(firstIndex != secondIndex);

		RadAct moved1 = node.configuration[node.elevator][firstIndex];
		RadAct moved2 = node.configuration[node.elevator][secondIndex];

		if (node.elevator < 3)
		{
			std::vector<std::vector<RadAct>> newFloors = node.configuration;
			newFloors[node.elevator].erase(newFloors[node.elevator].begin() + biggerIndex);
			newFloors[node.elevator].erase(newFloors[node.elevator].begin() + smallerIndex);
			newFloors[node.elevator + 1].push_back(moved1);
			newFloors[node.elevator + 1].push_back(moved2);

			if (isValid(newFloors))
			{
				queue.push(Node{ newFloors, node.elevator + 1, node.distance + 1 });
			}
		}
		if (node.elevator > 0)
		{
			std::vector<std::vector<RadAct>> newFloors = node.configuration;
			newFloors[node.elevator].erase(newFloors[node.elevator].begin() + biggerIndex);
			newFloors[node.elevator].erase(newFloors[node.elevator].begin() + smallerIndex);
			newFloors[node.elevator - 1].push_back(moved1);
			newFloors[node.elevator - 1].push_back(moved2);

			if (isValid(newFloors))
			{
				queue.push(Node{ newFloors, node.elevator - 1, node.distance + 1 });
			}
		}
	}
}
int bfsFloors(std::vector<std::vector<RadAct>> floors)
{
	std::queue<Node> queue;
	std::unordered_set<std::string> hashes;

	queue.push(Node{ floors, 0, 0 });

	int iterated = 0;

	while (!queue.empty())
	{
		Node node = queue.front();
		queue.pop();

		std::string hash = hashFloors(node.configuration, node.elevator);
		if (hashes.count(hash)) continue;
		hashes.insert(hash);

		if (isFinal(node.configuration))
		{
			return node.distance;
		}

		iterated++;

		if (iterated % 1000 == 0)
		{
			std::cout << iterated << std::endl;
		}

		addToQueue(node, queue);
	}

	return -1;
}
void day11()
{
	std::vector<std::vector<RadAct>> floors(4, std::vector<RadAct>());

	floors[0].push_back(RadAct{ "promethium", true });
	floors[0].push_back(RadAct{ "promethium", false });
	floors[0].push_back(RadAct{ "elerium", true });
	floors[0].push_back(RadAct{ "elerium", false });
	floors[0].push_back(RadAct{ "dilithium", true });
	floors[0].push_back(RadAct{ "dilithium", false });
	floors[1].push_back(RadAct{ "cobalt", false });
	floors[1].push_back(RadAct{ "curium", false });
	floors[1].push_back(RadAct{ "ruthenium", false });
	floors[1].push_back(RadAct{ "plutonium", false });
	floors[2].push_back(RadAct{ "cobalt", true });
	floors[2].push_back(RadAct{ "curium", true });
	floors[2].push_back(RadAct{ "ruthenium", true });
	floors[2].push_back(RadAct{ "plutonium", true });
	
	assert(isValid(floors));

	std::cout << bfsFloors(floors) << std::endl;
}