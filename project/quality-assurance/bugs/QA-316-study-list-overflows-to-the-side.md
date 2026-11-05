# QA-316: Study list overflows to the side: the # and Study name columns are cut off (names read 'on LCTS', 'nt: sized'); and the Auto-approve control in the composer shows highlighted (blue) on a new chat, again and again

| Field | Value |
|---|---|
| Status | open |
| Severity | minor |
| Area | frontend |
| Reporter | Sahand (screenshot), Manual QA-IV |
| Found | 2026-11-05 19:12 UTC |
| Versions | backend 1.1.118, frontend live 2026-11-05 20:11 CET |
| Where | https://geomind.team/projects/8d5d21e0-ecb0-4894-9cfd-bdd61f670ac7/design/study, chat panel open beside it |
| Fixer | |

## Steps

1. Open a project with 9 studies, chat panel and Design panel side by side (normal laptop width).
2. Open Study.

## Expected

The study table fits the panel: #, Study name, Status, Result, Actions visible; long names wrap; the Actions column (Compare structures, Run again) does not push the table wider than the panel.

## Actual

The table is scrolled sideways: the # column and most of each Study name are hidden ('on LCTS', 'nt: sized', 'lingPlant: LCTS'); the evolve row's 'Compare structures' + 'Run again' make the Actions column wide.
Also (Sahand: "it keeps coming up and gets on my nerves"): the composer's Auto-approve control is shown highlighted (blue) on a new, empty chat; it draws attention every time and it is not clear whether it is on. It should be a quiet toggle that clearly says off/on and is off unless the user turns it on.

## Evidence

- ![screenshot](../evidence/QA-316/1.png)

## Fix

## Retest
