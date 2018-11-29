#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>
#include <iomanip>

struct Program
{
    int id;
    std::vector<int> pipes;
};

int findConnections(std::unordered_map<int, Program>& programs, std::unordered_set<int>& visited, int program)
{
    if (visited.find(program) != visited.end()) return 0;
    visited.insert(program);

    int count = 1;
    for (auto& p: programs[program].pipes)
    {
        count += findConnections(programs, visited, p);
    }
    return count;
}

void day12()
{
    std::fstream input("input.txt");
    std::string line;

    std::unordered_map<int, Program> programs;
    while (std::getline(input, line))
    {
        line = line.substr(line.find("> ") + 2);
        Program program;
        program.id = programs.size();

        for (int i = 0; i < line.size();)
        {
            int pipe = 0;
            while (i < line.size() && isdigit(line[i]))
            {
                pipe *= 10;
                pipe += (line[i] - '0');
                i++;
            }
            i += 2;
            program.pipes.push_back(pipe);
        }

        programs.insert({ program.id, program });
    }

    std::unordered_set<int> visited;
	int groups = 0;
	for (auto& kv : programs)
	{
		if (findConnections(programs, visited, kv.first) > 0)
		{
			groups++;
		}
	}

    std::cout << groups << std::endl;
	getchar();
}
