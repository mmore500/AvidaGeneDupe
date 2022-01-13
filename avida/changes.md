# Changes from original version of Avida

- Output more detailed slip mutation information (detail.spop)
  - NOTE: These changes will likely only work for default reproduction (asexual) and hardware settings.
  - NOTE: Currently only adding output for on divide slip mutations
  - Add MutationInfo struct for tracking mutation information
  - Add mutation information member variable to `Genome` class (`Genome.h`)
    - Modify `Genome` constructors and offspring construction in `ActivateOffspring` function (`cPopulation.cc`) to pass mutation information w/offspring submitted to birthchamber.
  - ?Move slip mutations to happen after other types of mutations?
    - TODO: figure out what information we want to track
  - Pass mutation information through (don't modify or use) in analyze mode