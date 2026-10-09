        if command in ('moves', 'hint'):
            for start, paths in sorted(game.legal_moves().items()):
                for p in paths:
                    print('  ' + format_path(p))
            continue