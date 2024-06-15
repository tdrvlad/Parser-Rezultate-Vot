from bs4 import BeautifulSoup


COUNT_VOTERS = 'alegători înscriși în liste'
COUNT_PRESENT_VOTERS = 'alegători prezenți la urne'
COUNT_VALID_VOTES = 'voturi valabil exprimate'
COUNT_INVALID_VOTES = 'voturi nule'


def convert_to_float(european_number_str):
    # Replace the thousand separator (.) with nothing
    # Replace the decimal separator (,) with a dot (.)
    clean_str = european_number_str.replace('.', '').replace(',', '.')
    return float(clean_str)


def validate_statistics(stats_dict: dict) -> dict:
    numbers_stats_dict = {k: convert_to_float(v) for k, v in stats_dict.items()}
    num_voters = numbers_stats_dict[COUNT_PRESENT_VOTERS]
    invalid_votes = numbers_stats_dict[COUNT_INVALID_VOTES]
    valid_votes = numbers_stats_dict[COUNT_VALID_VOTES]

    if valid_votes + invalid_votes != num_voters:
        print(f"Mismatch in stats: {num_voters} != {valid_votes} + {invalid_votes}")
    return numbers_stats_dict


def extract_election_statistics(html_content: str) -> dict:
    soup = BeautifulSoup(html_content, 'html.parser')

    stats = {
        COUNT_VOTERS: None,
        COUNT_PRESENT_VOTERS: None,
        COUNT_VALID_VOTES: None,
        COUNT_INVALID_VOTES: None,
    }

    try:
        showcase_items = soup.find_all('div', class_='ElectionResultsProcess-module_showcaseContainer__1lzg_')
        for item in showcase_items:
            value = item.find('h2').text.strip()
            label = item.find('div', class_='Typography-module_bodyLarge__15VfE').text.strip()
            if COUNT_VOTERS in label:
                stats[COUNT_VOTERS] = value
            elif COUNT_PRESENT_VOTERS in label:
                stats[COUNT_PRESENT_VOTERS] = value
            elif COUNT_VALID_VOTES in label:
                stats[COUNT_VALID_VOTES] = value
            elif COUNT_INVALID_VOTES in label:
                stats[COUNT_INVALID_VOTES] = value

        if None in stats.values():
            missing_fields = [key for key, value in stats.items() if value is None]
            print(f"Warning: Missing fields - {', '.join(missing_fields)}")
            return None

        return validate_statistics(stats)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
