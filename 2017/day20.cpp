#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <regex>
#include <iomanip>
#include <climits>

using ssize_t = long long;

#define CHECK_OVERFLOW(base, add)\
    if (((add) > 0) && ((base) > INT_MAX - (add))) std::cout << "overflow" << std::endl;\
    if (((add) < 0) && ((base) < INT_MIN - (add))) std::cout << "underflow" << std::endl;

struct Vector
{
    Vector() = default;
    Vector(ssize_t x, ssize_t y, ssize_t z): x(x), y(y), z(z)
    {

    }
    ssize_t x, y, z;

    bool operator==(const Vector& other)
    {
        return this->x == other.x && this->y == other.y && this->z == other.z;
    }
};
struct Particle
{
    Particle() = default;
    Particle(Vector position, Vector velocity, Vector acceleration)
            : position(position), velocity(velocity), acceleration(acceleration)
    {

    }

    ssize_t dist()
    {
        return std::abs(this->position.x) + std::abs(this->position.y) + std::abs(this->position.z);
    }
    void move()
    {
        this->velocity.x += this->acceleration.x;
        this->velocity.y += this->acceleration.y;
        this->velocity.z += this->acceleration.z;

        CHECK_OVERFLOW(this->position.x, this->velocity.x);
        this->position.x += this->velocity.x;

        CHECK_OVERFLOW(this->position.y, this->velocity.y);
        this->position.y += this->velocity.y;

        CHECK_OVERFLOW(this->position.z, this->velocity.z);
        this->position.z += this->velocity.z;
    }

    Vector position;
    Vector velocity;
    Vector acceleration;
    bool active = true;
};

void day20()
{
    std::fstream input("input.txt");
    std::string line;

    std::vector<Particle> particles;
    while (std::getline(input, line))
    {
        line = line.substr(line.find('<') + 1);
        ssize_t px = std::stoll(line.substr(0, line.find(',')));
        line = line.substr(line.find(',') + 1);
        ssize_t py = std::stoll(line.substr(0, line.find(',')));
        line = line.substr(line.find(',') + 1);
        ssize_t pz = std::stoll(line.substr(0, line.find('>')));
        line = line.substr(line.find('>') + 6);

        ssize_t vx = std::stoll(line.substr(0, line.find(',')));
        line = line.substr(line.find(',') + 1);
        ssize_t vy = std::stoll(line.substr(0, line.find(',')));
        line = line.substr(line.find(',') + 1);
        ssize_t vz = std::stoll(line.substr(0, line.find('>')));
        line = line.substr(line.find('>') + 6);

        ssize_t ax = std::stoll(line.substr(0, line.find(',')));
        line = line.substr(line.find(',') + 1);
        ssize_t ay = std::stoll(line.substr(0, line.find(',')));
        line = line.substr(line.find(',') + 1);
        ssize_t az = std::stoll(line.substr(0, line.find('>')));

        particles.emplace_back(Vector(px, py, pz), Vector(vx, vy, vz), Vector(ax, ay, az));
    }

    std::vector<Particle> data[2] = { particles, {} };
    int active = 0;
    for (int iter = 0; iter < 10500; iter++)
    {
        int other = 1 - active;
        for (int i = 0; i < data[active].size(); i++)
        {
            data[active][i].move();
        }
        for (int i = 0; i < data[active].size(); i++)
        {
            if (data[active][i].active)
            {
                for (int j = i + 1; j < data[active].size(); j++)
                {
                    if (data[active][i].position == data[active][j].position)
                    {
                        data[active][i].active = false;
                        data[active][j].active = false;
                    }
                }

                if (data[active][i].active)
                {
                    data[other].push_back(data[active][i]);
                }
            }
        }

        data[active].clear();
        active = other;
    }

    std::cout << data[active].size() << std::endl;
}
