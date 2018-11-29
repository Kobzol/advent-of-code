#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>
#include <iomanip>
#include <mutex>
#include <queue>
#include <atomic>
#include <chrono>

using ssize_t = long long;
using namespace std::chrono_literals;

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

void day18()
{
    std::fstream input("input.txt");
    std::string line;

    std::vector<std::vector<std::string>> instructions;
    while (std::getline(input, line))
    {
        instructions.push_back(parse(line));
    }

    std::queue<ssize_t> queues[2];
    std::mutex mutexes[2];
    std::atomic<int> waiting{0};
    auto thread_fn = [&queues, &instructions, &mutexes, &waiting](int id)
    {
        ssize_t ip = 0;
        std::unordered_map<char, ssize_t> registers;
        registers['p'] = id;

        int target = 1 - id;
        int sent = 0;
        while (ip >= 0 && ip < instructions.size())
        {
            auto cmd = instructions[ip];
            if (cmd[0] == "snd")
            {
                std::lock_guard<decltype(mutexes[0])> guard(mutexes[target]);
                queues[target].push(registers[cmd[1][0]]);
                //printf("Sending to %d (%lld)\n", target, queues[target].size());
                ip++;
                sent++;
            }
            else if (cmd[0] == "set")
            {
                registers[cmd[1][0]] = getValue(registers, cmd[2]);
                ip++;
            }
            else if (cmd[0] == "add")
            {
                registers[cmd[1][0]] += getValue(registers, cmd[2]);
                ip++;
            }
            else if (cmd[0] == "mul")
            {
                registers[cmd[1][0]] *= getValue(registers, cmd[2]);
                ip++;
            }
            else if (cmd[0] == "mod")
            {
                registers[cmd[1][0]] = getValue(registers, cmd[1]) % getValue(registers, cmd[2]);
                ip++;
            }
            else if (cmd[0] == "rcv")
            {
                int incremented = 0;
                while (true)
                {
                    {
                        std::lock_guard<std::mutex> guard(mutexes[id]);
                        //printf("Receiving on %d (%lld)\n", id, queues[id].size());
                        if (!queues[id].empty())
                        {
                            registers[cmd[1][0]] = queues[id].front();
                            queues[id].pop();

                            if (incremented > 0)
                            {
                                waiting -= incremented;
                            }

                            break;
                        }
                        else
                        {
                            if (incremented < 3)
                            {
                                incremented++;
                                waiting++;
                            }
                            if (waiting > 5)
                            {
                                if (id == 1)
                                {
                                    printf("%d sent %d times\n", id, sent);
                                }
                                return;
                            }
                        }
                    }

                    std::this_thread::sleep_for(500ms);
                }
                //printf("Received on %d\n", id);
                ip++;
            }
            else if (cmd[0] == "jgz")
            {
                if (getValue(registers, cmd[1]) > 0)
                {
                    ip += getValue(registers, cmd[2]);
                }
                else ip++;
            }
        }
    };
    std::thread threads[2] = {
            std::thread(thread_fn, 0),
            std::thread(thread_fn, 1)   
    };
    for (auto& t: threads)
    {
        t.join();
    }
}
