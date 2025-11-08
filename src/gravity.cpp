#include "gravity.hpp"

#include <algorithm>
#include <random>
#include <ranges>
#include <thread>

static constexpr auto G = 6.6743e-11;

namespace gravity
{
Model::Model(const int N) : x(N), y(N), vx(N), vy(N), ax(N), ay(N), m(N, 5e6)
{
    auto eng = std::mt19937{1337};
    auto pos_dis = std::uniform_real_distribution{-100.0, 100.0};

    std::ranges::generate(x, [&] { return pos_dis(eng); });
    std::ranges::generate(y, [&] { return pos_dis(eng); });
    for (auto i = 0; i < N; ++i)
    {
        auto x_ = x[i];
        auto y_ = y[i];
        auto r = std::sqrt(x_ * x_ + y_ * y_);
        vx[i] = -y_ / r;
        vy[i] = x_ / r;
    }

    x[0] = 0.0;
    y[0] = 0.0;
    vx[0] = 0.0;
    vy[0] = 0.0;
    m[0] = 1e12;
}

auto Model::update(const std::chrono::duration<double> dt) -> void
{
    static constexpr auto n_threads = 8;
    auto threads = std::vector<std::jthread>{};
    threads.reserve(n_threads);
    auto s = x.size() / n_threads;

    {
        auto slice = [&](auto start, auto end) {
            for (auto i = start; i < end; ++i)
            {
                for (auto j = 0; j < x.size() / 2; ++j)
                {
                    if (i == j) [[unlikely]]
                    {
                        continue;
                    }
                    auto dx = x[j] - x[i];
                    auto dy = y[j] - y[i];
                    auto r = std::sqrt(dx * dx + dy * dy);
                    auto f = G * m[i] * m[j] / (r * r);
                    auto theta = std::atan2(dy, dx);
                    ax[i] += f * std::cos(theta) / m[i];
                    ay[i] += f * std::sin(theta) / m[i];
                    ax[j] -= f * std::cos(theta) / m[j];
                    ay[j] -= f * std::sin(theta) / m[j];
                }
            }
        };

        for (auto i = std::size_t{}; i < n_threads; ++i)
        {
            auto start = i * s;
            auto end = start + s;
            end = end > x.size() ? x.size() - 1 : end;
            threads.emplace_back(slice, start, end);
        }
    }

    for (auto &thread : threads)
    {
        thread.join();
    }

    threads.clear();

    {
        auto slice = [&](auto start, auto end) {
            for (auto i = start; i < end; ++i)
            {
                vx[i] += ax[i] * dt.count();
                vy[i] += ay[i] * dt.count();
                x[i] += vx[i] * dt.count();
                y[i] += vy[i] * dt.count();
                ax[i] = 0.0;
                ay[i] = 0.0;
            }
        };

        for (auto i = std::size_t{}; i < n_threads; ++i)
        {
            auto start = i * s;
            auto end = start + s;
            end = end > x.size() ? x.size() - 1 : end;
            threads.emplace_back(slice, start, end);
        }
    }
}
} // namespace gravity