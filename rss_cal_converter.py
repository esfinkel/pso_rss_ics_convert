import xml.etree.ElementTree as ET
from icalendar import Calendar, Event
from dateutil.parser import parse
from datetime import timedelta, datetime

def create_ics(xml_file, ics_file):
    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Create calendar
    cal = Calendar()

    # Cut-off date
    cut_off_date = datetime(2024, 1, 1)

    # Counters for validation
    total_events = 0
    added_events = 0

    # Iterate over items in XML
    for item in root.iter('item'):
        total_events += 1

        # Extract values
        title = item.find('title').text
        presenter = item.find('presenter').text
        link = item.find('link').text
        venue = item.find('venue').text if item.find('venue') is not None else None
        event_date = parse(item.find('datetime').text)

        # Ignore if before cut-off date
        if event_date < cut_off_date:
            print(f"Event '{title}' on {event_date.strftime('%Y-%m-%d')} is before the cut-off date. Skipping.")
            continue

        # Create event
        event = Event()

        # Set properties
        event.add('summary', "PSO concert - " + title)
        event.add('dtstart', event_date)
        event.add('dtend', event_date + timedelta(hours=2.5))
        description = f"Presenter: {presenter}\nLink: {link}"
        if venue is not None:
            description += f"\nVenue: {venue}"
        event.add('description', description)

        # Add event to calendar
        cal.add_component(event)
        added_events += 1
        print(f"Added event '{title}' on {event_date.strftime('%Y-%m-%d')} to the calendar.")

    # Write to file
    with open(ics_file, 'wb') as f:
        f.write(cal.to_ical())

    print(f"\nProcessed {total_events} events in total.")
    print(f"Added {added_events} events to the calendar.")
    print("wrote to", ics_file)

# Use the function
create_ics('events_2026_27.xml', 'psoevents_2026_27.ics')

