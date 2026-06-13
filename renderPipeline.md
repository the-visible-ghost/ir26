# Master Filtering Pipeline ->
- take a ranking of suspiciousness and map it to all candidates, increment if they fail the checks listed below.
- ### Sanity + Honeypot Detection
  - don't care about the candidate, just make sure the profile is realistically valid and internally consistent.
  - the checks--
      - Experience vs Career History
        > match the total career jobs duration with the claimed experience
        
      - Claimed Proficiency vs actual career duration
        > if a candidate claims to be `expert` in `python`, but his career duration is unrealistic like under 5 or 0, then he fails this test.
      
      - `len(expert_languages)` > `years_of_exp`^2
      
      - career jobs timeline overlap [Special Case]
        > candidate worked `2023-2024` in Google and `2021-2025` in Flipkart, which overlaps with Google.
          this doesn't directly increase the suspiciousness because it can be possible in some cases.
          This is a special case that alters/checks/calls these additional checks: ![>](https://img.shields.io/badge/TODO-blue)
