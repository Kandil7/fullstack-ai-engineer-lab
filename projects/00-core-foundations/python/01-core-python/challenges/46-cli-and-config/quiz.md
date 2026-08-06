# Challenge 46 — Quiz: CLI & Configuration

1. `sys.argv[0]` is:
   - A) the first argument  (B) the script name  (C) always `"--help"`  (D) undefined
2. argparse converts argument strings to typed values via:
   - A) `cast=`  (B) `type=`  (C) `fmt=`  (D) `convert=`
3. `--verbose` as a boolean flag uses:
   - A) `action="store_true"`  (B) `type=bool`  (C) `default=flag`  (D) `nargs=0`
4. A `required=True` option:
   - A) is ignored  (B) fails fast when missing  (C) prompts interactively  (D) sets a default
5. Secrets should live:
   - A) in source code  (B) in the environment  (C) in `--help`  (D) in test files
6. Correct precedence is:
   - A) default > file > env > CLI  (B) CLI > env > file > default  (C) env > CLI > default  (D) file > CLI
7. `main(argv=None) -> int` makes the CLI:
   - A) slower  (B) unit-testable  (C) web-ready  (D) async
8. Diagnostics should be printed to:
   - A) `stdout`  (B) `sys.stderr`  (C) a log file only  (D) nowhere

**Answers:** 1-B, 2-B, 3-A, 4-B, 5-B, 6-B, 7-B, 8-B
