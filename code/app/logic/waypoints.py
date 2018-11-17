from datetime import datetime


def assemble_waypoints(proposal):
    results = proposal['results']

    last = False
    if len(results) <= 0:
        last = True

    waypoints = []
    ti = type_info(proposal)
    waypoints.append({'date': proposal['date'],
                      'icon': ti['icon'],
                      'title': ti['text'],
                      'text': '',
                      'last': last})

    i = 0
    for result in results:
        title = result['committee_name']
        icon = 'user'
        if 'Versammlung' in title or 'versammlung' in title:
            icon = 'users'
        if 'Ausschuss' in title or 'ausschuss' in title:
            icon = 'user'

        i += 1
        last = False
        if i >= len(results):
            last = True
            icon = 'book'

        waypoints.append({'date': result['result_time'],
                          'icon': icon,
                          'title': title,
                          'text': result['result_description'],
                          'last': last})

    return waypoints


def status_color(proposal):
    color = {'bg': 'grey',
             'text': 'black'}

    if proposal['status'] == 'Erledigt':
        color = {'bg': 'green',
                 'text': 'white'}
    # TODO evaluate by result description 

    return color


def type_info(proposal):
    proposal_type = proposal['type']

    switcher_icon = {
        'Antrag': 'book-open',
        'Anfrage': 'file-text',
        'Aenderungsantrag': 'edit',
        'Ergaenzungsantrag': 'file-plus',
        'Dringlichkeitsantrag': 'chevrons-right',
        'Nachpruefungsantrag': 'check-square',
        'Fragestunde': 'help-circle',
        'Aktuelle Stunde': 'grid',
    }

    switcher_text = {
        'Antrag': 'Antrag gestellt',
        'Anfrage': 'Anfrage gestellt',
        'Aenderungsantrag': 'Aenderungsantrag gestellt',
        'Ergaenzungsantrag': 'Ergaenzungsantrag gestellt',
        'Dringlichkeitsantrag': 'Dringlichkeitsantrag gestellt',
        'Nachpruefungsantrag': 'Nachpruefungsantrag gestellt',
        'Fragestunde': 'Fragestunde',
        'Aktuelle Stunde': 'Aktuelle Stunde',
    }

    return {'icon': switcher_icon.get(proposal_type, 'book-open'),
            'text': switcher_text.get(proposal_type, 'Antrag gestellt')}