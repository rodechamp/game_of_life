import game_of_life as gol


def main() -> None:
    gol.demo.compare_rules(100, length=100, height=100, p_live=0.1)
    
    return None


if __name__ == '__main__':
    main()