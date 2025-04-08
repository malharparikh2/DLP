#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <stack>
#include <algorithm>
#include <iomanip>

using namespace std;

// Grammar representation
struct Production {
    string lhs;
    vector<string> rhs;
};

class LL1Parser {
private:
    vector<Production> productions;
    map<string, set<string>> firstSets;
    map<string, set<string>> followSets;
    map<string, map<string, vector<string>>> parsingTable;
    string startSymbol;

    // Helper functions
    bool isTerminal(const string& symbol) {
        return symbol[0] != toupper(symbol[0]) || symbol == "ε";
    }

    void computeFirst(const string& symbol) {
        if (firstSets.find(symbol) != firstSets.end()) return;

        set<string> first;

        if (isTerminal(symbol)) {
            first.insert(symbol);
            firstSets[symbol] = first;
            return;
        }

        for (const auto& prod : productions) {
            if (prod.lhs == symbol) {
                if (prod.rhs[0] == "ε") {
                    first.insert("ε");
                } else {
                    bool allHaveEpsilon = true;
                    for (const string& s : prod.rhs) {
                        computeFirst(s);
                        for (const string& val : firstSets[s]) {
                            if (val != "ε") {
                                first.insert(val);
                            }
                        }
                        if (firstSets[s].find("ε") == firstSets[s].end()) {
                            allHaveEpsilon = false;
                            break;
                        }
                    }
                    if (allHaveEpsilon) {
                        first.insert("ε");
                    }
                }
            }
        }

        firstSets[symbol] = first;
    }

    void computeFollow(const string& symbol) {
        if (followSets.find(symbol) != followSets.end()) return;

        set<string> follow;

        if (symbol == startSymbol) {
            follow.insert("$");
        }

        for (const auto& prod : productions) {
            for (size_t i = 0; i < prod.rhs.size(); ++i) {
                if (prod.rhs[i] == symbol) {
                    if (i + 1 < prod.rhs.size()) {
                        string nextSymbol = prod.rhs[i + 1];
                        computeFirst(nextSymbol);
                        for (const string& val : firstSets[nextSymbol]) {
                            if (val != "ε") {
                                follow.insert(val);
                            }
                        }
                        if (firstSets[nextSymbol].find("ε") != firstSets[nextSymbol].end()) {
                            computeFollow(prod.lhs);
                            for (const string& val : followSets[prod.lhs]) {
                                follow.insert(val);
                            }
                        }
                    } else {
                        if (prod.lhs != symbol) {
                            computeFollow(prod.lhs);
                            for (const string& val : followSets[prod.lhs]) {
                                follow.insert(val);
                            }
                        }
                    }
                }
            }
        }

        followSets[symbol] = follow;
    }

    void buildParsingTable() {
        for (const auto& prod : productions) {
            set<string> firstAlpha;
            bool hasEpsilon = true;

            for (const string& symbol : prod.rhs) {
                computeFirst(symbol);
                for (const string& val : firstSets[symbol]) {
                    if (val != "ε") {
                        firstAlpha.insert(val);
                    }
                }
                if (firstSets[symbol].find("ε") == firstSets[symbol].end()) {
                    hasEpsilon = false;
                    break;
                }
            }

            if (hasEpsilon) {
                firstAlpha.insert("ε");
            }

            for (const string& terminal : firstAlpha) {
                if (terminal != "ε") {
                    // Check for conflicts
                    if (parsingTable[prod.lhs].find(terminal) != parsingTable[prod.lhs].end()) {
                        cerr << "Conflict detected for " << prod.lhs << " and terminal " << terminal << endl;
                    }
                    parsingTable[prod.lhs][terminal] = prod.rhs;
                }
            }

            if (hasEpsilon) {
                computeFollow(prod.lhs);
                for (const string& terminal : followSets[prod.lhs]) {
                    // Check for conflicts
                    if (parsingTable[prod.lhs].find(terminal) != parsingTable[prod.lhs].end()) {
                        cerr << "Conflict detected for " << prod.lhs << " and terminal " << terminal << endl;
                    }
                    parsingTable[prod.lhs][terminal] = prod.rhs;
                }
            }
        }
    }

public:
    LL1Parser(const vector<Production>& prods, const string& start)
        : productions(prods), startSymbol(start) {

        // Initialize FIRST and FOLLOW sets from given data
        firstSets = {
            {"S", {"a", "b", "(", "c"}},
            {"A", {"a", "ε"}},
            {"B", {"b", "ε"}},
            {"C", {"(", "c"}},
            {"D", {"a", "(", "c"}}
        };

        followSets = {
            {"S", {")", "$"}},
            {"A", {"b", "(", ")", "$"}},
            {"B", {"c", ")", "$"}},
            {"C", {")", "$"}},
            {"D", {")", "$"}}
        };

        buildParsingTable();
    }

