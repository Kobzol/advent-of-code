#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>
#include <iomanip>
#include <queue>

void day16()
{
    std::fstream input("input.txt");
    std::string line;
    std::getline(input, line);

    std::regex swap(R"(x(\d+)/(\d+))");
    std::string data = "abcdefghijklmnop";
    std::string oldData = "";
    std::string originalLine = line;

    for (int c = 0; c < 244; c++)
    {
        line = originalLine;
        while (!line.empty())
        {
            auto pos = line.find(',');
            std::string command = line.substr(0, pos);
            std::smatch match;
            line = line.substr(pos + 1);

            if (command[0] == 's')
            {
                int count = 0;
                int i = 1;
                while (i < pos)
                {
                    count *= 10;
                    count += command[i++] - '0';
                }

                count %= data.size();
                std::string moved = data;
                for (int j = 0; j < data.size(); j++)
                {
                    moved[j] = data[((j - (count)) + data.size()) % data.size()];
                }
                data = std::move(moved);
            }
            else if (command[0] == 'x')
            {
                std::regex_match(command, match, swap);
                std::swap(data[std::stoi(match[1].str().c_str())], data[std::stoi(match[2].str())]);
            }
            else
            {
                auto left = command[1];
                auto right = command[3];
                std::swap(data[data.find(left)], data[data.find(right)]);
            }
        }
    }
    
    std::cout << data << std::endl;
}
