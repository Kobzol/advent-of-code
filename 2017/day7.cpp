#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>

struct Disc
{
	std::string name;
	size_t weight;
	std::vector<std::string> above;
};

size_t getWeight(const std::string& disc, std::unordered_map<std::string, Disc>& discs)
{
	size_t weight = discs[disc].weight;
	for (auto& above : discs[disc].above)
	{
		weight += getWeight(above, discs);
	}
	return weight;
}

void day7()
{
    std::fstream input("input.txt");
    std::string line;
	std::regex reg(R"(([a-z]+)\s+\((\d+)\)(?:\s+->\s+((?:[a-z]+(?:, )?)+))?)");

    size_t count = 0;
	std::vector<Disc> discs;
	std::unordered_set<std::string> isAbove;
	std::unordered_map<std::string, Disc> discMap;

    while (std::getline(input, line))
    {
        std::smatch match;
		if (std::regex_match(line, match, reg))
		{
			std::vector<std::string> above;
			int i = 0;
			std::string aboveStr = match[3].str();
			std::string neighbour;

			while (i < aboveStr.size())
			{
				while (i < aboveStr.size() && isalpha(aboveStr[i]))
				{
					neighbour += aboveStr[i];
					isAbove.insert(neighbour);
					i++;
				}
				above.push_back(neighbour);
				neighbour.clear();
				while (i < aboveStr.size() && !isalpha(aboveStr[i])) i++;
			}

			Disc disc{ match[1], (size_t)std::strtoll(match[2].str().c_str(), nullptr, 10), above };
			discs.push_back(disc);
			discMap.insert({ disc.name, disc });
		}
    }

	std::string bottom = "rugzyaj";
	for (auto& above : discMap[bottom].above)
	{
		std::cerr << getWeight(above, discMap) << " " << discMap[above].weight << " " << discMap[above].name << std::endl;
	}
    
	getchar();
}
