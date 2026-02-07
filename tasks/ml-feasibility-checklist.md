# ML Feasibility Checklist

Use this checklist when a task may require a model.

## Gates
- [ ] Data available and licensed for local use
- [ ] Hardware budget documented (CPU/GPU, memory)
- [ ] Runtime budget documented (target duration)
- [ ] Acceptance metric defined (quality threshold)

## Decision
- [ ] Local training/inference path selected when all gates pass
- [ ] Deterministic scripted fallback selected when any gate fails
- [ ] Decision recorded in run notes with `[ASSUMPTION]` where needed
