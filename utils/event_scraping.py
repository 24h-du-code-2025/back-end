import requests
from bs4 import BeautifulSoup


def transform_image_url(relative_url):
    base_url = "https://www.lemans.fr"
    if relative_url.startswith("/"):
        return base_url + relative_url
    return relative_url


def extract_html_page():
    url = 'https://www.lemans.fr/agenda/les-prochains-evenements/'
    response = requests.get(url)
    return response.content


def extract_events():
    html_content = extract_html_page()
    soup = BeautifulSoup(html_content, 'html.parser')
    event_list = soup.find('ul', class_='event-list')
    events = []
    
    if event_list:
        for event_item in event_list.find_all('li', id=lambda x: x and x.startswith('eventref-')):
            event_data = {}
            
            # Extract event date
            date_div = event_item.find('div', class_='event-date')
            event_data['date'] = date_div.get_text(strip=True) if date_div else None
            
            # Extract event image URL
            visuel_div = event_item.find('div', class_='event-visuel')
            img_tag = visuel_div.find('img') if visuel_div else None
            event_data['image_url'] = transform_image_url(img_tag['src']) if img_tag and 'src' in img_tag.attrs else None
            
            # Extract event title
            title_h3 = event_item.find('h3', class_='event-title')
            show_expanded_span = title_h3.find('span', class_='show-expanded') if title_h3 else None
            event_data['title'] = show_expanded_span.get_text(strip=True) if show_expanded_span else None
            
            # Extract category
            category_span = event_item.find('span', class_='category')
            strong_tag = category_span.find('strong') if category_span else None
            event_data['category'] = strong_tag.get_text(strip=True).strip('-').strip() if strong_tag else None
            
            # Extract event description
            desc_span = event_item.find('span', class_='mdesc more')
            event_data['description'] = desc_span.get_text(strip=True) if desc_span else None
            
            events.append(event_data)
    
    return events
    