#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>

static bool getCondition(int value, const std::string& condition, int conditionValue)
{
    if (condition == "==") return value == conditionValue;
    if (condition == "!=") return value != conditionValue;
    if (condition == ">=") return value >= conditionValue;
    if (condition == ">") return value > conditionValue;
    if (condition == "<") return value < conditionValue;
    if (condition == "<=") return value <= conditionValue;

    return false;
}

void day8()
{
    std::fstream input("input.txt");
    std::string line;
    std::regex regex(R"(([a-z]+)\s+(inc|dec)\s+(-?\d+)\s+if\s+([a-z]+)\s+(<|<=|>|>=|==|!=)\s+(-?\d+))");

    std::unordered_map<std::string, int> registers;
    int maximum = std::numeric_limits<int>::min();
    while (std::getline(input, line))
    {
        std::smatch match;
        if (std::regex_match(line, match, regex))
        {
            auto reg = match[1].str();
            auto op = match[2].str();
            auto value = (int) std::strtol(match[3].str().c_str(), nullptr, 10);
            auto condreg = match[4].str();
            auto condition = match[5].str();
            auto condvalue = (int) std::strtol(match[6].str().c_str(), nullptr, 10);

            if (getCondition(registers[condreg], condition, condvalue))
            {
                registers[reg] += value * (op == "inc" ? 1 : -1);
                maximum = registers[reg] > maximum ? registers[reg] : maximum;
            }
        }
    }

    std::cout << maximum << std::endl;
}
