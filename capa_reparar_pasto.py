"""Use a native PLACE/CARE/PASS window to finish a missing animal structure."""
_AB_PARENT = [value for value in list(globals().values()) if callable(value)][-1]
_AB_ENABLED = True
_AB_REPORT = {}
_AB_EVENTS = []
_AB_PENDING = {}


def _ab_commands(action):
    return [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]


def _ab_repair(obs, action):
    player = int(obs['player']); step = int(obs['step'])
    farm = obs['farms'][player]; private = obs['private']
    positions = [list(farm['farmer']), *map(list, farm['hands'])]
    commands = copy.deepcopy(_ab_commands(action)); original = copy.deepcopy(commands)
    processed = set()
    for key, pending in list(_AB_PENDING.items()):
        if key[0] != player:
            continue
        actor = key[1]; event = pending['event']; phase = pending['phase']
        processed.add(actor)
        expected = ['CARE'] if phase == 1 else ['PASS']
        valid = (step == event['step']+phase and actor < len(positions)
                 and actor < len(commands) and positions[actor] == event['xy']
                 and commands[actor] == expected)
        tile = farm['tiles'][event['xy'][1]][event['xy'][0]]
        if phase == 1:
            valid = (valid and isinstance(tile, dict) and tile.get('kind') == event['structure']
                     and not tile.get('animal') and private['inventories'][actor].get(event['animal'], 0) >= 1)
        else:
            valid = valid and isinstance(tile, dict) and tile.get('animal') == event['animal']
        if not valid:
            event['aborted_at'] = step
            event['abort_observation'] = dict(position=positions[actor] if actor < len(positions) else None,
                                             command=commands[actor] if actor < len(commands) else None,
                                             tile=copy.deepcopy(tile))
            _AB_REPORT['aborts'] += 1
            del _AB_PENDING[key]
            continue
        if phase == 1:
            commands[actor] = ['PLACE', event['animal']]
            _AB_REPORT['observed_builds'] += 1; _AB_REPORT['place_requests'] += 1
            pending['phase'] = 2
        else:
            commands[actor] = ['CARE']
            _AB_REPORT['observed_placements'] += 1; _AB_REPORT['care_requests'] += 1
            event['all_phases_requested'] = True
            del _AB_PENDING[key]
        event['phases'].append(dict(step=step, original=expected, emitted=copy.deepcopy(commands[actor]),
                                    tile_before=copy.deepcopy(tile), bag_before=copy.deepcopy(private['inventories'][actor])))
    if step < 648 and step % 24 <= 21:
        future1 = _ab_commands(_sr_tape(player, step+1))
        future2 = _ab_commands(_sr_tape(player, step+2))
        used = {tuple(value['event']['xy']) for key, value in _AB_PENDING.items() if key[0] == player}
        for actor, command in enumerate(original):
            if actor in processed or actor >= len(positions) or len(command) < 2:
                continue
            animal = command[1]
            if command[0] != 'PLACE' or animal not in ('COW', 'SHEEP', 'GOOSE'):
                continue
            xy = positions[actor]; x, y = xy
            if farm['tiles'][y][x] is not None or tuple(xy) in used:
                continue
            if private['inventories'][actor].get(animal, 0) < 1:
                continue
            if actor >= len(future1) or actor >= len(future2) or future1[actor] != ['CARE'] or future2[actor] != ['PASS']:
                continue
            if any(other != actor and position == xy and other < len(original)
                   and original[other] and original[other][0] not in ('PASS', 'NORTH', 'SOUTH', 'EAST', 'WEST')
                   for other, position in enumerate(positions)):
                continue
            structure = 'COOP' if animal == 'GOOSE' else 'PASTURE'
            commands[actor] = ['BUILD_' + structure]
            event = dict(step=step, actor=actor, xy=xy, animal=animal, structure=structure,
                         planned_next=[copy.deepcopy(future1[actor]), copy.deepcopy(future2[actor])],
                         phases=[dict(step=step, original=copy.deepcopy(command), emitted=copy.deepcopy(commands[actor]),
                                      tile_before=None, bag_before=copy.deepcopy(private['inventories'][actor]))])
            _AB_EVENTS.append(event)
            _AB_PENDING[player, actor] = dict(phase=1, event=event)
            used.add(tuple(xy)); _AB_REPORT['build_requests'] += 1
    if commands == original:
        return action
    return dict(action, farmer=commands[0], hands=commands[1:])


def animal_build_agent(observation, configuration=None):
    if int(observation['step']) == 0:
        _AB_PENDING.clear(); _AB_EVENTS.clear(); _AB_REPORT.clear()
        _AB_REPORT.update(build_requests=0, observed_builds=0, place_requests=0,
                          observed_placements=0, care_requests=0, aborts=0, errors=0)
    result = _AB_PARENT(observation, configuration)
    if not _AB_ENABLED:
        return result
    if configuration is not None and any(configuration.get(key, value) != value for key, value in (
            ('boardSize', 10), ('turnsPerDay', 24), ('shedCapacity', 100), ('maxMarketOrdersPerTurn', 10))):
        return result
    try:
        return _ab_repair(observation, result)
    except Exception:
        _AB_REPORT['errors'] += 1
        return result


animal_build_agent.telemetry = _AB_REPORT
animal_build_submission = animal_build_agent
