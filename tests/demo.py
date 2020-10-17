from brzo.graphviz import get_dfa, get_dfa_without_error_state


if __name__ == "__main__":
    regexpr = "(ab)*cad|da|raa"
    g = get_dfa_without_error_state("abracd", regexpr)
    g.format = "png"
    g.render()
    