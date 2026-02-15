#!/usr/bin/env python3
"""
Quality Scoring System for NutriGene AI

Calculates objective quality scores (0-100) based on defined rubrics.
Enforces quality gates: 80 (commit), 90 (PR), 95 (excellence).

Usage:
    python scripts/quality_score.py src/models/nutrition.py
    python scripts/quality_score.py src/models/nutrition.py --summary
    python scripts/quality_score.py src/**/*.py
    python scripts/quality_score.py scripts/R/analysis.R
"""

import sys
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
import re
import json

# ==============================================================================
# SCORING RUBRIC (from .claude/rules/quality-gates.md)
# ==============================================================================

PYTHON_RUBRIC = {
    'critical': {
        'import_error': {'points': 100, 'auto_fail': True},
        'missing_type_hints': {'points': 15},
        'no_tests': {'points': 15},
        'hardcoded_credentials': {'points': 20},
    },
    'major': {
        'missing_error_handling': {'points': 5},
        'no_input_validation': {'points': 5},
        'hardcoded_path': {'points': 5},
    },
    'minor': {
        'missing_docstring': {'points': 1},
        'long_line': {'points': 1},
    }
}

R_SCRIPT_RUBRIC = {
    'critical': {
        'syntax_error': {'points': 100, 'auto_fail': True},
        'hardcoded_path': {'points': 20},
        'missing_library': {'points': 10},
    },
    'major': {
        'missing_set_seed': {'points': 10},
        'missing_figure': {'points': 5},
        'missing_rds': {'points': 5},
    },
    'minor': {
        'style_violation': {'points': 1},
        'missing_roxygen': {'points': 1},
    }
}

THRESHOLDS = {
    'commit': 80,
    'pr': 90,
    'excellence': 95
}

# ==============================================================================
# ISSUE DETECTION
# ==============================================================================

