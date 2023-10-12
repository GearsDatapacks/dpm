# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0-rc1] - 2023-10-12
Increased customisability

### Added
- Basic config file

### Changed
- DPM now by default only downloads the latest stable version of a datapack, this behaviour can be overridden
- DPM now donwloads datapacks into the parent directory when inside a project folder

### Fixed
- Skipping remaining downloads if a file is already present
- Storing data in undesirable location on windows

## [0.1.0-beta-1] - 2023-09-01
Useful functions

### Added
- `dpm create` for datapack generation from templates
- `dpm alias` for auth aliasing
- `--version` flag

### Changed
- The `dpm` command now prints the help message on invalid input

### Fixed
- `dpm init` generating null fields

## [0.1.0-alpha-3] - 2023-08-28
Switched to golang

### Changed
- Migrated project to golang
  - Releases now consist of a single binary, rather than entire source code
  - You don't need python installed to run dpm

## [0.1.0-alpha-2] - 2023-06-16
Improved dpm command

### Added
- Custom argument parser for dpm command
- `dpm install` to download all dependencies

### Changed
- Use the Pyrinth pip project instead of source code

## [0.1.0-alpha-1] - 2023-06-10
First version!

### Added
- Installing datapacks into a world
- Adding dependencies
- Publishing projects
