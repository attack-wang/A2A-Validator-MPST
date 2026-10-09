def _slide_and_merge_line(self, line):
    # Remove zeros
    non_zero = [v for v in line if v != 0]
    result = []
    gained_score = 0
    i = 0
    while i < len(non_zero):
        if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
            merged = non_zero[i] * 2
            result.append(merged)
            gained_score += merged
            i += 2
        else:
            result.append(non_zero[i])
            i += 1
    # Pad with zeros
    result += [0] * (len(line) - len(result))
    return result, gained_score