    bool isLL1Grammar() {
        for (const auto& row : parsingTable) {
            for (const auto& entry : row.second) {
                // If any cell has more than one production, it's not LL(1)
                if (entry.second.size() > 1) {
                    return false;
                }
            }
        }
        return true;
    }

    void printParsingTable() {
        cout << "\nPredictive Parsing Table:\n";
        cout << "------------------------\n";

        // Collect all terminals
        set<string> terminals;
        for (const auto& row : parsingTable) {
            for (const auto& entry : row.second) {
                terminals.insert(entry.first);
            }
        }
        terminals.insert("$");

        // Print header
        cout << setw(15) << left << "Non-Terminal";
        for (const string& term : terminals) {
            cout << setw(15) << left << term;
        }
        cout << endl;

        // Print table rows for each non-terminal
        vector<string> nonTerminals = {"S", "A", "B", "C", "D"};
        for (const string& nonTerm : nonTerminals) {
            cout << setw(15) << left << nonTerm;
            for (const string& term : terminals) {
                if (parsingTable[nonTerm].find(term) != parsingTable[nonTerm].end()) {
                    string production;
                    for (const string& sym : parsingTable[nonTerm][term]) {
                        production += sym + " ";
                    }
                    cout << setw(15) << left << production;
                } else {
                    cout << setw(15) << left << "";
                }
            }
            cout << endl;
        }
    }

    bool validateString(const string& input) {
        stack<string> parseStack;
        parseStack.push("$");
        parseStack.push(startSymbol);

        size_t inputPtr = 0;
        string currentInput = (inputPtr < input.size()) ? string(1, input[inputPtr]) : "$";

        while (!parseStack.empty()) {
            string top = parseStack.top();
            parseStack.pop();

            if (top == "$") {
                if (currentInput == "$") {
                    return true;
                } else {
                    return false;
                }
            } else if (isTerminal(top)) {
                if (top == currentInput) {
                    inputPtr++;
                    currentInput = (inputPtr < input.size()) ? string(1, input[inputPtr]) : "$";
                } else if (top == "ε") {
                    continue;
                } else {
                    return false;
                }
            } else {
                if (parsingTable[top].find(currentInput) != parsingTable[top].end()) {
                    const vector<string>& production = parsingTable[top][currentInput];
                    // Push production in reverse order
                    for (auto it = production.rbegin(); it != production.rend(); ++it) {
                        if (*it != "ε") {
                            parseStack.push(*it);
                        }
                    }
                } else {
                    return false;
                }
            }
        }

        return false;
    }
};

int main() {
    // Define the grammar productions
    vector<Production> productions = {
        {"S", {"A", "B", "C"}},
        {"S", {"D"}},
        {"A", {"a"}},
        {"A", {"ε"}},
        {"B", {"b"}},
        {"B", {"ε"}},
        {"C", {"(", "S", ")"}},
        {"C", {"c"}},
        {"D", {"A", "C"}}
    };

    LL1Parser parser(productions, "S");

    // Print parsing table
    parser.printParsingTable();

    // Check if grammar is LL(1)
    if (parser.isLL1Grammar()) {
        cout << "\nThe grammar is LL(1).\n";
    } else {
        cout << "\nThe grammar is not LL(1) due to conflicts in the parsing table.\n";
    }

    // Test cases
    vector<string> testCases = {
        "abc", "ac", "(abc)", "c", "(ac)",
        "a", "()", "(ab)", "abcabc", "b"
    };

    cout << "\nString Validation:\n";
    cout << "-----------------\n";
    for (const string& testCase : testCases) {
        cout << "Testing string \"" << testCase << "\": ";
        if (parser.validateString(testCase)) {
            cout << "Valid string\n";
        } else {
            cout << "Invalid string\n";
        }
    }

    return 0;
}
