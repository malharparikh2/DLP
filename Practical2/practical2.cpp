#include <iostream>
using namespace std;

const int MAX_STATES = 10;
const int MAX_SYMBOLS = 10;

int transitions[MAX_STATES][MAX_SYMBOLS];
int num_states, num_symbols, initial_state, accepting_states[MAX_STATES], num_accepting;
char symbols[MAX_SYMBOLS];

void create_finite_automaton() {
    cout << "Enter the number of input symbols: ";
    cin >> num_symbols;
    
    cout << "Enter the symbols: ";
    for (int i = 0; i < num_symbols; i++) {
        cin >> symbols[i];
    }
    
    cout << "Enter the number of states: ";
    cin >> num_states;
    
    cout << "Enter the initial state: ";
    cin >> initial_state;
    initial_state--;
    
    cout << "Enter the number of accepting states: ";
    cin >> num_accepting;
    cout << "Enter the accepting states: ";
    for (int i = 0; i < num_accepting; i++) {
        cin >> accepting_states[i];
        accepting_states[i]--;
    }
    
    for (int i = 0; i < num_states; i++) {
        for (int j = 0; j < num_symbols; j++) {
            transitions[i][j] = -1;
        }
    }
    
    cout << "Enter transitions (from_state symbol to_state): " << endl;
    for (int i = 0; i < num_states * num_symbols; i++) {
        int from, to;
        char sym;
        cin >> from >> sym >> to;
        from--; to--;
        
        for (int j = 0; j < num_symbols; j++) {
            if (symbols[j] == sym) {
                transitions[from][j] = to;
                break;
            }
        }
    }
}

bool validate_string(const string &input) {
    int current_state = initial_state;
    
    for (char sym : input) {
        int symbol_index = -1;
        for (int i = 0; i < num_symbols; i++) {
            if (symbols[i] == sym) {
                symbol_index = i;
                break;
            }
        }
        
        if (symbol_index == -1) {
            cout << "Invalid symbol: " << sym << endl;
            return false;
        }
        
        current_state = transitions[current_state][symbol_index];
        if (current_state == -1) {
            cout << "No transition for symbol: " << sym << endl;
            return false;
        }
    }
    
    for (int i = 0; i < num_accepting; i++) {
        if (current_state == accepting_states[i]) {
            cout << "The string is accepted." << endl;
            return true;
        }
    }
    
    cout << "The string is not accepted." << endl;
    return false;
}

int main() {
    create_finite_automaton();
    
    string input;
    cout << "Enter the string to validate: ";
    cin >> input;
    
    validate_string(input);
    
    return 0;
}