class IssueDetector:
    """Detect common issues for quality scoring."""

    @staticmethod
    def check_python_syntax(filepath: Path) -> Tuple[bool, str]:
        """Check if Python file has syntax errors."""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'py_compile', str(filepath)],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                return False, result.stderr
            return True, ""
        except subprocess.TimeoutExpired:
            return False, "Syntax check timeout"

    @staticmethod
    def check_python_type_hints(content: str) -> List[int]:
        """Detect public functions missing type hints."""
        issues = []
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Match function definitions that don't start with _
            match = re.match(r'\s*def\s+([a-zA-Z][a-zA-Z0-9_]*)\s*\(', line)
            if match and not match.group(1).startswith('_'):
                # Check if return type annotation exists
                if '->' not in line:
                    issues.append(i)
        return issues

    @staticmethod
    def check_hardcoded_paths(content: str) -> List[int]:
        """Detect absolute paths in code."""
        issues = []
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if re.search(r'["\'][/\\]|["\'][A-Za-z]:[/\\]', line):
                if not re.search(r'http:|https:|file://|/tmp/|/dev/', line):
                    issues.append(i)
        return issues

    @staticmethod
    def check_hardcoded_credentials(content: str) -> List[int]:
        """Detect potential hardcoded credentials."""
        issues = []
        lines = content.split('\n')
        patterns = [
            r'password\s*=\s*["\']',
            r'api_key\s*=\s*["\']',
            r'secret\s*=\s*["\']',
            r'token\s*=\s*["\'](?!{)',  # exclude template strings
        ]
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('#') or stripped.startswith('//'):
                continue
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(i)
                    break
        return issues

    @staticmethod
    def check_missing_docstrings(content: str) -> List[int]:
        """Detect public functions/classes missing docstrings."""
        issues = []
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            match = re.match(r'\s*(def|class)\s+([a-zA-Z][a-zA-Z0-9_]*)', line)
            if match and not match.group(2).startswith('_'):
                # Check next non-empty line for docstring
                for j in range(i, min(i + 3, len(lines))):
                    next_line = lines[j].strip()
                    if next_line and next_line != '':
                        if not (next_line.startswith('"""') or next_line.startswith("'''")):
                            issues.append(i)
                        break
        return issues

    @staticmethod
    def check_r_syntax(filepath: Path) -> Tuple[bool, str]:
        """Check R script for syntax errors."""
        try:
            result = subprocess.run(
                ['Rscript', '-e', f'parse("{filepath}")'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                return False, result.stderr
            return True, ""
        except subprocess.TimeoutExpired:
            return False, "Syntax check timeout"
        except FileNotFoundError:
            return False, "Rscript not installed"


# ==============================================================================
# QUALITY SCORER
# ==============================================================================

class QualityScorer:
    """Calculate quality scores for project files."""

    def __init__(self, filepath: Path, verbose: bool = False):
        self.filepath = filepath
        self.verbose = verbose
        self.score = 100
        self.issues = {
            'critical': [],
            'major': [],
            'minor': []
        }
        self.auto_fail = False

    def score_python(self) -> Dict:
        """Score Python module quality."""
        content = self.filepath.read_text(encoding='utf-8')

        # Check syntax
        is_valid, error = IssueDetector.check_python_syntax(self.filepath)
        if not is_valid:
            self.auto_fail = True
            self.issues['critical'].append({
                'type': 'import_error',
                'description': 'Python syntax/import error',
                'details': error[:200],
                'points': 100
            })
            self.score = 0
            return self._generate_report()

        # Check type hints
        type_hint_issues = IssueDetector.check_python_type_hints(content)
        for line in type_hint_issues:
            self.issues['critical'].append({
                'type': 'missing_type_hints',
                'description': f'Public function missing return type hint at line {line}',
                'details': 'Add -> ReturnType annotation',
                'points': 15
            })
            self.score -= 15

        # Check hardcoded credentials
        cred_issues = IssueDetector.check_hardcoded_credentials(content)
        for line in cred_issues:
            self.issues['critical'].append({
                'type': 'hardcoded_credentials',
                'description': f'Potential hardcoded credential at line {line}',
                'details': 'Use environment variables or config files',
                'points': 20
            })
            self.score -= 20

        # Check hardcoded paths
        path_issues = IssueDetector.check_hardcoded_paths(content)
        for line in path_issues:
            self.issues['major'].append({
                'type': 'hardcoded_path',
                'description': f'Hardcoded absolute path at line {line}',
                'details': 'Use relative paths or config',
                'points': 5
            })
            self.score -= 5

        # Check docstrings
        doc_issues = IssueDetector.check_missing_docstrings(content)
        for line in doc_issues:
            self.issues['minor'].append({
                'type': 'missing_docstring',
                'description': f'Missing docstring at line {line}',
                'details': 'Add Google-style docstring',
                'points': 1
            })
            self.score -= 1

        self.score = max(0, self.score)
        return self._generate_report()

    def score_r_script(self) -> Dict:
        """Score R script quality."""
        content = self.filepath.read_text(encoding='utf-8')

        # Check syntax
        is_valid, error = IssueDetector.check_r_syntax(self.filepath)
        if not is_valid:
            self.auto_fail = True
            self.issues['critical'].append({
                'type': 'syntax_error',
                'description': 'R syntax error',
                'details': error[:200],
                'points': 100
            })
            self.score = 0
            return self._generate_report()

        # Check hardcoded paths
        path_issues = IssueDetector.check_hardcoded_paths(content)
        for line in path_issues:
            self.issues['critical'].append({
                'type': 'hardcoded_path',
                'description': f'Hardcoded absolute path at line {line}',
                'details': 'Use relative paths or here::here()',
                'points': 20
            })
            self.score -= 20

        # Check for set.seed() if randomness detected
        has_random = any(fn in content for fn in ['rnorm', 'runif', 'sample', 'rbinom', 'rnbinom'])
        has_seed = 'set.seed' in content
        if has_random and not has_seed:
            self.issues['major'].append({
                'type': 'missing_set_seed',
                'description': 'Missing set.seed() for reproducibility',
                'details': 'Add set.seed(YYYYMMDD) after library() calls',
                'points': 10
            })
            self.score -= 10

        self.score = max(0, self.score)
        return self._generate_report()

    def _generate_report(self) -> Dict:
        """Generate quality score report."""
        if self.auto_fail:
            status = 'FAIL'
            threshold = 'None (auto-fail)'
        elif self.score >= THRESHOLDS['excellence']:
            status = 'EXCELLENCE'
            threshold = 'excellence'
        elif self.score >= THRESHOLDS['pr']:
            status = 'PR_READY'
            threshold = 'pr'
        elif self.score >= THRESHOLDS['commit']:
            status = 'COMMIT_READY'
            threshold = 'commit'
        else:
            status = 'BLOCKED'
            threshold = 'None (below commit)'

        critical_count = len(self.issues['critical'])
        major_count = len(self.issues['major'])
        minor_count = len(self.issues['minor'])
        total_count = critical_count + major_count + minor_count

        return {
            'filepath': str(self.filepath),
            'score': self.score,
            'status': status,
            'threshold': threshold,
            'auto_fail': self.auto_fail,
            'issues': {
                'critical': self.issues['critical'],
                'major': self.issues['major'],
                'minor': self.issues['minor'],
                'counts': {
                    'critical': critical_count,
                    'major': major_count,
                    'minor': minor_count,
                    'total': total_count
                }
            },
            'thresholds': THRESHOLDS
        }

    def print_report(self, summary_only: bool = False) -> None:
        """Print formatted quality report."""
        report = self._generate_report()

        print(f"\n# Quality Score: {self.filepath.name}\n")

        status_emoji = {
            'EXCELLENCE': '[EXCELLENCE]',
            'PR_READY': '[PASS]',
            'COMMIT_READY': '[PASS]',
            'BLOCKED': '[BLOCKED]',
            'FAIL': '[FAIL]'
        }

        print(f"## Overall Score: {report['score']}/100 {status_emoji.get(report['status'], '')}")

        if report['status'] == 'BLOCKED':
            print(f"\n**Status:** BLOCKED - Cannot commit (score < {THRESHOLDS['commit']})")
        elif report['status'] == 'COMMIT_READY':
            print(f"\n**Status:** Ready for commit (score >= {THRESHOLDS['commit']})")
            gap_to_pr = THRESHOLDS['pr'] - report['score']
            print(f"**Next milestone:** PR threshold ({THRESHOLDS['pr']}+)")
            print(f"**Gap analysis:** Need +{gap_to_pr} points to reach PR quality")
        elif report['status'] == 'PR_READY':
            print(f"\n**Status:** Ready for PR (score >= {THRESHOLDS['pr']})")
            gap_to_excellence = THRESHOLDS['excellence'] - report['score']
            if gap_to_excellence > 0:
                print(f"**Next milestone:** Excellence ({THRESHOLDS['excellence']})")
                print(f"**Gap analysis:** +{gap_to_excellence} points to excellence")
        elif report['status'] == 'EXCELLENCE':
            print(f"\n**Status:** Excellence achieved! (score >= {THRESHOLDS['excellence']})")
        elif report['status'] == 'FAIL':
            print(f"\n**Status:** Auto-fail (syntax/import error)")

        if summary_only:
            print(f"\n**Total issues:** {report['issues']['counts']['total']} "
                  f"({report['issues']['counts']['critical']} critical, "
                  f"{report['issues']['counts']['major']} major, "
                  f"{report['issues']['counts']['minor']} minor)")
            return

        # Detailed issues
        print(f"\n## Critical Issues (MUST FIX): {report['issues']['counts']['critical']}")
        if report['issues']['counts']['critical'] == 0:
            print("No critical issues - safe to commit\n")
        else:
            for i, issue in enumerate(report['issues']['critical'], 1):
                print(f"{i}. **{issue['description']}** (-{issue['points']} points)")
                print(f"   - {issue['details']}\n")

        if report['issues']['counts']['major'] > 0:
            print(f"## Major Issues (SHOULD FIX): {report['issues']['counts']['major']}")
            for i, issue in enumerate(report['issues']['major'], 1):
                print(f"{i}. **{issue['description']}** (-{issue['points']} points)")
                print(f"   - {issue['details']}\n")

        if report['issues']['counts']['minor'] > 0 and self.verbose:
            print(f"## Minor Issues (NICE-TO-HAVE): {report['issues']['counts']['minor']}")
            for i, issue in enumerate(report['issues']['minor'], 1):
                print(f"{i}. {issue['description']} (-{issue['points']} points)\n")

        # Recommendations
        if report['status'] == 'BLOCKED':
            print("## Recommended Actions")
            print("1. Fix all critical issues above")
            print(f"2. Re-run quality score (target: >={THRESHOLDS['commit']})")
            print("3. Commit after reaching threshold\n")
        elif report['status'] == 'COMMIT_READY' and report['score'] < THRESHOLDS['pr']:
            print("## Recommended Actions to Reach PR Threshold")
            points_needed = THRESHOLDS['pr'] - report['score']
            print(f"Need +{points_needed} points to reach {THRESHOLDS['pr']}/100")
            if report['issues']['counts']['major'] > 0:
                print("Fix major issues listed above to improve score")

# ==============================================================================
# CLI INTERFACE
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Calculate quality scores for NutriGene AI project files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Score a Python module
  python scripts/quality_score.py src/models/nutrition.py

  # Score multiple files
  python scripts/quality_score.py src/**/*.py

  # Score an R script
  python scripts/quality_score.py scripts/R/analysis.R

  # Summary only
  python scripts/quality_score.py src/api/main.py --summary

  # Verbose output (include minor issues)
  python scripts/quality_score.py src/api/main.py --verbose

Quality Thresholds:
  80/100 = Commit threshold (blocks if below)
  90/100 = PR threshold (warning if below)
  95/100 = Excellence (aspirational)

Exit Codes:
  0 = Score >= 80 (commit allowed)
  1 = Score < 80 (commit blocked)
  2 = Auto-fail (syntax/import error)
        """
    )

    parser.add_argument('filepaths', type=Path, nargs='+', help='Path(s) to file(s) to score')
    parser.add_argument('--summary', action='store_true', help='Show summary only')
    parser.add_argument('--verbose', action='store_true', help='Show all issues including minor')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    results = []
    exit_code = 0

    for filepath in args.filepaths:
        if not filepath.exists():
            print(f"Error: File not found: {filepath}")
            exit_code = 1
            continue

        try:
            scorer = QualityScorer(filepath, verbose=args.verbose)

            if filepath.suffix == '.py':
                report = scorer.score_python()
            elif filepath.suffix == '.R':
                report = scorer.score_r_script()
            else:
                print(f"Error: Unsupported file type: {filepath.suffix} (supported: .py, .R)")
                continue

            results.append(report)

            if not args.json:
                scorer.print_report(summary_only=args.summary)

            if report['auto_fail']:
                exit_code = max(exit_code, 2)
            elif report['score'] < THRESHOLDS['commit']:
                exit_code = max(exit_code, 1)

        except Exception as e:
            print(f"Error scoring {filepath}: {e}")
            import traceback
            traceback.print_exc()
            exit_code = 1

    if args.json:
        print(json.dumps(results, indent=2))

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
