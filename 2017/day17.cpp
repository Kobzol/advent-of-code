#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>
#include <iomanip>

void day17()
{
    int steps = 303;
    int pos = 0;
    for (int i = 0; i < 50000000; i++)
    {
        pos = (pos + steps) % (i + 1);
        if (pos == 0)
        {
            std::cerr << i + 1 << std::endl;
        }
        pos++;
    }
}
