#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>
#include <iomanip>

using ssize_t = long long;

static std::vector<std::string> parse(std::string line)
{
    std::vector<std::string> data;

    line += ' ';
    while (!line.empty())
    {
        data.push_back(line.substr(0, line.find(' ')));
        line = line.substr(line.find(' ') + 1);
    }

    return data;
}
static ssize_t getValue(std::unordered_map<char, ssize_t>& registers, const std::string& label)
{
    if (isdigit(label[0]) || label[0] == '-')
    {
        return std::stol(label, nullptr, 10);
    }
    else return registers[label[0]];
}

ssize_t fn()
{
    ssize_t a = 1, b = 0, c = 0, d = 0, e = 0, f = 0, g = 0, h = 0;

    b = 67;
    c = b;
    b *= 100;
    b -= -100000;
    c = b;
    c -= -17000;
    l6:
    f = 1;
    d = 2;

    l3:
    e = 2;

    l2: // if (b == d * e) f = 0;
    g = d;
    g *= e;
    g -= b;
    if (g != 0)
    {
        goto l1;
    }
    f = 0;

    l1: // e = b;
    e++;
    g = e;
    g -= b;
    if (g != 0)
    {
        goto l2;
    }

    d++;
    g = d;
    g -= b;
    if (g != 0)
    {
        goto l3;
    }
    if (f != 0)
    {
        goto l4;
    }
    h++;
    l4:
    g = b;
    g -= c;
    if (g != 0)
    {
        goto l5;
    }
    return h;
    l5:
    b -= -17;
    goto l6;
}

bool isPrime(ssize_t num)
{
    if (num % 2 == 0) return false;
    ssize_t target = std::sqrt(num);
    for (int i = 3; i <= target; i += 2)
    {
        if (num % i == 0) return false;
    }
    return true;
}

void day23()
{
    int j = 0;
    for (int i = 106700; i <= 123700; i += 17)
    {
        if (!isPrime(i))
        {
            j++;
        }
    }

    std::cout << j << std::endl;

    std::cout << fn() << std::endl;
    return;

    std::fstream input("input.txt");
    std::string line;

    std::vector<std::vector<std::string>> instructions;
    while (std::getline(input, line))
    {
        if (line[0] != '#')
        {
            instructions.push_back(parse(line));
        }
    }

    ssize_t ip = 0;
    std::unordered_map<char, ssize_t> registers;
    registers['a'] = 1;

    while (ip >= 0 && ip < instructions.size())
    {
        auto cmd = instructions[ip];
        if (cmd[0] == "set")
        {
            registers[cmd[1][0]] = getValue(registers, cmd[2]);
            ip++;
        }
        else if (cmd[0] == "sub")
        {
            registers[cmd[1][0]] -= getValue(registers, cmd[2]);
            ip++;
        }
        else if (cmd[0] == "mul")
        {
            registers[cmd[1][0]] *= getValue(registers, cmd[2]);
            ip++;
        }
        else if (cmd[0] == "jnz")
        {
            if (getValue(registers, cmd[1]) != 0)
            {
                ip += getValue(registers, cmd[2]);
            }
            else ip++;
        }
    }

    std::cout << registers['h'] << std::endl;
}
