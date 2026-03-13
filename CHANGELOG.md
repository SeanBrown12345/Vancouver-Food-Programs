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


## [0.4.0] - 15-3-2026

### Added 
- Playwright testing for app, [PR #61](https://github.com/UBC-MDS/DSCI-532_2026_22_Vancouver-LC_Food-Programs/pull/61), [PR #69](https://github.com/UBC-MDS/DSCI-532_2026_22_Vancouver-LC_Food-Programs/pull/69), [PR #68](https://github.com/UBC-MDS/DSCI-532_2026_22_Vancouver-LC_Food-Programs/pull/68)
- Refactored app code into separate function and created unit tests [PR #61](https://github.com/UBC-MDS/DSCI-532_2026_22_Vancouver-LC_Food-Programs/pull/61)
- Converted app to use Parquet + DuckDB instead of CSV [PR #58](https://github.com/UBC-MDS/DSCI-532_2026_22_Vancouver-LC_Food-Programs/pull/58)

### Changed
- (Addressing Feedback) Moved the download CSV button into the dataframe card as suggested by instructor. [PR #67](https://github.com/UBC-MDS/DSCI-532_2026_22_Vancouver-LC_Food-Programs/pull/67)   
- (Addressing Feedback) Removed all @output decorators from app as suggested by instructor. [PR #76](https://github.com/UBC-MDS/DSCI-532_2026_22_Vancouver-LC_Food-Programs/pull/76)
- Updated CONTRIBUTING.md with M3 retrospective and M4 collaboration norms. [PR #73](https://github.com/UBC-MDS/DSCI-532_2026_22_Vancouver-LC_Food-Programs/pull/73)


### Fixed
- (Addressing Feedback) Fixed the map pins disappearing issue by refactoring the app to use a plotly map instead of ipyleaflet. [PR #78](https://github.com/UBC-MDS/DSCI-532_2026_22_Vancouver-LC_Food-Programs/pull/78)
 
### Known Issues
- N/A


### Release Highlight: Map Drilldown

Our advanced feature requirement was already satisfied in the previous milestones with the implementation of the map drilldown functionality. Since this requirement was already fufilled, we were told by the instructor that we didn't have to implement another advanced feature for this milestone. Therefore, just keep in mind that this feature has existed since Milestone 2.

- **Option chosen:**  D
- **PR:** [PR #19](https://github.com/UBC-MDS/DSCI-532_2026_22_Vancouver-LC_Food-Programs/pull/19)
- **Why this option over the others:** This feature was chosen because it allows users to see more details about the food programs by clicking on the map pins, which is a key aspect of our app. This feature enhances the user experience by allowing the map to be used as an input and output feature, enabling users to explore the data more interactively.
- **Feature prioritization issue link:** https://github.com/UBC-MDS/DSCI-532_2026_22_Vancouver-LC_Food-Programs/issues/64

### Collaboration
- **CONTRIBUTING.md:** https://github.com/UBC-MDS/DSCI-532_2026_22_Vancouver-LC_Food-Programs/pull/73
- **M3 retrospective:** 
During Milestone 3, our team successfully implemented the main features of the dashboard, including filtering, summary outputs, map display, and the AI explorer. However, we noticed several areas where our workflow could be improved.

Because team members had different schedules, some work was completed close to the deadline. This caused a few pull requests to be merged later than planned, which made reviewing and testing more rushed. We also found that some discussions happened outside GitHub, so the reasoning behind certain changes was not always recorded in Issues or Pull Requests.

Overall, Milestone 3 went well, but the team agreed that better planning and
more consistent use of GitHub tools would make collaboration smoother.
- **M4:** 
For Milestone 4, we decided to improve our workflow to make the final stage of the project more organized.

We agreed on the following rules:

- All changes should be done in a separate branch  
- Every change must go through a Pull Request before merging  
- Pull requests should stay small and focused on one issue  
- At least one teammate should review each Pull Request  
- Issues should be created before starting larger changes  
- Work should be started earlier to avoid last-minute commits  
- Each team member should complete at least one feedback item  
- Important discussions should be recorded in GitHub Issues or PR comments  

These guidelines help keep the project history clear and ensured that all team members contributed during the final milestone. Overall, collaboration during Milestone 4 was much smoother, and we were able to complete the project successfully with no last minute rushes by following these rules.

### Reflection

Overall, our team is very happy with the outcome of our project. The dashboard is functional, visually appealing, and meets the needs of the target users we outlined in M1. We were able to implement all of the core features with no known issues, and we also added some advanced features that enhance the user experience. We are proud of the work we have done and believe that our project will be useful for individuals looking for food programs in Vancouver.

Testing Coverage:

- test_mealcost_filter (unit tests): Verifies that the filter_by_meal_cost function correctly filters the dataset based on the selected meal cost option.

- test_meal_cost_filter_options (playwright):  Verifies that the selections in the "Meal Cost" filter only display "All", "Free" and "Low Cost" options. This can break if filter options are changed by the Open Data Vancouver.

- test_feature_checkbox_* (playwright): Verifies that the feature checkboxes correctly filter the dataset based on the selected features (wheelchair accessibility, takeout available, provides hampers, delivery available). This can break if the feature options values (Yes/No to True/False) changed.

- test_dashboard_tab_shows_summary_and_map (playwright): Checks that the Dashboard tab displays the overview summary and map components.

- test_filter_panel_labels_are_rendered (playwright): Checks that the main filter panel renders its key controls. This can break if the filter panel is redesigned and the labels are changed.


In the feedback we received from our peers and instructors, we identified only two critical issues that we absolutely needed to address, with the rest being minor. Therefore, the prioritization of the feedback was clear: two people could focus on the critical issues while the rest of the team worked on the minor ones.

The lectures that shaped our work the most were the general Shiny dashboard lectures and the LLM lectures. These lectures were helpful because they provided us with the knowledge and tools to create a functional and visually appealing dashboard, as well as to implement the AI chat interface feature. These skills are in high demand, and most of us had no prior experience with them, so it was great to learn how to use these tools effectively in our project. Something that would have been nice to cover in the lectures is Plotly maps and a simple CSS tutorial for customizing the dashboard.