from app.logic.waypoints import switcher_icon


def prepare_proposals(proposals):
    ps = []

    for p in proposals:
        icon = switcher_icon.get(p['type'], 'book-open')
        d = {'icon': icon}
        ps.append({**p, **d})

    return ps
