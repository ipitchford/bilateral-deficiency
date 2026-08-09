// Dependency-free exact solver for bilateral deficiency on indexed DIMACS CNF.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

struct Formula {
    int variables = -1;
    std::vector<std::vector<int>> clauses;
};

Formula read_dimacs(const std::string& path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open input: " + path);

    Formula formula;
    int declared_clauses = -1;
    std::vector<int> clause;
    std::string line;
    while (std::getline(input, line)) {
        if (line.empty() || line[0] == 'c') continue;
        if (line[0] == 'p') {
            std::istringstream header(line);
            std::string p, format;
            if (!(header >> p >> format >> formula.variables >> declared_clauses) ||
                p != "p" || format != "cnf" || formula.variables < 0 ||
                declared_clauses < 0) {
                throw std::runtime_error("invalid DIMACS header");
            }
            continue;
        }
        if (formula.variables < 0) {
            throw std::runtime_error("clause data precedes DIMACS header");
        }
        std::istringstream fields(line);
        int literal = 0;
        while (fields >> literal) {
            if (literal == 0) {
                std::set<int> normalized(clause.begin(), clause.end());
                formula.clauses.emplace_back(normalized.begin(), normalized.end());
                clause.clear();
            } else {
                if (literal == std::numeric_limits<int>::min() ||
                    std::abs(literal) > formula.variables) {
                    throw std::runtime_error("literal outside declared variable range");
                }
                clause.push_back(literal);
            }
        }
    }
    if (!clause.empty()) throw std::runtime_error("unterminated final DIMACS clause");
    if (formula.variables < 0) throw std::runtime_error("missing DIMACS header");
    if (static_cast<int>(formula.clauses.size()) != declared_clauses) {
        throw std::runtime_error("declared clause count does not match input");
    }
    return formula;
}

std::uint64_t checked_power(std::uint64_t base, int exponent) {
    std::uint64_t answer = 1;
    for (int i = 0; i < exponent; ++i) {
        if (answer > std::numeric_limits<std::uint64_t>::max() / base) {
            throw std::runtime_error("assignment space exceeds uint64_t");
        }
        answer *= base;
    }
    return answer;
}

std::string assignment_text(const std::vector<unsigned char>& state) {
    std::string text;
    text.reserve(state.size());
    for (unsigned char value : state) text.push_back(value == 0 ? '*' : value == 1 ? '0' : '1');
    return text;
}

struct Receipt {
    std::uint64_t total = 0;
    std::uint64_t bilateral = 0;
    int minimum = std::numeric_limits<int>::max();
    std::string witness;
    std::map<int, std::uint64_t> spectrum;
    std::vector<std::uint64_t> bilateral_by_unassigned;
    std::vector<int> minimum_clauses_by_unassigned;
};

Receipt solve(const Formula& formula) {
    Receipt receipt;
    receipt.total = checked_power(3, formula.variables);
    receipt.bilateral_by_unassigned.assign(formula.variables + 1, 0);
    receipt.minimum_clauses_by_unassigned.assign(
        formula.variables + 1, std::numeric_limits<int>::max()
    );

    std::vector<unsigned char> state(formula.variables, 0); // 0=*, 1=false, 2=true
    std::vector<unsigned char> positive(formula.variables, 0);
    std::vector<unsigned char> negative(formula.variables, 0);

    for (std::uint64_t code = 0; code < receipt.total; ++code) {
        std::uint64_t digits = code;
        int unassigned = 0;
        for (int variable = 0; variable < formula.variables; ++variable) {
            state[variable] = static_cast<unsigned char>(digits % 3);
            digits /= 3;
            unassigned += state[variable] == 0;
        }

        std::fill(positive.begin(), positive.end(), 0);
        std::fill(negative.begin(), negative.end(), 0);
        int residual_clauses = 0;
        for (const auto& clause : formula.clauses) {
            bool satisfied = false;
            for (int literal : clause) {
                const int variable = std::abs(literal) - 1;
                const unsigned char value = state[variable];
                if (value != 0) {
                    const bool truth = value == 2;
                    if (truth == (literal > 0)) satisfied = true;
                }
            }
            if (satisfied) continue;
            ++residual_clauses;
            for (int literal : clause) {
                const int variable = std::abs(literal) - 1;
                if (state[variable] == 0) {
                    (literal > 0 ? positive : negative)[variable] = 1;
                }
            }
        }

        bool bilateral = true;
        for (int variable = 0; variable < formula.variables; ++variable) {
            if (state[variable] == 0 && !(positive[variable] && negative[variable])) {
                bilateral = false;
                break;
            }
        }
        if (!bilateral) continue;

        ++receipt.bilateral;
        ++receipt.bilateral_by_unassigned[unassigned];
        receipt.minimum_clauses_by_unassigned[unassigned] = std::min(
            receipt.minimum_clauses_by_unassigned[unassigned], residual_clauses
        );
        const int deficiency = residual_clauses - unassigned;
        ++receipt.spectrum[deficiency];
        if (deficiency < receipt.minimum) {
            receipt.minimum = deficiency;
            receipt.witness = assignment_text(state);
        }
    }
    if (receipt.minimum == std::numeric_limits<int>::max()) {
        throw std::runtime_error("no bilateral assignment found; internal error");
    }
    return receipt;
}

void print_json(const Formula& formula, const Receipt& receipt, const std::string& path) {
    std::cout << "{\n";
    std::cout << "  \"schema\": \"bilateral-deficiency/exhaustive-receipt/v1\",\n";
    std::cout << "  \"input\": \"" << path << "\",\n";
    std::cout << "  \"variables\": " << formula.variables << ",\n";
    std::cout << "  \"indexed_clauses\": " << formula.clauses.size() << ",\n";
    std::cout << "  \"partial_assignments\": " << receipt.total << ",\n";
    std::cout << "  \"bilateral_assignments\": " << receipt.bilateral << ",\n";
    std::cout << "  \"beta\": " << receipt.minimum << ",\n";
    std::cout << "  \"witness\": \"" << receipt.witness << "\",\n";

    std::cout << "  \"spectrum\": {";
    bool first = true;
    for (const auto& [value, count] : receipt.spectrum) {
        if (!first) std::cout << ", ";
        std::cout << "\"" << value << "\": " << count;
        first = false;
    }
    std::cout << "},\n";

    std::cout << "  \"bilateral_by_unassigned\": [";
    for (std::size_t i = 0; i < receipt.bilateral_by_unassigned.size(); ++i) {
        if (i) std::cout << ", ";
        std::cout << receipt.bilateral_by_unassigned[i];
    }
    std::cout << "],\n";

    std::cout << "  \"minimum_residual_clauses_by_unassigned\": [";
    for (std::size_t i = 0; i < receipt.minimum_clauses_by_unassigned.size(); ++i) {
        if (i) std::cout << ", ";
        const int value = receipt.minimum_clauses_by_unassigned[i];
        if (value == std::numeric_limits<int>::max()) std::cout << "null";
        else std::cout << value;
    }
    std::cout << "]\n";
    std::cout << "}\n";
}

} // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 2) {
            std::cerr << "usage: bd_exact FORMULA.cnf\n";
            return 2;
        }
        const Formula formula = read_dimacs(argv[1]);
        const Receipt receipt = solve(formula);
        print_json(formula, receipt, argv[1]);
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "bd_exact: " << error.what() << "\n";
        return 1;
    }
}
