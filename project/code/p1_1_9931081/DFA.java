import java.io.File;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;

public class DFA {
    private Set<String> states;  // A set of states
    private Set<String> alphabet;  // A set of alphabets
    private Map<String, Map<String, String>> transitions;  // A dictionary of transition functions
    private String start_state;  // A start state
    private Set<String> accept_states;  // A set of accept states
    private String current_state;  // A current state

    public DFA(Set<String> states, Set<String> alphabet, Map<String, Map<String, String>> transitions,
            String start_state, Set<String> accept_states) {
        this.states = states;
        this.alphabet = alphabet;
        this.transitions = transitions;
        this.start_state = start_state;
        this.accept_states = accept_states;
        this.current_state = start_state;
    }

    public boolean run(String input_string) {
        String current_state = this.start_state;  // Start from the initial state
        for (char symbol : input_string.toCharArray()) {
            if (!this.alphabet.contains(Character.toString(symbol))) {  // Check the validity of the alphabet symbol
                return false;
            }
            current_state = this.transitions.get(current_state).get(Character.toString(symbol));  // Transition to the next state
            if (current_state == null) {
                return false;  // If no transition exists for the symbol, reject the string
            }
        }
        return this.accept_states.contains(current_state);  // Check if the current state is an accepting state
    }

    public static DFA read_dfa_from_file(String filePath) throws FileNotFoundException {
        File file = new File(filePath);
        Scanner scanner = new Scanner(file);

        // Read the DFA specifications from the input file
        String[] alphabets = scanner.nextLine().split(" ");
        Set<String> alphabet = new HashSet<>();
        for (String alpha : alphabets) {
            alphabet.add(alpha);
        }

        String[] statess = scanner.nextLine().split(" ");
        Set<String> states = new HashSet<>();
        for (String state : statess) {
            states.add(state);
        }

        String start_state = scanner.nextLine();
        String[] accept_statess = scanner.nextLine().split(" ");
        Set<String> accept_states = new HashSet<>();
        for (String accept_state : accept_statess) {
            accept_states.add(accept_state);
        }

        Map<String, Map<String, String>> transitions = new HashMap<>();
        while (scanner.hasNextLine()) {
            String line = scanner.nextLine();
            String[] transition = line.split(" ");
            String source = transition[0];
            String symbol = transition[1];
            String target = transition[2];
            if (!transitions.containsKey(source)) {
                transitions.put(source, new HashMap<>());
            }
            transitions.get(source).put(symbol, target);
        }

        return new DFA(states, alphabet, transitions, start_state, accept_states);
    }

    public static void main(String[] args) throws FileNotFoundException {
        DFA dfa_object = DFA.read_dfa_from_file("DFA_Input_1.txt");

        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a string: ");
        String input_string = scanner.nextLine();
        if (dfa_object.run(input_string)) {
            System.out.println("Accepted");
        } else {
            System.out.println("Rejected");
        }
    }

    public Set<String> getStates() {
        return states;
    }

    public void setStates(Set<String> states) {
        this.states = states;
    }

    public Set<String> getAlphabet() {
        return alphabet;
    }

    public void setAlphabet(Set<String> alphabet) {
        this.alphabet = alphabet;
    }

    public Map<String, Map<String, String>> getTransitions() {
        return transitions;
    }

    public void setTransitions(Map<String, Map<String, String>> transitions) {
        this.transitions = transitions;
    }

    public String getStart_state() {
        return start_state;
    }

    public void setStart_state(String start_state) {
        this.start_state = start_state;
    }

    public Set<String> getAccept_states() {
        return accept_states;
    }

    public void setAccept_states(Set<String> accept_states) {
        this.accept_states = accept_states;
    }

    public String getCurrent_state() {
        return current_state;
    }

    public void setCurrent_state(String current_state) {
        this.current_state = current_state;
    }
}
