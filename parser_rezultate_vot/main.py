from parser_rezultate_vot.constants import VOTE_TYPE_DICT, COUNTY_DICT, URL_TEMPLATE
from parser_rezultate_vot.extract_html import get_html_content, filter_html_content
from parser_rezultate_vot.extract_statistics import extract_election_statistics
from multiprocessing import Pool, cpu_count
import pandas as pd


RESULTS_FILE = './data/Statistici-Alegeri-2024.xlsx'


def print_stats():
    for vote_type_name, vote_type_id in VOTE_TYPE_DICT.items():
        print(f"\n{vote_type_name}\n")
        for county_name, county_id in COUNTY_DICT.items():
            stats_url = URL_TEMPLATE.format(county_id=county_id, vote_type_id=vote_type_id)
            content = get_html_content(stats_url)
            filtered_content = filter_html_content(content)

            print(f'\n{county_name}')
            stats = extract_election_statistics(filtered_content)

            if stats is None:
                print(f"Error for {county_name}")
                continue

            for k, v in stats.items():
                print(f"{k}: {v}")


def fetch_county_data(args):
    vote_type_id, county_name, county_id, url_template = args
    stats_url = url_template.format(county_id=county_id, vote_type_id=vote_type_id)
    content = get_html_content(stats_url)
    filtered_content = filter_html_content(content)

    print(f'Processing {county_name}')
    stats = extract_election_statistics(filtered_content)

    if stats is None:
        print(f"Error for {county_name}")
        return None

    # Add county name to the statistics
    stats['County'] = county_name
    return stats


def gather_data(vote_type_id, url_template, num_workers):
    args = [(vote_type_id, county_name, county_id, url_template) for county_name, county_id in COUNTY_DICT.items()]
    with Pool(num_workers) as pool:
        results = pool.map(fetch_county_data, args)
    # Filter out None results
    results = [result for result in results if result is not None]
    df = pd.DataFrame(results)

    # Add total row
    if not df.empty:
        totals = df.select_dtypes(include='number').sum()
        totals['County'] = 'Total'
        df = pd.concat([df, pd.DataFrame(totals).T], ignore_index=True)
    return df


def save_to_excel(excel_path, data_frames):
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        for vote_type_name, df in data_frames.items():
            df.to_excel(writer, sheet_name=vote_type_name, index=False)
            print(f"Sheet {vote_type_name} written successfully.")
    print("All data written to election_statistics.xlsx successfully.")


def main(num_workers=4):
    data_frames = {}
    for vote_type_name, vote_type_id in VOTE_TYPE_DICT.items():
        print(f"\nProcessing statistics for: {vote_type_name}\n")
        df = gather_data(vote_type_id, URL_TEMPLATE, num_workers)
        data_frames[vote_type_name] = df

    save_to_excel(RESULTS_FILE, data_frames)


if __name__ == "__main__":
    main(num_workers=8)
