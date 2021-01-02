# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased] - yyyy-mm-dd

## [0.6.0] - 2021-01-02

### Added

- Ability to set an user agent for all requests
- Ability to set max retries to any value and disable it

### Changed

- Remove support for Python 3.5

## [0.5.1] - 2020-12-30

### Fixed

- Did not return a WebhookResponse object for http errors

## [0.5.0] - 2020-07-03

### Added

- Added new ability to create an Embed from a dict
- Added missing type hints
- Added API documentation for `from_dict()` and `asdict()`

### Changes

- Removed support for Python 3.4
- Renamed `to_dict()` to `asdict()`

## [0.4.1] - 2020-06-15

### Fixed

- Wrong PyPI upload format

## [0.4.0] - 2020-06-14

### Added

- Automatic retries on retry-able HTTP errors with exponential backoff
- Timeout for requests
- Included response headers in debug log

## [0.3.2] - 2020-03-31

### Fixed

- Removed deprecated attributes, added missing test cases

## [0.3.1] - 2019-12-07

### Fixed

- pip install error when "requests" module was not already present

## [0.3.0] - 2019-12-04

### Added

- Webhooks returns HTTP status code and headers. This allows the implementation of rate limit handling.

### Changed

- Webhook.execute() now returns a response object instead of the send report. The response objects contains the HTTP status code, headers and content of the response from Discord (e.g. send report)

- Webhook.execute() wil no longer throw an exception on non 2xx HTTP codes. Instead the application code needs to investigate the status code that is returned. It will still through exceptions on all network related issues.

## [0.2.0] - 2019-11-12

### Added

- Initial
