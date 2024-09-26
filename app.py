import requests
from scholarly import scholarly
def extract_scholar_data(faculty_name, n=10):
    scholar_data = []
    print(f"Searching for publications by {faculty_name} on Google Scholar...")
    try:
        search_query = scholarly.search_author(faculty_name)
        author = next(search_query)

        author_filled = scholarly.fill(author)
        print(f"\nGoogle Scholar Author: {author_filled['name']}")
        print(f"Affiliation: {author_filled['affiliation']}")
        print(f"Total Citations: {author_filled.get('citedby', 'N/A')}")
        print("Google Scholar Publications:")

        for publication in author_filled['publications'][:n]:
            pub_filled = scholarly.fill(publication)
            print(f"- {pub_filled['bib']['title']} ({pub_filled['bib'].get('pub_year', 'N/A')})")
            print(f"  Citations: {pub_filled.get('num_citations', 0)}")

    except StopIteration:
        print(f"Author {faculty_name} not found on Google Scholar.")
    except Exception as e:
        print(f"Error occurred while fetching Google Scholar data: {e}")

def extract_dblp_data(faculty_name, n=5):
    print(f"\nSearching for publications by {faculty_name} on DBLP...")
    try:
        query_url = f'https://dblp.org/search/publ/api?q={faculty_name}&format=json'

        response = requests.get(query_url)
        data = response.json()

        if 'result' in data and 'hits' in data['result'] and 'hit' in data['result']['hits']:
            publications = data['result']['hits']['hit']

            print(f"\nDBLP Publications by {faculty_name}:")
            for pub in publications[:n]:
                pub_info = pub['info']
                authors = pub_info['authors']['author']
                if isinstance(authors, dict):  
                    author_names = authors['text']
                else:  
                    author_names = ', '.join([author['text'] if isinstance(author, dict) else author for author in authors])

                print(f"- {pub_info['title']} ({pub_info.get('year', 'Unknown Year')})")
                print(f"  Venue: {pub_info.get('venue', 'Unknown Venue')}")
                print(f"  Authors: {author_names}")
        else:
            print(f"No publications found for {faculty_name} on DBLP.")
    except Exception as e:
        print(f"Error occurred while fetching DBLP data: {e}")

def search_publications(faculty_name, n=5):
    extract_scholar_data(faculty_name, n)
    extract_dblp_data(faculty_name, n)

if __name__ == "__main__":
    faculty_name = 'Benjamin W.J. Kwok' 
    n = 10  
    search_publications(faculty_name, n)
