# MPLAD Anomaly Detection Review Summary

## Date
09/09/2026

## Reviewer
Aditi

## Cost Outlier Logic Review
### What Works
- Grouping by district + workcategory is correct
- Median calculation is accurate
- 3x threshold is appropriate

### Issues Found
- No major issue; groups with fewer than 3 projects are excluded because a median from a tiny sample is not reliable

### Suggestions
- Keep the median-only rule for fairness and consider a secondary guardrail for very small datasets

### Status
✅ Passed

## Stalled Project Logic Review
### What Works
- Pending filter is correct
- Amount threshold is appropriate
- Date calculation is accurate

### Issues Found
- The logic uses the sanction date as the delay reference. If a project was reactivated or an updated date exists, the review should use the most recent activity date instead

### Suggestions
- Consider using latest progress/update date when available

### Status
✅ Passed

## Duplicate Logic Review
### What Works
- Grouping by district + village is correct
- Similarity threshold is appropriate
- Fuzzy matching is working

### Issues Found
- Missing village values are handled as 'Unknown', which is acceptable

### Suggestions
- Add a second rule using work category and sanction date to reduce false positives

### Status
✅ Passed

## Anomaly Model Verification
- All required anomaly fields are present in the current model structure
- `project_id`, `anomaly_type`, `severity_score`, `description`, `detected_at`, `reviewed`, `notes`, `related_project_id`, and `similarity_score` are covered
- Relationship logic is consistent with a one-to-many project-to-anomaly design and a duplicate-related project link

## Final Status
✅ Review complete and ready to share with the team
