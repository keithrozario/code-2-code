## Step 1:

```bash
codmod create full -c moneynote-api/ \
--format markdown \
-o customized_report_money_note_detailed_journeys.md \
--context-file context-file.md
```

```bash
codmod create data-layer -c moneynote-api/ \
--format markdown \
-o customized_report_money_note_data_layer.md
```

## Step 3:

  $ python gen_user_j.py

This generated the user journeys. Don't forget to activate a new virtual environment before executing this step. You can do it this way:

  $ uv venv
  $ source ./venv/bin/activate
  $ uv sync

## Step 5: Consolidation

  $ python gen_fs.py
