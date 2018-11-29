#pragma once

#include <fstream>
#include <string>
#include <iostream>
#include <vector>
#include <regex>

class ClusterNode
{
public:
	int size, used;

	int getSize() { return this->size; }
	int getUsed() { return this->used; }
	int getFree() { return this->getSize() - this->getUsed(); }

	void transferTo(ClusterNode& node)
	{
		if (node.getFree() < this->getUsed()) throw "not enough space";
		node.used += this->getUsed();
		this->used = 0;
	}

	bool isEmpty() { return this->used == 0; }
};

void day22()
{
	std::fstream fs("input.txt", std::ios::in);

	const std::regex regex(".*node-x(\\d+)-y(\\d+)\\s+(\\d+)T\\s+(\\d+).*");
	
	std::vector<std::vector<ClusterNode>> cluster;
	std::vector<ClusterNode> nodes;

	std::string row;
	while (std::getline(fs, row))
	{
		std::smatch match;

		if (std::regex_match(row, match, regex))
		{
			int x = std::stoi(match[1].str());
			int y = std::stoi(match[2].str());
			int size = std::stoi(match[3].str());
			int used = std::stoi(match[4].str());

			if (x == cluster.size())
			{
				cluster.push_back(std::vector<ClusterNode>());
			}

			cluster[cluster.size() - 1].push_back(ClusterNode{ size, used });
			nodes.push_back(ClusterNode{ size, used });
		}
	}

	for (int i = 0; i < cluster.size(); i++)
	{
		for (int j = 0; j < cluster[i].size(); j++)
		{
			std::cout << cluster[i][j].getUsed() << "/" << cluster[i][j].getSize() << " ";
		}
		std::cout << std::endl;
	}
}