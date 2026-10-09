"""Recompute final artifact acceptance and durations using archived evidence only."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = {'baseline': 'ChatDev 基线', 'mpst': 'ChatDev + MPST', 'mpst_contract': 'ChatDev + MPST + 契约'}
EXPECTED = {'baseline': (300, 88), 'mpst': (300, 91), 'mpst_contract': (360, 200)}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def metrics(records):
    values = [r['elapsed_seconds'] for r in records]
    passed = sum(r['artifact_pass'] is True for r in records)
    return {'runs': len(records), 'artifact_passed': passed, 'artifact_acceptance_percent': passed / len(records) * 100,
            'mean_seconds': statistics.mean(values), 'median_seconds': statistics.median(values),
            'p90_seconds_nearest_rank': sorted(values)[math.ceil(len(values) * .9) - 1]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-hashes', action='store_true')
    args = parser.parse_args()
    records = read(ROOT / 'data/records.json')
    tasks = read(ROOT / 'data/tasks.json')
    assert len(tasks) == 30 and len(records) == 960
    assert len({r['run_id'] for r in records}) == 960
    for r in records:
        assert tasks[r['task_index']]['project_name'] == r['project_name']
        assert type(r['artifact_pass']) is bool
        assert isinstance(r['elapsed_seconds'], (int, float)) and math.isfinite(r['elapsed_seconds']) and r['elapsed_seconds'] >= 0
        evaluation = read(ROOT / r['evaluation_source'])
        run = read(ROOT / r['run_result_source'])
        assert evaluation['artifact_pass'] == r['artifact_pass'], r['run_id']
        assert run['elapsed_seconds'] == r['elapsed_seconds'], r['run_id']
        if r['supplemental_evaluation']:
            assert run.get('artifact_pass') is None, r['run_id']
    assert sum(r['supplemental_evaluation'] for r in records) == 2
    if args.verify_hashes:
        for entry in read(ROOT / 'data/provenance.json'):
            assert hashlib.sha256((ROOT / entry['path']).read_bytes()).hexdigest() == entry['published_sha256'], entry['path']
        for variant in ['chatdev-mpst', 'pure-contract', 'inline-contract']:
            source = ROOT / 'source' / variant
            for name, value in read(source / 'SOURCE_MANIFEST.json')['files'].items():
                assert hashlib.sha256((source / name).read_bytes()).hexdigest() == value, name
    groups = {}
    rounds = []
    for condition in CONDITIONS:
        subset = [r for r in records if r['condition'] == condition]
        groups[condition] = metrics(subset)
        assert (len(subset), groups[condition]['artifact_passed']) == EXPECTED[condition]
        for number in sorted({r['round'] for r in subset}):
            batch = [r for r in subset if r['round'] == number]
            assert sorted(r['task_index'] for r in batch) == list(range(30))
            rounds.append({'condition': condition, 'round': number, **metrics(batch)})
    report = {'groups': groups, 'rounds': rounds, 'unique_tasks': 30,
              'timing_includes_independent_artifact_evaluation': False,
              'artifact_acceptance_is_gold_test_accuracy': False}
    output = ROOT / 'reports'
    output.mkdir(exist_ok=True)
    (output / 'summary.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (output / 'records.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader(); writer.writerows(records)
    lines = ['# 最终产物评估与实验耗时', '', '本表仅读取历史证据，不调用模型。', '',
             '| 方案 | 运行数 | 最终通过数 | 最终通过率 | 平均耗时/秒 | 中位耗时/秒 |',
             '|---|---:|---:|---:|---:|---:|']
    for key, g in groups.items():
        lines.append(f"| {CONDITIONS[key]} | {g['runs']} | {g['artifact_passed']} | {g['artifact_acceptance_percent']:.2f}% | {g['mean_seconds']:.2f} | {g['median_seconds']:.2f} |")
    lines += ['', '同一组 30 题重复运行：基线与 MPST 各 10 轮，契约 12 轮。这里只统计最终产物，不用流程是否结束替代产物结果。', '',
              '最终通过率是自动产物验收代理指标（编译、完整性与独立模型评审），不是标准答案单元测试正确率。', '',
              '计时不包含独立产物评审；包括超时和提前停止。版本、配套提示、运行日期不同，不能把差异全部归因于契约检查。', '',
              '契约组 R1、R3 各补评一条原评审接口异常记录，保留原始结果和补评文件；补评只填补缺失值。', '',
              '## 分轮结果', '', '| 方案 | 轮次 | 最终通过数/30 | 平均耗时/秒 |', '|---|---:|---:|---:|']
    for r in rounds:
        lines.append(f"| {CONDITIONS[r['condition']]} | {r['round']} | {r['artifact_passed']}/30 | {r['mean_seconds']:.2f} |")
    (output / 'results.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'verified_records': len(records), 'verified_supplements': 2, 'groups': groups}, ensure_ascii=False))


if __name__ == '__main__':
    main()
