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

## Fixed
Based on instructor feedback in #18, changed original single-select widgets to selectize widgets for the dropdowns

### Known Issues
- N/A

### Reflection 
From the spec file ('reports/m2_spec.md'), all job stories have been implemented. 

Originally, we were planning to have some histograms / bar charts on the right-hand side of the dashboard. However, after discussion and visualizing this on the dashboard, we realized the graphs would not 1) be visually appealing or fit nicely, and 2) not really be useful to our end-user. Regarding the latter point, our user is a layperson who is wanting to find low-cost or free food programs near them. So, having summary statistics about wheelchair accessibility, percentage that are low-cost versus free, etc. would not be useful to this individual. Therefore, we decided to simplify and have the map plus the location descriptions as the main focal point of the dashboard.  
 
## 0.3.0
### Added 
- A querychat AI chat interface
- A dataframe output component to see the filtered dataframe
- A data download button that downloads the querychat filtered dataframe
- Release v0.3.0 was created on GitHub with release notes.

### Changed
- Changed the meal cost filtering options for the food programs from $2, $4, $9.95, Free and Low cost to All, Free and Low Cost. 
- Updated requirements file with packages used in milestone 3.
- Updated only the production URL in the git hub about section based on instructors feedback.

### Fixed
- Fixed the page overflow issue based on instructor feedback in #39
- Fixed filter options for meal cost based on instructor feedback in #39

### Known Issues
- Map pins seems to disappear when selecting and deselecting filters. We attempted a fix on this issue but it only ended up making the problem worse.


### Reflection 

Asides the Jobs To Be Done(JBTD) for milestone 3, a few other fixes made were to incoporate instructor and TA's feedback.

In response to instructor feedback to use the side menu bar so the app doesn't scroll, we found a way to fix the page overflow issue without neccessarily implementing the side bar menu.

In response to instructor feedback regarding fixing the map pins, due to time constraints we were unable to resolve the issue. However, we will continue working on fixing it for the next milestone.