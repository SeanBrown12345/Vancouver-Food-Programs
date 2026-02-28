# CHANGELOG

## 0.1.0
### Added
- Initial Repo Setup
- Project Board Setup
- Drafted a proposal Document
- Conducted initial EDA on dataset
- Created a sketch design for dashboard app
- Created skeleton for dashboard app
- updated README and other relevant files

## 0.2.0
### Added 
- App Specification: reports/m2_spec.md 
- App Code Revisions
- Deployment Setup: Deployment to Posit Connect Cloud is set up on both main (stable, no autoupdate) and dev (preview) branches.
- Working App: Functional prototype deployed; both URLs added to repo "About" section.
- Release v0.2.0: Created on GitHub with release notes.

### Changed
- Deviated from original app sketch by removing distribution charts and using those cards for row details instead.
- Original summary statistics in sketch slightly modified to show proportions instead.
- README and Demo: Updated README with embedded demo animation and deployed link.

### Fixed
- Based on instructor feedback in #18, changed original single-select widgets to selectize widgets for the dropdowns

### Known Issues
- N/A

### Reflection 
From the spec file ('reports/m2_spec.md'), all job stories have been implemented. 

Originally, we were planning to have some histograms / bar charts on the right-hand side of the dashboard. However, after discussion and visualizing this on the dashboard, we realized the graphs would not 1) be visually appealing or fit nicely, and 2) not really be useful to our end-user. Regarding the latter point, our user is a layperson who is wanting to find low-cost or free food programs near them. So, having summary statistics about wheelchair accessibility, percentage that are low-cost versus free, etc. would not be useful to this individual. Therefore, we decided to simplify and have the map plus the location descriptions as the main focal point of the dashboard.  
 